# Luna Midplatform — OCR / Text Adapter Skeleton v1

## Scope

Adapter Skeleton only. Based on Smoke IO Inspection artifacts. No real OCR execution.

## Pipeline

```
build_ocr_text_adapter_input_package
→ load_ocr_text_raw_output_candidate
→ normalize_ocr_text_output_to_candidates
→ build_text_anchor_candidates
→ build_text_normalization_candidates
→ assemble_ocr_text_adapter_result
```

## Output Candidates

- TextObservationCandidate
- TextRegionCandidate
- TextAnchorCandidate
- TextNormalizationCandidate
- TextQualityCandidate
- OCRTextAdapterResultCandidate

## Prohibited

- Real OCR execution / model download / weight download
- World model assembly
- Task reasoning / action output
- Field simulation
- LLM text correction
