# Luna 长语音反馈与互动机制 v1

> 目标不是「说得很像人」，而是：**让用户稳定地知道系统听懂什么、打算怎么做、缺什么、做不了什么、执行到哪一步**。  
> 本层定义语义类别、占位模板与统一结果对象；**不**绑定 TTS、**不**自动播报。

## 0. 情感引擎与任务编排的边界（必须先写死）

情感引擎**不是**聊天外挂，而是任务理解与编排的**增强层**：可在「体验目标」上提出建议（如顺路甜品店、偏好记忆）。

**系统原则**：情感引擎可以增强任务理解与任务建议，**不得直接篡改用户明确任务**。

| 允许 | 不允许 |
|------|--------|
| 加建议、体验优化候选、情绪友好选项 | 把「去商场」**偷偷改成**「先去甜品店」 |
| 弱插入、不影响主任务锚点的提示 | 未经确认的强替换主任务 |

**例外**：用户明确确认；或建议为弱插入且不改变用户声明的主目标。

后续 `experience_enhancement_suggestion` 挂在 **task_plan_v2** 候选上，与主任务分离。

---

## 1. 主反馈 6 类（固定枚举）

| # | `feedback_mode` | 场景 | 模板方向 |
|---|-----------------|------|----------|
| 1 | `task_understood_and_ready` | 理解清楚、参数够、可生成 task_plan_v1、可进入下一阶段 | 「我明白了。接下来我会先做 A，再做 B。」 |
| 2 | `task_understood_but_need_clarification` | 大体理解但关键信息缺失 | 「我知道你想做 A，但还需要你告诉我 B。」 |
| 3 | `task_understood_but_need_confirmation` | 理解清楚但影响任务链 / 顺序优化 / 高影响动作 | 「我建议这样安排：先做 A，再做 B。你要我这样做吗？」 |
| 4 | `partially_supported` | 一部分能做，一部分当前不能做 | 「我可以先帮你做 A，但 B 这一步我现在还不能直接处理。」 |
| 5 | `unsupported_or_rejected` | 不支持、越权、高风险 | 「这个请求我现在还不能直接执行。」 |
| 6 | `mixed_input_acknowledged` | 混合型长语音：任务 + 非任务/情绪/背景 | 「我先帮你处理任务部分，其他内容我记住了。」 |

代码：`capabilities/voice/schemas/voice_long_input_feedback_kind.py`（`PRIMARY_FEEDBACK_MODES_V1`）。

---

## 2. 与三层计划对象的对应关系

| 计划层 | 反馈侧重 | 说明 |
|--------|----------|------|
| **task_plan_v1** | 听懂什么、原始顺序、缺什么参数 | 当前大多数反馈落在此层 |
| **task_plan_v2**（预留） | 顺序/体验增强建议、优化候选 | 模板与 `task_understood_but_need_confirmation`、未来 `experience_enhancement_suggestion` 对齐 |
| **task_plan_final**（预留） | 定稿后的执行承诺 | 「好的，我按这个顺序来。先做 A，再做 B。」 |

当前阶段 V1 反馈**只反映**当前规则解析结果；**不提前**宣称 V2 优化已完成，除非进入「需确认」类反馈。

---

## 3. 执行过程反馈 4 类

| `feedback_mode` | 模板方向 |
|-----------------|----------|
| `execution_started` | 「我开始处理了。先做 A。」 |
| `execution_progress` | 「已经完成 A，接下来做 B。」 |
| `execution_waiting_user` | 「我现在需要你确认一下，是否继续做 B？」 |
| `execution_completed` | 「已经完成这次任务。」 / 多步合并说明 |

代码：`EXECUTION_FEEDBACK_MODES`（与主 6 类并列枚举，供编排/执行层消费）。

---

## 4. 无任务模式

### A. 无任务观察（一次性）

直接回答观察结果，不进入长期任务链。

### B. 无任务长对话

当前不接情感引擎，**不**当无效拒绝。反馈语义接近：

- 「我听到了。这个我先记下来。」

对应解析侧：`non_task_dialogue_future` + `voice_feedback` 中 `no_task_long_dialogue_ack`（见 `voice_long_input_feedback_kind.py`）。

---

## 5. 临时插话 vs 临时插入任务

| 类型 | 行为 | 反馈 |
|------|------|------|
| 一次性临时问询 | 直接结果，**不改变**主任务链 | `temp_query_direct` |
| 临时插入任务 | `task.insert_temporary` / 恢复点 | `temp_insert_task_ack`：「我会先带你去厕所，之后再继续去医院。」 |

两类**不能混**，避免过度编排。

---

## 6. 情感引擎预留：`experience_enhancement_suggestion`

未来：体验增强建议（非主任务、非纯闲聊），例如「商场里新开了甜品店，要不要顺便看看？」。

归类常量：`EXPERIENCE_ENHANCEMENT_SUGGESTION`；建议挂在 **v2 候选**，**不**覆盖用户明确主任务。

---

## 7. 统一反馈结果对象

解析后统一落在 `VoiceLongVoiceFeedbackResult`（`capabilities/voice/schemas/voice_long_voice_feedback_result.py`）：

- `feedback_mode`
- `feedback_text_candidate`
- `requires_user_response`
- `related_plan_version`：`v1` | `v2` | `final` | `none`
- `non_task_acknowledged`

`VoiceLongInputParseResult.voice_feedback` 由 `derive_long_voice_feedback_result` 在 `run_long_input_task_planning_v1` 返回前填充；`to_dict()` 含 `voice_feedback` 字段。

---

## 8. 当前阶段硬规则

1. **任务反馈优先于情绪表达**（文案上先把任务说清楚）。
2. **非任务内容不丢弃**，但也不假装已被情感引擎深度处理。
3. **V1 反馈只反映当前理解**，不提前说 V2 优化结果，除非进入确认型反馈。
4. **部分支持必须拆开说**，不能整段一刀切拒绝。
5. **执行反馈**须让用户知道：已完成什么、接下来做什么。

---

## 9. 与输出主链的关系

策略层消费 `voice_feedback` 后生成最终话术；**不**在本轮修改 Piper/Fish、selector、rollback 等输出主链。
