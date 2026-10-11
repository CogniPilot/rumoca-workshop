# Hands-On with Rumoca

Editable source for both workshop.pptx and workshop.pdf. Build with:
`uv run --frozen --group slides python scripts/build_slides.py`.
Notes are included in the presentation; Checkpoint appears on the slide.
Main slide times are contiguous and total 180 minutes, including two breaks.

## 01 · Hands-On with Rumoca
Time: 10:00–10:05
Layout: title
Visual: assets/repo-qr.png
Badge: American Modelica Conference · October 12, 2026

- James Goppert
- Purdue University · School of Aeronautics and Astronautics
- Georgia Tech · 10:00–13:00

Checkpoint: github.com/CogniPilot/rumoca_workshop_amc2026
Notes:
Welcome to Hands-On with Rumoca. Introduce Purdue University, School of Aeronautics and Astronautics, and the Georgia Tech venue. Point to the QR and ask attendees to keep the participant worksheet open. No aerospace background is required. Allow five minutes for arrivals and orientation; announce the optional app challenge on the next slide.

## 02 · Run the core. Build something extra.
Time: 10:05–10:10
Layout: cards
Badge: OPEN APP CHALLENGE · demos + audience vote at 12:50

- Core: edit a model, fit data, optimize a trajectory
- Extra: create an app with coding agents
- Open theme: show your idea on your GitHub
- Audience favorite wins a CogniPilot stocking cap

Checkpoint: Start whenever ready · CHALLENGE.md · core needs no agent account
Notes:
Announce the challenge now: “If you want an extra challenge, build an app with coding agents during the workshop. The theme is open. Put it on your GitHub, show a working interaction at 12:50, and the audience will choose the winner by a show of hands. The prize is a free CogniPilot stocking cap.” Introduce rumoca_fixed_wing as the lead example; BROWSER_APPS.md has its live link. Participants may extend an existing app or start a new one and should explain their contribution. Core exercises need no agent account or GitHub account. Experienced attendees can begin once their environment is ready and keep building during independent work. Ask for a show of hands for Modelica/JAX/CasADi experience. Today's data are synthetic and the trajectory is open loop.

## 03 · Make declared physics reusable
Time: 10:10–10:15
Layout: statement
Badge: Why we built Rumoca

- A physical model should travel with the question.
- Simulation → identification → control → experiment
- Open tools and explicit mathematics help us compare results.

Checkpoint: Rumoca connects Modelica to modern computational tools.
Notes:
Explain the motivation: carry declared physical equations into simulation, parameter fitting and constrained optimization. Rumoca is an evolving open mathematical compiler; this workshop demonstrates a small tested workflow. OpenModelica, Dymola, Modelon, JuliaHub/Dyad, FMI, JAX and CasADi offer ecosystem and interoperability opportunities.

## 04 · Declare once. Ask different questions.
Time: 10:15–10:20
Layout: wide
Visual: assets/architecture.png
Badge: Verified workshop architecture

- Same Quadrotor.mo equations, two generated Python representations

Checkpoint: Modelica declares physics · Rumoca compiles · backends compute.
Notes:
Explain that VS Code is the authoring/LSP path and the playground is browser modeling/simulation. Python 0.10.2 exports JAX and CasADi; deployed browser 0.8.13 is separate. Common Python code performs integration and builds optimization objectives, not another plant. Full language/backends are not certified by this example. Native compiler AD is not today's demonstration.

## 05 · Everyone gets a browser plot
Time: 10:20–10:25
Layout: image
Visual: assets/browser-drag-linear.png
Badge: LIVE DEMO · zero-install modeling

- Open the playground
- Paste the complete browser bundle
- Gear → BrowserFlight → Play

Checkpoint: You should see BrowserFlight Results and a plot.
Notes:
Exact URL https://rumoca.cognipilot.org/playground/. Raw source https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/browser/Quadrotor_browser.mo. Select all inside editor, paste; gear next to Play opens simulation settings; select BrowserFlight and close settings. Screenshot records a real run. Browser is not Python/JAX/CasADi. If offline, label the screenshot as backup and continue local/demo path. Five-minute guided demo.

## 06 · Choose a full-workshop route
Time: 10:25–10:30
Layout: cards
Badge: Setup decision · worksheet has every link

- Browser: modeling and predictions; no account
- Codespaces: Python + VS Code; login and allowance
- Local uv: Python + VS Code; pinned CPU packages
- Pair or screenshare: keep working if setup fails

