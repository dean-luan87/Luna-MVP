# LUNA Guarded Trial Gate 与 Global Kill Switch v0

**Phase**：Phase-Mainline-RuntimeReadiness-003  
**实现模块**：`capabilities/runtime_readiness/guarded_trial_gate_v0.py`

---

## Global kill switch

| Flag | 默认 | 为 true 时 |
|------|------|------------|
| `LUNA_DISABLE_ALL_GUARDED_TRIALS` | false（未设置即关） | **所有** trial 强制 `forced_disabled_by_global_kill`，忽略分项 `LUNA_ENABLE_*` |

**优先级**：global kill **>** capability entry flag **>** mode / provider / playback 子闸。

---

## 分项入口（默认 false）

- `LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1`
- `LUNA_ENABLE_OCR_GUARDED_TRIAL_V1`
- `LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1`

---

## Mode 解析（仅解析，不执行 provider）

| Capability | 允许的模式 |
|------------|------------|
| yolo | `shadow_only`, `guarded_local` |
| ocr | `shadow_only`, `guarded_provider` |
| qwen_voice | `shadow_only`, `governed_entry`, `provider_dry_run`, `controlled_provider` |

非法字符串 → `trial_mode=invalid`，`decision=blocked_invalid_mode`。

---

## Gate decision 字段

与生成 JSON 对齐：`mainline_guarded_trial_gate_decisions.json` 中每条含 `global_kill_switch`、`entry_flag_enabled`、`trial_mode`、`decision`、`provider_invocation_allowed`、`playback_allowed`、`downstream_allowed`、`world_write_allowed` 等。

**默认空 env**：三条 trial 均为 `decision=disabled`，所有 `*_allowed` 为 false。

---

## TRW 与 gate 的衔接

`evaluate_guarded_trial_gate_v0(GuardedTrialGateInput(..., trw_payload=...))` 可在提供 payload 时调用 `validate_guarded_trial_trw_fields_v0`；校验失败且模式需要 TRW 时 → `blocked_missing_trw`（见实现）。
