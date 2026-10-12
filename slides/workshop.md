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
Badge: American Modelica Conference Workshop 2026

- James Goppert · Micah Condie
- Purdue University · School of Aeronautics and Astronautics
- October 12, 2026 · 10:00–13:00
- Any modeling domain welcome · no aerospace background needed

Checkpoint: Scan to create the core Codespace · materials linked below
Notes:
Welcome to Hands-On with Rumoca. Lead with the reason to care: “We want your declared physics to travel into simulation, identification, optimization and verification without silently becoming different models. Today you will take one small Modelica model through simulation, fitting and a constrained flight plan.” Introduce James Goppert as Managing Director of the Purdue UAS Research and Test Facility (PURT) and Research Assistant Professor in Purdue’s School of Aeronautics and Astronautics. Introduce Micah Condie as his PhD student in that school. Explain that PURT connects modeling with motion capture, closed-loop experiments and flight validation; the facility photograph comes from the supplied PURT overview deck. Acknowledge Penn State’s firmware-rehosting research collaboration and the NXP hardware ecosystem; the small logos identify these contributors and platforms, not additional workshop presenters. Welcome the Georgia Tech audience. Point to the QR and ask attendees to keep the participant worksheet open. No aerospace background is required. Welcome models and expertise from other disciplines; the closing slide has concrete ways to join the work. Allow five minutes for arrivals and orientation; announce the optional experiment challenge on the next slide.

## 02 · Run the core. Explore your own question.
Links: Challenge rules | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/CHALLENGE.md ; Example prompts | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/APP_PROMPT.md ; Agent setup | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/AGENT_SETUP.md
Time: 10:05–10:10
Layout: cards
Badge: OPEN EXPERIMENT CHALLENGE · demos + audience vote at 12:50
Prompt: “Use Three.js and Rumoca to make an interactive Artemis rocket launch simulation. Let me vary payload or throttle and check one result.”

- Core: edit a model, fit data, optimize a trajectory
- Apply Rumoca to a problem you care about
- One change in an existing model or simulator is enough
- Audience favorite wins a CogniPilot stocking cap

Checkpoint: Enter by 12:40 · up to 5 demos · CHALLENGE.md · hosting optional
Notes:
Announce the challenge now: “Explore a question you care about with Rumoca. Change an existing model, controller or interactive simulator during downtime. Show the effect and explain one result you checked. The audience favorite wins a free CogniPilot stocking cap.” A new app, WASM build, public GitHub repository, deployment and coding-agent subscription are optional. Power users can work with agents; manual experiments are welcome too. Read the visible Artemis launch prompt as inspiration, then point to APP_PROMPT.md for a copyable prompt. No Artemis app is supplied or built for this workshop; a small educational vertical-ascent model is enough, with assumptions and one check. An interactive Falcon 9-style landing experience is creative inspiration, not a supplied or qualified rocket starter. Welcome equally small experiments from other domains. Full Three.js apps and AD-based fixed-wing MPC are optional stretches; MPC is ambitious. The core Modelica → JAX → CasADi exercises remain the main activity. Entries close at 12:40: collect name/team, question, starting model/app, original change, tool, elapsed work time and a ready interaction or before/after comparison. A local tab, file or screenshare is enough; public links are voluntary. One entry per participant or team. Up to five ready experiments present at 12:50 for 45 seconds; if more are ready, draw five plus a backup and presentation order. Announce by 12:45. Selection is not a quality judgment. Each demo includes question, change, result, one check, tool used and elapsed time, with estimates labeled. Audience members each vote once by show of hands. Ask for a show of hands for Modelica/JAX/CasADi experience. Today's data are synthetic and the trajectory is open loop.

## 03 · Why Rumoca? One model, many questions.
Links: Rumoca compiler | https://github.com/CogniPilot/rumoca ; Model library | https://github.com/CogniPilot/modelica_models ; Cerebri RDD2 | https://github.com/CogniPilot/cerebri_rdd2
Time: 10:10–10:15
Time group: Motivation
Layout: research
Badge: Purdue + CogniPilot · how we are using declared mathematics
Directions: Array-native research: vision, PDEs and differentiable aerodynamic design

- Lie group theory: Represent rotations and motion with their geometric structure.
- Reachable sets: Bound possible behavior of cyberphysical systems under uncertainty.
- Formal software verification: Connect model equations to explicit proof obligations.
- System identification + digital twins: Fit physical parameters; compare simulation with experiments.

Checkpoint: Goal: mathematical guarantees for specified properties under explicit assumptions.
Notes:
Ask first: “How many versions of the same physics do you maintain?” Independently maintained simulation, fitting and control models drift apart. The payoff is a shared source that lets us compare tools without silently changing the plant. Attendees bring Modelica knowledge and models from domains beyond aerospace; that breadth is valuable to the research community. We are building a unified, declarative modeling and simulation environment for cyberphysical systems. Modelica expresses physical intent as equations, so execution choices can change without rewriting that intent. We want declared physics and mathematical structure to travel across computational tools, so we can inspect equations, compare implementations and check assumptions. Rumoca is our open Modelica compiler for this workflow. Explain our broader uses in plain language: Lie group theory keeps rotations and rigid-body motion geometrically structured; reachable-set computation asks which states may be possible under bounded initial conditions and disturbances; formal software verification connects specified properties to proof obligations; system identification and digital twins connect models with measured behavior and experiments. The CogniPilot modelica_models library includes LieGroups SO(2), SO(3), SE(2), SE(3), SE_2(3), geometric estimation/control, and pure functions intended for verification and reachable-set propagation. These functions are building blocks, not complete safety certificates. Show the Cerebri RDD2 deployment strip: our Zephyr-based autopilot takes Modelica controllers and estimation through Rumoca eFMI Production Code to C running on a real drone. Its current documented path is CRSF → generated control/estimation → quad-X mixer → DSHOT, with ACRO and AUTO_LEVEL modes. The build generates Vehicles.Rdd2.Controller and Estimation.ComplementaryAttitude from the shared modelica_models library. Source: https://github.com/CogniPilot/cerebri_rdd2. Mathematical guarantees must name a property and its assumptions; carrying verified model/controller properties through code generation, scheduling, sensors and actuators is a research goal. Neither eFMI generation nor this workshop’s planar-model proofs certify the complete Cerebri firmware, Zephyr RTOS or physical flight. Fast Monte Carlo/RL, native AD and heterogeneous compute remain further research directions. Array-native mathematical models also connect vision, PDEs and differentiable aerodynamic design. We are experimenting with differentiable vortex-lattice methods for aircraft design; describe the goal as an XFOIL-like analysis/design workflow with gradients, while making clear that vortex-lattice lifting-surface physics differs from XFOIL's airfoil/boundary-layer method. Those experiments are not a supplied or qualified workshop example. Today uses a compact planar model, synthetic data, JAX fitting, CasADi trajectory optimization and a scoped Lean companion proof. It does not demonstrate a full Lie-group vehicle, compute a reachable tube, certify generated machine code or validate a physical digital twin. References: https://github.com/CogniPilot/modelica_models; Solà, Deray and Atchuthan, A micro Lie theory for state estimation in robotics, https://arxiv.org/abs/1812.01537; Althoff, Frehse and Girard, Set Propagation Techniques for Reachability Analysis, https://doi.org/10.1146/annurev-control-071420-081941. These support the mathematical ideas, not a claim that Rumoca implements every cited algorithm. Welcome questions from any discipline; the workshop needs no aerospace background.

