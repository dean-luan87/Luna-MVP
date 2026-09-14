#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-009 — OCR Stage-2 static config validation tool v0.

CLI (absolute paths only):
python3 tools/validate_ocr_stage2_static_config_v0.py \
  --ocr-precheck-root /Users/luanlei/LunaRuntime/logs/ocr_stage2_trial_precheck_008_... \
  --output-root /Users/luanlei/LunaRuntime/logs/ocr_stage2_static_config_validation_009_<UTC>
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.guarded_trial.ocr_stage2_static_config_validator_v0 import (  # noqa: E402
    run_ocr_stage2_static_config_validation_v0,
)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ocr-precheck-root", required=True, help="ABSOLUTE root from Phase-008 precheck")
    ap.add_argument("--output-root", required=True, help="ABSOLUTE output directory")
    args = ap.parse_args()

    pre_root = Path(args.ocr_precheck_root).expanduser()
    out_root = Path(args.output_root).expanduser()
    if not pre_root.is_absolute() or not out_root.is_absolute():
        raise SystemExit("ERROR: --ocr-precheck-root and --output-root must be absolute paths")
    pre_root = pre_root.resolve()
    out_root = out_root.resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    res = run_ocr_stage2_static_config_validation_v0(ocr_precheck_root=str(pre_root))

    _write_json(out_root / "ocr_stage2_static_config_summary.json", {"phase": "Phase-Mainline-GuardedTrial-009", "ts": _now_iso(), "output_root": str(out_root)})
    _write_json(out_root / "ocr_stage2_static_config_result.json", res)
    _write_json(out_root / "ocr_stage2_source_policy_entrypoint_matrix.json", res.get("source_policy_entrypoint_matrix"))
    _write_json(out_root / "ocr_stage2_provider_candidate_matrix.json", res.get("provider_candidate_matrix"))
    _write_json(out_root / "ocr_stage2_fallback_policy_matrix.json", res.get("fallback_policy_matrix"))
    _write_json(out_root / "ocr_stage2_raw_text_candidate_schema_validation.json", res.get("raw_text_candidate_schema_validation"))
    _write_json(out_root / "ocr_stage2_provider_output_schema_validation.json", res.get("provider_output_schema_validation"))
    _write_json(out_root / "ocr_stage2_trw_output_contract_validation.json", res.get("trw_output_contract_validation"))
    _write_json(out_root / "ocr_stage2_controlled_provider_runbook.json", res.get("controlled_provider_runbook"))

    # Minimal non-empty trace/replay/whitebox for static validation
    _append_jsonl(out_root / "ocr_stage2_static_config_trace.jsonl", {"type": "ocr_stage2_static_trace_v0", "ts": _now_iso(), "validation_id": res.get("validation_id")})
    _append_jsonl(out_root / "ocr_stage2_static_config_replay.jsonl", {"type": "ocr_stage2_static_replay_v0", "ts": _now_iso(), "validation_id": res.get("validation_id")})
    _append_jsonl(out_root / "ocr_stage2_static_config_whitebox.jsonl", {"type": "ocr_stage2_static_whitebox_v0", "ts": _now_iso(), "validation_id": res.get("validation_id")})

    notes = "\n".join(
        [
            "# OCR Stage-2 Static Config Validation v0 (Phase-009)",
            "",
            f"- **ocr_precheck_root:** `{str(pre_root)}`",
            f"- **output_root:** `{str(out_root)}`",
            f"- **static_validation_result:** `{res.get('static_validation_result')}`",
            "",
            "## Hard boundary",
            "",
            "- provider_invoked=false",
            "- ocr_model_invoked=false",
            "- semantic_interpretation_enabled=false",
            "- midplatform/scene_delta/world_context all false",
            "",
        ]
    )
    (out_root / "validation_notes.md").write_text(notes + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out_root), "static_validation_result": res.get("static_validation_result")}, ensure_ascii=False))
    return 0 if res.get("static_validation_result") in {"GO", "CONDITIONAL_GO"} else 2


if __name__ == "__main__":
    raise SystemExit(main())

