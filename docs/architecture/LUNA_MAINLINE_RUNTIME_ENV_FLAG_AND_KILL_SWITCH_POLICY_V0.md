# LUNA 主线 Runtime Env Flag & Kill Switch Policy v0

**Phase**：Phase-Mainline-RuntimeReadiness-001  
**原则**：凡通往真实推理 / 真实 TTS / 真实播报的路径，须有 **显式 env**，**默认 false**；rollback 行为须可叙述。

机器可读表：`mainline_runtime_env_flag_matrix.json`（review 脚本生成）。

---

## Voice / Qwen（已存在或高频引用）

| flag | 用途（摘要） | default |
|------|----------------|---------|
| `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1` | VoiceOutputPlane submit 闭环总闸 | false |
| `LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS` | submit 内是否进入 `run_tts_unified_entry` | false |
| `LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1` | 扬声器 / playback 真执行 | false |

**Rollback**：上述任一置 **0/false** → 回到 dry-run / 无真实播报路径（与既有代码注释一致）。

---

## Voice / Qwen（建议新增，接线 PR 冻结名称）

| flag | 用途 | default |
|------|------|---------|
| `LUNA_ENABLE_GOVERNED_QWEN_ENTRY_V1` | 强制 governed entry 进入真实 TTS 前置链 | false |
| `LUNA_ENABLE_QWEN_PRIMARY_VOICE_MODE_V1` | 显式 trial online_prefer_qwen（与 yaml 默认解耦） | false |

**说明**：名称可在 Phase-002 接线前最终冻结；本 Phase **不改变**任何默认 provider 策略。

---

## YOLO / OCR（占位）

- `LUNA_*_YOLO_RUNTIME_TRIAL_V1`（占位）：在线 detector / 帧主链 trial 总闸。
- `LUNA_*_OCR_RUNTIME_TRIAL_V1`（占位）：在线 OCR provider trial 总闸。

具体前缀与命名在 **首个 guarded wiring PR** 中与 MidPlatform/OCR 合同一并冻结。

---

## OCR source / bridge（未来接线时）

- Source policy 与 YOLO→OCR bridge 在 runtime 下必须 **可观测**；若尚无独立 flag，须在接线 PR 中拆分 **read path** 与 **trial path**，避免隐式默认开启。

---

## Kill switch 与 owner

| owner | 含义 |
|-------|------|
| runtime | 运行实例上的实时闸 |
| shadow | 仅影响影子/导出，不影响用户感知 |
| sandbox | 开发 / 短窗 trial |

**未定义 kill switch 即建议接线 → NO_GO**（见 GO 包）。
