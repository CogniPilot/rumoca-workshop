"""CLI export, independent FMU execution and generated eFMU C checks (Linux)."""
from __future__ import annotations
import argparse
import hashlib
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"scripts"))
from common import ROOT, MODEL, write_json
from run_fmu import verify_fmu
import numpy as np
from lxml import etree


def check_efmu(archive: Path, output: Path):
    # Execute bytes extracted from the actual archive, rather than its sibling.
    cache = Path.home()/"scratch/rumoca-workshop/fmi-build"
    cache.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=cache) as temporary:
        directory = Path(temporary)
        with zipfile.ZipFile(archive) as package:
            package.extractall(directory)
        registry = etree.parse(str(directory/"__content.xml"))
        schema_checks, checksum_checks = [], 0
        for path in [directory/"__content.xml", directory/"AlgorithmCode/manifest.xml", directory/"ProductionCode/manifest.xml"]:
            document = etree.parse(str(path))
            location = document.getroot().get("{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation")
            etree.XMLSchema(etree.parse(str(path.parent/location))).assertValid(document)
            schema_checks.append(path.relative_to(directory).as_posix())
        manifests = {}
        for representation in registry.getroot().findall("ModelRepresentation"):
            path = directory/representation.get("name")/representation.get("manifest")
            assert hashlib.sha1(path.read_bytes()).hexdigest() == representation.get("checksum")
            document = etree.parse(str(path))
            assert document.getroot().get("id") == representation.get("manifestRefId")
            manifests[document.getroot().get("id")] = path
            checksum_checks += 1
            for file in document.findall("Files/File"):
                artifact = path.parent/file.get("path")/file.get("name")
                assert hashlib.sha1(artifact.read_bytes()).hexdigest() == file.get("checksum")
                checksum_checks += 1
        production = directory/"ProductionCode"
        document = etree.parse(str(production/"manifest.xml"))
        for reference in document.findall("ManifestReferences/ManifestReference"):
            path = manifests[reference.get("manifestRefId")]
            assert hashlib.sha1(path.read_bytes()).hexdigest() == reference.get("checksum")
            checksum_checks += 1
        executable = directory/"check-controller"
        subprocess.run(["cc", "-std=c99", "-O2", "-I", str(production),
                        str(ROOT/"extras/exports/check_controller.c"),
                        str(production/"HoverController.c"), str(production/"rumoca_galec_kernels.c"),
                        "-lm", "-o", str(executable)], check=True)
        rng = np.random.default_rng(2026)
        cases = np.vstack([[1., 1., 0.], [100., 0., 0.], [-100., 0., 0.],
                           rng.uniform([-2., -2., -5.], [3., 3., 5.], (512, 3))]).astype(np.float32)
        rows = "\n".join(" ".join(f"{float(value):.9g}" for value in row) for row in cases)+"\n"
        observed = np.fromstring(subprocess.check_output([str(executable)], input=rows, text=True), sep="\n")
        # Independent oracle for the declared controller, not a second vehicle.
        expected = np.clip(1.2*9.81+2.*(cases[:, 0].astype(float)-cases[:, 1])-cases[:, 2], .2, 25.)
        np.testing.assert_allclose(observed, expected, atol=4e-6, rtol=0)
        report = {"status": "PASS", "source_sha256": hashlib.sha256((ROOT/"extras/exports/HoverController.mo").read_bytes()).hexdigest(),
                  "efmu_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
                  "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  "harness_sha256": hashlib.sha256((ROOT/"extras/exports/check_controller.c").read_bytes()).hexdigest(),
                  "schemas": schema_checks, "checksum_checks": checksum_checks, "generated_C_cases": len(cases),
                  "max_thrust_error_N": float(np.max(np.abs(observed-expected))),
                  "hover_thrust_N": float(observed[0]), "high_saturation_N": float(observed[1]), "low_saturation_N": float(observed[2]),
                  "sample_period_s": .01, "real_precision": "float32",
                  "scope": "Bundled eFMI schemas and checksum web; compile and execute generated C for finite test inputs. No MISRA, DO-178C, full stability or drone safety claim."}
        write_json(output/"efmu.json", report)
        print(f'eFMU PASS: 3 XML schemas, {checksum_checks} checksums, {len(cases)} generated-C checks; hover {observed[0]:.6f} N')
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT/"results/live/exports")
    parser.add_argument("--check-efmu", type=Path, help="Check and execute an existing controller eFMU archive")
    args = parser.parse_args()
    if platform.system() != "Linux":
        raise SystemExit("This CLI export rehearsal is qualified in the Linux devcontainer. Use that route on Mac/Windows.")
    if not shutil.which("cc"):
        raise SystemExit("C compiler missing: use the devcontainer, or install build-essential on Debian/Ubuntu.")
    if args.check_efmu:
        check_efmu(args.check_efmu, args.check_efmu.parent)
        return
    subprocess.run([sys.executable, str(ROOT/"scripts/install_rumoca_cli.py"), "--check"], check=True)
    # Nix's CMake takes precedence over the generic pip wheel on NixOS.
    if os.environ.get("WORKSHOP_CMAKE"):
        os.environ["PATH"] = str(Path(os.environ["WORKSHOP_CMAKE"]).parent)+os.pathsep+os.environ["PATH"]
    scratch = Path.home()/"scratch/rumoca-workshop/tmp"
    scratch.mkdir(parents=True, exist_ok=True)
    os.environ["TMPDIR"] = str(scratch)
    tempfile.tempdir = str(scratch)
    reports = []
    for target in ["fmi2", "fmi3"]:
        dest = args.output/target
        subprocess.run(["rumoca", "compile", str(MODEL), "--model", "Quadrotor", "--target", target, "--output", str(dest)], check=True)
        filename = dest/"Quadrotor.fmu"
        subprocess.run(["fmpy", "validate", str(filename)], check=True)
        subprocess.run(["fmpy", "compile", str(filename)], check=True)
        reports.append(verify_fmu(filename, dest))
    dest = args.output/"efmi"
    subprocess.run(["rumoca", "compile", str(ROOT/"extras/exports/HoverController.mo"), "--model", "HoverController",
                    "--target", "galec-production", "--output", str(dest)], check=True)
    controller = check_efmu(dest/"HoverController.efmu", dest)
    write_json(args.output/"exports.json", {"status": "PASS", "fmu": reports, "efmu": controller,
              "cli_version": subprocess.check_output(["rumoca", "--version"], text=True).strip(),
              "platform": platform.machine(), "scope": "Native FMI 2/3 and eFMI exports. FMI-LS-WASM is a planned Rumoca 0.11 feature; not this workshop demo."})


if __name__ == "__main__":
    main()
