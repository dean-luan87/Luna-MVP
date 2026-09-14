# LUNA — OCR Stage-2 Controlled Provider Test Matrix v0

## Phase

- **Phase-Mainline-GuardedTrial-011**

## Matrix

### A. Approval input

- `--approval-root` readable
- input snapshot match: path/sha256/size

### B. Provider

- selected provider is local/mock/offline
- no network request
- provider invoked once (or clean fallback to not_available)

### C. Outputs

- raw_text candidate JSON exists
- schema validation exists and passes
- post-trial report exists
- trace/replay/whitebox jsonl non-empty

### D. Governance

- semantic/midplatform/scene/world all false
- downstream=0; navigation null; no world write; no hive upload; no TTS/Qwen

