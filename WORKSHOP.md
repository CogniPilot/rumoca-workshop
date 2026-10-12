# Hands-On with Rumoca — participant worksheet

**Monday, October 12, 2026 · Georgia Tech · 10:00–13:00**
James Goppert · Micah Condie
Purdue University, School of Aeronautics and Astronautics

Start with [README.md](README.md) to choose browser, cloud or local access.
Keep this worksheet open. Work in pairs if only one laptop has Python running.
Every core exercise has a [reference figure](results/reference) for recovery.
The math assumptions and proofs are in [MATH_REVIEW.md](MATH_REVIEW.md).
No aerospace background is required; the example lets us change a parameter,
fit measurements and solve a constrained problem in one workflow.

## 10:00–10:20 · The result we are building

Why Rumoca? Keep the physical equations consistent as computational questions
change. Our broader work uses declared mathematics for Lie group theory,
reachable sets of cyberphysical systems, formal software verification,
system identification and digital twins. Today focuses on simulation,
identification and optimization of one small model.

One source file, [models/Quadrotor.mo](models/Quadrotor.mo), declares six planar
states and two inputs. Rumoca compiles it into JAX functions for identification
and CasADi functions for constrained trajectory optimization. Python supplies
integrators, data handling and optimization problems; it does not re-declare the
vehicle equations. The core Python exercises run on CPU.

Today’s data are **synthetic**. Today’s control result is an **open-loop trajectory**.
The example does not certify a real aircraft or implement MPC.

**Optional challenge, announced now:** change a Rumoca model, controller or
existing interactive simulator and show one checked result. Apply it to a problem
you care about during downtime and independent work. Agents, a new app and
public hosting are optional. Enter by **12:40**; up to five presenters give short demos
at **12:50**. An audience hand vote chooses the winner of a
**free CogniPilot stocking cap**. Our lead example is `rumoca_fixed_wing`;
`slam_web` is another example in development. See [CHALLENGE.md](CHALLENGE.md).
You can begin when ready and return to your app during independent work.
Copy the short experiment prompt in [APP_PROMPT.md](APP_PROMPT.md). Its public
Three.js launch app and fixed-wing app prompts are optional stretches, not
assigned projects. AD-based fixed-wing MPC is an ambitious
optional extension. Any subject is welcome. More than five ready entries are shortlisted
by random draw; selection is not a quality judgment.

## 10:20–10:40 · Get running

### Everyone: browser first (about 3 minutes)

