# LUNA — PaddleOCR Output Normalization and BBox Conversion v0

## Phase

- **Phase-ModelOCR-006B**

## Output audit points

- raw paddle output structure and hierarchy
- normalized candidate mapping correctness
- polygon-to-xyxy bbox conversion correctness
- coordinate space consistency with GT image pixels

## Artifacts

- `per_sample_raw_paddle_output.json`
- `per_sample_normalized_candidates.json`
- `coordinate_conversion_report.json`
