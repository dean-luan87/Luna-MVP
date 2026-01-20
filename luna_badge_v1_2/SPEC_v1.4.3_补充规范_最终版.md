# Luna Badge v1.4.3 - 补充规范（最终版，可直接给 Cursor）

**版本**: v1.4.3  
**创建日期**: 2025-12-05  
**状态**: 📋 补充规范（必须遵循）  
**标准级别**: 最高工程标准

---

## 📋 概述

以下内容为必须补齐的 1.4.3 系统规范，所有模块必须遵循本规范实施。

**目标**:
- 不推翻 A/B 的既有结构
- 仅补齐"契约、接口、降级策略、日志规范"等必须的工程规则
- 保证 Cursor 能无歧义落地
- 架构可持续扩展到 1.4.4 / 二期情感引擎

---

## 1. 统一意图 Schema（ParsedIntent）

### 1.1 标准结构

所有用户意图（来自 ASR、问询系统、语义解析等）必须输出下列规范结构：

```python
ParsedIntent = {
    "intent_name": str,        # 标准化意图名
    "slots": dict,             # 结构化参数
    "source": str,             # 来源: "asr" / "inquiry" / "system"
    "need_confirm": bool,      # 是否需要二次确认
    "raw": str                 # 用户原始表达
}
```

### 1.2 统一意图命名

| 用户表达 | intent_name | 示例 slots |
|---------|------------|-----------|
| "先去厕所" | INSERT_TASK | {"task_type": "toilet"} |
| "改去医院" | CHANGE_DESTINATION | {"destination": "hospital"} |
| "是的" | CONFIRM | {} |
| "不用了" | REJECT | {} |
| "继续主任务" | RESUME_MAIN_TASK | {} |
| "停掉导航" | CANCEL_TASK | {} |
| "你看着办" | AMBIGUOUS | {} |
| "我也不知道" | UNKNOWN | {} |

### 1.3 实现要求

**InquiryParser 必须输出此结构**:
```python
def parse(self, text: str, tpl: dict) -> Dict[str, Any]:
    # ... 解析逻辑 ...
    return {
        "intent_name": "CONFIRM",  # 或 "REJECT", "INSERT_TASK", 等
        "slots": {"task_type": "toilet"},  # 如果有
        "source": "inquiry",
        "need_confirm": False,
        "raw": text
    }
```

**ASR 解析器必须输出此结构**:
```python
def parse_asr_result(self, asr_text: str) -> Dict[str, Any]:
    # ... ASR 解析逻辑 ...
    return {
        "intent_name": "INSERT_TASK",
        "slots": {"task_type": "toilet"},
        "source": "asr",
        "need_confirm": True,
        "raw": asr_text
    }
```

**DecisionCore 对意图的判断只能基于此 Schema**:
- 不允许读取任意自定义字段
- 只能读取 `intent_name`, `slots`, `need_confirm`
- 所有判断逻辑基于标准字段

---

## 2. TaskChainManager 增加统一执行入口：apply_decision()

### 2.1 新增方法

```python
def apply_decision(self, decision_output: DecisionOutput) -> Dict[str, Any]:
    """
    统一执行决策输出
    
    Args:
        decision_output: 决策输出对象
        
    Returns:
        dict: 执行结果
    """
    if decision_output.action == DecisionAction.CONTINUE_TASK:
        return self._continue_task(decision_output.params)
    
    elif decision_output.action == DecisionAction.INSERT_TASK:
        return self.insert_task(
            task_spec=decision_output.params["insert_task_spec"],
            resume_strategy=decision_output.params.get("resume_strategy", "auto")
        )
    
    elif decision_output.action == DecisionAction.REPLACE_TASK:
        return self._replace_task(decision_output.params)
    
    elif decision_output.action == DecisionAction.NO_OP:
        return {"status": "no_op"}
    
    # ASK_USER 与 TRIGGER_PLANB 不在此处理，由上层负责
    else:
        return {"status": "not_handled", "action": decision_output.action.value}
```

### 2.2 辅助方法

```python
def _continue_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
    """继续任务"""
    task_id = params.get("task_id")
    node_id = params.get("node_id")
    
    if node_id:
        # 移动到指定节点
        return self.move_to_node(task_id, node_id)
    else:
        # 自动移动到下一个节点
        return self.move_to_next()
    
def _replace_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
    """替换任务"""
    old_task_id = params.get("old_task_id")
    new_task_spec = params.get("new_task_spec")
    
    if new_task_spec is None:
        # 取消任务
        return self.cancel_task(old_task_id)
    else:
        # 替换为新任务
        return self.replace_task(old_task_id, new_task_spec)
```

