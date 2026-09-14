# OCR Result Mapping

| RapidOCR native field | Provider Runtime / evidence field |
|---|---|
| `provider_id` | native implementation identity in `provider_native_result` |
| `model_config_id` | native model config identity in `provider_native_result` |
| `raw_text_candidates[].text` | `output_candidate.text_candidates[].text` |
| `raw_text_candidates[].normalized_text` | preserved as a text normalization candidate |
| `raw_text_candidates[].bbox` | preserved as pixel bounding-box candidate |
| `raw_text_candidates[].confidence` | `confidence_candidate` is the maximum available candidate confidence |
| `raw_text_candidates[].line_order` | preserved as provider reading-order candidate |
| `raw_text_joined` | `output_candidate.text_joined` |
| native trace/runtime metadata | `raw_result_ref`, `trace_refs`, `provenance_refs` |

`quality_candidate` remains `None` because RapidOCR does not provide a Luna
quality score in this adapter. No language, region, reading order, or semantic
field is invented when the provider does not supply it.

For non-empty success the Gateway emits `ocr_text_evidence` with the candidate
payload. For a real empty provider result it emits `ocr_empty_success` as an
execution-status candidate, with no text candidate; this is not a fabricated
OCR text evidence.