## 04 · Reuse the building blocks. Deploy the controller.
Links: Library reference | https://cognipilot.github.io/modelica_models/ ; Model library source | https://github.com/CogniPilot/modelica_models ; Vehicle models | https://github.com/CogniPilot/modelica_models/tree/main/Vehicles ; Cerebri RDD2 | https://github.com/CogniPilot/cerebri_rdd2
Time: 10:10–10:15
Time group: Motivation
Layout: model-library
Badge: COGNIPILOT MODELICA_MODELS · reusable equations + interfaces
Family 1: Motion + geometry
Packages 1: LieGroups · RigidBody · Geodesy
Use 1: Rotations, dynamics and coordinate frames
Family 2: Control + navigation
Packages 2: Control · Estimation · Avionics
Use 2: Controllers, filters and sensor contracts
Family 3: Vehicles + missions
Packages 3: Vehicles.Templates · Rdd2 · Cubs2
Use 3: Quadrotor / fixed-wing plants + vehicle models
Family 4: Perception + planning
Packages 4: Vision · SLAM · Planning
Use 4: RGB-D vision, mapping and planning
Utilities: Shared mathematics: LinearAlgebra · Polynomials · MathUtilities
Deployment: Modelica library → Rumoca eFMI → Cerebri C → Zephyr RTOS

- Start with a component, not another copy of its mathematics.
Checkpoint: Browse the linked package docs; use one Modelica source across simulation and firmware.
Notes:
Give a 60–90 second tour immediately after the Cerebri motivation. These are the reusable packages in CogniPilot/modelica_models, not the workshop's small standalone Quadrotor.mo. LieGroups includes SO(2), SO(3), SE(2), SE(3) and SE_2(3), with quaternion and other rotation representations; RigidBody provides 6-DOF dynamics and Geodesy converts geodetic/local frames. Control contains PID and sampled multirotor control, rate-loop and allocation building blocks. Estimation includes complementary attitude and strapdown ESKF/manifold-UKF components; Avionics defines sensor and navigation-estimate contracts independently of a wire transport. Vehicles.Templates provides quadrotor and fixed-wing templates, while Vehicles.Rdd2 and Vehicles.Cubs2 add named vehicle parameterizations, control and mission examples. Vision and SLAM expose camera/perception/localization/mapping components; Planning includes Dubins paths and trajectory tools. LinearAlgebra, Polynomials and MathUtilities supply reusable numerical functions. The shared library is larger than today's tested scalar plant; presence in the library is not a claim every component has been qualified by this workshop or every target accepts it. Click the library reference and open one package rather than cloning/building the full library during class. Connect the deployment strip to Cerebri RDD2: its documented CRSF → generated eFMI control/estimation → mixer → DSHOT path runs against Zephyr on the drone. Each deployed model and property needs its own verification evidence. Review basis: library README at f63ab60d6e4bd6a6ed855c9c153f701217d7a307, https://github.com/CogniPilot/modelica_models/blob/f63ab60d6e4bd6a6ed855c9c153f701217d7a307/README.md; firmware source https://github.com/CogniPilot/cerebri_rdd2. Next show the compiler stages that make this reuse possible, and later the concrete CLI FMU/eFMU exports.

## 05 · How equations become executable programs
Links: Compiler pipeline | https://github.com/CogniPilot/rumoca/blob/v0.10.2/docs/dev-guide/src/compiler/pipeline-overview.md ; Custom targets | https://github.com/CogniPilot/rumoca/blob/v0.10.2/docs/user-guide/src/codegen/custom-targets.md ; GaLEC / eFMI | https://github.com/CogniPilot/rumoca/blob/v0.10.2/docs/user-guide/src/codegen/galec-efmi.md
Time: 10:15–10:20
Layout: pipeline
Badge: IR = intermediate representation · Rumoca 0.10.2

- Quadrotor.mo → JAX + CasADi · the same declared equations

Checkpoint: Same declared physics · inspectable stages · targets choose the IR they need.
Notes:
Spend three minutes on the pipeline and two on the shared Session API. IR means intermediate representation: each stage preserves the information later consumers need. Parse builds AST (abstract syntax tree), retaining source syntax and locations. Resolve, typecheck and instantiate establish names, types, modifications and the requested model instance; flatten expands hierarchy and connection equations into Flat with fully qualified variables. Flat is not yet an execution order. DAE (differential-algebraic equations) is the canonical equation system, with event/clock metadata. Structural preparation matches equations to unknowns, orders blocks, handles algebraic loops/index reduction as needed and selects states; Solve holds solver-facing scalar/register and tensor computation plans. This small ODE does not exercise every general DAE feature. The separate DAE → GaLEC branch is checked eFMI Algorithm Code (Guarded Algorithmic Language for Embedded Control); the released projection accepts fixed-sample discrete models with no continuous states or der(). GaLEC can be rendered/packaged for eFMI and embedded C. Today's continuous quadrotor uses the Solve route; the GaLEC branch describes the fixed-sample controller deployment route. References are pinned to the actual 0.10.2 release. Today uses small Solve-based Lean/Torch targets; custom targets can choose earlier IRs when appropriate. Explain that VS Code provides native authoring/LSP and the playground provides browser modeling/simulation. The Python/CLI release is pinned to 0.10.2; the public browser editor is a separately deployed build. Open examples/simulate.py: rum.Session().load(...) then model.to_jax(); open examples/optimize_casadi.py: model.to_casadi(). Python integrates or constructs objectives without maintaining a second plant. Fast Monte Carlo/RL, native AD and heterogeneous solver specialization are research directions. This diagram explains architecture; numerical and proof qualification remain scoped to the workshop model. Return to this diagram when opening target.toml on slide 20.

## 06 · Everyone gets a browser plot
Links: Open playground | https://cognipilot.github.io/rumoca/ ; Browser model | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/browser/Quadrotor_browser.mo
Time: 10:20–10:25
Layout: image
Visual: assets/browser-drag-linear.png
Badge: LIVE DEMO · zero-install modeling

- Open editor; paste browser bundle
- Lightning bolt → create scenario
- Model name: BrowserFlight; end time: 8 s
- Save → Run Simulation

