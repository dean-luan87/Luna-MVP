#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-008 — Run OCR Stage-2 dry-run precheck v0.

Outputs a precheck bundle without invoking any OCR provider.
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

from capabilities.guarded_trial.ocr_stage2_trial_precheck_v0 import (  # noqa: E402
    OcrStage2TrialPrecheckInput,
    run_ocr_stage2_trial_precheck_v0,
)
from capabilities.guarded_trial.ocr_stage2_trial_runner_skeleton_v0 import (  # noqa: E402
    run_ocr_stage2_trial_runner_skeleton_v0,
)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yolo-closure-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    out_root = Path(args.output_root)
    if not out_root.is_absolute():
        out_root = Path(REPO_ROOT) / str(args.output_root)
    out_root = out_root.resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    request_trace_dir = out_root / "request_trace"
    trw_dir = out_root / "trw"

    # Minimal TRW payload for precheck-only run
    trw_payload: Dict[str, Any] = {
        "request_id": f"ocr_stage2_precheck_{_now_iso()}",
        "source_run_id": "run_ocr_stage2_trial_precheck_v0",
        "pending_ref": True,
        "hard_audit": {
            "shadow_only": True,
            "real_runtime_activation": False,
            "provider_invoked": False,
            "semantic_interpretation_enabled": False,
        },
    }

    inp = OcrStage2TrialPrecheckInput(
        yolo_closure_root=str(args.yolo_closure_root),
        output_root=str(out_root),
        request_trace_dir=str(request_trace_dir),
        trace_replay_whitebox_dir=str(trw_dir),
        trw_payload=trw_payload,
        env_override=None,
    )

    res, artifacts = run_ocr_stage2_trial_precheck_v0(inp)
    runner = run_ocr_stage2_trial_runner_skeleton_v0(trial_id=res.trial_id)

    # Write all requested artifacts
    _write_json(out_root / "ocr_stage2_trial_precheck_summary.json", {"phase": "Phase-Mainline-GuardedTrial-008", "ok": True, "output_root": str(out_root)})
    _write_json(out_root / "ocr_stage2_trial_env_snapshot.json", artifacts.get("env_snapshot"))
    _write_json(out_root / "ocr_stage2_trial_precheck_result.json", res.to_dict())
    _write_json(out_root / "ocr_stage2_trial_runner_skeleton.json", runner)
    _write_json(out_root / "ocr_stage2_source_policy_readiness.json", artifacts.get("source_policy_readiness"))
    _write_json(out_root / "ocr_stage2_provider_readiness_static.json", artifacts.get("provider_readiness_static"))
    _write_json(out_root / "ocr_stage2_raw_text_candidate_schema_validation.json", artifacts.get("raw_text_candidate_schema_validation"))
    _write_json(out_root / "ocr_stage2_abort_rollback_plan.json", artifacts.get("rollback_plan"))

    # The trace/replay/whitebox jsonl files are written by capability into trw_dir; copy refs into root for convenience.
    notes = "\n".join(
        [
            "# OCR Stage-2 dry-run precheck v0",
            "",
            f"- **yolo_closure_root:** `{os.path.abspath(args.yolo_closure_root)}`",
            f"- **output_root:** `{str(out_root)}`",
            f"- **trial_id:** `{res.trial_id}`",
            f"- **precheck_result:** `{res.precheck_result}`",
            "",
            "## Hard boundary",
            "",
            "- provider_invoked=false",
            "- semantic_interpretation_enabled=false",
            "- midplatform/scene_delta/world_context all false",
            "",
        ]
    )
    (out_root / "precheck_notes.md").write_text(notes + "\n", encoding="utf-8")

    # Convenience copies
    for name in ("ocr_stage2_trial_trace.jsonl", "ocr_stage2_trial_replay.jsonl", "ocr_stage2_trial_whitebox.jsonl"):
        src = trw_dir / name
        dst = out_root / name
        if src.is_file():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out_root), "trial_id": res.trial_id, "precheck_result": res.precheck_result}, ensure_ascii=False))
    return 0 if res.precheck_result in {"GO", "CONDITIONAL_GO"} else 2


if __name__ == "__main__":
    raise SystemExit(main())

