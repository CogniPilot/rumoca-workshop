"""Run a compiled workshop FMU with FMPy and compare with Rumoca's JAX model."""
from __future__ import annotations
import argparse
import hashlib
import tempfile
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"scripts"))
from common import MODEL, STATE_NAMES, jax_rollout, parameters, plot_style, source_hash, write_json
import numpy as np
import rumoca as rum
from fmpy import read_model_description, simulate_fmu, __version__ as fmpy_version
from fmpy.validation import validate_fmu


def simulate_native(filename, description, **options):
    import fmpy
    if fmpy.architecture != "aarch64" or not description.fmiVersion.startswith("3."):
        return simulate_fmu(str(filename), **options)
    # FMPy 0.3.30's supported_platforms() recognizes x86 Linux FMI 3 paths,
    # but not binaries/aarch64-linux. Use its public pre-instantiation API
    # with the actual native library; retain schema/ABI/numerical validation.
    from fmpy.simulation import instantiate_fmu
    scratch = Path.home()/"scratch/rumoca-workshop/fmi-build"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as temporary:
        fmpy.extract(str(filename), unzipdir=temporary)
        profile = options["fmi_type"]
        interface = description.coSimulation if profile == "CoSimulation" else description.modelExchange
        library = Path(temporary)/"binaries"/fmpy.platform_tuple/(interface.modelIdentifier+fmpy.sharedLibraryExtension)
        if not library.is_file():
            raise RuntimeError(f"Native ARM64 FMU binary missing: {library}")
        instance = instantiate_fmu(temporary, description, fmi_type=profile, library_path=str(library))
        try:
            return simulate_fmu(temporary, model_description=description, fmu_instance=instance, **options)
        finally:
            instance.freeInstance()


def verify_fmu(filename: Path, output: Path):
    problems = validate_fmu(str(filename))
    if problems:
        raise RuntimeError(f"FMU validation failed: {problems}")
    description = read_model_description(str(filename), validate=True)
    assert description.modelName == "Quadrotor"
    assert description.modelExchange and description.coSimulation
    variables = {variable.name: variable for variable in description.modelVariables}
    assert {name for name, v in variables.items() if v.causality == "input"} == {"T", "tau"}
    # 0.10.2 exports the time unit, but omits other Modelica unit annotations.
    # Keep the explicit SI interface contract; reject conflicting metadata.
    for name, unit in {"T": "N", "tau": "N.m"}.items():
        assert variables[name].unit in {None, unit}
    model = rum.Session().load(str(MODEL), model="Quadrotor")
    export = model.to_jax()
    import jax
    jax.config.update("jax_enable_x64", True)
    # The reference integrates compiler-generated dynamics, with no Python plant.
    dt = 0.0025
    rollout = jax_rollout(export, dt=dt)
    base = dict(zip(export.parameter_names, export.default_parameters))
    output.mkdir(parents=True, exist_ok=True)
    plot_style()
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6), layout="constrained")
    checks = []
    for case, vx0, torque, k_quad in [
        ("hover", 0., 0., 0.), ("linear coast", 6., 0., 0.),
        ("quadratic coast", 6., 0., .08), ("pitch excitation", .4, .015, .08),
    ]:
        thrust = base["m"]*base["g"]
        x0 = np.array([0., 1., 0., vx0, 0., 0.])
        controls = np.tile([thrust, torque], (800, 1))
        reference = np.asarray(rollout(parameters(export, k_quad=k_quad), x0, controls))[::8]
        for profile in ["CoSimulation", "ModelExchange"]:
            # CVode ships for Linux x64. The portable ARM route uses CS, whose
            # integrator is part of the FMU; no Sundials binary is required.
            import fmpy
            cvode = Path(fmpy.__file__).parent/"sundials"/fmpy.platform_tuple/("sundials_cvode"+fmpy.sharedLibraryExtension)
            if profile == "ModelExchange" and not cvode.exists():
                continue
            trace = simulate_native(
                filename, description, fmi_type=profile, stop_time=2.0,
                output_interval=.02, relative_tolerance=1e-9,
                start_values={"vx": vx0, "T": thrust, "tau": torque, "k_quad": k_quad},
                output=STATE_NAMES, validate=True,
            )
            assert len(trace) == 101 and np.allclose(trace["time"], np.arange(101)*.02, atol=1e-12, rtol=0)
            values = np.column_stack([trace[name] for name in STATE_NAMES])
            assert np.isfinite(values).all()
            errors = np.max(np.abs(values-reference), axis=0)
            # Per-state SI tolerances: m, m, rad, m/s, m/s, rad/s.
            np.testing.assert_allclose(values, reference, atol=3e-6, rtol=0)
            analytic_error = None
            if case == "linear coast":
                rate = base["k_linear"]/base["m"]
                analytic_vx = vx0*np.exp(-rate*trace["time"])
                analytic_x = vx0*(-np.expm1(-rate*trace["time"]))/rate if rate else vx0*trace["time"]
                analytic_error = float(max(np.max(np.abs(trace["vx"]-analytic_vx)), np.max(np.abs(trace["x"]-analytic_x))))
                assert analytic_error < 3e-6
            if case == "hover":
                np.testing.assert_allclose(values, np.tile(x0, (101, 1)), atol=1e-9, rtol=0)
            checks.append({"case": case, "profile": profile, "samples": len(trace),
                           "max_error_by_state_SI": dict(zip(STATE_NAMES, errors.tolist())),
                           "analytic_max_error": analytic_error})
            label = f"{case} · {'CS' if profile == 'CoSimulation' else 'ME'}"
            style = "-" if profile == "CoSimulation" else "--"
            axes[0].plot(trace["time"], trace["vx"], style, label=label)
            axes[1].plot(trace["time"], trace["z"], style, label=label)
            np.savetxt(output/f'{case.replace(" ", "-")}-{profile}.csv',
                       np.column_stack([trace[name] for name in trace.dtype.names]),
                       delimiter=",", header=",".join(trace.dtype.names), comments="")
    for ax, ylabel in zip(axes, ["Horizontal velocity [m/s]", "Altitude [m]"]):
        ax.set(xlabel="Time [s]", ylabel=ylabel)
        ax.grid(alpha=.2)
    axes[0].legend(fontsize=7, ncol=2)
    fig.suptitle(f"Same Quadrotor.mo · FMI {description.fmiVersion} · independent FMPy execution")
    fig.savefig(output/"fmu.png", dpi=160)
    plt.close(fig)
    report = {"status": "PASS", "rumoca_version": rum.version(), "fmpy_version": fmpy_version,
              "fmi_version": description.fmiVersion, "source_sha256": source_hash(),
              "input_units_SI": {"T": "N", "tau": "N.m"},
              "unit_metadata_note": "Rumoca 0.10.2 omits non-time units in FMU XML; use the Modelica SI contract.",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "fmu_sha256": hashlib.sha256(filename.read_bytes()).hexdigest(), "checks": checks,
              "scope": "This event-free planar model: schema, metadata, hover, analytic linear coast, nonlinear drag and coupled pitch traces. Not whole-compiler or hardware assurance."}
    write_json(output/"fmu.json", report)
    print(f'FMU PASS: FMI {description.fmiVersion}, {len(checks)} FMPy runs; saved {output/"fmu.png"}')
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fmu", type=Path)
    parser.add_argument("--output", type=Path, default=Path("results/live/fmi3"))
    args = parser.parse_args()
    verify_fmu(args.fmu, args.output)
