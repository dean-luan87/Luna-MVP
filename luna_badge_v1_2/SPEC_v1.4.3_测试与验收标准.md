# Luna Badge v1.4.3 - 测试与验收标准

**版本**: v1.4.3  
**创建日期**: 2025-12-05  
**状态**: 📋 规范文档  
**标准级别**: 最高标准

---

## 📋 概述

本文档定义了 v1.4.3 的测试与验收标准，按照最高工程标准制定，确保系统质量、稳定性和可扩展性。

---

## 1. 功能覆盖测试

### 1.1 测试用例清单

#### 用例 1：任务节点完成 → 自动继续下一节点（不问）

**输入**:
```python
DecisionInput(
    event_type=EventType.TASK_NODE_COMPLETE,
    event_payload={"node_id": "street_corner"},
    task_context={
        "task_id": "nav_to_hospital_1",
        "active_node": {
            "id": "street_corner",
            "requires_user_confirmation": False
        },
        "has_next_node": True
    },
    ...
)
```

**期望输出**:
```python
DecisionOutput(
    action=DecisionAction.CONTINUE_TASK,
    reason="next_node_available",
    params={
        "task_id": "nav_to_hospital_1",
        "node_id": "hospital_gate"  # 可选
    }
)
```

**验证点**:
- [ ] DecisionOutput.action == CONTINUE_TASK
- [ ] TaskChainManager 成功移动到下一个节点
- [ ] 没有触发 ASK_USER

---

#### 用例 2：任务节点完成 + requires_user_confirmation=True → 触发 ASK_USER

**输入**:
```python
DecisionInput(
    event_type=EventType.TASK_NODE_COMPLETE,
    event_payload={"node_id": "to_hospital_gate"},
    task_context={
        "task_id": "nav_to_hospital_1",
        "active_node": {
            "id": "to_hospital_gate",
            "requires_user_confirmation": True
        }
    },
    ...
)
```

**期望输出**:
```python
DecisionOutput(
    action=DecisionAction.ASK_USER,
    reason="node_requires_confirmation",
    params={
        "question_type": "enter_hospital_flow",
        "related_task_id": "nav_to_hospital_1",
        "context": {...}
    }
)
```

**验证点**:
- [ ] DecisionOutput.action == ASK_USER
- [ ] InquiryManager 成功生成问询
- [ ] 问询内容符合模板

---

#### 用例 3：用户主动说"停掉导航" → REPLACE_TASK (new_task_spec=None)

**输入**:
```python
DecisionInput(
    event_type=EventType.USER_INTENT,
    event_payload={
        "parsed_intent": {
            "type": "CANCEL_TASK",
            "task_id": "nav_to_hospital_1"
        }
    },
    task_context={"task_id": "nav_to_hospital_1", ...},
    ...
)
```

**期望输出**:
```python
DecisionOutput(
    action=DecisionAction.REPLACE_TASK,
    reason="user_cancel_task",
    params={
        "old_task_id": "nav_to_hospital_1",
        "new_task_spec": None
    }
)
```

**验证点**:
- [ ] DecisionOutput.action == REPLACE_TASK
- [ ] new_task_spec == None
- [ ] TaskChainManager 成功取消任务
- [ ] 没有启动新任务

---

#### 用例 4：用户说"先去厕所" → INSERT_TASK + 子任务完成后恢复主任务

**输入**:
```python
DecisionInput(
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
    task_context={
        "task_id": "nav_to_hospital_1",
        "active_node": {"id": "on_the_way"}
    },
    ...
)
```

**期望输出**:
```python
DecisionOutput(
    action=DecisionAction.INSERT_TASK,
    reason="user_insert_task",
    params={
        "main_task_id": "nav_to_hospital_1",
        "insert_task_spec": {
            "type": "go_to_toilet",
            "target": {"poi_type": "toilet"}
        },
        "resume_strategy": "auto"
    }
)
```

**验证点**:
- [ ] DecisionOutput.action == INSERT_TASK
- [ ] TaskChainManager 成功暂停主任务
- [ ] TaskChainManager 成功插入子任务
- [ ] 子任务完成后，主任务自动恢复

---

#### 用例 5：用户说"改去别的地方" → REPLACE_TASK，新任务生效

**输入**:
```python
DecisionInput(
    event_type=EventType.USER_INTENT,
    event_payload={
        "parsed_intent": {
            "type": "REPLACE_TASK",
            "task_spec": {
                "type": "navigation",
                "target": {"poi": "home"}
            }
        }
    },
    task_context={"task_id": "nav_to_hospital_1", ...},
    ...
)
```

**期望输出**:
```python
DecisionOutput(
    action=DecisionAction.REPLACE_TASK,
    reason="user_change_dest",
    params={
        "old_task_id": "nav_to_hospital_1",
        "new_task_spec": {
            "type": "navigation",
            "target": {"poi": "home"}
        }
    }
)
```

