# Luna Badge v1.4.3 - 事件流样例

**版本**: v1.4.3  
**创建日期**: 2025-12-05  
**状态**: 📋 规范文档

---

## 📋 概述

本文档提供了关键事件流的完整样例，特别是与导航相关的场景，用于验证 1.4.3 的实际可用性。

---

## 场景 1：到达医院大门，询问是否进入医院流程

### 1.1 事件输入

**TaskChain 报告节点完成**:

```python
decision_input = DecisionInput(
    event_type=EventType.TASK_NODE_COMPLETE,
    event_payload={
        "node_id": "to_hospital_gate"
    },
    scene_context={
        "location": "hospital_gate",
        "objects": [],
        "texts": ["医院入口"]
    },
    task_context={
        "task_id": "nav_to_hospital_1",
        "active_node": {
            "id": "to_hospital_gate",
            "name": "到达医院大门",
            "requires_user_confirmation": True
        },
        "has_next_node": True,
        "task_type": "navigation"
    },
    user_context={},
    model_context={
        "vision_main": "ok",
        "vision_fallback": "ok",
        "semantic_basic": "ok"
    }
)
```

### 1.2 决策处理流程

1. **ContextManager 合并上下文**:
```python
merged_ctx = {
    "event_type": EventType.TASK_NODE_COMPLETE,
    "event": {"node_id": "to_hospital_gate"},
    "scene": {"location": "hospital_gate", ...},
    "task": {
        "task_id": "nav_to_hospital_1",
        "active_node": {
            "id": "to_hospital_gate",
            "requires_user_confirmation": True
        },
        ...
    },
    "user": {},
    "models": {"vision_main": "ok", ...}
}
```

2. **DecisionRules 评估**:
   - 检测到 `requires_user_confirmation=True`
   - 返回 `ASK_USER` 决策

### 1.3 决策输出

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

### 1.4 Inquiry 系统处理

```python
# InquiryManager 生成问询
inquiry = inquiry_manager.ask(
    question_type="enter_hospital_flow",
    context={
        "location": "hospital_gate",
        "node_id": "to_hospital_gate"
    }
)

# 输出：
{
    "type": "inquiry",
    "question_type": "enter_hospital_flow",
    "question": "已到达医院门口，需要我带你进去吗？",
    "options": ["是", "否"],
    "context": {...}
}
```

### 1.5 用户回答处理

**用户说："要，帮我挂号"**

```python
# InquiryManager 解析
parsed_intent = inquiry_manager.parse_response("要，帮我挂号")

# 输出：
{
    "intent_type": "CONFIRM",
    "task_spec": {
        "type": "hospital_flow",
        "action": "register",
        "department": None
    }
}
```

### 1.6 重新决策

**生成新的 USER_INTENT 事件**:

```python
decision_input = DecisionInput(
    event_type=EventType.USER_INTENT,
    event_payload={
        "parsed_intent": {
            "intent_type": "CONFIRM",
            "task_spec": {
                "type": "hospital_flow",
                "action": "register"
            }
        }
    },
    scene_context={"location": "hospital_gate"},
    task_context={"task_id": "nav_to_hospital_1", ...},
    user_context={},
    model_context={...}
)
```

**DecisionCore 再次处理**:

```python
# 可能输出 INSERT_TASK 或 REPLACE_TASK
DecisionOutput(
    action=DecisionAction.INSERT_TASK,
    reason="user_insert_task",
    params={
        "main_task_id": "nav_to_hospital_1",
        "insert_task_spec": {
            "type": "hospital_flow",
            "action": "register",
            "target": {"poi_type": "hospital"}
        },
        "resume_strategy": "auto"
    }
)
```

---

## 场景 2：导航途中用户说"我先去厕所"

### 2.1 事件输入

**用户语音 → 解析为 USER_INTENT**:

```python
decision_input = DecisionInput(
    event_type=EventType.USER_INTENT,
    event_payload={
        "parsed_intent": {
            "type": "INSERT_TASK",
            "task_spec": {
                "type": "go_to_toilet",
                "target": {"poi_type": "toilet"}
            }
        }
    },
    scene_context={
        "location": "street_corner",
        "objects": [],
        "texts": []
    },
    task_context={
        "task_id": "nav_to_hospital_1",
        "active_node": {
            "id": "on_the_way",
            "name": "前往医院途中"
        },
        "task_type": "navigation"
    },
    user_context={},
    model_context={...}
)
```

### 2.2 决策处理

**DecisionRules._handle_user_intent** 检测到 `INSERT_TASK` 意图:

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

### 2.3 TaskChainManager 处理

**TaskChainManager 执行插入任务**:

```python
# 1. 暂停主任务
task_chain_manager.pause_task("nav_to_hospital_1")

# 2. 插入子任务
task_chain_manager.insert_task(
    main_task_id="nav_to_hospital_1",
    insert_task_spec={
        "type": "go_to_toilet",
        "target": {"poi_type": "toilet"},
        "priority": "high"
    }
)

# 3. 启动子任务
task_chain_manager.start_task("go_to_toilet_1")
```

### 2.4 子任务完成

**子任务完成后，自动恢复主任务**:

```python
# 子任务完成事件
decision_input = DecisionInput(
    event_type=EventType.TASK_NODE_COMPLETE,
    event_payload={"node_id": "toilet_reached"},
    task_context={
        "task_id": "go_to_toilet_1",
        "task_type": "go_to_toilet",
        "is_subtask": True,
        "main_task_id": "nav_to_hospital_1"
    },
    ...
)

# DecisionCore 处理
DecisionOutput(
    action=DecisionAction.CONTINUE_TASK,
    reason="subtask_complete_resume_main",
    params={
        "task_id": "nav_to_hospital_1",
        "resume_from": "on_the_way"
    }
)
```

