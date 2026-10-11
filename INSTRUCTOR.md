# Instructor guide

**James Goppert · Purdue University, School of Aeronautics and Astronautics**  
American Modelica Conference · Georgia Tech · October 12, 2026 · 10:00–13:00

Use [slides/workshop.pptx](slides/workshop.pptx); its speaker notes and
[editable source](slides/workshop.md) carry the timed cues. Keep the PDF and
reference figures on your laptop. Participant entry:
<https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/WORKSHOP.md>.

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

| Clock | Slides | Activity / instructor cue |
|---|---|---|
| 10:00–10:10 | 1–2 | Welcome, core outcomes and **open app challenge**. Announce GitHub demos, audience hand vote and stocking-cap prize now. |
| 10:10–10:20 | 3–4 | Motivation and compiler bridge. Connect declared physics to different questions. |
| 10:20–10:40 | 5–7 | Browser plot, cloud/local setup and smoke. Experienced participants can begin their app when ready. |
| 10:40–11:00 | 8–10 | Introduce the small model, change a parameter, run and inspect the plot. Assume no aerospace background. |
| 11:00–11:10 | 11 | **Break 1**, ten full minutes. Leave recovery link visible. |
| 11:10–11:50 | 12–14 | Synthetic data, prediction error, JAX fit and before/after outputs. App builders use independent work time. |
| 11:50–12:00 | 15 | Checkpoint and independent work/questions. Offer detailed mathematics only when requested. |
| 12:00–12:10 | 16 | **Break 2**, ten full minutes. Leave next command visible. |
| 12:10–12:40 | 17–18 | Constraints, CasADi solve and plots. Optional target variant or continued app development. |
| 12:40–12:45 | 19 | PURT/upstream work; connect models to experiments and the lead app example. |
| 12:45–12:50 | 20 | Explore **rumoca_fixed_wing** or finish challenge demos. Show SLAM as another example in development. |
| 12:50–12:55 | 21 | Short participant demos, then **audience show-of-hands vote** and stocking-cap award. |
| 12:55–13:00 | 22 | Questions, research invitation and take-home links. |

Total **180 minutes**, including **20 minutes of breaks**. Aim for roughly
35–40 minutes of explanation; the remaining teaching time is guided work,
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
- **Cloud not ready by 10:35:** use instructor local path and participant pairs;
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

Suggested close: “Bring a hard modeling, identification,
optimization or cyber-physical testing problem. We’re building open-source
tools and validating ideas on real systems at Purdue. Let’s find a useful
research question together.”

## Optional app challenge

Announce [CHALLENGE.md](CHALLENGE.md) on slide 2. The theme is open: participants
can build a new app or extend an existing one with coding agents, publish it on
their own GitHub and explain their contribution. The main exercise remains
accessible without agent tools or a GitHub account. Keep advanced participants
working during the independent portions; use the practical checkpoints rather
than requiring a specialist aerodynamics discussion.

At 12:50, allow four minutes for short demos and one minute for an audience vote.
Up to four entries get one minute each; more entries share the time equally.
Each attendee votes for one entry by a show of hands. Count visibly, resolve a
tie with a quick vote among the tied entries and, if needed, a draw. Award one
free CogniPilot stocking cap to the winning entry. A winning team chooses its
recipient. If there are no entries, take a brief app question and continue.
