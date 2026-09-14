#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-Supervision-Structure-Reference-Analysis-001 — structure reference only."""

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
        "--supervision-experiment-root",
        default="",
        help="Directory with external_supervision_availability_probe.json",
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    default_exp = Path(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/external_supervision_adapter_experiment_smoke_v0_after_install"
    )
    exp = Path(args.supervision_experiment_root).expanduser() if args.supervision_experiment_root.strip() else default_exp
    if not exp.is_absolute():
        exp = (WS_ROOT / exp).resolve()
    exp_root = _require_abs(str(exp), "--supervision-experiment-root (resolved)")

    from capabilities.vision_runtime.supervision_structure_reference_analysis_v0 import (
        run_supervision_structure_reference_analysis_v0,
    )

    summary, capability, mapping, reuse, risk, adoption, ab_plan, audit, errs = (
        run_supervision_structure_reference_analysis_v0(supervision_experiment_root=str(exp_root))
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "supervision_structure_reference_summary.json", summary)
    _write_json(out / "supervision_capability_structure_report.json", capability)
    _write_json(out / "supervision_to_luna_mapping_matrix.json", mapping)
    _write_json(out / "supervision_reuse_classification_report.json", reuse)
    _write_json(out / "supervision_architecture_risk_report.json", risk)
    _write_json(out / "supervision_recommended_adoption_plan.json", adoption)
    _write_json(out / "supervision_ab_test_plan.json", ab_plan)
    _write_json(out / "supervision_structure_reference_audit.json", audit)

    (out / "supervision_structure_reference_notes.md").write_text(
        "# Phase-Vision-Supervision-Structure-Reference-Analysis-001\n\n"
        "Structural reference analysis of **Roboflow Supervision** vs Luna Vision evidence models. "
        "**No** mainline integration, **no** YOLO, **no** real detector, **no** navigation, **no** fact writes.\n",
        encoding="utf-8",
    )

    if errs:
        _write_json(out / "supervision_structure_reference_blocking_errors.json", {"errors": errs})

    ok = not errs
    print(
        json.dumps(
            {
                "supervision_structure_reference_smoke_root": str(out),
                "supervision_version": summary.get("supervision_version"),
                "status": "success" if ok else "blocking_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
