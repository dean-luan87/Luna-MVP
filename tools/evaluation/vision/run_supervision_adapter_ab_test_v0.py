#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-Supervision-Adapter-AB-Test-001 — evaluation-only A/B (no mainline)."""

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
    ap.add_argument("--supervision-structure-reference-root", default="")
    ap.add_argument("--vision-detection-schema-alignment-root", default="")
    ap.add_argument("--rule-stub-roi-root", default="")
    ap.add_argument("--external-supervision-experiment-root", default="")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    defaults = {
        "sup": WS_ROOT / "_eval_out/supervision_structure_reference_analysis_smoke_v0",
        "schema": WS_ROOT / "_eval_out/vision_detection_evidence_schema_alignment_smoke_v0",
        "stub": WS_ROOT / "_eval_out/vision_roi_proposal_stub_smoke_v0",
        "exp": WS_ROOT / "_eval_out/external_supervision_adapter_experiment_smoke_v0_after_install",
    }

    def _root(arg: str, default_key: str, cli_label: str) -> Path:
        if arg.strip():
            p = Path(arg).expanduser()
            if not p.is_absolute():
                p = (WS_ROOT / p).resolve()
            return _require_abs(str(p), f"--{cli_label}")
        return _require_abs(str(defaults[default_key]), f"default {default_key}")

    sup_root = _root(args.supervision_structure_reference_root, "sup", "supervision-structure-reference-root")
    schema_root = _root(args.vision_detection_schema_alignment_root, "schema", "vision-detection-schema-alignment-root")
    stub_root = _root(args.rule_stub_roi_root, "stub", "rule-stub-roi-root")
    exp_root = _root(args.external_supervision_experiment_root, "exp", "external-supervision-experiment-root")

    from capabilities.vision_runtime.supervision_adapter_ab_test_v0 import run_supervision_adapter_ab_test_v0

    summary, input_summary, fixture, comparison, score_report, risk, audit, errs = run_supervision_adapter_ab_test_v0(
        supervision_structure_reference_root=str(sup_root),
        vision_detection_schema_alignment_root=str(schema_root),
        rule_stub_roi_root=str(stub_root),
        external_supervision_experiment_root=str(exp_root),
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "supervision_adapter_ab_test_summary.json", summary)
    _write_json(out / "supervision_adapter_ab_input_summary.json", input_summary)
    _write_json(out / "supervision_synthetic_to_vision_detection_fixture.json", fixture)
    _write_json(out / "supervision_adapter_ab_comparison_matrix.json", comparison)
    _write_json(out / "supervision_adapter_structure_score_report.json", score_report)
    _write_json(out / "supervision_adapter_ab_risk_report.json", risk)
    _write_json(out / "supervision_adapter_ab_audit_report.json", audit)

    (out / "supervision_adapter_ab_notes.md").write_text(
        "# Phase-Vision-Supervision-Adapter-AB-Test-001\n\n"
        "Evaluation-only A/B: **rule_stub** ROI vs **supervision_synthetic_adapter** converted to "
        "`vision_detection_evidence_v0`. No mainline, no YOLO, no fact writes.\n",
        encoding="utf-8",
    )

    if errs:
        _write_json(out / "supervision_adapter_ab_blocking_errors.json", {"errors": errs})

    ok = not errs
    print(
        json.dumps(
            {
                "supervision_adapter_ab_test_smoke_root": str(out),
                "supervision_roi_count": summary.get("supervision_roi_count"),
                "rule_stub_roi_count": summary.get("rule_stub_roi_count"),
                "status": "success" if ok else "blocking_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
