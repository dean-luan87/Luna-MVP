# Luna — Vision-OCR Evidence Ingest Integration Check v1

**Phase**：`Vision-OCR-Evidence-Ingest-Integration-Check-v1-001`  
**性质**：integration check only；验证 observation request → vision/OCR evidence ingest 入口

## 链路

```
Observation Request Candidate
  → Vision Evidence Candidate (16)
  → OCR Evidence Candidate (gate allows later only)
  → Action Support / Verification Support
  → Evidence-to-Task Feedback (later)
```

## 边界

- 不是 Vision/OCR runtime；不调用 camera/detector/OCR provider
- `raw_text_candidate=null`；`empty_text_is_not_no_text_fact=true`
- evidence 不写 fact；不 commit task state

## 下一推荐 Phase

**Navigation-Guidance-to-Speech-Candidate-Adapter-v1** — 已完成（见 `LUNA_NAVIGATION_GUIDANCE_TO_SPEECH_CANDIDATE_ADAPTER_V1.md`）  
**Basic-Navigation-Guidance-Loop-DryRun-v1**

## 实现

- `capabilities/midplatform/vision_ocr_evidence_ingest_integration_check_v1.py`
- `tools/evaluation/midplatform/run_vision_ocr_evidence_ingest_integration_check_v1.py`
- `tools/evaluation/midplatform/verify_vision_ocr_evidence_ingest_integration_check_v1.py`