Checkpoint: Switch route after ten minutes of setup trouble.
Notes:
Codespaces URL https://codespaces.new/CogniPilot/rumoca_workshop_amc2026?quickstart=1. Codespaces requires an account with allowance or billing enabled. Cloud qualification is recorded in VERIFICATION.md; account availability varies. Local: download/extract ZIP, install uv/extension, uv sync --frozen. Python and released editor are qualified on Linux/Windows x64 and macOS Intel/Apple Silicon. The local route uses uv and CPU packages.

## 07 · Edit with feedback. Check the pipeline.
Time: 10:30–10:40
Layout: image
Visual: assets/vscode-quadrotor.png
Badge: HANDS-ON · released LSP verified on four platforms

- Open models/Quadrotor.mo
- Hover m; try sin completion
- Run the smoke test; open results/live
Command: uv run --frozen python scripts/smoke_test.py
Checkpoint: WORKSHOP PASS · model editor ready
Notes:
Give participants most of these ten minutes. Verify extension ID JamesGoppert.rumoca-modelica; choose Modelica language, trust workspace per policy. Show a temporary broken expression then undo for actual syntax diagnostics. Hover, completion and diagnostics passed in real VS Code 1.119.0 hosts on all four supported OS/architecture targets; navigation and Codespaces remote activation are separate checks. Smoke runs all three commands, checks gradient/backend agreement, fits, constraints and outputs. Local measured total about 12 seconds after setup. At 10:40 move to the exercise; use pair or demo recovery if setup is incomplete. App builders can begin their independent challenge once ready.

## 08 · A planar quadrotor we can inspect
Time: 10:40–10:45
Layout: image
Visual: assets/quadrotor.png
Badge: Six states · two aggregate inputs

- World x right; z up
- Positive pitch tilts thrust toward +x
- Hover: T = mg = 11.772 N
Checkpoint: Find velocities, pitch rate, thrust and torque in the model.
Notes:
States x,z,theta,vx,vz,omega; inputs T and tau. m=1.2 kg,Iyy=.025 kg m²,g=9.81. Diagram is generated from our convention, not a borrowed paper figure. Simplified world-axis drag; no roll/yaw/motors/wind/contact. The compact planar example keeps the equations inspectable and the computations short. Introduce pitch as the angle that directs the thrust; specialist aerodynamics is optional.

## 09 · Your first engineering change: drag
Time: 10:45–10:55
Layout: wide
Visual: assets/drag-law.png
Badge: HANDS-ON · predict before running

- Change k_quad = 0.0 to 0.08, save, then simulate.
Command: uv run --frozen python scripts/simulate.py
Checkpoint: What changes at high speed? What about negative velocity?
Notes:
Explain units kl N s/m,kq N s²/m²,epsilon .01 m/s. Smooth componentwise law approximates |v|v and never adds energy for nonnegative coefficients; Lean proves the signs and smoothing bound. It differs from Faessler et al.'s body-frame rotor-drag model; do not claim their flatness theorem. Allow 7–8 minutes editing/predicting. Browser users make the same coefficient change and Play again. Default parameter changes affect simulation; fitting estimates parameters explicitly.

## 10 · More drag, less distance
Time: 10:55–11:00
Layout: wide
Visual: assets/simulation-hero.png
Badge: HANDS-ON · same prescribed Python inputs

- Reference at 8 s: 41.60 m → 17.97 m
Checkpoint: Compare your current default with the two reference cases.
Notes:
Open the actual live plot and ask participants to explain the sign. The slide plot uses emitted JAX equations and reference parameters; not real flight data. Browser wrapper coasts at level hover, so its numbers differ. Optional kl=.30 then restore .18. Instructor solution is an inheritance override, not a second dynamics implementation. Take two questions. End on time for break.

## 11 · Break · back at 11:10
Time: 11:00–11:10
Layout: break
Badge: Ten full minutes

- Keep your editor and terminal open.
- Recovery: results/reference/simulation.png
- Next: fit drag from noisy flight data.
Checkpoint: Worksheet and commands: WORKSHOP.md · scan the opening QR.
Notes:
Actually pause for ten minutes. Help only small recovery questions; avoid turning the break into a lecture. Browser-only attendees can pair for the next exercise. Keep the next command in the worksheet, not a wall of terminal text.

## 12 · Known experiment. Unknown coefficients.
Time: 11:10–11:20
Layout: wide
Visual: assets/data-hero.png
Badge: Synthetic data · seed 20261012

