# Hands-On with Rumoca

Editable source for both workshop.pptx and workshop.pdf. Build with:
`uv run --frozen --group slides python scripts/build_slides.py`.
Notes are included in the presentation; Checkpoint appears on the slide.
Main slide times are contiguous and total 180 minutes, including two breaks.

## 01 · Hands-On with Rumoca
Links: Repository | https://github.com/CogniPilot/rumoca_workshop_amc2026 ; Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md ; Create Codespace | https://codespaces.new/CogniPilot/rumoca_workshop_amc2026?quickstart=1
Time: 10:00–10:05
Layout: title
Visual: assets/repo-qr.png
Photo: assets/purt-facility.png
Purdue logo: assets/purdue-logo.png
Penn State logo: assets/penn-state-logo.png
NXP logo: assets/nxp-logo.png
Presenter 1: James Goppert
Role 1: Managing Director, PURT · Research Assistant Professor
Presenter 2: Micah Condie
Role 2: PhD student · School of Aeronautics and Astronautics
Badge: American Modelica Conference · October 12, 2026

- James Goppert · Micah Condie
- Purdue University · School of Aeronautics and Astronautics
- Georgia Tech · 10:00–13:00
- Any modeling domain welcome · no aerospace background needed

Checkpoint: Scan to create the core Codespace · materials linked below
Notes:
Welcome to Hands-On with Rumoca. Lead with the reason to care: “We want your declared physics to travel into simulation, identification, optimization and verification without silently becoming different models. Today you will take one small Modelica model through simulation, fitting and a constrained flight plan.” Introduce James Goppert as Managing Director of the Purdue UAS Research and Test Facility (PURT) and Research Assistant Professor in Purdue’s School of Aeronautics and Astronautics. Introduce Micah Condie as his PhD student in that school. Explain that PURT connects modeling with motion capture, closed-loop experiments and flight validation; the facility photograph comes from the supplied PURT overview deck. Acknowledge Penn State’s firmware-rehosting research collaboration and the NXP hardware ecosystem; the small logos identify these contributors and platforms, not additional workshop presenters. Welcome the Georgia Tech audience. Point to the QR and ask attendees to keep the participant worksheet open. No aerospace background is required. Welcome models and expertise from other disciplines; the closing slide has concrete ways to join the work. Allow five minutes for arrivals and orientation; announce the optional experiment challenge on the next slide.

## 02 · Run the core. Explore your own question.
Links: Challenge rules | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/CHALLENGE.md ; Example prompts | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/APP_PROMPT.md
Time: 10:05–10:10
Layout: cards
Badge: OPEN EXPERIMENT CHALLENGE · demos + audience vote at 12:50

- Core: edit a model, fit data, optimize a trajectory
- Apply Rumoca to a problem you care about
- One change in an existing model or simulator is enough
- Audience favorite wins a CogniPilot stocking cap

Checkpoint: Enter by 12:40 · up to 5 demos · CHALLENGE.md · hosting optional
Notes:
Announce the challenge now: “Explore a question you care about with Rumoca. Change an existing model, controller or interactive simulator during downtime. Show the effect and explain one result you checked. The audience favorite wins a free CogniPilot stocking cap.” A new app, WASM build, public GitHub repository, deployment and coding-agent subscription are optional. Power users can work with agents; manual experiments are welcome too. Point to the short experiment prompt in APP_PROMPT.md. An interactive Falcon 9-style landing experience is creative inspiration, not a supplied or qualified rocket starter. Welcome equally small experiments from other domains. Full Three.js apps and AD-based fixed-wing MPC are optional stretches; MPC is ambitious. The core Modelica → JAX → CasADi exercises remain the main activity. Entries close at 12:40: collect name/team, question, starting model/app, original change, tool, elapsed work time and a ready interaction or before/after comparison. A local tab, file or screenshare is enough; public links are voluntary. One entry per participant or team. Up to five ready experiments present at 12:50 for 45 seconds; if more are ready, draw five plus a backup and presentation order. Announce by 12:45. Selection is not a quality judgment. Each demo includes question, change, result, one check, tool used and elapsed time, with estimates labeled. Audience members each vote once by show of hands. Ask for a show of hands for Modelica/JAX/CasADi experience. Today's data are synthetic and the trajectory is open loop.

## 03 · Why Rumoca? One model, many questions.
Links: Rumoca compiler | https://github.com/CogniPilot/rumoca ; Model library | https://github.com/CogniPilot/modelica_models ; Cerebri RDD2 | https://github.com/CogniPilot/cerebri_rdd2
Time: 10:10–10:15
Layout: research
Badge: Purdue + CogniPilot · how we are using declared mathematics

