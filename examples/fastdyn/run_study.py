"""Run inside the pinned FastDyn image; reuse its checked study and report runner."""
from pathlib import Path
import subprocess
import tomllib
import tomli_w

root = Path("/workspace")
output = Path("/runs")
settings = tomllib.loads((root / "configs/monte-carlo/payload.toml").read_text())
settings["study"].update(samples=1, seed=462, max_payload_to_vehicle_mass_ratio=0.2)
settings["execution"].update(output="/runs/campaign", publish="", wall_timeout_s=180)
# Reference + 100 g endpoint + one seeded uniform sample: three sequential runs.
study = output / "study.toml"
study.write_text(tomli_w.dumps(settings))
base = output / "base.toml"
subprocess.run(["fastdyn-config", "--base", "configs/copter462.toml", "--overlay",
                "configs/models/qavr-side-payload.toml", "--output", str(base)], check=True)
subprocess.run(["python", "utils/payload_study.py", "--config", str(study),
                "--run-config", str(base), "--limit", "3"], check=True)
manifest = tomllib.loads((output / "campaign/runs.toml").read_text())
assert len(manifest["runs"]) == 3, "Campaign did not record all three trials"
assert manifest["runs"][0]["status"] == "reference", "Unloaded reference did not complete"
print("Three firmware trials recorded. Inspect each outcome; failures are experiment results.")
