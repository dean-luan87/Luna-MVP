# LUNA Qwen Voice Controlled Trial Plan v0（Stage 3）

**Phase**：Phase-Mainline-GuardedTrial-001  
**启动条件**：Stage 1 YOLO = **GO** 且 Stage 2 OCR = **GO**。

---

## 1. 目标

验证 voice governance → governed entry → provider 选择 / diff audit / RequestTrace。**不**默认真实播放。

---

## 2. 分步（3A / 3B / 3C）

| 子阶段 | 内容 | Phase-001 状态 |
|--------|------|----------------|
| **3A** | governed entry dry-run；`provider_invoked=false`、`playback=false`；校验 selection/diff_audit | **计划中** |
| **3B** | 仅 3A GO 后；受控 provider invocation；仍 **`playback=false`** | **计划中** |
| **3C** | 仅 3B GO 后；极短播放窗口；**单独人工确认** | **本 Phase 不批准**，仅登记为未来项 |

---

## 3. 禁止（贯穿）

默认真实 Qwen、默认 TTS、默认 playback、绕过 governance、删除 Piper fallback、改默认 provider 策略、未经批准进入用户可听链路。

---

## 4. 验收 / Abort / Rollback（摘要）

见机器可读 `mainline_controlled_trial_acceptance_matrix.json` 与 `abort_rollback_matrix.json` 中 Stage_3 条目；Rollback 含关闭 `LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1`、关闭 provider invocation flag、强制 offline_only / `selected_provider=none`、保留日志与 post_trial_report。