### 2.3 禁止直接修改内部属性

**上层模块不允许直接操作**:
- `active_task`
- `active_node`
- `sub_task_stack`
- `main_task`
- `main_task_state`

**只能通过以下方法操作**:
- `apply_decision(decision_output)` - 统一执行入口
- `insert_task(task_spec, resume_strategy)` - 插入任务
- `complete_active_task()` - 完成当前任务
- `create_task(task_spec)` - 创建任务
- `start_task(task_id)` - 启动任务
- `pause_task(task_id)` - 暂停任务
- `cancel_task(task_id)` - 取消任务

---

## 3. 统一任务结果结构（TaskResult）

### 3.1 标准结构

TaskChain 汇报任务结果时必须使用以下格式：

```python
TaskResult = {
    "status": str,       # "ok" | "failed" | "cancelled"
    "reason": str,       # 非 ok 必填
    "task_id": str,
    "task_type": str
}
```

### 3.2 状态说明

- **"ok"**: 任务正常完成
- **"failed"**: 任务执行失败（如导航失败、无法到达）
- **"cancelled"**: 用户主动中止任务

### 3.3 决策层行为规范

#### failed → 必须返回 ASK_USER

```python
# TaskChain 返回
task_result = {
    "status": "failed",
    "reason": "navigation_failed",
    "task_id": "go_to_toilet_1",
    "task_type": "go_to_toilet"
}

# DecisionCore 处理
DecisionOutput(
    action=DecisionAction.ASK_USER,
    reason="subtask_failed",
    params={
        "question_type": "subtask_failed",
        "failed_task": task_result,
        "main_task_context": main_task_state
    }
)
```

#### cancelled（用户主动中止）→ 不自动恢复主任务

```python
# TaskChain 返回
task_result = {
    "status": "cancelled",
    "reason": "user_cancelled",
    "task_id": "go_to_toilet_1",
    "task_type": "go_to_toilet"
}

# DecisionCore 处理
# 不自动恢复主任务，由 USER_INTENT 决定下一步
DecisionOutput(
    action=DecisionAction.NO_OP,
    reason="subtask_cancelled_by_user",
    params={}
)
```

#### ok → 继续任务链

```python
# TaskChain 返回
task_result = {
    "status": "ok",
    "task_id": "go_to_toilet_1",
    "task_type": "go_to_toilet"
}

# DecisionCore 处理
# 根据 resume_strategy 决定是否恢复主任务
if resume_strategy == "auto":
    DecisionOutput(
        action=DecisionAction.CONTINUE_TASK,
        reason="subtask_complete_resume_main",
        params={"task_id": main_task_id}
    )
```

---

## 4. 问询系统的降级策略（必做）

### 4.1 连续 UNKNOWN（无法理解用户回答）

**规则**: 当问询连续两次解析为 UNKNOWN 时

**系统行为**:
```python
# 第一次 UNKNOWN
parsed = {"intent_name": "UNKNOWN", ...}
# 系统再问一次（fallback）

# 第二次 UNKNOWN
parsed = {"intent_name": "UNKNOWN", ...}
# 系统播报：
narration = "我先保持当前状态，如果需要变更任务，可以再告诉我。"

# DecisionCore 返回：
DecisionOutput(
    action=DecisionAction.NO_OP,
    reason="continuous_unknown_response",
    params={},
    narration=narration
)
```

**实现要求**:
- InquiryManager 需要记录连续 UNKNOWN 次数
- 达到 2 次时触发降级策略
- 重置计数器

### 4.2 用户长时间不回答（默认 30 秒）

**ASR/状态机需抛出事件**:
```python
EventType.USER_INACTIVE
event_payload = {
    "timeout_seconds": 30,
    "last_question_type": "enter_hospital_flow"
}
```

**DecisionCore 的处理**:
```python
DecisionOutput(
    action=DecisionAction.NO_OP,
    reason="user_inactive_timeout",
    params={}
)
```

**要求**:
- 不改变当前任务
- 记录日志
- 系统继续运行（不阻塞）

### 4.3 用户回答模糊（例如"你看着办"）

