# LUNA — Realtime OCR Candidate Asset Completion Fix v0

## Phase

- **Phase-ModelOCR-006E-Fix** — *Realtime OCR Candidate Dependency & Asset Completion v0*

## Intent

Close the **three** gaps that left 006E at **CONDITIONAL_GO**: EasyOCR weights/cache, Tesseract binary + `pytesseract`, and **PP-OCRv5 mobile** ONNX + recognition dictionary under repo control.

## Actions performed (representative)

1. **EasyOCR**  
   - `pip install easyocr` in project venv.  
   - Warmup `Reader(['ch_sim','en'])` once to materialize cache under `~/.EasyOCR/model/`.  
   - Record file paths, sizes, SHA256 in `tools/prepare_realtime_ocr_candidate_assets_v0.py` output.

2. **Tesseract**  
   - `brew install tesseract` (macOS) → binary e.g. `/opt/homebrew/bin/tesseract`.  
   - `pip install pytesseract` + Pillow.  
   - Capture `tesseract --version` stdout in asset report.

3. **PP-OCRv5 mobile ONNX**  
   - Download community ONNX from Hugging Face `ilaylow/PP_OCRv5_mobile_onnx` (`ppocrv5_det.onnx`, `ppocrv5_rec.onnx`).  
   - Copy to manifest names under `models/ocr/rapidocr_ppocrv5_mobile/`.  
   - Download `languages/chinese/dict.txt` from `monkt/paddleocr-onnx` → `ppocrv5_dict.txt` for `rec_keys_path`.  
   - Optional: copy bundled cls ONNX from `rapidocr-onnxruntime` into same directory for parity.  
   - **Provenance:** community export; official Paddle HF repos ship Paddle inference format — ONNX is a separate audit line.

## Boundaries

No default OCR provider; no downstream; no complex-layout providers in 006E harness.

## Artifact

- Prepare report example: `logs/realtime_ocr_candidate_asset_prepare_006e_fix_20260429_120748.json`
