# Optional: three firmware flights in VS Code

The core workshop Codespace stays lightweight. This separate demo runs
**ArduPilot firmware in patched QEMU**, connected by FastDyn to a **Rumoca FMI 3
plant**. It uses the upstream payload study, with a reference, a 100 g endpoint
and one seeded random load. Runs execute sequentially on a two-core machine.

Create a second Codespace using the repository's **New with options** page and
select **FastDyn + Rumoca: optional firmware Monte Carlo**. Its configuration is
[devcontainer.json](../.devcontainer/fastdyn/devcontainer.json). Prepare it before
the session: source and image downloads happen during creation. The pinned image
downloads **744 MB / 710 MiB compressed**; the installed image is **2.92 GiB**. The source checkout adds about **798 MiB**.
The actual optional Codespace used **7.9 GiB of its 32 GiB disk** after setup,
leaving about **22 GiB** free before the campaign.
This environment requests 32 GB disk and 8 GB RAM. It does not add FastDyn to
the default workshop container. Each additional Codespace uses account storage;
running machines consume compute allowance.

In that Codespace, select **Terminal → Run Task → Workshop: optional FastDyn
Monte Carlo**, or run:

```sh
uv run --frozen python scripts/fastdyn_demo.py
```

Open `results/live/fastdyn/trajectories.png`. The campaign retains the seed,
model sources, firmware logs, per-trial outcomes and trajectories under
`$HOME/scratch/rumoca-workshop/fastdyn/runs`. Repeating unchanged inputs resumes
the upstream study. To start a new experiment, preserve the old results and
use a fresh output directory; the runner refuses changed inputs in an existing
campaign. The optional image pins Rumoca 0.10.0, independently of the core
Python 0.10.2 environment.

The load is a prescribed world-down force at the front-right motor. It changes
neither inertial mass nor payload motion. Ask how the same firmware and gains
respond; compare completion, tilt and trajectory. Three runs demonstrate the
workflow and do not establish a reliability probability or safety certificate.

The [upstream recorded study](https://jgoppert.github.io/FastDyn/rumoca/monte-carlo.html)
is the immediate fallback. Its 18-run results are upstream evidence, not a claim
that this workshop's three-run configuration has passed. The workshop campaign has now passed in an actual two-core Codespace:
[receipt](../verification/fastdyn-codespace.json),
[all three trajectories](../slides/assets/fastdyn-trajectories.png).
Run times were approximately **74, 68 and 61 seconds**, excluding initial setup.
[Verification](VERIFICATION.md) records scope and limits.

Credit **Arslan Khan’s group at Penn State** and the Penn State/Purdue
collaboration. Muhammad Hammad Bashir, Michael Rooney, Colin Smith, Dongyan Xu
and Arslan Khan, *BoardRunner: Automatic Firmware Rehosting using High-Fidelity
Compositional Device Models*, ACM CCS 2026.
[Official accepted-paper program](https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html).
BoardRunner supplies the rehosting research; the Rumoca/FMI integration is
documented in [FastDyn](https://github.com/jgoppert/FastDyn).