---

## 场景 3：模型故障 → PlanB 触发

### 3.1 事件输入

**模型状态更新事件**:

```python
decision_input = DecisionInput(
    event_type=EventType.MODEL_STATUS,
    event_payload={
        "source": "health_monitor",
        "model_name": "vision_fallback",
        "status": "down"
    },
    scene_context={},
    task_context={
        "task_id": "nav_to_hospital_1",
        "active_node": {"id": "on_the_way"}
    },
    user_context={},
    model_context={
        "vision_main": "down",
        "vision_fallback": "down",
        "semantic_basic": "ok"
    }
)
```

### 3.2 PlanB 触发检查

**PlanBTrigger.should_trigger**:

```python
# 检查模型状态
models = ctx["models"]
if models.get("vision_main") == "down" and models.get("vision_fallback") == "down":
    return True  # 触发 PlanB
```

### 3.3 决策输出

```python
DecisionOutput(
    action=DecisionAction.TRIGGER_PLANB,
    reason="planB_condition_matched",
    params={
        "context_snapshot": {
            "task_id": "nav_to_hospital_1",
            "active_node": {"id": "on_the_way"},
            "model_status": {
                "vision_main": "down",
                "vision_fallback": "down",
                "semantic_basic": "ok"
            },
            "location": "street_corner"
        }
    }
)
```

### 3.4 上层系统处理

**系统进入 PlanB 模式**:

```python
# 1. 标记系统模式
system_state.system_mode = "planB"

# 2. 暂停任务链
task_chain_manager.pause_all_tasks()

# 3. 记录 PlanB 触发日志
logger.warning("[PlanB] Triggered: %s", context_snapshot)

# 4. 后续会接入三/四期 PlanB 真正逻辑
# （人工接管、远程监控等）
```

---

## 场景 4：用户说"停掉导航"

### 4.1 事件输入

```python
decision_input = DecisionInput(
    event_type=EventType.USER_INTENT,
    event_payload={
        "parsed_intent": {
            "type": "CANCEL_TASK",
            "task_id": "nav_to_hospital_1"
        }
    },
    scene_context={...},
    task_context={
        "task_id": "nav_to_hospital_1",
        "active_node": {"id": "on_the_way"}
    },
    user_context={},
    model_context={...}
)
```

### 4.2 决策输出

```python
DecisionOutput(
    action=DecisionAction.REPLACE_TASK,
    reason="user_cancel_task",
    params={
        "old_task_id": "nav_to_hospital_1",
        "new_task_spec": None  # None 表示取消任务，不启动新任务
    }
)
```

### 4.3 TaskChainManager 处理

```python
# 取消当前任务
task_chain_manager.cancel_task("nav_to_hospital_1")

# 清理任务状态
task_chain_manager.clear_active_task()
```

---

## 场景 5：用户说"改去别的地方"

### 5.1 事件输入

```python
decision_input = DecisionInput(
    event_type=EventType.USER_INTENT,
    event_payload={
        "parsed_intent": {
            "type": "REPLACE_TASK",
            "task_spec": {
                "type": "navigation",
                "target": {"poi": "home"},
                "source": "user_request"
            }
        }
    },
    scene_context={...},
    task_context={
        "task_id": "nav_to_hospital_1",
        "active_node": {"id": "on_the_way"}
    },
    user_context={},
    model_context={...}
)
```

### 5.2 决策输出

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

### 5.3 TaskChainManager 处理

```python
# 1. 取消旧任务
task_chain_manager.cancel_task("nav_to_hospital_1")

# 2. 创建新任务
new_task_id = task_chain_manager.create_task(
    task_spec={
        "type": "navigation",
        "target": {"poi": "home"},
        "source": "user_request"
    }
)

# 3. 启动新任务
task_chain_manager.start_task(new_task_id)
```

---

## 场景 6：任务节点完成，自动继续

### 6.1 事件输入

```python
decision_input = DecisionInput(
    event_type=EventType.TASK_NODE_COMPLETE,
    event_payload={"node_id": "street_corner"},
    scene_context={...},
    task_context={
        "task_id": "nav_to_hospital_1",
        "active_node": {
            "id": "street_corner",
            "requires_user_confirmation": False  # 不需要确认
        },
        "has_next_node": True,
        "next_node": {"id": "hospital_gate"}
    },
    user_context={},
    model_context={...}
)
```

### 6.2 决策输出

```python
DecisionOutput(
    action=DecisionAction.CONTINUE_TASK,
    reason="next_node_available",
    params={
        "task_id": "nav_to_hospital_1",
        "node_id": "hospital_gate"  # 可选，TaskChain 也可以自己决定
    }
)
```

### 6.3 TaskChainManager 处理

```python
# 自动移动到下一个节点
task_chain_manager.move_to_next("nav_to_hospital_1")
```

---

## 事件流总结

### 关键流程

1. **任务节点完成** → 检查是否需要确认 → ASK_USER 或 CONTINUE_TASK
2. **用户插入任务** → INSERT_TASK → 暂停主任务 → 执行子任务 → 恢复主任务
3. **用户取消任务** → REPLACE_TASK (new_task_spec=None) → 取消任务
4. **用户更换目标** → REPLACE_TASK → 取消旧任务 → 启动新任务
5. **模型故障** → 检查 PlanB 条件 → TRIGGER_PLANB → 进入 PlanB 模式

### 决策链

```
事件输入 → ContextManager 合并 → PlanB 检查 → DecisionRules 评估 → 决策输出
                                                                    ↓
                                                            各模块处理（TaskChain/Inquiry/PlanB）
```

---

**文档状态**: ✅ 已完成  
**版本**: v1.4.3  
**最后更新**: 2025-12-05


