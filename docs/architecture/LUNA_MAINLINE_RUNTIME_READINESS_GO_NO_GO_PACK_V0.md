# LUNA 主线 Runtime Readiness Go / No-Go Pack v0

**Phase**：Phase-Mainline-RuntimeReadiness-001

---

## GO（本 Phase「runtime readiness review」交付）

下列条件 **同时** 满足 → 本 Phase **GO**：

- Readiness matrix、blocker register、wiring candidate、env、killing switch、TRW、abort/rollback **均已产出**。
- YOLO / OCR / Qwen Voice **均有** capability 行。
- **未接**真实 runtime；**未**真实调用 Qwen/TTS；**未**真实播报。
- **未**修改默认 provider 策略与 env 语义。

**脚本 verdict 字段**：`verdict.phase_review_documentation` = **GO**。

---

## CONDITIONAL_GO（下一跳「受控接线准备」）

- 部分日志快照目录在本地仓库 **缺失**（脚本记入 `review_notes`），但不影响矩阵结构。
- 若干 wiring point 须在 **下一接线 PR** 中与具体符号名对齐（已登记为 soft follow-up）。
- **guarded_wiring_preparation_next_phase** = **CONDITIONAL_GO**：须在 Phase-002 冻结 flag 名与验收脚本。

---

## NO_GO（红线）

任一成立 → **NO_GO**：

- 本 Phase **接入**真实 runtime 或真实 provider。
- 本 Phase **修改**默认 provider 或开启真实播报。
- **未**定义 kill switch / TRW 注入 / abort-rollback 即 **合并**接线 PR。
- 评审宣称 **R4/R5** 或「生产默认开启」。

**脚本 verdict**：`verdict.real_runtime_or_provider_activation` = **NO_GO**（直至专门 trial Phase）。

---

## Hard blockers（摘自生成 register）

见 `mainline_runtime_blocker_register.json`，典型包括：

- 真实 YOLO/OCR runtime 主链 **尚未验收闭合**。
- `run_tts_unified_entry` 前 **强制** governed entry / governance 与代码路径 **完全对齐**仍待接线 PR。
- VoiceOutputPlane 部分路径与「全量 SpeechGate」目标 **已知差距**（须在后续 Phase 追踪，不得在本 Phase 偷偷改主链「顺手修复」）。

---

## Soft follow-ups

- 统一 trace/export 本地日志目录若缺失，可在 CI 或 artifact 归档中补快照以便对比。
- YOLO/OCR 与设备相机 pipeline 的 **契约与性能基线**。
- Piper/Qwen 在真实网络下的 **超时矩阵复测**。

---

## Recommended next phase

**Phase-Mainline-RuntimeReadiness-002**（建议）：分别冻结 YOLO / OCR / Voice 的 **guarded trial** 范围、env 名、验收脚本与回滚手册；仍 **默认关闭**全部 trial flag。

---

**一句话**：影子链闭合后先做 **runtime 接入前体检**；kill switch、TRW、abort/rollback 不齐 → **不碰真实主链**。