1. Open the [public Rumoca playground](https://rumoca.cognipilot.org/playground/).
2. Open [browser/Quadrotor_browser.mo](browser/Quadrotor_browser.mo), select
   **Raw**, copy all text. Click inside the playground’s editor, select all and paste.
   This generated bundle includes the canonical model and a short experiment wrapper.
3. Click the **gear** beside the editor’s Play button. In simulation settings,
   choose model **BrowserFlight**, close settings, then click **Play**.
4. Find **BrowserFlight Results** and the time-series plot. Select `x` or `vx`
   in the plot’s variable controls if other curves obscure the response.

The deployed playground was tested at Rumoca **0.8.13**. Python is pinned to
**0.10.2**. Both run the same Modelica equations here; they are separate runtimes.
The browser has no JAX/CasADi Python terminal.

### Full Python route: cloud or local (about 10 minutes)

**Cloud:** [create a Codespace](https://codespaces.new/CogniPilot/rumoca_workshop_amc2026?quickstart=1).
Sign in with GitHub; check your account’s allowance/policy before creating it.
Wait for container setup to complete and the smoke test to say **WORKSHOP PASS**.
An actual two-core Codespace passed startup and all core commands. Test your
intended account before class: allowance, prebuild readiness, region availability
and capacity for 50 users remain presenter preflight items; see
[verification](VERIFICATION.md).

**Local:** follow [local VS Code setup](LOCAL_SETUP.md), or [download the ZIP](https://github.com/CogniPilot/rumoca_workshop_amc2026/archive/refs/heads/main.zip),
extract it, open the extracted folder in VS Code. Install
[uv](https://docs.astral.sh/uv/getting-started/installation/) and the
[Rumoca extension](https://marketplace.visualstudio.com/items?itemName=JamesGoppert.rumoca-modelica).
In **Terminal → New Terminal**, run:

```sh
uv sync --frozen
uv run --frozen python scripts/smoke_test.py
```

The same commands work in PowerShell and Unix shells. `uv` obtains Python 3.12
if needed. Supported qualified Python paths: Windows x64, Linux x64 with
glibc ≥2.28, macOS ≥14 on Apple Silicon or Intel. Linux ARM wheels are pinned
but the ARM route has not been executed in this workshop’s CI.

Open `models/Quadrotor.mo`. Accept Workspace Trust for this workshop if your
policy allows it. The status bar should identify **Modelica**. In Extensions,
check that **Rumoca Modelica** (`JamesGoppert.rumoca-modelica`) is installed and
enabled. Hover over `m`; try Ctrl+Space while typing `si` in an expression, then
undo. The released extension provides verified hover, completion and syntax
diagnostics on Linux x64, Windows x64 and both Mac architectures. Actual Codespace remote hover, completion and diagnostics are separately
qualified; see [verification](VERIFICATION.md).

**Checkpoint 1:** a browser plot; on the full route, **WORKSHOP PASS** and a
`.mo` editor with the extension active. If setup takes over 10 minutes, use
the browser and pair/screenshare path; [troubleshooting](TROUBLESHOOTING.md).

## 10:35–10:40 · Explore a live user-guide example

The [user guide](https://cognipilot.github.io/rumoca/user-guide/) includes embedded
editors and runnable examples. Open the
[NACA 2412 airfoil flow example](https://cognipilot.github.io/rumoca/user-guide/language/arrays-pde.html#2-d-navierstokes-flow-over-a-naca-2412-airfoil).
In its `AirfoilFlow` editor, change **`StopTime = 30` to `StopTime = 2`**.
Keep the default grid, leave **Interactive** off, and click **Simulate** with
**GPU** checked. Select the last frame; try **Field → Vorticity / Pressure**.

This is a coarse artificial-compressibility and penalized-flow teaching
visualization, not validated airfoil performance. It uses a separate deployed
browser runtime. If WebGPU is unavailable or the short run fails, follow the
presenters’ [saved demonstration](slides/assets/user-guide-naca.png) and continue.
The recorded NACA rehearsal covers WebGPU; the CPU NACA route is unqualified
and is not the recovery path for this five-minute segment.
The same guide page also offers turkey heating and a vibrating membrane.
Revisit these examples during downtime if they connect better with your domain.

## 10:40–11:00 · Change a parameter and see the result

World `x` points right; `z` points up. Positive pitch `theta` tilts thrust toward
positive `x`. States are `x, z, theta, vx, vz, omega`; inputs are thrust `T` in
newtons and torque `tau` in newton metres. Mass is 1.2 kg, pitch inertia
0.025 kg m². At rest, level thrust `m*g = 11.772 N` balances gravity.

For either velocity component, drag force is

```text
D(v) = -k_linear*v - k_quad*sqrt(v*v + eps*eps)*v
k_linear: N s/m      k_quad: N s²/m²      eps = 0.01 m/s
```

This is a smooth, componentwise **world-axis teaching drag law**. It omits
body-axis rotor aerodynamics, motor dynamics, wind, roll, yaw and contact.

1. Predict: with the same thrust/torque inputs, will adding positive quadratic
   drag increase or decrease travelled distance? What happens for negative speed?
2. Run the first Python command and open `results/live/simulation.png`:

   ```sh
   uv run --frozen python scripts/simulate.py
   ```

3. In `models/Quadrotor.mo`, change only `k_quad = 0.0` to `k_quad = 0.08`.
   Save; rerun the same command. The plot compares linear-only and quadratic
   cases and also marks your current model default. The prescribed Python
   manoeuvre is different from the browser’s level coasting experiment.
4. In the browser’s pasted model, make the same coefficient change and press
   Play with **BrowserFlight** selected. Compare `vx` and `x` qualitatively.
5. Optional: change `k_linear` to `0.30`; predict the low-speed response first.
   Restore it to `0.18` before continuing.

**Checkpoint 2:** larger drag shortens the response. In the reference Python
experiment, final distance is about **41.60 m** with linear-only drag and
**17.97 m** with quadratic drag. Negative velocity produces positive drag force,
so force still opposes motion. `models/Quadrotor_solution.mo` records the answer
as an inheritance override; the underlying equations stay in one file.

## 11:00–11:10 · Break 1

Keep your editor and terminal open. Recovery image:
[simulation.png](results/reference/simulation.png). Next command: JAX fit.

## 11:10–11:50 · Fit physical parameters with JAX

[data/noisy_flight.csv](data/noisy_flight.csv) contains four 8-second experiments
sampled at 20 Hz. Three flights train the fit; a negative-initial-speed flight
is held out. Input commands are known; initial states are assumed known exactly.
Subsequent measurements contain independent Gaussian noise: position 0.025 m,
velocity 0.035 m/s, angle 0.001 rad and rate 0.003 rad/s.

The dataset was generated from the **Rumoca CasADi export with adaptive DOP853**;
the fit predicts using the **Rumoca JAX export with RK4**. This avoids generating
and fitting with the very same numerical integrator. You do not regenerate data
during class. Ground truth is in `data/truth.json` for checking afterward, not
as an input to the fitted objective.

1. Run:

   ```sh
   uv run --frozen python scripts/fit_drag_jax.py
   ```

2. Open `results/live/fit_drag.png` and `fit_drag.json`. Compare before/after
   predictions, the three training flights and the held-out flight.
3. Find `drag`, `final_loss`, `noise_scaled_rms`, `rms_by_state` and
   `sensitivity_condition_number`. The loss weights position and velocity
   errors by their measurement standard deviations, so it is dimensionless.
4. Expected estimates: **linear ≈0.18042 N s/m; quadratic ≈0.07991 N s²/m²**.
   Truth: 0.18 and 0.08. The initial guesses are 0.06 and 0.025. The mean
   noise-scaled squared loss drops from about 26,932 to 1.073.
5. Inspect `scripts/fit_drag_jax.py`: `log` coefficients enforce positivity,
   `jax.value_and_grad` differentiates through the generated RHS and the RK4
   rollout, and SciPy L-BFGS-B performs the bounded optimization.

**Checkpoint 3:** two estimates, a loss decrease and improved holdout prediction.
The sensitivity condition number (about 10.87) is a **local diagnostic**; it is
not a theorem of global identifiability or statistical certainty.

**Recovery:** fit only quadratic drag with linear drag assumed known:

```sh
uv run --frozen python scripts/fit_drag_jax.py --one-coefficient
```

**Stretch:** change the initial guesses in the fitting script, rerun, compare
estimates. Keep the canonical source equations unchanged. Restore script edits
before the presenters’ smoke test. The presenter audit already checks six
starting guesses and twelve noise seeds.

## 11:50–11:55 · Check your result or keep building

Open the before-and-after plot. Check the fitted values and whether the held-out
prediction improved. Ask for help if a result is unexpected. If you are ready,
continue your [challenge app](CHALLENGE.md) or try another fit starting guess.

JAX autodiff differentiates the implemented discretized computation, subject to
floating-point arithmetic. It does not remove integration error or model error.
Native compiler AD is a separate capability and is not demonstrated today.
The Lean proofs and profile-likelihood audit are presenter evidence in
[MATH_REVIEW.md](MATH_REVIEW.md), not extra attendee installs.

## 11:55–12:00 · Extend a backend; learn a small policy

Watch the presenters generate **PyTorch** dynamics from the same vehicle with
an external `target.toml`, then learn two feedback gains for vertical hover.
The [optional backend guide](BACKENDS.md) explains the code, checks and commands.
This is differentiable model-based policy optimization, a small bridge to RL.
The saved [held-out result](results/reference/torch_policy.png) compares 128 new
initial conditions. The demonstration is qualified on Linux x64 CPU, including
Codespaces; the extra Torch package is optional and need not be installed in class.

## 12:00–12:10 · Break 2

Leave `fit_drag.json` in `results/live/`. Next: use those coefficients in CasADi.
Recovery image: [fit_drag.png](results/reference/fit_drag.png).

## 12:10–12:40 · Optimize a constrained flight with CasADi

Move from hover at **(0, 1) m** to hover at **(4, 2) m** in 6 seconds. The same
Modelica source is compiled again; fitted drag is loaded from your JAX output.
Direct multiple shooting uses 60 constant-input intervals, RK4 dynamics,
exact endpoint constraints at nodes and IPOPT to solve a local nonlinear program.

Physical limits: thrust 0–20 N; torque ±0.35 N m; altitude 0.25–4 m; pitch
±0.55 rad. The solver uses ±0.54 rad at nodes to leave a margin between samples.
An illustrative rotor-pair allocation also restricts each pair to 0–10 N at
0.2 m moment arm. The objective trades normalized tracking, effort and changes
in control. It is dimensionless; weights are teaching choices.

1. Run after your fit:

   ```sh
   uv run --frozen python scripts/optimize_casadi.py
   ```

2. Open `results/live/optimization.png` and `optimization.json`. Look for
   **Solve_Succeeded**, motion to the target, braking tilt, thrust limits,
   terminal error, dynamics defects and finer-rollout error.
3. Confirm `drag` equals your fitted values. A source hash prevents silently
   consuming an old fit after further model edits; refit if prompted.
4. Explain why essentially zero endpoint error at transcription nodes can
   coexist with about 2 mm altitude error under independent integration.

**Checkpoint 4:** a feasible discretized trajectory, both terminal velocities
near zero, and bounds checked in finer integration. No claim of global
optimality or real-aircraft safety follows from IPOPT convergence.

**Recovery:** if your fit file is missing or scripts were changed, restore the
canonical model defaults (linear 0.18, quadratic 0.0), then run:

```sh
uv run --frozen python scripts/optimize_casadi.py --fit results/reference/fit_drag.json
```

If the canonical source hash differs, run your own fit instead. Reference plots
remain available without Python. The optional target variant `--target-x 3`
was also rehearsed successfully; see [verification](VERIFICATION.md).
MPC would repeat optimization with updated measured state; we do not run an MPC loop today.

## 12:40–12:45 · Connect the model to experiments

The next **PURT pylon racing competition will leverage Rumoca**. Follow the
[competition site](https://pylon-racing.geddes.rcac.purdue.edu/) for announcements.
Its published format connects digital-twin simulation with physical flight
tests. Upcoming dates, rules and registration will be announced by the organizers.

Purdue’s [UAS Research and Test Facility](https://engineering.purdue.edu/PURT)
grounds model-based work in experiments. Public
[CogniPilot workspace documentation](https://github.com/CogniPilot/cognipilot_workspace)
describes pure-Modelica and FastDyn/QEMU embedded testing workflows. They are
upstream examples, not exercises executed here. Monte Carlo and reinforcement
learning are application directions. Unified vision/SLAM/estimation models and
automatic hardware partitioning are research goals.

## 12:45–12:50 · Explore the fixed-wing app or finish your demo

Open [BROWSER_APPS.md](BROWSER_APPS.md) and try the **rumoca_fixed_wing**
autopilot experiment: change its controller rate, restart and observe.
This is the lead example of an app we built with coding agents. `slam_web` is
another example **in development**; `mocap_sysid` is a stored-results viewer.
No agent account or API key is required to explore the examples manually.
Selected app builders can use this time to rehearse their 45-second demo and
open their app and GitHub repo. All entries remain in the shared gallery.

**Checkpoint 5:** describe one observation and one test needed before trusting
it. These apps use their own models and data. The workshop’s planar-model Lean
proofs do not cover them. SLAM Lab’s inertial demo is distinct from its unfinished
full visual-SLAM pipeline; the benchmark viewer displays previously generated
results rather than retraining methods in your browser.

## 12:50–12:55 · Participant demos and audience vote

Show your app and GitHub repository, explain your contribution, and demonstrate
one working interaction in **45 seconds**. Name the agent used and elapsed
build time, labeling estimates. Any subject is welcome. An audience **show-of-hands vote**
chooses the winner of a **free CogniPilot stocking cap**.
[CHALLENGE.md](CHALLENGE.md) gives the short-demo format and voting rules.

## 12:55–13:00 · Questions, collaboration and take-home

Bring a model from your own domain, a scientific question and one result we can
check together. [Join the work](COMMUNITY.md): share a validation case, improve
a model library or compiler, or open a research/model collaboration conversation.
Speak with James Goppert or Micah Condie before leaving, or follow the closing QR.
Take-home challenge: try another initial fit guess, inspect holdout prediction,
and explain one model limitation before suggesting an extension.

## Slides and proofs in VS Code

The Codespace installs [PDF Viewer](https://marketplace.visualstudio.com/items?itemName=mathematic.vscode-pdf)
and [Lean 4](https://marketplace.visualstudio.com/items?itemName=leanprover.lean4)
alongside Rumoca. Open `slides/workshop.pdf` in Explorer to view the slides
inside VS Code; if necessary choose **Open With → PDF View**. Existing Codespaces
need **Codespaces: Rebuild Container** to apply the updated configuration.

Lean is optional for participants. Its extension provides editor support;
checking `formal/Generated.lean` also needs the pinned toolchain and Mathlib
setup described in [MATH_REVIEW.md](MATH_REVIEW.md). The core exercises do not
require those downloads.
