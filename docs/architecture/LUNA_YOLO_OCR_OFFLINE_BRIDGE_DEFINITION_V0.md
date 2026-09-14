# LUNA — YOLO × OCR Offline Bridge Definition v0

## Phase

- **Phase-ModelOCR-YOLO-Bridge-001** — definition only, offline only.

## Scope

Define how YOLO proposes where OCR should look, while OCR remains raw-text-only.

This phase also freezes control boundaries: TaskChain defines intent only, MidPlatform is the scheduler/controller, and capability modules are not directly orchestrated by TaskChain.

## Frozen upstream facts

## Standard control chain (frozen wording)

`TaskChain / Task Intent`
`→ MidPlatform Scene Controller`
`→ Capability Scheduler`
`→ Vision Perception Layer (YOLO / OCR / YOLO→OCR bridge)`
`→ MidPlatform Evidence Layer (snapshot / delta reuse / validation / relevance filtering)`
`→ TaskChain Update / Decision Candidate`

Key rule: TaskChain does not directly command YOLO/OCR. MidPlatform decides whether to use vision, OCR, full-frame vs crop, reuse vs refresh, fallback, and budget usage.

- YOLO offline engineering mainline: **closed_v0**.
- OCR offline source policy: **closed_v0** (`ocr_default_offline_raw_text_source_policy_v0`).
- OCR default offline chain: `rapidocr_ppocrv4_mobile_onnx` → `rapidocr_current` → `macos_vision_ocr_system_v0` → `not_available`.

## Responsibilities

- **TaskChain**: defines task intent and required information only; does not directly schedule capability modules.
- **MidPlatform**: performs scene control and capability scheduling; decides whether OCR is needed, full-frame vs crop, reuse vs refresh, fallback, and budget enforcement.
- **YOLO**: discovers OCR-worthy objects/regions, emits detection attribution and crop proposals; does not interpret text meaning.
- **OCR**: reads raw text from full frame or crop, outputs candidates/bbox/confidence/line-order/joined text; does not interpret world meaning.
- **Bridge**: converts detection to OCR request candidate, preserves source attribution and traceability, remains candidate-only and raw-text-only.

## Hard boundaries

- No runtime implementation.
- No change to YOLO closed_v0 or OCR closed_v0.
- No mid-platform, SceneTask/Fusion/Output, semantic condensation, navigation execution, real TTS, controlled live stream.
- No Option A expansion.

## OCR trigger source note

YOLO is an important OCR source, but not the only source. OCR trigger sources include:
- `full_frame_low_frequency`
- `yolo_guided_crop`
- `task_hint_guided_crop` (placeholder only in Bridge-001)
- `scene_context_probe` (placeholder only in Bridge-001)

Bridge-001 focuses on defining `full_frame_low_frequency` and `yolo_guided_crop` behavior and boundaries.
