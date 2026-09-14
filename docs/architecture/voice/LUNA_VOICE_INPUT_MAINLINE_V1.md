# Luna 语音输入主线 v1

> **前置依赖与口径**：请先阅读并遵循  
> - [LUNA_VOICE_STAGE1_OVERVIEW.md](./LUNA_VOICE_STAGE1_OVERVIEW.md)（Voice 总纲、三入口概念）  
> - `capabilities/voice/runtime/README.md`（运行态目录说明）  
> - [TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md](../../TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md)（任务链 × 主链 × 桥接）  
> 以及任务链快照 / Bridge 交付相关 M0 文档（与 proposal/query/response 一致，不另起一套「语音指令系统」）。

## 1. 为什么先做最小输入主线

在完整对话系统、情感引擎、开放式长语音理解之前，需要先把 **受控的「能听」路径** 立住：

- 统一经 `VoiceInputEvent` 进入后续 Bridge / 任务链，禁止裸文本直闯主链。
- 用 **唤醒词 + 会话窗口 + 白名单短指令 + 任务态分流** 把输入面收窄，可测、可治理。
- 与 Stage-1 的 **proposal/query/response** 思路对齐，不绕开既有协议。

本阶段目标：**能听、能分流、能记住当前一小段上下文、能受控地进入任务链与 Bridge** —— 不是把 Luna 做成完整语音助手。

## 2. 三入口定义（v1 唯一合法入口）

| 入口 | 条件 | 行为 |
|------|------|------|
| **唤醒词入口** | 文本包含固定唤醒词「艾达」 | 打开/刷新会话窗口；去掉唤醒词后的正文进入后续处理 |
| **会话窗口入口** | 当前处于 **active_window**（30 秒内有效且未过期） | 无需再说「艾达」，整句进入路由 |
| **任务短指令入口** | 当前 **任务态**（`is_task_mode=True`）且命中白名单 | 即使未唤醒、窗口已过期，仍允许进入（受任务态与条目约束） |

其余语音输入一律 **reject**（或上游不入管线），**不得** 增加「自由长语音」暗门。

## 3. 唤醒词固定为「艾达」

- v1 **固定**为 **艾达**（中文，发音相对稳定，避免 Luna 的 L/N 类混淆）。
- 不实现多唤醒词、不实现模糊匹配泛滥；扩展位留在路由常量/配置，**本轮策略保持简单**。

实现参考：`capabilities/voice/bridge/voice_input_router.py` 中 `WAKE_WORD`。

## 4. 两层时间规则

### 4.1 3 秒：输入切段（句结束）

- **含义**：语音停止（静默）超过 **3 秒**，视为 **当前这一句 / 当前这一轮** 结束，可将本句文本送入处理管线。
- **不是**会话失效规则；会话窗口仍由 30 秒规则管理。
- 实现：`capabilities/voice/runtime/voice_segment_timeout_policy.py`（`VoiceSegmentTimeoutPolicy`）。  
- 上游在检测到 **一句结束** 后调用 `VoiceInputSessionManager.process_final_text(...)`（本模块不直接采集音频）。

### 4.2 30 秒：会话窗口（免唤醒连续对话）

- 用户首次说「艾达」并成功接受后，进入 **active_window**。
- 窗口内后续输入 **无需**重复唤醒词。
- **每次有效输入**（路由接受）**刷新** 30 秒计时。
- 超过 30 秒无有效输入 → 窗口 **expired**，之后必须重新说「艾达」（除非任务态白名单另行放行）。
- 关机 / 长待机 / 任务彻底结束 / 用户显式「结束对话」类白名单 → **清空窗口**（见窗口管理器）。

实现：`capabilities/voice/runtime/voice_wake_window_manager.py`（`VoiceWakeWindowManager`）。

## 5. 任务态 / 普通态分流

- **任务态**（`is_task_mode=True`）：系统已有主任务链运行时，允许白名单短指令、任务进度问询、暂停/继续/取消等（以白名单为准）。
- **普通态**（`is_task_mode=False`）：无任务时，主要依赖 **唤醒词** 或 **窗口内** 输入；白名单仅允许在注册表中 `allowed_in_normal_mode=True` 的条目（如部分设备控制、会话结束等）。

路由：`capabilities/voice/bridge/voice_input_router.py` 中 `route_voice_text`。

## 6. 白名单短指令原则

- 本轮 **不做**大模型长语音拆解；仅 **白名单短指令** 走捷径路径。
- 白名单 **集中注册**，不散落在业务分支：`capabilities/voice/runtime/voice_shortcut_registry.py`。
- 明细与确认策略见：[LUNA_VOICE_SHORTCUT_WHITELIST_V1.md](./LUNA_VOICE_SHORTCUT_WHITELIST_V1.md)。

> **后续扩展（明确不在 v1 实现）**：将引入 **大模型** 从长语音中提炼关键词并映射为任务链动作，该能力属于 **语音输入扩展层**，不属于 v1 白名单主线。

## 7. 短期记忆 / 上下文承接（最小目标）

v1 只做 **最小承接**：

- 通过 `VoiceInputEvent.context_resume_hint` 等字段，携带 **上一轮与本轮** 的 strip 后摘要（用于 Bridge / 任务链消费）。
- **不做**自由长多轮推理、情感理解、LLM 开放式意图拆解。

协调器：`capabilities/voice/runtime/voice_input_session_manager.py`。

## 8. ASR 与统一事件

- 所有 ASR 经 **`ASRProvider` 协议**（`capabilities/voice/interfaces/asr_provider.py`），禁止业务散点直调。
- 可先使用 **`MockASRProvider`**（`capabilities/voice/providers/mock_asr_provider.py`）做骨架联调。
- 管线在 **句结束** 后产出统一 **`VoiceInputEvent`**（含 `request_id`、`session_id`、`raw_text`、`normalized_text`、`wake_word`、`active_window`、`task_shortcut`、`is_task_mode`、`shortcut_id`、`router_decision`、`context_resume_hint` 等），定义见 `capabilities/voice/schemas/voice_input_event.py`。

## 9. 当前明确不做什么

- 自由闲聊主线、情感输入分析  
- 大模型开放式长语音理解与拆解（v1 仅预留扩展说明）  
- 复杂多轮对话系统  
- 云端 ASR / 真实流式 ASR 生产化  
- UI、输出主链重构  

---

**验收对照**：见 [LUNA_VOICE_INPUT_MAINLINE_CHANGESET_V1.md](./LUNA_VOICE_INPUT_MAINLINE_CHANGESET_V1.md)。
