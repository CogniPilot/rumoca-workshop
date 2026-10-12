"""Move between hovers with bounded controls using the fitted Modelica plant."""
from __future__ import annotations
import argparse
import time
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import (ROOT, MODEL, STATE_NAMES, parameters, rk4, output_dir, plot_style, source_hash, write_json, validate_layout)
import numpy as np
import json
import hashlib
import rumoca as rm


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fit", type=Path, help="Defaults to OUTPUT/fit_drag.json; run the JAX fit first")
    parser.add_argument("--target-x", type=float, default=4.0)
    args = parser.parse_args()
    start = time.perf_counter()
    import casadi as ca
    dest = output_dir(args.output)
    fit_file = args.fit or dest / "fit_drag.json"
    if not fit_file.exists():
        raise SystemExit("Run fit_drag_jax.py first, or pass --fit results/reference/fit_drag.json")
    fit = json.loads(fit_file.read_text())
    if fit["source_sha256"] != source_hash():
        raise SystemExit("Model changed since fit. Re-run the JAX fit before optimizing.")
    model = rm.Session().load(str(MODEL), model="Quadrotor")
    export = model.to_casadi()
    validate_layout(export)
    p = parameters(export, **fit["drag"])
    hover = p[export.parameter_names.index("m")]*p[export.parameter_names.index("g")]
    n, dt = 60, 0.1
    initial = np.array([0., 1., 0., 0., 0., 0.])
    target = np.array([args.target_x, 2., 0., 0., 0., 0.])
    opti = ca.Opti()
    X, U = opti.variable(6, n+1), opti.variable(2, n)
    opti.subject_to(X[:, 0] == initial)
    opti.subject_to(X[:, -1] == target)
    opti.subject_to(opti.bounded(0.25, X[1, :], 4.0))
    # A 0.01-rad margin leaves room for between-node integration error.
    opti.subject_to(opti.bounded(-0.54, X[2, :], 0.54))
    opti.subject_to(opti.bounded(0., U[0, :], 20.0))
    opti.subject_to(opti.bounded(-0.35, U[1, :], 0.35))
    # Illustrative rotor pairs at +/- 0.2 m, each pair capable of 10 N.
    # This also prevents physically impossible torque at zero total thrust.
    arm = 0.2
    pair_left = (U[0, :] + U[1, :]/arm)/2
    pair_right = (U[0, :] - U[1, :]/arm)/2
    opti.subject_to(opti.bounded(0., pair_left, 10.))
    opti.subject_to(opti.bounded(0., pair_right, 10.))
    cost = 0
    for k in range(n):
        opti.subject_to(X[:, k+1] == rk4(export.rhs, k*dt, X[:, k], U[:, k], p, dt))
        error = X[:, k]-target
        # Dimensionless cost: reference units 1 m, 1 m/s, 10 N, 0.35 N*m,
        # 1 rad, and 1 s. Weights express tradeoffs, not quantities with mixed units.
        cost += dt*(0.3*ca.sumsqr(error[:2]/1.0) + 0.03*ca.sumsqr(error[3:5]/1.0)
                    + 2*((U[0, k]-hover)/10)**2
                    + 0.3675*(U[1, k]/0.35)**2 + 0.02*(X[2, k]/1.0)**2)
        if k > 0:
            cost += 0.5*((U[0, k]-U[0, k-1])/10)**2 + 0.0006125*((U[1, k]-U[1, k-1])/0.35)**2
    opti.minimize(cost)
    # A stored successful primal solution is used when it matches this problem.
    warm_file = ROOT / "results/reference/trajectory.npz"
    warm_used = False
    if warm_file.exists() and args.target_x == 4.0:
        with np.load(warm_file) as warm:
            if warm["X"].shape == (6, n+1):
                opti.set_initial(X, warm["X"])
                opti.set_initial(U, warm["U"])
                warm_used = True
    if not warm_used:
        opti.set_initial(X, initial[:, None] + (target-initial)[:, None]*np.linspace(0, 1, n+1))
        opti.set_initial(U, np.vstack((np.full(n, hover), np.zeros(n))))
    opti.solver("ipopt", {"expand": True, "print_time": False},
                {"print_level": 0, "max_iter": 500, "tol": 1e-8})
    solution = opti.solve()
    xs, us = solution.value(X), solution.value(U)
    defects = [np.max(np.abs(xs[:, k+1]-np.array(rk4(export.rhs, k*dt, xs[:, k], us[:, k], p, dt)).ravel())) for k in range(n)]
    # A 4x finer RK4 rollout checks beyond NLP nodes. math_audit.py also uses DOP853.
    fine = [initial]
    for k in range(n):
        for j in range(4):
            fine.append(np.array(rk4(export.rhs, k*dt+j*dt/4, fine[-1], us[:, k], p, dt/4)).ravel())
    fine = np.array(fine)
    fine_error = float(np.max(np.abs(fine[-1]-target)))
    stats = solution.stats()
    np.savez(dest / "trajectory.npz", X=xs, U=us, p=p, dt=dt)
    np.savetxt(dest / "trajectory.csv", np.column_stack((np.arange(n+1)*dt, xs.T)),
               delimiter=",", header="time,"+",".join(STATE_NAMES), comments="")
    plot_style()
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2, 2, figsize=(11, 7), layout="constrained")
    axs[0, 0].plot(xs[0], xs[1], lw=3)
    axs[0, 0].scatter([initial[0], target[0]], [initial[1], target[1]], s=70, zorder=3)
    axs[0, 0].set(xlabel="Horizontal position [m]", ylabel="Altitude [m]", title="Bounded flight between two hovers")
    t = np.arange(n+1)*dt
    axs[0, 1].plot(t, xs[3], label="vx")
    axs[0, 1].plot(t, xs[4], label="vz")
    axs[0, 1].set(xlabel="Time [s]", ylabel="Speed [m/s]", title="Arrive at rest")
    axs[0, 1].legend()
    axs[1, 0].step(t[:-1], us[0], where="post", label="thrust")
    axs[1, 0].axhline(20, ls="--", color="#d65a31", label="upper bound")
    axs[1, 0].axhline(0, ls="--", color="#d65a31")
    axs[1, 0].set(xlabel="Time [s]", ylabel="Thrust [N]", title="Input constraint")
    axs[1, 0].legend(fontsize=10)
    axs[1, 1].plot(t, xs[2], label="pitch [rad]")
    torque_ax = axs[1, 1].twinx()
    torque_ax.step(t[:-1], us[1], where="post", color="#d65a31", label="torque")
    torque_ax.set_ylabel("Torque [N m]", color="#d65a31")
    torque_ax.set_ylim(-0.45, 0.45)
    axs[1, 1].axhline(0.55, color="#555555", ls="--", label="pitch bounds ±0.55")
    axs[1, 1].axhline(-0.55, color="#555555", ls="--")
    axs[1, 1].set(xlabel="Time [s]", ylabel="Pitch [rad]", title="Tilt to accelerate, then brake")
    axs[1, 1].legend(fontsize=9)
    for ax in axs.flat:
        ax.grid(alpha=0.2)
    fig.savefig(dest / "optimization.png")
    plt.close(fig)
    report = {"success": bool(stats["success"]), "solver_status": stats["return_status"],
              "iterations": int(stats["iter_count"]), "cost": float(solution.value(cost)),
              "drag": fit["drag"], "horizon_seconds": n*dt, "shooting_intervals": n,
              "terminal_max_error": float(np.max(np.abs(xs[:, -1]-target))),
              "max_dynamics_defect": float(max(defects)), "fine_rollout_terminal_max_error": fine_error,
              "thrust_range": [float(us[0].min()), float(us[0].max())],
              "torque_range": [float(us[1].min()), float(us[1].max())],
              "rotor_pair_force_range": [float(min(solution.value(pair_left).min(), solution.value(pair_right).min())),
                                          float(max(solution.value(pair_left).max(), solution.value(pair_right).max()))],
              "pitch_abs_max": float(np.max(np.abs(xs[2]))),
              "altitude_range": [float(xs[1].min()), float(xs[1].max())],
              "fine_pitch_abs_max": float(np.max(np.abs(fine[:, 2]))),
              "pitch_node_limit": 0.54, "pitch_physical_limit": 0.55,
              "fine_rollout_terminal_error_by_state": dict(zip(STATE_NAMES, (fine[-1]-target).tolist())),
              "fine_altitude_range": [float(fine[:, 1].min()), float(fine[:, 1].max())],
              "warm_start_used": warm_used, "runtime_seconds": time.perf_counter()-start,
              "source_sha256": source_hash(), "fit_sha256": hashlib.sha256(fit_file.read_bytes()).hexdigest(),
              "rumoca_version": rm.version()}
    write_json(dest / "optimization.json", report)
    print(f"IPOPT: {report['solver_status']}; cost={report['cost']:.3f}; {report['runtime_seconds']:.2f}s")
    print(f"Terminal error {report['terminal_max_error']:.2e}; fine rollout {fine_error:.2e}; max defect {max(defects):.2e}")
    print(f"Saved {dest / 'optimization.png'}")


if __name__ == "__main__":
    main()
