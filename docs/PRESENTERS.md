# Presenters guide

**James Goppert · Micah Condie**
Purdue University, School of Aeronautics and Astronautics
American Modelica Conference · Georgia Tech · October 12, 2026 · 10:00–13:00

Use [slides/workshop.pptx](../slides/workshop.pptx); its speaker notes and
[editable source](../slides/workshop.md) carry the timed cues. Keep the PDF and
reference figures on your laptop. Participant entry:
<https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/docs/WORKSHOP.md>.

## Presentation preflight

1. Open the PPTX/PDF on the presentation laptop, inspect equations at projector
   scale and rehearse browser → editor → PNG switching. Keep local backups.
2. Check the chosen cloud or local environment, terminal, interpreter and smoke
   test before class. [PUBLICATION.md](PUBLICATION.md) covers account-dependent
   cloud availability; [VERIFICATION.md](VERIFICATION.md) records tested paths.
3. Check venue network, projector resolution and accessible power. Make pair/demo
   seats available for attendees whose setup is incomplete.
4. Rehearse the three commands and one parameter edit. Restore the canonical
   source before using reference fit results.
5. Bring the CogniPilot stocking cap and rehearse the short-demo/audience-vote
   format in [CHALLENGE.md](CHALLENGE.md).

## Facilitation and pacing

| Clock | Slides | Activity / presenter cue |
|---|---|---|
| 10:00–10:10 | 1–2 | Welcome, core outcomes and **open experiment challenge**. Announce small interactive experiments, optional agents/hosting, hand vote and prize now. |
| 10:10–10:20 | 3–4 | Why Rumoca; Lie groups, reachable sets, formal verification, identification and digital twins. Then show today's Modelica → JAX / CasADi compiler bridge. |
| 10:20–10:35 | 5–7 | Browser plot, cloud/local setup and smoke. Experienced participants can begin their app when ready. |
| 10:35–10:40 | 8 | User-guide embedded editor and NACA flow visualization. Use a warm successful tab; keep the saved capture ready. |
| 10:40–11:00 | 9–11 | Introduce the small model, change a parameter, run and inspect the plot. Assume no aerospace background. |
| 11:00–11:10 | 12 | **Break 1**, ten full minutes. Leave recovery link visible. |
| 11:10–11:50 | 13–15 | Synthetic data, prediction error, JAX fit and before/after outputs. App builders use independent work time. |
| 11:50–11:55 | 16 | Checkpoint and independent work/questions. Offer detailed mathematics only when requested. |
| 11:55–12:00 | 17 | External target.toml → Torch dynamics → small differentiable hover policy. Presenter demo; optional package preinstalled. |
| 12:00–12:10 | 18 | **Break 2**, ten full minutes. Leave next command visible. |
| 12:10–12:40 | 19–20 | Constraints, CasADi solve and plots. Optional target variant or continued app development. |
| 12:40–12:45 | 21 | Advertise the next PURT pylon racing competition and its planned Rumoca use. Share the site/QR; announce challenge presenters by 12:45. |
| 12:45–12:50 | 22 | Explore **rumoca_fixed_wing** or finish challenge demos. Show SLAM as another example in development. |
| 12:50–12:55 | 23 | Short participant demos, then **audience show-of-hands vote** and stocking-cap award. |
| 12:55–13:00 | 24 | Questions, research invitation and take-home links. |

Total **180 minutes**, including **20 minutes of breaks**. Aim for roughly
40–45 minutes of explanation; the remaining teaching time is guided work,
individual app development, questions and interpreting results. Avoid reading every slide. Appendix slides
have no extra scheduled time; open only when an audience question requires them.

## Explain the single-model choice

