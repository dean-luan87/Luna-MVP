# Luna Badge v1.4.3 - 硬契约规范

**版本**: v1.4.3  
**创建日期**: 2025-12-05  
**状态**: 📋 规范文档

---

## 📋 概述

本文档定义了决策层（Decision Layer）与各模块之间的"硬契约"规范，确保所有模块之间的接口参数统一、可预测。

---

## 1. DecisionAction 硬契约约定

### 1.1 CONTINUE_TASK

**语义**: 继续当前任务链按既定节点往下走。

**DecisionOutput 格式**:

```python
DecisionOutput(
    action=DecisionAction.CONTINUE_TASK,
    reason="xxx",
    params={
        "task_id": str,              # 当前任务ID（必需）
        "node_id": Optional[str],     # 可选：下一节点ID（如不指定则由 TaskChain 自己接着跑）
    }
)
```

**约定**:
- 如果不传 `node_id`，约定 TaskChain 自己基于当前状态推进到下一节点
- `task_id` 必须存在，用于标识当前任务

**示例**:
```python
DecisionOutput(
    action=DecisionAction.CONTINUE_TASK,
    reason="next_node_available",
    params={
        "task_id": "nav_to_hospital_1",
        "node_id": "hospital_entrance"  # 可选
    }
)
```

---

### 1.2 INSERT_TASK

**语义**: 在主任务中间插入一个子任务（如"先上厕所"）。

**DecisionOutput 格式**:

```python
DecisionOutput(
    action=DecisionAction.INSERT_TASK,
    reason="user_insert_task" | "system_recommend",
    params={
        "main_task_id": str,          # 当前主任务ID（必需）
        "insert_task_spec": dict,     # 子任务定义（必需）
        "resume_strategy": str        # "auto" | "ask"（必需）
    }
)
```

**insert_task_spec 格式**:
```python
{
    "type": str,                      # 任务类型，如 "go_to_toilet"
    "target": dict,                   # 目标信息
    "priority": str,                   # "high" | "normal" | "low"
    "metadata": dict                  # 可选：额外元数据
}
```

**resume_strategy 说明**:
- `"auto"`: 插入任务完成后，自动恢复主任务
- `"ask"`: 插入任务完成后，询问用户是否恢复主任务

**示例**:
```python
DecisionOutput(
    action=DecisionAction.INSERT_TASK,
    reason="user_insert_task",
    params={
        "main_task_id": "nav_to_hospital_1",
        "insert_task_spec": {
            "type": "go_to_toilet",
            "target": {"poi_type": "toilet"},
            "priority": "high"
        },
        "resume_strategy": "auto"
    }
)
```

---

### 1.3 REPLACE_TASK

**语义**: 放弃当前主任务，换一个新任务（如"原来去医院，改成回家"）。

**DecisionOutput 格式**:

```python
DecisionOutput(
    action=DecisionAction.REPLACE_TASK,
    reason="user_change_dest" | "task_obsolete",
    params={
        "old_task_id": str,           # 旧任务ID（必需）
        "new_task_spec": dict         # 新任务完整定义（必需）
    }
)
```

**new_task_spec 格式**:
```python
{
    "type": str,                      # 任务类型，如 "navigation"
    "target": dict,                   # 目标信息，如 {"poi": "home"}
    "source": str,                    # 来源，如 "user_request"
    "metadata": dict                  # 可选：额外元数据
}
```

**特殊说明**:
- 如果 `new_task_spec` 为 `None` 或空，表示取消当前任务，不启动新任务

**示例**:
```python
DecisionOutput(
    action=DecisionAction.REPLACE_TASK,
    reason="user_change_dest",
    params={
        "old_task_id": "nav_to_hospital_1",
        "new_task_spec": {
            "type": "navigation",
            "target": {"poi": "home"},
            "source": "user_request"
        }
    }
)
```

---

### 1.4 ASK_USER

**语义**: 进入问询系统，让语音模块来问一句话，等用户反应。

