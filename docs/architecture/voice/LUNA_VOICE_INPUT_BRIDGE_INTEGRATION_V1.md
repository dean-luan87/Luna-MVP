# Luna 语音输入接线 v1（VoiceInputEvent → Bridge → Core 边界）

> **约束基线**：[LUNA_VOICE_STAGE1_OVERVIEW.md](./LUNA_VOICE_STAGE1_OVERVIEW.md)、[LUNA_VOICE_CONSTITUTION_V1.md](./LUNA_VOICE_CONSTITUTION_V1.md)、[LUNA_VOICE_MODEL_BOUNDARY_PRECHECK.md](./LUNA_VOICE_MODEL_BOUNDARY_PRECHECK.md)；任务链桥接见 [TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md](../../TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md)。

## 1. 为什么输入主线完成后要接 Bridge / Core

输入主线已产出统一 **`VoiceInputEvent`**，但若止步于此，主链仍无法以 **proposal/query/response** 形态消费输入。接线阶段把事件映射为既有 **`BridgeDecision`** + **`DeviceActionProposal` / `TaskActionProposal` / `TaskContextQuery` / `ConfirmationResponse`**（及可追踪 **reject**），使 Voice 仍 **不拥有裁决权**，仅提交候选与证据。

## 2. 本轮接通的类型

| 输入语义 | BridgeRouteType | 占位对象 |
|----------|-----------------|----------|
| 仅唤醒「艾达」、无白名单正文 | `SESSION_WAKE` | 无 proposal（会话激活） |
| 设备控制（音量、暂停等） | `DEVICE_CONTROL` | `DeviceActionProposal` |
| 任务生命周期（开始/暂停/结束/切换任务等） | `TASK_LIFECYCLE` | `TaskActionProposal` |
| 任务问询（到哪了、附近有什么等） | `TASK_CONTEXT_ENHANCEMENT` | `TaskContextQuery` |
| 确认证据（是/不是等） | `CONFIRMATION` | `ConfirmationResponse` |
| 会话结束类（不用了等） | `FEEDBACK_RESPONSE` | metadata（占位） |
| 路由拒绝 | `INPUT_REJECTED` | `VoiceInputRejectionResult` |
| 窗口内未命中白名单的长句 | `RESERVED_OPEN_DIALOGUE` | `execution_class=reject_or_degrade` |

## 3. VoiceInputEvent 如何映射到 Bridge

固定路径：

1. **`VoiceInputSessionManager.process_final_text`** → `VoiceInputEvent`
2. **`voice_input_to_bridge.voice_input_to_bridge_decision`**（可选经 **`adapt_voice_input_for_bridge`** 反查 `VoiceShortcutRegistry`）
3. **`BridgeDecision`**（`proposal` 字段承载上述占位对象之一）
4. **`dispatch_voice_bridge_to_core_placeholder`**：仅占位 trace，**不执行业务**

唤醒路径上，路由器会对 **去掉唤醒词后的正文** 再跑白名单匹配（例如「艾达，开始导航去医院」→ `task_start_nav`），避免仅唤醒、无 shortcut 时无法映射任务类短语。

### 3.1 任务态下「暂停 / 继续」与设备播报（白名单口径）

- **`is_task_mode=True`**：**「暂停」→ `task_pause`**，**「继续」→ `task_resume`**（`TaskActionProposal` / `TASK_LIFECYCLE`）。  
- **设备播报**：**「暂停播报」「继续播报」** → `dev_pause` / `dev_resume`（`DeviceActionProposal` / `DEVICE_CONTROL`）；另有 **「先暂停」** 仍属设备。  
- 这样短词优先服务 **任务链**，长词/显式短语服务 **播报与设备**，无需改路由器架构，仅白名单短语拆分即可。

## 4. 哪些输入会被 reject

- `VoiceInputEvent.router_decision == "reject"` → `BridgeRouteType.INPUT_REJECTED`，并附带 **`VoiceInputRejectionResult`**（含 `reason_code`、原文等），**不静默丢弃**。

## 5. 哪些命令会降级为确认（confirm_then_execute）

- **设备**：`requires_confirmation=True` 的条目（如 **关机**）→ `DeviceActionProposal.needs_confirmation=True`，`BridgeDecision.execution_class=confirm_then_execute`。
- **任务**：除 **`task_start_nav`（开始导航）** 外，其余任务控制类默认 **`confirm_then_execute`**（暂停/继续/结束/切换任务等），由 Core 最终裁决。

## 6. 当前明确不做什么

- 长语音开放式理解、闲聊、情感输入  
- LLM 意图拆解与关键词抽取（仅文档扩展位）  
- 输出主链（Piper/Fish/TTS 路由等）改造  
- UI  

---

变更清单：[LUNA_VOICE_INPUT_BRIDGE_INTEGRATION_CHANGESET_V1.md](./LUNA_VOICE_INPUT_BRIDGE_INTEGRATION_CHANGESET_V1.md)