The compact planar ODE keeps the source inspectable, exports fast and the
parameter edit visible. It has six states and two inputs, with explicitly
stated units and frame conventions. The
[CogniPilot Modelica models](https://github.com/CogniPilot/modelica_models)
also include richer multirotor formulations; those are outside this example's
qualification scope.

Rumoca 0.10.2’s tested API is `rm.Session().load(path, model="Quadrotor")`,
followed by `.to_jax()` or `.to_casadi()`. Each script recompiles the current
Modelica file. `scripts/common.py` asserts the actual state/input ordering and
uses named parameter indices; it contains numerical integration, not plant
equations. `uv run --frozen python scripts/export_model.py` saves the actual
generated source under ignored `generated/` for optional inspection.

The browser bundle is generated from the same source plus `BrowserFlight`.
Its wrapper sets level hover thrust, zero torque and initial horizontal speed
6 m/s. The Python exercise uses prescribed oscillatory controls, so browser and
Python distances are not directly comparable. Qualitative drag effects are.

## Answer key and interpretation

**Frames and equilibrium:** `z` up, gravity negative; thrust projections
`T*sin(theta)`, `T*cos(theta)`. `T=11.772 N`, zero tilt/rates/velocities gives
hover. Positive torque increases positive pitch. Linear/angular damping oppose
motion. Increasing positive drag slows coasting at either velocity sign.

**Model edit:** `k_quad=0.08`. Restore any exploratory `k_linear` edit to 0.18.
The Python plot always includes linear-only and explicit quadratic cases plus
current defaults. In the reference manoeuvre, 41.60 m versus 17.97 m at eight
seconds. Do not call this a real flight-log or step-response experiment.

**Data:** 4 flights ×161 samples, three train and one validation; 20 Hz; seed
20261012. Synthetic coefficients 0.18 and 0.08. DOP853 generation and RK4 fit
use separate integrators with the same compiled physics. Noise is added after
the exactly known initial state. Inputs and remaining parameters are assumed
known. Real identification would need synchronized commands/logs, calibrated
sensors, actuator delays, wind treatment and uncertainty in initial states.

**Fit:** roughly 0.18042/0.07991; mean standardized loss 26,932→1.073;
local sensitivity condition about 10.87. The held-out case has a different
pitch excitation and negative initial velocity. Look at per-state units and
dimensionless `noise_scaled_rms`; legacy combined RMS is not a homogeneous
physical norm. Loss near one is consistent with the assumed noise; it does not
prove the model captures real aerodynamics. The joint fit is the tested main
path; `--one-coefficient` is recovery with linear drag assumed known.

**Gradients:** autodiff here is JAX through generated functions and a fixed-step
rollout. It computes derivatives of that numerical computation. It is neither
finite differences nor a demonstration of compiler-native reverse-mode AD.
Finite differences are an independent validation check. Lean proves scoped
exact-real invariants, not statistical recovery. See [MATH_REVIEW.md](MATH_REVIEW.md)
for papers, theorem mapping, profile diagnostics and all assumptions.

**Control:** default target (4,2) m in 6 s, all terminal rates/velocities zero
at nodes. 60 intervals, dimensional normalization before weighted cost,
thrust/torque/altitude/pitch bounds and illustrative rotor allocation. Cost
about 5.118, not a measure of electrical energy. Node pitch margin is 0.01 rad; independent adaptive rollout
peaks near 0.542 rad, below the 0.55 physical limit. Terminal altitude is about 2.1 mm from the
node target under independent integration. State constraints at nodes and
sampled checks do not provide an all-time formal certificate. IPOPT success
does not establish global optimality. This is open loop; MPC is discussed only.

## Demo recovery decisions

- **First browser load fails:** keep the real screenshot visible, explain the
  edit, retry once. Move into local VS Code or pair work immediately.
- **Cloud not ready by 10:35:** use presenter local path and participant pairs;
  do not ask 50 people to download Docker. Browser-only attendees predict and
  interpret rather than waiting through an installation.
- **Fit fails or model edits diverge:** return to defaults and run joint fit.
  Try one-coefficient recovery once. Then display the committed, clearly labeled
  reference figure and explain the real commands/evidence.
- **Optimization fails:** inspect source-hash message; refit after source edits.
  Restore canonical defaults and use the committed reference fit/warm start.
  If still failing, show the reference trajectory and state that the live solve
  failed. Do not claim reference figures were generated by that failed run.
- **Running late:** move to paired/demo recovery; omit stretch questions and appendix.
  Keep both breaks, finish the core fit→optimization and reserve the app
  exploration and closing invitation. Use gallery screenshots if apps cannot
  load promptly. No native AD, full visual SLAM, MPC or Colab rescue demo is required.

## Research slides: evidence and wording

Open with why Rumoca: separate implementations of the same physical equations
can drift. We want one declared model to feed simulation, identification,
optimization and mathematical analysis. Slide 3 introduces our broader work:
Lie group theory for structured motion, reachable-set computation for
cyberphysical systems under uncertainty, formal software verification, system
identification and digital twins. The
[model library](https://github.com/CogniPilot/modelica_models) supplies geometric
models and verification-oriented functions; these are building blocks with
explicit proof obligations. Today's planar exercise does not compute a reachable
tube or certify generated machine code. [Math context](MATH_REVIEW.md) links
primary sources for the broader ideas.

Slide 21 promotes the next **PURT pylon racing competition**, which will leverage
Rumoca. Share the [competition site](https://pylon-racing.geddes.rcac.purdue.edu/)
and the slide's QR code. The public site explains the digital-twin-to-flight-test
format; its currently listed dates are for April 2026. Refer attendees to future
announcements for the next event's dates, rules, registration and exact integration.

The [official PURT page](https://engineering.purdue.edu/PURT) supports discussion
of motion-capture experiments, aircraft testing, fixed-wing racing and security
applications. The [Purdue faculty profile](https://engineering.purdue.edu/AAE/people/ptProfile?resource_id=37293)
identifies James Goppert’s School of Aeronautics and Astronautics affiliation and
PURT leadership. Use the precise school name even when speaking informally of
Purdue Aerospace Engineering. Georgia Tech is the event venue; no implied
Georgia Tech endorsement of the software or proof results.

The public [CogniPilot workspace](https://github.com/CogniPilot/cognipilot_workspace)
documents pure-Modelica dynamics, host Zephyr software-in-the-loop and FastDyn/
QEMU binary-in-the-loop rehosting of Cortex-M7 firmware. **Documented upstream;
not executed during this workshop.** Avoid performance claims without a cited
benchmark. Monte Carlo and reinforcement learning are application directions;
no result from those workflows is shown here.

App exploration at 12:45: use [BROWSER_APPS.md](BROWSER_APPS.md). Explain that
coding agents helped create these applications, while engineering review and
validation remain essential. Lead with the more complete **rumoca_fixed_wing** workbench and its
controller-rate experiment. No API key or agent account is needed to use it.
Participants may explore for four minutes or finish their own app. Present
**slam_web as another example in development**.
Full visual SLAM is pending; the tested inertial baseline is the appropriate
short SLAM Lab exercise. Stored mocap benchmark metrics were not regenerated
or independently validated by this workshop. Gallery models are outside the
planar quadrotor’s proof scope.

Future roadmap in Appendix A3: unified vision/SLAM/estimation and physics; compiler-scale
differentiation; richer browser/FMI/WASM workflows; CPU/GPU/embedded partitioning.
Label these **research directions**. The current browser demonstration is real,
but it does not establish these larger future workflows or million-variable
scalability. Native AD/airfoil sensitivity is not demonstrated or benchmarked
in this workshop. No unrelated evolving project is on the critical path.

Suggested close: “You bring Modelica knowledge we need. Bring a model from
your domain, one scientific question and one result we can check together.
Help us make declared mathematics reusable across tools.” Use the closing QR
to open [COMMUNITY.md](COMMUNITY.md) and its research/model collaboration form.
Invite attendees to speak with James Goppert or Micah Condie before leaving.
Ask which model from their work they would try next, and leave time to listen.

## Optional interactive experiment challenge

Announce [CHALLENGE.md](CHALLENGE.md) on slide 2: apply Rumoca to a question you
care about. One change to an existing model, controller or simulator and one
checked comparison is enough. Public GitHub hosting, a new WASM app and coding
agents are optional. Keep power users experimenting during downtime while the
core walkthrough remains available to everyone.

Point to the short experiment prompt in [APP_PROMPT.md](APP_PROMPT.md). The
full Three.js launch-app, fixed-wing app and ambitious AD-based MPC prompts are
optional stretches. Falcon 9-style interactivity is inspiration; no qualified
rocket model is supplied. Welcome equally small experiments in other domains.

Collect entries by 12:40: name/team, question, starting model/app, original change,
tool used, elapsed work time and a ready interaction or before/after comparison.
Local files, tabs and screenshares are acceptable; public links are optional.
Say “manual” if no agent was used. One entry per participant or team prevents
multiple projects from adding extra draw chances. The readiness check does not
rank polish, complexity or experience.

If more than five entries are ready, draw five at random plus one backup;
otherwise all present. Draw their order and announce it by 12:45. Explain the
rules at the opening. Give each presenter 45 seconds; five demos leave
75 seconds for the hand vote and award. Have tabs/files ready. Each demo names
the question, change, result, one check, tool and elapsed time. Each attendee votes
once. Count visibly; resolve a tie with a quick revote, then a draw if needed.
Award one CogniPilot stocking cap; a winning team chooses its recipient.
Use the gallery for voluntary links. If no entries are ready, take a brief
question and continue to the close.

## Rehearse the guide and extensibility showcases

Slide 8 uses the [user guide](https://cognipilot.github.io/rumoca/user-guide/),
with embedded editors and examples. Use the exact NACA link and short two-second
sequence in [WORKSHOP.md](WORKSHOP.md). Warm the successful WebGPU tab before
class; use the labeled saved capture for graphics/network recovery. Describe
artificial-compressibility and penalization as a coarse qualitative teaching
model. Do not claim aerodynamic prediction, lift/drag accuracy or GPU speedup
from the UI rehearsal. Other guide examples include turkey heating and a membrane.

Slide 17 makes extensibility concrete. Preinstall the optional CPU Torch group
in the presenters’ Linux x64 Codespace. Open `templates/torch-ode/target.toml`,
then the generated RHS, run its check, and show the hover-policy result. The
[backend guide](BACKENDS.md) gives commands, assumptions and a small extension
exercise. Sixty Adam updates took 14–27 seconds across the two-core
Codespace rehearsals; first package downloads are separate. This is differentiable
model-based policy optimization restricted to vertical motion, a bridge to RL.
Keep the group optional so all other participants stay with the core exercises.

Connect both to the vision: declarative Modelica for cyberphysical systems,
solver specialization for heterogeneous compute, fast batched Monte Carlo/RL,
native AD and integrations, and small independently checked target extensions.
Today's checked CPU workflow and experimental browser GPU demo support concrete
starting points; broad hardware partitioning and scaling remain research work.
