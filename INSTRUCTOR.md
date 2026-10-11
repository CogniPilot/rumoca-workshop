# Instructor guide

**James Goppert · Purdue University, School of Aeronautics and Astronautics**  
American Modelica Conference · Georgia Tech · October 12, 2026 · 10:00–13:00

Use [slides/workshop.pptx](slides/workshop.pptx); its speaker notes and
[editable source](slides/workshop.md) carry the timed cues. Keep the PDF and
reference figures on your laptop. Participant entry:
<https://github.com/CogniPilot/rumoca-workshop/blob/main/WORKSHOP.md>.

## Tonight’s review — five personal checks

1. Open the PPTX/PDF on your presentation laptop, inspect equations at projector
   scale and rehearse browser → editor → PNG switching. Keep local backups.
2. Open a **fresh Codespace** with the actual presenting account; confirm
   remote extension activation, interpreter, terminal, smoke PASS and startup
   time. Check your/organization billing, quotas and region availability.
   Without this, announce browser + qualified local `uv` as the default.
3. Check venue network, projector resolution and accessible power. Ask who has
   no GitHub account; assign pair/demo seats rather than delaying the class.
4. Rehearse the three commands on the presenting laptop and make one drag edit.
   Return to a clean source before using reference results. Run smoke once.
5. Review final research/collaboration wording and confirm your preferred public
   contact details. Public slides make no pricing, staffing or IP promises.

The automated check could not access Codespaces because the available token
lacks the `codespace` scope. No cloud quota, prebuild readiness, startup, remote
LSP activation or 50-user concurrency is asserted. See [PUBLICATION.md](PUBLICATION.md).

## Facilitation and pacing

| Clock | Slides | Activity / instructor cue |
|---|---|---|
| 10:00–10:10 | 1–2 | Welcome, four outcomes. Ask for Modelica/JAX/CasADi experience by show of hands. |
| 10:10–10:20 | 3–4 | Motivation and compiler bridge. Explain what Rumoca adds; respect established tools. |
| 10:20–10:40 | 5–7 | Everyone gets a browser plot, then cloud/local setup. Cap individual setup help at 10 minutes. |
| 10:40–11:05 | 8–10 | Explain frames, predict drag, edit/run, compare. Circulate and ask what changed physically. |
| 11:05–11:15 | 11 | **Break 1**, actual ten minutes. Leave recovery link visible. |
| 11:15–11:50 | 12–14 | Synthetic data, noise-scaled loss, run JAX fit, inspect training and held-out predictions. |
| 11:50–12:00 | 15 | Pair discussion on excitation, gradients and assumptions; show proof/audit scope if asked. |
| 12:00–12:10 | 16 | **Break 2**, actual ten minutes. Leave next command visible. |
| 12:10–12:45 | 17–18 | State/control constraints, run CasADi, interpret braking and numerical defects. |
| 12:45–13:00 | 19–22 | PURT/upstream work, research frontier, collaboration, questions/take-home. |

Total **180 minutes**, including **20 minutes of breaks**. Aim for roughly
35–40 minutes of explanation; the remaining teaching time is guided work,
discussion and interpreting results. Avoid reading every slide. Appendix slides
have no extra scheduled time; open only when an audience question requires them.

## Explain the single-model choice

The existing [CogniPilot Modelica models](https://github.com/CogniPilot/modelica_models)
include a full multirotor/Lie-group formulation. That dependency-rich model was
inspected, but not qualified end to end for this workshop. We selected the
deliberately compact planar ODE to make both exports fast and the drag edit
visible. Do not say the full model is broken or supported by both backends based
on this rehearsal. No changes to the main Rumoca repository were needed.

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
about 5.118, not a measure of electrical energy. Node pitch margin 0.01 rad was
added after detecting intersample overshoot; independent adaptive rollout now
peaks near 0.542 rad, below 0.55. Terminal altitude is about 2.1 mm from the
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
- **Running late:** stop setup rabbit holes; omit stretch questions and appendix.
  Keep both breaks, finish the core fit→optimization and reserve the closing
  invitation. No native AD, SLAM, MPC, Colab or full 6-DoF rescue demo is required.

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

Future slide: unified vision/SLAM/estimation and physics; compiler-scale
differentiation; richer browser/FMI/WASM workflows; CPU/GPU/embedded partitioning.
Label these **research directions**. The current browser demonstration is real,
but it does not establish these larger future workflows or million-variable
scalability. Native AD/airfoil sensitivity is not demonstrated or benchmarked
in this workshop. No unrelated evolving project is on the critical path.

Suggested close, in your own voice: “Bring a hard modeling, identification,
optimization or cyber-physical testing problem. We’re building open-source
tools and validating ideas on real systems at Purdue. Let’s find a useful
research question together.” Sponsored research terms belong in approved
Purdue discussions. Public materials contain no unapproved funding ranges,
student allocations, licensing promises or sponsor IP guarantees.