- Lie group theory: Represent rotations and motion with their geometric structure.
- Reachable sets: Bound possible behavior of cyberphysical systems under uncertainty.
- Formal software verification: Connect model equations to explicit proof obligations.
- System identification + digital twins: Fit physical parameters; compare simulation with experiments.

Checkpoint: Goal: mathematical guarantees for specified properties under explicit assumptions.
Notes:
Ask first: “How many versions of the same physics do you maintain?” Independently maintained simulation, fitting and control models drift apart. The payoff is a shared source that lets us compare tools without silently changing the plant. Attendees bring Modelica knowledge and models from domains beyond aerospace; that breadth is valuable to the research community. We are building a unified, declarative modeling and simulation environment for cyberphysical systems. Modelica expresses physical intent as equations, so execution choices can change without rewriting that intent. We want declared physics and mathematical structure to travel across computational tools, so we can inspect equations, compare implementations and check assumptions. Rumoca is our open Modelica compiler for this workflow. Explain our broader uses in plain language: Lie group theory keeps rotations and rigid-body motion geometrically structured; reachable-set computation asks which states may be possible under bounded initial conditions and disturbances; formal software verification connects specified properties to proof obligations; system identification and digital twins connect models with measured behavior and experiments. The CogniPilot modelica_models library includes LieGroups SO(2), SO(3), SE(2), SE(3), SE_2(3), geometric estimation/control, and pure functions intended for verification and reachable-set propagation. These functions are building blocks, not complete safety certificates. Show the Cerebri RDD2 deployment strip: our Zephyr-based autopilot takes Modelica controllers and estimation through Rumoca eFMI Production Code to C running on a real drone. Its current documented path is CRSF → generated control/estimation → quad-X mixer → DSHOT, with ACRO and AUTO_LEVEL modes. The build generates Vehicles.Rdd2.Controller and Estimation.ComplementaryAttitude from the shared modelica_models library. Source: https://github.com/CogniPilot/cerebri_rdd2. Mathematical guarantees must name a property and its assumptions; carrying verified model/controller properties through code generation, scheduling, sensors and actuators is a research goal. Neither eFMI generation nor this workshop’s planar-model proofs certify the complete Cerebri firmware, Zephyr RTOS or physical flight. Fast Monte Carlo/RL, native AD and heterogeneous compute remain further research directions. Today uses a compact planar model, synthetic data, JAX fitting, CasADi trajectory optimization and a scoped Lean companion proof. It does not demonstrate a full Lie-group vehicle, compute a reachable tube, certify generated machine code or validate a physical digital twin. References: https://github.com/CogniPilot/modelica_models; Solà, Deray and Atchuthan, A micro Lie theory for state estimation in robotics, https://arxiv.org/abs/1812.01537; Althoff, Frehse and Girard, Set Propagation Techniques for Reachability Analysis, https://doi.org/10.1146/annurev-control-071420-081941. These support the mathematical ideas, not a claim that Rumoca implements every cited algorithm. Welcome questions from any discipline; the workshop needs no aerospace background.

## 04 · Declare once. Ask different questions.
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
Time: 10:15–10:20
Layout: bridge
Visual: assets/architecture.png
Photo: assets/purt-fixed-wing.jpg
Badge: Verified workshop architecture

- Quadrotor.mo → JAX + CasADi · the same declared equations

Checkpoint: Modelica declares physics · Rumoca compiles · backends compute.
Notes:
The fixed-wing photograph, from the PURT overview, shows the physical experiment side of the digital-twin workflow. Connect modeling, identification and optimization with measured flight; this photographed aircraft is contextual, not the planar exercise model. Explain that VS Code is the authoring/LSP path and the playground is browser modeling/simulation. Python 0.10.2 exports JAX and CasADi; deployed browser 0.8.13 is separate. Open examples/simulate.py and point to rum.Session().load(...) then model.to_jax(); open examples/optimize_casadi.py and point to model.to_casadi(). Python code performs integration and builds optimization objectives, not another plant. Full language/backends are not certified by this example. The compiler structure is an extension seam for solver specialization and heterogeneous compute. Fast Monte Carlo and RL, native AD or JAX/CasADi/PyTorch integrations, and extensible targets are research directions. Today's core qualifies particular CPU exports; the guide and small Torch target are separate demonstrations, not a general hardware-partitioning or throughput claim.

