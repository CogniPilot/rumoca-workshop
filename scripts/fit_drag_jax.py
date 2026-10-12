"""Compatibility command; participant source lives in examples/."""
from pathlib import Path
import runpy

namespace = runpy.run_path(str(Path(__file__).resolve().parents[1] / "examples" / "fit_drag_jax.py"))
globals().update({key: value for key, value in namespace.items() if not key.startswith("__")})

if __name__ == "__main__":
    main()
