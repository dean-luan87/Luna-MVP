# LUNA — OCR Stage-2 Static Config Validation Go/No-Go Pack v0

## Phase

- **Phase-Mainline-GuardedTrial-009**

## GO

- `static_validation_result=GO`（或 `CONDITIONAL_GO`）
- source policy ready
- provider manifests static ok
- raw_text candidate schema ok
- fallback materials ok
- RequestTrace/TRW contract ok
- controlled provider runbook exists and `execution_allowed_by_this_phase=false`
- hard boundary remains clean（provider_invoked=false；不入 midplatform）

## NO_GO

- 任意材料缺失或不可解析
- 任意 forbidden scope 被触发（本阶段实现层面应恒为 false；若出现即视为治理泄漏）

## Commands（absolute output required）

运行：

- `python3 tools/run_ocr_stage2_static_config_validation_v0.py --output-root /Users/luanlei/LunaRuntime/logs/ocr_stage2_static_config_validation_009_<UTC>`

校验：

- `python3 tools/verify_ocr_stage2_static_config_validation_v0.py --output-root /Users/luanlei/LunaRuntime/logs/ocr_stage2_static_config_validation_009_<UTC>`

