"""Load our small target.toml backend; physics still comes from Quadrotor.mo."""
from __future__ import annotations

import types
from common import ROOT, MODEL, rum


def load_torch_backend():
    import torch
    torch.set_default_dtype(torch.float64)
    torch.set_num_threads(1)
    model = rum.Session().load(str(MODEL), model="Quadrotor")
    target = ROOT / "templates" / "torch-ode"
    generated = model.codegen(str(target))
    generated.save_all(str(ROOT / "generated" / "torch-ode"))
    module = types.ModuleType("workshop_torch")
    exec(compile(generated.files[0].content, "<Rumoca workshop-torch-ode>", "exec"), module.__dict__)
    return model, module
