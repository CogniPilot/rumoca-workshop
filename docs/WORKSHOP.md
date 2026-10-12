# One model → JAX → CasADi

Follow the [slides](../slides/workshop.pdf). Use this page for commands and
checkpoints. The opening QR creates the **core** Codespace.

## Start in VS Code

Open `models/Quadrotor.mo`. This is the single source of the plant equations.
The Explorer keeps infrastructure hidden so you can focus on `models/`,
`examples/` and your plots in `results/live/`.

```sh
uv sync --frozen
```

Codespaces has already prepared the packages and installed Rumoca's Modelica
extension. Local users follow [setup](LOCAL_SETUP.md).

## Interactive quadrotor walkthrough

Slides 7–10 use the [user guide’s Quadrotor SIL](https://cognipilot.github.io/rumoca/user-guide/simulation/interactive.html#quadrotor-sil).
Follow [the simulation settings and Three.js walkthrough](SIMULATION_SETUP.md)
for the TOML, controls, signal routing and frame conversion. Then return to the
compact planar vehicle below for the Python Session API exercises.

## Configure a simulation: lightning bolt → TOML → Run

1. Open **`models/BrowserFlight.mo`**. This binds the Quadrotor's inputs to hover
   thrust and zero torque, and starts with horizontal speed 6 m/s. A simulation
   needs an experiment's inputs and initial conditions as well as plant equations.
2. Click the **lightning-bolt “Create Rumoca Scenario”** icon in the editor title.
   If it is hidden, use the Command Palette: **Rumoca: Create Rumoca Scenario**.
3. Save the generated **`rumoca-scenario.…toml`** next to the `.mo` file.
   Rumoca opens the scenario editor. This TOML describes the run; it does not
   replace the Modelica equations.
4. Check **Model = BrowserFlight**, **model file = BrowserFlight.mo**,
   **solver = auto**, and **Batch end time = 8 seconds**. Under **Plot panels**,
   replace `*states` in **y series** with `x` and `vx` on separate lines so the
   two quantities are easy to compare.
   Use the scenario settings form, or **Reopen Editor With → Text Editor** to
   inspect the TOML. Its key sections are:

   ```toml
   source_roots = ["."]
   [rumoca]
   version = "1"
   task = "simulate"
   [model]
   file = "BrowserFlight.mo"
   name = "BrowserFlight"
   [viewer]
   mode = "results_panel"
   [sim]
   solver = "auto"
   t_end = 8.0
   ```

   The newly generated TOML may omit `source_roots`: sources next to the model
   file are found automatically. The explicit `["."]` above describes that
   same folder. The default generated batch horizon is 10 seconds; change it
   to 8 in the form and save before running.

5. Save and **Run Current Rumoca Scenario**. Use the scenario editor's Run
   control or the Command Palette command. Inspect horizontal speed `vx` and
   position `x`: speed should decay and position should continue increasing.
6. Change `k_quad` in **Quadrotor.mo** from `0.0` to `0.08`, save and run again.
   Compare the plots. The TOML keeps the experiment the same while the declared
   physics changes. Restore `0.0` when you finish this comparison.

**Checkpoint:** explain which settings live in Modelica and which live in TOML.
The plant has free inputs; `BrowserFlight` supplies an experiment around it.
Python below supplies a different prescribed input experiment.

## Use the Session API with JAX

Open [simulate.py](../examples/simulate.py). Find these lines:

```python
model = rum.Session().load(str(MODEL), model="Quadrotor")
export = model.to_jax()
```

`export.rhs` is the compiled plant. Python chooses the inputs and integrates it;
it does not rewrite the vehicle equations. Run:

```sh
uv run --frozen python examples/simulate.py
```

Open `results/live/simulation.png`. At 8 seconds, the two reference cases travel
about **41.60 m** and **17.97 m**. Your current Modelica defaults are shown too.
These values belong to the Python experiment, not the native coast experiment.

Next open [fit_drag_jax.py](../examples/fit_drag_jax.py). It also starts with
`Session().load(...).to_jax()`. Find `jax.value_and_grad`: gradients pass through
Rumoca's dynamics and the integration into a noise-scaled fitting objective.

```sh
uv run --frozen python examples/fit_drag_jax.py
```

Open `results/live/fit_drag.png`. Expect estimates near **0.18** and **0.08**,
and improved prediction on the flight held out from fitting. The supplied data
are synthetic. [Math evidence](MATH_REVIEW.md) explains assumptions and limits.

## Use the same Session API with CasADi

Open [optimize_casadi.py](../examples/optimize_casadi.py). Find:

```python
model = rum.Session().load(str(MODEL), model="Quadrotor")
export = model.to_casadi()
```

The script uses the JAX-fitted parameters, `export.rhs` and `ca.Opti()` to plan
between two hover states under thrust, torque and state constraints.

```sh
uv run --frozen python examples/optimize_casadi.py
```

Open `results/live/optimization.png`. Expect **Solve_Succeeded**, a final
position near **(4 m, 2 m)** and a separately checked finer rollout. This is a
local, open-loop trajectory solution—not a feedback controller or flight safety
certificate. If you edit the model after fitting, repeat the fit first.

**Checkpoint:** point to the same Modelica source in both exports and explain
what JAX and CasADi contribute. The compiler supplies the equations; the backend
and Python code supply differentiation, integration and optimization.

## If you finish early

Explore one [browser experiment](BROWSER_APPS.md), including the reusable-booster
landing example and the NACA visualization. Apply Rumoca to a question you care
about. Agents are optional. [Challenge rules](CHALLENGE.md): entries close at
12:40, up to five 45-second demos at 12:50, random draw if needed, audience hand
vote for the CogniPilot stocking cap. Record the tool used and elapsed work time.

The optional [FastDyn firmware demo](FASTDYN.md) has a separate Codespace.
[Custom targets](BACKENDS.md) and [Lean proofs](MATH_REVIEW.md) are take-home
extensions. They are outside the core Session → JAX → CasADi path.

If a setup or run fails, use [recovery](TROUBLESHOOTING.md), the presenters' plots
or the [browser playground](https://rumoca.cognipilot.org/playground/).
Finish by [joining the research community](COMMUNITY.md) with your model and one
result we can check together.