**DecisionOutput 格式**:

```python
DecisionOutput(
    action=DecisionAction.ASK_USER,
    reason="node_requires_confirmation" | "task_finished_ask_new" | "ambiguous_intent",
    params={
        "question_type": str,         # 问题类型（必需）
        "related_task_id": Optional[str],  # 相关任务ID（可选）
        "context": dict               # 上下文信息（必需）
    }
)
```

**question_type 可选值**:
- `"next_step"`: 询问下一步操作
- `"new_task"`: 询问新任务
- `"confirm_change"`: 确认变更
- `"enter_hospital_flow"`: 进入医院流程
- `"confirm_completion"`: 确认完成

**约定**:
- 问询系统根据 `question_type` 在 `inquiry_templates.json` 中选模板
- 用户回答被解析为结构化 intent 后，会重新作为 `EventType.USER_INTENT` 返回 DecisionCore

**示例**:
```python
DecisionOutput(
    action=DecisionAction.ASK_USER,
    reason="node_requires_confirmation",
    params={
        "question_type": "enter_hospital_flow",
        "related_task_id": "nav_to_hospital_1",
        "context": {
            "location": "hospital_gate",
            "node_id": "to_hospital_gate"
        }
    }
)
```

---

### 1.5 TRIGGER_PLANB

**语义**: 系统进入"PlanB 待命状态"，停止当前正常流程。

**DecisionOutput 格式**:

```python
DecisionOutput(
    action=DecisionAction.TRIGGER_PLANB,
    reason="planB_condition_matched",
    params={
        "context_snapshot": dict      # 触发前的关键信息（必需）
    }
)
```

**context_snapshot 内容**:
- 当前任务状态
- 模型状态
- 场景信息
- 用户位置

**约定**:
- 后续 PlanB 真正做什么，不在 1.4.3 范围内
- 1.4.3 只负责触发，不执行 PlanB 逻辑

**示例**:
```python
DecisionOutput(
    action=DecisionAction.TRIGGER_PLANB,
    reason="planB_condition_matched",
    params={
        "context_snapshot": {
            "task_id": "nav_to_hospital_1",
            "model_status": {
                "vision_main": "down",
                "vision_fallback": "down"
            },
            "location": "hospital_gate"
        }
    }
)
```

---

### 1.6 NO_OP

**语义**: 当前事件不需要动作，只记录日志。

**DecisionOutput 格式**:

```python
DecisionOutput(
    action=DecisionAction.NO_OP,
    reason="no_rule_matched" | "unknown_intent" | "task_complete",
    params={}                         # 空字典
)
```

**使用场景**:
- 没有匹配的决策规则
- 未知的用户意图
- 任务已完成，无需进一步操作

**示例**:
```python
DecisionOutput(
    action=DecisionAction.NO_OP,
    reason="no_rule_matched",
    params={}
)
```

---

## 2. DecisionInput 硬契约约定

### 2.1 必需字段

所有 `DecisionInput` 必须包含以下字段：

```python
DecisionInput(
    event_type: EventType,            # 事件类型（必需）
    event_payload: dict,              # 事件负载（必需）
    scene_context: dict,              # 场景上下文（必需）
    task_context: dict,               # 任务上下文（必需）
    user_context: dict,               # 用户上下文（必需）
    model_context: dict               # 模型上下文（必需）
)
```

### 2.2 各字段详细规范

#### event_payload

根据 `event_type` 不同，`event_payload` 的格式不同：

**TASK_NODE_COMPLETE**:
```python
{
    "node_id": str                    # 完成的节点ID
}
```

**USER_INTENT**:
```python
{
    "parsed_intent": {
        "type": str,                  # 意图类型
        "task_spec": Optional[dict],  # 任务规格（如果有）
        "department": Optional[str],   # 部门（医院场景）
        # ... 其他字段
    }
}
```

**MODEL_STATUS**:
```python
{
    "source": str,                    # 来源，如 "health_monitor"
    "model_name": Optional[str],      # 模型名称（如果有）
    "status": str                     # "ok" | "down"
}
```

