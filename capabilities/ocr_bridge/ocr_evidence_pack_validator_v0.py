# -*- coding: utf-8 -*-
"""
OcrEvidencePackV0 validator — design-time static checks.
"""

from __future__ import annotations

from typing import Any, Dict, List, Set

from capabilities.ocr_bridge.ocr_evidence_pack_contract_v0 import OCR_EVIDENCE_PACK_VERSION


def validate_ocr_evidence_pack_v0(*, pack: Dict[str, Any], non_ocr_types: Set[str]) -> Dict[str, Any]:
    violations: List[str] = []

    if not str(pack.get("pack_id") or "").strip():
        violations.append("A_missing_pack_id")
    if str(pack.get("pack_version") or "") != OCR_EVIDENCE_PACK_VERSION:
        violations.append("B_bad_pack_version")

    for k in (
        "source_image_ref",
        "source_provider_ref",
        "source_quality_gate_ref",
        "source_layout_ref",
        "source_eligibility_gate_ref",
    ):
        if not isinstance(pack.get(k), str) or not str(pack.get(k)).strip():
            violations.append(f"C_missing_source_ref:{k}")

    list_keys = (
        "eligible_text_evidence",
        "conditional_text_evidence",
        "symbol_evidence",
        "glyph_evidence",
        "layout_evidence",
        "rejected_or_uncertain_evidence",
        "fact_text_layer_candidates",
        "must_not_enter_fact_text_layer",
    )
    for k in list_keys:
        if k not in pack or not isinstance(pack.get(k), list):
            violations.append(f"D_missing_evidence_list:{k}")

    def _refs(it: Dict[str, Any]) -> Dict[str, Any]:
        return it.get("source_refs") if isinstance(it.get("source_refs"), dict) else {}

    for bucket in ("eligible_text_evidence", "conditional_text_evidence", "symbol_evidence", "glyph_evidence", "layout_evidence", "rejected_or_uncertain_evidence"):
        for it in pack.get(bucket) or []:
            if not isinstance(it, dict):
                violations.append(f"E_non_object_in:{bucket}")
                continue
            if not str(it.get("evidence_id") or "").strip():
                violations.append(f"E_missing_evidence_id:{bucket}")
            if not str(it.get("evidence_type") or "").strip():
                violations.append(f"E_missing_evidence_type:{bucket}:{it.get('evidence_id')}")
            if "should_enter_fact_text_layer" not in it:
                violations.append(f"E_missing_should_enter_fact:{bucket}:{it.get('evidence_id')}")
            refs = _refs(it)
            for rk in ("source_image_ref", "provider_ref", "quality_gate_ref", "routing_ref"):
                if rk not in refs or not str(refs.get(rk) or "").strip():
                    violations.append(f"C_item_missing_source_refs:{bucket}:{it.get('evidence_id')}:{rk}")

    for it in pack.get("eligible_text_evidence") or []:
        ct = str((_refs(it)).get("eval_content_type") or "")
        if ct in non_ocr_types and bool(it.get("should_enter_fact_text_layer")):
            violations.append(f"F_non_ocr_fact_layer:{it.get('evidence_id')}:{ct}")

    for it in pack.get("conditional_text_evidence") or []:
        if bool(it.get("should_enter_fact_text_layer")):
            violations.append(f"I_conditional_fact_layer:{it.get('evidence_id')}")

    for it in pack.get("symbol_evidence") or []:
        if bool(it.get("should_enter_raw_text")) or bool(it.get("should_enter_fact_text_layer")):
            violations.append(f"G_symbol_raw_or_fact:{it.get('evidence_id')}")
    for it in pack.get("glyph_evidence") or []:
        if bool(it.get("should_enter_raw_text")) or bool(it.get("should_enter_fact_text_layer")):
            violations.append(f"G_glyph_raw_or_fact:{it.get('evidence_id')}")

    ro = pack.get("reading_order") or {}
    if bool(ro.get("reading_order_uncertain")) and pack.get("fact_text_layer_candidates"):
        violations.append("H_reading_order_uncertain_with_fact_candidates")

    for it in pack.get("eligible_text_evidence") or []:
        ct = str((_refs(it)).get("eval_content_type") or "")
        if ct == "multi_panel_layout":
            violations.append(f"I_multi_panel_in_eligible:{it.get('evidence_id')}")

    for it in pack.get("eligible_text_evidence") or []:
        qg = str(it.get("quality_gate") or "")
        if qg == "NO_GO":
            violations.append(f"J_low_quality_no_go_eligible:{it.get('evidence_id')}")
        if qg == "CONDITIONAL_GO":
            u = pack.get("uncertainty") or {}
            reasons = u.get("reasons") if isinstance(u.get("reasons"), list) else []
            if not bool(u.get("has_uncertainty")) and not reasons:
                violations.append(f"J_conditional_go_eligible_missing_pack_uncertainty:{it.get('evidence_id')}")

    ha = pack.get("hard_audit") or {}
    if ha.get("midplatform_invoked") is not False:
        violations.append("K_midplatform_invoked_not_false")
    if ha.get("world_write_invoked") is not False:
        violations.append("L_world_write_invoked_not_false")
    if ha.get("navigation_action") is not None:
        violations.append("M_navigation_action_not_null")

    return {
        "validation_passed": len(violations) == 0,
        "violations": violations,
        "rules_checked": [
            "A_pack_id",
            "B_pack_version",
            "C_source_refs",
            "D_evidence_lists",
            "E_should_enter_fact_flag",
            "F_non_ocr_fact_text",
            "G_symbol_glyph_raw_fact",
            "H_reading_order_vs_fact_candidates",
            "I_multi_panel_eligible",
            "J_low_quality_uncertainty",
            "K_midplatform_invoked",
            "L_world_write",
            "M_navigation_action",
        ],
    }
