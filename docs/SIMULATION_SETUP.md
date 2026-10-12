# Configure and visualize a quadrotor simulation

Open the [user guide’s Quadrotor SIL example](https://cognipilot.github.io/rumoca/user-guide/simulation/interactive.html#quadrotor-sil).
Slides 8–11 walk through its actual scenario and Three.js scene. This example
uses a full 3D vehicle and controller; the workshop’s `models/Quadrotor.mo`
is a smaller planar model for the Python Session API exercises.

## Start a run

In **VS Code**, open a `.mo` file and click the **lightning-bolt Create Rumoca
Scenario** icon. This creates the TOML; then use the scenario’s **Settings**
form or text editor, save, and **Run Current Rumoca Scenario**. The Command
Palette offers the same Create and Run commands.

For this richer example, use the deployed **user-guide editor**. Click its
**Settings** button to inspect the scenario, then **Simulate**. Its scenario
already selects an interactive scene. Keep GPU off for this CPU walkthrough.
Wait for the scene to initialize, then press **Capture** to enable keyboard
input. Space arms/disarms at low throttle, W/S raises/lowers throttle,
arrows command roll/pitch, A/D yaw, R resets. Esc releases capture; **Stop**
ends the run. Start with brief taps and reset between comparisons.

The ACRO wrapper commands angular rates. Neutral sticks do not command level
attitude or altitude hold. Its arming gate is a simulator interaction rule.

The deployed browser runtime is separate from the container’s pinned Rumoca
0.10.2 Python package and editor. The full CMM-dependent SIL model is linked
from the guide, rather than installed as the small workshop plant.
[The planar VS Code exercise](WORKSHOP.md#configure-a-simulation-lightning-bolt--toml--run)
is the native fallback.

## Read the TOML from top to bottom

Use the [actual quadrotor scenario](https://github.com/CogniPilot/rumoca/blob/main/examples/interactive/quadrotor/rumoca-scenario.acro.toml)
and [scenario reference](https://cognipilot.github.io/rumoca/user-guide/simulation/scenario-tomls.html).
The snippets below are selected sections of that file, not a standalone
replacement for its full input and viewer configuration.

```toml
source_roots = ["../../../target/cmm/CMM-a642c381"]

[rumoca]
version = "1"
task = "simulate"

[model]
file = "QuadrotorSIL.mo"
name = "QuadrotorAcro"

[sim]
solver = "rk-like"
dt = 0.01
mode = "realtime"
```

| Setting | What it controls |
|---|---|
| `source_roots` | Extra Modelica package directories. A top-level key, before any section. The upstream example needs the CMM library. |
| `[rumoca].version` | Scenario schema version, **not** the installed compiler release. |
| `task` | Simulation versus code generation. |
| `[model].file` | Source file; paths resolve relative to this TOML. |
| `name` | Class to compile. Here `QuadrotorAcro` wraps the plant with controls. |
| `solver` | `rk-like` for the explicit solver family; `bdf` for stiff cases; `auto` chooses automatically. |
| `dt` | Simulation advance/scheduling interval. 0.01 s requests 100 advances per simulated second, independently of display FPS and adaptive internal solver steps. |
| `mode` | `realtime` paces against wall time; `as_fast_as_possible` removes sleeps; `lockstep` advances with an external packet. |
| `t_end` | Batch/results-panel horizon. Live interactive runs require an explicit stop. |
| `atol`, `rtol` | Optional numerical error tolerances. Check important results by tighter tolerances or refinement. |

For a native run **inside the Rumoca source repository**, first run
`cargo xtask repo modelica-deps ensure` to prepare the CMM dependency. That
upstream-relative path is not a portable path into the workshop checkout.
A realtime mode is a pacing policy; it does not guarantee a slow computer
meets the requested deadline.

## Trace one control into the Modelica model

```toml
[input]
mode = "auto"

[locals.throttle]
type = "float"
default = 0.0

[input.gamepad.integrators.throttle]
source = "LeftStickY"
write = "throttle"
rate = 0.7
deadband = 0.1
clamp = [0.0, 1.0]

[signals.model_inputs]
stick_throttle = "local:throttle"
armed = { from = "local:armed", when_false = 0, when_true = 1 }
```

The integrator accumulates a persistent `throttle` local from the stick, with
rate, deadband and clamp. Keyboard W/S sets `throttle_input`; the keyboard
integrator writes the same `throttle` local. A direct axis mapping replaces
its command instead of accumulating it. Local state is the input interface;
Modelica still computes the vehicle and controller.

```toml
[input.keyboard.keys.Space]
action = "toggle"
state = "armed"
debounce_ms = 500
precondition = "throttle <= 0.05"
```

The arm command needs low throttle. `debounce_ms` limits repeated toggles.
The full file also declares the Boolean `armed` local. Its numeric Modelica
input receives 0 or 1 through `signals.model_inputs`.

**Try one change:** in Settings, change the **keyboard** throttle integrator
rate from 0.7 to 0.3. Reset and compare equal W taps. Predict a slower throttle
increase, then check the displayed command. If using a gamepad, change its
integrator rate instead. Restore 0.7 afterward.

Keyboard decay (`factor=0.85`, `ref_dt=0.016`) relaxes released commands;
it is input shaping. `[reset]` chooses whether a reset clears both simulation
and locals. `[[viewer.controls.keyboard]]` supplies help labels;
`[input.keyboard.keys.*]` supplies behavior.

## Name the signals the viewer reads

```toml
[signals.viewer]
px = "model:position[1]"
py = "model:position[2]"
pz = "model:position[3]"
q1 = "model:quat[2]"
q2 = "model:quat[3]"
q3 = "model:quat[4]"
omega_m1 = "model:omega_m[1]"
armed = "local:armed"

[signals.viewer.q0]
from = "model:quat[1]"
default = 1
```

`model:` reads physical channels, `local:` reads input state, and `runtime:`
reads execution metadata such as frame number. Aliases like `px` are display
names, not additional dynamics. The full file routes all four motors and
velocity channels. `[[viewer.frame]]` groups position and scalar-first
quaternion channels into the `body` frame; camera mounts and HUD settings
reference that frame.

## Connect the Three.js scene

```toml
[transport.http]
port = 8080
scene = "quadrotor_scene.js"
asset_dir = "../../assets"

[transport.websocket]
port = 8081
```

These settings serve the **native** HTTP viewer, assets and WebSocket state
stream. The embedded guide hosts its own browser surface. No native port
forwarding is needed to try it. A native Codespaces viewer needs both ports
forwarded and a reachable secure WebSocket URL. UDP/schema routes are only
needed when connecting an external process; this keyboard demo uses the
controller already in the Modelica wrapper.

Open [the actual scene script](https://github.com/CogniPilot/rumoca/blob/main/examples/interactive/quadrotor/quadrotor_scene.js).

| Script hook/API | Purpose |
|---|---|
| `ctx.onInit(api)` | Create lighting, load the drone GLB/textures, prepare propeller groups and camera anchors once. |
| `api.THREE`, `api.GLTFLoader` | Host-provided Three.js library and asset loader. |
| `api.state` | Persistent meshes and other display objects. |
| `ctx.onFrame(api)` | Read the latest state and update the display each animation frame. |
| `api.get("px")` | Read a named `signals.viewer` channel. |

The script’s position mapping is:

```js
const get = api.get;
const px = get("px") ?? 0;
const py = get("py") ?? 0;
const pz = get("pz") ?? 0;
const tx = -py, ty = pz, tz = px;
```

The model uses **Forward–Left–Up**. The mesh uses **+Z forward, −X left,
+Y up**. Therefore model +x maps to scene +z, +y to −x, and +z to +y.
The same basis change must also transform attitude:

```text
A = [ 0 -1  0 ]       p_scene = A p_model
    [ 0  0  1 ]       R_scene = A R_model A⁻¹
    [ 1  0  0 ]
```

The full script constructs a rotation matrix from scalar-first `(q0,q1,q2,q3)`
and applies this transformation before writing `quad.matrix`. Identity attitude
must remain identity. Three.js’s Quaternion constructor instead takes `(x,y,z,w)`;
passing the Modelica quaternion in scalar-first order gives a wrong view.
A stale upstream DCM comment says “NED”; the model and the applied transform
are FLU. Follow the explicit model axes and transformation.

Motor channels and the armed flag drive a bounded, illustrative propeller
animation; its per-frame visual angle is not the physical motor integrator.
Camera following, shadows, HUD and colors are presentation choices. Change a
color, add a trail or move the camera for your experiment; keep vehicle physics
and controller equations in Modelica.