**验证点**:
- [ ] DecisionOutput.action == REPLACE_TASK
- [ ] TaskChainManager 成功取消旧任务
- [ ] TaskChainManager 成功创建新任务
- [ ] 新任务成功启动

---

#### 用例 6：模型状态正常 → 不触发 PlanB

**输入**:
```python
DecisionInput(
    event_type=EventType.MODEL_STATUS,
    event_payload={"source": "health_monitor"},
    model_context={
        "vision_main": "ok",
        "vision_fallback": "ok",
        "semantic_basic": "ok"
    },
    ...
)
```

**期望输出**:
```python
DecisionOutput(
    action=DecisionAction.NO_OP,
    reason="model_status_normal",
    params={}
)
```

**验证点**:
- [ ] DecisionOutput.action != TRIGGER_PLANB
- [ ] PlanBTrigger.should_trigger() == False

---

#### 用例 7：主模型+备份均失败 → 触发 PlanB

**输入**:
```python
DecisionInput(
    event_type=EventType.MODEL_STATUS,
    event_payload={"source": "health_monitor"},
    model_context={
        "vision_main": "down",
        "vision_fallback": "down",
        "semantic_basic": "ok"
    },
    task_context={"task_id": "nav_to_hospital_1", ...},
    ...
)
```

**期望输出**:
```python
DecisionOutput(
    action=DecisionAction.TRIGGER_PLANB,
    reason="planB_condition_matched",
    params={
        "context_snapshot": {...}
    }
)
```

**验证点**:
- [ ] DecisionOutput.action == TRIGGER_PLANB
- [ ] PlanBTrigger.should_trigger() == True
- [ ] context_snapshot 包含关键信息
- [ ] 系统进入 PlanB 模式

---

### 1.2 测试执行要求

每个测试用例必须包含：

1. **输入数据**：完整的 `DecisionInput` 对象
2. **期望输出**：完整的 `DecisionOutput` 对象
3. **验证点**：具体的断言检查项
4. **集成验证**：验证 TaskChain/Inquiry 等模块的行为

---

## 2. 稳定性与可观测性

### 2.1 日志要求

#### 2.1.1 决策日志格式

每次决策必须记录结构化日志：

```python
{
    "timestamp": "2025-12-05T10:00:00Z",
    "level": "INFO",
    "module": "decision_layer",
    "event_type": "TASK_NODE_COMPLETE",
    "action": "ASK_USER",
    "reason": "node_requires_confirmation",
    "task_id": "nav_to_hospital_1",
    "node_id": "to_hospital_gate",
    "context": {
        "location": "hospital_gate",
        "model_status": {...}
    }
}
```

**验证点**:
- [ ] 每次决策都有日志记录
- [ ] 日志包含所有必需字段
- [ ] 日志格式统一
- [ ] 日志可被解析和查询

#### 2.1.2 PlanB 触发日志

PlanB 触发必须单独记录：

```python
{
    "timestamp": "2025-12-05T10:00:00Z",
    "level": "WARNING",
    "module": "decision_layer",
    "event": "planb_triggered",
    "context_snapshot": {
        "task_id": "nav_to_hospital_1",
        "model_status": {
            "vision_main": "down",
            "vision_fallback": "down"
        },
        "location": "street_corner"
    },
    "trigger_reason": "all_vision_models_down"
}
```

**验证点**:
- [ ] PlanB 触发有独立日志
- [ ] 日志级别为 WARNING
- [ ] 包含完整的 context_snapshot

---

### 2.2 错误处理要求

#### 2.2.1 字段缺失处理

如果 `DecisionInput` 缺少必需字段：

```python
# 输入缺少 task_context
decision_input = DecisionInput(
    event_type=EventType.TASK_NODE_COMPLETE,
    event_payload={},
    scene_context={},
    task_context={},  # 缺少 task_id
    user_context={},
    model_context={}
)

# 期望输出
DecisionOutput(
    action=DecisionAction.NO_OP,
    reason="missing_required_field",
    params={"missing_field": "task_context.task_id"}
)
```

**验证点**:
- [ ] 不抛出异常
- [ ] 返回 NO_OP
- [ ] 记录错误日志

#### 2.2.2 未知 event_type 处理

```python
# 输入未知 event_type（模拟）
decision_input = DecisionInput(
    event_type=EventType.UNKNOWN,  # 假设存在
    ...
)

# 期望输出
DecisionOutput(
    action=DecisionAction.NO_OP,
    reason="unknown_event_type",
    params={"event_type": "UNKNOWN"}
)
```

**验证点**:
- [ ] 不抛出异常
- [ ] 返回 NO_OP
- [ ] 记录警告日志

#### 2.2.3 参数格式错误处理

```python
# 输入 params 格式错误
decision_output = DecisionOutput(
    action=DecisionAction.INSERT_TASK,
    params={
        "main_task_id": "nav_to_hospital_1",
        # 缺少 insert_task_spec
    }
)

# TaskChainManager 处理时
# 期望：不崩溃，记录错误，返回失败状态
```

