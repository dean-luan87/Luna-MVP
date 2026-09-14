# LUNA — YOLO × OCR Bridge Result Contract v0

## Schema: `YOLOOCRBridgeResult`

```json
{
  "bridge_result_id": "yolo_ocr_bridge_001",
  "frame_id": "...",
  "timestamp_ms": 0,
  "proposal_id": "ocr_prop_001",
  "source_detection_id": "det_001",
  "ocr_source_policy_id": "ocr_default_offline_raw_text_source_policy_v0",
  "ocr_provider_selected": "rapidocr_ppocrv4_mobile_onnx",
  "fallback_used": false,
  "fallback_reason": null,
  "crop_region": {},
  "raw_text_candidates": [],
  "raw_text_joined": "",
  "raw_text_segments": [],
  "length_policy_applied": true,
  "reading_direction_candidate": "unknown",
  "line_order_status": "present",
  "source_attribution": {
    "yolo_source": {
      "model_config_id": "...",
      "detection_id": "det_001",
      "class_name": "sign",
      "bbox": [0, 0, 0, 0],
      "confidence": 0.0
    },
    "ocr_source": {
      "provider_id": "...",
      "model_config_id": "...",
      "provider_kind": "...",
      "source_policy_id": "ocr_default_offline_raw_text_source_policy_v0"
    }
  },
  "candidate_only": true,
  "semantic_interpretation_enabled": false,
  "allows_execute_now": false,
  "downstream_invocation_count": 0,
  "real_tts_invoked": false,
  "trace_ref": "...",
  "replay_ref": "...",
  "whitebox_ref": "...",
  "hard_blockers": [],
  "soft_followups": []
}
```

## Contract constraints

- raw-text-only, candidate-only
- traceable linkage from detection → proposal → OCR result
- no semantic summary, no navigation advice, no downstream execution