## 05 · Everyone gets a browser plot
Links: Open playground | https://rumoca.cognipilot.org/playground/ ; Browser model | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/browser/Quadrotor_browser.mo
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
Links: Local VS Code setup | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/LOCAL_SETUP.md ; Create Codespace | https://codespaces.new/CogniPilot/rumoca_workshop_amc2026?quickstart=1 ; Recovery help | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/TROUBLESHOOTING.md
Time: 10:25–10:30
Layout: cards
Badge: Setup decision · worksheet has every link

- Local container: Docker + Reopen in Container
- Codespaces: same container; login and allowance
- Local uv: optional native installation
- Browser or pair: keep working during setup

Checkpoint: Switch route after ten minutes of setup trouble.
Notes:
Codespaces URL https://codespaces.new/CogniPilot/rumoca_workshop_amc2026?quickstart=1. Codespaces requires an account with allowance or billing enabled. Cloud qualification is recorded in VERIFICATION.md; account availability varies. Local: download/extract ZIP, install uv/extension, uv sync --frozen. Python and released editor are qualified on Linux/Windows x64 and macOS Intel/Apple Silicon. The local Dev Container route uses the same configuration as Codespaces: install Docker and the VS Code Dev Containers extension, open the workshop folder, run Dev Containers: Reopen in Container, and select the core workshop. Wait for WORKSHOP PASS. No host uv or Nix is required. Docker Desktop uses Linux containers / WSL 2 on Windows; Docker Engine works on Linux. Native uv remains an optional route.

## 07 · Configure the experiment, then run it
Links: Simulation walkthrough | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md ; Scenario model | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/models/BrowserFlight.mo
Time: 10:30–10:35
Layout: statement
Badge: VS CODE · lightning bolt creates the TOML

- Open BrowserFlight.mo → click the lightning bolt
- Save scenario TOML → model, source roots, solver, end time
- Run the scenario → inspect vx and x

Checkpoint: Modelica owns physics · TOML owns the run configuration.
Notes:
Start with the .mo file, not a settings icon. Open models/BrowserFlight.mo, which binds the same Quadrotor plant to level hover thrust, zero torque and initial horizontal speed 6 m/s. Click the lightning-bolt Create Rumoca Scenario icon; the Command Palette fallback is Rumoca: Create Rumoca Scenario. Save the generated rumoca-scenario.…toml beside the model. The selected model is BrowserFlight; inspect the scenario editor and text view. Set source_roots=["."], model.file="BrowserFlight.mo", model.name="BrowserFlight", sim.solver="auto", sim.t_end=8.0 and viewer.mode="results_panel". Save and Run Current Rumoca Scenario. Inspect speed decay and increasing position. Explain that solver and horizon are experiment choices, while Modelica declares physics. The core plant has free inputs; this wrapper defines an experiment. Python later supplies a different prescribed input experiment. Do not compare native coast distances directly to the Python maneuver values. Hover/completion can be checked briefly while opening the model. Let attendees create the TOML themselves; do not paste a prepared scenario first. See WORKSHOP.md for fallback commands and settings. If the editor run is unavailable, use the Python experiment and clearly label that alternate route.

## 08 · The user guide is a live modeling lab
Links: Open NACA example | https://cognipilot.github.io/rumoca/user-guide/language/arrays-pde.html#2-d-navierstokes-flow-over-a-naca-2412-airfoil ; Explore user guide | https://cognipilot.github.io/rumoca/user-guide/
Time: 10:35–10:40
Layout: image
Visual: assets/user-guide-naca.png
Badge: LIVE DEMO · NACA 2412 · embedded editor + WebGPU

- Edit StopTime: 30 → 2 s
- Simulate; select the final frame
- Switch vorticity / pressure

Checkpoint: User-guide link and recovery: WORKSHOP.md · no install needed
Notes:
Use the deployed user guide as a workshop resource, not only a reference manual. Open https://cognipilot.github.io/rumoca/user-guide/language/arrays-pde.html#2-d-navierstokes-flow-over-a-naca-2412-airfoil. This page embeds Monaco editors, simulation controls, plots and custom visualizations; it also has turkey heating and a vibrating membrane for other domains. Find AirfoilFlow, change StopTime = 30 to 2, leave NX=30 and NY=18, keep GPU checked and Interactive off, then Simulate. Move the time slider to the final frame and switch Field between Vorticity and Pressure. Our rehearsal used Chromium with a software WebGPU adapter; it demonstrates execution and UI, not a hardware speed claim. The NACA contour and coarse artificial-compressibility/penalization flow field make declared array equations visible; this is a qualitative teaching model, not a validated lift/drag or aircraft design calculation. If WebGPU is unavailable or the short run fails, show the labeled saved capture and continue. Do not try the unqualified CPU NACA route during this five-minute segment. The browser guide is a separately deployed compiler/runtime from the pinned Python release. Keep the warm successful tab ready before class; participants can revisit these editors during downtime.