Checkpoint: You should see BrowserFlight Results and a plot.
Notes:
Exact URL https://cognipilot.github.io/rumoca/. Raw source https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/browser/Quadrotor_browser.mo. Wait for Runtime: Ready. Select all inside Main.mo and paste the complete bundle. Click the lightning-bolt Create Scenario button and accept the TOML filename. Set Model name to BrowserFlight and Batch end time to 8 s; Save, then Run Simulation. For the second run, reopen Main.mo, edit k_quad to 0.08, return to the scenario TOML and run again. Screenshot records a real run. Browser is not Python/JAX/CasADi. If offline, label the screenshot as backup and continue local/demo path. Five-minute guided demo.

## 07 · Choose a full-workshop route
Links: Local VS Code setup | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/LOCAL_SETUP.md ; Create Codespace | https://codespaces.new/CogniPilot/rumoca_workshop_amc2026?quickstart=1 ; Recovery help | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/TROUBLESHOOTING.md
Time: 10:25–10:30
Layout: cards
Badge: Setup decision · worksheet has every link

- Codespaces: cloud VS Code; login and allowance
- Local uv: optional native installation
- Browser or pair: keep working during setup

Checkpoint: Switch route after ten minutes of setup trouble.
Notes:
Codespaces URL https://codespaces.new/CogniPilot/rumoca_workshop_amc2026?quickstart=1. Codespaces requires an account with allowance or billing enabled. Cloud qualification is recorded in VERIFICATION.md; account availability varies. Local: download/extract ZIP, install uv/extension, uv sync --frozen. Python and released editor are qualified on Linux/Windows x64 and macOS Intel/Apple Silicon. In Codespaces, select the core workshop and wait for WORKSHOP PASS. Native uv remains an optional route.

## 08 · Fly the user guide’s quadrotor
Links: Open Quadrotor SIL | https://cognipilot.github.io/rumoca/user-guide/simulation/interactive.html#quadrotor-sil ; Simulation apps | https://rumoca.cognipilot.org/simulation ; Walkthrough | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/SIMULATION_SETUP.md
Time: 10:30–10:40
Time group: Simulation setup
Layout: image
Visual: assets/user-guide-quadrotor.png
QR: assets/simulation-qr.png
QR URL: https://rumoca.cognipilot.org/simulation
Badge: LIVE WALKTHROUGH · one scenario connects model, inputs and view

- Open Quadrotor SIL → Settings
- Inspect the TOML → save → Simulate
- Capture enables keys: Space arms; W / S changes throttle

Checkpoint: VS Code: open .mo → lightning bolt creates TOML → Settings → Run.
Notes:
This is the linked user-guide QuadrotorAcro example, built around the six-degree-of-freedom QuadrotorSIL plant and CMM controller/library. It is a richer interactive example than our six-state planar Quadrotor.mo; keep those models distinct. Open the link and choose Settings in the first embedded editor. Walk through the next three slides using its actual TOML and scene script. In VS Code, first open the .mo file and click the lightning-bolt Create Rumoca Scenario icon; it creates the scenario TOML. Settings then edits the run through typed controls or text. Do not imply that the guide’s CMM paths are already installed in the small workshop checkout. For the guided live experience, use the already deployed browser guide. The scenario already selects its live viewer. Leave GPU off for this CPU example, choose Simulate, then press Capture in the scene. Space toggles arming only with throttle at or below 0.05. W/S raises/lowers throttle; arrows command roll/pitch, A/D yaw, R resets, Q quits, and the Stop button is the reliable browser stop control. Use brief throttle taps rather than holding W. The ACRO wrapper commands angular rate; neutral sticks do not mean automatic altitude hold or attitude leveling. Preview this browser run before the workshop; browser runtime is a separate deployed build from the pinned Python/VS Code 0.10.2. If the live guide cannot start, use the labeled saved capture and inspect its linked TOML and scene. After this ten-minute walkthrough, return to the compact planar model and Python Session API. Native BrowserFlight scenario creation remains documented in WORKSHOP.md.

## 09 · TOML: choose the model and the clock
Links: Actual quadrotor TOML | https://github.com/CogniPilot/rumoca/blob/main/examples/interactive/quadrotor/rumoca-scenario.acro.toml ; Settings reference | https://cognipilot.github.io/rumoca/user-guide/simulation/scenario-tomls.html
Time: 10:30–10:40
Time group: Simulation setup
Layout: code
Code title: rumoca-scenario.acro.toml · selected sections
Code: [rumoca]\nversion = "1"\ntask = "simulate"\n\n[model]\nfile = "QuadrotorSIL.mo"\nname = "QuadrotorAcro"\n\n[sim]\nsolver = "rk-like"\ndt = 0.01\nmode = "realtime"
Badge: RUN CONFIGURATION · Modelica still owns the physics

- file selects source; name selects the runnable class
- dt = 0.01 s schedules 100 updates per simulated second
- realtime paces the run; solver chooses the numerical method
- Batch: set t_end; live: stop explicitly

Checkpoint: Schema version "1" is the TOML format, not the Rumoca release.
Notes:
Read the actual file. source_roots is a top-level key before any section; the upstream example points to ../../../target/cmm/CMM-a642c381, prepared in the Rumoca repository by cargo xtask repo modelica-deps ensure. It supplies the CMM library dependency. Paths resolve relative to the scenario file, not the terminal directory. file selects the source containing multiple classes; name selects QuadrotorAcro, not just the file-stem plant. version="1" is the scenario schema, not Rumoca 1.0. solver="rk-like" selects the explicit RK-like solver family; auto chooses automatically, bdf is intended for stiff models. dt=0.01 is the live scheduling/advance interval, not a claim that an adaptive solver takes exactly one fixed internal step or that the renderer runs at 100 FPS. realtime paces against wall-clock time with held inputs; it cannot guarantee a slow computer meets deadlines. as_fast_as_possible removes sleeps; lockstep advances when an external packet arrives. atol/rtol optionally control solver accuracy and should be checked by refinement rather than chosen for appearance. t_end sets batch/results-panel horizon; live interactive runs continue until the quit signal, Stop control or interrupt. Have attendees locate these fields in Settings, then view TOML. Save before running; changing a horizon or solver is changing the experiment rather than the physical equations.

## 10 · TOML: route controls into the model
Links: Full input mappings | https://github.com/CogniPilot/rumoca/blob/main/examples/interactive/quadrotor/rumoca-scenario.acro.toml ; Copyable walkthrough | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/SIMULATION_SETUP.md
Time: 10:30–10:40
Time group: Simulation setup
Layout: code
Code title: Local state → input mapping → Modelica input
Code: [locals.throttle]\ntype = "float"\ndefault = 0.0\n\n[input.gamepad.integrators.throttle]\nsource = "LeftStickY"\nwrite = "throttle"\nrate = 0.7\ndeadband = 0.1\nclamp = [0.0, 1.0]\n\n[signals.model_inputs]\nstick_throttle = "local:throttle"
Badge: TRACE ONE SIGNAL · device → local → model → viewer

