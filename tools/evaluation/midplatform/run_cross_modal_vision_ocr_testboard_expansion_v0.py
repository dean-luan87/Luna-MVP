#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-Expansion-001 runner."""

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
    gov = out / "testboard_governance.json"
    if gov_src.is_file():
        gov.write_text(gov_src.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        fallback = ws / "configs/ocr/ocr_image_input_governance_v0.example.json"
        gov.write_text(fallback.read_text(encoding="utf-8"), encoding="utf-8")
    return _require_abs(str(gov), "governance")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument("--governance-config", default="")
    ap.add_argument(
        "--chain-closure-root",
        default=str(WS_ROOT / "_eval_out/cross_modal_vision_ocr_chain_closure_smoke_v0"),
    )
    ap.add_argument(
        "--text-bearing-sample-root",
        default=str(WS_ROOT / "_eval_out/vision_roi_text_bearing_ocr_sample_smoke_v0"),
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    ws = _require_abs(args.workspace_root, "--workspace-root")
    gov = _prepare_governance(ws, out, args.governance_config)

    from capabilities.midplatform.cross_modal_vision_ocr_testboard_expansion_v0 import (
        run_cross_modal_vision_ocr_testboard_expansion_v0,
    )

    summary, registry, fixture_manifest, expected_doc, boundary_doc, execution_doc, audit, errs = (
        run_cross_modal_vision_ocr_testboard_expansion_v0(
            output_work_root=out,
            workspace_root=ws,
            governance_config_path=gov,
            chain_closure_root=str(_require_abs(args.chain_closure_root, "--chain-closure-root")),
            text_bearing_sample_root=str(_require_abs(args.text_bearing_sample_root, "--text-bearing-sample-root")),
        )
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "cross_modal_vision_ocr_testboard_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_testboard_registry.json", registry)
    _write_json(out / "cross_modal_vision_ocr_testboard_fixture_manifest.json", fixture_manifest)
    _write_json(out / "cross_modal_vision_ocr_testboard_expected_behavior_matrix.json", expected_doc)
    _write_json(out / "cross_modal_vision_ocr_testboard_boundary_matrix.json", boundary_doc)
    _write_json(out / "cross_modal_vision_ocr_testboard_case_execution_matrix.json", execution_doc)
    _write_json(out / "cross_modal_vision_ocr_testboard_audit_report.json", audit)
    (out / "cross_modal_vision_ocr_testboard_notes.md").write_text(
        "\n".join(
            [
                "# CrossModal Vision OCR TestBoard Expansion",
                "",
                f"- testboard_id: {summary.get('testboard_id')}",
                f"- case_count: {summary.get('case_count')}",
                f"- executed: {summary.get('executed_case_count')} / planned: {summary.get('planned_case_count')}",
                "",
                "Evaluation-only TestBoard; no writes; no executor.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "case_count": summary.get("case_count"),
                "executed_case_count": summary.get("executed_case_count"),
                "planned_case_count": summary.get("planned_case_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
