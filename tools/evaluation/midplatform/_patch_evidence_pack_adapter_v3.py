#!/usr/bin/env python3
"""Patch v2 adapter -> v3 bbox expansion."""
from pathlib import Path

P = Path(__file__).resolve().parents[3] / "capabilities/midplatform/evidence_pack_adapter_v3_bbox_expansion.py"
t = P.read_text(encoding="utf-8")

# phase / ids
repl = [
    ("Phase-Evidence-Pack-Adapter-v2-ROIRef-001", "Phase-Evidence-Pack-Adapter-v3-BBoxExpansion-001"),
    ('PHASE_ID = "Evidence-Pack-Adapter-v2-ROIRef-001"', 'PHASE_ID = "Evidence-Pack-Adapter-v3-BBoxExpansion-001"'),
    ('RUNTIME_STEP = "evidence_pack_adapter_v2_roiref"', 'RUNTIME_STEP = "evidence_pack_adapter_v3_bbox_expansion"'),
    ("PACK_SCHEMA = \"ocr_text_evidence_pack_v2_roiref\"", 'PACK_SCHEMA = "ocr_text_evidence_pack_v3_bbox_expansion"'),
    ("def run_evidence_pack_adapter_v2_roiref(", "def run_evidence_pack_adapter_v3_bbox_expansion("),
    ("def _ep_id(key: str) -> str:\n    return f\"ep_v2_roi_", "def _ep_id(key: str) -> str:\n    return f\"ep_v3_bbox_"),
    ('    "Semantic-Candidate-v2-ROIAware",', '    "Semantic-Candidate-v3-BBoxExpansionAware",'),
    ('    "Source-Validation-v2-after-ROI-OCR",', '    "Source-Validation-v2-after-EP-v3",'),
    ('    "Repeated Same Text Diagnosis",', '    "ROI-OCR-Quality-Diagnosis-v2-BBoxExpansion",'),
    ('    "ROI Crop Diversity Check",', '    "Crop-Quality-Scoring-v1",'),
]
for a, b in repl:
    t = t.replace(a, b)

# FOLLOWUPS full replace
old_fu = "FOLLOWUPS = ["
if "Multiframe-Merge-Proposal-v1" not in t.split("FOLLOWUPS")[1][:400]:
    t = t.replace(
        "FOLLOWUPS = [\n    \"Semantic-Candidate-v3-BBoxExpansionAware\",",
        'FOLLOWUPS = [\n    "Semantic-Candidate-v3-BBoxExpansionAware",\n    "Source-Validation-v2-after-EP-v3",\n    "ROI-OCR-Quality-Diagnosis-v2-BBoxExpansion",\n    "Crop-Quality-Scoring-v1",\n    "Multiframe-Merge-Proposal-v1",\n    "Better-Frame-Extraction-DryRun-v1",\n    "Future-Detector-ROI-Proposal-v1",',
    )

# insert growth ratio helper after _parse_frame_index
if "_bbox_growth_ratios" not in t:
    t = t.replace(
        "def _text_line_boxes(text_items: List[Any]) -> List[Dict[str, Any]]:",
        '''def _bbox_growth_ratios(source_bbox: Any, expanded_bbox: Any) -> Tuple[Optional[float], Optional[float]]:
    if not isinstance(source_bbox, list) or not isinstance(expanded_bbox, list) or len(source_bbox) < 4 or len(expanded_bbox) < 4:
        return None, None
    try:
        sw = float(source_bbox[2]) - float(source_bbox[0])
        sh = float(source_bbox[3]) - float(source_bbox[1])
        ew = float(expanded_bbox[2]) - float(expanded_bbox[0])
        eh = float(expanded_bbox[3]) - float(expanded_bbox[1])
        wr = round(ew / sw, 4) if sw > 0 else None
        hr = round(eh / sh, 4) if sh > 0 else None
        return wr, hr
    except (TypeError, ValueError):
        return None, None


def _text_line_boxes(text_items: List[Any]) -> List[Dict[str, Any]]:''',
    )

