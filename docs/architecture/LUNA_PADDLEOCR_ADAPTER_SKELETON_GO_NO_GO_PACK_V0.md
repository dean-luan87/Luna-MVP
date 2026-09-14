# LUNA — PaddleOCR Adapter Skeleton Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-004B**
- Subject: adapter skeleton + dependency readiness + fail-closed validity.

## GO

- skeleton exists and outputs contract fields.
- dependency readiness report exists.
- det/rec pinned_partial recognized.
- cls missing handled as optional/not-claimed.
- fail-closed works.
- fallback candidates preserved.
- no semantic/downstream/execute/TTS.

## CONDITIONAL_GO

- `paddle` / `paddleocr` / `PIL` missing,
- but fail-closed is active and outputs are honest,
- adapter remains safe for subsequent dependency installation and benchmark preparation.

## NO_GO

- dependency missing but provider fakes available.
- weights missing but marked ready.
- cls missing while claiming orientation support.
- semantic/downstream/execute/TTS violations.
- fallback candidates removed.

## Recommended next

1. **ModelOCR-005** GT dataset + raw text benchmark (after 004B accepted).
2. Keep 004A Vision fallback and 004C RapidOCR candidate lanes unchanged.
