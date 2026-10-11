# Local VS Code setup

Use this route if you want the workshop on your own computer. **No Nix, Rust,
CUDA or paid coding agent is required.** Python packages and the native Rumoca
extension are tested in CI on Linux x64, Windows x64, macOS Apple Silicon and
macOS Intel. [Verification](VERIFICATION.md) records the actual checks.

If local installation is taking more than ten minutes, use the
[Codespace route](PUBLICATION.md#codespaces-preflight) or pair with someone whose
environment works. Cloud compute keeps package downloads off your laptop; a
usable internet connection and GitHub allowance/billing are still required.
For outages, use the provided reference figures and instructor screenshare.

## 1. Install VS Code and uv

Install [VS Code for your operating system](https://code.visualstudio.com/download).
Use its normal installer; on macOS, open the Command Palette and run
**Shell Command: Install 'code' command in PATH** if you want terminal commands.

Install uv using [Astral's installation instructions](https://docs.astral.sh/uv/getting-started/installation/).
The workshop CI and container use uv **0.11.21**; the frozen project pins Python
3.12 and its packages independently of your system Python.

Linux/macOS terminal:

```sh
curl -LsSf https://astral.sh/uv/0.11.21/install.sh | sh
```

Windows PowerShell, using the package manager:

```powershell
winget install --id=astral-sh.uv -e
```

Close and reopen the terminal after installation. Run `uv --version`.

## 2. Get the workshop and open its folder

[Download the ZIP](https://github.com/CogniPilot/rumoca_workshop_amc2026/archive/refs/heads/main.zip),
extract it, then use **VS Code → File → Open Folder** on the extracted directory
containing `pyproject.toml`. A GitHub account and Git are unnecessary for this
route. Alternatively:

```sh
git clone https://github.com/CogniPilot/rumoca_workshop_amc2026.git
cd rumoca_workshop_amc2026
code .
```

In VS Code's integrated terminal, with that folder as the working directory:

```sh
uv sync --frozen
uv run --frozen python scripts/smoke_test.py
```

Expect **WORKSHOP PASS**. uv installs the right Python and CPU packages. For
macOS it automatically selects the workshop's qualified release wheels; there
is no manual compiler/library repair. Linux requires a compatible glibc host
(the release wheel targets manylinux 2.28); use Codespaces for incompatible
distributions. NixOS maintainers may use the optional flake below.

## 3. Install the native Rumoca language server extension

Accept the workshop's recommended extensions, or search Extensions for
**Rumoca Modelica**, publisher **JamesGoppert**, ID
`JamesGoppert.rumoca-modelica`. The qualified version is **0.10.2**.
Also install the recommended **Python** extension (`ms-python.python`).

If Marketplace installation is unavailable, download the matching VSIX from the
[Rumoca 0.10.2 release](https://github.com/CogniPilot/rumoca/releases/tag/v0.10.2).
In Extensions, select **… → Install from VSIX…**, then reload the window.

| Computer | Native VSIX asset |
|---|---|
| Linux x64 | `rumoca-modelica-linux-x64-0.10.2.vsix` |
| Windows x64 | `rumoca-modelica-win32-x64-0.10.2.vsix` |
| macOS Apple Silicon | `rumoca-modelica-darwin-arm64-0.10.2.vsix` |
| macOS Intel | `rumoca-modelica-darwin-x64-0.10.2.vsix` |

Open `models/Quadrotor.mo`; the status bar should say **Modelica**. Hover `m`,
try completion on `sin`, and briefly change `der(x) = vx;` to `der(x) = ;`.
Expect a syntax diagnostic; undo the edit and confirm it clears. Do not save
the broken example. The extension bundles the native LSP; a separate Rust
build is unnecessary.

Select **Python: Select Interpreter → .venv** when prompted. Workshop terminal
commands use `uv run` so they select the project interpreter directly.

## 4. Use the same checks as CI

**Terminal → Run Task → Workshop: CI checks** runs the core smoke test followed
by the numerical math audit. Individual simulation, fit and optimization tasks
are available too. These tasks work locally and in Codespaces. Reference
results stay in `results/reference`; new results go to ignored `results/live`.

The optional Torch tasks are qualified on **Linux x64 CPU**, including the
Codespace. They download an extra CPU-only package; see [BACKENDS.md](BACKENDS.md).
Lean checks run in the repository's CI; attendees need not install Mathlib.

## Optional maintainer flake

Maintainers with Nix can use the pinned tool environment:

```sh
nix develop
nix run .#check
nix run .#check -- --torch
nix run .#container-build
```

The last command requires a running Docker daemon and builds the same Debian
devcontainer used by Codespaces and container CI. The flake supplies maintainer
tools; the Python versions and packages remain pinned in `uv.lock`. Linux flake
checks run in GitHub Actions. Darwin shells are declared but are separate from
the Mac qualification performed with ordinary uv. Nix is optional for attendees
and is not installed in the Codespace.
