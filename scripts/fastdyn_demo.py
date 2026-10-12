"""Prepare or run the optional pinned FastDyn/QEMU firmware campaign."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REVISION = "1b6fc8e0eb19b978aee4075ad45f981cc2a19b35"
IMAGE = "ghcr.io/jgoppert/fastdyn/dev@sha256:e150b2dd164e06a4b47f990032548edd6ac7263fcc1a728fe4ffe7a62a1235b0"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true", help="Download sources and tools without flying")
    args = parser.parse_args()
    if not shutil.which("docker"):
        parser.error("Select the separate FastDyn devcontainer, or use Linux with Docker. See docs/FASTDYN.md.")
    scratch = Path.home() / "scratch/rumoca-workshop/fastdyn"
    checkout = scratch / "source"
    scratch.mkdir(parents=True, exist_ok=True)
    if not checkout.exists():
        subprocess.run(["git", "clone", "--filter=blob:none", "--no-checkout", "https://github.com/jgoppert/FastDyn", str(checkout)], check=True)
        subprocess.run(["git", "checkout", REVISION], cwd=checkout, check=True)
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=checkout, text=True).strip()
    if actual != REVISION or subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"], cwd=checkout, text=True).strip():
        raise RuntimeError("FastDyn sources changed. Preserve your work and choose a fresh demo source directory.")
    subprocess.run(["git", "submodule", "update", "--init", "--depth", "1", "third_party/common/modelica_models"], cwd=checkout, check=True)
    subprocess.run(["docker", "pull", IMAGE], check=True)
    size = json.loads(subprocess.check_output(["docker", "image", "inspect", IMAGE], text=True))[0]["Size"]
    print(f"FastDyn image installed: {size / 1024**3:.2f} GiB", flush=True)
    if args.prepare:
        return
    runs = scratch / "runs"
    runs.mkdir(exist_ok=True)
    command = ["docker", "run", "--rm", "--init", "--user", f"{os.getuid()}:{os.getgid()}",
               "--volume", f"{checkout}:/workspace", "--volume", f"{ROOT}:/workshop:ro",
               "--volume", f"{runs}:/runs", "--workdir", "/workspace", IMAGE,
               "python", "/workshop/extras/fastdyn/run_study.py"]
    subprocess.run(command, check=True)
    report = runs / "campaign/report"
    destination = ROOT / "results/live/fastdyn"
    destination.mkdir(parents=True, exist_ok=True)
    for source in report.iterdir():
        if source.is_file():
            shutil.copy2(source, destination / source.name)
    print("Open results/live/fastdyn/trajectories.png in VS Code.")


if __name__ == "__main__":
    main()
