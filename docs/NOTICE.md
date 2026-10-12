# Third-party software and modified binary notice

Workshop sources are Apache-2.0 licensed; see LICENSE. Dependencies retain their
own licenses. Rumoca source and release assets originate from
<https://github.com/CogniPilot/rumoca> (Apache-2.0). Upstream
[third-party notices](https://github.com/CogniPilot/rumoca/releases/download/v0.10.2/THIRD_PARTY_NOTICES.md)
apply to its included components.

The two Rumoca 0.10.2 macOS Python wheels in workshop release
`workshop-wheels-2026` are **modified distribution artifacts**, not unmodified
upstream binaries. Only a Mach-O libiconv dependency path was changed from an
unavailable build-machine Nix path to `/usr/lib/libiconv.2.dylib`; ad-hoc signing
and wheel RECORD hashes were updated. No compiler source or mathematical
operation was changed. Script: `scripts/repair_macos_wheel.py`; repair and smoke
workflow: `.github/workflows/repair-macos.yml`. Per-artifact provenance JSON is
available alongside the wheels in that release and in `verification/wheels/`.

The wheel hashes are pinned in uv.lock. macOS ARM64 and Intel runners install
and execute the end-to-end pipeline using them. This qualification is specific
to the Python wheels and supported macOS version; it does not qualify upstream
editor binaries. CasADi, JAX, NumPy, SciPy, Matplotlib, Mathlib and presentation
libraries are separate third-party dependencies with their own notices.
FMPy is distributed under the BSD 2-Clause license; see its
[license](https://github.com/CATIA-Systems/FMPy/blob/v0.3.30/LICENSE.txt).

Browser and VS Code screenshots record real executions of public Rumoca tools.
Workshop plots/diagrams are generated locally from the supplied teaching model;
Asset credits, including institutional marks, are recorded in
[slides/media/README.md](../slides/media/README.md).

The optional gallery screenshots record the public CogniPilot
[fixed-wing app](https://github.com/CogniPilot/rumoca_fixed_wing),
[SLAM Lab](https://github.com/CogniPilot/slam_web) and
[mocap benchmark viewer](https://github.com/CogniPilot/mocap_sysid).
Their source projects use Apache-2.0; third-party models, textures and actors
retain the upstream notices and [SLAM Lab asset credits](https://github.com/CogniPilot/slam_web/blob/main/public/models/licenses/ACTORS.md).
The gallery does not redistribute their complete applications or datasets.
