# Model Invocation Map v1

## Scope note

This map records discovered invocation or runner-entry surfaces, not a claim that every listed asset is enabled in the current runtime. Most assets are planning, dry-run, adapter, or controlled-runner code. Future attention control always occurs before a capability request is admitted; a model output is evidence, never a decision or fact.

| 模型 / 能力 | 调用入口 | 输入 | 输出 | 当前控制方式 | 未来 Attention 控制位置 |
|---|---|---|---|---|---|
| OCR | `capabilities/model_ocr/yolo_ocr_bridge_v0.py`; provider adapters in `capabilities/model_ocr/*_adapter_v0.py` | detection proposals, image/frame reference, dimensions, timestamp | OCR crop proposal and OCR evidence-style bridge result | YOLO-driven proposal filtering, per-frame budget/cooldown, offline source policy selection | Input Attention → Evidence Admission → Capability Bundle Candidate → OCR Adapter → EvidenceCandidate |
| Text detection | Model Manager planning, OCR bridge, Model Test Lens controlled runner/test-board assets | visual capability need / frame or runner request | text-recognition/model route or result envelope | model routing and controlled runner records | Attention Controller grants text-search depth; Kernel/resource bounds check before adapter request |
| Object detection | `capabilities/model_perception/yolo_shadow_adapter_v0.py`; OCR bridge consumes detections | frame/image reference | detection candidates / regions | shadow or controlled capability paths | Input Attention selects risk/goal-relevant regions; output becomes visual EvidenceCandidate |
| Segmentation | Model Test Lens MobileSAM / segmentation adapters and runner records | image / prompt / runner request | segmentation result envelope | controlled runner / sandbox planning | Capability composition only after Attention allocation; output is spatial evidence |
| VLM / visual-language | Model Manager provider/routing assets and VLM-oriented model integration assets | situation / capability request / visual input candidate | provider route or interpretation candidate | model manager planning; provider policy | Attention may request visual semantic evidence; VLM result enters Evidence Field with uncertainty, never Situation Fact |
| SLAM | `capabilities/midplatform/model_test_lens/adapters/slam/slam_evaluation_adapter_v1.py`; local runner bridge SLAM runners | video / SLAM output / runner request | spatial metrics, diagnostics, or runner result | evaluation adapter plus limited runner bridge | Active Attention creates spatial-information request candidate; SLAM output is spatial evidence, not route plan |
| Camera / capture | `capabilities/device_env/mac_camera_archive_adapter_v0.py`; `phone_local_capture_bundle_v0.py` | device/video archive or transferred capture bundle | frame/archive/bundle metadata | device/archive adapter boundary | Active Attention → sensor request candidate → future approved perception adapter; never direct camera call from controller |
| ASR | `capabilities/voice/input/asr_final_text_event_contract_v0.py`; `capabilities/voice/providers/mock_asr_provider.py` | audio stream/event | final text event candidate | contract/mock provider | Input Attention chooses speech relevance; Language/Audio Adapter wraps output as EvidenceCandidate / intent evidence |
| TTS | `capabilities/voice/providers/tts_provider_selector.py`; `tts_fallback_manager.py` | text / provider request | synthesized-speech provider/result | provider selection/fallback | Outside A-route cognition; only future external expression/execution boundary may request it |
| Language model / voice task bridge | `capabilities/voice/bridge/voice_long_input_model_validation.py`; `bridge_decision.py` | voice/model task candidate | validated mapping or bridge decision | mapping whitelist / legacy bridge policy | Future Language Adapter produces evidence/intent candidate; direct bridge decisions must not enter A-route authority |

## Required target control chain

`Attention Candidate Pool → Attention Controller → Allocation Candidate → Kernel / resource consistency candidate → Capability Bundle Candidate → approved adapter request → EvidenceCandidate → Evidence Field`

Forbidden shortcuts:

- model output → truth;
- OCR/VLM/SLAM → decision;
- attention controller → camera/model invocation;
- evidence → action;
- model router → Cognitive State mutation.

**Model-control-chain status: `MIGRATE`. Existing adapters/providers are retained as sensory capability sources, but direct cognitive control is `REPLACE`.**
