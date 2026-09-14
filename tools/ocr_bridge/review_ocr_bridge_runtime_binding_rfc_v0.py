#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCRBridge-Implementation-RFC-001 — Read-only RFC completeness check + matrix export.

Does not modify runtime implementation modules; writes only --output-root artifacts.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

RFC_DOCS = [
    "LUNA_OCR_BRIDGE_RUNTIME_BINDING_RFC_V0.md",
    "LUNA_OCR_BRIDGE_RUNTIME_SOURCE_REF_PLAN_V0.md",
    "LUNA_OCR_BRIDGE_RUNTIME_FLAG_AND_KILL_SWITCH_POLICY_V0.md",
    "LUNA_OCR_BRIDGE_SHADOW_ONLY_WIRING_STRATEGY_V0.md",
    "LUNA_OCR_BRIDGE_ABORT_ROLLBACK_POLICY_V0.md",
    "LUNA_OCR_BRIDGE_IMPLEMENTATION_RFC_GO_NO_GO_PACK_V0.md",
]


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _binding_candidate_matrix() -> Dict[str, Any]:
    return {
        "categories": [
            {
                "id": "provider_invocation",
                "candidates": [
                    "capabilities/guarded_trial/ocr_stage2_controlled_provider_executor_v0.py",
                    "capabilities/model_ocr/rapidocr_adapter_v0.py",
                    "capabilities/model_ocr/rapidocr_variant_adapter_v0.py",
                ],
                "outputs": ["raw_text_candidate", "provider_payload", "bbox", "confidence", "layout_fields"],
            },
            {
                "id": "layout_symbol_glyph_governance",
                "candidates": ["capabilities/guarded_trial/ocr_layout_symbol_governance_v0.py"],
                "outputs": [
                    "visual_symbol_candidates",
                    "visual_glyph_candidates",
                    "layout_groups",
                    "reading_order_candidates",
                ],
            },
            {
                "id": "input_quality_gate",
                "candidates": ["capabilities/evaluation/ocr/ocr_input_image_quality_gate_v0.py"],
                "outputs": ["image_quality_gate", "blur", "contrast", "text_scale", "skew", "preprocess_suggestion"],
            },
            {
                "id": "eligibility_gate",
                "candidates": [
                    "capabilities/evaluation/ocr/ocr_eligibility_gate_simulator_v0.py (design/eval only)",
                    "future:runtime_eligibility_module_TBD",
                ],
                "outputs": ["eligible_text_evidence", "conditional_text_evidence", "rejected_or_uncertain_evidence"],
            },
            {
                "id": "request_trace_trw",
                "candidates": ["capabilities/core_trw (RequestTrace stages)", "tools/export_* observability (TBD wiring)"],
                "outputs": ["trace_ref", "replay_ref", "audit_ref", "request_id", "trace_id", "session_id"],
            },
        ],
        "notes": "Inventory only; no code changes in RFC phase.",
    }


def _source_ref_plan_matrix() -> Dict[str, Any]:
    refs = [
        ("image_frame_ref", "unified_frame_or_buffer_id", "must_be_replayable"),
        ("crop_or_roi_ref", "ocr_input_roi_or_full_frame_roi", "no_forge"),
        ("ocr_provider_invocation_ref", "stage2_or_adapter_invocation_record", "no_forge"),
        ("raw_candidate_ref", "raw_line_or_block_candidate_store", "no_forge"),
        ("layout_governance_ref", "layout_symbol_glyph_governance_snapshot", "no_forge"),
        ("image_quality_gate_ref", "input_quality_gate_output", "no_forge"),
        ("eligibility_gate_ref", "runtime_eligibility_output_not_eval_pack", "no_forge"),
        ("reading_order_ref", "reading_order_candidates_or_chosen_ro", "no_forge"),
        ("trace_ref", "request_trace_jsonl_handle", "no_forge"),
        ("replay_ref", "replay_jsonl_handle", "no_forge"),
        ("audit_ref", "hard_audit_or_audit_export_key", "no_forge"),
    ]
    return {
        "refs": [
            {
                "ref_name": r[0],
                "runtime_source_intent": r[1],
                "constraint": r[2],
                "eval_prefix_allowed_in_runtime": False,
                "missing_policy": "fail_closed_no_midplatform",
                "missing_fields_required": True,
            }
            for r in refs
        ],
        "rules": [
            "runtime ref must not use eval:* prefix",
            "do_not_fabricate trace_id session_id or any source_ref",
        ],
    }


def _flag_matrix() -> Dict[str, Any]:
    return {
        "global_kill": {
            "name": "LUNA_DISABLE_OCR_BRIDGE_RUNTIME_V1",
            "recommended_default": True,
            "priority": "highest",
        },
        "flags": [
            {"name": "LUNA_ENABLE_OCR_EVIDENCE_PACK_SHADOW_V1", "recommended_default": False},
            {"name": "LUNA_ENABLE_OCR_EVIDENCE_PACK_VALIDATE_V1", "recommended_default": False},
            {"name": "LUNA_ENABLE_OCR_EVIDENCE_PACK_FORWARD_MIDPLATFORM_V1", "recommended_default": False, "long_term_default": False},
            {"name": "LUNA_ENABLE_OCR_FACT_TEXT_LAYER_CANDIDATES_V1", "recommended_default": False, "separate_gate": True},
        ],
        "derived_defaults": {
            "forward_midplatform_default": False,
            "fact_text_layer_candidates_default": False,
            "global_kill_exists": True,
        },
    }


