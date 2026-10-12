# Make a small target; learn with the same vehicle

For terminal packaging and independent execution, see
[FMU and eFMU export](EXPORTS.md): native FMI 2/3 via FMPy, plus fixed-sample
GALEC/C99 controller export. FMI-LS-WASM is planned for Rumoca 0.11.

Rumoca separates declared physics from numerical execution. This optional
presenter demonstration uses the **same `models/Quadrotor.mo`** as the core,
then renders its checked scalar Solve program into batched PyTorch operations.
No Python vehicle equations are added.

The teaching target is in [templates/torch-ode](../templates/torch-ode).
[target.toml](../templates/torch-ode/target.toml) declares its IR, capabilities and
output file; [rhs.py.jinja](../templates/torch-ode/rhs.py.jinja) maps supported
operations to Torch. The pinned Rumoca release accepts an external target
directory through `model.codegen(path)`. See the
[official custom-target guide for 0.10.2](https://github.com/CogniPilot/rumoca/blob/v0.10.2/docs/user-guide/src/codegen/custom-targets.md).
Editing the compiler's Rust source is unnecessary for this target.

## Run in the Codespace or Linux x64

```sh
uv run --frozen --group torch python scripts/check_torch_backend.py
uv run --frozen --group torch python scripts/learn_hover_torch.py
```

The optional group pins **PyTorch 2.10.0 CPU** and adds about a 180 MiB wheel;
the core environment does not install it. This route is qualified on Linux x64,
including the two-core workshop Codespace. Mac/Windows participants can watch
the demonstration, use the Codespace or inspect the saved
[policy plot](../results/reference/torch_policy.png).

The first command creates `generated/torch-ode/Quadrotor_torch.py`. Inspect its
state/input/parameter maps and the `torch.stack` output. It checks 101 batched
RHS evaluations against JAX and CasADi, state/input/parameter Jacobians,
forward/reverse AD, central-difference `gradcheck`, batched time in a separate
time-dependent Modelica test, and explicit rejection of
unsupported operations/events. Reports go to `results/live`.

## A small bridge to reinforcement learning

The second command optimizes a feedback policy through differentiable RK4
rollouts. The vehicle stays level, uses zero torque, and learns **two positive
altitude/vertical-speed gains** to hold `z = 1 m`:

```text
T = m*g + 6 N * tanh(kp*(1 m - z)/(1 m) - kd*vz/(1 m/s))
tau = 0
```

The bounded thrust correction acts on the generated six-state plant. Training
uses 64 initial conditions for two seconds and 60 Adam updates. Evaluation uses
128 new initial conditions with a separate seed. The dimensionless objective
weights altitude error, vertical velocity and thrust correction. The reference
held-out cost falls from about **0.116 to 0.021**. The script also checks complete
rollout gradients and reintegrates with four substeps while preserving the
feedback sampling period. See [reference results](../results/reference/torch_policy.json).

This is **model-based differentiable policy optimization**, a bridge to RL;
it is not PPO, DQN or a full-flight trained vehicle. A learned simulator,
stochastic transitions, exploration, longer horizons and independent robustness
tests would make larger research projects. The direct pathwise-gradient idea
connects with [Heess et al., Learning Continuous Control Policies by Stochastic
Value Gradients, NeurIPS 2015](https://arxiv.org/abs/1510.09142); this compact
demo does not implement that paper's complete algorithm.

## Try extending the target

Pick a primitive your own model needs. The current template fails on `exp`.
Add a `Unary Exp → torch.exp` mapping, run a scalar test model, then compare
values and both AD modes with JAX/CasADi before claiming support. Add capabilities
only when their implementation and checks exist. Declaring a capability does
not implement it. Do not enable events, residual DAEs, implicit algebraics or
external functions merely to suppress a gate.

The target supports a deliberately small explicit scalar ODE subset with
batching and float64 autograd. Its capability declarations, validation receipts
and generated code are part of the example. The Lean companion applies to the
core exact-real equations; it does not certify Torch floating-point execution
or the learned policy.

## Research direction

Our aim is a unified declarative modeling and simulation environment for
cyberphysical systems. Shared compiler structure can support specialized solver
generation, batched Monte Carlo and RL, native AD or connections to JAX, CasADi
and PyTorch, and deployment across CPU, GPU and embedded hardware. Today's core
qualifies specific CPU workflows; this target demonstrates one extension seam.
The guide's browser flow demo exercises a separate experimental WebGPU path.
Automatic hardware partitioning, general solver optimization and production
RL throughput remain research questions to benchmark and validate. Array-native
IR is also important for PDE discretizations and connected vision pipelines.
Our differentiable vortex-lattice experiments target aerodynamic design:
geometry → model → objective → gradients → geometry update. An XFOIL-like
design workflow is an analogy; vortex-lattice and XFOIL airfoil/boundary-layer
models have different assumptions. The NACA flow editor is a qualitative PDE
demo, not a supplied vortex-lattice or differentiated XFOIL implementation.
For method context, see [AeroSandbox's vortex-lattice implementation](https://aerosandbox.readthedocs.io/en/master/autoapi/aerosandbox/aerodynamics/aero_3D/vortex_lattice_method/)
and [XFOIL](https://web.mit.edu/drela/Public/web/xfoil/).

## Compiler stages and target inputs

An **IR** is an intermediate representation. Rumoca 0.10.2 moves from parsed
**AST** (abstract syntax tree) through name/type resolution and instantiation
to **Flat** (expanded hierarchy and connections), then **DAE**
(differential-algebraic equations and event/clock metadata). Structural
preparation and lowering produce **Solve**: computation plans that execution
backends consume. Flat equations describe relationships; Solve specifies the
computations needed by a solver.

**GaLEC** (Guarded Algorithmic Language for Embedded Control) is a separate
projection from DAE for fixed-sample discrete control models. In this release
it requires no continuous states or `der()`. Its algorithm-code representation
supports eFMI/embedded C export. Today's continuous quadrotor takes the Solve
route. See the released [pipeline overview](https://github.com/CogniPilot/rumoca/blob/v0.10.2/docs/dev-guide/src/compiler/pipeline-overview.md)
and [GaLEC guide](https://github.com/CogniPilot/rumoca/blob/v0.10.2/docs/user-guide/src/codegen/galec-efmi.md).
The [GaLEC target manifest](https://github.com/CogniPilot/rumoca/blob/v0.10.2/crates/rumoca-phase-codegen/src/templates/galec/target.toml)
selects `ir = "algorithm-code"`: the dedicated DAE projection constructs this
checked representation before the target renders it.

## Walk through the Lean target

Slide 19 uses these actual files. Start with
[target.toml](../templates/lean-proof/target.toml): `version = 1` is the manifest
version and `ir = "solve"` selects its input representation. `[capabilities]`
declares supported features. Each `[[files]]` block names an output and its
template: `program.json.jinja` produces an inspectable Solve operation list;
`rhs.lean.jinja` produces Lean types and the exact-real RHS. This manifest
configures code generation; scenario TOML configures simulation.

Open [rhs.lean.jinja](../templates/lean-proof/rhs.lean.jinja) at `structure Control`.
With line breaks added to make the loop readable, its actual excerpt is:

```jinja
structure Control where
{% for name in solve.solve_layout.input_scalar_names %}
  {{ name }} : ℝ
{% endfor %}
```

`{% ... %}` executes template control flow; `{{ ... }}` inserts a value. Solve
supplies `T` and `tau`, so the template generates two real-valued fields:

```lean
structure Control where
  T : ℝ
  tau : ℝ
```

Farther down, `LoadY` and `LoadP` map compiler registers to the named state,
parameter and control fields. `Unary` and `Binary` render supported operations;
the final `fail(...)` rejects unsupported cases. Jinja owns the rendering of
types and equations; the Python driver invokes it and records provenance.

The shared helper in `scripts/common.py` already uses Rumoca's Python Session
API for the core JAX and CasADi examples. A minimal custom-target call is:

```python
import rumoca as rum
model = rum.Session().load("models/Quadrotor.mo", model="Quadrotor")
model.codegen("templates/lean-proof").save_all("formal")
```

The [Lean target](../templates/lean-proof/target.toml) renders fields, operations
and the exact-real RHS in [rhs.lean.jinja](../templates/lean-proof/rhs.lean.jinja).
Python only invokes the target, checks the workshop layout and records hashes.
The JSON output exposes the same checked Solve program for inspection.
The teaching target rejects unsupported operations and events; constants must
be finite integers. Extending this subset requires an exact rational rule and
new proof checks. This target and the compiler remain trusted; the Lean kernel
checks the exported equations and the 17 scoped workshop theorems.

Run `uv run --frozen python scripts/export_lean.py`, then compare
[Generated.lean](../formal/Generated.lean) with
[Workshop.lean](../formal/Workshop.lean). `generated_matches_physics` relates
the generated RHS to the displayed physics. `hover_equilibrium` proves that
level, still flight with thrust `m*g` and zero torque has zero derivatives over
exact reals. The [proof instructions and trusted boundary](MATH_REVIEW.md#what-lean-checks)
explain what is checked; use the completed CI proof log during the talk.

For a small edit, copy the target and export to a separate results folder:

```python
from pathlib import Path
import shutil
import rumoca as rum

target = Path("examples/agent_experiment/lean-proof")
shutil.copytree("templates/lean-proof", target, dirs_exist_ok=True)
template = target / "rhs.lean.jinja"
text = template.read_text()
text = text.replace("  {{ name }} : ℝ", "  -- generated field: {{ name }}\n  {{ name }} : ℝ")
template.write_text(text)
model = rum.Session().load("models/Quadrotor.mo", model="Quadrotor")
model.codegen(str(target)).save_all("results/live/lean-template")
```

Open `results/live/lean-template/Generated.lean` and find the inserted comments.
This demonstrates a Jinja edit with compiler-provided names while preserving
the checked baseline in `formal/`. It changes comments, not equations. Extending
operation support requires new mathematical and rejection checks.
