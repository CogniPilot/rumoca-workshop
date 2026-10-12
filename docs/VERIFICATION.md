# Verification and remaining preflight

Qualification performed October 11–12, 2026 (UTC). Evidence is committed in
`verification/` and `results/reference/`. Scope is this small
smooth ODE and its stated parameters, not arbitrary Modelica or real flight.

## Reproducibility and measured CPU time

[Clean CI run 38189451071](https://github.com/CogniPilot/rumoca_workshop_amc2026/actions/runs/38189451071)
at commit `5c59bd3` passed all **seven** jobs: four Python OS runners,
full devcontainer configuration, features and startup commands, pinned-flake CPU/Torch checks, and
generated-equation Lean proof checking.
The machine-readable [job receipt](../verification/ci-jobs.json) and
[platform reports](../verification/platforms) record exact platforms and results.
The receipt records the exact tested commit and job URLs. Subsequent receipt
and documentation updates do not change the qualified model or numerical code.

Times below are **command wall time after dependency setup**, including imports,
JAX compilation and plotting. They are not network installation or fresh
Codespaces startup measurements. First Matplotlib font-cache creation can
dominate the first simulation.

| Tested environment | Simulate | JAX fit | CasADi optimize | Full smoke |
|---|---:|---:|---:|---:|
| Local Linux x64, Ryzen 9 5950X, Python 3.12.13 | 1.4 s | 5.9 s | 1.7 s | 11.7 s |
| Ubuntu hosted x64 | 2.6 s | 6.3 s | 1.6 s | 14.4 s |
| Windows Server 2025 hosted x64 | 5.4 s | 7.0 s | 1.6 s | 19.2 s |
| macOS 26.6.2 hosted Apple Silicon | 14.8 s | 3.9 s | 1.0 s | 23.3 s |
| macOS 15.7.9 hosted Intel | 31.7 s | 12.5 s | 6.1 s | 60.0 s |
| Debian devcontainer, non-root vscode user | 2.1 s | 5.6 s | 1.4 s | 12.4 s |
| Actual two-core Codespace, Python 3.12.11 | 2.8 s | 12.6 s | 3.0 s | 24.6 s |

Each of the three examples finishes under the one-minute acceptance target on
these runs. Local NixOS supplies system libraries through a machine-specific
environment; participant instructions use ordinary native `uv`, as exercised
in clean CI. Frozen Python 3.12 dependencies: Rumoca 0.10.2, JAX 0.4.38,
CasADi 3.7.2, NumPy 2.2.6, SciPy 1.15.3, Matplotlib 3.10.3; uv 0.11.21 in CI.
No GPU/CUDA or attendee compiler installation is needed.

Linux ARM64 wheel URLs are pinned but not executed in this matrix. macOS ≥14,
glibc ≥2.28 Linux x64, and Windows x64 are supported wheel assumptions; CI
qualifies the exact versions above, not every older OS build.

The simplified Session examples and `import rumoca as rum` were subsequently
refreshed at `299ec0f` in the actual core Codespace: all three commands, numerical
smoke checks and material provenance passed in **17.7 seconds** for the smoke
run. [Codespace receipt](../verification/codespace.json) separates this source
refresh from the fresh container rebuild and original deeper audit.

## Model, fit and trajectory

Canonical SHA256:
`3864d44035bd894931586749afc60c33a4190e6810b3b81b69fde9c52fddb56a`.
All three scripts compile the same file and record that hash; optimization
rejects a fit from a different source. CSV SHA256 is recorded in fit reports.
No backend substitutes handwritten vehicle dynamics.

- Both emitted RHS functions agree at 20 smoke-test states. Hover is an
  equilibrium; JAX rollout gradient agrees with central differences.
- Synthetic CSV: 644 samples / four flights; CasADi RHS + independent DOP853
  generation, fixed seed 20261012, exact initial states, independent Gaussian
  noise, separate held-out flight. No private/real flight logs.
- Joint JAX estimate: `kl≈0.1804156`, `kq≈0.0799076`; truth 0.18/0.08.
  Noise-scaled mean squared loss 26,931.78→1.073, about 25,100× reduction.
  Local sensitivity condition 10.87. Per-state and standardized errors are
  available; legacy mixed-unit RMS is not interpreted as metres.
- Default IPOPT result: `Solve_Succeeded`, dimensionless cost about 5.118;
  max dynamics defect about `1.7e−14`; exact terminal-node constraints.
  Reintegrated altitude error about 2.1 mm. Physical bounds include rotor-pair
  realizability, pitch-node margin and sampled/finer checks.
- [Independent audit](../results/reference/math_audit.json): analytic linear-drag
  coasting, JAX/CasADi Jacobians including zero-speed regimes, full-objective
  finite-difference checks, six starting guesses, twelve noise seeds and
  re-optimized profiles. Maximum noise-seed relative coefficient error about
  **0.39%**. Adaptive integration plus analytic interval pitch extrema gives
  peak approximately **0.54164 rad**, below the 0.55 physical limit.

One-coefficient recovery was executed successfully: quadratic ≈0.08001 with
known linear 0.18; [receipt](../verification/recovery-fit_drag.json). Target x=3
variant also solved with no stored warm start; fine terminal error ≈1.6 mm,
and it is independently audited in `verification/target3-math_audit.json`.
These optional results apply to the rehearsed variants, not arbitrary targets.
Both raw code-generation targets `jax-ode` and `casadi-ode` were executed.

## Lean and primary literature

Lean 4.29.1 + public Mathlib v4.29.1, exact commit
`5e932f97dd25535344f80f9dd8da3aab83df0fe6`. Clean CI regenerated the actual
Solve→Lean representation without a diff, built the proofs, rechecked terms
with **leanchecker**, and rejected admissions/custom axioms. The assumption
log is [verification/lean-ci.txt](../verification/lean-ci.txt). Exact theorem
statements, trusted boundary, dimensional review and checked primary papers:
[MATH_REVIEW.md](MATH_REVIEW.md).

Seventeen exact-real theorems are checked. Proven: RHS/displayed-equation equality; drag signs/dissipation; smoothness and
regularization bound; hover; power balance; ideal two-speed excitation algebra;
rotor allocation; positive parameterization; pointwise tangency of the vertical
policy subspace. Not proven: compiler/translator
correctness, floating-point behavior, integration error bounds, noisy-data
identifiability, global optimum, all-time state constraints or safe flight.

## Browser and editor

The actual public [playground](https://rumoca.cognipilot.org/playground/) was
tested in Chromium, with the complete browser bundle, visible gear/settings
model selector, **BrowserFlight** selected, and Play at quadratic values 0 and
0.08. Both compiled balanced and produced **501 points, 8 variables** and a
plot. Browser-reported simulation times approximately 48 ms and 10 ms;
automation waited longer for rendering. Runtime **0.8.13**, distinct from the
Python release. Intentional syntax errors produced browser LSP markers.
Evidence: [browser.json](../verification/browser.json), actual screenshots in
`slides/assets/`, reproducible [UI test](../verification/browser-proof.mjs).

The released **0.10.2** VSIX was installed in isolated real **VS Code 1.119.0**
extension hosts on **Linux x64, Windows x64, macOS ARM64 and macOS x64**.
Verified activation, no errors on the canonical model, `sin` completion,
parameter hover, errors on intentionally invalid syntax, and clean diagnostics
after restoring valid source. CI checks the exact version and
[release VSIX hashes](../verification/vsix-sha256.json) before qualification.
[Editor CI run](https://github.com/CogniPilot/rumoca_workshop_amc2026/actions/runs/38189450891)
passed all four jobs. Receipts: [verification/editors](../verification/editors),
local [vscode-linux.json](../verification/vscode-linux.json), actual
`vscode-quadrotor.png`, and test source in `verification/`.

The same released extension passed from a **native VS Code workspace extension
host inside an actual two-core GitHub Codespace**. Desktop VS Code connected
over Remote SSH; the remote test ran the same activation, hover, completion,
broken-syntax and restoration checks. [Cloud editor receipt](../verification/codespace-editor.json).
Startup also installed the pinned, hash-checked VSIX in Codespaces' normal
remote extension directory and confirmed the second invocation was idempotent.
The latest full rebuild also installed **PDF Viewer**, **Lean 4**, **Jinja** and
**Markdown preview styles** before editor attachment; [extension receipt](../verification/codespace-extensions.json).
The Lean extension supplies editor support; toolchain/Mathlib setup remains
optional and separate from the CI proof qualification.

**Not qualified:** browser-native Python and GitHub's browser frontend.
The editor test is independent of Python CI; exact release/platform
qualification does not guarantee every older OS/editor build.

## Optional target, policy and embedded guide

The [custom Torch target](BACKENDS.md) passed 101-point batched RHS parity,
state/input/parameter Jacobians against JAX/CasADi, forward/reverse AD,
finite-difference gradcheck and unsupported-feature rejection. The small vertical
policy's held-out cost improved **0.1156→0.0210** on 128 new initial conditions;
complete rollout gradients and fixed-sampling fine integration passed.
[Backend receipt](../results/reference/torch_backend.json),
[policy receipt](../results/reference/torch_policy.json). Both commands also passed
in the actual two-core Codespace: about **11 s** and **14 s** after package setup.
This is a restricted differentiable policy-learning task with known parameters,
not a full-flight or model-free RL qualification. The optional CPU package is
qualified on Linux x64 only and is excluded from the base install.

The deployed [user guide](https://cognipilot.github.io/rumoca/user-guide/) embeds
editors and simulations. Its NACA flow example passed an edit from 30 to 2 s,
default-grid WebGPU simulation, final-frame selection and Pressure/Vorticity
switching in Chromium with a **software** adapter. About **21 s** total UI time;
reported integration about **6.6 s**. [Receipt](../verification/user-guide.json),
[test](../verification/user-guide-proof.mjs),
[capture](../slides/assets/user-guide-naca.png). This is an experimental coarse
artificial-compressibility/penalization visualization, not a CFD accuracy or
hardware-throughput test. The guide runs a separate deployed compiler/runtime.

The pinned **NixOS 26.05** flake evaluated all four declared systems and ran the
CPU core, audit and Torch commands successfully on Linux. CI also uses its
container-build app with the tested Debian Dockerfile. Participants use uv or
Codespaces; the flake is a maintainer tool. Mac qualification uses ordinary uv;
Darwin flake evaluation alone does not establish runtime support.

## Optional agent-built app gallery

[BROWSER_APPS.md](BROWSER_APPS.md) provides a five-minute segment led by fixed-wing;
SLAM is another example in development.
The public Chromium UI rehearsal passed for all three linked applications:

- `rumoca_fixed_wing`: compiled the default Modelica controller and plant,
  observed waypoint/time progress at 50 Hz, selected 20 Hz, **restarted to
  compile at the new rate**, observed progress again and paused; about 14 s
  for the whole test. [Receipt](../verification/app-rumoca_fixed_wing.json).
  A [fresh-checkout rehearsal](../verification/app-starter.json) also reproduced
  the source at `3b972ccb1d5f795771ca9132f9a7e3d00d802145`, installed its pinned
  npm dependencies, passed the upstream static check, and ran the same 50/20 Hz
  interaction locally in about 13 s. This does not qualify new comparison features.
- `slam_web`: ran and paused `InertialOnly`, selected `ResponsiveInertial`,
  ran and paused again; simulated time advanced in both. Software WebGL warning
  and lightweight preview were visible; about 25 s. [Receipt](../verification/app-slam_web.json).
- `mocap_sysid`: selected synthetic open-loop data, opened Time Histories,
  Data Splits and Models, then selected LinearSS; about 6 s.
  [Receipt](../verification/app-mocap_sysid.json).

WASM requests returned HTTP 200 for fixed-wing and SLAM Lab. The tested mocap
viewer path displays stored results and does not invoke WASM. No page errors
occurred on the successful rehearsals. Actual screenshots are in
`slides/assets/app-*.png`; [test](../verification/apps-proof.mjs).
These are UI execution checks, not independent validation of benchmark metrics,
visual-SLAM completion, real flight or the applications’ complete mathematics.
The workshop’s planar-model Lean proofs do not cover these different models.
Agents helped build the apps, as described by the presenters; engineering
review and validation remain necessary.

## Qualified package artifacts

The workshop macOS wheels use the operating system's libiconv load reference.
The maintainer packaging script updates that reference, signature and wheel
RECORD without altering compiler code. Both artifacts passed qualification and
are selected by frozen hashes; participants use the ordinary uv commands.
[Qualification run](https://github.com/CogniPilot/rumoca_workshop_amc2026/actions/runs/38169067520),
[provenance](../verification/wheels), [notice](NOTICE.md).

The container CI now uses Dev Container CLI 0.87.0 from the pinned flake to
exercise `devcontainer.json`, SSH feature installation, workspace ownership and
the actual lifecycle command as `vscode`, followed by the numerical audit.
This covers the configured local container; the Codespaces extension installer
needs GitHub's staged VS Code Server and is qualified by the separate actual
cloud rehearsal. Formal CI pins the public Mathlib release and checks the
generated proof terms from a clean environment.

## Presentation and external limits

The deck has 30 main slides, no appendices, a contiguous **180-minute** schedule
and **two ten-minute breaks**. One editable Markdown source builds both PPTX
with speaker notes and PDF. Presenter credits name **James Goppert and Micah
Condie**. The design uses Purdue gold with deep navy, a light background for
technical figures, and teal/blue/terracotta accents for the three core phases.
The opening explains why Rumoca and the broader Lie-group, reachability,
formal-verification, identification and digital-twin context. A dedicated PURT
pylon-racing slide links the competition site and its next event's planned
Rumoca use; it does not repeat old event dates. All 30 PDF pages were rendered; revised layouts were visually reviewed;
commands, QR, screenshots and reference plots are real. Presenter text uses
large type; small evidence plots/screenshots are backups for live zoomable demos.
The PDF embeds fonts. Inspect the PPTX in the actual presentation application
for font substitution/projector differences before class.

The editable PPTX was also rendered by **LibreOffice Impress 26.2.1.2** on Linux.
All 30 pages retained every authored text item, with extracted text inside page
bounds. [Presentation receipt](../verification/presentation.json) records the
artifact hash and scope. This adds an office-renderer check to the PDF review;
the actual presentation laptop and projector remain preflight items.

An actual two-core Codespace built the devcontainer and passed the core, audit,
optional Torch and native remote-LSP checks. The [cloud receipt](../verification/codespace.json)
records source/configuration hashes and results. Account quotas, prebuild readiness,
region availability and simultaneous class capacity are not established by
that individual rehearsal. Venue Wi-Fi and the presentation laptop/projector are preflight
items. Browser, qualified local uv and reference plots provide alternate paths;
[PUBLICATION.md](PUBLICATION.md) covers cloud access.

Public upstream research is cited separately from workshop executions; future
work is labeled. The optional challenge is announced at the opening, uses an
open theme: apply Rumoca to a problem the participant cares about during
downtime. Entries document the tool used and elapsed work time. Public hosting and
coding agents are optional. Up to five 45-second experiment demos are selected by a readiness check and, if needed,
random draw, followed by an audience hand vote. The Artemis/Three.js idea is
only an [example prompt](APP_PROMPT.md); no rocket app/model was added.
[PRESENTERS.md](../slides/PRESENTERS.md) contains presentation and facilitation checks.

The separate FastDyn/QEMU environment is optional and does not alter the core
container's numerical dependencies. The three-flight workshop campaign passed in an actual two-core Codespace;
all three flights reached the final mission item and confirmed landing.
[Execution receipt](../verification/fastdyn-codespace.json) and
[trajectory plot](../slides/assets/fastdyn-trajectories.png) retain the results.
Do not infer Codespace readiness from upstream CI alone. See [FASTDYN.md](FASTDYN.md).

## Optional agent tooling

The actual configured Linux x64 and ARM64 containers passed fresh CI builds,
startup, CLI version/help checks and a detached tmux-session check. Codex 0.162.1,
Claude Code 2.1.296, Copilot CLI 1.0.95, Node 22, npm and GitHub CLI were installed automatically.
Receipts: [x64](../verification/agent-tools-ci-x86_64.json) and
[ARM64](../verification/agent-tools-ci-aarch64.json). This verifies installation
and startup, not authenticated model execution; participants use their own
accounts. The four native desktop editor qualifications also passed.

The [quadrotor guide rehearsal](../verification/quadrotor-guide.json) covers
its actual scenario/scene sources, browser start, rendering, keyboard arming
and stop. Slides 7–10 use that example for TOML and Three.js configuration;
the planar Session API exercise remains separate. The new frame-conversion
explanation was checked by exact matrix multiplication. The [settings
walkthrough](SIMULATION_SETUP.md) links the primary files.

The [prebuilt-image Codespace check](../verification/codespace-prebuilt.json)
confirms Rumoca **0.10.2**, the full core numerical workflow, all three terminal
agents, the requested editor extensions and the native LSP executable in an
actual two-core cloud environment. Its core test took **19.59 seconds** after
setup. Initial VM allocation and the approximately 2 GB image pull take
additional time; there is no shared Codespaces snapshot prebuild. This receipt
distinguishes installed extensions from separately qualified editor behavior.
