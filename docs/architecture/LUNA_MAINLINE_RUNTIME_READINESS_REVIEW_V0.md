# LUNA 主线 Runtime Readiness Review v0

**Phase**：Phase-Mainline-RuntimeReadiness-001  
**范围**：YOLO → OCR → Voice / Qwen governed entry 在 **接入真实 runtime 之前** 的总评（只读文档与日志，不接真实推理、不调 Qwen、不播报、不执行 TTS）。  
**关联产物**：`tools/run_mainline_runtime_readiness_review_v0.py` 生成的 `logs/mainline_runtime_readiness_001_<timestamp>/`。

---

## 1. 结论摘要（事实层）

| 域 | Shadow / offline / governance | 真实 runtime 主链 |
|----|------------------------------|------------------|
| YOLO | RequestTrace shadow、Unified Core View 已 GO | 未闭合 |
| OCR | source policy、bridge、MidPlatform、SceneDelta、WorldContext、shadow、Core View 已 GO | 未闭合 |
| Voice governance | closed_v0，governed submit shadow GO | 真实 submit / playback 受 env 闸 |
| Qwen / TTS governed entry | Phase-000～003 GO，RequestTrace shadow 闭合 | `run_tts_unified_entry` 前闸门未接线；`real_qwen_invoked=false`，`real_tts_invoked=false` |

**一句话**：影子链与观测面已收口；**没有 kill switch、TRW 注入、abort/rollback 合同，就不能碰真实主链**。

---

## 2. 本阶段交付物

- **Readiness matrix**：`mainline_runtime_readiness_matrix.json`
- **Blocker register**：`mainline_runtime_blocker_register.json`
- **Wiring candidate matrix（仅登记，不接线）**：`mainline_runtime_wiring_candidate_matrix.json`
- **Env / kill switch matrix**：`mainline_runtime_env_flag_matrix.json`
- **TRW requirement matrix**：`mainline_runtime_trw_requirement_matrix.json`
- **Abort / rollback matrix**：`mainline_runtime_abort_rollback_requirement_matrix.json`
- **Summary**：`mainline_runtime_readiness_summary.json`
- **Notes**：`review_notes.md`

分级定义见：`LUNA_MAINLINE_RUNTIME_READINESS_LEVEL_POLICY_V0.md`。

---

## 3. 禁止项（本 Phase 红线）

- 不接真实 runtime；不真实调用 Qwen；不真实播报；不执行真实 TTS。
- 不改 YOLO/OCR/Qwen/Voice **主链实现**；不改 provider **默认策略**；不改 **env 语义**。
- 不删除 legacy voice / TTS fallback。
- 不接地图/GPS/点云；不进入 SceneTask/Fusion/Output；不上传蜂巢；不接推荐。

---

## 4. Provider health / timeout / fallback / circuit breaker（盘点）

接入前须在 TRW 与 abort 矩阵中可证明：

- **health**：provider 状态枚举与健康判定入口一致。
- **timeout**：分层超时（连接 / 首包 / 全句）与熔断协同。
- **fallback**：Qwen → Piper（或 suppress）链路与 governance 决策一致。
- **circuit breaker**：打开时写入 suppression/block_reason，保留 shadow 证据。

详见：`LUNA_MAINLINE_RUNTIME_TRW_REQUIREMENTS_V0.md`、`LUNA_MAINLINE_RUNTIME_ABORT_ROLLBACK_REQUIREMENTS_V0.md`、既有 `LUNA_TTS_LATENCY_AND_CIRCUIT_BREAKER_POLICY_V0.md`。

---

## 5. 禁止旁路（登记）

以下任一绕过均属 **high bypass risk**，必须先有 env 闸 + shadow 对比 + abort：

- 帧或 OCR 结果不经 RequestTrace stage 写入。
- 跳过 `voice_output_governance` 进入 `run_tts_unified_entry`。
- 跳过 governed provider entry / diff_audit 调用真实 provider。
- 使用私有 JSONL 通道替代 Unified Core View（观测漂移）。

完整候选接线点见：`LUNA_MAINLINE_RUNTIME_WIRING_CANDIDATE_MATRIX_V0.md`。

---

## 6. 下一 Phase 建议名称（占位）

- **Phase-Mainline-RuntimeReadiness-002**：YOLO/OCR/Voice 各自 **guarded trial** 范围冻结与接线 PR 模板（仍默认关闭）。

决策包：`LUNA_MAINLINE_RUNTIME_READINESS_GO_NO_GO_PACK_V0.md`。
