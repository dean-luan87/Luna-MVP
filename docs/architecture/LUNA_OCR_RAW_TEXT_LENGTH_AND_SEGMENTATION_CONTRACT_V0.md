# LUNA — OCR Raw Text Length and Segmentation Contract v0

## Phase

- **Phase-ModelOCR-001-Patch-002**
- Scope: contract patch only, no runtime implementation in this phase.

## Objective

- Freeze hard limits for raw-text output length and per-frame output size.
- Freeze long-text segmentation contract to avoid downstream context pollution.

## Default limits (v0)

- `candidate_text_max_chars = 128`
- `segment_text_max_chars = 256`
- `joined_text_max_chars = 512`
- `max_candidates_per_frame = 50`
- `max_segments_per_frame = 20`

## Mandatory output fields (patch)

- `raw_text_joined_truncated: bool`
- `raw_text_joined_length: int`
- `raw_text_segments: []`
- `length_policy: { ... }`

## Mandatory boundaries

- no semantic summary
- no semantic compression
- no navigation instruction
- no execution action
- no real tts
- no downstream invocation

## Contract notes

- OCR must preserve raw facts. Over-limit handling uses split/truncate markers, not summarization.
- If `raw_text_joined` exceeds limit, must set `raw_text_joined_truncated=true`.
- Downstream text refinement must consume `raw_text_segments` instead of blindly consuming long joined text.
