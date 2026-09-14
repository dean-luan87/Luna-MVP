# OCR Synthetic Dataset Schema v0 (TRDG-preferred)

Dataset root layout:

```
<dataset_root>/
  images/
    sample_000001.png
  ground_truth/
    sample_000001.txt
  manifest.jsonl
  dataset_summary.json
  generation_config.json
  generation_notes.md
```

## `manifest.jsonl` row schema (v0)

```json
{
  "sample_id": "sample_000001",
  "image_path": ".../images/sample_000001.png",
  "ground_truth_path": ".../ground_truth/sample_000001.txt",
  "ground_truth_text": "....",
  "language": "zh|en|mixed",
  "category": "zh_plain_text|en_plain_text|digits_and_symbols|mixed_zh_en_digit|low_contrast_or_blur|multi_line_text|...",
  "generator": "trdg|pillow_fallback",
  "generator_config": { "width": 640, "height": 160, "seed": 42, "prefer_trdg": true },
  "sha256": "<sha256>",
  "width": 640,
  "height": 160
}
```

