#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-Gated-YOLO-Candidate-Adapter-001 — evaluation-only gated YOLO adapter."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    candidates: list[Path] = []
    for parent in here.parents:
        if (parent / "capabilities" / "vision_runtime").is_dir():
            candidates.append(parent)
    for parent in candidates:
        if (parent / "_eval_out").is_dir():
            return parent
        sibling = parent.parent / "Luna-Workspace-Min"
        if (sibling / "_eval_out").is_dir():
            return sibling
    return candidates[0] if candidates else here.parents[3]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--vision-detection-schema-alignment-root", default="")
    ap.add_argument("--roi-proposal-root", default="")
    ap.add_argument("--supervision-ab-root", default="")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    defaults = {
        "schema": WS_ROOT / "_eval_out/vision_detection_evidence_schema_alignment_smoke_v0",
        "roi": WS_ROOT / "_eval_out/vision_roi_proposal_stub_smoke_v0",
        "ab": WS_ROOT / "_eval_out/supervision_adapter_ab_test_smoke_v0",
    }

    def _root(arg: str, key: str, cli_label: str) -> Path:
        if arg.strip():
            p = Path(arg).expanduser()
            if not p.is_absolute():
                p = (WS_ROOT / p).resolve()
            return _require_abs(str(p), f"--{cli_label}")
        return _require_abs(str(defaults[key]), f"default {key}")

    schema_root = _root(args.vision_detection_schema_alignment_root, "schema", "vision-detection-schema-alignment-root")
    roi_root = _root(args.roi_proposal_root, "roi", "roi-proposal-root")
    ab_root = _root(args.supervision_ab_root, "ab", "supervision-ab-root") if args.supervision_ab_root.strip() else defaults["ab"]

    from capabilities.vision_runtime.yolo_candidate_adapter_v0 import run_yolo_candidate_adapter_eval_v0

    summary, probe, selection, raw, matrix, fixture, report, risk, audit, errs = run_yolo_candidate_adapter_eval_v0(
        vision_detection_schema_alignment_root=str(schema_root),
        roi_proposal_root=str(roi_root),
        supervision_ab_root=str(ab_root),
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "yolo_candidate_adapter_eval_summary.json", summary)
    _write_json(out / "yolo_availability_probe.json", probe)
    _write_json(out / "yolo_input_unit_selection.json", selection)
    _write_json(out / "yolo_raw_detector_result_summary.json", raw)
    _write_json(out / "yolo_detection_to_vision_evidence_matrix.json", matrix)
    _write_json(out / "yolo_vision_detection_evidence_fixture.json", fixture)
    _write_json(out / "yolo_candidate_adapter_report.json", report)
    _write_json(out / "yolo_candidate_adapter_risk_report.json", risk)
    _write_json(out / "yolo_candidate_adapter_audit_report.json", audit)

    (out / "yolo_candidate_adapter_notes.md").write_text(
        "# Phase-Vision-Gated-YOLO-Candidate-Adapter-001\n\n"
        "Gated **YOLO candidate adapter** evaluation: ROI units → "
        "`vision_detection_evidence_v0`. **Not** mainline; **not** fact writes.\n",
        encoding="utf-8",
    )

    if errs:
        _write_json(out / "yolo_candidate_adapter_blocking_errors.json", {"errors": errs})

    ok = not errs
    print(
        json.dumps(
            {
                "yolo_candidate_adapter_eval_smoke_root": str(out),
                "detector_mode": summary.get("detector_mode"),
                "converted_evidence_count": summary.get("converted_evidence_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "status": "success" if ok else "blocking_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
