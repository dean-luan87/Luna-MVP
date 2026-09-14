# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-007 — OCR Eligibility Gate Simulator v0 (Evaluation Tools).

Simulation-only: does not invoke OCR providers, does not integrate runtime/whitebox.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


def load_boundary_map_v0(boundary_eval_root: Path) -> Dict[str, Any]:
    p = boundary_eval_root / "ocr_capability_boundary_map.json"
    if not p.is_file():
        raise FileNotFoundError(f"missing_boundary_map:{p}")
    return json.loads(p.read_text(encoding="utf-8"))


def load_sample_matrix_v0(boundary_eval_root: Path) -> List[Dict[str, Any]]:
    p = boundary_eval_root / "ocr_capability_boundary_sample_matrix.json"
    if not p.is_file():
        raise FileNotFoundError(f"missing_sample_matrix:{p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("sample_matrix_not_list")
    return data


def _as_set(x: Any) -> Set[str]:
    if isinstance(x, list):
        return {str(v) for v in x}
    return set()


def _truth_has_chinese(truth: str) -> bool:
    for ch in truth or "":
        cp = ord(ch)
        if 0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF:
            return True
    return False


def _metrics_pass_for_eligible(
    *,
    content_type: str,
    cer: Optional[float],
    recall: Optional[float],
    garbled_score: float,
    pred_empty: bool,
    ground_truth_text: str,
) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    if pred_empty:
        return False, ["pred_empty"]
    if cer is None:
        return False, ["no_cer"]
    if cer > 0.15:
        reasons.append("cer_above_threshold")
    if garbled_score > 0.10:
        reasons.append("garbled_above_threshold")
    if _truth_has_chinese(ground_truth_text):
        if recall is None or recall < 0.80:
            reasons.append("chinese_recall_below_threshold")
    if reasons:
        return False, reasons
    return True, []


def classify_ocr_evidence_route_v0(
    *,
    sample: Dict[str, Any],
    eligible_types: Set[str],
    conditional_types: Set[str],
    non_ocr_types: Set[str],
) -> Dict[str, Any]:
    """
    Returns routing decision for one sample row (post-OCR evaluation row).
    Does not re-run OCR.
    """
    case_id = str(sample.get("case_id") or sample.get("sample_id") or "")
    content_type = str(sample.get("content_type") or "unknown")
    gen_status = str(sample.get("generation_status") or "generated")
    expected_route = str(sample.get("expected_ocr_route") or "")
    pred = str(sample.get("pred_text") or "")
    pred_empty = bool(sample.get("pred_empty"))
    cer = sample.get("cer")
    cer_f = float(cer) if cer is not None else None
    recall = sample.get("chinese_char_recall")
    recall_f = float(recall) if recall is not None else None
    garbled = float(sample.get("garbled_score") or 0.0)
    iq_gate = str(sample.get("input_quality_gate") or "NO_GO")
    truth = str(sample.get("ground_truth_text") or "")

    uncertainty: Dict[str, Any] = {
        "reason": [],
        "needs_layout": False,
        "needs_symbol_branch": False,
        "needs_glyph_branch": False,
        "needs_manual_review": False,
    }

    # Placeholder / no GT -> rejected_or_uncertain
    if gen_status != "generated" or not truth.strip():
        uncertainty["reason"].append("manual_sample_required_or_no_ground_truth")
        uncertainty["needs_manual_review"] = True
        return {
            "case_id": case_id,
            "content_type": content_type,
            "original_expected_route": expected_route,
            "ocr_raw_text": pred,
            "evidence_route": "rejected_or_uncertain",
            "should_enter_fact_text_layer": False,
            "uncertainty": uncertainty,
            "source_metrics": {
                "cer": cer_f,
                "chinese_recall": recall_f,
                "garbled_score": garbled,
                "empty_output": pred_empty,
                "image_quality_gate": iq_gate,
            },
        }

    # C-class explicit routing (never eligible fact text)
    if content_type in non_ocr_types:
        if content_type == "symbols_and_punctuation":
            route = "symbol"
            uncertainty["needs_symbol_branch"] = True
        elif content_type in ("artistic_text", "stylized_digits"):
            route = "glyph"
            uncertainty["needs_glyph_branch"] = True
        elif content_type == "icon_text_mix":
            route = "symbol_and_layout"
            uncertainty["needs_symbol_branch"] = True
            uncertainty["needs_layout"] = True
        elif content_type == "multi_panel_layout":
            route = "layout"
            uncertainty["needs_layout"] = True
        elif content_type == "decorative_graphic_non_text":
            route = "rejected_or_uncertain"
            uncertainty["reason"].append("decorative_non_text")
        elif content_type == "vertical_text":
            route = "layout"
            uncertainty["needs_layout"] = True
            uncertainty["reason"].append("vertical_text_not_eligible_for_plain_ocr_fact")
        elif content_type == "handwritten_style":
            route = "conditional_text"
            uncertainty["needs_manual_review"] = True
            uncertainty["reason"].append("handwritten_style_requires_review")
            uncertainty["reason"].extend(
                [
                    "preprocess_recommendation:eval_handwritten_v0",
                    "layout_branch_recommendation:eval_handwritten_v0",
                    "provider_fallback_recommendation:manual_or_specialized_v0",
                ]
            )
        else:
            route = "rejected_or_uncertain"
            uncertainty["reason"].append("non_ocr_default_reject")

        return {
            "case_id": case_id,
            "content_type": content_type,
            "original_expected_route": expected_route,
            "ocr_raw_text": pred,
            "evidence_route": route,
            "should_enter_fact_text_layer": False,
            "uncertainty": uncertainty,
            "source_metrics": {
                "cer": cer_f,
                "chinese_recall": recall_f,
                "garbled_score": garbled,
                "empty_output": pred_empty,
                "image_quality_gate": iq_gate,
            },
        }

    # B-class -> conditional (never direct fact without uncertainty)
    if content_type in conditional_types:
        uncertainty["reason"].append("conditional_content_domain")
        uncertainty["reason"].extend(
            [
                "preprocess_recommendation:eval_conditional_v0",
                "layout_branch_recommendation:eval_conditional_v0",
                "provider_fallback_recommendation:non_primary_ocr_or_manual_v0",
            ]
        )
        if iq_gate == "CONDITIONAL_GO":
            uncertainty["reason"].append("input_quality_conditional")
        if iq_gate == "NO_GO":
            uncertainty["reason"].append("input_quality_no_go")
            uncertainty["needs_manual_review"] = True
        return {
            "case_id": case_id,
            "content_type": content_type,
            "original_expected_route": expected_route,
            "ocr_raw_text": pred,
            "evidence_route": "conditional_text",
            "should_enter_fact_text_layer": False,
            "uncertainty": uncertainty,
            "source_metrics": {
                "cer": cer_f,
                "chinese_recall": recall_f,
                "garbled_score": garbled,
                "empty_output": pred_empty,
                "image_quality_gate": iq_gate,
            },
        }

    # A-class (eligible domain) — gate on quality + metrics
    if content_type in eligible_types:
        if iq_gate == "NO_GO":
            uncertainty["reason"].append("input_quality_no_go")
            uncertainty["needs_manual_review"] = True
            return {
                "case_id": case_id,
                "content_type": content_type,
                "original_expected_route": expected_route,
                "ocr_raw_text": pred,
                "evidence_route": "rejected_or_uncertain",
                "should_enter_fact_text_layer": False,
                "uncertainty": uncertainty,
                "source_metrics": {
                    "cer": cer_f,
                    "chinese_recall": recall_f,
                    "garbled_score": garbled,
                    "empty_output": pred_empty,
                    "image_quality_gate": iq_gate,
                },
            }

        ok, reasons = _metrics_pass_for_eligible(
            content_type=content_type,
            cer=cer_f,
            recall=recall_f,
            garbled_score=garbled,
            pred_empty=pred_empty,
            ground_truth_text=truth,
        )
        if iq_gate == "CONDITIONAL_GO":
            uncertainty["reason"].append("input_quality_conditional")
        if not ok:
            uncertainty["reason"].extend(reasons)
            return {
                "case_id": case_id,
                "content_type": content_type,
                "original_expected_route": expected_route,
                "ocr_raw_text": pred,
                "evidence_route": "conditional_text",
                "should_enter_fact_text_layer": False,
                "uncertainty": uncertainty,
                "source_metrics": {
                    "cer": cer_f,
                    "chinese_recall": recall_f,
                    "garbled_score": garbled,
                    "empty_output": pred_empty,
                    "image_quality_gate": iq_gate,
                },
            }

        # Eligible: GO or CONDITIONAL_GO with metrics pass
        if iq_gate == "CONDITIONAL_GO":
            uncertainty["reason"].append("eligible_but_quality_conditional")
        return {
            "case_id": case_id,
            "content_type": content_type,
            "original_expected_route": expected_route,
            "ocr_raw_text": pred,
            "evidence_route": "eligible_text",
            "should_enter_fact_text_layer": True,
            "uncertainty": uncertainty,
            "source_metrics": {
                "cer": cer_f,
                "chinese_recall": recall_f,
                "garbled_score": garbled,
                "empty_output": pred_empty,
                "image_quality_gate": iq_gate,
            },
        }

    # Unknown type -> manual review / reject
    uncertainty["reason"].append("unknown_content_type")
    uncertainty["needs_manual_review"] = True
    return {
        "case_id": case_id,
        "content_type": content_type,
        "original_expected_route": expected_route,
        "ocr_raw_text": pred,
        "evidence_route": "rejected_or_uncertain",
        "should_enter_fact_text_layer": False,
        "uncertainty": uncertainty,
        "source_metrics": {
            "cer": cer_f,
            "chinese_recall": recall_f,
            "garbled_score": garbled,
            "empty_output": pred_empty,
            "image_quality_gate": iq_gate,
        },
    }


def build_ocr_evidence_routing_pack_v0(
    *,
    routing_pack_id: str,
    source_eval_root: str,
    decisions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    eligible: List[Dict[str, Any]] = []
    conditional: List[Dict[str, Any]] = []
    symbol: List[Dict[str, Any]] = []
    glyph: List[Dict[str, Any]] = []
    layout: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []

    for d in decisions:
        route = str(d.get("evidence_route") or "")
        item = {
            "case_id": d.get("case_id"),
            "content_type": d.get("content_type"),
            "original_expected_route": d.get("original_expected_route"),
            "ocr_raw_text": d.get("ocr_raw_text"),
            "evidence_route": route,
            "should_enter_fact_text_layer": bool(d.get("should_enter_fact_text_layer")),
            "uncertainty": d.get("uncertainty") or {},
            "source_metrics": d.get("source_metrics") or {},
        }
        if route == "eligible_text":
            eligible.append(item)
        elif route == "conditional_text":
            conditional.append(item)
        elif route == "symbol":
            symbol.append(item)
        elif route == "glyph":
            glyph.append(item)
        elif route == "layout":
            layout.append(item)
        elif route == "symbol_and_layout":
            symbol.append({**item, "evidence_route": "symbol"})
            layout.append({**item, "evidence_route": "layout"})
        elif route == "rejected_or_uncertain":
            rejected.append(item)
        else:
            rejected.append({**item, "evidence_route": "rejected_or_uncertain"})

    total = len(decisions)
    return {
        "routing_pack_id": routing_pack_id,
        "source_eval_root": source_eval_root,
        "gate_version": "ocr_eligibility_gate_simulator_v0",
        "eligible_text_evidence": eligible,
        "conditional_text_evidence": conditional,
        "symbol_evidence": symbol,
        "glyph_evidence": glyph,
        "layout_evidence": layout,
        "rejected_or_uncertain_evidence": rejected,
        "summary": {
            "total_cases": total,
            "eligible_count": len(eligible),
            "conditional_count": len(conditional),
            "symbol_count": len(symbol),
            "glyph_count": len(glyph),
            "layout_count": len(layout),
            "rejected_or_uncertain_count": len(rejected),
        },
        "runtime_integration": False,
        "whitebox_integration": False,
        "mainline_side_effect": False,
    }


def simulate_ocr_eligibility_gate_v0(
    *,
    boundary_eval_root: Path,
    dataset_root: Path,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    _ = dataset_root  # reserved for manifest merge in future
    bm = load_boundary_map_v0(boundary_eval_root)
    samples = load_sample_matrix_v0(boundary_eval_root)
    eligible_types = _as_set(bm.get("ocr_eligible_content_types"))
    conditional_types = _as_set(bm.get("conditional_ocr_content_types"))
    non_ocr_types = _as_set(bm.get("non_ocr_content_types"))

    decisions: List[Dict[str, Any]] = []
    for s in samples:
        decisions.append(
            classify_ocr_evidence_route_v0(
                sample=s,
                eligible_types=eligible_types,
                conditional_types=conditional_types,
                non_ocr_types=non_ocr_types,
            )
        )
    return decisions, bm


def compute_false_text_risk_after_gate_v0(
    *,
    pack: Dict[str, Any],
    before_report: Dict[str, Any],
    non_ocr_types: Set[str],
    all_samples: List[Dict[str, Any]],
) -> Dict[str, Any]:
    non_ocr_cases = [s for s in all_samples if str(s.get("content_type") or "") in non_ocr_types and str(s.get("generation_status") or "") == "generated"]
    non_ocr_count = len(non_ocr_cases)
    eligible = pack.get("eligible_text_evidence") or []
    eligible_ids = {str(x.get("case_id")) for x in eligible if isinstance(x, dict)}
    non_ocr_ids = {str(s.get("case_id") or s.get("sample_id")) for s in non_ocr_cases}
    entered = len([cid for cid in non_ocr_ids if cid in eligible_ids])
    before_rate = before_report.get("false_text_risk_rate")
    after_rate = float(entered) / float(max(1, non_ocr_count)) if non_ocr_count else 0.0
    return {
        "false_text_risk_before": before_rate,
        "false_text_risk_after": after_rate,
        "non_ocr_case_count": non_ocr_count,
        "non_ocr_entered_eligible_text_count": entered,
        "non_ocr_routed_to_symbol_glyph_layout_or_reject_count": int(non_ocr_count - entered),
        "risk_reduction": (float(before_rate) - after_rate) if before_rate is not None else None,
    }


def _actual_route_label(decision: Dict[str, Any]) -> str:
    r = str(decision.get("evidence_route") or "")
    if r in ("symbol", "glyph", "layout"):
        return r
    if r == "symbol_and_layout":
        return "symbol+layout"
    if r == "eligible_text":
        return "eligible_text"
    if r == "conditional_text":
        return "conditional_text"
    if r == "rejected_or_uncertain":
        return "rejected_or_uncertain"
    return "other"


def compute_eligibility_accuracy_after_gate_v0(
    *,
    decisions: List[Dict[str, Any]],
    samples: List[Dict[str, Any]],
    before_accuracy_report: Dict[str, Any],
    eligible_types: Set[str],
    conditional_types: Set[str],
    non_ocr_types: Set[str],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Proxy: for each generated sample with GT, check routing expectation vs gate output label.
    """
    by_id = {str(d.get("case_id")): d for d in decisions}
    correct = 0
    incorrect = 0
    confusion: Dict[str, Dict[str, int]] = {}

    def bump(ideal: str, actual: str) -> None:
        confusion.setdefault(ideal, {})
        confusion[ideal][actual] = int(confusion[ideal].get(actual, 0) + 1)

    for s in samples:
        cid = str(s.get("case_id") or s.get("sample_id") or "")
        if cid not in by_id:
            continue
        gen = str(s.get("generation_status") or "")
        truth = str(s.get("ground_truth_text") or "")
        if gen != "generated" or not truth.strip():
            continue
        ct = str(s.get("content_type") or "")
        dec = by_id[cid]
        actual = _actual_route_label(dec)

        match = False
        ideal = "unknown"

        if ct in non_ocr_types:
            ideal = "non_ocr_not_eligible_text"
            match = actual in ("symbol", "glyph", "layout", "symbol+layout", "rejected_or_uncertain", "conditional_text")
        elif ct in conditional_types:
            ideal = "conditional_domain"
            match = actual in ("conditional_text", "rejected_or_uncertain", "layout")
        elif ct in eligible_types:
            iq = str(s.get("input_quality_gate") or "")
            cer = s.get("cer")
            cer_f = float(cer) if cer is not None else None
            recall = s.get("chinese_char_recall")
            recall_f = float(recall) if recall is not None else None
            garbled = float(s.get("garbled_score") or 0.0)
            pred_empty = bool(s.get("pred_empty"))
            ok, _ = _metrics_pass_for_eligible(
                content_type=ct,
                cer=cer_f,
                recall=recall_f,
                garbled_score=garbled,
                pred_empty=pred_empty,
                ground_truth_text=truth,
            )
            if iq == "NO_GO" or not ok:
                ideal = "eligible_domain_but_gated_to_conditional_or_reject"
                match = actual in ("conditional_text", "rejected_or_uncertain")
            else:
                ideal = "eligible_domain_ok"
                match = actual == "eligible_text"
        else:
            ideal = "unknown_type"
            match = actual == "rejected_or_uncertain"

        if match:
            correct += 1
        else:
            incorrect += 1
        bump(ideal, actual)

    total = correct + incorrect
    before_acc = before_accuracy_report.get("eligibility_accuracy")
    after_acc = float(correct) / float(max(1, total)) if total else 0.0
    report = {
        "eligibility_accuracy_before": before_acc,
        "eligibility_accuracy_after": after_acc,
        "evaluated_case_count": total,
        "correct_route_count": correct,
        "incorrect_route_count": incorrect,
        "route_confusion_matrix": confusion,
        "notes": "after metrics are evaluation-only simulator results, not runtime router truth",
    }
    return report, confusion


def build_distortion_prevention_report_v0(
    *,
    pack: Dict[str, Any],
    decisions: List[Dict[str, Any]],
    non_ocr_types: Set[str],
    conditional_types: Set[str],
    samples: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    violations: List[str] = []
    eligible = pack.get("eligible_text_evidence") or []
    eligible_ids = {str(x.get("case_id")) for x in eligible if isinstance(x, dict)}
    by_id_dec = {str(d.get("case_id")): d for d in decisions}
    for it in eligible:
        ct = str(it.get("content_type") or "")
        if ct in non_ocr_types:
            violations.append(f"non_ocr_in_eligible:{it.get('case_id')}:{ct}")
        if not bool(it.get("should_enter_fact_text_layer")):
            violations.append(f"eligible_missing_fact_flag:{it.get('case_id')}")

    # symbol/glyph not raw fact: any eligible with symbol-like type already caught
    # low_quality: B domain should not be eligible
    for it in eligible:
        ct = str(it.get("content_type") or "")
        if ct in conditional_types:
            violations.append(f"conditional_domain_in_eligible:{it.get('case_id')}:{ct}")

    sym_like = {"symbols_and_punctuation", "artistic_text", "stylized_digits", "icon_text_mix"}
    for it in eligible:
        ct = str(it.get("content_type") or "")
        if ct in sym_like:
            violations.append(f"symbol_glyph_like_in_eligible:{it.get('case_id')}:{ct}")

    if samples:
        for s in samples:
            cid = str(s.get("case_id") or s.get("sample_id") or "")
            ro_unc = s.get("reading_order_uncertain")
            if ro_unc is True and cid in eligible_ids:
                violations.append(f"reading_order_uncertain_in_eligible:{cid}")
            if str(s.get("content_type") or "") == "multi_panel_layout":
                if cid in eligible_ids:
                    violations.append(f"multi_panel_cross_fact_eligible:{cid}")
            iq = str(s.get("input_quality_gate") or "")
            if cid not in eligible_ids:
                continue
            if iq == "NO_GO":
                violations.append(f"low_quality_no_go_in_eligible:{cid}")
            elif iq == "CONDITIONAL_GO":
                dec = by_id_dec.get(cid) or {}
                u = dec.get("uncertainty") or {}
                reasons = u.get("reason") or []
                if dec.get("evidence_route") == "eligible_text" and isinstance(reasons, list):
                    if "eligible_but_quality_conditional" not in reasons:
                        violations.append(f"low_quality_conditional_missing_warning:{cid}")

    passed = len(violations) == 0
    return {
        "distortion_prevention_passed": passed,
        "violations": violations,
        "rules_checked": [
            "non_ocr_not_fact_text",
            "symbol_glyph_not_raw_text_fact",
            "reading_order_uncertain_not_global_fact",
            "multi_panel_not_cross_joined",
            "low_quality_requires_uncertainty",
        ],
    }