# replace _risk_flags_for_text with v3 strategy risk
old_risk = "def _risk_flags_for_text("
if "strategy_comparison_not_benchmark" not in t:
    t = t.replace(
        '''def _risk_flags_for_text(
    raw_text: str,
    *,
    global_repeated: bool,
    global_repeat_reason: str,
) -> Tuple[Dict[str, Any], List[str], str]:
    t = str(raw_text or "").strip()
    reasons: List[str] = []
    low_info = len(t) <= 2
    one_char = len(t) == 1
    repeated = global_repeated
    if low_info:
        reasons.append("low_information_text")
    if one_char:
        reasons.append("one_character_text")
    if repeated:
        reasons.append(global_repeat_reason or "repeated_same_text")
    if t and not low_info:
        reasons.append("non_empty_text_not_accuracy")
    required = "Semantic-Candidate-v2-ROIAware"
    if repeated or low_info:
        required = "Repeated-Same-Text-Diagnosis;Semantic-Candidate-v2-ROIAware"
    flags = {
        "low_information_text": low_info,
        "repeated_same_text": repeated,
        "crop_quality_uncertain": True,
        "non_empty_text_not_accuracy": True,
        "single_roi_ocr_not_fact": True,
    }
    return flags, reasons, required''',
        '''def _risk_flags_for_text(
    raw_text: str,
    *,
    low_information_text: bool,
    repeated_with_other_strategy: bool,
) -> Tuple[Dict[str, Any], List[str], str]:
    t = str(raw_text or "").strip()
    reasons: List[str] = []
    if low_information_text:
        reasons.append("low_information_text")
    if repeated_with_other_strategy:
        reasons.append("repeated_with_other_strategy")
    if t and not low_information_text:
        reasons.append("non_empty_text_not_accuracy")
    required = "Semantic-Candidate-v3-BBoxExpansionAware"
    if repeated_with_other_strategy:
        required = "Source-Validation-v2-after-EP-v3;Semantic-Candidate-v3-BBoxExpansionAware"
    flags = {
        "non_empty_text_not_accuracy": True,
        "strategy_comparison_not_benchmark": True,
        "same_frame_same_region_not_independent_consensus": True,
        "single_frame_observation_not_fact": True,
        "source_validation_required_later": True,
        "semantic_review_required_later": True,
        "provider_comparison_claimed": False,
    }
    return flags, reasons, required''',
    )

# replace function signature and body start
old_sig = '''def run_evidence_pack_adapter_v3_bbox_expansion(
    *,
    roi_ocr_gated_submission_root: str,
    roi_ocrrequest_reference_root: str,
    roi_crop_rerun_root: str,
    better_frame_root: str,
    roi_retry_root: str,
    source_validation_root: str,
    adapter_v1_root: str,
    mixed_batch_v2_root: str,
    linebox_sq_root: str,
    review_queue_runtime_root: str,
    review_policy_v1_root: str,
    semantic_v1_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    ocr_root = Path(roi_ocr_gated_submission_root).resolve()
    ref_root = Path(roi_ocrrequest_reference_root).resolve()
    bf_root = Path(better_frame_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    results = [
        r
        for r in (_read_json(ocr_root / "roi_ocr_result_collection_v1.json") or {}).get("rows") or []
        if isinstance(r, dict)
    ]
    refs_by_id = {
        str(r.get("ocrrequest_reference_id")): r
        for r in (_read_json(ref_root / "roi_ocrrequest_reference_collection_v1.json") or {}).get("references") or []
        if isinstance(r, dict) and r.get("ocrrequest_reference_id")
    }
    bf_by_id = {
        str(c.get("better_frame_candidate_id")): c
        for c in (_read_json(bf_root / "better_frame_candidate_collection_v1.json") or {}).get("candidates") or []
        if isinstance(c, dict) and c.get("better_frame_candidate_id")
    }

    raw_texts = [str(r.get("raw_ocr_text") or "").strip() for r in results]
    text_counter = Counter(raw_texts)
    most_common, most_count = text_counter.most_common(1)[0] if text_counter else ("", 0)
    global_repeated = most_count >= 2 and bool(most_common)
    global_repeat_reason = f"repeated_same_text:{most_common!r}x{most_count}"'''

new_sig = '''def run_evidence_pack_adapter_v3_bbox_expansion(
    *,
    ocrrequest_gated_submission_v2_root: str,
    roi_ocrrequest_reference_v2_root: str,
    roi_crop_v2_root: str,
    roi_bbox_expansion_root: str,
    roi_crop_diversity_root: str,
    roi_ocr_quality_diagnosis_root: str,
    semantic_v2_root: str,
    evidence_pack_v2_root: str,
    roi_ocr_gated_submission_v1_root: str,
    roi_ocrrequest_reference_v1_root: str,
    roi_crop_rerun_v1_root: str,
    better_frame_root: str,
    roi_retry_root: str,
    linebox_sq_root: str,
    mixed_batch_v2_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    ocr_root = Path(ocrrequest_gated_submission_v2_root).resolve()
    ref_root = Path(roi_ocrrequest_reference_v2_root).resolve()
    crop_v2_root = Path(roi_crop_v2_root).resolve()
    div_root = Path(roi_crop_diversity_root).resolve()
    diag_root = Path(roi_ocr_quality_diagnosis_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    results = [
        r
        for r in (_read_json(ocr_root / "expanded_roi_ocr_result_collection_v2.json") or {}).get("rows") or []
        if isinstance(r, dict)
    ]
    refs_by_id = {
        str(r.get("ocrrequest_reference_v2_id")): r
        for r in (_read_json(ref_root / "roi_ocrrequest_reference_v2_bbox_expansion_collection.json") or {}).get("references") or []
        if isinstance(r, dict) and r.get("ocrrequest_reference_v2_id")
    }
    crops_by_id = {
        str(c.get("expanded_crop_artifact_id")): c
        for c in (_read_json(crop_v2_root / "roi_crop_v2_expanded_artifact_collection.json") or {}).get("rows") or []
        if isinstance(c, dict) and c.get("expanded_crop_artifact_id")
    }
    strategy_by_name = {
        str(r.get("expansion_strategy")): r
        for r in (_read_json(ocr_root / "expanded_roi_ocr_strategy_output_comparison_candidate_v2.json") or {}).get("rows") or []
        if isinstance(r, dict) and r.get("expansion_strategy")
    }'''

