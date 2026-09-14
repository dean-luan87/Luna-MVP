# LUNA — OCR Provider Decision Review v0

## Phase

- **Phase-ModelOCR-007** — *OCR Provider Decision Review v0* (**documentation only**; no runtime default switch)

## Evidence baseline

| Source | Role |
|--------|------|
| 005B unified GT benchmark | 30-sample raw-text stratified dataset |
| 006 / 006A–C | PaddleOCR fairness, real inference, audit gaps |
| 006D | Role reclassification; realtime vs complex branch split |
| 006E / 006E-Fix | Five realtime candidates on same GT; full asset closure |

**Authoritative benchmark root (006E-Fix re-run):**  
`logs/realtime_ocr_candidate_benchmark_006e_fix_20260429_120908`  
- Verifier: **GO**  
- `default_ocr_provider_set=false`, governance leakage **0**

## Frozen metric summary (30 samples)

| Provider | text_exact_match | avg latency (ms) | bbox_iou_avg | Notes |
|----------|------------------|------------------|--------------|--------|
| `rapidocr_current` | 0.2 | ~117 | ~0.279 | Fast; bundled default ONNX (v4-class) |
| `rapidocr_ppocrv4_mobile_onnx` | 0.2 | ~113 | ~0.279 | **Explicit auditable paths**; ~equivalent to current |
| `rapidocr_ppocrv5_mobile_onnx` | 0.2 | ~119 | ~0.117 | **No accuracy gain**; **weaker bbox**; **community ONNX** (not official Paddle export chain) |
| `easyocr` | 0.0 | ~693 | ~0.103 | High latency; poor on this GT |
| `tesseract` | 0.0 | ~216 | ~0.062 | Classic baseline; weak on zh/natural scene for this set |

**Out of 006E harness but in policy:**  
- **macOS Vision** — `FALLBACK_OR_COMPARISON_ONLY` (system API; ~460 ms/frame class historically — not realtime primary).  
- **PaddleOCR (current workspace config)** — offline / complex track; **not** realtime default (latency ~2.3s/frame class; path/bbox audit not closed).

## Decision recommendations (non-binding; no code change)

### Primary realtime candidate (choose one for future policy)

- **`rapidocr_ppocrv4_mobile_onnx`** — **preferred** where **explicit det/rec/cls ONNX paths** and hashes matter for audit.  
- **`rapidocr_current`** — **acceptable equivalent** operationally; same effective model tier as bundled v4 ONNX.

Rationale: same accuracy tier (~0.2 exact match), best **bbox_iou** group among successful rapid line, latency ~113–117 ms/frame — suitable for **realtime / near-realtime region OCR** *as a candidate*, not as a shipped default until product thresholds are met.

### Secondary realtime candidate

- **`rapidocr_current`** if primary is pinned to `ppocrv4_mobile`; **or** swap labels if product standardizes on “default RapidOCR()” — **document the choice in policy**, not in silent code defaults.

### Fallback / comparison

- **`macos_vision_ocr_system_v0`** — availability and Apple baseline.  
- **`tesseract_cli_baseline_v0`** — **classic baseline only**; not a quality default for mixed zh/en navigation scenes on current GT.

### Not recommended for realtime default

- **`easyocr_multilingual_v0`** — fails exact-match bar on this GT; **~693 ms/frame** average.  
- **`tesseract_cli_baseline_v0`** — **not** promoted beyond baseline / spot-check.  
- **`paddleocr_ppocrv5_lightweight_v0` (current config)** — realtime default **ineligible** (latency, bbox/path closure).  
- **`rapidocr_ppocrv5_mobile_onnx`** — **do not** promote to primary without new evidence: **no accuracy improvement**, **worse bbox**, **community ONNX provenance risk**.

### Complex / document / OCR-VL branch (not realtime default)

Surya, docTR, PaddleOCR-VL, DeepSeek-OCR / OCR2, and **PaddleOCR** for heavy offline / layout / long-text — **separate** product lane; **must not** merge into realtime default eligibility.

## Explicit non-actions (Phase-007)

- Do **not** set default OCR in code or config.  
- Do **not** integrate YOLO, mid-platform, SceneTask, Fusion, Expression.  
- Do **not** add semantic interpretation, navigation execution, real TTS, controlled live stream.

## Related documents

- `LUNA_OCR_REALTIME_PROVIDER_RECOMMENDATION_MATRIX_V0.md`  
- `LUNA_OCR_PROVIDER_DECISION_RISK_REGISTER_V0.md`  
- `LUNA_OCR_PROVIDER_DECISION_GO_NO_GO_PACK_V0.md`

## Next phase (policy only)

- **Phase-ModelOCR-008** — *OCR Default Offline Source Policy Definition v0* — defines **policy text** for defaults and pins; **still** no mandatory runtime implementation in 008 by charter.
