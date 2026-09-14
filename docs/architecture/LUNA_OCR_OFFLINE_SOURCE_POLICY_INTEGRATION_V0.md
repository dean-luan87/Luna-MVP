# LUNA — OCR Offline Source Policy Integration v0

## Phase

- **Phase-ModelOCR-009** — wires **`ocr_default_offline_raw_text_source_policy_v0`** into the **offline** raw-text benchmark default path (`tools/run_ocr_raw_text_benchmark_v0.py`). **Does not** set product runtime OCR default.

## Implementation map

| Artifact | Role |
|----------|------|
| `capabilities/model_ocr/offline_source_policy_v0.py` | `probe_ocr_offline_provider_registry_v0`, `select_ocr_offline_source_v0` — pure selection + local probe. |
| `tools/run_ocr_raw_text_benchmark_v0.py` | `--source-policy` and disable flags; policy mode runs **one** selected provider; writes **008/009** audit fields into summary and per-sample JSON. |
| `tools/verify_ocr_offline_source_policy_v0.py` | Selector cases A–J + optional `--normal-root` / `--fallback-root` summary checks. |

## CLI (policy mode)

```bash
python3 tools/run_ocr_raw_text_benchmark_v0.py \
  --source-policy ocr_default_offline_raw_text_source_policy_v0 \
  --dataset-manifest datasets/ocr_raw_text_benchmark_v0/manifests/ocr_benchmark_samples_v0.json \
  --output-root logs/ocr_offline_source_policy_009_normal_<timestamp>
```

Fallback demonstration (skip PP-OCRv4 explicit path → `rapidocr_current`):

```bash
python3 tools/run_ocr_raw_text_benchmark_v0.py \
  --source-policy ocr_default_offline_raw_text_source_policy_v0 \
  --disable-rapidocr-ppocrv4 \
  --dataset-manifest datasets/ocr_raw_text_benchmark_v0/manifests/ocr_benchmark_samples_v0.json \
  --output-root logs/ocr_offline_source_policy_009_fallback_<timestamp>
```

## Compatibility

- **Without** `--source-policy`, behavior matches **legacy** multi-provider explicit `--providers` mode (unchanged default list).

## Boundaries (unchanged from 008)

- No YOLO, mid-platform, SceneTask/Fusion/Output, semantic condensation, navigation, real TTS, controlled live stream, Option A expansion.

## Evidence run (example)

- Normal: `logs/ocr_offline_source_policy_009_normal_20260429_124053`
- Fallback: `logs/ocr_offline_source_policy_009_fallback_20260429_124053`

## Related

- `LUNA_OCR_DEFAULT_OFFLINE_SOURCE_POLICY_V0.md` (008 policy)
- `LUNA_OCR_OFFLINE_SOURCE_POLICY_INTEGRATION_TEST_MATRIX_V0.md`
- `LUNA_OCR_OFFLINE_SOURCE_POLICY_INTEGRATION_GO_NO_GO_PACK_V0.md`
