# Luna Badge v1.4.3 - Cursor 开发指令（完整版）

**版本**: v1.4.3  
**创建日期**: 2025-12-05  
**状态**: 📋 可直接执行  
**用途**: 直接复制给 Cursor 执行

---

## BEGIN CURSOR BLUEPRINT

你现在要实现的是 Luna Badge v1.4.3 的"任务链 × 决策层 × 问询系统"能力。

**要求**: 严格工程化、模块解耦、全部通过测试用例，禁止随意改动契约。

整体分 8 个阶段执行，每个阶段都要确保代码可运行且通过对应测试。

---

## ========================================
## 阶段 0：目录与基础结构
## ========================================

请确保项目包含如下目录（若不存在则创建）：

```
/core
/taskchain
/inquiry
/decision
/logging
/tests
```

**不要在其它随机目录里散落核心逻辑。**

---

## ========================================
## 阶段 1：核心契约层（先做）
## ========================================

在 `/core` 目录下创建以下文件：

### 1) `/core/intent_schema.py`

定义 ParsedIntent 结构（可以用 dataclass 或普通 class，但字段名要一致）：

```python
- intent_name: str        # INSERT_TASK / CHANGE_DESTINATION / CONFIRM / REJECT / RESUME_MAIN_TASK / AMBIGUOUS / UNKNOWN ...
- slots: dict             # {"task_type": "toilet"} / {"destination": "hospital"} 等
- source: str             # "inquiry" / "asr" / "system"
- need_confirm: bool      # 是否需要二次确认
- raw: str                # 原始用户输入文本
```

### 2) `/core/decision_actions.py`

定义 DecisionAction 枚举：

```python
- CONTINUE_TASK
- INSERT_TASK
- REPLACE_TASK
- RESUME_MAIN_TASK
- NO_OP
- ASK_USER
- TRIGGER_PLANB
```

### 3) `/core/decision_output.py`

定义 DecisionOutput 结构：

```python
- action: DecisionAction
- params: dict      # 如 insert_task_spec / new_task_spec / question_type 等
- narration: str    # 给 TTS 播报用的自然语言文案
```

### 4) `/core/task_result.py`

定义 TaskResult 结构：

```python
- status: "ok" | "failed" | "cancelled"
- reason: str
- task_id: str
- task_type: str
```

### 5) `/core/events.py`

定义事件枚举或常量，例如：

```python
- TASK_NODE_COMPLETE
- USER_INTENT
- INQUIRY_RESPONSE
- SYSTEM_ALERT
- USER_INACTIVE
- MODEL_STATUS
```

**要求**: 此阶段不写业务逻辑，只定义结构和枚举，并保证可被其它模块 import。

---

## ========================================
## 阶段 2：TaskChainManager 实现（模块 A）
## ========================================

**文件**: `/taskchain/manager.py`

任务链支持主任务 + 子任务栈 + 恢复机制。

### 核心字段（可放在类属性里）：

```python
- main_task
- sub_task_stack: list
- active_task
- active_node
- main_task_state（恢复用）
```

### 必须实现的方法（签名可略调，但语义必须一致）：

```python
- start_main_task(task_spec)
- advance()                         # 推进到下一节点
- complete_active_node()            # 当前节点完成
- insert_task(task_spec, resume_strategy="auto")
- _replace_task(new_task_spec)
- complete_active_task()            # 子任务完成后调用
- resume_main_task()
- apply_decision(decision_output: DecisionOutput)
```

`apply_decision` 要根据 `decision_output.action` 分派到：

- `CONTINUE_TASK` → `_continue_task` / `advance`
- `INSERT_TASK` → `insert_task(...)`
- `REPLACE_TASK` → `_replace_task(...)`

### 禁止：

- 从外部直接改 `active_task` / `sub_task_stack` 等内部属性；外部只能调用 `apply_decision` 和公开方法。

### 错误处理：

错误时返回 `TaskResult(status="failed"/"cancelled"` 等)。

---

## ========================================
## 阶段 3：Inquiry 问询系统实现（模块 B）
## ========================================

**目录**: `/inquiry`

**文件**:
- `inquiry_manager.py`
- `parser.py`
- `inquiry_state.py`（如有需要，可简单管理上下文）

### 1) InquiryParser（`/inquiry/parser.py`）

实现 `parse(text: str, tpl: dict) → ParsedIntent`：

**解析逻辑优先级**:

1. 同义词匹配（`tpl["synonyms"]`）
2. 精确选项匹配（`tpl["options"]`）
3. 特殊指令解析（如"厕所/换/买"等）
4. 无法解析 → `intent_name="UNKNOWN"`

**特殊指令示例**:

- 包含"厕所" → `intent_name="INSERT_TASK"`，`slots={"task_type": "toilet"}`，`need_confirm=True`
- 包含"换"或"改" → `intent_name="CHANGE_DESTINATION"`，`need_confirm=True`
- 包含"买" → `intent_name="INSERT_TASK"`，`slots={"task_type": "buy"}`

第二次封装为 `ParsedIntent`（注意字段：`intent_name`/`slots`/`source`/`need_confirm`/`raw`）。

### 2) InquiryManager（`/inquiry/inquiry_manager.py`）

**职责**:

- 根据 `question_type` + `context` 生成问句（从模板中取）
- 接收用户回答，调用 `InquiryParser` 生成 `ParsedIntent` 返回给决策层

**降级规则（必须实现）**:

- 若连续两次解析为 `UNKNOWN`:
  - 返回 `ParsedIntent(intent_name="UNKNOWN", need_confirm=False)`
  - 留给决策层决定 `NO_OP`
- 不处理任务流，只负责问和解析。

---