def _shadow_strategy_matrix() -> Dict[str, Any]:
    return {
        "allowed_first_implementation": [
            "generate_shadow_OcrEvidencePack",
            "validate_pack_when_flag_on",
            "write_trace_replay_audit",
            "emit_report",
        ],
        "forbidden_before_authorize_phase": [
            "real_midplatform_call",
            "real_scene_delta_call",
            "real_world_context_call",
            "navigation_action",
            "tts_broadcast",
            "fact_text_layer_write_without_flag",
            "mutate_ocr_provider_routing",
            "use_evaluation_routing_pack_as_runtime_source",
        ],
    }


def _abort_rollback_matrix() -> Dict[str, Any]:
    return {
        "abort_triggers": [
            "missing_required_source_ref",
            "pack_validation_failed",
            "non_ocr_fact_layer_violation",
            "symbol_glyph_merged_into_fact_text",
            "reading_order_uncertain_with_global_fact_text",
            "quality_no_go_in_eligible_fact_path",
            "hard_audit_runtime_or_midplatform_true",
            "real_midplatform_scene_world_called_without_authorize",
            "world_write_or_hive_upload",
            "trace_replay_audit_write_failed",
        ],
        "rollback_sequence": [
            "set LUNA_ENABLE_OCR_EVIDENCE_PACK_SHADOW_V1=false",
            "set LUNA_ENABLE_OCR_EVIDENCE_PACK_VALIDATE_V1=false",
            "set LUNA_DISABLE_OCR_BRIDGE_RUNTIME_V1=true",
            "preserve_logs",
            "do_not_delete_shadow_evidence_by_default",
            "emit_rollback_report",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--design-root", required=True)
    ap.add_argument("--review-root", required=True)
    ap.add_argument("--luna-core-root", default=REPO_ROOT)
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    design = _require_abs(args.design_root, "--design-root")
    review = _require_abs(args.review_root, "--review-root")
    lc = _require_abs(args.luna_core_root, "--luna-core-root")

    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / f"ocr_bridge_runtime_binding_rfc_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    issues: List[str] = []
    if not design.is_dir():
        issues.append("design_root_not_dir")
    elif not (design / "ocr_evidence_pack_example.json").is_file():
        issues.append("missing_design_pack_example")

    if not review.is_dir():
        issues.append("review_root_not_dir")
    elif not (review / "ocr_bridge_interface_freeze_summary.json").is_file():
        issues.append("missing_review_freeze_summary")

    doc_dir = lc / "docs" / "architecture" / "ocr_bridge"
    rfc_present = {fn: (doc_dir / fn).is_file() for fn in RFC_DOCS}
    if not all(rfc_present.values()):
        issues.append("missing_rfc_docs")
        for k, v in rfc_present.items():
            if not v:
                issues.append(f"missing_rfc_doc:{k}")

    verdict = "GO" if not issues else "NO_GO"

    flag_mx = _flag_matrix()
    summary = {
        "phase": "Phase-OCRBridge-Implementation-RFC-001",
        "verdict": verdict,
        "design_input_root": str(design),
        "review_input_root": str(review),
        "rfc_output_root": str(out),
        "luna_core_root": str(lc),
        "rfc_docs_present": rfc_present,
        "constraints": {
            "implementation_code_changes_scope": "none_rfc_tools_and_docs_only",
            "runtime_implementation_modules_modified": False,
            "runtime_integration": False,
            "midplatform_call": False,
            "whitebox_integration": False,
            "ocr_provider_routing_changed": False,
        },
        "forward_midplatform_default": flag_mx["derived_defaults"]["forward_midplatform_default"],
        "fact_text_layer_candidates_default": flag_mx["derived_defaults"]["fact_text_layer_candidates_default"],
        "global_kill_defined": flag_mx["derived_defaults"]["global_kill_exists"],
        "issues": issues,
    }

    _write_json(out / "ocr_bridge_runtime_binding_rfc_summary.json", summary)
    _write_json(out / "ocr_bridge_runtime_binding_candidate_matrix.json", _binding_candidate_matrix())
    _write_json(out / "ocr_bridge_runtime_source_ref_plan_matrix.json", _source_ref_plan_matrix())
    _write_json(out / "ocr_bridge_runtime_flag_matrix.json", flag_mx)
    _write_json(out / "ocr_bridge_shadow_only_strategy_matrix.json", _shadow_strategy_matrix())
    _write_json(out / "ocr_bridge_abort_rollback_matrix.json", _abort_rollback_matrix())

    notes = out / "ocr_bridge_runtime_binding_rfc_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# OCR Bridge — Runtime Binding RFC (v0)",
                "",
                f"- **design_input_root**: `{design}`",
                f"- **review_input_root**: `{review}`",
                f"- **rfc_output_root**: `{out}`",
                f"- **verdict**: `{verdict}`",
                "",
                "This phase produces **RFC matrices and notes only**. No runtime wiring.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "verdict": verdict}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
