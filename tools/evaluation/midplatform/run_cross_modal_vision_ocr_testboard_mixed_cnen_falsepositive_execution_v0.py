#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-MixedCNEN-FalsePositive-Execution-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if (parent / "_eval_out").is_dir():
                return parent
            sibling = parent.parent / "Luna-Workspace-Min"
            if (sibling / "_eval_out").is_dir():
                return sibling
            return parent
    return here.parents[3]


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


def _prepare_governance(ws: Path, out: Path, gov_arg: str) -> Path:
    gov_src = (
        Path(gov_arg).expanduser()
        if gov_arg.strip()
        else (ws / "configs/ocr/ocr_image_input_governance_lightweight_normalized_smoke_v0.example.json")
    )
    if not gov_src.is_absolute():
        gov_src = (ws / gov_src).resolve()
    gov = out / "mixed_cnen_falsepositive_governance.json"
    if gov_src.is_file():
        gov.write_text(gov_src.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        fallback = ws / "configs/ocr/ocr_image_input_governance_v0.example.json"
        gov.write_text(fallback.read_text(encoding="utf-8"), encoding="utf-8")
    return _require_abs(str(gov), "governance")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--testboard-expansion-root", required=True)
    ap.add_argument("--full-chain-5cases-root", required=True)
    ap.add_argument("--lowquality-partial-root", required=True)
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument("--governance-config", default="")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    ws = _require_abs(args.workspace_root, "--workspace-root")
    tb = _require_abs(args.testboard_expansion_root, "--testboard-expansion-root")
    fc5 = _require_abs(args.full_chain_5cases_root, "--full-chain-5cases-root")
    lp = _require_abs(args.lowquality_partial_root, "--lowquality-partial-root")
    gov = _prepare_governance(ws, out, args.governance_config)

    from capabilities.midplatform.cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_execution_v0 import (
        run_cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_execution_v0,
    )

    (
        summary,
        fixture_doc,
        execution_doc,
        planned_doc,
        expected_doc,
        risk_report,
        boundary_doc,
        audit,
        errs,
    ) = run_cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_execution_v0(
        testboard_expansion_root=str(tb),
        full_chain_5cases_root=str(fc5),
        lowquality_partial_root=str(lp),
        workspace_root=ws,
        governance_config_path=gov,
        work_root=out,
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_fixture_report.json", fixture_doc)
    _write_json(
        out / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_case_execution_matrix.json",
        execution_doc,
    )
    _write_json(
        out / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_planned_only_matrix.json",
        planned_doc,
    )
    _write_json(
        out / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_expected_vs_observed_report.json",
        expected_doc,
    )
    _write_json(out / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_risk_report.json", risk_report)
    _write_json(out / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_boundary_matrix.json", boundary_doc)
    _write_json(out / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_audit_report.json", audit)
    (out / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_notes.md").write_text(
        "\n".join(
            [
                "# CrossModal Vision OCR TestBoard Mixed CN/EN + False Positive Execution",
                "",
                f"- executed_case_count: {summary.get('executed_case_count')}",
                f"- planned_only_case_count: {summary.get('planned_only_case_count')}",
                "",
                "No translation, no semantic interpretation, no confirmed sign; evaluation-only.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "executed_case_count": summary.get("executed_case_count"),
                "planned_only_case_count": summary.get("planned_only_case_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
