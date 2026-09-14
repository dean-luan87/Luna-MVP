# LUNA — OCR Default Offline Raw Text Source Policy v0

## Phase

- **Phase-ModelOCR-008** — *OCR Default Offline Source Policy Definition v0* (**policy text only**; **no** runtime default change; **no** code mandate in this phase)

## Purpose

Freeze **how** the workspace chooses a **default offline OCR raw-text source** for **offline evaluation** and **offline OCR harnesses** — analogous in role to `LUNA_YOLO_DEFAULT_OFFLINE_PERCEPTION_SOURCE_POLICY_V0.md`, but for **OCR**.

This policy **does not** set product runtime default OCR. It **does not** expand Option A scope.

## Policy identity

| Field | Value |
|-------|--------|
| **source_policy_id** | `ocr_default_offline_raw_text_source_policy_v0` |
| **policy_version** | `v0` |

## Evidence baseline (frozen)

| Phase | Verdict |
|-------|---------|
| ModelOCR-005B | GO |
| ModelOCR-006 | GO |
| ModelOCR-006E-Fix | GO |
| ModelOCR-007 | GO |

**006E-Fix benchmark root:**  
`logs/realtime_ocr_candidate_benchmark_006e_fix_20260429_120908`

**Provider roles (from 007):**  
- **Primary candidate:** `rapidocr_ppocrv4_mobile_onnx`  
- **Secondary candidate:** `rapidocr_current`  
- **Fallback / comparison:** macOS Vision OCR, Tesseract (classic baseline)  
- **Not recommended for realtime default:** EasyOCR, PaddleOCR (current config), RapidOCR PP-OCRv5 mobile ONNX  
- **Complex branch:** Surya, docTR, PaddleOCR-VL, DeepSeek-OCR, PaddleOCR complex/offline track

## Allowed scope (when this policy applies)

The policy is **only** meaningful when **all** of the following are true:

- `offline_evaluation=true`
- `raw_text_only=true`
- `semantic_interpretation_enabled=false`
- `downstream_invocation_allowed=false`
- `real_tts_allowed=false`
- `controlled_live_stream=false`

If any condition fails — **do not** treat this policy as active; record violation and use explicit harness mode or `not_available` per selection doc.

## Hard boundaries

- **Default offline OCR source ≠ runtime default OCR provider**  
- **Default offline OCR source ≠ mid-platform text refinement / semantic pipeline**  
- **Default offline OCR source ≠ SceneTask / Fusion / Expression / navigation output**  
- **This phase does not wire** YOLO, mid-platform, downstream consumers, semantic condensation, navigation execution, real TTS, or controlled live stream.  
- **Option A** scope is **not** expanded by this document.

## Default offline source chain (ordered)

When the allowed scope holds and no disable flag blocks the chain:

1. `rapidocr_ppocrv4_mobile_onnx`
2. `rapidocr_current`
3. `macos_vision_ocr_system_v0`
4. **`not_available`** (terminal; must record `not_available_reason` when used)

### Tesseract

- **Not** in the default offline fallback chain.  
- **Default role:** **classic comparison baseline** only.  
- A future **`classic_fallback_mode`** (if defined) may allow Tesseract in chain — **out of scope for v0**.

## Providers that must NOT enter the default offline source chain (v0)

Unless a **separate** chartered policy exists:

| Provider / class | Reason (summary) |
|------------------|------------------|
| `easyocr` | Not recommended default; keep for explicit benchmarks only |
| `paddleocr_current` | Current config not for default chain |
| `rapidocr_ppocrv5_mobile_onnx` | Future review; community ONNX lineage |
| **Tesseract** | Not in default chain v0 (classic baseline only) |
| Surya, docTR, PaddleOCR-VL, DeepSeek-OCR, complex layout stacks | **Complex branch** — not offline default chain |

Explicit **opt-in** harness runs may still invoke these; they **must not** be selected by the **default** policy chain.

## Relationship to Phase-007 / 007A

- **007** recommends providers; **008** turns that into **written offline default source rules**.  
- **007A** defines archive / exclusion / re-entry; **008** defines **which** sources are allowed in the **default offline** ordered chain.

## Relationship to mid-platform monitoring (future)

- OCR **provider health** and **selection / fallback** events are intended to feed **Phase-MidPlatform-Monitoring-001** (*Unified Capability Runtime Monitoring*) **later**.  
- **This phase defines fields and policy only** — **no** mid-platform integration.

## Related documents

- `LUNA_OCR_OFFLINE_SOURCE_SELECTION_AND_FALLBACK_POLICY_V0.md` — selection order, conditions, fallback, disable / rollback.  
- `LUNA_OCR_OFFLINE_SOURCE_POLICY_AUDIT_REQUIREMENTS_V0.md` — mandatory audit fields.  
- `LUNA_OCR_DEFAULT_OFFLINE_SOURCE_POLICY_GO_NO_GO_PACK_V0.md` — GO pack and next phase.
