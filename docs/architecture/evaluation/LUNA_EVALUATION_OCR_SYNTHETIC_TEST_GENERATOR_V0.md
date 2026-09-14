# OCR Synthetic Test Generator v0 (Evaluation Tools)

## Goal

Generate a small synthetic OCR dataset (v0 default: **200 samples**) with:

- One image per sample
- One ground truth text per sample
- A dataset `manifest.jsonl` that records sample metadata and hashes

## TRDG preference

TRDG (`trdg`) is recommended, but **not required** in v0 due to installation variability.  
The generator must:

- Prefer TRDG if importable
- Otherwise fall back to Pillow-only rendering
- Record which generator was used in the manifest and dataset summary

## Boundaries

See `LUNA_EVALUATION_OCR_TEST_HARNESS_BOUNDARY_V0.md`.