## 09 · A planar quadrotor we can inspect
Links: Open vehicle model | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/models/Quadrotor.mo ; Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
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

## 10 · Your first engineering change: drag
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md ; Open playground | https://rumoca.cognipilot.org/playground/
Time: 10:45–10:55
Layout: wide
Visual: assets/drag-law.png
Badge: HANDS-ON · predict before running

- Change k_quad = 0.0 to 0.08, save, then simulate.
Command: uv run --frozen python examples/simulate.py
Checkpoint: What changes at high speed? What about negative velocity?
Notes:
Explain units kl N s/m,kq N s²/m²,epsilon .01 m/s. Smooth componentwise law approximates |v|v and never adds energy for nonnegative coefficients; Lean proves the signs and smoothing bound. It differs from Faessler et al.'s body-frame rotor-drag model; do not claim their flatness theorem. Allow 7–8 minutes editing/predicting. Browser users make the same coefficient change and Play again. Default parameter changes affect simulation; fitting estimates parameters explicitly.

## 11 · More drag, less distance
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
Time: 10:55–11:00
Layout: wide
Visual: assets/simulation-hero.png
Badge: HANDS-ON · same prescribed Python inputs

- Reference at 8 s: 41.60 m → 17.97 m
Checkpoint: Compare your current default with the two reference cases.
Notes:
Open the actual live plot and ask participants to explain the sign. The slide plot uses emitted JAX equations and reference parameters; not real flight data. Browser wrapper coasts at level hover, so its numbers differ. Optional kl=.30 then restore .18. Presenter solution is an inheritance override, not a second dynamics implementation. Take two questions. End on time for break.

## 12 · Break · back at 11:10
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
Time: 11:00–11:10
Layout: break
Badge: Ten full minutes

- Keep your editor and terminal open.
- Your simulation plot is the recovery point.
- Next: learn drag from noisy data.
Checkpoint: Worksheet and commands: WORKSHOP.md · scan the opening QR.
Notes:
Actually pause for ten minutes. Help only small recovery questions; avoid turning the break into a lecture. Browser-only attendees can pair for the next exercise. Keep the next command in the worksheet, not a wall of terminal text.

## 13 · Known experiment. Unknown coefficients.
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
Time: 11:10–11:20
Layout: wide
Visual: assets/data-hero.png
Badge: Synthetic data · seed 20261012

- Three training flights; one held-out flight. 20 Hz, 8 s each.
Checkpoint: Speed variation helps separate linear and quadratic drag.
Notes:
Data generated by Rumoca CasADi + independent adaptive DOP853; JAX fit uses RK4. Position noise .025 m; velocity .035 m/s; angles/rates also noisy, but only exact initial angles/rates enter the fit. Commands and initial state assumed known. Holdout has different excitation and negative initial speed. The data are synthetic. Explain how real logs would bring actuator timing, wind and sensor bias. Truth is reporting only.

## 14 · Differentiate the prediction error
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
Time: 11:20–11:30
Layout: wide
Visual: assets/fit-workflow.png
Badge: JAX autodiff through generated physics + RK4

- Positive parameters; noise-scaled loss; bounded optimization
Checkpoint: JAX provides gradients. SciPy updates the coefficients.
Notes:
Show fit script's p_from_log, residual, value_and_grad, minimize. Each coefficient divided by one native SI unit equals exp(log parameter), so the logarithm is dimensionless; fitted bounds .001..2 in native units. Mean residual² divided by known noise variance is dimensionless, over x,z,vx,vz. Avoid differentiating noisy acceleration estimates. JAX derivative is of the implemented discrete rollout; finite differences are checks. The system ID is not an autodiff proof of model correctness. Participants can run the next command and inspect the provided algorithm.

## 15 · Run the fit. Test the held-out flight.
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
Time: 11:30–11:50
Layout: wide
Visual: assets/fit-hero.png
Badge: HANDS-ON · estimates ≈ 0.18042 and 0.07991