**解析为**:
```python
ParsedIntent = {
    "intent_name": "AMBIGUOUS",
    "slots": {},
    "source": "inquiry",
    "need_confirm": False,
    "raw": "你看着办"
}
```

**决策层响应**:
```python
DecisionOutput(
    action=DecisionAction.NO_OP,
    reason="ambiguous_response",
    params={},
    narration="那我继续当前任务，如果需要更改，请再告诉我。"
)
```

**InquiryParser 需要识别模糊表达**:
```python
ambiguous_keywords = ["你看着办", "随便", "都可以", "你决定"]
if any(kw in text for kw in ambiguous_keywords):
    return {
        "intent_name": "AMBIGUOUS",
        "slots": {},
        "source": "inquiry",
        "need_confirm": False,
        "raw": text
    }
```

---

## 5. 决策层日志结构（必须统一）

### 5.1 标准日志格式

每条决策日志必须包含以下字段：

```python
{
    "event_type": str,            # USER_INTENT / TASK_NODE_COMPLETE / INQUIRY_RESPONSE / SYSTEM_ALERT
    "intent_name": str | None,    # 若来源是意图
    "action": str,                # DecisionAction 的枚举值
    "reason": str,                # 推理说明
    "task_id": str | None,
    "task_type": str | None,
    "need_confirm": bool,
    "timestamp": float,
    "context": dict               # 可选：关键上下文信息
}
```

### 5.2 日志发布

**发布至**:
- 本地日志模块（decision_layer.logger）
- 全局日志管理器（已集成）

**实现示例**:
```python
def log_decision(ctx: Dict[str, Any], result: DecisionOutput) -> None:
    """记录决策日志"""
    log_entry = {
        "event_type": ctx["event_type"].value if hasattr(ctx["event_type"], "value") else str(ctx["event_type"]),
        "intent_name": ctx.get("event", {}).get("parsed_intent", {}).get("intent_name"),
        "action": result.action.value,
        "reason": result.reason,
        "task_id": ctx.get("task", {}).get("task_id"),
        "task_type": ctx.get("task", {}).get("task_type"),
        "need_confirm": ctx.get("event", {}).get("parsed_intent", {}).get("need_confirm", False),
        "timestamp": time.time(),
        "context": {
            "scene_location": ctx.get("scene", {}).get("location"),
            "model_status": ctx.get("models", {})
        }
    }
    
    logger.info("[Decision] %s", json.dumps(log_entry, ensure_ascii=False))
```

---

## 6. 中断一致性规则（必须保证）

### 6.1 Rule 1: 主任务永不丢失

**规则**: 除非明确触发 REPLACE_TASK，主任务永不丢失

**实现要求**:
- `main_task` 对象始终存在
- 只能暂停，不能删除
- 状态通过 `main_task_state` 缓存

**验证**:
```python
# 插入任务后
assert taskchain.main_task is not None
assert taskchain.main_task_state is not None

# 替换任务时
if decision_output.action == DecisionAction.REPLACE_TASK:
    # 允许替换主任务
    taskchain.main_task = new_task_spec
```

### 6.2 Rule 2: 插入任务完成后自动返回主任务

**规则**: 若 `resume_strategy = "auto"`，插入任务完成后自动返回主任务

**实现要求**:
- `complete_active_task()` 检查 `resume_strategy`
- 自动恢复时调用 `_resume_main_task()`
- 恢复后的节点与插入前一致

**验证**:
```python
# 插入前
original_node = taskchain.active_node.copy()

# 插入任务
taskchain.insert_task(sub_task, resume_strategy="auto")

# 完成任务
result = taskchain.complete_active_task()

# 验证恢复
assert result["status"] == "resumed"
assert taskchain.active_node["id"] == original_node["id"]
```

### 6.3 Rule 3: 问询必须阻塞决策层，但不阻塞视觉/感知模块

**规则**: 问询期间决策层暂停，但视觉/感知模块继续运行

**实现要求**:
- 问询状态通过标志位管理
- 决策层检查问询状态，问询中返回 NO_OP
- 视觉/感知模块不受影响

**实现示例**:
```python
class DecisionCore:
    def __init__(self):
        self._inquiry_pending = False
        self._pending_question_type = None
    
    def handle_event(self, decision_input: DecisionInput) -> DecisionOutput:
        # 如果正在问询中，暂停决策
        if self._inquiry_pending:
            return DecisionOutput(
                action=DecisionAction.NO_OP,
                reason="inquiry_pending",
                params={}
            )
        
        # ... 正常决策逻辑 ...
    
    def start_inquiry(self, question_type: str):
        """开始问询"""
        self._inquiry_pending = True
        self._pending_question_type = question_type
    
    def end_inquiry(self):
        """结束问询"""
        self._inquiry_pending = False
        self._pending_question_type = None
```

