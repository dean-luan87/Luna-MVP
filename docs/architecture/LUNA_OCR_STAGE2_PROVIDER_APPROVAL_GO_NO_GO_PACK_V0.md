# LUNA — OCR Stage-2 Provider Approval Go/No-Go Pack v0

## Phase

- **Phase-Mainline-GuardedTrial-010**

## GO

- Static config root readable
- Valid input image sample + sha256
- Dependency snapshot generated
- Credential snapshot generated with **no secrets logged**
- Fallback snapshot OK
- Runbook snapshot present (`found=true`)
- Hard audit clean; trace/replay/whitebox non-empty
- Verifier passed

## CONDITIONAL_GO

- Optional credentials absent but offline/`not_available` path acceptable
- Dependency import differs on target machine (needs re-verify)

## NO_GO

- Invalid/missing input sample
- Missing static config / runbook snapshot
- Secret values leaked into logs
- Any OCR provider/model/network invocation in this phase

## Commands (absolute paths)

```bash
python3 tools/prepare_ocr_stage2_provider_approval_gate_v0.py \
  --static-config-root /Users/luanlei/LunaRuntime/logs/ocr_stage2_static_config_validation_009_<UTC> \
  --input-image /absolute/path/to/sample.png \
  --output-root /Users/luanlei/LunaRuntime/logs/ocr_stage2_provider_approval_gate_010_<UTC>

python3 tools/verify_ocr_stage2_provider_approval_gate_v0.py \
  --static-config-root /Users/luanlei/LunaRuntime/logs/ocr_stage2_static_config_validation_009_<UTC> \
  --output-root /Users/luanlei/LunaRuntime/logs/ocr_stage2_provider_approval_gate_010_<UTC>
```
