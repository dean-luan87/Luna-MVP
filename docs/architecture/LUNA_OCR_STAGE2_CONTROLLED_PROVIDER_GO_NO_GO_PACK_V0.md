# LUNA — OCR Stage-2 Controlled Provider Go/No-Go Pack v0

## Phase

- **Phase-Mainline-GuardedTrial-011**

## GO

- approval root readable
- input snapshot match = true
- provider invoked (local) OR clean not_available fallback
- raw_text candidate generated
- schema valid
- network_request_invoked=false
- semantic/midplatform/scene/world all false
- TRW (trace/replay/whitebox) non-empty
- verifier passed

## CONDITIONAL_GO

- provider unavailable but not_available handled cleanly; raw_text empty but schema valid

## NO_GO

- snapshot mismatch (must abort, no provider invocation)
- network request attempted
- semantic/downstream/midplatform invoked
- secret leaked

## Commands (absolute paths)

```bash
python3 tools/run_ocr_stage2_controlled_provider_trial_v0.py \
  --approval-root /Users/luanlei/LunaRuntime/logs/ocr_stage2_provider_approval_gate_010_<UTC> \
  --output-root /Users/luanlei/LunaRuntime/logs/ocr_stage2_controlled_provider_trial_011_<UTC>

python3 tools/verify_ocr_stage2_controlled_provider_trial_v0.py \
  --approval-root /Users/luanlei/LunaRuntime/logs/ocr_stage2_provider_approval_gate_010_<UTC> \
  --output-root /Users/luanlei/LunaRuntime/logs/ocr_stage2_controlled_provider_trial_011_<UTC>
```

