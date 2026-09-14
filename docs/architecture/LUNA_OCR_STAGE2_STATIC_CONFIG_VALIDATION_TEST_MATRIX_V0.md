# LUNA — OCR Stage-2 Static Config Validation Test Matrix v0

## Phase

- **Phase-Mainline-GuardedTrial-009**

## Matrix

### A. Source policy

- selector module exists: `capabilities/model_ocr/offline_source_policy_v0.py`
- `SOURCE_POLICY_ID_OCR_V0 == ocr_default_offline_raw_text_source_policy_v0`
- policy doc exists: `docs/architecture/LUNA_OCR_DEFAULT_OFFLINE_SOURCE_POLICY_V0.md`

### B. Provider manifests（static）

- directory exists: `configs/models/ocr/`
- `*_manifest_v0.json` 至少 1 个
- 每个 manifest 可解析为 object 且包含可识别 id（`provider_id|model_id|id|name|model_config_id|model_name`）

### C. Raw text candidate schema contract

- schema 非空
- required: `text`, `confidence`, `bbox`

### D. Fallback / not_available materials

- doc exists: `docs/architecture/LUNA_OCR_OFFLINE_SOURCE_SELECTION_AND_FALLBACK_POLICY_V0.md`
- selector supports terminal `not_available`

### E. RequestTrace / TRW contract materials

- TRW validator module exists: `capabilities/runtime_readiness/guarded_trial_trw_validator_v0.py`
- stage mapping doc exists: `docs/architecture/LUNA_OCR_REQUEST_TRACE_STAGE_MAPPING_DEFINITION_V0.md`
- shadow adapter module exists: `capabilities/core_trw/ocr_request_trace_shadow_adapter_v0.py`

### F. Controlled provider runbook

- runbook emitted
- `execution_allowed_by_this_phase=false`

