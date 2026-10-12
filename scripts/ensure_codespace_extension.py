"""Install workshop editor extensions and the qualified native LSP in Codespaces' remote extension directory.

Normal VS Code/devcontainer customization installs remain enabled. This pinned
VSIX fallback also works before the first browser/editor attaches.
"""
from pathlib import Path
import json
import hashlib
import os
import platform
import re
import time
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile


def main():
    if os.environ.get("CODESPACES") != "true":
        print("Codespaces extension fallback: local editor uses its normal extension installation.")
        return
    assert platform.system() == "Linux" and platform.machine() == "x86_64"
    home = Path.home()
    extension_root = home/".vscode-remote/extensions"
    # GitHub stages its native VS Code Server before postCreate runs.
    candidates = sorted(Path("/vscode/bin/linux-x64").glob("*/bin/code-server"))
    candidates += sorted((home/".vscode-server/bin").glob("*/bin/code-server"))
    servers = [path for path in candidates if path.is_file() and os.access(path, os.X_OK)]
    if not servers:
        raise RuntimeError("VS Code Server unavailable; rebuild the Codespace to finish extension setup.")
    def server_version(server):
        package = server.parents[1]/"package.json"
        version = json.loads(package.read_text()).get("version", "") if package.exists() else ""
        return tuple(int(n) for n in re.findall(r"\d+", version)[:3])
    servers.sort(key=server_version, reverse=True)
    cache = Path("/opt/workshop-vsix")
    index = json.loads((cache/"index.json").read_text()) if (cache/"index.json").exists() else {}

    def installed(identifier, version):
        return any(json.loads(p.read_text()).get("version") == version
                   for p in extension_root.glob(identifier.lower()+"-*/package.json"))

    def install(identifier, version, optional=False):
        if installed(identifier, version):
            print(f"Workshop extension already installed: {identifier} {version}")
            return
        entry = index.get(identifier.lower())
        if entry and entry["version"] == version:
            file = cache/entry["file"]
            if hashlib.sha256(file.read_bytes()).hexdigest() != entry["sha256"]:
                raise RuntimeError(f"Cached VSIX checksum mismatch: {identifier}")
            target = str(file)
        else:
            target = identifier+"@"+version if version else identifier
        for attempt in range(3):
            result = subprocess.run([str(servers[0]), "--install-extension", target,
                                     "--extensions-dir", str(extension_root)])
            if result.returncode == 0:
                return
            if attempt < 2:
                time.sleep(2*(attempt+1))
        if optional:
            print(f"Optional agent extension unavailable: {identifier}; install from Extensions when the Marketplace responds.")
        else:
            raise RuntimeError(f"Required workshop extension could not be installed: {identifier}")

    # Keep the viewer compatible with both the qualified desktop and cloud editors.
    agent_extensions = json.loads(Path(__file__).with_name("agent_tools.json").read_text())["extensions"]
    for identifier, version in agent_extensions.items():
        # Current VS Code bundles Copilot Chat. Respect it rather than forcing an
        # older Marketplace dependency over the bundled extension.
        bundled = [path for server in servers
                   for path in (server.parents[1]/"extensions").glob("*/package.json")
                   if (lambda package: (package.get("publisher", "")+"."+package.get("name", "")).lower()
                       == identifier.lower())(json.loads(path.read_text()))]
        if bundled:
            print(f"Agent extension supplied by VS Code: {identifier}")
            continue
        install(identifier, version, optional=True)
    for identifier, version in (("mathematic.vscode-pdf", "0.1.11"),
                                ("leanprover.lean4", "0.0.240"),
                                ("samuelcolvin.jinjahtml", "0.20.0"),
                                ("bierner.markdown-preview-github-styles", "2.2.0")):
        install(identifier, version)
        installed = [json.loads(path.read_text())
                     for path in extension_root.glob(identifier.lower()+"-*/package.json")]
        if not any(package.get("version") == version for package in installed):
            raise RuntimeError(f"Workshop extension was not installed: {identifier}")
        print(f"Workshop extension installed: {identifier} {version}")
    for metadata in extension_root.glob("jamesgoppert.rumoca-modelica-*/package.json"):
        package = json.loads(metadata.read_text())
        server = metadata.parent/"bin/rumoca-lsp"
        if package.get("version") == "0.10.2" and server.is_file() and os.access(server, os.X_OK):
            print("Rumoca Modelica 0.10.2 native LSP already installed for Codespaces.")
            return
    if "jamesgoppert.rumoca-modelica" in index:
        install("JamesGoppert.rumoca-modelica", "0.10.2")
        server = next(extension_root.glob("jamesgoppert.rumoca-modelica-*/bin/rumoca-lsp"))
        assert server.is_file() and os.access(server, os.X_OK)
        print("Rumoca Modelica 0.10.2 native LSP installed from the image's cached VSIX.")
        return
    scratch = home/"scratch/rumoca-workshop/downloads"
    scratch.mkdir(parents=True, exist_ok=True)
    url = "https://github.com/CogniPilot/rumoca/releases/download/v0.10.2/rumoca-modelica-linux-x64-0.10.2.vsix"
    with tempfile.TemporaryDirectory(dir=scratch) as tmp:
        vsix = Path(tmp)/"rumoca-modelica-linux-x64-0.10.2.vsix"
        with urllib.request.urlopen(url, timeout=60) as response, vsix.open("wb") as output:
            shutil.copyfileobj(response, output)
        assert hashlib.sha256(vsix.read_bytes()).hexdigest() == "d90956a83df22165f9ba6aea44d8e89f93d993b010bdef0902bd56e190c8d451"
        with zipfile.ZipFile(vsix) as bundle:
            package = json.loads(bundle.read("extension/package.json"))
            assert package["version"] == "0.10.2" and package["publisher"] == "JamesGoppert"
        subprocess.run([str(servers[0]), "--install-extension", str(vsix),
                        "--extensions-dir", str(extension_root), "--force"], check=True)
    packages = [json.loads(path.read_text()) for path in extension_root.glob("jamesgoppert.rumoca-modelica-*/package.json")]
    assert any(package.get("version") == "0.10.2" for package in packages)
    print("Rumoca Modelica 0.10.2 installed for Codespaces; open a .mo file to activate its LSP.")


if __name__ == "__main__":
    main()