## ========================================
## 阶段 4：DecisionCore 实现（模块 C）
## ========================================

**文件**: `/decision/decision_core.py`

**类**: `DecisionCore`

**方法**: `handle_event(event_type, payload, context) → DecisionOutput`

### 处理逻辑包括：

#### 1) 事件类型 USER_INTENT：根据 ParsedIntent.intent_name 做策略：

- `INSERT_TASK` → `action=INSERT_TASK`，`params.insert_task_spec` 从 slots 中生成
- `CHANGE_DESTINATION` → `action=REPLACE_TASK`，`params.new_task_spec` 从 slots 生成
- `RESUME_MAIN_TASK` → `CONTINUE_TASK`
- `CONFIRM` → `CONTINUE_TASK` 或执行特定确认逻辑
- `REJECT` → `NO_OP`
- `AMBIGUOUS` → `NO_OP`
- `UNKNOWN`（第二次）→ `NO_OP`
- 其它未识别 → `NO_OP`

#### 2) 事件类型 TASK_NODE_COMPLETE：

- 若节点标记 `requires_user_confirmation=True` → `ASK_USER`（`question_type` 由 node 类型决定）
- 否则 → `CONTINUE_TASK`

#### 3) 事件类型 SYSTEM_ALERT / USER_INACTIVE：

- 一律 `NO_OP` + 记录日志

#### 4) MODEL_STATUS 触发 TRIGGER_PLANB 条件（如主视觉 + 备份均 down）。

### narration：

用简单规则生成中文播报文案，例如：

- `INSERT_TASK(toilet)` → "好的，我先带你去厕所。"
- `REPLACE_TASK` → "明白了，我帮你更改目的地。"
- `NO_OP` → "我保持当前任务不变。"

**DecisionCore 只做策略，不直接修改 TaskChain，由外部根据 DecisionOutput 调用 TaskChainManager.apply_decision。**

---

## ========================================
## 阶段 5：日志模块（Logging）
## ========================================

**文件**: `/logging/decision_logger.py`

实现一个函数 `log_decision(event, parsed_intent, decision_output, task_context)`：

**必须记录字段**:

- `event_type`
- `intent_name`（若有）
- `action`（DecisionAction 值）
- `reason`（如果你在 DecisionOutput 中有）
- `task_id`
- `task_type`
- `need_confirm`（若有）
- `timestamp`

输出到 stdout 或日志文件均可，但结构要清晰，方便后续检索。

**所有 DecisionCore.handle_event 完成时必须调用 log_decision。**

---

## ========================================
## 阶段 6：联调（Integration）
## ========================================

将上述模块串起来：

1. 用户输入文本 → InquiryParser → ParsedIntent
2. ParsedIntent → DecisionCore.handle_event → DecisionOutput
3. DecisionOutput → TaskChainManager.apply_decision → 更新任务状态
4. 每一步必须有日志。

这里可以写一个简单的 orchestrator / facade 用于测试，如：

- `simulate_user_input("我先去厕所")`
- `simulate_node_complete("到达医院门口")`

等。

---

## ========================================
## 阶段 7：测试用例实现
## ========================================

在 `/tests` 下创建测试文件，建议用 pytest：

- `test_inquiry_parser.py`
- `test_taskchain.py`
- `test_decision_core.py`
- `test_integration_flow.py`

**测试内容要覆盖（示例）**:

- 同义词解析正确（"好，继续吧" → `RESUME_MAIN_TASK`）
- 指令解析正确（"先去厕所" → `INSERT_TASK` with `task_type=toilet`, `need_confirm=True`）
- 插入任务后，完成子任务能正确恢复主任务
- `CHANGE_DESTINATION` 能清空任务栈并替换主任务
- `UNKNOWN` 两次不会卡死，决策层返回 `NO_OP`
- PlanB 条件触发 `TRIGGER_PLANB`

**所有测试必须通过才算 1.4.3 完成。**

---

## ========================================
## 阶段 8：禁止行为（强约束）
## ========================================

- **禁止**从 DecisionCore 直接修改 TaskChain 内部状态
- **禁止**从 Inquiry 改任务流
- **禁止**绕过 DecisionCore，直接对 TaskChain 下命令
- **禁止**新增与 ParsedIntent/DecisionOutput/TaskResult 不兼容的返回结构
- **禁止**在决策时不打日志

---

## END CURSOR BLUEPRINT

---

## 📋 执行检查清单

### 阶段 0
- [ ] 创建所有必需目录
- [ ] 创建 `__init__.py` 文件

### 阶段 1
- [ ] 创建所有核心契约文件
- [ ] 所有结构可被 import
- [ ] 类型注解完整

### 阶段 2
- [ ] TaskChainManager 实现完成
- [ ] `apply_decision()` 方法实现
- [ ] 所有方法签名正确

### 阶段 3
- [ ] InquiryParser 实现完成
- [ ] InquiryManager 实现完成
- [ ] 降级规则实现

### 阶段 4
- [ ] DecisionCore 实现完成
- [ ] 所有事件类型处理
- [ ] narration 生成逻辑

### 阶段 5
- [ ] 日志模块实现完成
- [ ] 所有必需字段记录
- [ ] 日志格式统一

### 阶段 6
- [ ] 模块联调完成
- [ ] 端到端流程正常
- [ ] 日志输出正常

### 阶段 7
- [ ] 所有测试用例实现
- [ ] 所有测试通过
- [ ] 测试覆盖率达标

### 阶段 8
- [ ] 检查禁止行为
- [ ] 代码审查通过
- [ ] 符合工程规范

---

**文档状态**: ✅ 已完成  
**版本**: v1.4.3  
**可直接给 Cursor 执行**: ✅ 是













