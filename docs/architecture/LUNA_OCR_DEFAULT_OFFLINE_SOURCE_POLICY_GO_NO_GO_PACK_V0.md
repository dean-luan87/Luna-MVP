# LUNA — OCR Default Offline Source Policy Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-008** — *OCR Default Offline Source Policy Definition v0*

## GO

All true:

- **`source_policy_id`** fixed: `ocr_default_offline_raw_text_source_policy_v0`.  
- **Default offline source chain** explicit: v4 mobile → `rapidocr_current` → macOS Vision → `not_available`; Tesseract **not** in chain (classic baseline only).  
- **Fallback** conditions explicit (`LUNA_OCR_OFFLINE_SOURCE_SELECTION_AND_FALLBACK_POLICY_V0.md`).  
- **Audit** field set explicit (`LUNA_OCR_OFFLINE_SOURCE_POLICY_AUDIT_REQUIREMENTS_V0.md`).  
- **Disable / rollback** flags explicit.  
- **Excluded** providers from default chain explicit (EasyOCR, PaddleOCR current, PP-OCRv5, Tesseract in default chain, complex branch).  
- **No** runtime code change and **no** production default OCR flag in this phase.  
- **No** downstream, semantic refinement, mid-platform wiring, YOLO, navigation, real TTS, controlled live stream.

**Suggested verdict:** **GO** for Phase-008 **policy documentation** closure.

## CONDITIONAL_GO

- Policy complete but **`reproducibility_risk`** or asset pinning still **open** on some machines — allowed; track as soft follow-up. **Still** eligible to proceed to **009** (integration to **offline** harness default entry — **not** runtime).

## NO_GO

- **Runtime default** OCR changed in this phase.  
- EasyOCR / PaddleOCR / PP-OCRv5 / Tesseract **placed** in the **default** offline chain without a new chartered policy.  
- **Ignore** mandatory fallback rules.  
- **Omit** required audit fields for policy-claiming runs.  
- **Wire** semantic pipeline, mid-platform, downstream, `allows_execute_now=true`, or `real_tts_invoked=true`.

## Hard blockers (process)

- None if documents merged and no forbidden code changes landed.

## Soft follow-ups

- Pin assets / reduce `reproducibility_risk`; expand GT; task-relevant metrics; later **MidPlatform-Monitoring-001** event schema alignment.

## Recommended next phase

- **Phase-ModelOCR-009 — OCR Offline Source Policy Integration v0**  
  - May wire **`ocr_default_offline_raw_text_source_policy_v0`** into **offline** OCR benchmark / harness **default entry** only.  
  - **Still not** product runtime default OCR.

## Frozen evidence pointer

- **006E-Fix:** `logs/realtime_ocr_candidate_benchmark_006e_fix_20260429_120908`

## Charter reminder (Phase-008)

- **008** = **policy definition only** — **not** runtime switch.  
- **007** recommendations are **encoded** as **offline** default source rules here; **009** may integrate into **offline** tooling.
