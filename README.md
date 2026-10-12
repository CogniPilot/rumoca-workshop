# Hands-On with Rumoca

American Modelica Conference · Georgia Tech · October 12, 2026 · 10:00–13:00

**James Goppert · Micah Condie**
Purdue University · School of Aeronautics and Astronautics

**[Bring your model. Join the research community.](docs/COMMUNITY.md)**

**[Start here: participant walkthrough](docs/WORKSHOP.md)**

Declare a planar quadrotor once in Modelica. Use Rumoca to export its dynamics,
JAX to identify drag from noisy synthetic flight data, and CasADi to optimize a
constrained trajectory. CPU only; no GPU or AI assistant required.

Our broader work connects declared models with Lie group theory, reachable-set
computation for cyberphysical systems, formal software verification, system
identification and digital twins. Our aim is a unified, declarative environment
for cyberphysical systems, with solver specialization, heterogeneous compute,
fast Monte Carlo/RL and extensible AD/backend integrations as research directions.
The workshop follows one compact example
through simulation, fitting and optimization; the opening slides explain the
larger motivation and distinguish these research uses from today's exercises.

The next **PURT pylon racing competition will leverage Rumoca**.
Follow the [competition site](https://pylon-racing.geddes.rcac.purdue.edu/)
for announcements and event details.

Want an extra challenge? Change a Rumoca model or existing interactive simulator
and show one checked result. Agents, a new app and public hosting are optional. Short demos and an audience hand vote at **12:50** decide who wins
a **free CogniPilot stocking cap**. Apply Rumoca to a problem you care about;
[challenge details](docs/CHALLENGE.md).

## Choose your route in 60 seconds

- **Want to start immediately / no account?** Open the [Rumoca playground](https://rumoca.cognipilot.org/playground/). Browser modeling is zero-install. JAX and CasADi use Python on the routes below; follow the presenters’ plots if Python is unavailable.
- **GitHub login and Codespaces available?** [Open a Codespace](https://codespaces.new/CogniPilot/rumoca_workshop_amc2026?quickstart=1). The devcontainer prepares Python and installs the pinned native Rumoca LSP. Your account needs allowance or authorized billing. The core and optional Torch workflows have passed in an actual two-core Codespace; class capacity still needs preflight. See [verification](docs/VERIFICATION.md).
- **Prefer local VS Code?** Follow the [local VS Code setup](docs/LOCAL_SETUP.md) for uv, native LSP installation and the editor checkpoint, then run the commands below. Windows x64, macOS 14+ (Intel/Apple Silicon), Linux x64 with glibc 2.28+; CI evidence is recorded in [verification](docs/VERIFICATION.md).
- **Cloud or installation failed?** Continue the browser exercise and use [committed reference figures](results/reference). Pair with someone whose Python setup works, or follow the presenters. No account is needed to read these files.

## Local / Codespaces terminal

Open a terminal in this repository (the folder containing `pyproject.toml`):

```sh
uv sync --frozen
uv run --frozen python scripts/smoke_test.py
```

Three workshop commands, in order:

```sh
uv run --frozen python scripts/simulate.py
uv run --frozen python scripts/fit_drag_jax.py
uv run --frozen python scripts/optimize_casadi.py
```

Open the PNGs in `results/live/` in VS Code. Use **Terminal → Run Task** for the
same named commands. Each script compiles the current `models/Quadrotor.mo`;
no generated Python dynamics are hand-written. The committed dataset is ready
to use. The simulation honors your model defaults; fitting and optimization
estimate/use drag parameters explicitly.

## Materials

Use the **[slides (PDF)](slides/workshop.pdf)** to follow the presentation and the
**[participant worksheet](docs/WORKSHOP.md)** for copyable commands and checkpoints.
[PowerPoint](slides/workshop.pptx) includes presenter notes.

Open Markdown in VS Code with **Open Preview** (Ctrl+Shift+V on Linux/Windows,
Cmd+Shift+V on Mac). Codespaces includes GitHub-style Markdown preview, PDF,
Modelica, Lean and Jinja extensions.

Optional references: [setup](docs/LOCAL_SETUP.md), [recovery](docs/TROUBLESHOOTING.md),
[custom targets](docs/BACKENDS.md), [apps](docs/BROWSER_APPS.md),
[challenge](docs/CHALLENGE.md), [math evidence](docs/MATH_REVIEW.md),
[verification](docs/VERIFICATION.md), [presenter guide](docs/PRESENTERS.md).

Rumoca is an evolving compiler and less mature than established Modelica tools.
This workshop checks one deliberately small, smooth ODE workflow. It complements
JAX, CasADi, FMI, and existing Modelica tools.

[Rumoca source](https://github.com/CogniPilot/rumoca) ·
[User guide](https://cognipilot.github.io/rumoca/user-guide/) ·
[Report a workshop issue](https://github.com/CogniPilot/rumoca_workshop_amc2026/issues)

The [user guide](https://cognipilot.github.io/rumoca/user-guide/) is also a live
modeling resource: embedded editors, runnable examples and visualizations.
The workshop includes a short NACA flow demo and an optional custom Torch target
using the core vehicle. Automatic CI runs the core on four platforms, rechecks
Lean proofs, builds the devcontainer and checks the Linux flake/Torch path.
**Terminal → Run Task → Workshop: CI checks** repeats the CPU checks in your
local VS Code or Codespace. See [LOCAL_SETUP.md](docs/LOCAL_SETUP.md).
