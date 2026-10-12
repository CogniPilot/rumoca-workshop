"""Predict how adding quadratic drag changes a quadrotor's response."""
from __future__ import annotations
import argparse
import time
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import (MODEL, DT, jax_rollout, maneuver, parameters, output_dir, plot_style, source_hash, write_json, validate_layout)
import numpy as np
import json
import hashlib
import rumoca as rum


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.perf_counter()
    model = rum.Session().load(str(MODEL), model="Quadrotor")
    export = model.to_jax()
    validate_layout(export)
    rollout = jax_rollout(export)
    x0, u = maneuver(export, vx0=6.0)
    # Primary response honors the participant's current Modelica defaults.
    current = np.asarray(rollout(parameters(export), x0, u))
    linear = np.asarray(rollout(parameters(export, k_quad=0), x0, u))
    quadratic = np.asarray(rollout(parameters(export, k_quad=0.08), x0, u))
    t = np.arange(len(current))*DT
    dest = output_dir(args.output)
    plot_style()
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(11, 4), layout="constrained")
    for y, label, style in [(linear, "linear drag only", "--"),
                             (quadratic, "linear + quadratic (0.08)", "-"),
                             (current, "your Modelica defaults", ":")]:
        axs[0].plot(t, y[:, 3], style, label=label)
        axs[1].plot(t, y[:, 0], style, label=label)
    axs[0].set(xlabel="Time [s]", ylabel="Horizontal speed [m/s]", title="More drag removes speed faster")
    axs[1].set(xlabel="Time [s]", ylabel="Horizontal position [m]", title="The same commands travel less far")
    for ax in axs:
        ax.grid(alpha=0.2)
        ax.legend(fontsize=9)
    fig.savefig(dest / "simulation.png")
    plt.close(fig)
    report = {"rumoca_version": rum.version(), "source_sha256": source_hash(),
              "model_drag": dict(zip(["k_linear", "k_quad"],
                                  [float(parameters(export)[export.parameter_names.index(n)]) for n in ["k_linear", "k_quad"]])),
              "final_x_linear": float(linear[-1, 0]), "final_x_quadratic": float(quadratic[-1, 0]),
              "runtime_seconds": time.perf_counter()-started}
    write_json(dest / "simulation.json", report)
    print(f"Final x: linear {linear[-1,0]:.2f} m; quadratic {quadratic[-1,0]:.2f} m")
    print(f"Saved {dest / 'simulation.png'} ({report['runtime_seconds']:.2f}s)")


if __name__ == "__main__":
    main()
