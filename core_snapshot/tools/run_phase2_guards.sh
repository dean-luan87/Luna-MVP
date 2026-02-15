#!/usr/bin/env bash
# Phase 2.1 + 2.2 护栏一键跑：外部字段只写不读 → Provider 无逻辑 → determinism guard。
# 用法: ./tools/run_phase2_guards.sh --video <path> [--frames N] [--fps F]
set -e
cd "$(dirname "$0")/.."
python3 tools/guard_no_external_field_reads.py
python3 tools/guard_providers_no_logic.py
python3 tools/run_determinism_guard.py "$@"
