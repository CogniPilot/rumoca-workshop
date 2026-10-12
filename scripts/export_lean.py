"""Invoke the Lean Jinja target through Rumoca's Session API and record provenance.

Types, field layouts, operations and rejection rules live in templates/lean-proof.
Python does not interpret or assemble equations.
"""
from common import *


def main():
    model = rum.Session().load(str(MODEL), model="Quadrotor")
    model.codegen(str(ROOT / "templates/lean-proof")).save_all(str(ROOT / "formal"))
    export = model.to_jax()  # Layout metadata only; no alternate Lean equations.
    program = json.loads((ROOT / "formal/solve_program.json").read_text())
    if (program["n_y"], program["n_p"], program["n_u"]) != (6, 7, 2):
        raise RuntimeError("Unexpected workshop proof-export dimensions")
    output = ROOT / "formal/Generated.lean"
    # A provenance envelope, independent of the target's mathematical rendering.
    prefix = ("-- Generated from models/Quadrotor.mo by Rumoca " + rum.version() + "\n"
              "-- Model SHA256: " + source_hash() + "\n")
    source = prefix + output.read_text(encoding="utf-8")
    output.write_text(source, encoding="utf-8", newline="\n")
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    write_json(ROOT / "formal/provenance.json", {
        "model_sha256": source_hash(), "rumoca_version": rum.version(),
        "state_names": export.state_names, "parameter_names": export.parameter_names,
        "input_names": export.input_names,
        "solve_program_sha256": digest(ROOT / "formal/solve_program.json"),
        "lean_sha256": digest(output),
        "target_sha256": {p.name: digest(p) for p in sorted((ROOT / "templates/lean-proof").iterdir()) if p.is_file()},
        "scope": "Actual checked Solve RHS rendered by the Jinja target as real arithmetic; target not formally verified."})
    print("Exported formal/Generated.lean with the Lean Jinja target via Rumoca Session")


if __name__ == "__main__":
    main()
