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
| Cloud startup | Open Codespaces link → choose authorized account → create → wait for postCreate → open terminal → check WORKSHOP PASS | **Unmeasured fresh cloud startup**; start tonight, not on stage | Local `uv`; paired/screenshared Python |
| Local startup | VS Code → File/Open Folder → extracted repo → Terminal/New Terminal → `uv sync --frozen` → smoke command below | Network install time depends on first downloads; successful end-to-end smoke ~12 s locally after setup | Browser + figures if installation exceeds 10 min |
| LSP | Open `models/Quadrotor.mo` → Extensions verify Rumoca enabled → hover `m` → Ctrl+Space after typing `si` → undo; optionally create `scratch.mo` with `model Broken` / `Real x = ;` / `end Broken;`, observe error then delete | 2 min; actual 0.10.2 Linux LSP tested hover, sin completion, syntax errors | Real `vscode-quadrotor.png`; no claims about navigation not tested |
| Simulation | Terminal run simulate → Explorer `results/live/simulation.png` → change k_quad default to 0.08/save → run again | 1–2 s local computation per run; 5 min demo; curves separated | Reference simulation PNG |
| JAX fit | Terminal run fit → open fit_drag PNG → open JSON → highlight drag, final_loss, per-state and scaled RMS | ~5–6 s local computation; 5 min demo; 0.18042 / 0.07991 | Restore defaults, refit; one-coefficient; then reference figure |
| CasADi | Keep same source since fit → run optimize → open PNG → JSON solver_status, drag, terminal and fine error | ~1–2 s local computation; 5 min demo; Solve_Succeeded | Source-hash error: refit; canonical defaults + reference fit; then reference PNG |
| Mathematical appendix | Open MATH_REVIEW then proof log and audit figure; point out exact-real theorem scope versus numerical evidence | 2 min if asked; no attendee Lean installation | Explain verbally; no live Mathlib download |
| Close | Return to slides 19–22 → label public upstream/future work → point to issue and repo links | Exactly 12:45–13:00 | PDF; no live research-project startup |

Three core commands (copy individually):

```sh
uv run --frozen python scripts/simulate.py
uv run --frozen python scripts/fit_drag_jax.py
uv run --frozen python scripts/optimize_casadi.py
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

Independent instructor numerical audit, after a successful smoke run:

```sh
uv run --frozen python scripts/math_audit.py --output results/live
```

Before going on stage, switch airplane/offline mode briefly and confirm that
the local deck, CSV, installed Python dependencies and reference PNGs still open.
Browser/cloud routes need a network. Do not turn an offline screenshot into a
claim of a live browser run. Re-enable networking afterward.

For each timed segment, announce the worksheet checkpoint and ask for a show of
hands. At 10:40 stop setup support; at 11:05 and 12:00 display the break slide;
at 12:45 move to the research close. Keep the two full ten-minute breaks.
