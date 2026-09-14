#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-IntegrationPlan-001 — Next-stage integration roadmap (planning only).

Reads StatusReview-001 output; does NOT invoke providers or modify runtime.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
from pathlib import Path
from typing import Any, Dict, List

StatusReviewFiles = (
    "mainline_status_review_summary.json",
    "mainline_phase_status_matrix.json",
)


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _option_comparison_matrix() -> List[Dict[str, Any]]:
    return [
        {
            "id": "A",
            "name": "OCRBridge-Implementation-001 shadow",
            "goal": "OcrEvidencePack shadow serialization binding",
            "constraints": ["no_midplatform_forward", "no_fact_layer", "no_scene_delta_worldcontext"],
            "priority_rank": 3,
        },
        {
            "id": "B",
            "name": "VoiceInteraction-Readiness-001",
            "goal": "Full voice interaction mainline readiness (ASR, multi-turn, Qianwen path, TTS fallback, governance, TRW)",
            "constraints": ["no_full_prod_voice_without_readiness_signoff"],
            "priority_rank": 2,
        },
        {
            "id": "C",
            "name": "PaddleOCR-Readiness-001",
            "goal": "PaddleOCR provider readiness / manifest; Chinese enhancement",
            "constraints": ["do_not_replace_rapidocr_primary", "evaluation_or_shadow_only"],
            "priority_rank": 5,
        },
        {
            "id": "D",
            "name": "EvaluationTools-OCR-RealSamples-001",
            "goal": "Real OCR samples + human labels; tighten OCR-006 boundary credibility",
            "constraints": ["evaluation_only"],
            "priority_rank": 4,
        },
        {
            "id": "E",
            "name": "Mainline-IntegrationPlan-001",
            "goal": "Unify next-stage order across YOLO/OCR/Voice/OCRBridge/EvaluationTools (this phase output)",
            "constraints": ["planning_only"],
            "priority_rank": 1,
        },
    ]


def _dependency_matrix() -> List[Dict[str, Any]]:
    return [
        {"from": "E", "to": "B", "relation": "recommended_prerequisite", "note": "Lock execution order before voice gap work."},
        {"from": "E", "to": "A", "relation": "recommended_prerequisite", "note": "Defer OCRBridge shadow until MidPlatform receive strategy exists."},
        {"from": "B", "to": "A", "relation": "soft_order", "note": "Voice readiness may proceed in parallel design but A stays after B per default policy."},
        {"from": "MidPlatform_receive_OcrEvidencePack", "to": "A", "relation": "hard_prerequisite_for_forwarding", "note": "Real MidPlatform ingest is out of scope; shadow A does not require it but forward does."},
        {"from": "D", "to": "OCR-006", "relation": "strengthens", "note": "Parallel-friendly; should not preempt E/B."},
        {"from": "C", "to": "OCR-012", "relation": "must_not_disrupt", "note": "RapidOCR primary remains; Paddle is additive readiness."},
    ]


def _blocked_action_matrix() -> List[Dict[str, Any]]:
    return [
        {"scope": "all_options", "blocked": "invoke_midplatform_production"},
        {"scope": "all_options", "blocked": "invoke_whitebox_without_phase"},
        {"scope": "all_options", "blocked": "modify_ocr_provider_routing"},
        {"scope": "all_options", "blocked": "auto_consume_ocr_as_facts"},
        {"scope": "A", "blocked": "forward_midplatform_before_authorize"},
        {"scope": "A", "blocked": "write_fact_text_layer_without_flag"},
        {"scope": "B", "blocked": "mark_full_voice_done_prematurely"},
        {"scope": "C", "blocked": "replace_rapidocr_as_primary_without_adr"},
        {"scope": "D", "blocked": "promote_eval_samples_to_runtime_router"},
    ]


def _execution_sequence() -> Dict[str, Any]:
    return {
        "default_policy_id": "voice_gap_first_then_bridge_shadow",
        "ordered_phases": [
            {"step": 1, "id": "E", "title": "Mainline-IntegrationPlan-001", "status": "this_document_phase"},
            {"step": 2, "id": "B", "title": "VoiceInteraction-Readiness-001", "rationale": "Largest mainline completeness gap; ASR/multi-turn/Qianwen/TTS governance."},
            {"step": 3, "id": "A", "title": "OCRBridge-Implementation-001 shadow", "rationale": "Design deep; wiring touches MidPlatform story—defer until plan + voice path clearer."},
            {"step": 4, "id": "D", "title": "EvaluationTools-OCR-RealSamples-001", "rationale": "Parallel-friendly; do not preempt E/B resources."},
            {"step": 5, "id": "C", "title": "PaddleOCR-Readiness-001", "rationale": "Enhancement; must not interrupt mainline."},
        ],
        "user_override_note": "Order may change by ADR; semantic: E before B before A is the frozen default recommendation.",
    }


