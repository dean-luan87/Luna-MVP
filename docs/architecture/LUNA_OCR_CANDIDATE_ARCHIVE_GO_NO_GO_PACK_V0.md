# LUNA — OCR Candidate Archive & Exclusion Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-007A** — *OCR Candidate Archive & Exclusion Policy v0*

## GO

All true:

- **Active vs archived / comparison / complex / future-review** classification is **clear** (`LUNA_OCR_PROVIDER_ACTIVE_ARCHIVE_STATUS_MATRIX_V0.md`).
- **No deletion** of historical benchmark artifacts, provider code, or historical docs as a “cleanup” — **preservation** of negative evidence is explicit (`LUNA_OCR_CANDIDATE_ARCHIVE_AND_EXCLUSION_POLICY_V0.md`).
- **Re-entry criteria** are **written** for demoted providers (`LUNA_OCR_CANDIDATE_REENTRY_CRITERIA_V0.md`).
- **Default OCR provider** is **still not set** in code or config in this phase.
- **Intent** documented: **code retained**; **default realtime chain** must not **silently** treat excluded providers as primary (policy layer; implementation in a **later** explicit phase if ever).

**Suggested verdict:** **GO** for **documentation / governance closure** of 007A.

## NO_GO

Any of:

- **Delete** historical benchmark outputs or logs to “remove failure evidence.”
- **Delete** or gut **provider code** so benchmarks are **non-reproducible**.
- **Purge** documentation that records why a candidate **failed** the current bar.
- **Silently enable** an excluded provider on the **default** realtime chain without re-entry evidence and a **named** implementation phase.

## CONDITIONAL_GO

- Matrix complete but team wants **stronger GT** before treating **primary vs secondary** (v4 vs current) as final — **still** no code default; **still** no deletion.

## Hard blockers (process)

- None if the four 007A documents are merged and **no** destructive cleanup occurred.

## Soft follow-ups

- Expand GT; task-relevant metrics; official PP-OCRv5 lineage if revisiting v5; Phase-008 offline **policy definition** (`OCR Default Offline Source Policy Definition v0`).

## Recommended next phase

- **Phase-ModelOCR-008 — OCR Default Offline Source Policy Definition v0**  
  - **Written policy only** for *when* a default may be chosen — **not** a mandate to implement runtime wiring in 008.

## Relationship to Phase-007

- **007** = decision **recommendations** from evidence.  
- **007A** = **pool membership**, **archive semantics**, and **re-entry** — **without** deleting the engineering record.
