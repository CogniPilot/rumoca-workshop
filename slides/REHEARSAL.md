# End-to-end rehearsal sheet

Keep the presenting computer plugged in. Download the repository and PDF/PPTX
before venue Wi-Fi is needed. Open the participant worksheet, browser playground,
VS Code workspace, and `results/reference/` in advance. Rehearse on the actual
laptop; timings below are measured computation or a facilitation budget,
not a promise about network startup.

| Demo | Exact click/type sequence | Budget and pass point | Recovery |
|---|---|---|---|
| Browser opening | Playground → click editor → select all/paste complete `browser/Quadrotor_browser.mo` → gear beside Play → Model `BrowserFlight` → close settings → Play | 3 min including explanation; actual browser reports 501 points, 8 variables and balanced compilation | `slides/assets/browser-drag-linear.png` + local VS Code |
| Browser edit | Find `k_quad` parameter → 0.0 to 0.08 → Play → inspect `x`/`vx` curves | 2 min; drag opposes velocity; results panel still says BrowserFlight | `browser-drag-quadratic.png`; explain this is a recorded successful run |
| Cloud startup | Open Codespaces link → choose authorized account → create → wait for workspace preparation → open terminal → check WORKSHOP PASS | Fresh-cloud qualification is recorded in VERIFICATION.md; start before class | Local `uv`; paired/screenshared Python |
| Local startup | VS Code → File/Open Folder → extracted repo → Terminal/New Terminal → `uv sync --frozen` → smoke command below | Network install time depends on first downloads; successful end-to-end smoke ~12 s locally after setup | Browser + figures if installation exceeds 10 min |
| Compiler pipeline | Slide 4 → source/AST → resolve/type/instantiate → Flat → DAE → structural preparation → Solve; point out the separate DAE → GaLEC embedded-control branch | 10:15–10:20, including the Session API examples; define each IR in plain language | Released pipeline/GaLEC links on the slide; today's continuous model uses Solve |
| LSP | Open `models/Quadrotor.mo` → Extensions verify Rumoca enabled → hover `m` → Ctrl+Space after typing `si` → undo; optionally create `scratch.mo` with `model Broken` / `Real x = ;` / `end Broken;`, observe error then delete | 2 min; actual 0.10.2 LSP tested on Linux/Windows x64 and both Mac architectures | Real `vscode-quadrotor.png`; no claims about navigation not tested |
| Native scenario | Open `models/BrowserFlight.mo` → lightning bolt → save generated TOML → Batch end time 8 s → y series `x` and `vx` → Save → Run Simulation → repeat after saving k_quad 0.08 | Rehearsed in native VS Code inside the Codespace: both runs 501 points, 8 variables; final travel about 27.95 m then 15.78 m | WORKSHOP.md; restore canonical model after the edit |
| Simulation | Terminal run simulate → Explorer `results/live/simulation.png` → change k_quad default to 0.08/save → run again | 1–2 s local computation per run; 5 min demo; curves separated | Reference simulation PNG |
| JAX fit | Terminal run fit → open fit_drag PNG → open JSON → highlight drag, final_loss, per-state and scaled RMS | ~5–6 s local computation; 5 min demo; 0.18042 / 0.07991 | Restore defaults, refit; one-coefficient; then reference figure |
| CasADi | Keep same source since fit → run optimize → open PNG → JSON solver_status, drag, terminal and fine error | ~1–2 s local computation; 5 min demo; Solve_Succeeded | Source-hash error: refit; canonical defaults + reference fit; then reference PNG |
| Quadrotor scenario + scene | Slides 7–10 → guide Quadrotor SIL → Settings → model/solver/clock → Raw TOML → inputs/signals → Simulate → Capture → Space + short W taps → Stop | 10:30–10:40; settings iframe, live scene and keyboard arming rehearsed | SIMULATION_SETUP.md + user-guide-quadrotor.png; planar native scenario for Python path |
| User-guide NACA | Slide 11 → exact guide link in WORKSHOP.md → AirfoilFlow editor StopTime 30 → 2 → GPU on, Interactive off → Simulate → final frame → Field Vorticity/Pressure | Exactly 10:40–10:45; short default-grid WebGPU run rehearsed with software adapter | `slides/assets/user-guide-naca.png`; other embedded guide examples; warm the tab before class |
| Torch target + policy | Slide 20 → open target.toml + template + generated RHS → check backend → run learning → policy plot | Exactly 11:55–12:00; optional group preinstalled; 14–27 s policy computation in two-core Codespace | `results/reference/torch_policy.png` + BACKENDS.md; no extra attendee install |
| Lean Jinja target | Slide 19 → target.toml IR/capabilities/files → rhs.lean.jinja `Control` loop → Session codegen → Generated.lean → hover_equilibrium → completed Lean CI | 11:50–11:55; confirm fit checkpoint, demonstrate loop/substitution and one property; optional copy-and-comment exercise in BACKENDS.md | Checked generated source + CI log; no live Mathlib download |
| Optional terminal agent | Follow AGENT_SETUP.md login → new terminal → `tmux new -s experiment` → launch chosen agent → paste the first-experiment prompt → detach with Ctrl+B, D | All three initial screens rehearsed in the rebuilt Codespace. The starter prompt completed with authenticated Codex on the maintainer machine in about 81 s; timing varies | Core tasks and manual experiments remain available without agent login |
| App gallery | Slides 26–29 → BROWSER_APPS.md → choose one tested app experiment; lead with fixed-wing; let challenge entrants finish demos | Exactly 12:45–12:50: 1 min introduce, 30 s acknowledge LunCoSim/Taskyon, 3½ min explore or finish an experiment | Real app screenshots; prediction discussion if network/graphics fails |
| Community users | Slide 29 → LunCoSim simulator/download link and Taskyon app → source integration links in notes | Share 12:45–12:50; about 30 s, public pages/source checked; no live third-party mission/agent run claimed | Actual website previews and clickable simulator/app/source links |
| Challenge | Slide 2 announces open Rumoca experiment competition → collect experiment entries by 12:40 → draw up to five ready presenters if needed, plus order and backup → announce by 12:45 → slide 31 demos → hand vote → stocking-cap award | 12:50–12:55: up to five 45-second demos, 75 s vote/award; name tool and elapsed work time, label estimates; CHALLENGE.md | If a presenter is unavailable, use backup; if no entries, take an app question and continue |
| PURT racing | Slide 24 → next pylon racing competition will leverage Rumoca → site and QR | 12:40–12:45; upcoming dates/rules announced on the competition site | Link and QR; do not repeat April 2026 dates as upcoming |
| FastDyn | Slide 25 → trajectory/poster → play 20–30 s of embedded movie → show separate FastDyn Codespace route in FASTDYN.md | Share the 12:40–12:45 segment with racing. Three-flight firmware campaign passed in CI and cloud; prestart the larger environment | Embedded recording and existing campaign plots; avoid a fresh firmware/image download on stage |
| Close | Slide 31 → ask which model attendees would try next → research community invitation and clickable email | Exactly 12:55–13:00; invite conversation with James Goppert or Micah Condie | jgoppert@purdue.edu + compiler/model-library links |