- Three training flights; one held-out flight. 20 Hz, 8 s each.
Checkpoint: Speed variation helps separate linear and quadratic drag.
Notes:
Data generated by Rumoca CasADi + independent adaptive DOP853; JAX fit uses RK4. Position noise .025 m; velocity .035 m/s; angles/rates also noisy, but only exact initial angles/rates enter the fit. Commands and initial state assumed known. Holdout has different excitation and negative initial speed. The data are synthetic. Explain how real logs would bring actuator timing, wind and sensor bias. Truth is reporting only.

## 13 · Differentiate the prediction error
Time: 11:20–11:30
Layout: wide
Visual: assets/fit-workflow.png
Badge: JAX autodiff through generated physics + RK4

- Positive parameters; noise-scaled loss; bounded optimization
Checkpoint: JAX provides gradients. SciPy updates the coefficients.
Notes:
Show fit script's p_from_log, residual, value_and_grad, minimize. Each coefficient divided by one native SI unit equals exp(log parameter), so the logarithm is dimensionless; fitted bounds .001..2 in native units. Mean residual² divided by known noise variance is dimensionless, over x,z,vx,vz. Avoid differentiating noisy acceleration estimates. JAX derivative is of the implemented discrete rollout; finite differences are checks. The system ID is not an autodiff proof of model correctness. Participants can run the next command and inspect the provided algorithm.

## 14 · Run the fit. Test the held-out flight.
Time: 11:30–11:50
Layout: wide
Visual: assets/fit-hero.png
Badge: HANDS-ON · estimates ≈ 0.18042 and 0.07991

- Open fit_drag.png and fit_drag.json; compare before and after.
Command: uv run --frozen python scripts/fit_drag_jax.py
Checkpoint: Two coefficients · lower loss · improved held-out prediction
Notes:
Give at least 15 minutes for running the fit, inspecting outputs and individual questions. Participants who finish can return to the app challenge. Reference truth kl=.18 N s/m, kq=.08 N s²/m². Loss roughly 26932→1.073, about 25000×. Read rms_by_state with separate units or noise_scaled_rms; avoid calling mixed-unit legacy RMS metres. Recovery --one-coefficient assumes known kl=.18. Stretch: different initial guess; audit already checks six. Do not use holdout to tune parameters during this exercise. If live fails, label reference plot honestly.

## 15 · Check your result. Keep building.
Time: 11:50–12:00
Layout: cards
Badge: Checkpoint · go deeper at your own pace

- Open your before-and-after prediction plot
- Compare the held-out flight and fitted values
- Stretch: rerun from another starting guess
- App builders: keep your prototype moving

Checkpoint: Fit complete? Continue your app or explore the optional checks.
Notes:
Spend two minutes showing where the result files are and eight minutes on independent work and questions. Ask whether the held-out prediction improved; no aerospace background is needed. App builders can continue the open challenge. Offer detailed gradient, excitation and proof discussion only when requested, using MATH_REVIEW.md and Appendix A1–A2. The audit checks six starting guesses, twelve noise seeds, Jacobians, analytic coasting and re-optimized profiles. Lean checks scoped exact-real equation equality and invariants; numerical and statistical claims have separate evidence.

## 16 · Break · back at 12:10
Time: 12:00–12:10
Layout: break
Badge: Ten full minutes

- Keep results/live/fit_drag.json.
- Next: use your coefficients to optimize a flight.
- Recovery: results/reference/fit_drag.png
Checkpoint: Same Modelica source; now compile to CasADi.
Notes:
Ten-minute break. Confirm most pairs have fit outputs. Do not edit the model again after fitting; a source hash will require refitting if it changes. Instructor has successful reference fit and primal trajectory warm start. No Mathlib or extra packages are needed for next exercise.

## 17 · Move between hovers, respect limits
Time: 12:10–12:20
Layout: image
Visual: assets/control-problem.png
Badge: CasADi symbolic dynamics · IPOPT local NLP

