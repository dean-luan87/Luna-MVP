#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-Gated-YOLO-Real-Smoke-001 — gated real YOLO evaluation-only smoke."""

from __future__ import annotations

import argparse
import json
import os
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


def _enforce_real_smoke_env() -> None:
    os.environ["LUNA_YOLO_EVAL_ONLY"] = "true"
    os.environ["LUNA_ENABLE_YOLO_EVAL_PROVIDER_V0"] = "true"
    os.environ["LUNA_YOLO_FORCE_FIXTURE_V0"] = "false"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--roi-proposal-root", default="")
    ap.add_argument("--yolo-candidate-adapter-root", default="")
    args = ap.parse_args()

    _enforce_real_smoke_env()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    default_roi = WS_ROOT / "_eval_out/vision_roi_proposal_stub_smoke_v0"
    default_prior = WS_ROOT / "_eval_out/yolo_candidate_adapter_eval_smoke_v0"

    def _root(arg: str, default: Path, cli_label: str) -> Path:
        if arg.strip():
            p = Path(arg).expanduser()
            if not p.is_absolute():
                p = (WS_ROOT / p).resolve()
            return _require_abs(str(p), f"--{cli_label}")
        return _require_abs(str(default), f"default {cli_label}")

    roi_root = _root(args.roi_proposal_root, default_roi, "roi-proposal-root")
    prior_root = _root(args.yolo_candidate_adapter_root, default_prior, "yolo-candidate-adapter-root")

    from capabilities.vision_runtime.yolo_candidate_adapter_v0 import run_yolo_real_smoke_v0

    summary, gate, model_load, selection, raw, matrix, fixture, risk, audit, errs = run_yolo_real_smoke_v0(
        roi_proposal_root=str(roi_root),
        yolo_candidate_adapter_root=str(prior_root),
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "yolo_real_smoke_summary.json", summary)
    _write_json(out / "yolo_real_gate_check.json", gate)
    _write_json(out / "yolo_model_load_report.json", model_load)
    _write_json(out / "yolo_real_input_unit_selection.json", selection)
    _write_json(out / "yolo_real_raw_detector_result_summary.json", raw)
    _write_json(out / "yolo_real_detection_to_vision_evidence_matrix.json", matrix)
    _write_json(out / "yolo_real_vision_detection_evidence_fixture.json", fixture)
    _write_json(out / "yolo_real_smoke_risk_report.json", risk)
    _write_json(out / "yolo_real_smoke_audit_report.json", audit)

    (out / "yolo_real_smoke_notes.md").write_text(
        "# Phase-Vision-Gated-YOLO-Real-Smoke-001\n\n"
        "Gated **real YOLO** smoke: local weights only, **no** network download, "
        "ROI crops → `vision_detection_evidence_v0` (not_fact).\n",
        encoding="utf-8",
    )

    if errs:
        _write_json(out / "yolo_real_smoke_blocking_errors.json", {"errors": errs})

    ok = summary.get("phase_verdict_hint") != "NO_GO"
    print(
        json.dumps(
            {
                "yolo_real_smoke_root": str(out),
                "detector_mode": summary.get("detector_mode"),
                "model_loaded": summary.get("model_loaded"),
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