- The stick changes persistent throttle; clamp keeps it within 0–1
- W / S drives the keyboard integrator instead
- Space toggles armed when throttle ≤ 0.05
- signals.viewer names the channels the scene reads

Checkpoint: Experiment: change rate 0.7 → 0.3; predict the throttle response.
Notes:
[input].mode="auto" chooses the available input route. locals declares persistent simulation state with types and defaults. The gamepad integrator accumulates throttle from LeftStickY, with a deadband, rate and clamp; a direct axis mapping would replace a command each update. The keyboard route maps W to throttle_input=1 and S to -1, then integrates into the same throttle local. Its decay factor=0.85 referenced to ref_dt=0.016 returns released stick commands toward neutral; it is input shaping, not aerodynamic drag. Space uses action="toggle", state="armed", debounce_ms=500 and precondition="throttle <= 0.05". signals.model_inputs converts the Boolean local to the Modelica numeric armed input with when_false=0 and when_true=1; stick_throttle points to local:throttle. These are educational simulator controls, not a physical arming safety guarantee. signals.viewer uses e.g. px="model:position[1]", pz="model:position[3]" and q0 from quat[1] with default=1 to expose named display channels; aliases are not new physical variables. [[viewer.controls.keyboard]] lists help text; it does not define key behavior—[input.keyboard.keys.*] does. [reset] can reset both model/session and locals in response to the reset signal. In Settings, change only the keyboard throttle integrator rate from 0.7 to 0.3, reset, and compare equal W taps. If using a gamepad, change the shown gamepad rate instead. Restore 0.7 afterward. Avoid discussing motor physics here; the audience needs the general route from a device to a model input.

## 11 · Three.js draws the simulated state
Links: Actual scene script | https://github.com/CogniPilot/rumoca/blob/main/examples/interactive/quadrotor/quadrotor_scene.js ; Scene + frame walkthrough | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/SIMULATION_SETUP.md
Time: 10:30–10:40
Time group: Simulation setup
Layout: code
Code title: quadrotor_scene.js · excerpt from onFrame(api)
Code: const get = api.get;\nconst px = get("px") ?? 0;\nconst py = get("py") ?? 0;\nconst pz = get("pz") ?? 0;\n\n// Model: forward, left, up\n// Three.js: map into x, y, z\nconst tx = -py, ty = pz, tz = px;\n\n// Full script also transforms\n// attitude and updates the mesh.
Badge: PRESENTATION · model states become position, attitude and motion

- onInit: create/load meshes, lighting and persistent state
- onFrame: read named signals and move the vehicle
- Convert position and attitude together: R₃ = A R A⁻¹
- Customize colors, trails or camera; keep physics in Modelica

Checkpoint: [transport.http].scene selects this JavaScript file.
Notes:
Start with the actual script header: ctx.onInit(api) is called once after Three.js is ready; ctx.onFrame(api) runs on animation frames. api.THREE supplies the library, api.scene the scene, api.state the persistent meshes and api.get(name) the latest named signal. onInit loads the GLB drone and desert textures, creates lighting/propeller groups and camera anchors; onFrame reads position, quaternion, motor speeds and armed state. The model is Forward-Left-Up, whereas the mesh uses +Z forward, -X left and +Y up. Its position mapping is tx=-py, ty=pz, tz=px. With A=[[0,-1,0],[0,0,1],[1,0,0]], the attitude is transformed by A R A^-1, then translation is inserted into quad.matrix. Check that model +x becomes scene +z, model +y becomes scene -x, and model +z becomes scene +y; identity attitude stays identity. q0 is scalar-first (model quat[1]); do not pass it first to Three.js Quaternion, whose constructor takes x,y,z,w. The upstream DCM comment says NED, but both the model and applied A map are FLU; call out the comment as stale when reading it, rather than teaching the wrong frame. No upstream files are changed for this workshop. The full script gates propeller visual motion on armed and reads omega_m1..4; visual spin is an illustrative bounded per-frame effect, not the physical motor integrator. Camera/HUD/shadows are presentation. [transport.http] chooses scene="quadrotor_scene.js", asset_dir="../../assets" and port=8080; [transport.websocket].port=8081 streams native state. Embedded browser execution hosts its own surface; those native ports need not be exposed to try the guide. [[viewer.frame]] declares scalar-first quaternion/position aliases for a named body frame; camera/HUD references reuse it. In native Codespaces runs, HTTP and WebSocket ports must be forwarded and reachable, with the correct wss URL; this guide demo avoids that additional setup. Make a small visual customization in the challenge rather than reimplementing dynamics in JavaScript.

## 12 · The user guide is a live modeling lab
Links: Open NACA example | https://cognipilot.github.io/rumoca/user-guide/language/arrays-pde.html#2-d-navierstokes-flow-over-a-naca-2412-airfoil ; Explore user guide | https://cognipilot.github.io/rumoca/user-guide/
Time: 10:40–10:45
Layout: image
Visual: assets/user-guide-naca.png
Badge: ARRAY-NATIVE PDEs · NACA 2412 · editor + WebGPU

- Edit StopTime: 30 → 2 s
- Simulate; select the final frame
- Switch vorticity / pressure

Checkpoint: Research direction: differentiable vortex-lattice / XFOIL-like design workflows
Notes:
Use the deployed user guide as a workshop resource, not only a reference manual. Open https://cognipilot.github.io/rumoca/user-guide/language/arrays-pde.html#2-d-navierstokes-flow-over-a-naca-2412-airfoil. This page embeds Monaco editors, simulation controls, plots and custom visualizations; it also has turkey heating and a vibrating membrane for other domains. Find AirfoilFlow, change StopTime = 30 to 2, leave NX=30 and NY=18, keep GPU checked and Interactive off, then Simulate. Move the time slider to the final frame and switch Field between Vorticity and Pressure. Our rehearsal used Chromium with a software WebGPU adapter; it demonstrates execution and UI, not a hardware speed claim. Explain why arrays matter: PDE discretizations and vision both contain large structured fields; preserving array shapes and operations gives the compiler opportunities for whole-kernel derivatives and hardware planning. Connect this to our experiments with differentiable vortex-lattice methods for aircraft aerodynamic design: geometry → aerodynamic model → objective → gradient → updated geometry. “Differentiable XFOIL-like” is an analogy for an accessible analysis/design workflow, not a claim that this NACA demo is XFOIL, a vortex-lattice method or a validated differentiable aerodynamic optimizer. Vortex-lattice models describe lifting surfaces, while XFOIL combines airfoil panel and boundary-layer analysis; keep their assumptions distinct. The workshop does not supply or rehearse our vortex-lattice experiments. Reference method context: https://aerosandbox.readthedocs.io/en/master/autoapi/aerosandbox/aerodynamics/aero_3D/vortex_lattice_method/ and https://web.mit.edu/drela/Public/web/xfoil/. The NACA contour and coarse artificial-compressibility/penalization flow field make declared array equations visible; this is a qualitative teaching model, not a validated lift/drag or aircraft design calculation. If WebGPU is unavailable or the short run fails, show the labeled saved capture and continue. Do not try the unqualified CPU NACA route during this five-minute segment. The browser guide is a separately deployed compiler/runtime from the pinned Python release. Keep the warm successful tab ready before class; participants can revisit these editors during downtime.