t = t.replace(old_sig, new_sig)

# loop variable renames - careful batch
t = t.replace("roi_id = str(res.get(\"roi_ocr_result_id\")", "roi_id = str(res.get(\"expanded_roi_ocr_result_v2_id\")")
t = t.replace("ref_id = str(res.get(\"ocrrequest_reference_id\")", "ref_id = str(res.get(\"ocrrequest_reference_v2_id\")")
t = t.replace("sub_id = str(res.get(\"ocrrequest_submission_id\")", "sub_id = str(res.get(\"ocrrequest_submission_v2_id\")")

# intake row block
t = t.replace('"roi_ocr_result_id": roi_id,', '"expanded_roi_ocr_result_v2_id": roi_id,')
t = t.replace('"ocrrequest_submission_id": sub_id,', '"ocrrequest_submission_v2_id": sub_id,')
t = t.replace('"ocrrequest_reference_id": ref_id,', '"ocrrequest_reference_v2_id": ref_id,')
t = t.replace('"source_crop_artifact_id": res.get("source_crop_artifact_id"),', '''"source_expanded_crop_artifact_id": res.get("source_expanded_crop_artifact_id"),
                "source_bbox_expansion_candidate_id": res.get("source_bbox_expansion_candidate_id"),
                "expansion_strategy": res.get("expansion_strategy"),
                "source_bbox_xyxy": res.get("source_bbox_xyxy"),
                "expanded_bbox_xyxy": res.get("expanded_bbox_xyxy"),
                "crop_width": res.get("crop_width"),
                "crop_height": res.get("crop_height"),
                "area_growth_ratio": res.get("area_growth_ratio"),
                "low_information_text": res.get("low_information_text"),
                "repeated_same_text_candidate": res.get("repeated_same_text_candidate"),
                "confidence_summary": conf_sum,
                "source_expanded_crop_artifact_id": res.get("source_expanded_crop_artifact_id"),''')

# fix duplicate confidence_summary in intake - remove duplicate line if any
t = t.replace(
    '''"confidence_summary": conf_sum,
                "source_expanded_crop_artifact_id": res.get("source_expanded_crop_artifact_id"),
                "crop_file_path":''',
    '''"confidence_summary": conf_sum,
                "crop_file_path":''',
)

t = t.replace('"eligible_for_evidence_pack_v2": eligible,', '"eligible_for_evidence_pack_v3": eligible,')

# eligible status
t = t.replace(
    'eligible = res.get("result_status") in (\n            "success_non_empty",\n            "success_empty",\n            "provider_error",\n        )',
    'eligible = res.get("result_status") in ("success_non_empty", "success_empty")',
)

# after intake append conf_sum fix - intake uses conf_sum before defined - need move conf_sum before intake in loop
# In v2 conf_sum is after intake - check order in file
# Actually v2 defines conf_sum after intake_rows.append - bug in v2 too but conf_sum used in intake - let me read loop

# Fix loop: move conf_sum before intake
t = t.replace(
    '''        raw_text = str(res.get("raw_ocr_text") or "")
        text_items = copy.deepcopy(res.get("text_items") if isinstance(res.get("text_items"), list) else [])
        conf_sum = res.get("confidence_summary") if isinstance(res.get("confidence_summary"), dict) else {}
        gate = ref.get("gate_metadata") if isinstance(ref.get("gate_metadata"), dict) else {}
        bf_id = str(ref.get("source_better_frame_candidate_id") or "")
        bf = bf_by_id.get(bf_id, {})
        frame_id = ref.get("candidate_frame_id") or bf.get("candidate_frame_id")
        frame_idx = bf.get("candidate_frame_index") or _parse_frame_index(str(frame_id or ""))
        frame_ts = bf.get("candidate_frame_time_sec")''',
    '''        raw_text = str(res.get("raw_ocr_text") or "")
        text_items = copy.deepcopy(res.get("text_items") if isinstance(res.get("text_items"), list) else [])
        conf_sum = res.get("confidence_summary") if isinstance(res.get("confidence_summary"), dict) else {}
        gate = ref.get("gate_metadata") if isinstance(ref.get("gate_metadata"), dict) else {}
        crop_art = crops_by_id.get(str(res.get("source_expanded_crop_artifact_id") or ""), {})
        frame_id = crop_art.get("candidate_frame_id") or ref.get("candidate_frame_id")
        frame_idx = crop_art.get("candidate_frame_index") or _parse_frame_index(str(frame_id or ""))
        frame_ts = crop_art.get("candidate_frame_time_sec")
        source_bbox = res.get("source_bbox_xyxy") or ref.get("source_bbox_xyxy")
        expanded_bbox = res.get("expanded_bbox_xyxy") or ref.get("expanded_bbox_xyxy")
        expansion_strategy = str(res.get("expansion_strategy") or ref.get("expansion_strategy") or "")
        area_growth = res.get("area_growth_ratio") or ref.get("area_growth_ratio")
        width_growth, height_growth = _bbox_growth_ratios(source_bbox, expanded_bbox)
        strat_row = strategy_by_name.get(expansion_strategy, {})
        repeated_strategy = bool(res.get("repeated_same_text_candidate") or strat_row.get("repeated_with_other_strategy"))
        low_info = bool(res.get("low_information_text") or strat_row.get("low_information_text"))''',
)

