#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-009 — Run OCR Stage-2 static configuration validation v0.

Hard rule: output-root must be ABSOLUTE to avoid audit ambiguity.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any

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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True, help="ABSOLUTE output directory")
    args = ap.parse_args()

    out_root = Path(args.output_root).expanduser()
    if not out_root.is_absolute():
        raise SystemExit("ERROR: --output-root must be an absolute path (e.g. /Users/.../LunaRuntime/logs/...)")
    out_root = out_root.resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    res = run_ocr_stage2_static_config_validation_v0()

    _write_json(out_root / "ocr_stage2_static_config_validation_summary.json", {"phase": "Phase-Mainline-GuardedTrial-009", "ts": _now_iso(), "output_root": str(out_root)})
    _write_json(out_root / "ocr_stage2_static_config_validation_result.json", res)
    _write_json(out_root / "ocr_stage2_controlled_provider_runbook_009.json", res.get("controlled_provider_runbook"))
    _write_json(out_root / "ocr_stage2_source_policy_entry_009.json", res.get("source_policy_scan"))
    _write_json(out_root / "ocr_stage2_provider_manifest_scan_009.json", res.get("provider_manifest_scan"))
    _write_json(out_root / "ocr_stage2_raw_text_candidate_schema_contract_009.json", res.get("raw_text_candidate_schema_contract"))
    _write_json(out_root / "ocr_stage2_fallback_policy_readiness_009.json", res.get("fallback_policy_readiness"))
    _write_json(out_root / "ocr_stage2_request_trace_trw_contract_009.json", res.get("request_trace_trw_contract"))

    notes = "\n".join(
        [
            "# OCR Stage-2 Static Config Validation v0 (Phase-009)",
            "",
            f"- **output_root:** `{str(out_root)}`",
            f"- **static_validation_result:** `{res.get('static_validation_result')}`",
            "",
            "## Hard boundary",
            "",
            "- provider_invoked=false",
            "- semantic_interpretation_enabled=false",
            "- midplatform/scene_delta/world_context all false",
            "",
        ]
    )
    (out_root / "static_validation_notes.md").write_text(notes + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out_root), "static_validation_result": res.get("static_validation_result")}, ensure_ascii=False))
    return 0 if res.get("static_validation_result") in {"GO", "CONDITIONAL_GO"} else 2


if __name__ == "__main__":
    raise SystemExit(main())

