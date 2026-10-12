# Synthetic flight-log schema

`noisy_flight.csv` is committed; attendees do not generate it during class.
Generated from the canonical Modelica equations through Rumoca's CasADi export
using independent SciPy DOP853 integration. No experimental/private data.

| Column | Meaning / unit |
|---|---|
| flight | Experiment ID 0–3 |
| split | train for 0–2; validation for 3 |
| time | Seconds, 0–8 inclusive in steps of 0.05 |
| T | Total thrust command, N |
| tau | Pitch torque command, N m |
| x, z | Measured centre-of-mass position, m |
| theta | Measured pitch, rad |
| vx, vz | Measured velocities, m/s |
| omega | Measured pitch rate, rad/s |

Each row's command is held constant until the next row. The terminal command
is repeated for a rectangular CSV schema and has no outgoing interval. All
initial states are exactly known; subsequent state measurements have independent
Gaussian noise specified in `truth.json`. `truth.json` is an presenter answer
and provenance reference; it is public but not used in computing the fit loss.

Regenerate deterministically:

```sh
uv run --frozen python scripts/make_dataset.py
```

Regeneration requires a working Python environment; it is an presenter step.
After a source-equation change, regenerate and requalify identification/control
instead of assuming this stored dataset still represents the new physics.
