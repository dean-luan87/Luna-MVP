# Luna 语音主线 V1：基础交互可用版 — 范围定义与现状映射（第一轮）

**文件**：`docs/architecture/voice/LUNA_VOICE_V1_PLAN.md`  
**性质**：版本规划 + 工程基线（**设计与梳理**；本轮不承诺实现完成度）  
**上位事实**：`capabilities/voice/README.md`（Voice 为可插拔板块、Stage-1 边界）、`docs/architecture/LUNA_MAINLINE_SYSTEM_STATUS_MAP_V1.md`（主线状态总图）  
**相关既有文档**：`LUNA_VOICE_INPUT_MAINLINE_V1.md`、`LUNA_VOICE_TIME_GOVERNANCE_V1.md`、`LUNA_VOICE_FINAL_TEXT_DISPATCH_INTEGRATION_V1.md`  
**最小闭环锚点（代码事实）**：`LUNA_VOICE_V1_MINIMAL_FLOW.md`  
**最小会话状态锚（设计）**：`LUNA_VOICE_V1_SESSION_STATE.md`  

---

## A. 版本目标（V1 是什么 / 不是什么）

- **V1 目标**：打通**基础语音交互闭环**——能听、能判、能答（或明确拒答）、能播，且在可控会话窗口内完成**一来一回**与**有限多轮**，并对**中断/继续**与**超时收口**有明确语义。
- **V1 不是**：高级智能对话产品、复杂任务编排中心、视觉融合、世界模型驱动、情绪系统深接入。

---

## B. V1 要做什么（最小能力包）

| 能力 | V1 期望语义 |
|------|-------------|
| 语音输入 | 将用户语音转为可路由文本，并进入统一 `VoiceInputEvent` |
| 语音输出 | 将系统应答以 TTS 路径提交（可 dry-run，但链路可观测） |
| 基础一来一回 | 单轮：输入 → 处理 → 输出 |
| 基础多轮 | 在会话窗口内可连续交互；窗口过期需重新唤醒/开会话 |
| 中断 / 继续 | 能对“暂停/继续/取消”等**白名单短控**给出一致语义（先以桥接候选为主） |
| 超时收口 | 静默切段、长捕获上限、会话窗口过期等行为可解释、可观测 |
| 最小会话状态 | 至少具备：会话窗口、运行相（idle/capturing/...）、短承接 hint |
| 真实性约束 | 见下文 **No Fabrication Rule**（硬约束） |

---

## C. V1 不做什么（明确排除）

- 复杂语义推理与开放域“万能问答”
- 视觉接入与多模态融合主线
- 高级任务链 / 长期任务状态机（超出最小桥接占位）
- 世界模型联动、情绪系统深接入、复杂长期记忆驱动决策

---

## D. V1 最小模块图（文字链路）

1. **语音输入层**：采集/ASR（可插拔）→ 路由/规范化 → `VoiceInputEvent`
2. **对话处理层**：长度分流 →（短）桥接决策 /（长）任务规划占位 → 与 Core 协议对象候选对接（Voice 不裁决）
3. **会话状态层**：时间治理 + 唤醒窗口 +（可选）`VoiceRuntimeContext` 注入
4. **语音输出层**：`SpeechRequest` → `VoiceOutputPlaneV1.submit` →（可选）TTS 执行 → playback 观测链
5. **输出真实性约束层**：策略性拒答、证据不足则追问/降级，不允许“无证据确定性编造”（见 **No Fabrication Rule**）

---

## E. V1 验收标准（草案，四类）

### 1) 交互闭环

- 输入能稳定落成 `VoiceInputEvent`；输出能稳定触发 `VoiceOutputPlaneV1.submit`（至少 dry-run 可观测闭环）
- 关键事件/request_id 可在 JSONL trace 中串联对齐（与仓库既有输出链观测一致）

### 2) 状态一致性

- 会话窗口、运行相、切段/强切原因在输入事件与观测中一致；不出现“口头状态”和“记录状态”打架

### 3) 输出真实性（硬）

- 满足 **No Fabrication Rule**；对不确定信息必须显式降级（模板/标记/追问），禁止假装确定

### 4) 降级能力

- Provider/执行失败时：可解释失败、可回退 dry-run/提示；主链路不因观测失败而崩溃（与当前“失败吞掉/可开关”的工程原则对齐）

---

## No Fabrication Rule（真实性硬约束）

本规则是 **V1 验收硬约束**，不是文风建议：

