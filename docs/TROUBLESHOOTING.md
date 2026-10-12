# Recover and keep participating

**If setup takes more than ten minutes:** use the browser exercise, pair with a
working laptop and interpret [reference results](../results/reference). The workshop
does not require Docker, CUDA, an AI account, Nix or a Google account.

| Symptom | Fix |
|---|---|
| `uv` not found | Install using the official [uv instructions](https://docs.astral.sh/uv/getting-started/installation/); reopen terminal. Do this before class if possible. |
| `pyproject.toml` not found | Open terminal in the extracted repository folder, not its parent ZIP/download folder. |
| Python version conflict | Let `uv sync --frozen` select/download Python 3.12. Do not use an unrelated activated environment or manually mix dependency versions. |
| Download blocked / offline first install | Finish installs before class or use paired/screenshared Python. Reference data/figures are committed. Browser/cloud require networking. |
| Windows path or shell trouble | Use PowerShell in VS Code; all three `uv run --frozen python ...` commands are shell-neutral. No `source`/activation command is needed. |
| macOS too old / unsupported architecture | Qualified wheels require macOS 14+; use browser/cloud/pair route if older. Windows ARM native and musl Linux are not qualified. Linux ARM is pinned but untested here. |
| macOS Rumoca import references `/nix/store` | Use this repository’s frozen lockfile; it pins workshop-qualified portable wheels. No attendee binary repair is needed. Do not substitute upstream macOS 0.10.2 wheels manually. See verification/NOTICE. |
| Local Rumoca extension fails | Release 0.10.2 is tested in actual VS Code 1.119.0 extension hosts on Linux/Windows x64 and both Mac architectures. Check the installed extension version and enable it in this workspace. Browser LSP provides an independent fallback; Codespaces remote activation is checked separately. |
| `.mo` has no highlighting/completion | Check status-bar language **Modelica**, Workspace Trust per local policy, extension enabled, then Developer/Reload Window. View → Output → Rumoca for errors. |
| Python interpreter warning | Ctrl/Cmd+Shift+P → Python: Select Interpreter → choose `.venv` Python (`.venv/Scripts/python.exe` on Windows, `.venv/bin/python` elsewhere). Terminal commands with `uv run` do not require manual activation. |
| Codespaces denied / quota exhausted | Use local `uv`, a partner or presenter demonstration. Do not enable paid billing without your account owner’s authorization. Organization allowance/prebuilds are not presumed. |
| Codespace opens before packages ready | Wait for postCreate completion; Terminal → New Terminal → `uv sync --frozen`, then smoke. If still blocked, switch route. |
| Browser shows stationary Quadrotor | Paste the **entire** bundle, choose **BrowserFlight** in gear/settings, then Play. Base model has stationary initial conditions; wrapper sets initial speed and hover inputs. |
| Browser still shows Ball / read-only example | Click inside the editable model; use a new editable file if the lock icon is closed. Paste all source, confirm outline contains Quadrotor and BrowserFlight. |
| Browser syntax markers after edit | Undo the last edit; recover complete bundle from Raw. Only change coefficient `0.0` to `0.08`; keep semicolons and equation syntax. |
| Plot file missing | Read terminal for successful exit and save path. Open `results/live/`, not `results/reference/`. PNGs are saved, not shown as separate GUI windows. |
| Fit looks unlike the answer | Restore `k_linear=0.18`; check you edited only defaults rather than equations. The fit estimates drag explicitly; editing k_quad defaults does not set the fitted answer. Run smoke for diagnostic failure. |
| JAX fit fails | Restore original fitting script and model; try `--one-coefficient`, which assumes known linear drag 0.18. Use the reference plot if the live run remains broken. |
| “Run fit_drag_jax.py first” | Run JAX fit in the same output directory, then optimize. |
| “Model changed since fit” | Save the model and refit; then optimize. This prevents stale model/fit combinations. |
| Reference fit rejected by source hash | It matches the untouched source only. Restore canonical defaults (linear 0.18, quadratic 0.0) or run your own fit after edits. |
| IPOPT variant fails / large fine-rollout error | Return to default target x=4 and source, refit and solve. A new target requires feasibility/integration validation; local NLP convergence is not guaranteed for arbitrary changes. |
| Solver says success but a bound differs in the last digits | Check tolerance; acceptance uses 1e−6 numerical tolerance, and physical pitch has an explicit margin. Larger violations fail smoke and require correction. |

Git-clone recovery, **only when you intend to discard your own edits**:

```sh
git restore models/Quadrotor.mo examples/fit_drag_jax.py examples/optimize_casadi.py
uv run --frozen python scripts/smoke_test.py
```

ZIP users can undo edits in VS Code or re-extract a clean download. Do not delete
the lockfile or “fix” dependency versions during class. Presenter source and
math audit details: [MATH_REVIEW.md](MATH_REVIEW.md), [VERIFICATION.md](VERIFICATION.md).
