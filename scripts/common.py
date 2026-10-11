"""Compiler bridge and numerical helpers. All physics comes from Modelica."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

# CPU works on attendee laptops. Set before any JAX / BLAS import.
os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("MPLBACKEND", "Agg")

import numpy as np
import rumoca as rm

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models" / "Quadrotor.mo"
STATE_NAMES = ["x", "z", "theta", "vx", "vz", "omega"]
TRUTH_DRAG = {"k_linear": 0.18, "k_quad": 0.08}
DT = 0.05


def compile_model(backend="jax"):
    model = rm.Session().load(str(MODEL), model="Quadrotor")
    export = model.to_jax() if backend == "jax" else model.to_casadi()
    # Fail clearly if a release changes ordering; never guess vector positions.
    if export.state_names != STATE_NAMES or export.input_names != ["T", "tau"]:
        raise RuntimeError(f"Unexpected generated layout: {export}")
    return model, export


def parameters(export, **overrides):
    values = np.array(export.default_parameters, dtype=float)
    for name, value in overrides.items():
        values[export.parameter_names.index(name)] = value
    return values


def rk4(rhs, t, x, u, p, dt=DT):
    """Integration only: no handwritten vehicle dynamics in Python."""
    k1 = rhs(t, x, u, p)
    k2 = rhs(t + dt/2, x + dt*k1/2, u, p)
    k3 = rhs(t + dt/2, x + dt*k2/2, u, p)
    k4 = rhs(t + dt, x + dt*k3, u, p)
    return x + dt*(k1 + 2*k2 + 2*k3 + k4)/6


def jax_rollout(export, dt=DT):
    import jax
    import jax.numpy as jnp

    def rollout(p, x0, controls):
        def step(x, tu):
            t, u = tu
            y = rk4(export.rhs, t, x, u, p, dt)
            return y, y
        _, ys = jax.lax.scan(step, x0, (jnp.arange(len(controls))*dt, controls))
        return jnp.concatenate((x0[None, :], ys), axis=0)
    return jax.jit(rollout)


def maneuver(export, *, amplitude=0.23, frequency=0.8, vx0=0.4, seconds=8):
    """Prescribed input experiment; feedforward pitch excitation, not a plant."""
    p = dict(zip(export.parameter_names, export.default_parameters))
    t = np.arange(round(seconds/DT))*DT
    theta = amplitude*np.sin(frequency*t)
    T = p["m"]*p["g"]/np.cos(theta)*(1 + 0.05*np.sin(1.3*t))
    tau = (-p["Iyy"]*amplitude*frequency**2*np.sin(frequency*t)
           + p["damping"]*amplitude*frequency*np.cos(frequency*t))
    x0 = np.array([0., 1., 0., vx0, 0., amplitude*frequency])
    return x0, np.column_stack((T, tau))


def output_dir(path=None):
    dest = Path(path) if path else ROOT / "results" / "live"
    dest.mkdir(parents=True, exist_ok=True)
    return dest


def source_hash():
    return hashlib.sha256(MODEL.read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def plot_style():
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 12, "axes.spines.top": False,
                         "axes.spines.right": False, "figure.dpi": 130,
                         "axes.prop_cycle": plt.cycler(color=["#007c91", "#d65a31", "#4c956c", "#6b5b95"])})