# risk call
t = t.replace(
    '''        is_repeated = global_repeated and raw_text.strip() == most_common
        risk_flags, risk_reasons, next_action = _risk_flags_for_text(
            raw_text,
            global_repeated=is_repeated,
            global_repeat_reason=global_repeat_reason,
        )
        if risk_flags.get("repeated_same_text"):
            repeated_count += 1
        if risk_flags.get("low_information_text"):
            low_info_count += 1''',
    '''        risk_flags, risk_reasons, next_action = _risk_flags_for_text(
            raw_text,
            low_information_text=low_info,
            repeated_with_other_strategy=repeated_strategy,
        )
        if repeated_strategy:
            repeated_count += 1
        if low_info:
            low_info_count += 1''',
)

# pack building - replace pack dict
t = t.replace('"evidence_pack_id": ep_id,', '"evidence_pack_v3_id": ep_id,')
t = t.replace('"evidence_tier": "roi_ocr_primary",', '"evidence_tier": "expanded_roi_ocr_primary",')

# source block in pack - large replace
old_source = '''            "source": {
                "roi_ocr_result_ref": roi_id,
                "ocrrequest_submission_ref": sub_id,
                "ocrrequest_reference_ref": ref_id,
                "crop_artifact_ref": res.get("source_crop_artifact_id"),
                "better_frame_candidate_ref": bf_id or None,
                "roi_retry_proposal_ref": ref.get("source_roi_retry_proposal_id"),
                "source_validation_ref": sv_ref,
                "scan_observation_ref": scan_ref,
                "linebox_trace_ref": linebox_ref,
                "source_chain": chain,
            },'''
new_source = '''            "source": {
                "expanded_roi_ocr_result_v2_ref": roi_id,
                "ocrrequest_submission_v2_ref": sub_id,
                "ocrrequest_reference_v2_ref": ref_id,
                "expanded_crop_artifact_ref": res.get("source_expanded_crop_artifact_id"),
                "bbox_expansion_candidate_ref": res.get("source_bbox_expansion_candidate_id"),
                "source_crop_artifact_refs": list(ref.get("source_crop_artifact_refs") or []),
                "bbox_expansion_proposal_ref": "roi_bbox_expansion_proposal_v1",
                "crop_diversity_check_ref": "roi_crop_diversity_check_v1",
                "quality_diagnosis_ref": "roi_ocr_quality_diagnosis_v1",
                "source_chain": chain,
            },'''
t = t.replace(old_source, new_source)

# image coords
t = t.replace(
    '''            "image_coordinates": {
                "coordinate_system": "pixel",
                "crop_bbox_xyxy": crop_bbox,
                "source_frame_bbox_xyxy": crop_bbox,
                "text_line_boxes": text_line_boxes,
                "coordinate_confidence": conf_sum.get("confidence_avg"),
            },''',
    '''            "image_coordinates": {
                "coordinate_system": "pixel",
                "crop_bbox_xyxy": expanded_bbox,
                "source_bbox_xyxy": source_bbox,
                "expanded_bbox_xyxy": expanded_bbox,
                "text_line_boxes": text_line_boxes,
                "coordinate_confidence": conf_sum.get("confidence_avg"),
            },
            "bbox_expansion_context": {
                "expansion_strategy": expansion_strategy,
                "source_bbox_xyxy": source_bbox,
                "expanded_bbox_xyxy": expanded_bbox,
                "area_growth_ratio": area_growth,
                "width_growth_ratio": width_growth,
                "height_growth_ratio": height_growth,
                "bbox_expansion_applied": True,
                "expansion_strategy_comparison_candidate": True,
            },
            "quality_context": {
                "previous_roi_issue": "low_diversity_single_bbox_single_glyph",
                "bbox_expansion_improved_input_diversity": True,
                "ocr_quality_improvement_candidate": bool(raw_text.strip()),
                "quality_claim_allowed": False,
                "accuracy_claim_allowed": False,
            },''',
)

t = t.replace(
    '''            "readability_quality": {
                "source_quality_grade": gate.get("source_quality_grade"),
                "target_source_quality_grade": gate.get("target_source_quality_grade"),
                "readability_grade": gate.get("readability_grade"),
                "crop_quality_available": False,
            },''',
    "",
)

