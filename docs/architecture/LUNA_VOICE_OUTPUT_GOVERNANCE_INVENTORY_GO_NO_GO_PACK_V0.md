# Phase-Voice-OutputGovernance-000
# Voice Output Governance Inventory Go/No-Go Pack v0（盘点阶段决策包）

**阶段目标**：完成“旧语音输出链”资产盘点（代码/文档/开关/观测/缺口），形成后续增强治理层的基线证据。  
**硬边界**：本阶段只盘点；不改 runtime、不接新 TTS、不改真实播报行为、不删 legacy、不改现有 env 开关、不接新链路。

---

## 1. Scope（范围）

- **In scope**：
  - 现有 Voice/TTS/Output/Speech Gate 相关代码资产定位与角色说明
  - 现有文档资产定位与有效性判断
  - 现有 env 开关与行为盘点
  - 现有 runtime flow 摘要（input→guard/gate→dispatch→output plane→submit→tts/playback）
  - 现有 observability（trace/log/whitebox）字段与缺口
  - gap table（timeout/priority/cancel/expiry/interruption/provider health/queue/stale/gate result/real_tts_invoked）

- **Out of scope（明确禁止）**：
  - 改任何真实播报链路行为
  - 接入/替换/新增任何 TTS provider
  - 改变或重命名任何现有 env 开关语义/默认值
  - 删除/迁移 legacy voice 代码
  - 新增导航/中台/SceneTask/Fusion/Output 新链路

---

## 2. Evidence checklist（证据清单：本阶段必须找到/输出）

### 2.1 已找到的主链路证据（本阶段盘点结论）

- **主链路入口**：`VoiceInputSessionManager.process_final_text_with_dispatch(...)`  
  - code：`capabilities/voice/runtime/voice_input_session_manager.py`
- **分流入口**：`dispatch_voice_final_text(...)`  
  - code：`capabilities/voice/runtime/voice_final_text_dispatcher.py`
- **输出平面**：`get_voice_output_plane_v1().submit(SpeechRequest)`  
  - code：`capabilities/voice/output/voice_output_plane_v1.py`
- **输出请求对象**：`SpeechRequest`（包含 priority/interruptible 等占位字段）  
  - code：`capabilities/voice/schemas/speech_request.py`
- **真实 submit 总开关**：`LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1`  
  - code/doc：`voice_final_text_dispatcher.py`、`docs/architecture/voice/LUNA_VOICE_V1_MINIMAL_FLOW.md`
- **Session anchor**：`VoiceV1SessionStateAnchor`  
  - code：`capabilities/voice/runtime/voice_v1_session_state_anchor.py`
- **Speech Gate**：`SpeechGate`（存在实现）  
  - code：`core/speech_gate.py`
- **Piper/Fish provider**：存在实现与配置入口  
  - code：`capabilities/voice/providers/piper_tts_provider.py`、`（已移除）`
- **观测/trace**：`LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL` JSONL envelope  
  - code/doc：`voice_output_plane_v1.py`、`docs/architecture/cross_domain/LUNA_REAL_OUTPUT_SUBMIT_V1_IMPLEMENTED_NOTE.md`

### 2.2 已识别的关键缺口（本阶段盘点结论）

- **`guard_v1_speakable_text` 实现未定位**：文档引用存在，但代码中未找到同名实现；当前仅见最小 token guard（unknown/todo/placeholder）  
  - 影响：后续增强需先做“命名/实现/接线点”对齐与审计
- **Speech Gate 接线点不明确**：`core/speech_gate.py` 存在，但是否在输出主链实际作为最终裁决调用需确认  
  - 影响：后续增强需补齐 gate-result 观测与统一裁决入口

---

## 3. GO conditions（通过条件）

满足以下全部条件判定 **GO**：

- **找到 voice output 主链路**：入口、分流、submit helper、output plane 的代码锚点路径明确
- **找到真实 submit 开关**：`LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1` 的读取位置与语义明确
- **找到 guard / gate 相关实现或文档**：
  - 至少定位到 `SpeechGate` 实现与其语义
  - 对 `guard_v1_speakable_text` 的“存在/缺失/替代实现”作出明确盘点结论
- **找到 legacy / Piper / Fish 当前状态**：provider 实现文件与配置入口明确
- **观测面可追溯**：至少明确 JSONL trace 路径、envelope 类型、关键白盒字典入口
- **缺口明确**：gap table 覆盖你指定的 10 个治理点，并给出“已有占位/缺失”的结论
- **边界未破坏**：本阶段未引入任何 runtime 行为改变（只新增/修改文档与索引）

---

## 4. CONDITIONAL_GO（条件通过）

允许在以下情况判定 **CONDITIONAL_GO**（可进入下一阶段，但必须先补齐条件）：

- **Speech Gate 接线点尚未完全确认**：可先进入 Phase-001 的 contract 定义，但必须在 Phase-001 里把“接线点与 gate-result 观测”列为 hard gate（不能拖到实现期再补）
- **provider 健康/依赖就绪的既有字段分散**：允许先定义统一健康快照 contract，但必须把“现有观测字段映射表”列为 Phase-001 的 deliverable

---

## 5. NO-GO conditions（否决条件）

出现任一情况判定 **NO-GO**：

- 盘点阶段改了真实播报行为（包括默认路径、submit 条件、执行链路）
- 删除/迁移 legacy voice 代码
- 直接接入新 provider（Piper/Fish/Qwen/其他）或改变 provider 选择策略
- 绕过 Speech Gate（新增旁路 submit/播放路径且不受 gate 管控）
- 未输出缺口表/未明确缺口就进入实现或增强

---

## 6. 本阶段产出与文件清单（验收用）

- **新增**：
  - `docs/architecture/LUNA_VOICE_OUTPUT_GOVERNANCE_EXISTING_ASSET_INVENTORY_V0.md`
  - `docs/architecture/LUNA_VOICE_OUTPUT_GOVERNANCE_INVENTORY_GO_NO_GO_PACK_V0.md`
- **修改**：
  - `docs/architecture/README.md`（加入 Phase-Voice-OutputGovernance-000 索引）

---

## 7. Verdict（本次盘点结论）

- **结论**：**GO（盘点完成）**  
- **Hard blockers**：
  - `guard_v1_speakable_text` 同名实现未定位（需要后续阶段明确“真实实现/替代实现/废弃策略”）
  - Speech Gate 在输出主链的接线点仍需专项确认（避免出现“gate 存在但不生效”的治理空洞）
- **Recommended next phase**：
  - `Phase-Voice-OutputGovernance-001: Voice Output Timeout / Priority / Cancellation / Expiry / Interruption / Provider Health Contract v0`

---

## 8. 本阶段产出声明（必须）

- 本阶段只做盘点：**不改 runtime**、不真实播报、**不接新 provider**、不删除 legacy voice、**不改 env 开关**。

