# Export a simulation FMU or an embedded-controller eFMU

These terminal demonstrations use Rumoca **0.10.2**, the workshop's existing
[quadrotor plant](../models/Quadrotor.mo) and a small
[fixed-sample controller](../extras/exports/HoverController.mo). The core
exercises remain simulate → identify → optimize. Export is an optional target
demonstration; use the Linux Codespace or local Dev Container on Mac/Windows.

| Package | Purpose | Who advances it? |
|---|---|---|
| FMI `.fmu`, Model Exchange | Exchange a dynamic model with a simulation tool | The importing tool integrates the derivatives |
| FMI `.fmu`, Co-Simulation | Exchange a model with its integration implementation | The FMU advances between communication points |
| eFMI `.efmu` | Deliver embedded algorithm/code representations and their manifests | The application schedules the generated controller's `DoStep` |

These are distinct formats. An eFMU is not an FMI simulation FMU and is not
loaded by FMPy. [FMI](https://fmi-standard.org/) and
[eFMI](https://efmi-standard.org/) describe their respective standards.

## Ready the command line

The updated container installs `rumoca` on `PATH`, plus a C compiler. Python
dependencies include **FMPy 0.3.30** and CMake. Check:

```sh
rumoca --version
uv run --frozen fmpy --version
cc --version
```

For an existing Linux environment that predates this update, install the
checksum-pinned CLI without rebuilding the workspace:

```sh
uv sync --frozen
uv run --frozen python scripts/install_rumoca_cli.py
export PATH="$HOME/.local/bin:$PATH"
```

The installer supports Linux x64/ARM64. On Debian/Ubuntu outside the prepared
container, install `build-essential` if a C compiler is missing. Participants
do not need Rust or Nix. The 0.10.2 **Python wheel lacks the `fmi` build feature**:
use the released CLI for FMU packaging. The independent reference still uses
`rum.Session().load(...).to_jax()` from the same Modelica source.

## FMU: export, compile, import with FMPy

```sh
rumoca compile models/Quadrotor.mo --model Quadrotor \
  --target fmi3 -o results/live/fmi
uv run --frozen fmpy validate results/live/fmi/Quadrotor.fmu
uv run --frozen fmpy compile results/live/fmi/Quadrotor.fmu
uv run --frozen python examples/run_fmu.py results/live/fmi/Quadrotor.fmu
```

The first command writes a **source-code FMU** and the unpacked
`results/live/fmi/Quadrotor/` directory. Open `modelDescription.xml` and
`sources/buildDescription.xml`: the package describes its variables,
capabilities and C translation units. FMPy's compile command builds the native
shared library and adds it under `binaries/<platform>/` in the `.fmu` archive.
The binary is platform-specific; source can be rebuilt on another platform.
Changing Modelica requires exporting and compiling again.

[run_fmu.py](../examples/run_fmu.py) uses an independent Python FMI importer:

```python
from fmpy import simulate_fmu

trace = simulate_fmu(
    "results/live/fmi/Quadrotor.fmu",
    fmi_type="CoSimulation",
    stop_time=2.0,
    output_interval=0.02,
    start_values={"T": 11.772, "tau": 0.0, "vx": 6.0, "k_quad": 0.0},
    output=["x", "z", "theta", "vx", "vz", "omega"],
)
```

Those thrust/start values use the canonical 1.2 kg plant. The runnable script
derives hover thrust from the actual model parameters. It checks hover,
analytic linear coast, nonlinear drag and coupled pitch excitation, comparing
**all six states** with Rumoca's Session-generated JAX dynamics. On Linux x64
it tests both Model Exchange and Co-Simulation; the ARM64 route uses
Co-Simulation because FMPy's bundled Linux CVode library is x64.
For FMI 3 on ARM64, the script uses FMPy's public pre-instantiation API
with the native `aarch64-linux` library; this avoids FMPy 0.3.30's x86-only
archive-platform detection while retaining XML, ABI and numerical checks. Open
`results/live/fmi3/fmu.png`, `fmu.json` and the CSVs after running.

Use `--target fmi2` for an FMI 2 package; the same FMPy workflow applies.
The default example checks an event-free ODE; it does not establish support
for every model or FMI capability. Rumoca 0.10.2 records the time unit in FMU
metadata but omits other unit annotations: use the explicit Modelica SI
contract (`T`: N, `tau`: N m, positions: m, angles: rad).

**FMI-LS-WASM is planned for the next Rumoca release, 0.11**, according to
the presenters' roadmap. It maps FMI 3 interfaces to WebAssembly components;
it is separate from today's tested native shared-library export. See the
[FMI-LS-WASM project](https://github.com/modelica/fmi-ls-wasm). This is a Rumoca
release plan, not a claim that the layered standard is finalized or that this
workshop's FMPy demo runs Wasm.

## eFMU: fixed-sample embedded controller

```sh
rumoca compile extras/exports/HoverController.mo --model HoverController \
  --target galec-production -o results/live/efmi
uv run --frozen python examples/export_fmi.py \
  --check-efmu results/live/efmi/HoverController.efmu
```

The export writes `HoverController.efmu` and an unpacked sibling directory:

```text
HoverController/
  __content.xml
  schemas/
  AlgorithmCode/HoverController.alg
  AlgorithmCode/manifest.xml
  ProductionCode/HoverController.c
  ProductionCode/HoverController.h
  ProductionCode/manifest.xml
  ProductionCode/rumoca_galec_kernels.c
  ProductionCode/rumoca_galec_kernels.h
```

`--target galec` exports the Algorithm Code representation only;
`--target galec-production` also emits C99 Production Code and LogicalData
mappings. The released projection accepts **fixed-sample discrete models**,
without continuous states or `der()`. We export a controller for the plant,
rather than asking this target to integrate the continuous quadrotor.
See the [pinned Rumoca eFMI guide](https://github.com/CogniPilot/rumoca/blob/v0.10.2/docs/user-guide/src/codegen/galec-efmi.md).

The controller uses a 0.01 s period, proportional altitude feedback (`kp` in
N/m), vertical-speed feedback (`kd` in N s/m) and thrust limits:

```text
T = clamp(m*g + kp*(z_ref-z) - kd*vz, minThrust, maxThrust)
```

The application allocates state, initializes it, supplies inputs and calls the
generated API on each **100 Hz** controller tick:

```c
HoverControllerState state;
HoverController_startup(&state);
HoverController_recalibrate(&state);
/* Each 0.01 s: write state.z_ref, state.z and state.vz. */
HoverController_dostep(&state);
/* Check state.rumoca_galec_error_signal_status, then read state.T. */
```

Hold the output between ticks. The host owns timing, sensor/actuator interfaces
and fault handling. [check_controller.c](../extras/exports/check_controller.c)
is a small executable harness for this API. For example, compile and run the
unpacked generated C directly in the terminal:

```sh
cc -std=c99 -O2 -I results/live/efmi/HoverController/ProductionCode \
  extras/exports/check_controller.c \
  results/live/efmi/HoverController/ProductionCode/HoverController.c \
  results/live/efmi/HoverController/ProductionCode/rumoca_galec_kernels.c \
  -lm -o results/live/efmi/check-controller
echo '1 1 0' | results/live/efmi/check-controller
```

Expected thrust is approximately **11.772 N** at hover. The Python checking
command validates the actual archive's three manifests against the bundled
schemas, checks nine checksum links, and compiles/runs the archived C for
**515 cases**, including hover and the 0.2/25 N saturation endpoints. C Real
storage is float32; the independent arithmetic oracle uses an explicit
4e-6 N absolute tolerance. This checks the export and calling contract, not
closed-loop flight, real-time scheduling, MISRA or DO-178C certification.

## Rehearse both exports

```sh
uv run --frozen python examples/export_fmi.py
```

This compiles FMI 2 and 3, validates them with FMPy, builds their platform
libraries, simulates them, then exports and executes the eFMU controller.
Outputs are under `results/live/exports/`; disposable CMake builds use
`$HOME/scratch/rumoca-workshop`. **Terminal → Run Task → Workshop: FMU and eFMU
export** runs the same check. Native NixOS maintainers can use
`nix develop .#ci --command uv run --frozen python examples/export_fmi.py`;
that shell supplies the native CMake needed on NixOS.
