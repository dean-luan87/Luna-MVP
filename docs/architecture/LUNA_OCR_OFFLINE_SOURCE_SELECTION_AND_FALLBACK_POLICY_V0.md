# LUNA — OCR Offline Source Selection & Fallback Policy v0

## Phase

- **Phase-ModelOCR-008** — implements the selection rules for **`ocr_default_offline_raw_text_source_policy_v0`**

## Policy identity

- **source_policy_id:** `ocr_default_offline_raw_text_source_policy_v0`

## Default attempt order

For each evaluation run under the policy scope, **try providers in order** until one succeeds without mandatory-fallback trigger:

1. `rapidocr_ppocrv4_mobile_onnx`
2. `rapidocr_current`
3. `macos_vision_ocr_system_v0`
4. Terminal: **`not_available`**

Record **`provider_attempt_order`** as the ordered list actually attempted (after applying disable flags).

---

## Selection: `rapidocr_ppocrv4_mobile_onnx`

Use as first choice when **all** hold:

| Condition | Notes |
|-----------|--------|
| `provider_enabled=true` | Not disabled by policy / harness flag |
| `model_assets_status` ∈ `pinned_local`, `cache_detected` | Other states → treat as failure → fallback |
| `dependency_ready=true` | Imports / runtime deps OK |
| `raw_text_schema_valid=true` | Output matches raw-text contract |
| `governance_boundary_valid=true` | No forbidden semantic / execute / leakage |
| `avg_latency_profile_acceptable=true` | Within agreed offline budget for the run |
| `reproducibility_risk` | **Recorded** (may be non-empty — see CONDITIONAL_GO) |
| `allows_execute_now=false` | Must stay false |
| `real_tts_invoked=false` | Must stay false |

If **any** fails → **fallback** to `rapidocr_current` (unless `disable_rapidocr_ppocrv4=true` — then skip to next allowed step).

---

## Selection: `rapidocr_current`

Use when v4 mobile is skipped or failed, and **all** hold:

| Condition |
|-----------|
| `provider_available=true` |
| `dependency_ready=true` |
| `asset_report_present=true` |
| `raw_text_schema_valid=true` |
| `governance_boundary_valid=true` |

If **any** fails → **fallback** to `macos_vision_ocr_system_v0` (unless `disable_rapidocr_current=true`).

---

## Selection: `macos_vision_ocr_system_v0`

Use when RapidOCR path failed, and **all** hold:

| Condition |
|-----------|
| `platform=darwin` |
| `provider_available=true` |
| `system_provider_ready=true` |
| `raw_text_schema_valid=true` |

If **any** fails (including non-macOS) → **`not_available`**.

---

## Terminal: `not_available`

- Emit explicit **`not_available_reason`** (enum or structured string).  
- Do **not** silently fall through to EasyOCR, PaddleOCR, PP-OCRv5, Tesseract default chain, or complex-branch providers.

---

## Mandatory fallback (any provider)

If **any** of the following occurs for the **current** attempt, **stop** using that provider for this run step and **advance** per the default chain (or skip if disabled):

- `dependency_missing`
- `model_asset_missing`
- `provider_import_failed`
- `provider_init_failed`
- `provider_timeout`
- `invalid_output_schema`
- `semantic_interpretation_enabled=true` (**forbidden** under policy scope)
- `allows_execute_now=true` (**forbidden**)
- `real_tts_invoked=true` (**forbidden**)
- `downstream_invocation_count>0`
- `forbidden_semantic_output_count>0`
- `navigation_instruction_leakage_count>0`
- Trace / replay / whitebox **missing** when required by harness charter
- `asset_report` **missing** when required
- `provider_exception`
- Provider output **empty** and **`not_available_reason` not set** (treat as failure → fallback)

Record **`fallback_used=true`** and **`fallback_reason`**.

---

## Disable / rollback flags (policy-level)

| Flag | Effect |
|------|--------|
| `disable_ocr_policy=true` | **Do not** apply default offline source policy; output `not_available` or use harness **explicit** mode (documented in run config). |
| `disable_rapidocr_ppocrv4=true` | Skip v4 mobile → start chain at `rapidocr_current` (subject to its conditions). |
| `disable_rapidocr_current=true` | Skip `rapidocr_current` → next is Vision (if eligible) else `not_available`. |
| `disable_macos_vision=true` | Skip Vision → **`not_available`** on Darwin if no earlier success. |

### Forbidden fallbacks (default chain)

- **Must not** fallback to **EasyOCR** as part of this default chain.  
- **Must not** fallback to **PaddleOCR current** as part of this default chain.  
- **Must not** fallback to **complex layout** providers (Surya, docTR, OCR-VL, etc.).  
- **Must not** switch provider **without** audit records (see audit doc).

---

## Prohibited default-chain providers (reminder)

`easyocr`, `paddleocr_current`, `rapidocr_ppocrv5_mobile_onnx`, **Tesseract** (unless future `classic_fallback_mode`), complex-branch stacks — **excluded** from **`ocr_default_offline_raw_text_source_policy_v0`** ordered chain.
