"""Rehearse the real workflow and check numerical acceptance criteria."""
from __future__ import annotations
import argparse
import platform
import subprocess
import sys
import time
from common import *


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def backend_checks():
    import jax
    import jax.numpy as jnp
    _, j = compile_model("jax")
    _, c = compile_model("casadi")
    require(j.parameter_names == c.parameter_names, "same backend parameter layout")
    p = parameters(j, **TRUTH_DRAG)
    rng = np.random.default_rng(4)
    max_error = 0
    for _ in range(20):
        x = rng.normal(size=6)
        u = np.array([rng.uniform(5, 18), rng.uniform(-0.1, 0.1)])
        a = np.asarray(j.rhs(0., jnp.array(x), jnp.array(u), jnp.array(p)))
        b = np.array(c.rhs(0., x, u, p)).ravel()
        max_error = max(max_error, float(np.max(np.abs(a-b))))
    require(max_error < 1e-10, "JAX/CasADi generated RHS parity at 20 physical states")
    hover = np.array([p[j.parameter_names.index("m")]*p[j.parameter_names.index("g")], 0])
    equilibrium = np.asarray(j.rhs(0., jnp.array([0., 1., 0., 0., 0., 0.]), jnp.array(hover), jnp.array(p)))
    require(np.max(np.abs(equilibrium)) < 1e-12, "stationary hover is an equilibrium")
    # Validate differentiation numerically; finite differences used only as a check.
    roll = jax_rollout(j)
    x0, controls = maneuver(j, vx0=3.0, seconds=2)
    idx = j.parameter_names.index("k_quad")
    f = lambda k: roll(jnp.array(p).at[idx].set(k), jnp.array(x0), jnp.array(controls))[-1, 0]
    ad = float(jax.grad(f)(0.08))
    fd = float((f(0.080001)-f(0.079999))/0.000002)
    require(abs(ad-fd) < 1e-5*max(1., abs(fd)), "JAX rollout gradient matches central difference")
    require(ad < 0, "more quadratic drag reduces travelled distance")
    return {"max_rhs_parity_error": max_error, "jax_gradient": ad, "finite_difference": fd}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    dest = output_dir(args.output).resolve()
    started = time.perf_counter()
    checks = backend_checks()
    command_times = {}
    for script in ["simulate", "fit_drag_jax", "optimize_casadi"]:
        t = time.perf_counter()
        subprocess.run([sys.executable, str(ROOT / f"scripts/{script}.py"), "--output", str(dest)],
                       cwd=ROOT, check=True, timeout=90)
        command_times[script] = time.perf_counter()-t
        require(command_times[script] < 60, f"{script} finishes within 60 seconds")
    sim = json.loads((dest / "simulation.json").read_text())
    fit = json.loads((dest / "fit_drag.json").read_text())
    opt = json.loads((dest / "optimization.json").read_text())
    truth = json.loads((ROOT / "data/truth.json").read_text())["drag"]
    require(sim["final_x_quadratic"] < sim["final_x_linear"], "quadratic drag shortens response")
    require(fit["success"] and fit["loss_reduction"] > 100, "drag fit converges and reduces loss >100x")
    for name in truth:
        require(abs(fit["drag"][name]/truth[name]-1) < 0.1, f"{name} recovered within 10%")
    require(fit["sensitivity_condition_number"] < 50, "drag sensitivities sufficiently distinct for this dataset")
    require(fit["noise_scaled_rms"]["validation_after"] < 1.5, "dimensionless holdout RMS below 1.5 measurement-noise scales")
    require(fit["noise_scaled_rms"]["validation_after"] < fit["noise_scaled_rms"]["validation_before"], "fit improves a flight excluded from optimization")
    require(opt["success"] and opt["max_dynamics_defect"] < 1e-6, "IPOPT solves dynamics constraints")
    require(opt["terminal_max_error"] < 1e-6, "terminal hover constraints hold")
    state_units = dict(zip(STATE_NAMES, ["m", "m", "rad", "m/s", "m/s", "rad/s"]))
    for name, error in opt["fine_rollout_terminal_error_by_state"].items():
        require(abs(error) < 0.02, f"4x finer rollout terminal {name} error below 0.02 {state_units[name]}")
    require(opt["thrust_range"][0] >= -1e-6 and opt["thrust_range"][1] <= 20.000001, "thrust bounds hold")
    require(max(abs(v) for v in opt["torque_range"]) <= 0.350001, "torque bounds hold")
    require(opt["rotor_pair_force_range"][0] >= -1e-6 and opt["rotor_pair_force_range"][1] <= 10.000001, "rotor pair forces are nonnegative and within capacity")
    require(opt["pitch_abs_max"] <= 0.540001 and opt["fine_pitch_abs_max"] <= 0.550001, "pitch bounds hold at nodes and finer rollout")
    require(opt["fine_altitude_range"][0] >= 0.249 and opt["fine_altitude_range"][1] <= 4.001, "altitude bounds hold in finer rollout")
    require(opt["drag"] == fit["drag"], "CasADi consumes the JAX-identified coefficients")
    require(len({r["source_sha256"] for r in [sim, fit, opt]}) == 1, "all examples compile the identical Modelica source")
    for name in ["simulation.png", "fit_drag.png", "optimization.png", "trajectory.csv", "trajectory.npz"]:
        require((dest / name).stat().st_size > 100, f"{name} generated")
    write_json(dest / "smoke.json", {"status": "PASS", "platform": platform.platform(),
               "python": platform.python_version(), "processor": platform.processor(),
               "rumoca_version": rm.version(), "source_sha256": source_hash(),
               "command_wall_seconds": command_times, "checks": checks,
               "total_seconds": time.perf_counter()-started})
    print(f"WORKSHOP PASS: {time.perf_counter()-started:.2f}s total")


if __name__ == "__main__":
    main()