## 13 · A planar quadrotor we can inspect
Links: Open vehicle model | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/models/Quadrotor.mo ; Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
Time: 10:45–10:50
Layout: image
Visual: assets/quadrotor.png
Badge: Six states · two aggregate inputs

- World x right; z up
- Positive pitch tilts thrust toward +x
- Hover: T = mg = 11.772 N
Checkpoint: Find velocities, pitch rate, thrust and torque in the model.
Notes:
States x,z,theta,vx,vz,omega; inputs T and tau. m=1.2 kg,Iyy=.025 kg m²,g=9.81. Diagram is generated from our convention, not a borrowed paper figure. Simplified world-axis drag; no roll/yaw/motors/wind/contact. The compact planar example keeps the equations inspectable and the computations short. Introduce pitch as the angle that directs the thrust; specialist aerodynamics is optional.

## 14 · Your first engineering change: drag
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md ; Open playground | https://cognipilot.github.io/rumoca/
Time: 10:50–10:55
Layout: wide
Visual: assets/drag-law.png
Badge: HANDS-ON · predict before running

- Change k_quad = 0.0 to 0.08, save, then simulate.
Command: uv run --frozen python examples/simulate.py
Checkpoint: What changes at high speed? What about negative velocity?
Notes:
Explain units kl N s/m,kq N s²/m²,epsilon .01 m/s. Smooth componentwise law approximates |v|v and never adds energy for nonnegative coefficients; Lean proves the signs and smoothing bound. It differs from Faessler et al.'s body-frame rotor-drag model; do not claim their flatness theorem. Allow about three minutes editing/predicting. Browser users make the same coefficient change and Play again. Default parameter changes affect simulation; fitting estimates parameters explicitly.

## 15 · More drag, less distance
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
Time: 10:55–11:00
Layout: wide
Visual: assets/simulation-hero.png
Badge: HANDS-ON · same prescribed Python inputs

- Reference at 8 s: 41.60 m → 17.97 m
Checkpoint: Compare your current default with the two reference cases.
Notes:
Open the actual live plot and ask participants to explain the sign. The slide plot uses emitted JAX equations and reference parameters; not real flight data. Browser wrapper coasts at level hover, so its numbers differ. Optional kl=.30 then restore .18. Presenter solution is an inheritance override, not a second dynamics implementation. Take two questions. End on time for break.

## 16 · Break · back at 11:10
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

## 17 · Known experiment. Unknown coefficients.
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
Time: 11:10–11:20
Layout: wide
Visual: assets/data-hero.png
Badge: Synthetic data · seed 20261012

- Three training flights; one held-out flight. 20 Hz, 8 s each.
Checkpoint: Speed variation helps separate linear and quadratic drag.
Notes:
Data generated by Rumoca CasADi + independent adaptive DOP853; JAX fit uses RK4. Position noise .025 m; velocity .035 m/s; angles/rates also noisy, but only exact initial angles/rates enter the fit. Commands and initial state assumed known. Holdout has different excitation and negative initial speed. The data are synthetic. Explain how real logs would bring actuator timing, wind and sensor bias. Truth is reporting only.

## 18 · Differentiate the prediction error
Links: Workshop guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md
Time: 11:20–11:30
Layout: fit
Visual: assets/fit-workflow.png
Badge: JAX autodiff through generated physics + RK4

- Positive parameters; noise-scaled loss; bounded optimization
Checkpoint: JAX provides gradients. SciPy updates the coefficients.
Notes:
Read the visible symbol key before showing code. k_l is k_linear in the source, the coefficient multiplying velocity; k_q is k_quad, the coefficient multiplying smooth speed magnitude times velocity. k_l has units N s/m and k_q N s²/m². a and b are dimensionless logarithms of the coefficients expressed in their native SI units. e is Euler’s number, about 2.718; exp(a) and exp(b) are strictly positive, so an optimizer cannot produce negative drag. k_l,ref = 1 N s/m and k_q,ref = 1 N s²/m² are unit references, not fitted truth values. L averages squared noise-scaled residuals, y_hat is predicted position/velocity, y is the corresponding measurement, and sigma is that channel’s supplied noise standard deviation. The code uses 0.025 m for positions and 0.035 m/s for velocities; division removes units. A lower L means better agreement in noise units, not a proof that the model is physically correct. Show fit script's p_from_log, residual, value_and_grad, minimize. Each coefficient divided by one native SI unit equals exp(log parameter), so the logarithm is dimensionless; fitted bounds .001..2 in native units. Mean residual² divided by known noise variance is dimensionless, over x,z,vx,vz. Avoid differentiating noisy acceleration estimates. JAX derivative is of the implemented discrete rollout; finite differences are checks. The system ID is not an autodiff proof of model correctness. Participants can run the next command and inspect the provided algorithm.

## 19 · Run the fit. Test the held-out flight.
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

## 20 · Write a template. Generate checked equations.
Links: Lean target.toml | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/templates/lean-proof/target.toml ; Jinja template | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/templates/lean-proof/rhs.lean.jinja ; Checked theorem | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/formal/Workshop.lean ; Try the walkthrough | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/BACKENDS.md#walk-through-the-lean-target
Time: 11:50–11:55
Layout: lean-target
Badge: EXTENSIBILITY DEMO · Solve → Jinja → Lean

