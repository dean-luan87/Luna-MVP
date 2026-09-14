# LUNA — MidPlatform OCR Evidence Input Contract v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001**

## Contract name

- `MidPlatformOCREvidenceInput`

## Schema（合同字段）

```json
{
  "evidence_id": "ocr_evidence_001",
  "source": "ocr_raw_text | yolo_ocr_bridge",
  "frame_id": "...",
  "timestamp_ms": 0,
  "source_frame_window_id": "...",
  "image_ref": "...",
  "crop_region": {...},
  "source_attribution": {
    "yolo_source": {...},
    "ocr_source": {...}
  },
  "raw_text_candidates": [],
  "raw_text_joined": "...",
  "raw_text_segments": [],

  "length_policy_applied": true,
  "reading_direction_candidate": "unknown",
  "line_order_status": "present | uncertain | not_available",

  "candidate_only": true,
  "semantic_interpretation_enabled": false,
  "allows_execute_now": false,
  "real_tts_invoked": false,
  "downstream_invocation_count": 0,

  "trace_ref": "...",
  "replay_ref": "...",
  "whitebox_ref": "..."
}
```

## Mandatory invariants（强约束）

- `candidate_only=true`
- `semantic_interpretation_enabled=false`
- `allows_execute_now=false`
- `real_tts_invoked=false`
- `downstream_invocation_count=0`
- `trace_ref / replay_ref / whitebox_ref` 必须存在且可追责

## Evidence acceptance gate（准入占位）

- 只接收 raw text candidates/segments 且与证据签名可对齐（用于后续 delta control）
- 不允许把 raw text 直接当“最终事实”进入任务链执行（仅进入 evidence layer）

