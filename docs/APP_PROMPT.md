# Example agent prompts: make something you care about

**Start with one useful experiment. Build a new app only if you want the stretch.**

The competition invites you to **apply Rumoca to any problem you care about**.
These are inspiration, not assigned projects. Power users can build with their
agents during downtime and independent work. Choose your own subject and make
the experiment yours. The full AD-based MPC idea below is **ambitious** and optional.

## Small starting prompt: one change, one checked result

```text
Help me explore a problem I care about with Rumoca. Start from a working
Modelica example or an existing interactive simulator; preserve its working
baseline. Use the workshop's tested playground or Codespace/local Python route.

Ask what behavior I want to explore. Propose one small model, controller or
scenario change I can finish during workshop downtime. Compare before and after,
make the effect visible in the existing interface or a plot, and check one result
against an analytic case, physical sign, numerical baseline or stated constraint.

Do not require a new web app, WASM toolchain, public repository or deployment.
Keep assumptions and units visible. Explain my contribution and credit the
starting example. Prepare a 45-second demo: question, change, result and check.
Record the agent/tool used and elapsed work time; label estimates.
```

An interactive rocket landing can inspire the presentation, like a Falcon 9-style
simulator; no qualified rocket starter is supplied. Choose another domain if it
fits your interests better. The following full-app prompts are optional stretches.

## Creative example: an Artemis-inspired launch lab

```text
Build a public, browser-only Artemis-inspired launch experience with Rumoca
physics and Three.js visuals. Publish it on my GitHub and deploy it with GitHub
Pages. You have three hours. Make creative choices about the experience: a
mission-control dashboard, payload challenge, launch replay, or something else
that lets a visitor ask a question and see the model respond.

Start small: write a compact Modelica model of vertical powered ascent with
altitude, vertical speed and remaining propellant. Use consistent SI units,
variable mass, gravity and a simple declared atmosphere/drag approximation.
Choose illustrative parameters and a short burn interval that preserve positive
mass and propellant. Document the operating bounds and assumptions. This is
an educational model, not a reconstruction of an actual SLS flight or an
orbit/Moon-mission predictor.
Use NASA's public SLS references for visual inspiration and cite sources.

Inspect https://github.com/CogniPilot/rumoca_fixed_wing for a working browser
Rumoca WASM/editor integration and its pinned npm package. Reuse that plumbing
with attribution; do not require its full fixed-wing model for the rocket.
Inspect https://github.com/CogniPilot/modelica_models for useful reusable models;
keep the small standalone launch model if reuse would expand the dependency
tree. Verify actual exported APIs and pin the versions you use.

Compile and simulate the actual Modelica in browser WASM. Use Three.js for a
rocket, launchpad, camera and flight trail driven by the simulated altitude.
Build the initial scene from simple geometry; detailed assets and particles
are extras. Clearly separate visual scale and playback speed from SI units
and simulated time. Keep the Modelica source editable with compilation errors
visible. All deployed computation runs locally: no Python server, simulation
API, login or secret key. Bundle runtime dependencies for GitHub Pages.

Pick ONE interaction first: payload or throttle within your documented range.
Reset/recompile and rerun. Show altitude, speed, remaining propellant
and dynamic pressure with units. Stop at the chosen burn interval, or earlier if the state leaves
the model's domain. Never continue with negative fuel or silently clamp it.
Show a baseline and one changed run. Give the visitor a question to explore;
you choose the narrative and visual design. Staging and guidance are optional
extensions requiring new Modelica dynamics and their own checks, not just an
animation presented as simulated physics.

0–30 min: compile/run the unchanged model and publish a working baseline.
30–90 min: add Three.js and one useful interaction; keep it deployable.
90–150 min: test reset/repeat, finite states, fuel/mass bounds, and compare the
           no-drag, constant-gravity case with the ideal rocket equation,
           including gravity loss. Check timestep refinement too.
150–180 min: polish the creative experience and rehearse a 45-second demo.

Test the actual deployed Pages URL, WASM, workers, editor assets and repository
subpaths. If a compiler issue appears, isolate a minimal reproducer and fix it
in your fork with a regression test. Timebox initial compiler debugging to
15 minutes and preserve the last working version. Publish usage, assumptions,
sources and test evidence; keep credentials and private working notes out.

Record the agent/tool, model/version when available, and elapsed wall time from
starting to the demo-ready app, including debugging and deployment. Label any
estimated time. Finish with GitHub + live URL and a 45-second demo: the problem,
one interaction, one checked result, and “built with [agent] in [time].”
```

