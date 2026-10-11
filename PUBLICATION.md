# Cloud access and reproducibility

The public workshop repository is
<https://github.com/CogniPilot/rumoca_workshop_amc2026>. It uses pinned release
dependencies and is independent of the main Rumoca checkout. Participants can
download the ZIP without a GitHub account.

## Workshop links

- [Participant walkthrough](https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/WORKSHOP.md)
- [Download ZIP](https://github.com/CogniPilot/rumoca_workshop_amc2026/archive/refs/heads/main.zip)
- [Create a Codespace](https://codespaces.new/CogniPilot/rumoca_workshop_amc2026?quickstart=1)
- [Rumoca browser playground](https://rumoca.cognipilot.org/playground/)

Browser participation needs no account. For the full Python workflow, use a
Codespace with an available account allowance, or install uv locally and run
`uv sync --frozen` followed by the smoke command in [README.md](README.md).
Bring a charged laptop. Paired work and reference figures provide recovery if
setup is incomplete.

## Codespaces preflight

The devcontainer builds in CI and its startup commands pass as the non-root
`vscode` user. [VERIFICATION.md](VERIFICATION.md) records fresh-cloud and editor
qualification separately from the container test.

Before class, open a fresh environment with the account you will use. Confirm
setup completes with **WORKSHOP PASS**, the terminal runs the three examples,
and the Python interpreter uses `.venv`. Open `models/Quadrotor.mo` and check
Rumoca hover, completion and diagnostics. Account quotas, supported regions
and venue connectivity should be checked for the intended participants.

Codespaces usage depends on account allowance, organization policy and billing;
public repository access does not include cloud compute. See
[GitHub billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces)
and [included usage](https://docs.github.com/en/billing/reference/product-usage-included).
The local uv route supports the four operating-system/architecture targets
listed in [VERIFICATION.md](VERIFICATION.md).

## Prebuilds

For accounts and organizations supporting prebuilds, repository
**Settings → Codespaces → Prebuilds** selects a branch and region. Wait for
“ready” and test creating a new Codespace from that prebuild.
[GitHub's prebuild documentation](https://docs.github.com/en/codespaces/prebuilding-your-codespaces/about-github-codespaces-prebuilds)
explains availability, storage and billing. `onCreateCommand` and
`updateContentCommand` run during prebuilds; `postCreateCommand` runs during
individual creation.

This workshop caches Python dependencies in the container image and runs
`uv sync` plus the smoke test at `postCreate`. A container CI pass does not
establish prebuild readiness or simultaneous availability for a class.

## Qualified macOS wheel release

The workshop owns release
[workshop-wheels-2026](https://github.com/CogniPilot/rumoca_workshop_amc2026/releases/tag/workshop-wheels-2026).
Upstream macOS 0.10.2 wheels contained a nonportable libiconv load reference.
The maintainer repair script changes that reference to the operating system’s
libiconv, signs the library and regenerates wheel RECORD. It does not alter
compiler code. Frozen hashes select these two tested artifacts automatically.
Linux/Windows retain upstream release wheels. See [NOTICE.md](NOTICE.md).

No Nix, Rust compiler or manual binary repair is required for attendees. The
released VS Code extension was separately qualified on all four OS/architecture
targets; Python and editor receipts are recorded in [VERIFICATION.md](VERIFICATION.md).
