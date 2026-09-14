# LUNA — Realtime OCR Candidate Asset Completion Matrix v0

## Phase

- **Phase-ModelOCR-006E-Fix** (post-completion snapshot)

## Matrix (frozen after asset prepare + 006E re-run)

| Candidate | dependency_ready | model_assets_status | reproducibility_risk | requires_network_at_runtime | Notes |
|-----------|-------------------|---------------------|----------------------|----------------------------|--------|
| **rapidocr_current** | yes | `cache_detected` | true | false | Bundled v4 ONNX in site-packages |
| **rapidocr_ppocrv4_mobile** | yes | `cache_detected` | true | false | Same ONNX, explicit paths |
| **rapidocr_ppocrv5_mobile** | yes | `pinned_local` | false | false | Repo `models/ocr/rapidocr_ppocrv5_mobile/*.onnx` + `ppocrv5_dict.txt` |
| **easyocr** | yes | `cache_detected` | true | true (first run) | Weights under `~/.EasyOCR/model/` |
| **tesseract** | yes | `system_binary` | true | false | Homebrew `tesseract` + `pytesseract` |

### PP-OCRv5 file evidence (example run)

| File | SHA256 (prefix) | Size (bytes) |
|------|-----------------|--------------|
| `ch_PP-OCRv5_mobile_det_infer.onnx` | `1eb7b4f7ab65…` | 4 826 518 |
| `ch_PP-OCRv5_mobile_rec_infer.onnx` | `243a0f06d826…` | 16 562 373 |
| `ppocrv5_dict.txt` | `d1979e9f794c…` | 74 012 |

Full hashes in `logs/realtime_ocr_candidate_asset_prepare_006e_fix_*.json`.
