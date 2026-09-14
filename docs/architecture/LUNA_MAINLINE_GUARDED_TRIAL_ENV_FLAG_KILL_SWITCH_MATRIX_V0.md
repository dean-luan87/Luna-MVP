# LUNA Guarded Trial Env Flag & Kill Switch 矩阵 v0

**Phase**：Phase-Mainline-RuntimeReadiness-002  
**机器可读源**：`mainline_guarded_trial_env_flag_matrix.json`（由 `run_mainline_guarded_trial_definition_v0.py` 生成）

---

## Global kill switch（必选）

| Flag | 默认值 | 为 true 时 |
|------|--------|------------|
| `LUNA_DISABLE_ALL_GUARDED_TRIALS` | **false** | **禁止** YOLO/OCR/Qwen Voice **全部** guarded trial；分项 flag 即使为 true 也不得运行 |

**优先级**：global disable **>** capability entry **>** provider/mode 子闸。

---

## YOLO（分项）

| Flag | 默认 | 角色 |
|------|------|------|
| `LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1` | false | Trial 总入口 |
| `LUNA_YOLO_TRIAL_MODE` | shadow_only | 模式枚举 |
| `LUNA_YOLO_TRIAL_MAX_FRAMES` | 0 | 帧预算（0＝内置默认） |
| `LUNA_YOLO_TRIAL_ABORT_ON_DETECTOR_ERROR` | true | 安全默认 |
| `LUNA_YOLO_TRIAL_WRITE_REQUEST_TRACE` | true | 观测默认开 |

---

## OCR（分项）

| Flag | 默认 | 角色 |
|------|------|------|
| `LUNA_ENABLE_OCR_GUARDED_TRIAL_V1` | false | Trial 总入口 |
| `LUNA_OCR_TRIAL_MODE` | shadow_only | 模式枚举 |
| `LUNA_OCR_TRIAL_PROVIDER_POLICY` | ocr_default_offline_raw_text_source_policy_v0 | policy 标识 |
| `LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION` | false | 真实 provider |
| `LUNA_OCR_TRIAL_ABORT_ON_GOVERNANCE_LEAKAGE` | true | 泄漏即 abort |
| `LUNA_OCR_TRIAL_WRITE_REQUEST_TRACE` | true | 观测 |

---

## Qwen Voice（分项）

| Flag | 默认 | 角色 |
|------|------|------|
| `LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1` | false | Trial 总入口 |
| `LUNA_QWEN_VOICE_TRIAL_MODE` | shadow_only | 模式枚举 |
| `LUNA_ENABLE_GOVERNED_QWEN_ENTRY_V1` | false | governed entry 闸 |
| `LUNA_ENABLE_QWEN_PRIMARY_VOICE_MODE_V1` | false | online_prefer_qwen trial |
| `LUNA_QWEN_VOICE_TRIAL_ALLOW_PROVIDER_INVOCATION` | false | 真实 provider |
| `LUNA_QWEN_VOICE_TRIAL_ALLOW_PLAYBACK` | false | 真实播放 |
| `LUNA_QWEN_VOICE_TRIAL_ABORT_ON_DIFF_AUDIT_MISSING` | true | 审计缺失 abort |
| `LUNA_QWEN_VOICE_TRIAL_WRITE_REQUEST_TRACE` | true | 观测 |

---

## 说明

- **Trial 入口类 flag** 默认必须为 **false**（验收项 E）。  
- 部分 **安全/观测** flag 默认为 **true**（abort on error、写 RequestTrace），表示「一旦启用 trial，默认行为偏保守、可观测」；**不**等同于开启 trial。  
- 本 Phase **不改变**仓库内既有 env 的语义实现；仅冻结 **trial 专用** 名称与意图，供后续接线 PR 对齐。