#### scene_context

```python
{
    "location": str,                  # 位置信息
    "objects": Optional[list],        # 检测到的物体
    "texts": Optional[list],          # 检测到的文字
    # ... 其他场景信息
}
```

#### task_context

```python
{
    "task_id": str,                   # 任务ID
    "active_node": Optional[dict],    # 当前活动节点
    "has_next_node": bool,            # 是否有下一个节点
    "task_type": str,                 # 任务类型
    # ... 其他任务信息
}
```

#### user_context

```python
{
    "user_id": Optional[str],         # 用户ID（如果有）
    "preferences": Optional[dict],     # 用户偏好
    # ... 其他用户信息
}
```

#### model_context

```python
{
    "vision_main": str,               # "ok" | "down"
    "vision_fallback": str,           # "ok" | "down"
    "semantic_basic": str,             # "ok" | "down"
    # ... 其他模型状态
}
```

---

## 3. 模块间调用约定

### 3.1 DecisionCore → TaskChainManager

当 `action` 为 `CONTINUE_TASK`、`INSERT_TASK`、`REPLACE_TASK` 时：

```python
# DecisionCore 输出
decision_output = DecisionOutput(...)

# TaskChainManager 接收并处理
task_chain_manager.handle_decision(decision_output)
```

### 3.2 DecisionCore → InquiryManager

当 `action` 为 `ASK_USER` 时：

```python
# DecisionCore 输出
decision_output = DecisionOutput(
    action=DecisionAction.ASK_USER,
    params={
        "question_type": "enter_hospital_flow",
        "context": {...}
    }
)

# InquiryManager 接收并生成问询
inquiry = inquiry_manager.ask(
    question_type=decision_output.params["question_type"],
    context=decision_output.params["context"]
)
```

### 3.3 InquiryManager → DecisionCore

用户回答后，解析为 `USER_INTENT` 事件：

```python
# InquiryManager 解析用户回答
parsed_intent = inquiry_manager.parse_response(user_text)

# 生成 USER_INTENT 事件
event = {
    "event_type": EventType.USER_INTENT,
    "event_payload": {
        "parsed_intent": parsed_intent
    },
    # ... 其他上下文
}

# 重新输入 DecisionCore
decision_input = DecisionInput(...)
decision_output = decision_core.handle_event(decision_input)
```

---

## 4. 错误处理约定

### 4.1 字段缺失

如果 `DecisionInput` 中缺少必需字段：

- 返回 `NO_OP`，reason 为 `"missing_required_field"`
- 记录错误日志

### 4.2 未知 event_type

如果 `event_type` 不在已知枚举中：

- 返回 `NO_OP`，reason 为 `"unknown_event_type"`
- 记录警告日志

### 4.3 参数格式错误

如果 `params` 格式不符合约定：

- 返回 `NO_OP`，reason 为 `"invalid_params_format"`
- 记录错误日志

---

## 5. 日志约定

### 5.1 决策日志格式

每次决策必须记录：

```python
{
    "timestamp": str,
    "event_type": str,
    "action": str,
    "reason": str,
    "task_id": Optional[str],
    "node_id": Optional[str],
    "context": dict
}
```

### 5.2 PlanB 触发日志

PlanB 触发必须单独记录：

```python
{
    "timestamp": str,
    "event": "planb_triggered",
    "context_snapshot": dict,
    "trigger_reason": str
}
```

---

## 6. 版本兼容性

### 6.1 向后兼容

- 新增 `params` 字段时，必须设为可选
- 新增 `DecisionAction` 时，旧代码应能处理（返回 `NO_OP`）

### 6.2 向前兼容

- 旧版本代码应能处理新增的 `DecisionAction`
- 未知的 `action` 应被安全忽略

---

**文档状态**: ✅ 已完成  
**版本**: v1.4.3  
**最后更新**: 2025-12-05













