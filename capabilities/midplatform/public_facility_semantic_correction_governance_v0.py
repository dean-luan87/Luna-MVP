# -*- coding: utf-8 -*-
"""Public facility semantic correction governance stub (no OCR mainline, no fact writes).

Phase-PublicFacility-Semantic-Correction-Governance-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "PublicFacility-Semantic-Correction-Governance-001"

SUMMARY_SCHEMA = "public_facility_semantic_correction_governance_summary_v0"
FIXTURE_SCHEMA = "public_facility_synthetic_fixture_manifest_v0"
TAXONOMY_SCHEMA = "public_facility_taxonomy_v0"
ROUTING_SCHEMA = "public_facility_evidence_routing_policy_v0"
CORRECTION_LEVELS_SCHEMA = "public_facility_correction_levels_v0"
PIPELINE_SCHEMA = "public_facility_pipeline_layers_v0"
CANDIDATE_EXAMPLE_SCHEMA = "public_facility_semantic_candidate_example_v0"
RISK_SCHEMA = "public_facility_governance_risk_report_v0"
GATE_SCHEMA = "public_facility_gate_policy_report_v0"
NON_CLAIMS_SCHEMA = "public_facility_governance_non_claims_v0"
AUDIT_SCHEMA = "public_facility_governance_audit_v0"

FACILITY_SEMANTICS: Tuple[str, ...] = (
    "elevator",
    "exit",
    "restroom",
    "bus_stop",
    "hospital",
    "service_desk",
    "information_desk",
    "accessible_route",
    "stairs",
    "subway_entrance",
    "first_aid",
    "parking",
    "payment_counter",
    "security_checkpoint",
)

SIGN_W = 480
SIGN_H = 320


def _load_font(size: int = 28) -> Any:
    from PIL import ImageFont

    for fp in (
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(fp, size)
        except OSError:
            continue
    return ImageFont.load_default()


def create_synthetic_facility_fixture_v0(work_dir: Path) -> Dict[str, Any]:
    """Restroom sign with typo 'Toliet' + pictogram (no OCR execution)."""
    from PIL import Image, ImageDraw

    work_dir.mkdir(parents=True, exist_ok=True)
    image_path = (work_dir / "public_facility_restroom_typo_sign_v0.png").resolve()

    img = Image.new("RGB", (SIGN_W, SIGN_H), (240, 245, 250))
    draw = ImageDraw.Draw(img)
    font = _load_font(36)
    small = _load_font(20)

    draw.rectangle([20, 20, SIGN_W - 20, SIGN_H - 20], outline=(60, 80, 120), width=3)
    draw.text((60, 40), "Toliet", fill=(30, 30, 40), font=font)
    ix1, iy1, ix2, iy2 = 300, 50, 420, 200
    draw.rectangle([ix1, iy1, ix2, iy2], fill=(220, 230, 245), outline=(80, 100, 140))
    draw.ellipse([ix1 + 50, iy1 + 30, ix1 + 70, iy1 + 50], fill=(80, 100, 140))
    draw.text((ix1 + 20, iy2 - 40), "WC", fill=(60, 70, 90), font=small)
    draw.text((40, SIGN_H - 50), "facility_sign_typo_example", fill=(120, 120, 130), font=small)

    img.save(image_path, format="PNG")
    return {
        "schema_version": FIXTURE_SCHEMA,
        "fixture_id": "public_facility_restroom_typo_sign_v0",
        "source_image_ref": str(image_path),
        "image_type": "public_facility_sign",
        "intentional_typo_text": "Toliet",
        "expected_human_semantic": "restroom",
        "visual_symbol_hint": "toilet_icon",
        "ocr_mainline_default": False,
        "ocr_invoked": False,
    }


def build_taxonomy() -> Dict[str, Any]:
    return {
        "schema_version": TAXONOMY_SCHEMA,
        "facility_semantic_ids": list(FACILITY_SEMANTICS),
        "display_names": {
            "elevator": "电梯",
            "exit": "出口",
            "restroom": "洗手间",
            "bus_stop": "公交站",
            "hospital": "医院",
            "service_desk": "服务台",
            "information_desk": "问询处",
            "accessible_route": "无障碍通道",
            "stairs": "楼梯",
            "subway_entrance": "地铁入口",
            "first_aid": "急救点",
            "parking": "停车场",
            "payment_counter": "收费处",
            "security_checkpoint": "安检口",
        },
    }


def build_evidence_routing_policy() -> Dict[str, Any]:
    return {
        "schema_version": ROUTING_SCHEMA,
        "image_type": "public_facility_sign",
        "default_ocr_mainline_allowed": False,
        "semantic_first_required": True,
        "primary_evidence_types": [
            "PublicFacilityEvidence",
            "FacilitySemanticCandidate",
            "VisualSymbolEvidence",
        ],
        "auxiliary_evidence_types": ["OCRTextEvidence"],
        "ocr_role": "auxiliary_only",
        "forbidden_default_path": [
            "image_input",
            "ocr_mainline_default",
            "ocr_text_as_primary_fact",
        ],
        "rationale": (
            "Facility signs are icon + sparse text + spatial intent; "
            "semantic value exceeds raw OCR text."
        ),
    }


def build_correction_levels() -> Dict[str, Any]:
    return {
        "schema_version": CORRECTION_LEVELS_SCHEMA,
        "levels": [
            {
                "level": 1,
                "name": "rule_dictionary",
                "scope": "Fixed tokens: EXIT, Toilet, Restroom, Elevator, Information, Hospital, etc.",
                "produces": "correction_candidate",
                "may_write_fact": False,
            },
            {
                "level": 2,
                "name": "facility_semantic_library",
                "scope": "Icon + scene type + POI context (e.g. WC + gender icons → restroom).",
                "produces": "facility_semantic_candidate",
                "may_write_fact": False,
            },
            {
                "level": 3,
                "name": "model_correction_candidate",
                "scope": "Deformed fonts, misspellings, partial text, mixed language.",
                "produces": "correction_candidate",
                "may_write_fact": False,
                "model_may_finalize_fact": False,
            },
        ],
        "midplatform_arbitration": {
            "combines": [
                "rule_dictionary",
                "visual_symbol_match",
                "facility_semantic_library",
                "ocr_auxiliary_candidate",
                "model_correction_candidate",
            ],
            "outputs": "FacilitySemanticCandidate",
            "fact_status_default": "not_fact",
        },
    }


def build_pipeline_layers() -> Dict[str, Any]:
    return {
        "schema_version": PIPELINE_SCHEMA,
        "approved_pipeline": [
            "image_input",
            "public_facility_classifier",
            "visual_symbol_evidence",
            "ocr_auxiliary_candidate",
            "facility_correction_layer",
            "midplatform_semantic_candidate",
            "gate_review",
            "announcement_candidate",
        ],
        "forbidden_pipeline": [
            "image_input",
            "ocr_mainline_default",
            "read_text_only",
            "interpret_text_as_facility_fact",
        ],
    }


def build_semantic_candidate_example() -> Dict[str, Any]:
    return {
        "schema_version": CANDIDATE_EXAMPLE_SCHEMA,
        "example_id": "restroom_typo_toliet_v0",
        "raw_ocr_text": "Toliet",
        "raw_ocr_text_preserved": True,
        "visual_symbol_candidate": "toilet_icon",
        "facility_semantic_candidate": "restroom",
        "correction_candidate": "toilet",
        "correction_source": [
            "facility_dictionary",
            "visual_symbol_match",
            "model_candidate",
        ],
        "fact_status": "not_fact",
        "requires_review": False,
        "confidence": 0.86,
        "output_semantics": "restroom_facility_nearby",
        "announcement_examples": {
            "high_confidence": "右前方疑似洗手间标识",
            "low_confidence_or_conflict": "前方疑似洗手间标识，但文字不完整，建议再靠近确认",
        },
        "non_goal": "Replace raw_ocr_text in storage; goal is facility semantics not spelling fix alone",
    }


def build_risk_report() -> Dict[str, Any]:
    risks = [
        ("ocr_typo_over_trust", "Trusting misspelled OCR as ground truth"),
        ("facility_semantic_confusion", "Exit vs elevator vs restroom confusion"),
        ("visual_symbol_ocr_swap", "Icon treated as text or vice versa"),
        ("model_overwrite_raw_text", "Model correction hiding original error"),
        ("premature_navigation_output", "Navigation without gate"),
        ("world_model_write_from_facility", "Writing facility candidate as fact"),
        ("default_ocr_mainline_on_facility", "Public facility routed to OCR mainline"),
        ("low_confidence_over_announce", "Over-confident TTS when evidence conflicts"),
    ]
    return {
        "schema_version": RISK_SCHEMA,
        "risks": [
            {"risk_id": rid, "description": desc, "mitigation": "semantic_first_governance_stub"}
            for rid, desc in risks
        ],
    }


def build_gate_policy() -> Dict[str, Any]:
    return {
        "schema_version": GATE_SCHEMA,
        "default_ocr_mainline_allowed": False,
        "semantic_first_required": True,
        "ocr_text_evidence_primary_allowed": False,
        "model_may_finalize_fact": False,
        "raw_ocr_text_must_be_preserved": True,
        "world_model_write_allowed": False,
        "scene_delta_write_allowed": False,
        "midplatform_fact_write_allowed": False,
        "navigation_output_requires_gate": True,
        "auto_approval_allowed": False,
        "parallel_governance_lines": {
            "poster_advertisement": "layout_segment_first_then_regional_ocr",
            "public_facility": "facility_semantic_first_ocr_auxiliary",
        },
    }


def build_non_claims() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "explicit_non_claims": [
            "Does not implement a pure rule-only or pure model-only corrector",
            "Does not run OCR or vision providers in this governance phase",
            "Does not write WorldModel or Scene Delta",
            "Does not auto-approve facility semantics for navigation",
            "Does not guarantee OCR spelling correction accuracy",
            "Does not replace formal Evaluation Platform",
        ],
    }


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "public_facility_semantic_correction_governance_executed": True,
        "governance_only": True,
        "default_ocr_mainline_allowed": False,
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "vlm_invoked": False,
        "ai_interpretation_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
    }


def build_summary(*, source_image_ref: str) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "governance_scope": "public_facility_semantic_governance_only",
        "image_type": "public_facility_sign",
        "semantic_first_required": True,
        "default_ocr_mainline_allowed": False,
        "source_image_ref": source_image_ref,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "fact_status": "not_fact",
    }


def run_public_facility_semantic_correction_governance_v0(
    *,
    metrics_schema_root: Optional[str] = None,
    work_dir: Path,
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    if metrics_schema_root:
        p = Path(metrics_schema_root) / "cross_modal_vision_ocr_testboard_metrics_schema_summary.json"
        if not p.is_file():
            errs.append("missing_metrics_schema_summary")

    manifest = create_synthetic_facility_fixture_v0(work_dir / "fixtures")
    source_ref = str(manifest["source_image_ref"])

    summary = build_summary(source_image_ref=source_ref)
    taxonomy = build_taxonomy()
    routing = build_evidence_routing_policy()
    levels = build_correction_levels()
    pipeline = build_pipeline_layers()
    example = build_semantic_candidate_example()
    risks = build_risk_report()
    gate = build_gate_policy()
    non_claims = build_non_claims()
    audit = build_audit()

    if metrics_schema_root:
        summary["metrics_schema_root"] = str(Path(metrics_schema_root).resolve())

    phase_verdict = "GO" if not errs else "CONDITIONAL_GO"
    summary["phase_verdict_hint"] = phase_verdict
    summary["errors"] = list(errs)

    return (
        summary,
        manifest,
        taxonomy,
        routing,
        levels,
        pipeline,
        example,
        risks,
        gate,
        non_claims,
        audit,
        errs,
    )
