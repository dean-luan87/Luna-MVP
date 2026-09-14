#!/usr/bin/env python3
"""One-shot builder: v1 -> v2 bbox expansion gated submission capability."""
from pathlib import Path

SRC = Path(__file__).resolve().parents[3] / "capabilities/ocr_runtime/ocrrequest_gated_submission_from_roi_v1.py"
DST = SRC.parent / "ocrrequest_gated_submission_from_roi_v2_bbox_expansion.py"


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    text = text.replace("Phase-OCRRequest-Gated-Submission-from-ROI-v1-001", "Phase-OCRRequest-Gated-Submission-from-ROI-v2-BBoxExpansion-001")
    text = text.replace('PHASE_ID = "OCRRequest-Gated-Submission-from-ROI-v1-001"', 'PHASE_ID = "OCRRequest-Gated-Submission-from-ROI-v2-BBoxExpansion-001"')
    text = text.replace('RUNTIME_STEP = "ocrrequest_gated_submission_from_roi_v1"', 'RUNTIME_STEP = "ocrrequest_gated_submission_from_roi_v2_bbox_expansion"')
    text = text.replace("def run_ocrrequest_gated_submission_from_roi_v1(", "def run_ocrrequest_gated_submission_from_roi_v2_bbox_expansion(")
    text = text.replace('def _build_ocr_request(', 'def _build_ocr_request_v2(')
    text = text.replace('_build_ocr_request(ref, sub_id)', '_build_ocr_request_v2(ref, sub_id)')
    text = text.replace('return f"ocrreq_sub_', 'return f"ocrreq_sub_v2_')
    text = text.replace('return f"roi_ocr_', 'return f"expanded_roi_ocr_')
    text = text.replace('task_context="roi_ocrrequest_gated_submission_v1"', 'task_context="roi_ocrrequest_gated_submission_v2_bbox_expansion"')
    text = text.replace(
        'source_task_id=str(ref.get("ocrrequest_reference_id") or ""),',
        'source_task_id=str(ref.get("ocrrequest_reference_v2_id") or ref.get("ocrrequest_reference_id") or ""),',
    )
    text = text.replace(
        '    roi_ref = str(payload.get("roi_ref") or "")\n    if roi_ref:\n        roi_refs = [roi_ref.replace("roi_crop_xyxy:", "ocr_roi_xyxy:")]',
        '    roi_ref = str(payload.get("roi_ref") or "")\n    exp_bbox = ref.get("expanded_bbox_xyxy")\n    if roi_ref:\n        roi_refs = [roi_ref.replace("roi_expanded_xyxy:", "ocr_roi_xyxy:").replace("roi_crop_xyxy:", "ocr_roi_xyxy:")]\n    elif isinstance(exp_bbox, list) and len(exp_bbox) >= 4:\n        roi_refs = ["ocr_roi_xyxy:" + ",".join(str(int(float(v))) for v in exp_bbox)]',
    )
    for old, new in [
        ('ocrrequest_reference_id: str', 'ocrrequest_reference_v2_id: str'),
        ('"ocrrequest_reference_id": ocrrequest_reference_id', '"ocrrequest_reference_v2_id": ocrrequest_reference_v2_id'),
        ('ocrrequest_reference_id=ref_id', 'ocrrequest_reference_v2_id=ref_id'),
        ('ref.get("ocrrequest_reference_id")', 'ref.get("ocrrequest_reference_v2_id")'),
        ('roi_ocrrequest_reference_root: str', 'roi_ocrrequest_reference_v2_root: str'),
        ('ref_root = Path(roi_ocrrequest_reference_root)', 'ref_root = Path(roi_ocrrequest_reference_v2_root)'),
        ('roi_ocrrequest_reference_collection_v1.json', 'roi_ocrrequest_reference_v2_bbox_expansion_collection.json'),
        ('ref_count_observed == 12 and submitted_count == 12', 'ref_count_observed == 4 and submitted_count == 4'),
        ('ocrrequest_gated_submission_from_roi_v1_summary_v0', 'ocrrequest_gated_submission_v2_bbox_expansion_summary_v0'),
        ('roi_ocrrequest_gated_submission_only', 'expanded_roi_ocrrequest_gated_submission_only'),
        ('based_on_roi_ocrrequest_reference', 'based_on_ocrrequest_reference_v2_bbox_expansion'),
        ('roi_ocr_result_collection_generated', 'expanded_roi_ocr_result_collection_generated'),
        ('ocrrequest_gated_submission_from_roi_v1_executed', 'ocrrequest_gated_submission_from_roi_v2_bbox_expansion_executed'),
        ('roi_ocr_gated_submission_only', 'expanded_roi_ocr_gated_submission_only'),
        ('evidence_pack_v2', 'evidence_pack_v3'),
        ('semantic_v2', 'semantic_v3'),
        ('Evidence-Pack-Adapter-v2-ROIRef', 'Evidence-Pack-Adapter-v3-BBoxExpansion'),
        ('roi_ocr_result_collection_v1', 'expanded_roi_ocr_result_collection_v2'),
        ('all_traceable_to_ocrrequest_reference', 'all_traceable_to_ocrrequest_reference_v2'),
        ('traceable_to_ocrrequest_reference": True', 'traceable_to_ocrrequest_reference_v2": True'),
        ('source_validation_invoked', 'source_validation_v2_invoked'),
    ]:
        text = text.replace(old, new)

    # Function signature roots
    text = text.replace(
        """    roi_ocrrequest_reference_v2_root: str,
    roi_crop_rerun_root: str,
    better_frame_root: str,
    roi_retry_root: str,
    source_validation_root: str,
    mixed_batch_v2_root: str,
    linebox_sq_root: str,
    adapter_v1_root: str,
    review_queue_runtime_root: str,
    review_policy_v1_root: str,
    semantic_v1_root: str,""",
        """    roi_ocrrequest_reference_v2_root: str,
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
    mixed_batch_v2_root: str,""",
    )
    text = text.replace(
        "    ref_root = Path(roi_ocrrequest_reference_v2_root).resolve()\n    bench = Path(benchmark_smoke_root)",
        "    ref_root = Path(roi_ocrrequest_reference_v2_root).resolve()\n    crop_v2_root = Path(roi_crop_v2_root).resolve()\n    div_root = Path(roi_crop_diversity_root).resolve()\n    diag_root = Path(roi_ocr_quality_diagnosis_root).resolve()\n    bench = Path(benchmark_smoke_root)",
    )

    # Patch _bridge_submit parameter name throughout function
    text = text.replace("ocrrequest_reference_v2_id: str,", "ocrrequest_reference_v2_id: str,")

    # FOLLOWUPS
    text = text.replace(
        'FOLLOWUPS = [\n    "Evidence-Pack-Adapter-v3-BBoxExpansion",',
        'FOLLOWUPS = [\n    "Evidence-Pack-Adapter-v3-BBoxExpansion",\n    "Semantic-Candidate-v3-BBoxExpansionAware",\n    "ROI-OCR-Quality-Diagnosis-v2-BBoxExpansion",\n    "Crop-Quality-Scoring-v1",\n    "Multiframe-Merge-Proposal-v1",\n    "Better-Frame-Extraction-DryRun-v1",\n    "Future-Detector-ROI-Proposal-v1",\n    "Source-Validation-v2-after-ROI-OCR",\n    "STC Contract later",\n    "Controlled runtime integration",\n    "PLACEHOLDER_REMOVE",',
    )
    # remove duplicate followups from v1 list
    import re
    text = re.sub(
        r'    "PLACEHOLDER_REMOVE",\n    "Semantic Candidate v2 ROIAware",\n.*?    "Controlled runtime integration",\n',
        "",
        text,
        count=1,
    )

    DST.write_text(text, encoding="utf-8")
    print("wrote", DST)


if __name__ == "__main__":
    main()