- (0, 1) m → (4, 2) m in 6 s
- Track target; limit effort and control changes
- Bound thrust, torque, pitch and altitude
Checkpoint: Identified drag is an input to this optimization.
Notes:
Explain 60 constant-input intervals and RK4 direct multiple shooting: decision states at each node, linked by continuity constraints. Bounds: thrust 0–20 N, torque ±0.35 N m, altitude 0.25–4 m, physical pitch ±0.55 rad, node pitch ±0.54 rad. Illustrative rotor pairs: each 0–10 N, arm 0.2 m. Normalize cost with physical reference scales before choosing weights. A stored successful primal solution warm-starts the default problem. Andersson et al. 2019, section 5.4 supports the transcription; their DAE/IDAS example differs from our ODE/RK4. Local feasible result; no global-optimality, electrical-energy or real-flight claim.

## 18 · Solve. Inspect. Explain the braking.
Time: 12:20–12:40
Layout: wide
Visual: assets/control-hero.png
Badge: HANDS-ON · fitted physics, constrained trajectory

- Open optimization.png and optimization.json.
Command: uv run --frozen python scripts/optimize_casadi.py
Checkpoint: Solve_Succeeded · limits respected · arrive near rest
Notes:
Allow about 15 minutes to run and inspect plots/JSON, with the remaining time for questions or app development. Live computation takes about 1–2 seconds locally. Show acceleration tilt and opposite tilt for braking. Confirm drag matches JAX values, defects near 1e−14, exact endpoint constraints at nodes, and about 2 mm altitude error under finer/adaptive integration. Analytic interval pitch extrema are about 0.542 rad, below 0.55. Checks allow 1e−6 numerical tolerance. Explain continuous/discretized differences and the absence of an all-time formal certificate. A source hash requires refitting after edits. Recover with canonical source/reference fit, then a clearly labeled reference figure. Optional --target-x 3 was separately rehearsed; its receipt is in verification/. MPC would repeat optimization online; it is not demonstrated.

## 19 · Bring the model back to the experiment
Time: 12:40–12:45
Layout: wide
Visual: assets/research-loop.png
Badge: Public Purdue / CogniPilot work · separate from today’s demo

- PURT: aircraft experiments, racing and security applications
Checkpoint: Experimental validation is the next engineering step.
Notes:
Official PURT source: https://engineering.purdue.edu/PURT. Public workspace: https://github.com/CogniPilot/cognipilot_workspace documents pure Modelica, host Zephyr SIL and FastDyn/QEMU Cortex-M7 binary-in-the-loop. Documented upstream; not run here. Monte Carlo and reinforcement learning are application directions, not demonstrated results. Avoid unsupported benchmarks and facility superlatives. Synthetic fitting does not establish real-aircraft validity. Briefly connect the model to physical experiments, then introduce the lead fixed-wing app. Leave time for questions and move to app exploration at 12:45.

## 20 · Explore the fixed-wing workbench
Time: 12:45–12:50
Layout: image
Visual: assets/app-rumoca_fixed_wing.png
Badge: AGENT-BUILT APPS · try fixed-wing or finish your own demo

- Modelica flight simulation + autopilot
- Try 50 Hz → 20 Hz, restart, then observe
- Also: slam_web (in development), mocap_sysid

Checkpoint: Live links + short experiments: BROWSER_APPS.md
Notes:
Lead with rumoca_fixed_wing, the more complete app example. Coding agents helped build the interface and experiments; engineers review models and validate output. Briefly show Autopilot → Start sim, waypoint progress, then 50 to 20 Hz → Start sim again → pause. Invite participants to try that interaction or finish their challenge app. SLAM Lab is an additional example in development; only its inertial baseline and filter variant were rehearsed, not the complete visual-SLAM pipeline. Mocap is a viewer for stored benchmark results, not browser retraining. Fixed-wing and SLAM use WASM; the tested mocap viewer interaction does not. No login, agent account or API key is needed to explore these examples manually. They use different models from the core exercise and are outside its Lean proof scope. Keep the recorded screenshots available for network/graphics recovery. At 12:50 move to participant demos.

## 21 · Show your app. Vote for the cap.
Time: 12:50–12:55
Layout: statement
Badge: OPEN CHALLENGE · short demos · audience show of hands

- Show one working interaction and your GitHub repo
- Explain your contribution and one result you checked
- Audience favorite wins a free CogniPilot stocking cap

Checkpoint: Short participant demos → one show-of-hands vote per person
Notes:
Use the first four minutes for participant demos: allow up to four one-minute demos; if more entries arrive, shorten each equally so every entry can be shown. Any app theme is welcome. Each entrant shows a working interaction, their own GitHub repository and their contribution. Reserve the final minute for a show-of-hands vote. Each attendee votes for one entry; count visibly. If tied, run a quick vote between the tied entries; if still tied, draw among them. Award one stocking cap to the winning entry; a team chooses its recipient. If there are no entries, invite a brief question about the fixed-wing example and continue to the closing slide. CHALLENGE.md carries the same rules.