- **知道就是知道，不知道就是不知道**
- **不确定就必须显式标记不确定**（对用户可感知的措辞或结构化标记，二者至少其一）
- **禁止在证据不足时输出“确定事实陈述”**
- **追问优先于脑补**：宁可问清边界，也不填充不存在证据的细节
- **允许拒答**：拒答必须说明原因类别（例如：无权限/无信息/需要用户确认）

---

## F. 当前仓库映射（事实 → V1）

### F.1 可直接复用 / 已具备骨架（高优先级承接 V1）

| 区域 | 代表路径 | 现状作用 | 与 V1 关系 |
|------|----------|----------|------------|
| 输入协调 | `capabilities/voice/runtime/voice_input_session_manager.py` | 组装 `VoiceInputEvent`，可直连 `dispatch_voice_final_text` | **V1 输入主入口骨架** |
| 主分流 | `capabilities/voice/runtime/voice_final_text_dispatcher.py` | 短/长/reject 分流；runtime_context 侧观测链 | **V1 对话处理中枢（能力已落地，边界需收敛）** |
| 路由/桥接 | `capabilities/voice/bridge/voice_input_router.py`、`bridge/voice_input_to_bridge.py` | 文本路由与 BridgeDecision 占位/候选 | **V1 短链最小闭环关键拼图** |
| 时间治理 | `capabilities/voice/runtime/voice_time_governance_v1.py`、`runtime/voice_wake_window_manager.py` | 30s 会话窗、切段/强切、四态 | **V1 多轮/超时收口核心** |
| 输出平面 | `capabilities/voice/output/voice_output_plane_v1.py`、`output/playback_*` | submit 真闭环锚点 + trace | **V1 输出闭环关键** |
| 协议对象 | `capabilities/voice/schemas/voice_input_event.py`、`schemas/speech_request.py`、`schemas/voice_runtime_context.py` | 统一事件/请求/context | **V1 数据契约基础** |
| 观测 | `capabilities/voice/observations/*` | request/playback/output 观测 | **V1 可验收、可对账** |

### F.2 需要补齐 / 与 README 声明存在张力之处（V1 必须正视）

| 主题 | 事实 | V1 含义 |
|------|------|---------|
| “Stage-1 不接真实 ASR/TTS” | `capabilities/voice/README.md` 仍写不接真实 provider | V1 若要做到“可用版”，需要**明确一条受控接线策略**（哪些文件允许接、默认仍 dry-run）并回写边界文档 |
| Core 裁决与 Voice 边界 | Voice 不拥有主权（README） | V1 必须定义：**哪些应答由 Core 生成**、Voice 只搬运；避免 Voice 侧“越权编造” |
| 长语音/模型链路 | `bridge/voice_long_input_*`、`providers/*` 体量大 | V1 可先**限制范围**（仅短链 + 受限长链），避免把 M3 长语音治理误当成 V1 必选项 |

### F.3 建议暂时绕开（后续阶段）

- 大规模 prefilter/路由灰度实验文档族（`LUNA_VOICE_PREFILTER_ROUTING_M3_5*.md` 等）：作为研究/治理资产保留，但 **不作为 V1 交付必要条件**
- 复杂 request trace 诊断体系：保留为工程能力，但 V1 只取**最小可观测集合**

---

## 附录：本轮已检查的主要工程目录（代码侧）

以下目录均已做结构级盘点（以 `capabilities/voice/**` 文件清单 + 关键 README/入口模块阅读为准）：

- `capabilities/voice/`
- `capabilities/voice/runtime/`
- `capabilities/voice/interfaces/`
- `capabilities/voice/output/`
- `capabilities/voice/observations/`
- `capabilities/voice/bridge/`
- `capabilities/voice/schemas/`
- `capabilities/voice/docs/`
- 并纳入 `capabilities/voice/providers/`、`config/` 作为输入/输出可插拔相关区域

---

## 下一轮建议最先动手的 1～2 个点（实现向，但仍保持小步）

1. **把 V1 的“可用闭环定义”从文档落到单一入口**：明确“从 `VoiceInputSessionManager` 到 `VoiceOutputPlaneV1.submit`”的最小调用样例与默认开关矩阵（仍可在 dry-run 下验收闭环）。
2. **对齐边界文档与代码事实**：更新 `capabilities/voice/README.md` / `runtime/README.md` / `output/README.md` 中仍写“Stage-1 仅占位”的句子，使其与 `VoiceOutputPlaneV1`、输入主链已存在的事实一致，避免团队误读。