- Open fit_drag.png and fit_drag.json; compare before and after.
Command: uv run --frozen python examples/fit_drag_jax.py
Checkpoint: Two coefficients · lower loss · improved held-out prediction
Notes:
Give at least 15 minutes for running the fit, inspecting outputs and individual questions. Participants who finish can return to the experiment challenge. Reference truth kl=.18 N s/m, kq=.08 N s²/m². Loss roughly 26932→1.073, about 25000×. Read rms_by_state with separate units or noise_scaled_rms; avoid calling mixed-unit legacy RMS metres. Recovery --one-coefficient assumes known kl=.18. Stretch: different initial guess; audit already checks six. Do not use holdout to tune parameters during this exercise. If live fails, label reference plot honestly.

## 16 · Check your result. Keep building.
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
Time: 11:50–11:55
Layout: cards
Badge: Checkpoint · go deeper at your own pace

- Open your before-and-after prediction plot
- Compare the held-out flight and fitted values
- Stretch: rerun from another starting guess
- App builders: keep your prototype moving

Checkpoint: Fit complete? Continue your experiment or explore the optional checks.
Notes:
Spend one minute showing where the result files are and four minutes on independent work and questions. Ask whether the held-out prediction improved; no aerospace background is needed. App builders can continue the open challenge. Offer detailed gradient, excitation and proof discussion only when requested, using MATH_REVIEW.md. The audit checks six starting guesses, twelve noise seeds, Jacobians, analytic coasting and re-optimized profiles. Lean checks scoped exact-real equation equality and invariants; numerical and statistical claims have separate evidence.

## 17 · Make a target. Learn a policy.
Links: Backend walkthrough | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/BACKENDS.md ; Torch target.toml | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/templates/torch-ode/target.toml ; Lean Jinja target | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/templates/lean-proof/rhs.lean.jinja
Time: 11:55–12:00
Layout: wide
Visual: ../results/reference/torch_policy.png
Badge: EXTENSIBILITY DEMO · same vehicle · Linux CPU / Codespaces

- target.toml → generated Torch → differentiable policy learning
Command: uv run --frozen --group torch python scripts/learn_hover_torch.py
Checkpoint: Held-out cost ≈ 0.116 → 0.021 · optional instructions: BACKENDS.md
Notes:
Show templates/torch-ode/target.toml: ir="solve", explicit capabilities and output template. Open rhs.py.jinja and the generated/torch-ode/Quadrotor_torch.py output. The small external target maps the actual scalar Solve operations to Torch; it does not handwrite the vehicle dynamics or require a Rust compiler change. The target passes 101-point batched RHS comparisons, JAX/CasADi Jacobians, forward/reverse AD, finite differences and rejection gates. Use the optional preinstalled Torch environment in the Codespace; do not ask all attendees to download the extra CPU package during the five-minute demonstration. Run or show learn_hover_torch.py: two positive feedback gains learned through the same generated six-state vehicle's RK4 rollout, restricted to vertical hover with zero torque. Sixty Adam updates on 64 initial conditions; test on 128 new initial conditions. The dimensionless held-out cost drops about .116 to .021; complete objective gradients and fixed-sampling finer-integration checks pass. Call this differentiable model-based policy optimization, a bridge to RL, not PPO/DQN or full-flight autonomy. Known fixed drag coefficients are used for this separate teaching task. Source/template provenance is saved with results. The full target supports a small scalar ODE subset and rejects events/unsupported primitives. Invite compiler contributors to add one primitive and compare its derivatives before declaring support. This is one concrete extension seam toward fast Monte Carlo/RL, native AD or JAX/CasADi/PyTorch integrations and solver specialization for heterogeneous compute. Broad automatic partitioning and performance scaling remain research directions. Primary context: Heess et al. 2015 https://arxiv.org/abs/1510.09142. Stop at noon for a full break.

## 18 · Break · back at 12:10
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
Time: 12:00–12:10
Layout: break
Badge: Ten full minutes

- Keep your fitted coefficients.
- Next: plan a flight using your fit.
- Your fit plot is the recovery point.
Checkpoint: Same Modelica source; now compile to CasADi.
Notes:
Ten-minute break. Confirm most pairs have fit outputs. Do not edit the model again after fitting; a source hash will require refitting if it changes. Presenters have successful reference fit and primal trajectory warm start. No Mathlib or extra packages are needed for next exercise.

## 19 · Move between hovers, respect limits
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
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

## 20 · Solve. Inspect. Explain the braking.
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
Time: 12:20–12:40
Layout: wide
Visual: assets/control-hero.png
Badge: HANDS-ON · fitted physics, constrained trajectory