def _next_phase_order_matrix() -> Dict[str, Any]:
    return {
        "columns": ["phase_id", "priority", "do_now", "defer", "preconditions", "acceptance_high_level"],
        "rows": [
            {
                "phase_id": "E",
                "priority": 1,
                "do_now": "Freeze roadmap + execution order + blocked actions",
                "defer": "All implementation",
                "preconditions": ["StatusReview-001 GO"],
                "acceptance_high_level": "Signed roadmap JSON + verifier GO",
            },
            {
                "phase_id": "B",
                "priority": 2,
                "do_now": "Readiness matrix for voice stack",
                "defer": "Full prod voice connection",
                "preconditions": ["E complete", "Output governance docs aligned"],
                "acceptance_high_level": "Readiness GO/NO-GO pack without runtime wire",
            },
            {
                "phase_id": "A",
                "priority": 3,
                "do_now": "Shadow pack serialization binding design",
                "defer": "MidPlatform forward",
                "preconditions": ["RFC-001 frozen", "MidPlatform receive policy phase scheduled"],
                "acceptance_high_level": "Shadow traces + validator; flags default safe",
            },
            {
                "phase_id": "D",
                "priority": 4,
                "do_now": "Dataset/label plan",
                "defer": "Runtime",
                "preconditions": ["OCR-006 baseline"],
                "acceptance_high_level": "Expanded boundary eval with human review package",
            },
            {
                "phase_id": "C",
                "priority": 5,
                "do_now": "Manifest + trial harness plan",
                "defer": "Primary provider swap",
                "preconditions": ["RapidOCR primary stable"],
                "acceptance_high_level": "Readiness doc + offline trial GO",
            },
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status-review-root", required=True, help="Output root of Phase-Mainline-StatusReview-001.")
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    sr = _require_abs(args.status_review_root, "--status-review-root")
    if not sr.is_dir():
        raise SystemExit(f"ERROR: status review root not a directory: {sr}")

    missing = [fn for fn in StatusReviewFiles if not (sr / fn).is_file()]
    if missing:
        raise SystemExit(f"ERROR: status review root missing files: {missing}")

    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / f"mainline_integration_plan_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    status_summary = json.loads((sr / "mainline_status_review_summary.json").read_text(encoding="utf-8"))

    summary = {
        "phase": "Phase-Mainline-IntegrationPlan-001",
        "status_review_input_root": str(sr),
        "integration_plan_output_root": str(out),
        "status_review_verdict_echo": status_summary.get("verdict"),
        "constraints": {
            "implementation_performed": False,
            "provider_invoked": False,
            "runtime_integration": False,
            "midplatform_invocation": False,
            "whitebox_integration": False,
            "ocr_routing_changed": False,
        },
        "recommended_next_phase_after_this_plan": "VoiceInteraction-Readiness-001 (Option B)",
        "verdict": "GO",
    }

    _write_json(out / "mainline_integration_plan_summary.json", summary)
    _write_json(out / "mainline_next_phase_order_matrix.json", _next_phase_order_matrix())
    _write_json(out / "mainline_option_comparison_matrix.json", {"options": _option_comparison_matrix()})
    _write_json(out / "mainline_dependency_matrix.json", {"edges": _dependency_matrix()})
    _write_json(out / "mainline_blocked_action_matrix.json", {"blocked": _blocked_action_matrix()})
    _write_json(out / "mainline_recommended_execution_sequence.json", _execution_sequence())

    notes = out / "mainline_integration_plan_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# Mainline Integration Plan (v0)",
                "",
                f"- **status_review_input_root**: `{sr}`",
                f"- **output_root**: `{out}`",
                "",
                "## Default execution order",
                "",
                "1. **E** — Integration plan (this phase)",
                "2. **B** — Voice interaction readiness",
                "3. **A** — OCRBridge shadow implementation (deferred after B)",
                "4. **D** — Evaluation real samples (parallel-friendly)",
                "5. **C** — PaddleOCR readiness (enhancement last)",
                "",
                "Planning only. No runtime wiring.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "verdict": summary["verdict"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
