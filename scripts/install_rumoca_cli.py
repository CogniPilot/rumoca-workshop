"""Install the checksum-pinned Rumoca CLI for Linux containers and local Linux."""
from pathlib import Path
import argparse
import hashlib
import os
import platform
import shutil
import subprocess
import tempfile
import urllib.request

VERSION = "0.10.2"
ARTIFACTS = {
    "x86_64": ("rumoca-linux-x86_64", "d6c9b51eb207477908aa2b74636ac2aa3c5d149e4ff9e9cdd0d9cfeca54111ba"),
    "aarch64": ("rumoca-linux-aarch64", "c12704c0f04af338dc32ab35801e45c322f9d64a26e0555a9f2b0b5901a2f7a9"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix", type=Path, default=Path.home()/".local")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if platform.system() != "Linux" or platform.machine() not in ARTIFACTS:
        raise SystemExit("This pinned CLI installer supports Linux x64/ARM64. Use the devcontainer on Mac/Windows.")
    name, expected = ARTIFACTS[platform.machine()]
    installed = shutil.which("rumoca") if args.check else str(args.prefix/"bin/rumoca")
    if installed and Path(installed).is_file():
        with Path(installed).open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() == expected:
                print(subprocess.check_output([installed, "--version"], text=True).strip())
                return
        if not args.check:
            raise SystemExit(f"Keeping the existing CLI at {installed}. Choose a separate --prefix for the pinned workshop CLI.")
    if args.check:
        raise SystemExit("Pinned Rumoca CLI missing or checksum differs. Run python scripts/install_rumoca_cli.py.")
    cache = Path.home()/"scratch/rumoca-workshop/cli-downloads"
    cache.mkdir(parents=True, exist_ok=True)
    dest = args.prefix/"bin/rumoca"
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=cache) as temporary:
        download = Path(temporary)/name
        url = f"https://github.com/CogniPilot/rumoca/releases/download/v{VERSION}/{name}"
        request = urllib.request.Request(url, headers={"User-Agent": "Rumoca-workshop"})
        with urllib.request.urlopen(request, timeout=120) as response, download.open("wb") as output:
            shutil.copyfileobj(response, output)
        with download.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != expected:
                raise RuntimeError("Rumoca CLI download checksum mismatch")
        staging = dest.with_name(".rumoca-new")
        shutil.copyfile(download, staging)
        staging.chmod(0o755)
        os.replace(staging, dest)
    print(subprocess.check_output([str(dest), "--version"], text=True).strip())


if __name__ == "__main__":
    main()