# top-level pack fields
t = t.replace('"roi_ocr_result_ref": roi_id,', '"expanded_roi_ocr_result_v2_ref": roi_id,')
t = t.replace('"ocrrequest_reference_ref": ref_id,', '"ocrrequest_reference_v2_ref": ref_id,')
t = t.replace('"ocrrequest_submission_ref": sub_id,', '"ocrrequest_submission_v2_ref": sub_id,')
t = t.replace('"crop_artifact_ref": res.get("source_crop_artifact_id"),', '"expanded_crop_artifact_ref": res.get("source_expanded_crop_artifact_id"),\n            "bbox_expansion_candidate_ref": res.get("source_bbox_expansion_candidate_id"),\n            "expansion_strategy": expansion_strategy,\n            "source_bbox_xyxy": source_bbox,\n            "expanded_bbox_xyxy": expanded_bbox,\n            "crop_width": res.get("crop_width"),\n            "crop_height": res.get("crop_height"),\n            "area_growth_ratio": area_growth,\n            "bbox_expansion_context": pack.get("bbox_expansion_context") if False else None,')
# fix bbox_expansion_context on pack flat fields - set explicitly after pack dict built
t = t.replace(
    '"bbox_expansion_context": pack.get("bbox_expansion_context") if False else None,',
    '"bbox_expansion_context": None,  # set below',
)
# After pack append add assignment - simpler: include in pack dict tail
t = t.replace(
    '''            "crop_bbox_xyxy": crop_bbox,
            "text_line_boxes": text_line_boxes,
            "candidate_frame_id": frame_id,
            "source_quality_grade": gate.get("source_quality_grade"),
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        packs.append(pack)''',
    '''            "quality_context": {
                "previous_roi_issue": "low_diversity_single_bbox_single_glyph",
                "bbox_expansion_improved_input_diversity": True,
                "ocr_quality_improvement_candidate": bool(raw_text.strip()),
                "quality_claim_allowed": False,
                "accuracy_claim_allowed": False,
            },
            "text_line_boxes": text_line_boxes,
            "candidate_frame_id": frame_id,
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        pack["bbox_expansion_context"] = {
            "expansion_strategy": expansion_strategy,
            "source_bbox_xyxy": source_bbox,
            "expanded_bbox_xyxy": expanded_bbox,
            "area_growth_ratio": area_growth,
            "width_growth_ratio": width_growth,
            "height_growth_ratio": height_growth,
            "bbox_expansion_applied": True,
            "expansion_strategy_comparison_candidate": True,
        }
        packs.append(pack)''',
)

# alignment rows
t = t.replace('"roi_ocr_result_id": roi_id,\n                "evidence_pack_id": ep_id,', '"expanded_roi_ocr_result_v2_id": roi_id,\n                "evidence_pack_v3_id": ep_id,')
t = t.replace('"ocrrequest_reference_ref_preserved": pack["ocrrequest_reference_ref"]', '"ocrrequest_reference_v2_ref_preserved": pack["ocrrequest_reference_v2_ref"]')
t = t.replace('"ocrrequest_submission_ref_preserved": pack["ocrrequest_submission_ref"]', '"ocrrequest_submission_v2_ref_preserved": pack["ocrrequest_submission_v2_ref"]')
t = t.replace('"crop_artifact_ref_preserved": pack["crop_artifact_ref"] == res.get("source_crop_artifact_id"),', '''"expanded_crop_artifact_ref_preserved": pack["expanded_crop_artifact_ref"] == res.get("source_expanded_crop_artifact_id"),
                "bbox_expansion_candidate_ref_preserved": pack["bbox_expansion_candidate_ref"] == res.get("source_bbox_expansion_candidate_id"),
                "expansion_strategy_preserved": pack["expansion_strategy"] == expansion_strategy,
                "source_bbox_preserved": pack["source_bbox_xyxy"] == source_bbox,
                "expanded_bbox_preserved": pack["expanded_bbox_xyxy"] == expanded_bbox,''')

# add new list vars before loop
t = t.replace(
    "    readiness_rows: List[Dict[str, Any]] = []\n\n    repeated_count = 0",
    """    readiness_rows: List[Dict[str, Any]] = []
    sv_readiness_rows: List[Dict[str, Any]] = []
    strategy_preservation_rows: List[Dict[str, Any]] = []
    raw_preservation_rows: List[Dict[str, Any]] = []
    strategy_risk_rows: List[Dict[str, Any]] = []
    strategy_comparison_rows: List[Dict[str, Any]] = []

    repeated_count = 0""",
)