**验证点**:
- [ ] 模块不崩溃
- [ ] 记录错误日志
- [ ] 返回明确的失败状态

---

## 3. 可扩展性要求

### 3.1 模块解耦

#### 3.1.1 决策层不直接依赖模型类

**要求**:
- 决策层通过 `ModelScheduler` 提供的 `model_context` 获取模型状态
- 不直接导入或使用具体模型类

**验证点**:
- [ ] `decision_layer` 模块中没有 `from models.vision_main import ...`
- [ ] 所有模型状态通过 `model_context` 传递
- [ ] 可以替换模型实现而不影响决策层

#### 3.1.2 决策层不直接调用 TaskChainManager

**要求**:
- 决策层只输出 `DecisionOutput`
- 上层系统负责调用 TaskChainManager

**验证点**:
- [ ] `decision_layer` 模块中没有 `from task_chain import TaskChainManager`
- [ ] 决策层代码不包含 TaskChainManager 的调用
- [ ] 通过统一接口（上层调用）连接

#### 3.1.3 枚举集中管理

**要求**:
- 所有枚举（EventType/DecisionAction）集中在 `types.py`
- 不在各模块散落写字符串

**验证点**:
- [ ] 所有枚举定义在 `types.py`
- [ ] 其他模块通过 `from types import ...` 导入
- [ ] 没有硬编码的字符串常量

---

### 3.2 接口统一

#### 3.2.1 DecisionInput/DecisionOutput 统一格式

**要求**:
- 所有模块使用统一的 `DecisionInput`/`DecisionOutput` 格式
- 不创建自定义格式

**验证点**:
- [ ] 所有模块使用 `from decision_layer.types import DecisionInput, DecisionOutput`
- [ ] 没有自定义的输入/输出格式

---

## 4. 性能要求

### 4.1 决策响应时间

**要求**:
- 单次决策处理时间 < 10ms（不含模型推理）
- 决策日志写入不阻塞主流程

**验证点**:
- [ ] 性能测试：1000 次决策平均时间 < 10ms
- [ ] 日志写入使用异步或非阻塞方式

---

## 5. 测试覆盖率要求

### 5.1 代码覆盖率

**要求**:
- 单元测试覆盖率 ≥ 80%
- 关键路径（决策规则）覆盖率 = 100%

**验证点**:
- [ ] 使用覆盖率工具（如 coverage.py）验证
- [ ] 所有决策规则都有测试用例

---

## 6. 验收标准总结

### 6.1 功能验收

- [ ] 所有 7 个测试用例通过
- [ ] 每个用例都有完整的输入/输出验证
- [ ] 集成测试验证模块间协作

### 6.2 稳定性验收

- [ ] 所有决策都有结构化日志
- [ ] PlanB 触发有独立日志
- [ ] 所有异常情况都有错误处理
- [ ] 系统不因异常输入而崩溃

### 6.3 可扩展性验收

- [ ] 决策层不直接依赖模型类
- [ ] 决策层不直接调用 TaskChainManager
- [ ] 所有枚举集中在 types.py
- [ ] 接口统一，格式规范

### 6.4 性能验收

- [ ] 决策响应时间 < 10ms
- [ ] 日志写入不阻塞主流程

### 6.5 测试覆盖率验收

- [ ] 单元测试覆盖率 ≥ 80%
- [ ] 关键路径覆盖率 = 100%

---

## 7. 测试执行计划

### 7.1 单元测试

- **文件**: `tests/test_decision_layer.py`
- **覆盖**: DecisionCore, DecisionRules, PlanBTrigger
- **目标**: 覆盖率 ≥ 80%

### 7.2 集成测试

- **文件**: `tests/test_integration.py`
- **覆盖**: DecisionCore → TaskChainManager, DecisionCore → InquiryManager
- **目标**: 所有场景用例通过

### 7.3 端到端测试

- **文件**: `tests/test_e2e.py`
- **覆盖**: 完整事件流（场景 1-6）
- **目标**: 所有场景正常执行

---

## 8. 验收检查清单

### 8.1 代码质量

- [ ] 所有代码符合 PEP 8
- [ ] 所有函数有类型注解
- [ ] 所有类和方法有文档字符串
- [ ] 没有循环导入
- [ ] 没有未使用的代码

### 8.2 文档完整性

- [ ] API 文档完整
- [ ] 使用说明完整
- [ ] 测试文档完整
- [ ] 变更日志更新

### 8.3 部署准备

- [ ] 所有依赖已列出
- [ ] 配置文件模板已提供
- [ ] 部署脚本已准备
- [ ] 回滚方案已准备

---

**文档状态**: ✅ 已完成  
**版本**: v1.4.3  
**标准级别**: 最高标准  
**最后更新**: 2025-12-05


