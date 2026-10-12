# Try our agent-built browser applications

**12:45–12:50 · Lead example: rumoca_fixed_wing. No install or account needed.**

Coding agents helped us build these interfaces and experiments. We still review
the equations, decide what the experiment means and check the output. An agent
can help develop a model; its output is evidence to examine, not a validation
certificate. Use the apps manually during this workshop.

Start with **rumoca_fixed_wing**, our more complete agent-built app example.
Try the controller-rate interaction below and inspect its Modelica source.
**slam_web is another example in development**; the short inertial exercise
works, while the full visual-SLAM pipeline is still being developed.
**mocap_sysid** illustrates a stored-data and benchmark-results viewer.

Allow one minute for the introduction and four minutes to explore. Open one
app at a time on a modest laptop. If you are entering the
[open experiment challenge](CHALLENGE.md), you can use this time to finish your own
demo instead. Participant demos and the audience hand vote begin at **12:50**.

| App | Open the live app | Source | Short experiment |
|---|---|---|---|
| Fixed-wing Modelica workbench | [rumoca_fixed_wing](https://cognipilot.github.io/rumoca_fixed_wing/) | [GitHub](https://github.com/CogniPilot/rumoca_fixed_wing) | Run a waypoint autopilot; change controller update rate. |
| SLAM Lab | [slam_web](https://cognipilot.github.io/slam_web/) | [GitHub](https://github.com/CogniPilot/slam_web) | Run the inertial baseline; compare a filter variant and sensor views. |
| Motion-capture identification viewer | [mocap_sysid](https://cognipilot.github.io/mocap_sysid/) | [GitHub](https://github.com/CogniPilot/mocap_sysid) | Inspect benchmark trajectories, splits and model information. |

## Fixed-wing: controller rate and flight

1. Wait for the dataset controls and editor to finish loading. Select
   **Autopilot** in the simulator’s tabs above the aircraft view.
2. Click **Start sim** (or **Start autopilot**). Wait for the Modelica controller
   and plant to compile. Watch the waypoint readout and simulated time advance.
3. Predict what reducing the controller update rate might change. Switch
   **50 Hz → 20 Hz**, click **Start sim** again to compile at the new rate,
   observe, then **Pause**. A few seconds is a qualitative
   observation, not a controlled performance comparison.
4. Inspect the **Autopilot** source tab below the view. Which model parameter,
   control limit or timing assumption would you validate before an aircraft test?

This application compiles its own fixed-wing plant and controller in WASM; it
does not run the workshop’s planar quadrotor or CasADi optimizer. Playback is
recorded flight data; an autopilot simulation is a different mode. Keep those
sources distinct when discussing what you see.

## SLAM Lab: inertial propagation and sensors

1. Wait until **Run** is available, keep **SLAM.Examples.InertialOnly**, then
   click **Run**. Inspect the world, RGB/depth views and trajectory display.
2. Click the same button to pause. Select
   **SLAM.Examples.ResponsiveInertial** under **Run model**, wait until ready,
   and run again. Predict the responsiveness/noise tradeoff; inspect the
   Modelica filter time constants. Pause before leaving the app.
3. Name a quantitative comparison you would make using identical sensor inputs.
   A visual impression alone does not establish which filter is better.

The supported short exercise is **inertial propagation with simulated sensors**.
Full connected visual SLAM, mapping/loop closure and robot/FMUs deployment remain
development work. A source file appearing in the library is not evidence that
its whole pipeline runs. Software WebGL rendering activates a reduced preview;
use it, lower graphics if needed, or compare the recorded screenshot.
Simulation speed depends on the browser/device; “1× real time” is a requested
rate, not a performance guarantee.
The manual exercise uses the simulation controls, with no provider credentials.

## Motion capture: inspect results before trusting a score

1. Under **Dataset**, choose **6-DOF open-loop maneuver** for the synthetic
   benchmark. Open **Time Histories**, then **Data Splits**.
2. Open **Models** and select **LinearSS**. Compare the mathematical model
   information with the available trajectory results and validation metrics.
3. Identify training versus validation information. Does a low normalized score
   settle the physical accuracy question? Which units and assumptions matter?
   Optional: select a Sport Cub motion-capture dataset to see the experimental
   context, keeping synthetic and measured sources distinct.

The viewer displays exported benchmark results. We do not retrain these methods
in the workshop or independently reproduce their published metrics. The
**Time Histories / Data Splits / Models** experiment does not invoke WASM;
this viewer complements the two WASM demonstrations.

## Evidence and recovery

Public UI rehearsal and actual screenshots are recorded in `verification/app-*.json`
and `slides/assets/app-*.png`; [VERIFICATION.md](VERIFICATION.md) states the exact
tested actions. These applications use different models, releases and datasets.
The planar-model Lean proofs and numerical audits **do not cover these apps**.

The rehearsed routes passed October 11 in Chromium with software WebGL: fixed-wing
controller/plant and both rates (about 14 s for the complete test), two SLAM Lab
inertial examples (about 25 s), and benchmark view/split/model selection (about
6 s). These times include page loading and the tested actions, not an algorithm
performance benchmark or a guarantee for every participant’s device.

If loading takes over a minute or the graphics are unresponsive, use a partner’s
working browser or the recorded screenshots. Continue the prediction/validation
exercise and finish at **12:50** for the participant demos and audience vote.
Closing questions run 12:55–13:00.

## A creative example: reusable-booster landing

[Open the interactive user-guide example](https://cognipilot.github.io/rumoca/user-guide/simulation/reusable-booster-landing.html), a Falcon-9-like teaching scenario.
Inspect the Modelica and scenario TOML tabs, run it, focus the scene and press
**Space** to launch. Change wind in **Tune environment and controller**, then
**R** to reset and compare. **Q** stops.
The [copied upstream source](../extras/reusable_booster/README.md) is available
for inspection. Native execution of that snapshot needs the upstream pinned
library and has not been qualified here. It is not a validated SpaceX model.
