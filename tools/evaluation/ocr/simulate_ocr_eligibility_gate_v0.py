#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-007 — OCR eligibility gate simulator CLI v0 (Evaluation Tools).

Reads OCR-006b boundary eval artifacts; does NOT invoke OCR providers or change runtime routing.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Set

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.evaluation.ocr.ocr_eligibility_gate_simulator_v0 import (  # noqa: E402
    build_distortion_prevention_report_v0,
    build_ocr_evidence_routing_pack_v0,
    compute_eligibility_accuracy_after_gate_v0,
    compute_false_text_risk_after_gate_v0,
    load_sample_matrix_v0,
    simulate_ocr_eligibility_gate_v0,
)


def _utc_stamp() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).strftime("%Y%m%d_%H%M%SZ")


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _as_set(x: Any) -> Set[str]:
    if isinstance(x, list):
        return {str(v) for v in x}
    return set()


def _load_json_optional(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description="OCR eligibility gate simulator v0 (evaluation-only).")
    ap.add_argument("--boundary-eval-root", required=True, help="OCR-006 boundary eval output directory.")
    ap.add_argument("--dataset-root", required=True, help="OCR-006 dataset root (manifest sanity only).")
    ap.add_argument(
        "--output-root",
        default="",
        help="Absolute output directory. Default: LunaRuntime/logs/.../ocr_eligibility_gate_sim_007_<UTC> under home if writable.",
    )
    args = ap.parse_args()

    boundary_root = _require_abs(args.boundary_eval_root, "--boundary-eval-root")
    dataset_root = _require_abs(args.dataset_root, "--dataset-root")

    if args.output_root.strip():
        out_root = _require_abs(args.output_root, "--output-root")
    else:
        base = Path.home() / "LunaRuntime" / "logs" / "evaluation"
        out_root = (base / f"ocr_eligibility_gate_sim_007_{_utc_stamp()}").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    before_false = _load_json_optional(boundary_root / "ocr_false_text_risk_report.json")
    before_elig = _load_json_optional(boundary_root / "ocr_eligibility_accuracy_report.json")

    decisions, bm = simulate_ocr_eligibility_gate_v0(
        boundary_eval_root=boundary_root,
        dataset_root=dataset_root,
    )
    eligible_types = _as_set(bm.get("ocr_eligible_content_types"))
    conditional_types = _as_set(bm.get("conditional_ocr_content_types"))
    non_ocr_types = _as_set(bm.get("non_ocr_content_types"))

    routing_pack_id = f"ocr_evidence_routing_{uuid.uuid4().hex[:12]}"
    pack = build_ocr_evidence_routing_pack_v0(
        routing_pack_id=routing_pack_id,
        source_eval_root=str(boundary_root),
        decisions=decisions,
    )

    samples = load_sample_matrix_v0(boundary_root)
    false_after = compute_false_text_risk_after_gate_v0(
        pack=pack,
        before_report=before_false or {"false_text_risk_rate": None},
        non_ocr_types=non_ocr_types,
        all_samples=samples,
    )
    elig_after, confusion = compute_eligibility_accuracy_after_gate_v0(
        decisions=decisions,
        samples=samples,
        before_accuracy_report=before_elig or {"eligibility_accuracy": None},
        eligible_types=eligible_types,
        conditional_types=conditional_types,
        non_ocr_types=non_ocr_types,
    )
    distortion = build_distortion_prevention_report_v0(
        pack=pack,
        decisions=decisions,
        non_ocr_types=non_ocr_types,
        conditional_types=conditional_types,
        samples=samples,
    )

    # Sample matrix: merge gate output into each row (by case_id)
    by_id = {str(d.get("case_id")): d for d in decisions}
    route_matrix: List[Dict[str, Any]] = []
    for s in samples:
        cid = str(s.get("case_id") or s.get("sample_id") or "")
        d = by_id.get(cid) or {}
        row = dict(s)
        row["gate_evidence_route"] = d.get("evidence_route")
        row["gate_should_enter_fact_text_layer"] = d.get("should_enter_fact_text_layer")
        row["gate_uncertainty"] = d.get("uncertainty")
        row["gate_source_metrics"] = d.get("source_metrics")
        route_matrix.append(row)

    trace_path = out_root / "ocr_eligibility_gate_trace.jsonl"
    replay_path = out_root / "ocr_eligibility_gate_replay.jsonl"
    if trace_path.is_file():
        trace_path.unlink()
    if replay_path.is_file():
        replay_path.unlink()

    ts = _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    for d in decisions:
        _append_jsonl(
            trace_path,
            {
                "ts": ts,
                "phase": "Phase-EvaluationTools-OCR-007",
                "case_id": d.get("case_id"),
                "content_type": d.get("content_type"),
                "evidence_route": d.get("evidence_route"),
                "should_enter_fact_text_layer": d.get("should_enter_fact_text_layer"),
                "uncertainty": d.get("uncertainty"),
                "source_metrics": d.get("source_metrics"),
            },
        )
        _append_jsonl(
            replay_path,
            {
                "case_id": d.get("case_id"),
                "evidence_route": d.get("evidence_route"),
                "should_enter_fact_text_layer": d.get("should_enter_fact_text_layer"),
            },
        )

    summary = {
        "phase": "Phase-EvaluationTools-OCR-007",
        "gate_version": "ocr_eligibility_gate_simulator_v0",
        "boundary_eval_root": str(boundary_root),
        "dataset_root": str(dataset_root),
        "output_root": str(out_root),
        "routing_pack_id": routing_pack_id,
        "total_decisions": len(decisions),
        "pack_summary": pack.get("summary"),
        "false_text_risk_after": false_after.get("false_text_risk_after"),
        "eligibility_accuracy_after": elig_after.get("eligibility_accuracy_after"),
        "distortion_prevention_passed": distortion.get("distortion_prevention_passed"),
        "hard_audit": {
            "runtime_integration": False,
            "whitebox_integration": False,
            "mainline_side_effect": False,
            "ocr_provider_invocation": False,
        },
        "notes": "Evaluation-only simulator; not runtime OCR router behavior.",
    }

    _write_json(out_root / "ocr_eligibility_gate_summary.json", summary)
    _write_json(out_root / "ocr_evidence_routing_pack.json", pack)
    _write_json(out_root / "ocr_evidence_route_sample_matrix.json", route_matrix)
    _write_json(out_root / "ocr_false_text_risk_after_gate_report.json", false_after)
    _write_json(out_root / "ocr_eligibility_accuracy_after_gate_report.json", elig_after)
    _write_json(out_root / "ocr_distortion_prevention_report.json", distortion)
    _write_json(out_root / "ocr_route_confusion_matrix.json", {"matrix": confusion, "evaluated_with": "compute_eligibility_accuracy_after_gate_v0"})

    notes = out_root / "eligibility_gate_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# OCR Eligibility Gate Simulation (v0)",
                "",
                f"- **boundary_eval_root**: `{boundary_root}`",
                f"- **dataset_root**: `{dataset_root}`",
                f"- **output_root**: `{out_root}`",
                "",
                "## Outputs",
                "",
                "- `ocr_evidence_routing_pack.json` — six-way evidence routing (evaluation schema).",
                "- `ocr_false_text_risk_after_gate_report.json` — non-OCR → eligible_text proxy risk after gate.",
                "- `ocr_eligibility_accuracy_after_gate_report.json` — routing expectation proxy (not runtime truth).",
                "- `ocr_distortion_prevention_report.json` — static distortion rule checks on pack + samples.",
                "",
                "## Boundaries",
                "",
                "- No OCR provider calls; no runtime / whitebox / mainline side effects.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out_root), "routing_pack_id": routing_pack_id}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
