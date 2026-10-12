"""Install workshop editor extensions and the qualified native LSP in Codespaces' remote extension directory.

Normal VS Code/devcontainer customization installs remain enabled. This pinned
VSIX fallback also works before the first browser/editor attaches.
"""
from pathlib import Path
import json
import hashlib
import os
import platform
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
        extension = identifier+"@"+version if version else identifier
        subprocess.run([str(servers[0]), "--install-extension", extension,
                        "--extensions-dir", str(extension_root)], check=True)
    for identifier, version in (("mathematic.vscode-pdf", "0.1.11"),
                                ("leanprover.lean4", "0.0.240"),
                                ("samuelcolvin.jinjahtml", "0.20.0"),
                                ("bierner.markdown-preview-github-styles", "2.2.0")):
        subprocess.run([str(servers[0]), "--install-extension", identifier+"@"+version,
                        "--extensions-dir", str(extension_root), "--force"], check=True)
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
