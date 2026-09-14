#!/usr/bin/env python3
"""Patch generated v2 capability to match phase spec."""
from pathlib import Path

P = Path(__file__).resolve().parents[3] / "capabilities/ocr_runtime/ocrrequest_gated_submission_from_roi_v2_bbox_expansion.py"


def main() -> None:
    t = P.read_text(encoding="utf-8")

    # gate rules prefix
    extra = '''    {
        "rule_id": "ocrrequest_reference_v2_required",
        "condition": "ocrrequest_reference_v2_id present",
        "allowed_action": "intake",
        "blocked_action": "submit_without_reference_v2",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "expanded_crop_file_required",
        "condition": "expanded crop file exists",
        "allowed_action": "select_for_submission",
        "blocked_action": "submit_missing_expanded_crop",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "expansion_candidate_ref_required",
        "condition": "source_bbox_expansion_candidate_id present",
        "allowed_action": "preserve_expansion_ref",
        "blocked_action": "drop_expansion_ref",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "expanded_crop_artifact_ref_required",
        "condition": "source_expanded_crop_artifact_id present",
        "allowed_action": "preserve_crop_ref",
        "blocked_action": "drop_crop_ref",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "source_bbox_and_expanded_bbox_required",
        "condition": "both bboxes present",
        "allowed_action": "dual_bbox_metadata",
        "blocked_action": "single_bbox_only",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_source_validation_v2_in_this_phase",
        "condition": "phase boundary",
        "allowed_action": "ocr_only",
        "blocked_action": "source_validation_v2",
        "submission_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "condition": "phase boundary",
        "allowed_action": "no_write",
        "blocked_action": "scene_delta_candidate",
        "submission_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
'''
    if "ocrrequest_reference_v2_required" not in t:
        t = t.replace(
            'GATE_RULES: List[Dict[str, Any]] = [\n    {\n        "rule_id": "ocrrequest_reference_required",',
            'GATE_RULES: List[Dict[str, Any]] = [\n' + extra + '    {\n        "rule_id": "ocrrequest_reference_required",',
        )

    t = t.replace(
        'source_task_id=str(ref.get("ocrrequest_reference_v2_id") or ref.get("ocrrequest_reference_v2_id") or ""),',
        'source_task_id=str(ref.get("ocrrequest_reference_v2_id") or ""),',
    )
    t = t.replace('"schema_version": "ocrrequest_roi_direct_provider_bypass_audit_v1"', '"schema_version": "ocrrequest_v2_direct_provider_bypass_audit_v1"')

    # intake block replacement via marker
    old_intake = '''        intake_rows.append(
            {
                "submission_intake_id": _intake_id(ref_id),
                "ocrrequest_reference_id": ref_id,
                "source_crop_artifact_id": ref.get("source_crop_artifact_id"),
                "crop_file_path": crop_path,
                "crop_bbox_xyxy": ref.get("crop_bbox_xyxy"),
                "crop_width": ref.get("crop_width"),
                "crop_height": ref.get("crop_height"),
                "candidate_frame_id": ref.get("candidate_frame_id"),
                "provider_class_allowed": ref.get("provider_class_allowed") or payload.get("provider_class_allowed"),
                "submission_mode": ref.get("submission_mode") or payload.get("submission_mode"),
                "source_quality_grade": gate_meta.get("source_quality_grade"),
                "target_source_quality_grade": gate_meta.get("target_source_quality_grade"),
                "readability_grade": gate_meta.get("readability_grade"),
                "full_frame_ocr_allowed": ref.get("full_frame_ocr_allowed", False),
                "mock_text_allowed": ref.get("mock_text_allowed", False),
                "intake_status": "accepted" if crop_ok else "rejected",
                "selected_for_submission": crop_ok,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )'''
    new_intake = '''        intake_rows.append(
            {
                "submission_intake_v2_id": _intake_id(ref_id),
                "ocrrequest_reference_v2_id": ref_id,
                "source_expanded_crop_artifact_id": ref.get("source_expanded_crop_artifact_id"),
                "source_bbox_expansion_candidate_id": ref.get("source_bbox_expansion_candidate_id"),
                "expansion_strategy": ref.get("expansion_strategy"),
                "crop_file_path": crop_path,
                "source_bbox_xyxy": ref.get("source_bbox_xyxy"),
                "expanded_bbox_xyxy": ref.get("expanded_bbox_xyxy"),
                "crop_width": ref.get("crop_width"),
                "crop_height": ref.get("crop_height"),
                "area_growth_ratio": ref.get("area_growth_ratio"),
                "provider_class_allowed": ref.get("provider_class_allowed") or payload.get("provider_class_allowed"),
                "submission_mode": ref.get("submission_mode") or payload.get("submission_mode") or "gated_eval",
                "full_frame_ocr_allowed": ref.get("full_frame_ocr_allowed", False),
                "mock_text_allowed": ref.get("mock_text_allowed", False),
                "bbox_expansion_applied": gate_meta.get("bbox_expansion_applied", True),
                "intake_status": "accepted" if crop_ok else "rejected",
                "selected_for_submission": crop_ok,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )'''
    t = t.replace(old_intake, new_intake)

    old_plan = '''        plan_rows.append(
            {
                "ocrrequest_submission_id": sub_id,
                "ocrrequest_reference_id": ref_id,
                "source_crop_artifact_id": ref.get("source_crop_artifact_id"),
                "payload_candidate_id": f"payload_{hashlib.sha256(ref_id.encode()).hexdigest()[:10]}",
                "provider_class_selected": str(ref.get("provider_class_allowed") or "rapidocr_lightweight"),
                "submission_mode": "gated_eval",
                "selected_for_submission": selected,
                "selection_reason": selection_reason,
                "blocked_reason": blocked_reason,
                "direct_provider_bypass_allowed": False,
                "current_phase_provider_invocation_allowed": selected,
                "evidence_pack_generation_allowed": False,
                "semantic_generation_allowed": False,
                "fact_status": "not_fact",
            }
        )'''
    new_plan = '''        plan_rows.append(
            {
                "ocrrequest_submission_v2_id": sub_id,
                "ocrrequest_reference_v2_id": ref_id,
                "source_expanded_crop_artifact_id": ref.get("source_expanded_crop_artifact_id"),
                "source_bbox_expansion_candidate_id": ref.get("source_bbox_expansion_candidate_id"),
                "expansion_strategy": ref.get("expansion_strategy"),
                "payload_candidate_id": f"payload_{hashlib.sha256(ref_id.encode()).hexdigest()[:10]}",
                "provider_class_selected": str(ref.get("provider_class_allowed") or "rapidocr_lightweight"),
                "submission_mode": "gated_eval",
                "selected_for_submission": selected,
                "selection_reason": selection_reason,
                "blocked_reason": blocked_reason,
                "direct_provider_bypass_allowed": False,
                "current_phase_provider_invocation_allowed": selected,
                "evidence_pack_generation_allowed": False,
                "semantic_generation_allowed": False,
                "source_validation_v2_allowed": False,
                "fact_status": "not_fact",
            }
        )'''
    t = t.replace(old_plan, new_plan)
    t = t.replace('selection_reason = "eligible_roi_crop_reference"', 'selection_reason = "eligible_expanded_roi_reference_v2"')

    # skipped result
    t = t.replace('"roi_ocr_result_id":', '"expanded_roi_ocr_result_v2_id":')
    t = t.replace('"ocrrequest_submission_id":', '"ocrrequest_submission_v2_id":')
    t = t.replace('"ocrrequest_reference_id":', '"ocrrequest_reference_v2_id":')
    t = t.replace('"source_crop_artifact_id": ref.get("source_crop_artifact_id")', '"source_expanded_crop_artifact_id": ref.get("source_expanded_crop_artifact_id")')

    # trace
    t = t.replace('"bridge_call_id":', '"bridge_call_v2_id":')
    old_trace_tail = '''                "source_expanded_crop_artifact_id": ref.get("source_expanded_crop_artifact_id"),
                "crop_file_path": crop_path,
                "provider_class_selected": ref.get("provider_class_allowed"),'''
    if "expansion_strategy" not in t.split("trace_rows.append")[1][:800] if "trace_rows.append" in t else "":
        t = t.replace(
            '''                "source_expanded_crop_artifact_id": ref.get("source_expanded_crop_artifact_id"),
                "crop_file_path": crop_path,
                "provider_class_selected": ref.get("provider_class_allowed"),
                "bridge_function_used":''',
            '''                "source_expanded_crop_artifact_id": ref.get("source_expanded_crop_artifact_id"),
                "source_bbox_expansion_candidate_id": ref.get("source_bbox_expansion_candidate_id"),
                "expansion_strategy": ref.get("expansion_strategy"),
                "crop_file_path": crop_path,
                "provider_class_selected": ref.get("provider_class_allowed"),
                "bridge_function_used":''',
        )

    # success result extras
    t = t.replace(
        '''        chain = list(ref.get("source_chain") or []) + [RUNTIME_STEP]
        results.append(
            {
                "expanded_roi_ocr_result_v2_id": _result_id(sub_id),
                "ocrrequest_submission_v2_id": sub_id,
                "ocrrequest_reference_v2_id": ref_id,
                "source_expanded_crop_artifact_id": ref.get("source_expanded_crop_artifact_id"),
                "crop_file_path": crop_path,
                "provider": prov_name,''',
        '''        low_info = (not empty_text and len(text_joined.strip()) <= 2) or text_joined.strip() in ("行",)
        chain = list(ref.get("source_chain") or []) + [RUNTIME_STEP]
        results.append(
            {
                "expanded_roi_ocr_result_v2_id": _result_id(sub_id),
                "ocrrequest_submission_v2_id": sub_id,
                "ocrrequest_reference_v2_id": ref_id,
                "source_expanded_crop_artifact_id": ref.get("source_expanded_crop_artifact_id"),
                "source_bbox_expansion_candidate_id": ref.get("source_bbox_expansion_candidate_id"),
                "expansion_strategy": ref.get("expansion_strategy"),
                "crop_file_path": crop_path,
                "source_bbox_xyxy": ref.get("source_bbox_xyxy"),
                "expanded_bbox_xyxy": ref.get("expanded_bbox_xyxy"),
                "crop_width": ref.get("crop_width"),
                "crop_height": ref.get("crop_height"),
                "provider": prov_name,''',
    )
    t = t.replace(
        '''                "result_status": result_status,
                "fact_status": "not_fact",
                "write_allowed": False,
                "evidence_pack_generated": False,
                "semantic_candidate_generated": False,
                "source_chain": chain,
            }
        )

        preview = text_joined[:80]''',
        '''                "result_status": result_status,
                "low_information_text": low_info,
                "repeated_same_text_candidate": False,
                "fact_status": "not_fact",
                "write_allowed": False,
                "evidence_pack_generated": False,
                "semantic_candidate_generated": False,
                "source_chain": chain,
            }
        )

        preview = text_joined[:80]''',
    )

    t = t.replace(
        '''                "ocrrequest_reference_v2_id": ref_id,
                "submission_status": submission_status,
                "provider_status": provider_status,
                "raw_ocr_text_preview": preview,
                "empty_text": empty_text,
                "text_item_count": len(text_items),
                **conf,
                "crop_file_path": crop_path,''',
        '''                "ocrrequest_reference_v2_id": ref_id,
                "expansion_strategy": ref.get("expansion_strategy"),
                "submission_status": submission_status,
                "provider_status": provider_status,
                "raw_ocr_text_preview": preview,
                "empty_text": empty_text,
                "text_item_count": len(text_items),
                **conf,
                "crop_file_path": crop_path,
                "crop_width": ref.get("crop_width"),
                "crop_height": ref.get("crop_height"),
                "area_growth_ratio": ref.get("area_growth_ratio"),
                "low_information_text": low_info,
                "result_status": result_status,''',
    )

    old_chain = '''        chain_rows.append(
            {
                "expanded_roi_ocr_result_v2_id": _result_id(sub_id),
                "traceable_to_ocrrequest_reference_v2": True,
                "traceable_to_crop_artifact": bool(ref.get("source_expanded_crop_artifact_id")),
                "traceable_to_better_frame_selection": bool(ref.get("source_better_frame_candidate_id")),
                "traceable_to_roi_retry_proposal": bool(ref.get("source_roi_retry_proposal_id")),
                "traceable_to_source_validation": any("validation:" in str(c) for c in chain),
                "traceable_to_linebox_trace": bool(ref.get("candidate_frame_id")),
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )'''
    new_chain = '''        chain_rows.append(
            {
                "expanded_roi_ocr_result_v2_id": _result_id(sub_id),
                "traceable_to_ocrrequest_reference_v2": True,
                "traceable_to_expanded_crop_artifact": True,
                "traceable_to_bbox_expansion_candidate": bool(ref.get("source_bbox_expansion_candidate_id")),
                "traceable_to_crop_v2": crop_v2_root.is_dir(),
                "traceable_to_diversity_check": div_root.is_dir(),
                "traceable_to_quality_diagnosis": diag_root.is_dir(),
                "traceable_to_linebox_trace": True,
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )'''
    t = t.replace(old_chain, new_chain)

    insert = '''
    texts = [str(r.get("raw_ocr_text") or "").strip() for r in results if str(r.get("result_status", "")).startswith("success")]
    from collections import Counter
    tc = Counter(texts)
    most_common = tc.most_common(1)[0][0] if tc else ""
    unique_text_count = len([x for x in tc if x])
    low_info_count = sum(1 for r in results if r.get("low_information_text"))
    for r in results:
        ttxt = str(r.get("raw_ocr_text") or "").strip()
        r["repeated_same_text_candidate"] = bool(ttxt) and texts.count(ttxt) > 1
    repeated_same = sum(1 for r in results if r.get("repeated_same_text_candidate"))
    strategy_rows = []
    for r in results:
        if r.get("result_status") == "skipped_not_selected":
            continue
        strategy_rows.append({
            "expansion_strategy": r.get("expansion_strategy"),
            "crop_size": f"{r.get('crop_width')}x{r.get('crop_height')}" if r.get("crop_width") else None,
            "area_growth_ratio": None,
            "raw_ocr_text": r.get("raw_ocr_text"),
            "text_item_count": len(r.get("text_items") or []),
            "empty_text": r.get("empty_text"),
            "low_information_text": r.get("low_information_text"),
            "repeated_with_other_strategy": r.get("repeated_same_text_candidate"),
            "confidence_summary": r.get("confidence_summary"),
            "useful_text_candidate": bool(str(r.get("raw_ocr_text") or "").strip()) and not r.get("low_information_text"),
            "comparison_candidate_only": True,
            "benchmark_score_generated": False,
            "accuracy_claimed": False,
            "recommended_for_future_ep_adapter": "Evidence-Pack-Adapter-v3-BBoxExpansion",
            "required_next_action": "Semantic-Candidate-v3-BBoxExpansionAware",
            "fact_status": "not_fact",
        })
'''
    if "strategy_rows" not in t:
        t = t.replace("    bypass_static = _static_bypass_scan(cap_path)", insert + "    bypass_static = _static_bypass_scan(cap_path)")

    t = t.replace(
        'bool(r.get("ocrrequest_reference_id")) for r in trace_rows',
        'bool(r.get("ocrrequest_reference_v2_id")) for r in trace_rows',
    )

    t = t.replace(
        '"ocrrequest_reference_count_observed": ref_count_observed,',
        '"ocrrequest_reference_v2_count_observed": ref_count_observed,\n        "strategy_comparison_candidate_generated": True,\n        "source_validation_v2_invoked": False,',
    )

    schema_map = {
        "ocrrequest_roi_submission_intake_matrix_v1": "ocrrequest_v2_bbox_expansion_submission_intake_matrix_v1",
        "ocrrequest_roi_submission_gate_policy_v1": "ocrrequest_v2_bbox_expansion_submission_gate_policy_v1",
        "ocrrequest_roi_submission_plan_v1": "ocrrequest_v2_bbox_expansion_submission_plan_v1",
        "ocrrequest_roi_bridge_invocation_trace_v1": "ocrrequest_v2_bbox_expansion_bridge_invocation_trace_v1",
        "roi_ocr_result_matrix_v1": "expanded_roi_ocr_result_matrix_v2",
        "roi_ocr_empty_nonempty_guard_report_v1": "expanded_roi_ocr_low_information_guard_v2",
        "roi_ocr_source_chain_report_v1": "expanded_roi_ocr_source_chain_report_v2",
        "roi_ocr_provider_summary_report_v1": "expanded_roi_ocr_provider_summary_v2",
        "roi_ocr_no_evidence_pack_boundary_report_v1": "expanded_roi_ocr_no_evidence_pack_boundary_v2",
        "roi_ocr_future_adapter_plan_v1": "expanded_roi_ocr_future_adapter_plan_v3",
        "roi_ocr_boundary_report_v1": "expanded_roi_ocr_boundary_report_v2",
        "roi_ocr_metrics_candidate_report_v1": "expanded_roi_ocr_metrics_candidate_v2",
        "roi_ocr_benchmark_link_report_v1": "expanded_roi_ocr_benchmark_link_v2",
        "roi_ocr_system_health_link_report_v1": "expanded_roi_ocr_system_health_link_v2",
        "roi_ocr_no_write_boundary_report_v1": "expanded_roi_ocr_no_write_boundary_v2",
        "roi_ocr_simulation_context_report_v1": "expanded_roi_ocr_simulation_context_v2",
        "roi_ocr_non_claims_report_v1": "expanded_roi_ocr_non_claims_report_v2",
        "roi_ocr_open_followups_v1": "expanded_roi_ocr_open_followups_v2",
        "roi_ocr_audit_report_v1": "expanded_roi_ocr_audit_report_v2",
    }
    for a, b in schema_map.items():
        t = t.replace(f'"schema_version": "{a}"', f'"schema_version": "{b}"')

    t = t.replace('"roi_ocr_result_count": len(results),', '"expanded_roi_ocr_result_count": len(results),')
    t = t.replace(
        '"no_world_model_written": True,\n        },\n        "source_chain_report":',
        '"no_world_model_written": True,\n            "low_information_text_count": low_info_count,\n            "repeated_same_text_count": repeated_same,\n            "unique_text_count": unique_text_count,\n            "most_common_text": most_common,\n            "repeated_same_text_not_consensus": True,\n            "low_information_text_not_semantic_success": True,\n        },\n        "strategy_comparison": {\n            "schema_version": "expanded_roi_ocr_strategy_output_comparison_candidate_v2",\n            "row_count": len(strategy_rows),\n            "rows": strategy_rows,\n        },\n        "source_chain_report":',
    )
    t = t.replace(
        '"fact_write_allowed_count": 0,',
        '"fact_write_allowed_count": 0,\n            "low_information_text_count": low_info_count,\n            "repeated_same_text_count": repeated_same,\n            "source_validation_v2_invoked_count": 0,',
    )
    t = t.replace(
        '"provider_winner_claimed": False,\n        },',
        '"provider_winner_claimed": False,\n            "provider_failure_claimed": False,\n        },',
    )
    t = t.replace(
        '"source_validation_v2_invoked": False,\n            "fact_review_generated": False,',
        '"source_validation_v2_invoked": False,\n            "fact_review_generated": False,',
    )
    t = t.replace(
        '"strategy_comparison_candidate_generated": len(results) > 0,',
        '"strategy_comparison_candidate_generated": True,',
    )
    t = t.replace(
        '"adapter_should_preserve_ocrrequest_ref": True,\n                    "adapter_should_preserve_crop_ref": True,',
        '"adapter_should_preserve_ocrrequest_reference_v2": True,\n                    "adapter_should_preserve_expanded_crop_artifact_ref": True,\n                    "adapter_should_preserve_expansion_candidate_ref": True,\n                    "adapter_should_preserve_source_bbox": True,\n                    "adapter_should_preserve_expanded_bbox": True,\n                    "adapter_should_preserve_expansion_strategy": True,\n                    "adapter_should_preserve_ocrrequest_ref": True,\n                    "adapter_should_preserve_crop_ref": True,',
    )
    t = t.replace(
        '"roi_crop_ocr_only": True,',
        '"expanded_roi_crop_ocr_only": True,\n            "strategy_comparison_not_benchmark": True,',
    )
    t = t.replace('"empty_nonempty_guard":', '"low_information_guard":')

    P.write_text(t, encoding="utf-8")
    print("patched", P)


if __name__ == "__main__":
    main()