- target.toml selects Solve, supported features and output files
- Jinja loops over compiler data and renders types + equations
- Lean checks emitted equations and explicit theorem statements
Command: uv run --frozen python scripts/export_lean.py
Checkpoint: 17 exact-real theorems · compiler, template and numerical execution have separate checks.
Notes:
First confirm the held-out prediction improved, then use three minutes to walk the actual files and one minute for an optional template edit or questions. Open templates/lean-proof/target.toml: version=1 is the manifest version; ir="solve" selects solver-facing IR. The capabilities declare continuous states, scalar fallback and rejection of events, residual equations and unsupported features. These gates are separate from the template's operation rejection rules. The two [[files]] entries map program.json.jinja to solve_program.json and rhs.lean.jinja to Generated.lean. This is a target manifest, distinct from a simulation scenario TOML. Open rhs.lean.jinja at structure Control: {% for name in ... %} repeats the body for each compiler input name; {{ name }} substitutes a value. For this model the Solve input names T and tau produce two real-valued Lean fields. The slide excerpt adds line breaks to the actual template for readability. Scroll to LoadY and LoadP: they map register loads to named state, parameter and control fields; Unary/Binary map supported operations; unsupported operations call fail rather than silently substituting equations. Use the same loaded Session model, model.codegen("templates/lean-proof").save_all("formal"). The export_lean.py driver adds hashes/layout checks; it does not construct equations. Run the displayed command, open formal/Generated.lean and formal/solve_program.json, then formal/Workshop.lean. Show generated_matches_physics and hover_equilibrium: level and still, thrust m*g, zero torque gives zero state derivatives over exact reals. CI regenerates, builds the 17 theorems, rechecks terms with leanchecker and rejects admissions; link the completed CI rather than downloading Mathlib during class. The compiler/target real-arithmetic interpretation remains trusted; floating-point integration and full compiler/firmware correctness have separate obligations. BACKENDS.md has a copy-and-comment exercise exporting to results/live/lean-template so participants can try Jinja while preserving the checked baseline. Participants still fitting and challenge entrants may keep working during this brief optional demo. Next show the same target mechanism generating Torch.

## 21 · Make a target. Learn a policy.
Links: Backend walkthrough | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/BACKENDS.md ; Torch target.toml | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/templates/torch-ode/target.toml ; Lean Jinja target | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/templates/lean-proof/rhs.lean.jinja
Time: 11:55–12:00
Time group: Deployment targets
Layout: wide
Visual: ../results/reference/torch_policy.png
Badge: EXTENSIBILITY DEMO · same vehicle · Linux CPU / Codespaces

- target.toml → generated Torch → differentiable policy learning
Command: uv run --frozen --group torch python scripts/learn_hover_torch.py
Checkpoint: Held-out cost ≈ 0.116 → 0.021 · optional instructions: BACKENDS.md
Notes:
Show templates/torch-ode/target.toml: ir="solve", explicit capabilities and output template. Open rhs.py.jinja and the generated/torch-ode/Quadrotor_torch.py output. The small external target maps the actual scalar Solve operations to Torch; it does not handwrite the vehicle dynamics or require a Rust compiler change. The target passes 101-point batched RHS comparisons, JAX/CasADi Jacobians, forward/reverse AD, finite differences and rejection gates. Use the optional preinstalled Torch environment in the Codespace; do not ask all attendees to download the extra CPU package during the five-minute demonstration. Run or show learn_hover_torch.py: two positive feedback gains learned through the same generated six-state vehicle's RK4 rollout, restricted to vertical hover with zero torque. Sixty Adam updates on 64 initial conditions; test on 128 new initial conditions. The dimensionless held-out cost drops about .116 to .021; complete objective gradients and fixed-sampling finer-integration checks pass. Call this differentiable model-based policy optimization, a bridge to RL, not PPO/DQN or full-flight autonomy. Known fixed drag coefficients are used for this separate teaching task. Source/template provenance is saved with results. The full target supports a small scalar ODE subset and rejects events/unsupported primitives. Invite compiler contributors to add one primitive and compare its derivatives before declaring support. This is one concrete extension seam toward fast Monte Carlo/RL, native AD or JAX/CasADi/PyTorch integrations and solver specialization for heterogeneous compute. Broad automatic partitioning and performance scaling remain research directions. Primary context: Heess et al. 2015 https://arxiv.org/abs/1510.09142. Stop at noon for a full break.

## 22 · Export an FMU. Run it with Python.
Links: Run the commands | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/EXPORTS.md ; FMPy example | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/examples/run_fmu.py ; FMI standard | https://fmi-standard.org/ ; FMI-LS-WASM | https://github.com/modelica/fmi-ls-wasm
Time: 11:55–12:00
Time group: Deployment targets
Layout: fmu-export
Visual: ../results/reference/fmu.png
Badge: INTEROPERABILITY · same Quadrotor.mo · native FMI 2 / 3
Code title: Terminal · export → build → simulate
Code: rumoca compile models/Quadrotor.mo \\n  --model Quadrotor --target fmi3 \\n  -o results/live/fmi\n\nuv run --frozen fmpy compile \\n  results/live/fmi/Quadrotor.fmu\n\nuv run --frozen python examples/run_fmu.py \\n  results/live/fmi/Quadrotor.fmu

- Model Exchange: host solver. Co-Simulation: FMU solver.
- FMPy runs the exported model; all six states are checked.
Checkpoint: FMI-LS-WASM planned for the next Rumoca release: 0.11
Notes:
Share this five-minute target gallery with Torch and eFMI; show the prepared terminal and plot rather than waiting on downloads. The pinned Linux CLI is rumoca 0.10.2 and is installed on PATH in the updated container. The release Python wheel omits the fmi feature; use the CLI for this package export, while run_fmu.py loads the same model through the Session API for the independent generated-JAX reference. Run the three commands exactly. Export creates results/live/fmi/Quadrotor.fmu plus the unpacked source directory. This is a source-code FMU: FMPy's compile command adds the current platform's shared library into the archive using CMake and the C compiler. Then the Python script uses from fmpy import simulate_fmu and calls simulate_fmu(filename, fmi_type="CoSimulation", stop_time=2.0, output_interval=.02, output=["x", "z", "theta", "vx", "vz", "omega"]). The complete script supplies named start values and tests hover, linear coast, quadratic coast and coupled pitch against the same Session-generated JAX RHS. It also checks Model Exchange where FMPy's CVode library is available; Linux ARM uses Co-Simulation. Open results/live/fmi3/fmu.png, the run script's default report location, and the CSV/JSON reports. Model Exchange gives the importer the derivatives; Co-Simulation advances the packaged kernel between communication points. The FMI 2 variant uses --target fmi2 and the same FMPy workflow. The all-in-one examples/export_fmi.py rehearses both versions, validates metadata/schema, runs both profiles on x64 and checks the eFMU C. Rumoca 0.10.2 exports time-unit metadata but omits other unit annotations in FMU XML; the interface uses the SI units stated in Modelica and the numerical checks, including T in N and tau in N m. Native shared-library FMUs are platform-specific; source can be rebuilt for another supported platform. FMI-LS-WASM, a WebAssembly mapping of FMI 3, is planned for Rumoca 0.11 per the presenters' release roadmap. Keep it visibly separate from today's tested native FMU export; existing experimental target code is not the promised next-release integration or a standard-finalization claim. This demo checks this event-free planar vehicle, not every FMI capability, whole-compiler correctness or drone safety.

