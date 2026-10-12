# Hands-On with Rumoca

AMC 2026 · Georgia Tech · October 12 · 10:00–13:00
**James Goppert** · Managing Director, PURT; Research Assistant Professor
**Micah Condie** · PhD student, School of Aeronautics and Astronautics
Purdue University

**[Open the core Codespace](https://codespaces.new/CogniPilot/rumoca_workshop_amc2026?quickstart=1)** ·
**[Slides](slides/workshop.pdf)** · **[Participant guide](docs/WORKSHOP.md)**

<a href="https://codespaces.new/CogniPilot/rumoca_workshop_amc2026?quickstart=1"><img src="slides/assets/repo-qr.png" width="180" alt="Scan to create the core workshop Codespace"></a>

Scan or click the QR to create the **core workshop Codespace**.

One Modelica model. Simulate it, fit its drag with JAX, then plan a trajectory
with CasADi. No aerospace background or AI assistant needed.

```python
import rumoca as rum
model = rum.Session().load("models/Quadrotor.mo", model="Quadrotor")
jax_model = model.to_jax()
casadi_model = model.to_casadi()
```

Start with [Quadrotor.mo](models/Quadrotor.mo). The three Python examples contain
these Session calls directly:

1. [simulate.py](examples/simulate.py) — integrate Rumoca's JAX dynamics and plot.
2. [fit_drag_jax.py](examples/fit_drag_jax.py) — differentiate a fit through those dynamics.
3. [optimize_casadi.py](examples/optimize_casadi.py) — export the same model to CasADi and optimize.

In the VS Code terminal:

```sh
uv run --frozen python examples/simulate.py
uv run --frozen python examples/fit_drag_jax.py
uv run --frozen python examples/optimize_casadi.py
```

Open plots in `results/live/`, or use **Terminal → Run Task**.
The [guide](docs/WORKSHOP.md) walks through simulation configuration, expected
results and the exercises. [Local setup](docs/LOCAL_SETUP.md) and
[recovery](docs/TROUBLESHOOTING.md) are available if needed.

The Explorer shows all workshop sources, including `templates/`, `formal/`,
`scripts/`, `docs/` and reference results. Only Git internals, the Python
environment and compiler caches are hidden. Pulling the latest workspace
settings applies this view in existing Codespaces without a container rebuild.
Markdown preview:
Ctrl+Shift+V (Linux/Windows), Cmd+Shift+V (Mac). Open the PDF for slides.

After the core: [browser experiments](docs/BROWSER_APPS.md),
[open challenge](docs/CHALLENGE.md), [custom targets](docs/BACKENDS.md),
[FMU / eFMU export](docs/EXPORTS.md),
[optional FastDyn/QEMU Codespace](docs/FASTDYN.md),
[optional coding agents](docs/AGENT_SETUP.md).
The upcoming [PURT pylon racing competition](https://pylon-racing.geddes.rcac.purdue.edu/)
will leverage Rumoca.

[Join the research community](docs/COMMUNITY.md) ·
[Mathematics and proof scope](docs/MATH_REVIEW.md) ·
[Test evidence](docs/VERIFICATION.md) ·
[User guide](https://cognipilot.github.io/rumoca/user-guide/)
