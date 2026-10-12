"""Execute the custom target and check values, batching, AD and rejection gates."""
from common import *
from torch_backend import load_torch_backend
import time
import torch
import jax
import jax.numpy as jnp
import casadi as ca
import types


def check_time_broadcast():
    # This model exposes errors hidden by the autonomous vehicle example:
    # batched time must also expand derivatives that are independent of time.
    source = """model ClockedSlope
      Real x(start=0, fixed=true);
      Real y(start=0, fixed=true);
    equation
      der(x) = time;
      der(y) = 1;
    end ClockedSlope;"""
    generated = rm.Session().loads(source, model="ClockedSlope").codegen(str(ROOT / "templates/torch-ode"))
    backend = types.ModuleType("time_broadcast_probe")
    exec(compile(generated.files[0].content, "<Rumoca ClockedSlope>", "exec"), backend.__dict__)
    t = torch.tensor([0., .5, 2.], requires_grad=True)
    x, u, p = torch.zeros(2), torch.empty(0), torch.empty(0)
    fun = lambda time: backend.rhs(time, x, u, p)
    expected = torch.stack((t.detach(), torch.ones_like(t)), dim=-1)
    torch.testing.assert_close(fun(t), expected, rtol=0, atol=0)
    jac = torch.stack((torch.eye(3), torch.zeros((3, 3))), dim=1)
    torch.testing.assert_close(torch.func.jacrev(fun)(t), jac, rtol=0, atol=0)
    torch.testing.assert_close(torch.func.jacfwd(fun)(t), jac, rtol=0, atol=0)
    assert torch.autograd.gradcheck(fun, (t,), eps=1e-6, atol=1e-7, rtol=1e-5)
    mixed = backend.rhs(t, torch.zeros((2, 1, 2)), u, p)
    torch.testing.assert_close(mixed, expected.expand(2, 3, 2), rtol=0, atol=0)
    try:
        backend.rhs(t, torch.zeros((4, 2)), u, p)
    except RuntimeError:
        pass
    else:
        raise AssertionError("Incompatible time/state batches were silently accepted")
    return {"model": "ClockedSlope", "source": source,
            "batched_time_and_constant_derivative": True,
            "mixed_time_state_broadcast": True, "time_forward_reverse_ad": True,
            "time_gradcheck": True, "incompatible_batch_rejected": True}


def main():
    started = time.perf_counter()
    model, backend = load_torch_backend()
    time_broadcast = check_time_broadcast()
    j = model.to_jax()
    c = model.to_casadi()
    assert backend.STATE_NAMES == j.state_names == c.state_names == STATE_NAMES
    assert backend.PARAM_NAMES == j.parameter_names == c.parameter_names
    assert backend.INPUT_NAMES == j.input_names == c.input_names == ["T", "tau"]
    rng = np.random.default_rng(20261012)
    x = rng.uniform(-2, 2, (101, 6))
    x[0] = 0  # Include the smoothed zero-velocity point.
    u = rng.uniform([0, -.35], [20, .35], (101, 2))
    p = np.tile(np.array(j.default_parameters), (101, 1))
    p[:, j.parameter_names.index("k_quad")] = rng.uniform(0, .12, 101)
    actual = backend.rhs(0., torch.tensor(x), torch.tensor(u), torch.tensor(p)).detach().numpy()
    jax_values = np.asarray(jax.jit(jax.vmap(j.rhs, in_axes=(None, 0, 0, 0)))(0., x, u, p))
    casadi_values = np.array([np.asarray(c.rhs(0., xx, uu, pp)).ravel() for xx, uu, pp in zip(x, u, p)])
    np.testing.assert_allclose(actual, jax_values, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(actual, casadi_values, rtol=1e-12, atol=1e-12)
    one = backend.rhs(0., torch.tensor(x[1]), torch.tensor(u[1]), torch.tensor(p[1]))
    np.testing.assert_allclose(one.detach().numpy(), actual[1], rtol=1e-12, atol=1e-12)
    broadcast = backend.rhs(0., torch.tensor(x), torch.tensor(u[1]), torch.tensor(p[1]))
    assert broadcast.shape == (101, 6)
    jac_error = 0.
    for index in [0, 1, 50]:
        inputs = tuple(torch.tensor(a[index], requires_grad=True) for a in [x, u, p])
        fun = lambda xx, uu, pp: backend.rhs(0., xx, uu, pp)
        assert torch.autograd.gradcheck(fun, inputs, eps=1e-6, atol=1e-7, rtol=1e-5)
        reverse = torch.func.jacrev(fun, argnums=(0, 1, 2))(*inputs)
        forward = torch.func.jacfwd(fun, argnums=(0, 1, 2))(*inputs)
        j_jac = jax.jacfwd(j.rhs, argnums=(1, 2, 3))(0., x[index], u[index], p[index])
        sx, su, sp = ca.MX.sym("x", 6), ca.MX.sym("u", 2), ca.MX.sym("p", backend.N_P)
        cf = c.rhs(0., sx, su, sp)
        cfun = ca.Function("torchParityJac", [sx, su, sp], [ca.jacobian(cf, a) for a in [sx, su, sp]])
        cj = cfun(x[index], u[index], p[index])
        for r, f, jj, cc in zip(reverse, forward, j_jac, cj):
            rr = r.detach().numpy()
            np.testing.assert_allclose(rr, f.detach().numpy(), rtol=1e-11, atol=1e-11)
            np.testing.assert_allclose(rr, np.asarray(jj), rtol=1e-11, atol=1e-11)
            np.testing.assert_allclose(rr, np.asarray(cc), rtol=1e-11, atol=1e-11)
            jac_error = max(jac_error, float(np.max(np.abs(rr - np.asarray(jj)))))
    rejected = []
    for name, source in [
        ("unsupported unary Exp", "model Unsupported Real x(start=1, fixed=true); equation der(x)=exp(x); end Unsupported;"),
        ("events", "model Unsupported Real x(start=0, fixed=true); equation der(x)=1; when x>1 then reinit(x,0); end when; end Unsupported;")]:
        try:
            rm.Session().loads(source, model="Unsupported").codegen(str(ROOT / "templates/torch-ode"))
        except Exception as exc:
            rejected.append({"case": name, "message": str(exc)[:500]})
        else:
            raise AssertionError(f"Teaching target silently accepted {name}")
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    report = {"status": "PASS", "rumoca": rm.version(), "torch": torch.__version__,
              "platform": "Linux x64 CPU", "source_sha256": source_hash(),
              "script_sha256": digest(Path(__file__)),
              "target_sha256": {p.name: digest(p) for p in (ROOT / "templates/torch-ode").iterdir()},
              "generated_sha256": digest(ROOT / "generated/torch-ode/Quadrotor_torch.py"),
              "state_names": backend.STATE_NAMES, "input_names": backend.INPUT_NAMES,
              "points": 101, "value_max_abs_difference": float(np.max(np.abs(actual-jax_values))),
              "jacobian_max_abs_difference": jac_error, "finite_difference_gradcheck": True,
              "forward_reverse_ad": True, "negative_tests": rejected,
              "time_broadcast": time_broadcast,
              "elapsed_seconds": time.perf_counter()-started,
              "scope": "Small teaching target for explicit scalar ODEs with the listed primitives. Runtime/autograd checks for this model; no full Modelica, GPU or compiler-correctness claim."}
    write_json(output_dir() / "torch_backend.json", report)
    print(f"TORCH BACKEND PASS: {report['points']} points, batched RHS, JAX/CasADi parity, forward/reverse AD and rejection gates ({report['elapsed_seconds']:.1f} s)")


if __name__ == "__main__":
    main()