## 23 · Export an eFMU. Call the controller each tick.
Links: Export and run | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/EXPORTS.md#efmu-fixed-sample-embedded-controller ; Controller model | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/extras/exports/HoverController.mo ; GaLEC / eFMI guide | https://github.com/CogniPilot/rumoca/blob/v0.10.2/docs/user-guide/src/codegen/galec-efmi.md
Time: 11:55–12:00
Time group: Deployment targets
Layout: code
Badge: EMBEDDED CONTROL · 100 Hz · GALEC + C99 in one .efmu
Code title: Terminal · compile + check the exported C
Code: rumoca compile \\n  extras/exports/HoverController.mo \\n  --model HoverController \\n  --target galec-production \\n  -o results/live/efmi\n\nuv run --frozen python \\n  examples/export_fmi.py --check-efmu \\n  results/live/efmi/HoverController.efmu

- .efmu contains AlgorithmCode, ProductionCode and manifests.
- Startup → Recalibrate → DoStep every 0.01 s; inputs z_ref, z, vz → thrust T.
- Compile the generated C99; check hover and thrust saturation.
Checkpoint: FMU: exchange a simulation · eFMU: deploy fixed-sample control code
Notes:
The eFMU is an eFMI container, with a different interface and purpose from the FMI simulation FMU. Show extras/exports/HoverController.mo: samplePeriod=0.01 seconds; T=min(maxThrust,max(minThrust,m*g+kp*(z_ref-z)-kd*vz)). kp is N/m and kd is N s/m; these are a simple demonstrator's fixed gains, not gains optimized by the preceding CasADi example. The continuous six-state plant cannot use this GaLEC projection directly; the released profile accepts fixed-sample discrete controllers without der(). Run the displayed compile command. It writes results/live/efmi/HoverController.efmu and a sibling unpacked directory containing __content.xml, schemas/, AlgorithmCode/HoverController.alg and ProductionCode/HoverController.c/.h with manifests and LogicalData mappings. --target galec exports AlgorithmCode only; --target galec-production adds C99. The checking command extracts the actual archive, validates three manifests against the bundled schemas and checks all nine SHA-1 links, then compiles its generated C and a small API harness. It invokes Startup, Recalibrate and DoStep for hover, both saturation endpoints and 512 seeded finite input triples. Expected hover T=m*g=11.772 N, max=25 N and min=0.2 N; generated Real storage is float32, and comparisons use an explicit 4e-6 N absolute tolerance. Inspect extras/exports/check_controller.c for the C calling pattern: allocate HoverControllerState, call HoverController_startup and HoverController_recalibrate, write input fields, call HoverController_dostep, check rumoca_galec_error_signal_status and read T. In an application, schedule DoStep at 100 Hz and hold T between updates; this harness tests the arithmetic/calling contract, not real-time scheduling or closed-loop flight. Cite the earlier Cerebri Modelica/eFMI/Zephyr deployment motivation. No FMPy execution of the eFMU, MISRA certification, DO-178C compliance or full-flight stability claim is made. Stop at noon for the ten-minute break.

## 24 · Break · back at 12:10
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

## 25 · Move between hovers, respect limits
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

## 26 · Solve. Inspect. Explain the braking.
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

## 27 · Next up: pylon racing at PURT
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

## 28 · FastDyn: fly the firmware against declared physics
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

## 29 · Explore the fixed-wing workbench
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

## 30 · Explore motion-capture identification
Links: Try the app | https://cognipilot.github.io/mocap_sysid/ ; Source code | https://github.com/CogniPilot/mocap_sysid ; Experiment guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/BROWSER_APPS.md
Time: 12:45–12:50
Time group: App showcase
Layout: image
Visual: assets/showcase-mocap_sysid.png
Badge: AGENT-BUILT APPS · explore your own scientific question

- Visualize vehicle data and model structure
- Compare experiments and data splits
- A viewer for exported benchmark results

Checkpoint: Explore exported identification results.
Notes:
Show the stored synthetic 6-DOF open-loop example and its model structure. This viewer does not train models or execute a WASM simulation. Recorded benchmark data is distinct from a live fit. Invite users to explore a problem or dataset from their own domain; do not invent method scores. Together with the neighboring app slides, share the five-minute showcase slot.

## 31 · SLAM Lab: one mathematical system, many targets
Links: Try the app | https://cognipilot.github.io/slam_web/ ; Source code | https://github.com/CogniPilot/slam_web ; Experiment guide | https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/BROWSER_APPS.md
Time: 12:45–12:50
Time group: App showcase
Layout: slam-vision
Variable scale: ≈12M
Visual: assets/showcase-slam_web.png
Badge: RESEARCH VISION · ROS 2 math → AD + hardware planning

- ROS 2 computations → one mathematical system
- Full vision, mapping and loop closure
- Stress-test tensor-native Solve IR

Checkpoint: Try the inertial demo. Help make full-system compilation practical.
Notes:
Use SLAM Lab to show the research idea, not only a browser demo. ROS 2 deployments can require substantial configuration of nodes, topics, clocks and executors; a declared mathematical model makes the computational dependencies explicit and reusable. ROS 2 can still supply hardware/message interfaces. The aim is to expose the entire mathematical computation to compiler analysis and AD rather than burying each stage in an independently configured node. Explain this concretely: a downstream pose or design objective can depend on upstream vision parameters, and a connected representation gives AD access across those smooth kernels. Hard feature selection, correspondence switches, occlusion and loop-closure decisions need explicit derivative treatment; a whole-system representation does not make every operation differentiable. This is a research direction, not a demonstrated end-to-end gradient of the complete SLAM pipeline. Then take the mathematical computations normally distributed across ROS nodes—camera processing, feature matching, state estimation, mapping and loop closure—and compose them into one declared system of equations and algorithms. “One mathematical system” does not mean a single scalar equation, or automatic conversion of arbitrary ROS software. Components stay readable; their interfaces, state, clocks and dependencies must be explicit. A compiler that sees the connected computation can optimize across component boundaries instead of forcing every algorithm author to hard-code its hardware partition. The current full-model scale is roughly 12 million scalar variables, a maintainer-provided estimate; this is not an independently recounted compiler statistic, ODE-state count or performance measurement. Full computer vision and loop closure make a strong stress test for Rumoca's tensor-native Solve IR: preserve shapes, tensor operations and dependencies rather than expanding every tensor operation into millions of unrelated scalar statements. The goal is compiler planning for CPU kernels, GPU kernels and heterogeneous placement, with numeric bit widths selected per computation subject to error budgets, range checks and numerical validation. Changing precision can change results; require comparisons, stability/error checks and state/timing semantics before deployment. The CPU/GPU placement and general precision planning shown here are research directions, not an automatic deployment feature demonstrated by this workshop. Today's rehearsed public browser path is InertialOnly / ResponsiveInertial, with Three.js sensor views; the full native SLAM model and loop-closure path were not executed in the workshop rehearsal. Invite contributors who care about compiler optimization, vision, numerical precision or systems to bring a model and a check. Keep the brief manual experiment available through the Try the app link. Primary architectural background: MLIR, https://arxiv.org/abs/2002.11054; Higham and Mary, Mixed Precision Algorithms in Numerical Linear Algebra, https://doi.org/10.1017/S0962492922000022. Together with the neighboring app/community slides, share the five-minute 12:45–12:50 showcase slot; begin participant demos at 12:50.