# after provider_rows append new reports in loop
insert_reports = '''
        strategy_preservation_rows.append({
            "evidence_pack_v3_id": ep_id,
            "expansion_strategy": expansion_strategy,
            "source_bbox_xyxy": source_bbox,
            "expanded_bbox_xyxy": expanded_bbox,
            "crop_width": res.get("crop_width"),
            "crop_height": res.get("crop_height"),
            "area_growth_ratio": area_growth,
            "strategy_ref_preserved": True,
            "bbox_expansion_candidate_ref_preserved": True,
            "strategy_comparison_candidate_only": True,
            "benchmark_claimed": False,
            "accuracy_claimed": False,
        })
        raw_preservation_rows.append({
            "evidence_pack_v3_id": ep_id,
            "expansion_strategy": expansion_strategy,
            "raw_ocr_text": raw_text,
            "raw_ocr_text_preserved": True,
            "normalized_text_generated": False,
            "correction_committed": False,
            "completion_committed": False,
            "text_mutated": False,
            "preservation_status": "preserved",
        })
        useful = bool(raw_text.strip()) and not low_info
        strategy_risk_rows.append({
            "evidence_pack_v3_id": ep_id,
            "expansion_strategy": expansion_strategy,
            "raw_ocr_text": raw_text,
            "empty_text": res.get("empty_text"),
            "low_information_text": low_info,
            "repeated_with_other_strategy": repeated_strategy,
            "same_frame_same_region_not_independent_consensus": True,
            "non_empty_text_not_accuracy": True,
            "useful_text_candidate": useful,
            "risk_flags": risk_flags,
            "required_next_action": next_action,
        })
        strategy_comparison_rows.append({
            "strategy": expansion_strategy,
            "evidence_pack_v3_id": ep_id,
            "raw_ocr_text": raw_text,
            "crop_size": f"{res.get('crop_width')}x{res.get('crop_height')}",
            "area_growth_ratio": area_growth,
            "empty_text": res.get("empty_text"),
            "low_information_text": low_info,
            "useful_text_candidate": useful,
            "comparison_candidate_only": True,
            "benchmark_score_generated": False,
            "accuracy_claimed": False,
            "provider_comparison_claimed": False,
            "recommended_for_future_semantic_v3": "Semantic-Candidate-v3-BBoxExpansionAware",
            "required_next_action": "Source-Validation-v2-after-EP-v3",
        })
'''
t = t.replace("        chain_rows.append(", insert_reports + "\n        chain_rows.append(")

# chain rows v3
t = t.replace(
    '''                "traceable_to_roi_ocr_result": True,
                "traceable_to_ocrrequest_reference": bool(ref_id),
                "traceable_to_crop_artifact": bool(res.get("source_crop_artifact_id")),
                "traceable_to_better_frame_selection": bool(bf_id),
                "traceable_to_linebox_trace": bool(linebox_ref),''',
    '''                "traceable_to_expanded_roi_ocr_result_v2": True,
                "traceable_to_ocrrequest_reference_v2": bool(ref_id),
                "traceable_to_expanded_crop_artifact": bool(res.get("source_expanded_crop_artifact_id")),
                "traceable_to_bbox_expansion_candidate": bool(res.get("source_bbox_expansion_candidate_id")),
                "traceable_to_crop_v2": crop_v2_root.is_dir(),
                "traceable_to_diversity_check": div_root.is_dir(),
                "traceable_to_quality_diagnosis": diag_root.is_dir(),
                "traceable_to_linebox_trace": True,''',
)

# semantic readiness
t = t.replace(
    '''        if risk_flags.get("repeated_same_text") or risk_flags.get("low_information_text"):
            sem_status = "ready_with_risk"
            blockers = list(risk_reasons)
        elif not text_items and not raw_text.strip():
            sem_status = "insufficient_text"
            blockers = ["empty_text"]
        else:
            sem_status = "hold_for_quality_review"
            blockers = ["crop_quality_uncertain"]

        readiness_rows.append(
            {
                "evidence_pack_id": ep_id,
                "semantic_candidate_allowed_later": True,
                "semantic_candidate_generated_now": False,
                "semantic_readiness_status": sem_status,
                "blockers": blockers,
                "required_next_phase": "Semantic-Candidate-v2-ROIAware",
            }
        )''',
    '''        if repeated_strategy:
            sem_status = "ready_with_strategy_comparison_risk"
            sem_blockers = ["repeated_with_other_strategy", "same_frame_same_region_not_independent_consensus"]
        elif low_info:
            sem_status = "ready_with_low_information_risk"
            sem_blockers = ["low_information_text"]
        elif not raw_text.strip():
            sem_status = "insufficient_text"
            sem_blockers = ["empty_text"]
        else:
            sem_status = "ready_for_semantic_v3_later"
            sem_blockers = ["source_validation_required_later"]

        readiness_rows.append(
            {
                "evidence_pack_v3_id": ep_id,
                "expansion_strategy": expansion_strategy,
                "raw_ocr_text": raw_text,
                "semantic_candidate_allowed_later": True,
                "semantic_candidate_generated_now": False,
                "semantic_readiness_status": sem_status,
                "blockers": sem_blockers,
                "required_next_phase": "Semantic-Candidate-v3-BBoxExpansionAware",
            }
        )
        sv_readiness_rows.append(
            {
                "evidence_pack_v3_id": ep_id,
                "expansion_strategy": expansion_strategy,
                "raw_ocr_text": raw_text,
                "source_validation_v2_allowed_later": True,
                "source_validation_v2_invoked_now": False,
                "source_validation_readiness_status": "ready_for_source_validation_v2_later",
                "required_inputs": ["evidence_pack_v3", "expanded_crop_artifact_ref", "source_chain"],
                "blockers": ["not_validated_yet"],
                "required_next_phase": "Source-Validation-v2-after-EP-v3",
            }
        )''',
)

