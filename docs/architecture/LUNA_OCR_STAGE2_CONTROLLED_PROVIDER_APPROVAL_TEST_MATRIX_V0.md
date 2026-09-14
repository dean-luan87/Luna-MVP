# LUNA — OCR Stage-2 Controlled Provider Approval Test Matrix v0

## Phase

- **Phase-Mainline-GuardedTrial-010**

## Matrix

### A. Paths

- `--static-config-root` readable (Phase-009 output)
- `--output-root` absolute and writable
- `--input-image` absolute, allowed extension, file exists

### B. Artifacts

- Dependency snapshot JSON
- Credentials snapshot JSON (**no secret logging**)
- Input sample snapshot JSON (**sha256 present**)
- Fallback snapshot JSON
- Runbook snapshot JSON (from Phase-009)
- Approval gate report JSON
- trace/replay/whitebox jsonl non-empty

### C. Hard boundaries

- `ocr_provider_invoked=false`, `ocr_model_invoked=false`
- `network_request_invoked=false`
- semantic / midplatform / scene / world / navigation / world-write / hive / TTS / Qwen all blocked