## 32 · A growing community builds with Rumoca
Links: LunCoSim simulator | https://lunco.space/luncosim ; LunCoSim source | https://github.com/LunCoSim/lunco-sim ; Taskyon app | https://taskyon.space/ ; Taskyon source | https://github.com/Xyntopia/taskyon
Time: 12:45–12:50
Time group: App showcase
Layout: community-users
Visual: assets/community-luncosim.png
Photo: assets/community-taskyon.png
Project 1: LunCoSim
Use 1: Space-mission co-simulation
Integration 1: Rumoca-powered Modelica runtime
Project 2: Taskyon
Use 2: AI-friendly system-design recipes
Integration 2: Browser-native Modelica + Rumoca
Badge: COMMUNITY USERS · different domains, shared declarative models

Checkpoint: Where could declarative models fit in your tools?
Notes:
Spend about 30 seconds recognizing community users beyond the Purdue workshop applications. LunCoSim is an open-source multiphysics mission simulator connecting Modelica, rigid-body physics, terrain and mission operations; its native workspace consumes Rumoca's compiler, Solve and simulation crates. The project website links to downloadable simulator releases; use https://github.com/LunCoSim/lunco-sim/releases/latest for the actual installer. Do not describe this website preview as a live browser mission simulation. Taskyon connects Modelica and Rumoca to browser-native, AI-friendly, reusable system-design recipes. Describe a recipe as a declared model, parameters, tool steps, assumptions and checks: an agent can call deterministic modeling tools, change a design parameter, rerun and preserve the evidence. This is a design-automation workflow, not just a chat interface. Reusable recipes let collaborators adapt a system-design question while retaining the mathematical source; full automatic replay and agent orchestration were not tested in this workshop. Taskyon is an open-source system for AI-assisted research/design workflows; its Modelica worker imports rumoca-full-web and calls the WASM compiler, template renderer and simulate_model API. The Taskyon app and both project source repositories are directly clickable. The images are actual public website/app-entry captures, not workshop simulations. Source integration and public-page loading were checked; we did not install/run a LunCoSim mission or execute a Taskyon agent workflow, and the planar workshop proofs do not cover these projects. Optional Taskyon agent features may require provider access; no login or model calls were made during the preview check. Credit each independent project's contributors; this is a community acknowledgement, not a claim of endorsement. Primary integration sources pinned at review: https://github.com/LunCoSim/lunco-sim/blob/851b45191130baf537d51e9a68e37fd0e881e241/Cargo.toml and https://github.com/Xyntopia/taskyon/blob/b409d3052238ab08f098b6cc6b18e7f0805a12b6/packages/modelica/modelicaWorker.worker.ts. Share the existing 12:45–12:50 showcase slot with the three preceding app slides, leaving participants time to finish an experiment. Begin demos at 12:50.

## 33 · More Modelica tools from the community
Links: ForgeLab app | https://app.forgelab.space/#/forgelab ; ForgeLab demo video | https://drive.google.com/file/d/1SZtXUm0E-ZaeyDW25z-vM8Mgn_Gv0iMc/view ; Joulios power demo | https://www.youtube.com/watch?v=VsuDOLvGzg8 ; Joulios BESS demo | https://www.youtube.com/watch?v=n3sboXcDEwk
Time: 12:45–12:50
Time group: App showcase
Layout: community-users
Visual: assets/community-forgelab.png
Photo: assets/community-joulios.jpg
Project 1: ForgeLab
Use 1: Browser block-diagram modeling
Integration 1: Compiles models with Rumoca
Caption 1: Public app welcome screen
Project 2: Modelica Joulios
Use 2: Power-system analysis on the web
Integration 2: PowerSystems power-plant demo
Caption 2: Public demo-video thumbnail
Badge: COMMUNITY USERS · Modelica tools in the browser

Checkpoint: Open app.forgelab.space · try the Quadcopter template
Notes:
Spend about 30 seconds on two more community tools. ForgeLab is a browser workspace at https://app.forgelab.space/#/forgelab: build models from blocks, compile them with Rumoca and script them in Python, Julia, C/C++ or Rust. Templates include a 6-DOF Quadcopter, DC motor + PID, a thermal network and a battery pack. Its demo workspace stores models temporarily and clears them after inactivity; signing in keeps work across devices. The ForgeLab demo video button opens a recorded walkthrough on Google Drive. The ForgeLab image is its public welcome screen captured on October 12, 2026; we did not run a ForgeLab template during the preview check. Modelica Joulios is shown in the public “Modelica Joulios Power Analysis Demo” video (https://www.youtube.com/watch?v=VsuDOLvGzg8): a web Modelica editor with a library tree, diagram view and run settings, here opening the PowerSystems.Examples.PowerWorld.PowerPlant model. A second public video, “Joulios BESS Parcel screening & Feasibility Demo” (no sound, https://www.youtube.com/watch?v=n3sboXcDEwk), shows battery energy storage system (BESS) site screening and feasibility; narrate it yourself if you play it. The Joulios image is the power-analysis video's public YouTube thumbnail; we did not run Joulios ourselves. Play either video if time allows, otherwise leave the links for participants. The planar workshop proofs do not cover these projects. Credit each independent project's contributors; this is a community acknowledgement, not a claim of endorsement. Share the 12:45–12:50 showcase slot with the neighboring app slides.

## 34 · Show your experiment. Vote for the cap.
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

## 35 · Join the Rumoca research community
Links: Email James | mailto:jgoppert@purdue.edu ; Rumoca compiler | https://github.com/CogniPilot/rumoca ; Model library | https://github.com/CogniPilot/modelica_models
Time: 12:55–13:00
Layout: title
Email: jgoppert@purdue.edu
Badge: Your Modelica expertise can move this research forward

- Bring a model or a question from your own domain
- Contribute a validation case, model library or compiler improvement
- Interested in research collaboration? Talk with James or Micah

Checkpoint: Email James with your problem, model and one result to check together.
Notes:
Invite participants to join the Rumoca research community: “Bring a model from your domain, one scientific question, and one result we can check together. Help us make declared mathematics reusable across simulation, identification, optimization and verification.” The invitation is to research collaboration and open-source participation, not a job offer or a promise of Purdue team membership. Ask attendees to speak with James Goppert or Micah Condie, or email jgoppert@purdue.edu. The large visible address and Email James button both open an email composer. Modelers can contribute small models with units and expected behavior; researchers can propose a measurable identification, geometry or verification question; software contributors can share a minimal compiler/backend reproduction or improvement. No aerospace background or coding-agent subscription is needed. Ask: “Which model from your work would you try next?” Allow answers and questions rather than reading the bullets. Stop at 13:00. Detailed mathematical proofs and references remain linked from the workshop guide.
