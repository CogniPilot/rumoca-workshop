# Mathematical review and proof scope

## Optional Torch and user-guide demonstrations

The external Torch target renders the checked scalar Solve operations of the
same Modelica vehicle. Its [backend checks](results/reference/torch_backend.json)
compare 101 batched evaluations with JAX/CasADi, forward/reverse Jacobians and
central-difference gradients, including zero velocity. Unsupported operations
and events fail explicitly. This validates the teaching target for this model,
not the whole Modelica language or arbitrary Torch programs.

The [small hover policy](results/reference/torch_policy.json) uses two positive
gains, zero torque, fixed known drag and 50 ms sampled feedback. Its dimensionless
objective weights squared altitude error scaled by 1 m, vertical speed scaled
by 1 m/s and thrust correction scaled by 6 N. Training and held-out initial
conditions have distinct fixed seeds; the script checks complete policy-loss
gradients and four-substep reintegration with the same feedback sampling period.
The exact-real `vertical_subspace_tangent` theorem states that horizontal and
pitch derivatives vanish at the restricted task's states and controls; it is
pointwise tangency, not an ODE-solution or floating-point invariance theorem.
[Heess et al., NeurIPS 2015](https://arxiv.org/abs/1510.09142) gives primary context
for pathwise model/policy gradients. The demo is direct differentiable policy
optimization; it does not implement their complete stochastic value-gradient
algorithm or a model-free RL method.

The deployed guide's NACA example uses artificial compressibility and a smooth
solid penalization on a coarse grid. Primary method context:
[Chorin's 1967 paper](https://math.berkeley.edu/~chorin/chorin67.pdf) and
[Angot, Bruneau and Fabrie, 1999](https://www.math.u-bordeaux.fr/~chabrune/publi/ABF-NM.pdf).
Those papers do not certify the guide's particular discretization or parameter
choices. The [guide receipt](verification/user-guide.json) checks editor changes,
a two-second WebGPU simulation and display controls only. It provides no
lift/drag validation, convergence study, stability proof or hardware speedup
benchmark. The guide uses a separate deployed browser compiler/runtime.

This is a reproducible engineering teaching example for Purdue’s School of
Aeronautics and Astronautics at Georgia Tech. Its exact-real invariants are
checked in Lean; numerical claims have separate executable checks. Neither
constitutes certification of real flight, all of Rumoca, or arbitrary edits.

## Equations, signs and dimensions

Let `s=(x,z,θ,vx,vz,ω)` with world `x` right and `z` up. Positive rotation about
the out-of-plane `+y` axis tilts thrust toward `+x`. The source declares

```text
ẋ = vx                         ż = vz                    θ̇ = ω
m v̇x = T sin θ + D(vx)
m v̇z = T cos θ − m g + D(vz)
Iyy ω̇ = τ − d ω
D(v) = −kl v − kq sqrt(v² + ε²) v
```

| Quantity | Value / units | Assumption |
|---|---|---|
| m | 1.2 kg | Positive, known |
| Iyy | 0.025 kg m² | Positive, known |
| g | 9.81 m/s² | Positive, known; downward acceleration |
| kl | 0.18 N s/m | Nonnegative fitted drag |
| kq | 0 initially; synthetic truth 0.08 N s²/m² | Nonnegative fitted drag |
| d | 0.04 N m s/rad | Nonnegative known pitch damping |
| ε | 0.01 m/s | Positive speed regularization |
| T, τ | N, N m | Aggregate ideal force and torque inputs |

`kl*v` and `kq*sqrt(v²+ε²)*v` both have force units. Divide forces by mass,
torques by inertia. Radians are dimensionless in SI; their annotations clarify
angle versus translation. Position is centre-of-mass position. No body/world
frame transformation is silently applied to drag: it is explicitly componentwise
in world axes. At nonzero pitch the law differs from body-axis rotor drag and
from isotropic vector quadratic drag `−kq ||v|| v`.

For `kl,kq≥0`, drag is odd, zero at rest and dissipative:
`v D(v)=−kl v²−kq sqrt(v²+ε²) v²≤0`. With `ε>0`, the square-root argument is
strictly positive, and drag is differentiable at every real velocity. Also
`0≤sqrt(v²+ε²)−|v|≤ε`, so smoothing changes the force by at most
`kq ε |v|`. Near zero it adds a small linear slope `kq ε`; the fitted linear
coefficient is interpreted **with ε fixed**, not independently of regularization.

The thrust vector has norm `|T|`. Level zero-speed/rate flight with `T=mg`,
`τ=0` is an equilibrium at any `(x,z)`. For
`E=m(vx²+vz²)/2+mgz+Iyy ω²/2`, its instantaneous chain-rule rate is

```text
Ė = T(vx sin θ + vz cos θ) + τ ω + vx D(vx) + vz D(vz) − d ω².
```

With controls zero it is nonpositive. This is a balance of mechanical energy;
potential energy need not be positive for arbitrary `z`. The theorem checks
the algebraic directional derivative `energyRate`, assuming nonzero mass and
inertia. It does not prove existence of a trajectory or apply a continuous-time
stability theorem to the discretized solver.

The illustrative rotor-pair allocation is
`FL=(T+τ/l)/2`, `FR=(T−τ/l)/2`, `l=0.2 m`. It reconstructs
`T=FL+FR`, `τ=l(FL−FR)` and enforces `0≤FL,FR≤10 N`. Rotor lag, saturation
dynamics, allocation among four individual rotors and actuator bandwidth are
omitted. Aircraft parameters are representative teaching values, not a
calibrated Purdue platform.

## What Lean checks

[formal/Generated.lean](formal/Generated.lean) is generated by
[scripts/export_lean.py](scripts/export_lean.py) from the actual checked Rumoca
scalar **Solve RHS program**, recorded in
[formal/solve_program.json](formal/solve_program.json). It is not a separately
typed copy of the desired equations. The narrow project-owned translator
accepts only the scalar operations used here and rejects unknown operations.
Source, program and output hashes are in [formal/provenance.json](formal/provenance.json).

[formal/Workshop.lean](formal/Workshop.lean) proves:

| Theorem | Meaning |
|---|---|
| generated_matches_physics | Exported RHS equals the displayed force/torque equations |
| drag_zero, drag_odd, drag_power | Exact drag algebra and signs |
| drag_dissipative | Nonnegative drag coefficients do not inject energy |
| smooth_magnitude_positive, drag_differentiable | Positive ε removes the singularity |
| smooth_magnitude_error_bound | Regularization magnitude error ≤ε |
| thrust_projection_norm, hover_equilibrium | Thrust projection and hover signs |
| mechanical_energy_balance, unforced_energy_dissipative | Instantaneous power balance |
| normalized_drag, two_speed_coefficients_unique | Ideal force observations at distinct speed magnitudes separate kl/kq |
| rotor_allocation | Algebraic force/torque reconstruction |
| log_parameters_positive | Exponential fit parameterization is positive |

The coefficient uniqueness theorem is deliberately narrow: for nonzero ideal
force observations, `−D(v)/v=kl+kq sqrt(v²+ε²)`. Two **distinct magnitudes**
produce independent regression rows. Merely changing velocity sign at the
same magnitude does not supply a second independent row. This algebra is not
a structural-identifiability proof for partially observed noisy trajectories
with unknown initial conditions or unknown mass.

Lean **4.29.1** and Mathlib commit
`5e932f97dd25535344f80f9dd8da3aab83df0fe6` (public v4.29.1) are pinned. There are no `sorry`,
`admit`, custom axioms or `native_decide` in the proof files. Printed assumption
audit: [verification/lean-check.txt](verification/lean-check.txt); only standard
Lean axioms `propext`, `Classical.choice`, `Quot.sound`. CI regenerates the actual
export, checks it against the committed files, builds the proofs, rechecks proof
terms with `leanchecker`, and rejects admissions.

To reproduce (instructor only; Mathlib downloads are substantial):

```sh
uv run --frozen python scripts/export_lean.py
cd formal
lake update
lake exe cache get Generated.lean Workshop.lean
lake build
lake env leanchecker Generated Workshop
lake env lean Workshop.lean
```

Install [elan](https://github.com/leanprover/elan) to obtain the pinned toolchain.
For substantial proof downloads, store `.lake` under
`$HOME/scratch/rumoca-workshop/` and link it into `formal/`.
CI follows this storage convention. Participants do not need Lean.

**Trusted boundary:** the compiler, JSON template, Python-to-Lean translator,
real interpretation of operations, Lean/Mathlib and kernel remain trusted.
No theorem covers floating-point code generation, browser integrators,
discrete-time integration error, statistical recovery, all-time constraint
feasibility, global NLP optimality or deployment safety. Proven equality and
independent numerical comparisons reduce risk without erasing this boundary.

## Identification and numerical checks

The objective is `L(a)=mean[((prediction−measurement)/σ)²]` over position and
velocity components on three training flights. Dimensionless log parameters
mean `kl/(1 N s/m)=exp(a₁)` and `kq/(1 N s²/m²)=exp(a₂)`; scripts store the
numerical SI magnitudes of the physical coefficients. Lean operates on those
real magnitudes, not a type system for physical dimensions.
Parameters are bounded to `[0.001,2]` in their respective native units; zero
drag is outside that fitting range. `σ` is the known synthetic measurement
standard deviation of each observed component. Gaussian, independent noise,
exact commands, exact initial state and known remaining parameters are teaching
assumptions. Angular observations after the initial sample do not enter the loss.

JAX differentiates the **discretized RK4 rollout** (`dt=0.05 s`), not an exact
continuous-time solution. Dataset generation uses CasADi RHS + SciPy DOP853
at `rtol=1e−11`, `atol=1e−12` with commands held constant per interval. The
held-out flight is not used by the optimizer or sensitivity calculation. The
instructor truth file is used for reporting, not computing the fit objective.

[scripts/math_audit.py](scripts/math_audit.py) independently checks:

- Analytic linear-drag level coasting versus generated JAX integration;
  maximum position error approximately `3.9e−10 m` in the reference run.
- JAX/CasADi state and parameter Jacobian agreement at zero, near-zero,
  positive and negative velocities; error approximately `2.8e−14`.
- Central finite differences of the full objective against JAX gradients.
- Six widely separated initial guesses and twelve independent measurement
  noise seeds. These are finite robustness tests, not probabilistic guarantees.
- Parameter profiles that **re-optimize the other coefficient** at each grid
  point; both sides cross the nominal `Δχ²=3.841` threshold in the tested grid.

The profile uses **sum** of squared standardized residuals (`χ²`), whereas the
participant loss uses their mean. Their ratio is the number of residuals
(1920). The 95% threshold is asymptotic and conditional on the Gaussian model;
finite-grid crossings do not certify interval coverage. A sensitivity condition
number alone would not establish practical identifiability. We therefore show
profiles and multi-start evidence alongside it, without publishing guaranteed
confidence intervals.

`rms_by_state` reports each physical unit separately; `noise_scaled_rms` is
dimensionless. Legacy `rms` combines metres and metres/second and is retained
as a backward-compatible report field, not a physically homogeneous error norm.
The console and holdout acceptance check use the dimensionless noise-scaled
RMS; fine-rollout terminal checks identify each state's physical unit.

## Optimal-control transcription

Six seconds, 60 intervals, `dt=0.1 s`; states and controls are decision variables.
Continuity constraints are `X[k+1]=RK4(f,X[k],U[k],p)`. Initial and final full
states are constrained to hover; thrust and torque are held constant per interval.
IPOPT solves a **local NLP**, with a saved successful primal solution as the
default warm start. It is neither a global optimizer nor proof of an optimum
for the continuous-time problem.

Let `ex,ez` be position errors scaled by 1 m, velocities by 1 m/s, pitch by 1 rad,
`aT=(T−mg)/(10 N)`, `aτ=τ/(0.35 N m)`, `h=dt/(1 s)`. The dimensionless cost is

```text
Σ h [0.3(ex²+ez²) + 0.03(vx_scaled²+vz_scaled²)
     + 2 aT² + 0.3675 aτ² + 0.02 θ_scaled²]
+ Σ_{k>0} [0.5(ΔT/(10 N))² + 0.0006125(Δτ/(0.35 N m))²].
```

The smoothness sum is an explicit discrete control-change penalty, not an
approximation of a continuous derivative penalty. The objective minimizes a
tracking/effort tradeoff, not electrical energy or minimum time. Bound checks
allow `1e−6` numerical solver tolerance. The physical pitch bound is 0.55 rad;
node bound 0.54 leaves a margin. Node feasibility alone was insufficient, so
we validate a four-times finer RK4 rollout and independent DOP853 integration.
The audit analytically locates pitch extrema within each constant-torque
interval using the linear angular ODE, anchored to numerical initial states.
Altitude is sampled densely; there is no interval-arithmetic all-time certificate.
Independent terminal errors are reported **per state**, about 0.3 mm horizontal
and 2.1 mm altitude in the reference case. These checks apply to the rehearsed
input trajectory; arbitrary target edits require new validation.

## Primary literature: what we adopted and what we did not

1. **Faessler, Franchi & Scaramuzza (2018)**,
   [*Differential Flatness of Quadrotor Dynamics Subject to Rotor Drag for Accurate Tracking of High-Speed Trajectories*](https://arxiv.org/html/1712.02402),
   IEEE RA-L 3(2), 620–626, DOI [10.1109/LRA.2017.2776353](https://doi.org/10.1109/LRA.2017.2776353).
   Checked equations (1)–(4) and identification/validation discussion. Supports
   downward gravity, thrust along body vertical, drag-aware modeling and
   exciting velocity regimes. Their linear rotor drag is body-frame and
   mass-normalized (`R D Rᵀ v`); our force coefficients divide by mass and our
   componentwise world-axis quadratic term is a pedagogical assumption.
   We do not invoke their flatness theorem or claim their experimental fidelity.
2. **Andersson, Gillis, Horn, Rawlings & Diehl (2019)**,
   [*CasADi: a software framework for nonlinear optimization and optimal control*](https://cdn.syscop.de/publications/Andersson2019.pdf),
   Mathematical Programming Computation 11, 1–36,
   DOI [10.1007/s12532-018-0139-4](https://doi.org/10.1007/s12532-018-0139-4).
   Checked sections 2.6 and 5.4: expression-graph AD, constant-input intervals,
   independent state variables and continuity constraints. Our small explicit
   ODE uses RK4 and Opti/IPOPT rather than their example’s DAE/IDAS/blockSQP.
3. **Raue et al. (2009)**,
   [*Structural and practical identifiability analysis … exploiting the profile likelihood*](https://pubmed.ncbi.nlm.nih.gov/19505944/),
   Bioinformatics 25(15), 1923–1929, DOI
   [10.1093/bioinformatics/btp358](https://doi.org/10.1093/bioinformatics/btp358).
   Primary abstract establishes the role of profiles and experimental design.
   Detailed method was also checked against **Wieland et al. (2021)**,
   [*On structural and practical identifiability*](https://arxiv.org/pdf/2102.05100),
   especially equation (6): fix one parameter, re-optimize the rest. This
   informed the added profiles and the limits placed on SVD-based claims.

Literature checks guide the approach; they are not a substitute for testing this
implementation. The stored [numerical audit](results/reference/math_audit.json),
[plot](results/reference/math_audit.png) and [verification report](VERIFICATION.md)
are evidence for the specific workshop instance.

## Mathematical context for the opening slides

The broader research motivation uses several distinct kinds of analysis:

- **Lie group theory:** [Solà, Deray & Atchuthan, *A micro Lie theory for state estimation in robotics*](https://arxiv.org/abs/1812.01537)
  describes geometric representations, local perturbations and Jacobians used
  in robotics estimation. The [CogniPilot model library](https://github.com/CogniPilot/modelica_models)
  contains Lie-group, estimation and control building blocks. Today's planar
  model does not exercise the full six-degree-of-freedom Lie-group workflow.
- **Reachable sets:** [Althoff, Frehse & Girard, *Set Propagation Techniques for Reachability Analysis* (2021)](https://doi.org/10.1146/annurev-control-071420-081941)
  surveys computation of guaranteed overapproximations under stated assumptions.
  A nominal trajectory and sampled numerical checks do not constitute such an
  enclosure. Today's workshop computes no reachable tube.
- **Formal software verification:** the Lean companion checks selected exact-real
  equations and invariants, with the trusted boundaries stated above. It does
  not prove floating-point execution, compiler correctness or generated machine code.
- **Identification and digital twins:** fitting physical parameters connects a
  model to observations. Today's observations are synthetic; real-system twin
  validation requires separate measurements and checks.

## Scope of the optional browser app experiments

The [app gallery](BROWSER_APPS.md) uses different fixed-wing and inertial models,
release versions and datasets. Public UI rehearsal confirms the documented
interactions execute. It does not transfer these planar-model Lean theorems,
coefficient-recovery results or trajectory constraint checks to those apps.
Motion-capture benchmark metrics are displayed as upstream stored results;
we did not regenerate or independently validate them. Full visual-SLAM coupling
remains development work. An agent’s role in building an app is development
provenance, not mathematical evidence.