- Open optimization.png and optimization.json.
Command: uv run --frozen python examples/optimize_casadi.py
Checkpoint: Solve_Succeeded · limits respected · arrive near rest
Notes:
Allow about 15 minutes to run and inspect plots/JSON, with the remaining time for questions or app development. Live computation takes about 1–2 seconds locally. Show acceleration tilt and opposite tilt for braking. Confirm drag matches JAX values, defects near 1e−14, exact endpoint constraints at nodes, and about 2 mm altitude error under finer/adaptive integration. Analytic interval pitch extrema are about 0.542 rad, below 0.55. Checks allow 1e−6 numerical tolerance. Explain continuous/discretized differences and the absence of an all-time formal certificate. A source hash requires refitting after edits. Recover with canonical source/reference fit, then a clearly labeled reference figure. Optional --target-x 3 was separately rehearsed; its receipt is in verification/. MPC would repeat optimization online; it is not demonstrated.

## 21 · Next up: pylon racing at PURT
Links: PURT pylon racing | https://pylon-racing.geddes.rcac.purdue.edu/ ; Watch race video | https://github.com/CogniPilot/rumoca_workshop_amc2026/releases/download/workshop-amc2026-r3/purt-fpv-chase.mp4 ; Challenge rules | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/CHALLENGE.md
Time: 12:40–12:45
Time group: Physical experiments
Layout: race
Visual: assets/pylon-qr.png
Movie: media/purt-fpv-chase.mp4
Poster: assets/purt-fpv-chase-poster.jpg
Video link: https://github.com/CogniPilot/rumoca_workshop_amc2026/releases/download/workshop-amc2026-r3/purt-fpv-chase.mp4
Badge: Purdue UAS Research and Test Facility · upcoming competition

- Design, simulate, then flight-test your autonomy
- The next competition will leverage Rumoca
- Digital twin → real aircraft at PURT

Checkpoint: pylon-racing.geddes.rcac.purdue.edu
Notes:
Advertise the upcoming autonomous fixed-wing pylon racing competition at Purdue UAS Research and Test Facility (PURT). Say: “The next competition will leverage Rumoca. Build your autonomy, learn in a digital twin, and bring it to the experiment.” Point attendees to https://pylon-racing.geddes.rcac.purdue.edu/ for announcements and information. The published competition format connects software-in-the-loop digital-twin simulation with physical flight tests; current public dated details are for the April 2026 edition, so do not announce those dates as upcoming. Future-event dates, registration, rules and exact Rumoca integration will be announced by the organizers. Play 20–30 seconds of the embedded September 2025 PURT FPV chase recording to show actual fixed-wing flight; pause before continuing. The complete 5:58 video is embedded as compressed 1080p H.264/AAC, with a downloadable MP4 fallback and a clickable poster in the PDF. The original user-provided SharePoint recording and matching local movie are the source. This is past event footage, not a newly announced event date. Keep the original 4K file as the quality master; no conference-network streaming is needed for the PPTX. Official facility source: https://engineering.purdue.edu/PURT. Public CogniPilot workspace https://github.com/CogniPilot/cognipilot_workspace documents pure Modelica, host Zephyr SIL and FastDyn/QEMU Cortex-M7 binary-in-the-loop; those paths were not executed here. Synthetic fitting does not establish real-aircraft validity. Briefly connect today's model → identify → optimize workflow with racing and physical validation. Collect challenge entries at 12:40, draw if more than five are ready, and announce presenters/order by 12:45. Move to the fixed-wing workbench at 12:45.

## 22 · FastDyn: fly the firmware against declared physics
Links: FastDyn demo guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/FASTDYN.md ; BoardRunner paper | https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html ; FastDyn source | https://github.com/jgoppert/FastDyn ; Recorded Monte Carlo | https://github.com/CogniPilot/rumoca_workshop_amc2026/releases/download/workshop-amc2026-r3/fastdyn-monte-carlo.mp4
Time: 12:40–12:45
Time group: Physical experiments
Layout: firmware
Visual: assets/fastdyn-monte-carlo-poster.png
Movie: media/fastdyn-monte-carlo.mp4
Video link: https://github.com/CogniPilot/rumoca_workshop_amc2026/releases/download/workshop-amc2026-r3/fastdyn-monte-carlo.mp4
Badge: Arslan Khan’s group · Penn State + Purdue · BoardRunner, CCS ’26

