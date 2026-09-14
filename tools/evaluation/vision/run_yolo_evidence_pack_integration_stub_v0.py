#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-YOLO-Evidence-Pack-Integration-Stub-001 — YOLO evidence pack integration."""

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
    ap.add_argument("--yolo-positive-sample-root", default="")
    ap.add_argument("--vision-recognition-evidence-pack-stub-root", default="")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    default_yolo = WS_ROOT / "_eval_out/yolo_real_positive_sample_smoke_v0"
    default_stub = WS_ROOT / "_eval_out/vision_recognition_evidence_pack_stub_smoke_v0"

    def _root(arg: str, default: Path, cli_label: str) -> Path:
        if arg.strip():
            p = Path(arg).expanduser()
            if not p.is_absolute():
                p = (WS_ROOT / p).resolve()
            return _require_abs(str(p), f"--{cli_label}")
        return _require_abs(str(default), f"default {cli_label}")

    yolo_root = _root(args.yolo_positive_sample_root, default_yolo, "yolo-positive-sample-root")
    stub_root = _root(
        args.vision_recognition_evidence_pack_stub_root,
        default_stub,
        "vision-recognition-evidence-pack-stub-root",
    )

    from capabilities.vision_runtime.yolo_evidence_pack_integration_stub_v0 import (
        run_yolo_evidence_pack_integration_stub_v0,
    )

    summary, pack, matrix, provider, consumer, risk, audit, errs = run_yolo_evidence_pack_integration_stub_v0(
        yolo_positive_sample_root=str(yolo_root),
        vision_recognition_evidence_pack_stub_root=str(stub_root),
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "yolo_evidence_pack_integration_summary.json", summary)
    _write_json(out / "yolo_vision_recognition_evidence_pack.json", pack)
    _write_json(out / "yolo_vision_recognition_evidence_matrix.json", matrix)
    _write_json(out / "yolo_provider_summary.json", provider)
    _write_json(out / "yolo_evidence_consumer_compatibility_report.json", consumer)
    _write_json(out / "yolo_evidence_pack_risk_report.json", risk)
    _write_json(out / "yolo_evidence_pack_audit_report.json", audit)

    (out / "yolo_evidence_pack_notes.md").write_text(
        "# Phase-Vision-YOLO-Evidence-Pack-Integration-Stub-001\n\n"
        "Integrates real YOLO **VisionDetectionEvidence** into "
        "`vision_recognition_evidence_pack_v0` (evaluation-only, not_fact).\n",
        encoding="utf-8",
    )

    if errs and summary.get("phase_verdict_hint") == "NO_GO":
        _write_json(out / "yolo_evidence_pack_blocking_errors.json", {"errors": errs})

    ok = summary.get("phase_verdict_hint") != "NO_GO"
    print(
        json.dumps(
            {
                "yolo_evidence_pack_integration_root": str(out),
                "evidence_count": summary.get("evidence_count"),
                "consumer_compatible": summary.get("consumer_compatible"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "status": "success" if ok else "blocking_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
