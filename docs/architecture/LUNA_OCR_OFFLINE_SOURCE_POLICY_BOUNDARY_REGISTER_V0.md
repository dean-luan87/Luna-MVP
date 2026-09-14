# LUNA — OCR Offline Source Policy Boundary Register v0

## Phase

- **Phase-ModelOCR-010** — hard boundaries for **008–010** and **closed_v0** offline policy work.

## Must not (process / product)

- **Change product runtime default OCR** without a new chartered phase and explicit product decision.
- **Route default offline policy chain** through EasyOCR, PaddleOCR current, PP-OCRv5 mobile ONNX, Tesseract default chain, or complex-layout providers.
- **Treat offline benchmark default** as **production runtime** default.

## Must not (integrations)

- **YOLO** — not part of OCR offline source policy closure.
- **Mid-platform** — no OCR selection event wiring in 010.
- **SceneTask / Fusion / Output** — no downstream consumption in this closure.
- **Semantic condensation / interpretation** — raw text only for this policy scope.
- **Navigation execution** — forbidden.
- **Real TTS** — forbidden.
- **Controlled live stream** — forbidden for policy scope.
- **Option A expansion** — not in scope.

## Must preserve

- **Explicit `--providers` mode** on `run_ocr_raw_text_benchmark_v0.py` when `--source-policy` is omitted.
- **Trace / replay / whitebox** artifacts for policy-mode runs.
- **Audit fields** on summary and per-sample outputs for policy runs.
- **Governance leakage = 0** as the acceptance bar for closure evidence.

## Review cadence

- Re-run regression when **policy id**, **selector logic**, or **benchmark contract** changes; update **010 baseline** doc.