- Modelica → Rumoca FMI 3 plant
- ArduPilot firmware → FastDyn / QEMU
- Recorded: 100 paired wind scenarios
- Try: 3 load trials in a FastDyn Codespace

Command: uv run --frozen python scripts/fastdyn_demo.py
Checkpoint: Choose the FastDyn container · open results/live/fastdyn/trajectories.png
Notes:
Credit Arslan Khan’s group at Penn State and the Penn State/Purdue collaboration. Cite Muhammad Hammad Bashir, Michael Rooney, Colin Smith, Dongyan Xu and Arslan Khan, “BoardRunner: Automatic Firmware Rehosting using High-Fidelity Compositional Device Models,” ACM CCS 2026. The accepted-paper program verifies the title and authors: https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html. BoardRunner is the firmware-rehosting work; the Rumoca/FMI coupling and workshop campaign are integration examples, not results attributed to that paper. Play the supplied 30-second public Monte Carlo recording. Its documented study compares 100 paired wind scenarios / 200 firmware-in-the-loop flights with and without ideal modeled current-based compass compensation; it uses a generic quadrotor and ArduCopter 4.7.0. It is separate recorded research evidence, not today’s three-load campaign (ArduCopter 4.6.2), and was not independently rerun by this workshop. The ideal compensation uses known synthetic coupling/current, empirical trajectories are not a reachable-set proof, and results do not establish field failure probabilities. Preserve the supplied drone-mesh CC BY 4.0 attribution; see slides/media/README.md. Instruction-counted virtual time coordinates firmware and plant steps. Follow the loop: firmware actuator command → FMU motor/rigid-body dynamics → simulated sensor values → firmware. This executes a rehosted hardware firmware binary, rather than ArduPilot SITL. The optional FastDyn configuration uses its own pinned Rumoca 0.10.0, separate from the workshop Python 0.10.2. The three-run example holds the vehicle, gains and mission fixed, applies prescribed external payload weight at a motor, and records seed, sources, telemetry, completion and failure reasons. It does not change inertial mass or simulate swinging payload motion. Three samples do not estimate rare-event probabilities or establish safety. Launch from https://github.com/codespaces/new/CogniPilot/rumoca_workshop_amc2026 using New with options and select FastDyn + Rumoca: optional firmware Monte Carlo, rather than the default core configuration. Then run the displayed command in its VS Code terminal, or select Terminal → Run Task → Workshop: optional FastDyn Monte Carlo. Open results/live/fastdyn/trajectories.png and compare the three flights; seed, sources, firmware logs and outcome summaries are retained. The pinned optional environment was created and the reference, 100 g endpoint and one seeded 87.7 g trial all completed the mission and landing in an actual two-core Codespace, taking about 74, 68 and 61 seconds after setup. Show the saved plot if the network is slow. See docs/FASTDYN.md for setup, storage and scope. Main workshop remains model → simulate → identify → optimize. Solver specialization, heterogeneous compute, batched Monte Carlo/RL and extensible AD targets remain research directions.

## 23 · Explore the fixed-wing workbench
Links: Try fixed-wing | https://cognipilot.github.io/rumoca_fixed_wing/ ; Source code | https://github.com/CogniPilot/rumoca_fixed_wing ; Experiment guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/BROWSER_APPS.md
Time: 12:45–12:50
Time group: App showcase
Layout: image
Visual: assets/app-rumoca_fixed_wing.png
Badge: AGENT-BUILT APPS · try fixed-wing or finish your own demo

- Modelica flight simulation + autopilot
- Try 50 Hz → 20 Hz, restart, then observe
- Change a setting. Check what changes.

Checkpoint: Live links + short experiments: BROWSER_APPS.md
Notes:
Lead with rumoca_fixed_wing, the more complete app example. Coding agents helped build the interface and experiments; engineers review models and validate output. Briefly show Autopilot → Start sim, waypoint progress, then 50 to 20 Hz → Start sim again → pause. Invite participants to try that interaction or finish their challenge app. SLAM Lab is an additional example in development; only its inertial baseline and filter variant were rehearsed, not the complete visual-SLAM pipeline. Mocap is a viewer for stored benchmark results, not browser retraining. Fixed-wing and SLAM use WASM; the tested mocap viewer interaction does not. No login, agent account or API key is needed to explore these examples manually. They use different models from the core exercise and are outside its Lean proof scope. Keep the recorded screenshots available for network/graphics recovery. At 12:50 move to participant demos.

