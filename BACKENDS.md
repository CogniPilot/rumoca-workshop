# Make a small target; learn with the same vehicle

Rumoca separates declared physics from numerical execution. This optional
instructor demonstration uses the **same `models/Quadrotor.mo`** as the core,
then renders its checked scalar Solve program into batched PyTorch operations.
No Python vehicle equations are added.

The teaching target is in [templates/torch-ode](templates/torch-ode).
[target.toml](templates/torch-ode/target.toml) declares its IR, capabilities and
output file; [rhs.py.jinja](templates/torch-ode/rhs.py.jinja) maps supported
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
[policy plot](results/reference/torch_policy.png).

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
feedback sampling period. See [reference results](results/reference/torch_policy.json).

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
RL throughput remain research questions to benchmark and validate.
