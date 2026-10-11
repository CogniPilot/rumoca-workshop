"""Independent numerical oracles, robustness and profile-likelihood diagnostics.

Instructor/CI audit, not an attendee dependency. Dynamics are emitted by Rumoca.
Analytic formulae below are independent test oracles, not replacement backends.
"""
from __future__ import annotations
import argparse
import time
from common import *
from fit_drag_jax import load_flights


def adaptive(export, p, x0, commands, dt, samples=1):
    from scipy.integrate import solve_ivp
    states = [np.array(x0)]
    for k, u in enumerate(commands):
        ts = np.linspace(k*dt, (k+1)*dt, samples+1)[1:]
        sol = solve_ivp(lambda t, x: np.array(export.rhs(t, x, u, p)).ravel(),
                        (k*dt, (k+1)*dt), states[-1], t_eval=ts,
                        method="DOP853", rtol=1e-11, atol=1e-12)
        if not sol.success:
            raise RuntimeError(sol.message)
        states.extend(sol.y.T)
    return np.array(states)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT/"results/reference")
    args = parser.parse_args()
    start = time.perf_counter()
    import casadi as ca
    import jax
    import jax.numpy as jnp
    from scipy.optimize import minimize
    dest = output_dir(args.output)
    _, j = compile_model("jax")
    _, c = compile_model("casadi")
    p = parameters(j, **TRUTH_DRAG)
    roll = jax_rollout(j)
    m, inertia, damping = [p[j.parameter_names.index(n)] for n in ["m", "Iyy", "damping"]]
    hover = m*p[j.parameter_names.index("g")]
    # Analytic level coasting: k_quad=0, T=m*g, tau=0, vz=theta=0.
    coast_p = parameters(j, k_quad=0.)
    x0 = np.array([0., 1., 0., 6., 0., 0.])
    controls = np.tile([hover, 0.], (160, 1))
    numerical = np.array(roll(coast_p, x0, controls))
    ts = np.arange(161)*DT
    kl = coast_p[j.parameter_names.index("k_linear")]
    exact_v = 6*np.exp(-kl*ts/m)
    exact_x = 6*m/kl*(1-np.exp(-kl*ts/m))
    coast_error = {"x_m": float(np.max(abs(numerical[:, 0]-exact_x))),
                   "vx_m_s": float(np.max(abs(numerical[:, 3]-exact_v)))}
    assert max(coast_error.values()) < 1e-8, coast_error
    # Different AD implementations, including the smoothed zero-speed regime.
    y, u, cp = ca.MX.sym("y", 6), ca.MX.sym("u", 2), ca.MX.sym("p", 7)
    cj = ca.Function("audit_jac", [y, u, cp], [ca.jacobian(c.rhs(0, y, u, cp), y),
                                               ca.jacobian(c.rhs(0, y, u, cp), cp)])
    jj = jax.jit(jax.jacfwd(lambda y, u, p: j.rhs(0., y, u, p), argnums=(0, 2)))
    rng = np.random.default_rng(9001)
    parity = 0.
    for speed in [0., 1e-12, -1e-8, 0.01, -0.01, 1., -6., 12.]:
        state = rng.normal(size=6)
        state[3:5] = [speed, -speed]
        control = np.array([12., 0.04])
        ja, jb = jj(state, control, p)
        caa, cab = cj(state, control, p)
        parity = max(parity, float(np.max(abs(np.array(ja)-np.array(caa)))),
                     float(np.max(abs(np.array(jb)-np.array(cab)))))
    assert parity < 1e-10, parity
    # Joint identification objective, exactly the participant's observation model.
    train = [f for f in load_flights(ROOT/"data/noisy_flight.csv") if f["split"] == "train"]
    ys = jnp.array(np.stack([f["y"] for f in train]))
    us = jnp.array(np.stack([f["u"] for f in train]))
    ids = jnp.array([j.parameter_names.index(n) for n in ["k_linear", "k_quad"]])
    obs = jnp.array([0, 1, 3, 4])
    sigma = jnp.array([.025, .025, .035, .035])
    def residual(logp, data):
        pars = jnp.array(p).at[ids].set(jnp.exp(logp))
        pred = jax.vmap(roll, in_axes=(None, 0, 0))(pars, data[:, 0], us)
        return ((pred[:, 1:, obs]-data[:, 1:, obs])/sigma).reshape(-1)
    value_grad = jax.jit(jax.value_and_grad(lambda a, data: jnp.mean(residual(a, data)**2)))
    def fit(initial, data):
        def fun(a):
            value, grad = value_grad(a, data)
            return float(value), np.array(grad)
        result = minimize(fun, np.log(initial), jac=True, method="L-BFGS-B",
                          bounds=[(np.log(.001), np.log(2.))]*2,
                          options={"maxiter": 150, "maxls": 50, "ftol": 1e-11, "gtol": 1e-6})
        assert result.success, (initial, result.message, result.x, result.jac)
        return result
    starts = [[.006, .006], [.06, .025], [.8, .4], [.02, .5], [1., .002], [.18, .08]]
    multi = [fit(s, ys) for s in starts]
    estimates = np.array([np.exp(r.x) for r in multi])
    assert np.max(np.ptp(estimates, axis=0)) < 1e-5, estimates
    best = min(multi, key=lambda r: r.fun)
    # Direct central differences of the full noise-scaled objective at two points.
    gradient_errors = []
    for point in [np.log([.06, .025]), best.x + [.01, -.01]]:
        _, ad = value_grad(point, ys)
        fd = np.array([(float(value_grad(point+np.eye(2)[i]*1e-5, ys)[0])-
                        float(value_grad(point-np.eye(2)[i]*1e-5, ys)[0]))/2e-5 for i in range(2)])
        error = float(np.max(abs(np.array(ad)-fd)/(1+abs(fd))))
        assert error < 1e-5, error
        gradient_errors.append(error)
    clean = np.array([adaptive(c, p, np.array(f["y"])[0], f["u"], DT) for f in train])
    noise = np.array([.025, .025, .001, .035, .035, .003])
    seed_estimates = []
    for seed in range(12):
        data = clean + np.random.default_rng(seed).normal(size=clean.shape)*noise
        data[:, 0] = clean[:, 0]
        result = fit([.06, .025], jnp.array(data))
        seed_estimates.append(np.exp(result.x))
    seed_estimates = np.array(seed_estimates)
    truth = np.array([TRUTH_DRAG["k_linear"], TRUTH_DRAG["k_quad"]])
    max_recovery_error = float(np.max(abs(seed_estimates/truth-1)))
    assert max_recovery_error < .1, seed_estimates
    # Profile: fix one log coefficient, re-optimize the other. Not a 2D slice.
    sensitivity = np.array(jax.jit(jax.jacfwd(residual))(best.x, ys))
    local_std = np.sqrt(np.diag(np.linalg.inv(sensitivity.T@sensitivity)))
    nres = sensitivity.shape[0]
    profiles = []
    for fixed in range(2):
        grid = best.x[fixed] + np.linspace(-5, 5, 31)*local_std[fixed]
        prof = []
        for v in grid:
            def fun(free):
                a = np.array(best.x)
                a[fixed], a[1-fixed] = v, free[0]
                value, grad = value_grad(a, ys)
                return float(value), np.array([grad[1-fixed]], float)
            result = minimize(fun, [best.x[1-fixed]], jac=True, method="L-BFGS-B",
                              bounds=[(np.log(.001), np.log(2.))],
                              options={"maxls": 50, "ftol": 1e-11, "gtol": 1e-6})
            assert result.success, result.message
            prof.append(max(0., nres*(result.fun-best.fun)))
        assert prof[0] > 3.841 and prof[-1] > 3.841, prof
        profiles.append({"parameter": ["k_linear", "k_quad"][fixed],
                         "grid": np.exp(grid).tolist(), "delta_chi_square": prof,
                         "scope": "Finite-grid conditional Gaussian profile diagnostic; asymptotic threshold, not certified confidence coverage."})
    # Truly independent adaptive integration of the optimized open-loop inputs.
    with np.load(dest/"trajectory.npz") as trajectory:
        xs, inputs, pars, dt = [trajectory[n] for n in ["X", "U", "p", "dt"]]
        dt = float(dt)
    dense = adaptive(c, pars, xs[:, 0], inputs.T, dt, samples=10)
    terminal = dense[-1]-xs[:, -1]
    # On each constant-torque interval, analytically locate pitch extrema.
    # Angular ODE is linear: omega'=tau/I - (d/I)*omega.
    extrema = []
    rate = damping/inertia
    for k, torque in enumerate(inputs[1]):
        theta0, omega0 = dense[k*10, [2, 5]]
        steady = torque/damping
        candidates = [0., dt]
        if omega0 != steady:
            ratio = -steady/(omega0-steady)
            if ratio > 0:
                tcrit = -np.log(ratio)/rate
                if 0 < tcrit < dt:
                    candidates.append(tcrit)
        extrema.extend(theta0+steady*t+(omega0-steady)*(1-np.exp(-rate*t))/rate for t in candidates)
    pitch_max = float(np.max(abs(np.array(extrema))))
    assert pitch_max < .55, pitch_max
    assert np.max(abs(terminal)) < .02, terminal
    assert .25 < dense[:, 1].min() and dense[:, 1].max() < 4.
    plot_style()
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 3, figsize=(13, 4), layout="constrained")
    for ax, profile in zip(axs[:2], profiles):
        ax.plot(profile["grid"], profile["delta_chi_square"])
        ax.axhline(3.841, ls="--", color="#d65a31", label="nominal 95% threshold")
        ax.set(xlabel=profile["parameter"], ylabel="Profile Δχ²", title="Re-optimize the other coefficient")
        ax.legend(fontsize=8)
    axs[2].scatter(seed_estimates[:, 0], seed_estimates[:, 1], label="12 independent noise seeds")
    axs[2].scatter(*truth, marker="*", s=140, label="synthetic truth")
    axs[2].set(xlabel="Linear drag [N s/m]", ylabel="Quadratic drag [N s²/m²]", title="Recovery under repeated noise")
    axs[2].legend(fontsize=8)
    fig.savefig(dest/"math_audit.png")
    plt.close(fig)
    write_json(dest/"math_audit.json", {
        "status": "PASS", "source_sha256": source_hash(), "rumoca_version": rm.version(),
        "coast_analytic_max_error": coast_error, "backend_jacobian_max_error": parity,
        "full_loss_gradient_relative_errors": gradient_errors,
        "multi_start_initial_parameters": starts, "multi_start_estimates": estimates.tolist(),
        "noise_seeds": list(range(12)), "noise_seed_estimates": seed_estimates.tolist(),
        "noise_max_relative_coefficient_error": max_recovery_error, "profiles": profiles,
        "adaptive_trajectory_terminal_error_by_state": dict(zip(STATE_NAMES, terminal.tolist())),
        "adaptive_pitch_abs_max": float(np.max(abs(dense[:, 2]))),
        "analytic_interval_pitch_abs_max": pitch_max,
        "adaptive_altitude_range": [float(dense[:, 1].min()), float(dense[:, 1].max())],
        "trajectory_check": "Generated CasADi RHS, DOP853 rtol=1e-11 atol=1e-12, 10 samples/interval; analytic pitch extrema. Numerical evidence, not interval arithmetic certification.",
        "runtime_seconds": time.perf_counter()-start})
    print(f"MATH AUDIT PASS: 6 starts, 12 noise seeds, profiles, analytic coast, AD parity, adaptive optimized flight; {time.perf_counter()-start:.2f}s")


if __name__ == "__main__":
    main()