## 24 · Explore motion-capture identification
Links: Try the app | https://cognipilot.github.io/mocap_sysid/ ; Source code | https://github.com/CogniPilot/mocap_sysid ; Experiment guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/BROWSER_APPS.md
Time: 12:45–12:50
Time group: App showcase
Layout: image
Visual: assets/app-mocap_sysid.png
Badge: AGENT-BUILT APPS · explore your own scientific question

- Visualize vehicle data and model structure
- Compare experiments and data splits
- A viewer for exported benchmark results

Checkpoint: Explore exported identification results.
Notes:
Show the stored synthetic 6-DOF open-loop example and its model structure. This viewer does not train models or execute a WASM simulation. Recorded benchmark data is distinct from a live fit. Invite users to explore a problem or dataset from their own domain; do not invent method scores. Together with the neighboring app slides, share the five-minute showcase slot.

## 25 · Explore SLAM Lab · in development
Links: Try the app | https://cognipilot.github.io/slam_web/ ; Source code | https://github.com/CogniPilot/slam_web ; Experiment guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/BROWSER_APPS.md
Time: 12:45–12:50
Time group: App showcase
Layout: image
Visual: assets/app-slam_web.png
Badge: AGENT-BUILT APPS · explore your own scientific question

- Try the inertial estimation baseline
- Inspect RGB, depth and trajectories
- Visual SLAM and loop closure are in development

Checkpoint: Start with the tested inertial baseline.
Notes:
Show the tested InertialOnly or ResponsiveInertial model. This is an additional app in development, with a browser WASM path; the full visual-SLAM pipeline was not qualified. Point out the declared estimator model. Invite users to explore the supported baseline or continue their challenge. Together with the neighboring app slides, share the five-minute showcase slot.

## 26 · Show your experiment. Vote for the cap.
Links: Challenge rules | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/CHALLENGE.md ; Optional gallery | https://github.com/CogniPilot/rumoca_workshop_amc2026/issues/1
Time: 12:50–12:55
Layout: statement
Badge: OPEN CHALLENGE · short demos · audience show of hands

- Up to 5 demos · 45 seconds each · local or browser
- One checked result · tool used · elapsed work time
- Audience favorite wins a free CogniPilot stocking cap

Checkpoint: Random draw if more than 5 ready entries → audience hand vote
Notes:
Use up to five 45-second demos, selected by the announced readiness check and random draw if needed. Draw order and a backup in advance. Each entrant shows a question Rumoca helps explore, their original change, a working interaction or before/after comparison, one checked result, tool used and elapsed work time. Local files, browser tabs and screenshares are acceptable; public source links are optional. Manual experiments are welcome; name the agent if used and label estimated times. Have tabs/files ready and use the same limit for everyone. Five demos leave 75 seconds for a hand vote and award. Each attendee votes for one entry; count visibly. If tied, run a quick vote between the tied entries; if still tied, draw among them. Award one stocking cap; a team chooses its recipient. Share voluntary links from all entries, including those not drawn. If no entries are ready, take a brief question and continue. CHALLENGE.md carries the same rules. Keep the core exercise as the workshop's main focus.

## 27 · Bring your model. Join the work.
Links: Join the community | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/COMMUNITY.md ; Rumoca compiler | https://github.com/CogniPilot/rumoca ; Model library | https://github.com/CogniPilot/modelica_models
Time: 12:55–13:00
Layout: title
Visual: assets/community-qr.png
Badge: Your Modelica expertise can move this research forward

- Bring a model or a question from your own domain
- Add a validation case, model library or compiler fix
- Start a conversation: problem + model + one check

Checkpoint: Scan to join the work · COMMUNITY.md · questions welcome
Notes:
Use a concrete invitation: “You already bring Modelica knowledge we need. Bring a model from your domain, one scientific question, and one result we can check together. Help us make declared mathematics reusable across simulation, identification, optimization and verification.” The community QR opens COMMUNITY.md, with a research/model collaboration issue form and links to the compiler and model library. Modelers can contribute small models with units and expected behavior; researchers can propose a measurable identification, geometry or verification question; software contributors can share a minimal compiler/backend reproduction or improvement. No aerospace background or coding-agent subscription is needed. Invite attendees to speak with James Goppert or Micah Condie before leaving, then continue through the public collaboration form. Ask: “Which model from your work would you try next?” Allow answers and questions rather than reading the bullets. The first step is a small shared check, not an implied promise of a certified full-system workflow. Point to today's tested source/results and MATH_REVIEW.md as an example of evidence we can build together. Stop at 13:00. Link to MATH_REVIEW.md for detailed proofs and references.

