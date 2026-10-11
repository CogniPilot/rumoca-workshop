"""Differentiate a small hover policy through the generated Torch vehicle.

Model-based policy optimization, restricted to vertical motion. This is an
RL bridge, not a trained full-flight controller or a model-free RL algorithm.
"""
from common import *
from torch_backend import load_torch_backend
import argparse
import time
import torch
import torch.nn.functional as F


def initial_states(seed, count):
    rng = np.random.default_rng(seed)
    x = np.zeros((count, 6))
    x[:, 1] = rng.uniform(.5, 1.5, count)
    x[:, 4] = rng.uniform(-.4, .4, count)
    return torch.tensor(x)


def rollout(backend, p, gains, x0, dt=.05, seconds=2., integration_substeps=1):
    """A dimensionless quadratic cost; all plant derivatives are generated."""
    x, states, controls, costs = x0, [x0], [], []
    mass = p[backend.PARAM_NAMES.index("m")]
    gravity = p[backend.PARAM_NAMES.index("g")]
    kp, kd = F.softplus(gains)
    for step in range(round(seconds/dt)):
        # z_ref=1 m. Scaling units: altitude 1 m, velocity 1 m/s, thrust 6 N.
        correction = 6*torch.tanh(kp*(1.-x[..., 1])-kd*x[..., 4])
        thrust = mass*gravity+correction
        u = torch.stack((thrust, torch.zeros_like(thrust)), dim=-1)
        # Keep the feedback sampling period fixed when refining integration.
        for substep in range(integration_substeps):
            h = dt/integration_substeps
            x = rk4(backend.rhs, step*dt+substep*h, x, u, p, h)
        costs.append((x[..., 1]-1.)**2 + .1*x[..., 4]**2 + .01*(correction/6)**2)
        states.append(x); controls.append(u)
    return torch.stack(costs).mean(), torch.stack(states), torch.stack(controls)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=60)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    assert args.iterations >= 1
    started = time.perf_counter()
    model, backend = load_torch_backend()
    export = model.to_jax()
    # Same declared model, fixed known coefficients for this separate task.
    p = torch.tensor(parameters(export, **TRUTH_DRAG))
    train = initial_states(20261012, 64)
    holdout = initial_states(20261013, 128)
    base = torch.full((2,), float(np.log(np.expm1(.05))))
    raw = torch.nn.Parameter(base.clone())
    optimizer = torch.optim.Adam([raw], lr=.12)
    loss_history = []
    for _ in range(args.iterations):
        optimizer.zero_grad()
        loss, _, _ = rollout(backend, p, raw, train)
        assert torch.isfinite(loss)
        loss.backward()
        assert torch.all(torch.isfinite(raw.grad))
        optimizer.step()
        loss_history.append(float(loss.detach()))
    # Check the complete discrete policy objective's gradient, not just RHS AD.
    probe = raw.detach().clone().requires_grad_()
    loss, _, _ = rollout(backend, p, probe, train[:8])
    ad = torch.autograd.grad(loss, probe)[0].detach().numpy()
    fd = []
    for index in range(2):
        offset = torch.zeros(2); offset[index] = 1e-5
        with torch.no_grad():
            plus = rollout(backend, p, probe+offset, train[:8])[0]
            minus = rollout(backend, p, probe-offset, train[:8])[0]
        fd.append(float((plus-minus)/2e-5))
    np.testing.assert_allclose(ad, fd, rtol=1e-4, atol=1e-8)
    with torch.no_grad():
        before, xb, _ = rollout(backend, p, base, holdout)
        after, xa, controls = rollout(backend, p, raw, holdout)
        _, fine, _ = rollout(backend, p, raw, holdout, integration_substeps=4)
    assert float(after) < .6*float(before), "No substantial held-out improvement"
    assert torch.max(torch.abs(xa[..., [0,2,3,5]])) < 1e-12
    fine_error = torch.max(torch.abs(xa-fine), dim=0).values.max(dim=0).values.numpy()
    assert fine_error[1] < .005 and fine_error[4] < .005
    dest = output_dir(args.output)
    report = {"status":"PASS", "source_sha256":source_hash(),
              "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "target_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in (ROOT/"templates/torch-ode").iterdir()},
              "rumoca":rm.version(), "torch":torch.__version__,
              "task":"Vertical hover at z=1 m, two positive feedback gains, zero torque",
              "method":"Differentiable model-based policy optimization through RK4, Adam",
              "training_seed":20261012, "holdout_seed":20261013,
              "training_episodes":64, "holdout_episodes":128,
              "iterations":args.iterations, "horizon_seconds":2., "dt_seconds":.05,
              "parameter_names":backend.PARAM_NAMES, "parameters":p.tolist(),
              "raw_gains":raw.detach().tolist(), "positive_gains":F.softplus(raw).detach().tolist(),
              "initial_positive_gains":[.05,.05], "loss_history":loss_history,
              "holdout_cost_before":float(before), "holdout_cost_after":float(after),
              "holdout_final_altitude_rms_m":float(torch.sqrt(torch.mean((xa[-1,:,1]-1.)**2))),
              "thrust_min_N":float(controls[...,0].min()), "thrust_max_N":float(controls[...,0].max()),
              "rollout_gradient_ad":ad.tolist(), "rollout_gradient_fd":fd,
              "fine_rollout_max_abs_error":dict(zip(STATE_NAMES,fine_error.tolist())),
              "elapsed_seconds":time.perf_counter()-started,
              "scope":"Synthetic fixed-parameter, two-second vertical task. Feedback optimized on 64 initial states and checked on 128 new states. No full-vehicle RL, disturbance robustness, continuous-time safety or physical-flight claim."}
    write_json(dest/"torch_policy.json", report)
    import matplotlib.pyplot as plt
    plot_style()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
    t = np.arange(xa.shape[0])*.05
    for states, name, color in [(xb,"Initial policy", "#627081"),(xa,"Learned policy", "#007E87")]:
        values = states[...,1].numpy()
        axes[0].plot(t, np.sqrt(np.mean((values-1.)**2,axis=1)),label=name,color=color,lw=2.5)
    axes[0].set(xlabel="Time [s]",ylabel="Held-out altitude RMS error [m]",title="128 new initial states")
    axes[0].legend()
    axes[1].plot(np.arange(1,len(loss_history)+1),loss_history,color="#345FB5",lw=2.5)
    axes[1].set(xlabel="Policy update",ylabel="Dimensionless training cost",title="Differentiate through the same vehicle")
    fig.savefig(dest/"torch_policy.png"); plt.close(fig)
    print(f"TORCH POLICY PASS: held-out cost {float(before):.4f} → {float(after):.4f}, gradient/fine-step checks, {report['elapsed_seconds']:.1f} s")


if __name__ == "__main__":
    main()