This is only an example prompt: no Artemis app or rocket model is supplied by
the workshop. The core Modelica → JAX → CasADi exercises remain the main activity.
NASA sources: [SLS overview](https://www.nasa.gov/reference/space-launch-system/),
[rocket momentum/ideal rocket equation](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/ideal-rocket-equation/)
and [drag/dynamic pressure](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-equation/).
Visuals: [Three.js documentation](https://threejs.org/docs/).

## Reuse a working app: Tune the autopilot

```text
Build a public, browser-only “Tune the autopilot” flight lab. Publish the source
on my GitHub and deploy it with GitHub Pages. You have a three-hour timebox;
keep a working, deployed version throughout.

Start from https://github.com/CogniPilot/rumoca_fixed_wing. Reuse its working
3D flight view, Monaco Modelica editors, Modelica plant/controller and pinned
Rumoca WASM package. Preserve attribution and licenses. Use
https://github.com/CogniPilot/modelica_models as the model-library source:
inspect Vehicles/Templates/FixedWingPlant.mo and the provenance of the
workbench's bundled fixed-wing model. Pin the versions actually used. Keep
the proven bundled model as the initial runnable example.

All Modelica compilation and simulation must run locally in browser WASM.
HTML/JavaScript may implement the interface and plots. The deployed app must
need no Python server, cloud simulation service, login or API key.

Make it easy to run the existing waypoint autopilot, then change ONE setting:
cruise speed, an existing controller gain, or controller update rate. Start
with a modest range around the existing default; inspect the actual parameter
names, units and bounds. Keep the Modelica source editable. Apply edits by
recompiling the actual controller, reset, and rerun. Show compilation errors
beside the editor. Never substitute a different handwritten plant.

Save a baseline run and a modified run. Overlay their flight trails and show
waypoint progress, simulated completion time, cross-track error and command
activity. Use identical initial conditions, the same ordered waypoint course,
the same simulation duration and the same output sample times. Pause/reset
must work, and the UI must remain responsive while simulation runs.

Define the metrics clearly. Cross-track RMS is measured in metres relative
to the active waypoint-course segment. Report ordered waypoint completion
alongside it; a stationary aircraft has not completed the course. Mark
unfinished runs explicitly and leave completion time blank. Command activity
is the time mean of squared normalized actuator commands; it is dimensionless
and is not an electrical-energy measurement. State which commands are included.
Report simulated time separately from browser wall time.

Deliver in stages:
  0–30 min: reproduce the unchanged workbench and deploy it on my GitHub Pages.
  30–60 min: add one parameter control, editor/recompile/reset, and a second run.
  60–120 min: add the trail comparison and clearly defined metrics.
  120–150 min: run browser checks, fix problems, and verify the live Pages URL.
  150–180 min: simplify, polish, and prepare a short demo. Add extras only after
               the main interaction works. Freeze new features for the finish.

Verify the actual public deployment, including repository subpath URLs,
WASM loading, workers and editor assets. Run baseline and modified settings,
check finite states and commands, then pause, reset and repeat. Check that the
default behaves consistently after reset and a source edit changes the real
simulation. Include screenshots and a small machine-readable run report.

If you find a Rumoca issue, isolate it in a minimal Modelica reproducer and
add a regression test. Develop a focused fix in your own fork/branch and
verify a rebuilt browser bundle before using it. Timebox compiler debugging
to 15 minutes at first; retain the last working app and show a clear status
for an unavailable extra. Publish code, usage instructions, attribution and
test evidence; keep credentials and private working notes out of the repo.

Record the agent/tool, model/version when available, and elapsed build wall
time including debugging and deployment. Label estimated times.
Finish with the public GitHub URL, live GitHub Pages URL, exact tested actions,
and a 45-second demo: baseline → one change → rerun → compare.
```

The existing app already runs a Modelica plant and waypoint controller in WASM;
the workshop rehearsed both 50 Hz and 20 Hz through its public UI.
[Run it](https://cognipilot.github.io/rumoca_fixed_wing/) and
[see the receipt](../verification/app-rumoca_fixed_wing.json).
A [fresh-checkout rehearsal](../verification/app-starter.json) also reproduced the
unchanged app from its pinned source and npm package.
The new comparison app is a challenge specification, rather than a completed
app or a guarantee about a particular agent's three-hour performance.

## Ambitious extension: AD-based fixed-wing MPC

Keep the main app working before attempting this extension. Copy this as a
follow-up only when you want a larger project:

```text
Extend the flight lab with model-predictive control implemented in Modelica
and compiled to browser WASM. Reuse the fixed-wing Modelica plant and inspect
CogniPilot/modelica_models Control/Mpc interfaces and their documented limits.
Use automatic differentiation for the MPC prediction Jacobians or rollout
gradients; finite differences may check AD, but must not supply the optimizer's
derivatives. Inspect the actual pinned WASM exports before choosing an API.
If a needed AD surface is missing, add a small tested WASM binding to an
existing Rumoca AD path in an isolated fork, preserving the working baseline.

First establish and verify a level-cruise trim for the actual plant. Define a
nominal straight flight path in its world frame, advancing with cruise speed
at constant altitude. Report trim residuals, units and frame conventions.
Start with a short horizon and longitudinal tracking; retain the existing
lateral stabilization. Optimize the control sequence against normalized path,
speed and command-change costs, apply only the first command, shift the warm
start, measure the new state and solve again. Include actual actuator bounds.
Clipping an unconstrained solution alone is not a constrained MPC solve.

Implement the controller states, sampled update and controller equations in
Modelica. State clearly where generated AD and solver support execute in WASM.
Differentiate the discrete prediction used by the optimizer, including its
integration steps. Check gradients at interior trim and perturbed states
against finite differences at several step sizes. Verify tracking, commands,
constraint violations and solve times in repeated browser runs. Compare with
the existing controller under identical conditions. Label numerical feasibility
and remaining limitations accurately; do not claim a real-flight safety proof.

This is ambitious. Within the same three-hour timebox, preserve the published
flight lab as the useful deliverable and label incomplete MPC/AD work clearly.
```

The current [Modelica MPC library](https://github.com/CogniPilot/modelica_models/blob/main/Control/Mpc/package.mo)
documents an unconstrained first milestone and a finite-difference
linearization adapter. [Rumoca's AD documentation](https://github.com/CogniPilot/rumoca/blob/main/docs/user-guide/src/language/neural-odes.md)
describes native Rust optimization APIs. Neither establishes a complete
browser AD-MPC controller. The extension must verify its own integration.

[GitHub Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
and the fixed-wing repository's deployment workflow provide the static hosting
starting point. [CHALLENGE.md](CHALLENGE.md) gives the demo and audience-vote rules.
