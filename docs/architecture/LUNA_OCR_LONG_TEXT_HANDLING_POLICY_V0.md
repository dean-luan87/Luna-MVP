# LUNA — OCR Long Text Handling Policy v0

## Phase

- **Phase-ModelOCR-001-Patch-002**

## Handling policy

1. Over-limit `candidate.text` must be split or marked truncated.
2. Over-limit `raw_text_joined` must set:
   - `raw_text_joined_truncated=true`
   - `raw_text_joined_length=<original_len>`
3. Long content must be emitted through `raw_text_segments`, never converted to summary.
4. Truncated output must include explicit reason (`truncated_reason`).
5. Segment output must keep raw line references (`line_ids`) for trace/replay/whitebox.

## Forbidden behaviors

- generate semantic summary from long text
- generate semantic compression/paraphrase
- generate navigation instruction
- treat truncated `raw_text_joined` as sole downstream input

## Downstream constraint

- Future mid-platform text refinement must consume governed segments (`raw_text_segments`) first.
- Ungoverned long `raw_text_joined` is not allowed as the only input to refinement.
