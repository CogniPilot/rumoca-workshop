#!/usr/bin/env bash
# The same CPU checks can run in a Codespace terminal, CI or a maintainer shell.
set -euo pipefail
if [[ "${1:-}" != "" && "${1:-}" != "--torch" ]]; then
  echo "Usage: bash scripts/ci_checks.sh [--torch]" >&2
  exit 2
fi
uv run --frozen python scripts/smoke_test.py
uv run --frozen python scripts/math_audit.py --output results/live
if [[ "${1:-}" == "--torch" ]]; then
  uv run --frozen --group torch python scripts/check_torch_backend.py
  uv run --frozen --group torch python scripts/learn_hover_torch.py
fi