### 6.4 Rule 4: 子任务失败不会直接崩溃任务链

**规则**: 子任务失败进入问询流，不直接崩溃

**实现要求**:
- 子任务失败返回 `TaskResult(status="failed")`
- DecisionCore 处理失败，输出 `ASK_USER`
- 询问用户是否继续主任务

**实现示例**:
```python
# 子任务失败
task_result = {
    "status": "failed",
    "reason": "navigation_failed",
    "task_id": "go_to_toilet_1",
    "task_type": "go_to_toilet"
}

# DecisionCore 处理
DecisionOutput(
    action=DecisionAction.ASK_USER,
    reason="subtask_failed",
    params={
        "question_type": "subtask_failed",
        "failed_task": task_result,
        "main_task_context": main_task_state
    }
)
```

---

## 7. 与 1.4.3 决策层衔接的固定输出格式

### 7.1 DecisionOutput 完整结构

DecisionCore 输出结构（供 TaskChain 和 Inquiry 使用）必须如下：

```python
@dataclass
class DecisionOutput:
    action: DecisionAction      # CONTINUE_TASK / INSERT_TASK / REPLACE_TASK / ASK_USER / TRIGGER_PLANB / NO_OP
    reason: str                # 推理说明
    params: Dict[str, Any]     # 任务数据、子任务 spec、planB trigger 信息
    narration: str = ""        # 供语音播报的自然语言（新增）
```

### 7.2 narration 字段说明

**用途**: 供语音播报的自然语言描述

**示例**:
```python
DecisionOutput(
    action=DecisionAction.ASK_USER,
    reason="node_requires_confirmation",
    params={...},
    narration="我们已经到医院门口了，需要我带你进去吗？"
)

DecisionOutput(
    action=DecisionAction.NO_OP,
    reason="continuous_unknown_response",
    params={},
    narration="我先保持当前状态，如果需要变更任务，可以再告诉我。"
)
```

**实现要求**:
- 所有 `ASK_USER` 必须有 `narration`
- 所有 `NO_OP`（带说明的）应该有 `narration`
- 其他 action 可选

---

## 8. 补充规范总结

### 8.1 核心改进

1. **统一意图 Schema** - 所有意图输出统一格式
2. **统一执行入口** - TaskChainManager.apply_decision()
3. **统一任务结果** - TaskResult 标准结构
4. **降级策略** - 连续 UNKNOWN、超时、模糊回答
5. **统一日志** - 决策日志标准格式
6. **中断一致性** - 4 条核心规则
7. **固定输出格式** - DecisionOutput 包含 narration

### 8.2 架构优势

经过这些补齐：

1. **A（TaskChain）** 不再是松散结构，具备完整契约体系
2. **B（问询系统）** 具备工业级降级机制，不会卡死或重复问询
3. **DecisionCore** 成为严格的"纯策略层"，未来二期情感引擎可直接接入
4. **PlanB** 触发点已固定，未来可直接填充真实的兜底逻辑
5. **整个 1.4.3** 的架构达到了"可上线可长期维护"的级别

---

## 9. 实施检查清单

### 9.1 代码实施

- [ ] InquiryParser 输出 ParsedIntent 标准结构
- [ ] TaskChainManager 实现 apply_decision() 方法
- [ ] TaskChain 返回 TaskResult 标准结构
- [ ] InquiryManager 实现降级策略（连续 UNKNOWN、超时、模糊回答）
- [ ] DecisionCore 日志使用标准格式
- [ ] DecisionOutput 包含 narration 字段
- [ ] 所有模块遵循中断一致性规则

### 9.2 测试验证

- [ ] 测试 ParsedIntent 结构
- [ ] 测试 apply_decision() 方法
- [ ] 测试 TaskResult 结构
- [ ] 测试降级策略
- [ ] 测试日志格式
- [ ] 测试中断一致性规则

---

**文档状态**: ✅ 已完成  
**版本**: v1.4.3  
**标准级别**: 最高工程标准  
**可直接给 Cursor 执行**: ✅ 是  
**最后更新**: 2025-12-05