Three core commands (copy individually):

```sh
uv run --frozen python examples/simulate.py
uv run --frozen python examples/fit_drag_jax.py
uv run --frozen python examples/optimize_casadi.py
```

One end-to-end rehearsal command:

```sh
uv run --frozen python scripts/smoke_test.py
```

It includes backend/gradient checks, the three commands, fit recovery, holdout,
constraints and generated-output checks. Run once after restoring the canonical
source (`k_linear=0.18`, `k_quad=0.0`) before class. Your drag edit changes the
source hash; fitting still works, but a reference fit requires the original hash.

Inspect the same model through its actual exports, if asked:

```sh
uv run --frozen python scripts/export_model.py
```

Independent presenter numerical audit, after a successful smoke run:

```sh
uv run --frozen python scripts/math_audit.py --output results/live
```

Before going on stage, switch airplane/offline mode briefly and confirm that
the local deck, CSV, installed Python dependencies and reference PNGs still open.
Browser/cloud routes need a network. Do not turn an offline screenshot into a
claim of a live browser run. Re-enable networking afterward.

For each timed segment, announce the worksheet checkpoint and ask for a show of
hands. At 10:40 stop setup support; at 11:00 and 12:00 display the break slide;
at 12:40 connect to experiments, at 12:45 explore apps and at 12:50 start demos. Keep the two full ten-minute breaks.
