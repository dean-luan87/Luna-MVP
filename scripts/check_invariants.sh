#!/usr/bin/env bash
set -euo pipefail

export LUNA_INVARIANTS=DEBUG

python3 -m pytest \
  tests/invariants \
  tests/test_bc_c_cooperation_table.py \
  tests/test_risk_layer_invariants.py \
  tests/risk_layer \
  tests/test_risk_bc_integration.py \
  tests/test_authority_risk_hysteresis.py \
  tests/test_debug_view.py \
  -v
