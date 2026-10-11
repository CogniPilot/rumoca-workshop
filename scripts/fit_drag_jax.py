"""Fit positive drag parameters with JAX gradients through Rumoca dynamics."""
from __future__ import annotations
import argparse
import csv
import time
from common import *


def load_flights(path):
    with Path(path).open(newline="") as f:
        rows = list(csv.DictReader(f))
    flights = []
    for flight_id in sorted({int(row["flight"]) for row in rows}):
        group = [row for row in rows if int(row["flight"]) == flight_id]
        ts = np.array([float(row["time"]) for row in group])
        if not np.allclose(np.diff(ts), DT):
            raise ValueError(f"Flight {flight_id} must have fixed dt={DT}")
        flights.append({"id": flight_id, "split": group[0]["split"], "t": ts,
                        "u": np.array([[float(row[n]) for n in ["T", "tau"]] for row in group[:-1]]),
                        "y": np.array([[float(row[n]) for n in STATE_NAMES] for row in group])})
    return flights


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--data", type=Path, default=ROOT / "data/noisy_flight.csv")
    parser.add_argument("--one-coefficient", action="store_true", help="Hold linear drag fixed; fit quadratic only")
    args = parser.parse_args()
    started = time.perf_counter()
    import jax
    import jax.numpy as jnp
    from scipy.optimize import minimize

    _, export = compile_model()
    rollout = jax_rollout(export)
    flights = load_flights(args.data)
    train = [f for f in flights if f["split"] == "train"]
    validation = [f for f in flights if f["split"] == "validation"]
    if not train or not validation:
        raise ValueError("Provide separate training and validation flights")
    names = ["k_quad"] if args.one_coefficient else ["k_linear", "k_quad"]
    indices = jnp.array([export.parameter_names.index(n) for n in names])
    # The one-parameter recovery path assumes linear drag is known.
    base = jnp.array(parameters(export, k_linear=0.18))
    initial = np.array([0.025] if args.one_coefficient else [0.06, 0.025])
    obs = jnp.array([0, 1, 3, 4])
    sigma = jnp.array([0.025, 0.025, 0.035, 0.035])
    u_train = jnp.array(np.stack([f["u"] for f in train]))
    y_train = jnp.array(np.stack([f["y"] for f in train]))

    def p_from_log(log_drag):
        return base.at[indices].set(jnp.exp(log_drag))

    def predictions(log_drag):
        return jax.vmap(rollout, in_axes=(None, 0, 0))(
            p_from_log(log_drag), y_train[:, 0, :], u_train)

    def residual(log_drag):
        return ((predictions(log_drag)[:, 1:, obs]-y_train[:, 1:, obs])/sigma).reshape(-1)

    @jax.jit
    def loss_grad(log_drag):
        return jax.value_and_grad(lambda v: jnp.mean(residual(v)**2))(log_drag)

    history = []
    def objective(log_drag):
        value, gradient = loss_grad(jnp.array(log_drag))
        history.append(float(value))
        return float(value), np.asarray(gradient, dtype=float)

    log_initial = np.log(initial)
    initial_loss, _ = objective(log_initial)
    result = minimize(objective, log_initial, method="L-BFGS-B", jac=True,
                      bounds=[(np.log(0.001), np.log(2.0))]*len(names),
                      options={"maxiter": 80, "ftol": 1e-12, "gtol": 1e-7})
    if not result.success:
        raise RuntimeError(f"Drag fit failed: {result.message}")
    fitted = dict(zip(names, np.exp(result.x).tolist()))
    if args.one_coefficient:
        fitted["k_linear"] = 0.18
    before_p = np.array(p_from_log(log_initial))
    after_p = np.array(p_from_log(result.x))
    # Scaled trajectory sensitivity of log parameters; report conditioning.
    sensitivity = np.asarray(jax.jit(jax.jacfwd(residual))(jnp.array(result.x)))
    singular = np.linalg.svd(sensitivity, compute_uv=False)
    conditioning = float(singular[0]/singular[-1])
    rms = {}
    predictions_by_flight = []
    for flight in flights:
        before = np.asarray(rollout(before_p, flight["y"][0], flight["u"]))
        after = np.asarray(rollout(after_p, flight["y"][0], flight["u"]))
        predictions_by_flight.append((flight, before, after))
    for split in ["train", "validation"]:
        group = [item for item in predictions_by_flight if item[0]["split"] == split]
        for label, idx in [("before", 1), ("after", 2)]:
            errors = np.concatenate([item[idx][1:, [0, 1, 3, 4]]-item[0]["y"][1:, [0, 1, 3, 4]] for item in group])
            rms[f"{split}_{label}"] = float(np.sqrt(np.mean(errors**2)))

    dest = output_dir(args.output)
    plot_style()
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2, 2, figsize=(11, 7), layout="constrained")
    axs[0, 0].semilogy(history)
    axs[0, 0].set(xlabel="Objective evaluation", ylabel="Noise-scaled mean square loss", title="JAX gradients guide the fit")
    labels = ["linear [N s/m]", "quadratic [N s²/m²]"]
    truth = json.loads((ROOT / "data/truth.json").read_text())["drag"]
    xpos = np.arange(2)
    axs[0, 1].bar(xpos-0.17, [truth[n] for n in ["k_linear", "k_quad"]], 0.34, label="synthetic truth")
    axs[0, 1].bar(xpos+0.17, [fitted[n] for n in ["k_linear", "k_quad"]], 0.34, label="estimated")
    axs[0, 1].set_xticks(xpos, labels)
    axs[0, 1].set_title("Recover both physical coefficients")
    axs[0, 1].legend()
    for ax, item in zip(axs[1], [predictions_by_flight[2], predictions_by_flight[-1]]):
        flight, before, after = item
        ax.scatter(flight["t"][::3], flight["y"][::3, 3], s=10, color="#555555", alpha=0.6, label="noisy velocity")
        ax.plot(flight["t"], before[:, 3], "--", label="before")
        ax.plot(flight["t"], after[:, 3], label="after")
        ax.set(xlabel="Time [s]", ylabel="Horizontal speed [m/s]", title=f"Flight {flight['id']}: {flight['split']}")
        ax.legend(fontsize=10)
    for ax in axs.flat:
        ax.grid(alpha=0.2)
    fig.savefig(dest / "fit_drag.png")
    plt.close(fig)
    report = {"drag": fitted, "initial_drag": dict(zip(names, initial.tolist())),
              "initial_loss": initial_loss, "final_loss": float(result.fun),
              "loss_reduction": initial_loss/float(result.fun), "rms": rms,
              "sensitivity_condition_number": conditioning,
              "sensitivity_singular_values": singular.tolist(),
              "optimizer": "L-BFGS-B, JAX autodiff through generated RHS + RK4 scan; log-positive parameters",
              "iterations": int(result.nit), "success": bool(result.success),
              "runtime_seconds": time.perf_counter()-started,
              "source_sha256": source_hash(), "data_sha256": hashlib.sha256(args.data.read_bytes()).hexdigest(),
              "rumoca_version": rm.version()}
    write_json(dest / "fit_drag.json", report)
    print(f"Drag estimates: linear={fitted['k_linear']:.5f}, quadratic={fitted['k_quad']:.5f}")
    print(f"Loss {initial_loss:.2f} -> {result.fun:.3f}; holdout RMS {rms['validation_before']:.3f} -> {rms['validation_after']:.3f}")
    print(f"Sensitivity condition number {conditioning:.2f}; {report['runtime_seconds']:.2f}s")
    print(f"Saved {dest / 'fit_drag.png'} and fit_drag.json")


if __name__ == "__main__":
    main()