## 22 · Questions + your next problem
Time: 12:55–13:00
Layout: title
Visual: assets/repo-qr.png
Badge: Keep the model. Change the question.

- Bring a modeling, identification or optimization problem
- Share a reproducible model and a measurable result
- Collaborate with Purdue and the open-source community

Checkpoint: github.com/CogniPilot/rumoca_workshop_amc2026
Notes:
Invite collaboration: “Bring a hard modeling, identification, optimization or cyber-physical testing problem. We are developing open-source tools and validating ideas on real systems at Purdue. Let us find a useful research question together.” Point to the repository, worksheet, math review and contribution links. Welcome ecosystem partners. Answer final questions and stop at 13:00. Appendix A3 covers research directions if asked.

## A1 · Exact-real proofs and numerical evidence
Time: Appendix
Layout: image
Visual: ../results/reference/math_audit.png
Badge: Scope matters · MATH_REVIEW.md

- Lean: equation equality and invariants
- Audit: gradients, profiles, integration
- Papers: model and method choices

Checkpoint: None of these certify arbitrary edits or real flight.
Notes:
Lean 4.29.1 and public Mathlib v4.29.1 are pinned. The proof representation comes from the actual Solve operation program. No admissions or custom axioms; standard propext, Classical.choice and Quot.sound only. The compiler/template/translator and real-arithmetic interpretation remain trusted. Assumptions: nonnegative coefficients, positive smoothing, nonzero mass/inertia for energy algebra. The profile threshold is asymptotic Gaussian; a finite grid does not guarantee confidence coverage.

## A2 · Primary papers behind the approach
Time: Appendix
Layout: statement
Badge: Full citations and checked equations: MATH_REVIEW.md

- Faessler et al., RA-L 2018: rotor-drag physics and excitation
- Andersson et al., 2019: CasADi AD and multiple shooting
- Raue 2009; Wieland 2021: practical identifiability and profiles

Checkpoint: World-axis teaching drag differs from body-axis rotor aerodynamics.
Notes:
Faessler DOI 10.1109/LRA.2017.2776353, equation 2: mass-normalized body-frame R D Rᵀ drag; we do not invoke their flatness theorem. CasADi DOI 10.1007/s12532-018-0139-4, sections 2.6 and 5.4: AD and multiple shooting. Journal: Mathematical Programming Computation. Raue DOI 10.1093/bioinformatics/btp358, primary abstract; Wieland arXiv 2102.05100, equation 6/full method checked. No paper figures or extensive quotations are reproduced.

## A3 · Research questions worth exploring
Time: Appendix
Layout: cards
Badge: FUTURE WORK · beyond the tested app experiments

- Vision + SLAM + estimation + physics in one declared system
- Richer browser / FMI / WebAssembly workflows
- Compiler differentiation and larger symbolic systems
- Partition work across CPU, GPU and embedded hardware

Checkpoint: Bring a falsifiable question and a measurable benchmark.
Notes:
The app gallery demonstrates selected browser interactions; it does not establish complete SLAM, deployable SLAM FMUs, automatic hardware partitioning or million-variable scaling. Agent-assisted development does not supply mathematical validation by itself. Use this appendix for roadmap questions only; no extra scheduled time. Recovery instructions remain in TROUBLESHOOTING.md and REHEARSAL.md.

## A4 · Numerical constraints need validation
Time: Appendix
Layout: wide
Visual: ../results/reference/optimization.png
Badge: Node solution ≠ exact continuous-time flight

- Reintegrate the inputs independently; inspect errors by physical unit.
Checkpoint: Small defects, pitch margin and fine rollout are separate checks.
Notes:
Default physical constraints: T 0–20 N, torque ±0.35 N m, pitch ±0.55 rad (nodes ±0.54), altitude 0.25–4 m, rotor pairs 0–10 N. Finer/adaptive peak pitch is about 0.542 rad. No interval-bound certificate, actuator dynamics or feedback is provided. IPOPT solves a local NLP. Active bounds can differ by about 1e−8 from floating-point solver tolerance; checks allow 1e−6. RK4 verification uses dt=0.025 s; DOP853 output samples are 0.01 s. These numerical checks are separate from exact-real Lean proofs.
