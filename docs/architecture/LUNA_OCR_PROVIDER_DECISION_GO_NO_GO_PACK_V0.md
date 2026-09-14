# LUNA — OCR Provider Decision Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-007**

## GO

All true:

- **006E-Fix** evidence cited (five candidates **success**, verifier **GO**, benchmark root recorded).  
- **Recommendation matrix** completed (`LUNA_OCR_REALTIME_PROVIDER_RECOMMENDATION_MATRIX_V0.md`).  
- **Fallback** and **not recommended** lists explicit.  
- **Complex branch** boundary explicit (no merge into realtime default).  
- **Risk register** completed (`LUNA_OCR_PROVIDER_DECISION_RISK_REGISTER_V0.md`).  
- **No** default OCR provider set in code or config in this phase.  
- Next step described as **policy definition** (Phase-008), **not** runtime implementation mandate.

**Suggested verdict for Phase-007 documentation closure:** **GO** (with **CONDITIONAL_GO** caveats carried from sample size — see below).

## CONDITIONAL_GO

- Primary/secondary choice between `rapidocr_ppocrv4_mobile` vs `rapidocr_current` may need **more GT** or **product-specific** latency/accuracy trade-off workshop — still **no code default**.

## NO_GO

- Any **runtime default** OCR flag changed in this phase.  
- **Ignore** sample-size / exact-match risks.  
- Promote **EasyOCR** or **Tesseract** to realtime **default** in documentation.  
- Merge **complex-branch** stacks into realtime **default** recommendation.  
- Treat **PP-OCRv5 community ONNX** as **official auditable** primary without further proof.

## Recommended next phase

- **Phase-ModelOCR-008 — OCR Default Offline Source Policy Definition v0**  
  - Defines **written policy** for which provider is allowed as default *when* the program chooses to implement it — **still** no mandatory runtime wiring in 008 by this charter.

## Hard blockers (process)

- None if documents merged and no code default landed.

## Soft follow-ups

- Expand GT; add task-relevant metrics; official PP-OCRv5 export audit if v5 is revisited; Phase-008 policy wording.
