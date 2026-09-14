#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-VisionDetectionEvidence-Schema-Alignment-001 — static schema alignment only."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WS_ROOT = Path(__file__).resolve().parents[3]
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
    ap.add_argument(
        "--supervision-structure-reference-root",
        default="",
    )
    ap.add_argument(
        "--vision-evidence-pack-root",
        default="",
    )
    ap.add_argument("--stub-fixture-max-items", type=int, default=5)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    default_sup = Path(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/supervision_structure_reference_analysis_smoke_v0"
    )
    default_pack = Path(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_recognition_evidence_pack_stub_smoke_v0"
    )

    sup = Path(args.supervision_structure_reference_root).expanduser() if args.supervision_structure_reference_root.strip() else default_sup
    pack = Path(args.vision_evidence_pack_root).expanduser() if args.vision_evidence_pack_root.strip() else default_pack
    if not sup.is_absolute():
        sup = (WS_ROOT / sup).resolve()
    if not pack.is_absolute():
        pack = (WS_ROOT / pack).resolve()

    sup_root = _require_abs(str(sup), "--supervision-structure-reference-root (resolved)")
    pack_root = _require_abs(str(pack), "--vision-evidence-pack-root (resolved)")

    from capabilities.vision_runtime.vision_detection_evidence_schema_alignment_v0 import (
        run_vision_detection_evidence_schema_alignment_v0,
    )

    summary, schema_doc, example, stub_fixture, mapping, boundary, audit, errs = (
        run_vision_detection_evidence_schema_alignment_v0(
            supervision_structure_reference_root=str(sup_root),
            vision_recognition_evidence_pack_root=str(pack_root),
            stub_fixture_max_items=int(args.stub_fixture_max_items),
        )
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "vision_detection_evidence_schema_alignment_summary.json", summary)
    _write_json(out / "vision_detection_evidence_schema_v0.json", schema_doc)
    _write_json(out / "vision_detection_evidence_schema_example.json", example)
    _write_json(out / "vision_detection_evidence_stub_compat_fixture.json", stub_fixture)
    _write_json(out / "vision_detection_evidence_supervision_mapping_matrix.json", mapping)
    _write_json(out / "vision_detection_evidence_boundary_report.json", boundary)
    _write_json(out / "vision_detection_evidence_schema_alignment_audit_report.json", audit)

    (out / "vision_detection_evidence_schema_alignment_notes.md").write_text(
        "# Phase-VisionDetectionEvidence-Schema-Alignment-001\n\n"
        "Defines **`vision_detection_evidence_v0`** and Supervision Detections → Luna mapping. "
        "Static only — **no** Supervision mainline, **no** YOLO, **no** writes.\n",
        encoding="utf-8",
    )

    if errs:
        _write_json(out / "vision_detection_evidence_schema_alignment_blocking_errors.json", {"errors": errs})

    ok = not errs
    print(
        json.dumps(
            {
                "vision_detection_evidence_schema_alignment_smoke_root": str(out),
                "schema_version": summary.get("vision_detection_evidence_schema_version"),
                "status": "success" if ok else "blocking_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