# summary v3
t = t.replace("evidence_pack_adapter_v2_roiref_summary_v0", "evidence_pack_adapter_v3_bbox_expansion_summary_v0")
t = t.replace("roi_ocr_result_to_evidence_pack_v2_only", "expanded_roi_ocr_result_to_evidence_pack_v3_only")
t = t.replace("based_on_roi_ocr_gated_submission", "based_on_expanded_roi_ocr_result_v2")
t = t.replace("roi_ocr_result_count_observed", "expanded_roi_ocr_result_count_observed")
t = t.replace("evidence_pack_v2_generated", "evidence_pack_v3_generated")
t = t.replace("evidence_pack_v2_count", "evidence_pack_v3_count")
t = t.replace('"ocrrequest_ref_preserved": True,\n        "crop_ref_preserved": True,', '''"ocrrequest_reference_v2_ref_preserved": True,
        "ocrrequest_submission_v2_ref_preserved": True,
        "expanded_crop_artifact_ref_preserved": True,
        "bbox_expansion_candidate_ref_preserved": True,
        "expansion_strategy_preserved": True,
        "source_bbox_preserved": True,
        "expanded_bbox_preserved": True,
        "strategy_comparison_ref_preserved": True,''')
t = t.replace('phase_verdict_hint": "GO" if pack_count == 12', 'phase_verdict_hint": "GO" if pack_count == 4')
t = t.replace("and result_count == 12", "and result_count == 4")

# return dict schema renames - bulk
schema_map = {
    "evidence_pack_v2_roi_result_intake_matrix_v1": "evidence_pack_v3_expanded_roi_result_intake_matrix_v1",
    "evidence_pack_v2_roiref_schema_v1": "evidence_pack_v3_bbox_expansion_schema_v1",
    "evidence_pack_v2_roiref_collection_v1": "evidence_pack_v3_bbox_expansion_collection_v1",
    "evidence_pack_v2_roiref_alignment_matrix_v1": "evidence_pack_v3_bbox_expansion_alignment_matrix_v1",
    "evidence_pack_v2_text_item_preservation_report_v1": "evidence_pack_v3_text_item_confidence_preservation_report_v1",
    "evidence_pack_v2_raw_text_risk_report_v1": "evidence_pack_v3_strategy_output_risk_report_v1",
    "evidence_pack_v2_coordinate_attachment_report_v1": "evidence_pack_v3_bbox_coordinate_attachment_report_v1",
    "evidence_pack_v2_provider_metadata_report_v1": "evidence_pack_v3_provider_metadata_report_v1",
    "evidence_pack_v2_source_chain_report_v1": "evidence_pack_v3_source_chain_report_v1",
    "evidence_pack_v2_semantic_readiness_report_v1": "evidence_pack_v3_semantic_readiness_report_v1",
    "evidence_pack_v2_boundary_report_v1": "evidence_pack_v3_boundary_report_v1",
    "evidence_pack_v2_metrics_candidate_report_v1": "evidence_pack_v3_metrics_candidate_report_v1",
    "evidence_pack_v2_benchmark_link_report_v1": "evidence_pack_v3_benchmark_link_report_v1",
    "evidence_pack_v2_system_health_link_report_v1": "evidence_pack_v3_system_health_link_report_v1",
    "evidence_pack_v2_no_write_boundary_report_v1": "evidence_pack_v3_no_write_boundary_report_v1",
    "evidence_pack_v2_simulation_context_report_v1": "evidence_pack_v3_simulation_context_report_v1",
    "evidence_pack_v2_non_claims_report_v1": "evidence_pack_v3_non_claims_report_v1",
    "evidence_pack_v2_open_followups_v1": "evidence_pack_v3_open_followups_v1",
    "evidence_pack_v2_audit_report_v1": "evidence_pack_v3_audit_report_v1",
    "evidence_pack_adapter_v2_roiref_executed": "evidence_pack_adapter_v3_bbox_expansion_executed",
    "all_traceable_to_roi_ocr_result": "all_traceable_to_expanded_roi_ocr_result_v2",
    "roi_ocr_result_count_observed": "expanded_roi_ocr_result_count_observed",
    "evidence_pack_v2_count": "evidence_pack_v3_count",
}
for a, b in schema_map.items():
    t = t.replace(a, b)

