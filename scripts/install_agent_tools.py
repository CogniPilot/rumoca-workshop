"""Install versioned native CLIs; credentials remain with each participant."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def codex_package(executable, version):
    """The interactive CLI needs its complete official package, not just bin/codex."""
    root = Path(executable).resolve().parent.parent
    metadata = root / "codex-package.json"
    if not metadata.is_file():
        return False
    package = json.loads(metadata.read_text())
    return package.get("version") == version and all(
        (root / name).is_file()
        for name in ["bin/codex-code-mode-host", "codex-path/rg", "codex-resources/bwrap"]
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix", type=Path, default=Path.home()/".local")
    parser.add_argument("--check", action="store_true", help="Check the installed tools without signing in")
    args = parser.parse_args()
    manifest = json.loads(Path(__file__).with_name("agent_tools.json").read_text())
    if not args.check:
        assert platform.system() == "Linux", "The container installer supports Linux only"
        cache = Path.home()/"scratch/rumoca-workshop/agent-downloads"
        cache.mkdir(parents=True, exist_ok=True)
        dest = args.prefix/"bin"
        dest.mkdir(parents=True, exist_ok=True)
        for name in ["codex", "claude", "copilot"]:
            pin = manifest[name]
            artifact = pin["platforms"][platform.machine()]
            existing = dest/name
            if existing.is_file():
                version = subprocess.check_output([str(existing), "--version"], text=True).strip()
                complete = not artifact.get("package") or codex_package(existing, pin["version"])
                if complete and pin["version"] in re.findall(r"\d+\.\d+\.\d+(?:[-+][\w.-]+)?", version):
                    print(f"Already installed: {version}")
                    continue
            with tempfile.TemporaryDirectory(dir=cache) as tmp:
                download = Path(tmp)/"download"
                request = urllib.request.Request(artifact["url"], headers={"User-Agent": "Rumoca-workshop"})
                with urllib.request.urlopen(request, timeout=120) as response, download.open("wb") as output:
                    shutil.copyfileobj(response, output)
                if digest(download) != artifact["sha256"]:
                    raise RuntimeError(f"Checksum mismatch: {name}")
                if artifact.get("package"):
                    package_dir = args.prefix / "lib" / name / f'{pin["version"]}-{platform.machine()}'
                    package_dir.parent.mkdir(parents=True, exist_ok=True)
                    # Preserve the official relative layout used to discover daemon resources.
                    # Extraction is checksum checked and rejects escaping links/paths.
                    with tarfile.open(download, "r:gz") as archive:
                        archive.extractall(package_dir, filter="data")
                    assert codex_package(package_dir / "bin/codex", pin["version"]), "Incomplete Codex package"
                    link = dest / f".{name}-new"
                    link.unlink(missing_ok=True)
                    link.symlink_to(package_dir.resolve() / "bin/codex")
                    link.replace(existing)
                elif "member" in artifact:
                    with tarfile.open(download, "r:gz") as archive:
                        member = archive.getmember(artifact["member"])
                        assert member.isfile(), "Expected a regular executable"
                        with archive.extractfile(member) as source, existing.open("wb") as output:
                            shutil.copyfileobj(source, output)
                else:
                    shutil.copyfile(download, existing)
                existing.chmod(0o755)
            print(subprocess.check_output([str(existing), "--version"], text=True).strip())
    else:
        versions = {}
        for name in ["codex", "claude", "copilot"]:
            versions[name] = subprocess.check_output([name, "--version"], text=True).strip()
            assert manifest[name]["version"] in re.findall(r"\d+\.\d+\.\d+(?:[-+][\w.-]+)?", versions[name]), versions[name]
            subprocess.run([name, "--help"], check=True, stdout=subprocess.DEVNULL)
        assert codex_package(shutil.which("codex"), manifest["codex"]["version"]), (
            "Codex interactive startup requires its complete official package; rebuild the container. "
            "For an existing older container, codex --no-daemon is a temporary fallback."
        )
        for name, flag in [("node", "--version"), ("npm", "--version"), ("gh", "--version"), ("tmux", "-V")]:
            versions[name] = subprocess.check_output([name, flag], text=True).strip()
        socket = f"rumoca-workshop-verification-{os.getpid()}"
        subprocess.run(["tmux", "-L", socket, "new-session", "-d", "-s", "check", "sleep 30"], check=True)
        try:
            subprocess.run(["tmux", "-L", socket, "has-session", "-t", "check"], check=True)
        finally:
            subprocess.run(["tmux", "-L", socket, "kill-session", "-t", "check"], check=True)
        root = Path(__file__).resolve().parents[1]
        output = root/"results/live/agent-tools.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({"status": "PASS", "platform": platform.machine(), "versions": versions,
            "detached_tmux_session": "PASS", "codex_complete_package": "PASS",
            "manifest_sha256": digest(Path(__file__).with_name("agent_tools.json")),
            "scope": "CLI version/help, complete Codex package, Node/npm and detached tmux execution. No account login or billed model request."}, indent=2)+"\n")
        print("AGENT TOOLS PASS: "+json.dumps(versions))


if __name__ == "__main__":
    main()
