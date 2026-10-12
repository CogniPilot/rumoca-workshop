"""Inspect the actual generated Python files; never hand-edit these outputs."""
from common import *

model, _ = compile_model()
for target in ["jax-ode", "casadi-ode"]:
    dest = ROOT / "generated" / target
    model.codegen(target).save_all(str(dest))
    print(f"Rumoca {rum.version()}: {target} -> {dest}")
