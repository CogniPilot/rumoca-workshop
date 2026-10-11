"""Export the actual checked Rumoca scalar Solve RHS into scoped Lean code.

The translator handles only the operations present in this workshop. It refuses
unknown operations. This is a reviewable bridge, not a formally proved compiler.
"""
from fractions import Fraction
from common import *


def main():
    model, export = compile_model()
    model.codegen(str(ROOT / "templates/lean-proof")).save_all(str(ROOT / "formal"))
    program = json.loads((ROOT / "formal/solve_program.json").read_text())
    if (program["n_y"], program["n_p"], program["n_u"]) != (6, 7, 2):
        raise RuntimeError("Unexpected proof-export dimensions")
    types = """import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic

namespace Workshop
noncomputable section

structure State where
  x : ℝ
  z : ℝ
  theta : ℝ
  vx : ℝ
  vz : ℝ
  omega : ℝ

structure Params where
  m : ℝ
  Iyy : ℝ
  g : ℝ
  k_linear : ℝ
  k_quad : ℝ
  damping : ℝ
  eps : ℝ

structure Control where
  T : ℝ
  tau : ℝ

def generatedRhs (_t : ℝ) (s : State) (u : Control) (p : Params) : State :=
"""
    fields = ["p."+name for name in export.parameter_names] + ["u."+name for name in export.input_names]
    lines = []
    stores = set()
    for op in program["ops"]:
        kind = op["kind"]
        if kind == "StoreOutput":
            lines.append(f"  let o{op['index']} := r{op['src']}")
            stores.add(op["index"])
            continue
        if kind == "LoadY":
            expr = "s."+export.state_names[op["index"]]
        elif kind == "LoadP":
            expr = fields[op["index"]]
        elif kind == "LoadTime":
            expr = "_t"
        elif kind == "Const":
            q = Fraction(str(op["value"]))
            expr = f"({q.numerator} / {q.denominator} : ℝ)"
        elif kind == "Move":
            expr = f"r{op['src']}"
        elif kind == "Unary":
            operation = {"Sin": "Real.sin", "Cos": "Real.cos", "Sqrt": "Real.sqrt", "Neg": "Neg.neg"}[op["operator"]]
            expr = f"{operation} r{op['arg']}"
        elif kind == "Binary":
            operation = {"Add": "+", "Sub": "-", "Mul": "*", "Div": "/"}[op["operator"]]
            expr = f"r{op['lhs']} {operation} r{op['rhs']}"
        else:
            raise RuntimeError(f"Unsupported Lean operation {op}")
        lines.append(f"  let r{op['dst']} := {expr}")
    if stores != set(range(6)):
        raise RuntimeError("Proof export omitted a derivative")
    lines.append("  { " + ", ".join(f"{name} := o{i}" for i, name in enumerate(export.state_names)) + " }")
    source = ("-- Generated from models/Quadrotor.mo by Rumoca " + rm.version() + "\n"
              "-- Model SHA256: " + source_hash() + "\n"
              "-- Real-arithmetic interpretation of the checked scalar Solve program.\n"
              "-- Floating-point execution, compiler correctness, and this translator are outside the proof.\n"
              + types + "\n".join(lines) + "\n\nend\nend Workshop\n")
    (ROOT / "formal/Generated.lean").write_text(source)
    write_json(ROOT / "formal/provenance.json", {
        "model_sha256": source_hash(), "rumoca_version": rm.version(),
        "state_names": export.state_names, "parameter_names": export.parameter_names,
        "input_names": export.input_names,
        "solve_program_sha256": hashlib.sha256((ROOT / "formal/solve_program.json").read_bytes()).hexdigest(),
        "lean_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "scope": "Actual checked Solve RHS operations translated to real arithmetic; bridge not formally verified."})
    print("Exported formal/Generated.lean from the checked Rumoca Solve program")


if __name__ == "__main__":
    main()
