#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ ! -f .venv/pyvenv.cfg ]]; then
  echo "[OAP] Creating local Python sandbox .venv"
  python3 -m venv .venv
fi
.venv/bin/python -c 'import sys; assert sys.prefix != sys.base_prefix; print(".venv OK:", sys.executable)'
