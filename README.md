# Hands-On with Rumoca

American Modelica Conference · Georgia Tech · October 12, 2026 · 10:00–13:00

**[Start here: participant walkthrough](WORKSHOP.md)**

Declare a planar quadrotor once in Modelica. Use Rumoca to export its dynamics,
JAX to identify drag from noisy synthetic flight data, and CasADi to optimize a
constrained trajectory. CPU only; no GPU or AI assistant required.

Want an extra challenge? Build an app with coding agents on your GitHub during
the workshop. Short demos and an audience hand vote at **12:50** decide who wins
a **free CogniPilot stocking cap**. Any app theme is welcome;
[challenge details](CHALLENGE.md).

## Choose your route in 60 seconds

- **Want to start immediately / no account?** Open the [Rumoca playground](https://rumoca.cognipilot.org/playground/). Browser modeling is zero-install. JAX and CasADi use Python on the routes below; follow the instructor's plots if Python is unavailable.
- **GitHub login and Codespaces available?** [Open a Codespace](https://codespaces.new/CogniPilot/rumoca_workshop_amc2026?quickstart=1). The devcontainer prepares Python and recommends the Rumoca VS Code extension. Your account needs allowance or authorized billing. Fresh cloud startup and class capacity require instructor preflight; see [verification](VERIFICATION.md).
- **Prefer local VS Code?** Download this repository, install [uv](https://docs.astral.sh/uv/getting-started/installation/) and the [Rumoca extension](https://marketplace.visualstudio.com/items?itemName=JamesGoppert.rumoca-modelica), then run the commands below. Windows x64, macOS 14+ (Intel/Apple Silicon), Linux x64 with glibc 2.28+; CI evidence is recorded in [verification](VERIFICATION.md).
- **Cloud or installation failed?** Continue the browser exercise and use [committed reference figures](results/reference). Pair with someone whose Python setup works, or follow the instructor. No account is needed to read these files.

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

| Resource | Purpose |
|---|---|
| [WORKSHOP.md](WORKSHOP.md) | Timed participant worksheet and checkpoints |
| [INSTRUCTOR.md](INSTRUCTOR.md) | Facilitation, answers, research context |
| [REHEARSAL.md](REHEARSAL.md) | Exact click/type sequence and recovery |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Setup and exercise recovery |
| [slides/workshop.pptx](slides/workshop.pptx) / [PDF](slides/workshop.pdf) | Presentation and offline backup |
| [slides/workshop.md](slides/workshop.md) | Editable slide text and speaker notes |
| [VERIFICATION.md](VERIFICATION.md) | Measured results and unverified items |
| [BROWSER_APPS.md](BROWSER_APPS.md) | Experiment with three agent-built browser apps |
| [CHALLENGE.md](CHALLENGE.md) | Optional open app competition, demos and audience vote |
| [PUBLICATION.md](PUBLICATION.md) | Cloud access, preflight and prebuild guidance |

Rumoca is an evolving compiler and less mature than established Modelica tools.
This workshop proves one deliberately small, smooth ODE example. It complements
JAX, CasADi, FMI, and existing Modelica tools.

[Rumoca source](https://github.com/CogniPilot/rumoca) ·
[User guide](https://cognipilot.github.io/rumoca/user-guide/) ·
[Report a workshop issue](https://github.com/CogniPilot/rumoca_workshop_amc2026/issues)