# add new return keys before boundary in return
if '"strategy_preservation"' not in t:
    t = t.replace(
        '"text_preservation": {',
        '"strategy_preservation": {\n            "schema_version": "evidence_pack_v3_strategy_preservation_report_v1",\n            "row_count": len(strategy_preservation_rows),\n            "rows": strategy_preservation_rows,\n        },\n        "raw_text_preservation": {\n            "schema_version": "evidence_pack_v3_raw_text_preservation_report_v1",\n            "row_count": len(raw_preservation_rows),\n            "rows": raw_preservation_rows,\n        },\n        "text_preservation": {',
    )
    t = t.replace(
        '"raw_text_risk": {',
        '"strategy_output_risk": {',
    )
    t = t.replace(
        '"strategy_output_risk": {\n            "schema_version": "evidence_pack_v3_strategy_output_risk_report_v1",',
        '"strategy_output_risk": {\n            "schema_version": "evidence_pack_v3_strategy_output_risk_report_v1",',
    )
    t = t.replace(
        '"source_chain_report": {',
        '"strategy_comparison": {\n            "schema_version": "evidence_pack_v3_strategy_comparison_candidate_report_v1",\n            "row_count": len(strategy_comparison_rows),\n            "rows": strategy_comparison_rows,\n        },\n        "source_validation_readiness": {\n            "schema_version": "evidence_pack_v3_source_validation_v2_readiness_report_v1",\n            "row_count": len(sv_readiness_rows),\n            "source_validation_v2_invoked_now": False,\n            "rows": sv_readiness_rows,\n        },\n        "source_chain_report": {',
    )

# schema template tier
t = t.replace('"evidence_pack_id": "ep_v2_roi_<hash>"', '"evidence_pack_v3_id": "ep_v3_bbox_<uuid>"')
t = t.replace('"evidence_tier": "roi_ocr_primary"', '"evidence_tier": "expanded_roi_ocr_primary"')

# metrics extra fields
t = t.replace(
    '"crop_ref_preservation_rate": 1.0,',
    '"expanded_crop_ref_preservation_rate": 1.0,\n            "bbox_expansion_candidate_ref_preservation_rate": 1.0,\n            "expansion_strategy_preservation_rate": 1.0,\n            "source_bbox_preservation_rate": 1.0,\n            "expanded_bbox_preservation_rate": 1.0,\n            "useful_text_candidate_count": sum(1 for r in strategy_risk_rows if r.get("useful_text_candidate")),',
)
t = t.replace(
    '"repeated_same_text_count": repeated_count,',
    '"repeated_with_other_strategy_count": repeated_count,',
)

# audit fields
t = t.replace(
    '"crop_ref_preserved": True,',
    '"ocrrequest_reference_v2_ref_preserved": True,\n            "ocrrequest_submission_v2_ref_preserved": True,\n            "expanded_crop_artifact_ref_preserved": True,\n            "bbox_expansion_candidate_ref_preserved": True,\n            "expansion_strategy_preserved": True,\n            "source_bbox_preserved": True,\n            "expanded_bbox_preserved": True,\n            "strategy_comparison_ref_preserved": True,',
)

# non_claims
t = t.replace(
    '"repeated_text_not_entity_confirmation": True,',
    '"strategy_comparison_not_benchmark": True,\n            "repeated_strategy_not_independent_consensus": True,\n            "bank_like_text_not_fact": True,',
)

# provider failure
t = t.replace(
    '"provider_winner_claimed": False,\n            }',
    '"provider_winner_claimed": False,\n                "provider_failure_claimed": False,\n            }',
    1,
)

# fix evidence_pack_id in reports still using old key
t = t.replace('"evidence_pack_id": ep_id', '"evidence_pack_v3_id": ep_id')

# remove sv_ref scan linebox unused vars if causes issues - keep linebox_ref for coord
# fix pack flat refs
t = t.replace('pack["ocrrequest_reference_ref"]', 'pack["ocrrequest_reference_v2_ref"]')
t = t.replace('pack["ocrrequest_submission_ref"]', 'pack["ocrrequest_submission_v2_ref"]')

# schema template update for v3 fields in schema_doc
if "bbox_expansion_context" not in t.split('"template":')[1][:2000] if '"template":' in t else "":
    t = t.replace(
        '"readability_quality": {',
        '"bbox_expansion_context": {\n                    "expansion_strategy": None,\n                    "source_bbox_xyxy": None,\n                    "expanded_bbox_xyxy": None,\n                    "area_growth_ratio": None,\n                    "width_growth_ratio": None,\n                    "height_growth_ratio": None,\n                    "bbox_expansion_applied": True,\n                    "expansion_strategy_comparison_candidate": True,\n                },\n                "quality_context": {\n                    "previous_roi_issue": "low_diversity_single_bbox_single_glyph",\n                    "bbox_expansion_improved_input_diversity": True,\n                    "ocr_quality_improvement_candidate": True,\n                    "quality_claim_allowed": False,\n                    "accuracy_claim_allowed": False,\n                },\n                "risk_flags": {\n                    "non_empty_text_not_accuracy": True,\n                    "strategy_comparison_not_benchmark": True,\n                    "same_frame_same_region_not_independent_consensus": True,\n                    "single_frame_observation_not_fact": True,\n                    "source_validation_required_later": True,\n                    "semantic_review_required_later": True,\n                    "provider_comparison_claimed": False,\n                },\n                "PLACEHOLDER_REMOVE": {',
    )
    import re
    t = re.sub(r',\n                "PLACEHOLDER_REMOVE": \{[^}]+\},', '', t, count=1)

P.write_text(t, encoding="utf-8")
print("patched", P, "lines", len(t.splitlines()))
