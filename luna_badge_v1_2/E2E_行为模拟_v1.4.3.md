# Luna Badge v1.4.3 - 端到端行为模拟

**版本**: v1.4.3  
**创建日期**: 2025-12-05  
**状态**: 📋 行为验证文档

---

## 📋 概述

这是"人话版本"的 E2E 跑一遍，帮你确认 1.4.3 的行为是不是符合预期。

---

## 场景：去医院途中 → 想先去厕所 → 完成后继续去医院

### 1) 系统正在执行主任务

**状态**:
- `main_task = nav_to_hospital`
- `active_node = "从家走到路口"`

**系统行为**: 正常执行导航任务

---

### 2) 到医院门口前，用户说："我先去厕所。"

#### 流程步骤：

**步骤 1: ASR 输出文本**
```
ASR 输出: "我先去厕所"
```

**步骤 2: InquiryParser.parse**

```python
# 输入
text = "我先去厕所"
tpl = inquiry_templates.get("resume_main_task", {})

# 解析过程
1. 同义词匹配：未命中
2. 精确选项匹配：未命中
3. 特殊指令解析：命中"厕所"
   → intent_name = "INSERT_TASK"
   → slots = {"task_type": "toilet"}
   → need_confirm = True

# 输出
ParsedIntent(
    intent_name="INSERT_TASK",
    slots={"task_type": "toilet"},
    source="asr",
    need_confirm=True,
    raw="我先去厕所"
)
```

**步骤 3: ParsedIntent 进 DecisionCore(USER_INTENT)**

```python
# DecisionCore 处理
if parsed_intent.intent_name == "INSERT_TASK":
    if parsed_intent.need_confirm:
        # 需要二次确认
        return DecisionOutput(
            action=DecisionAction.ASK_USER,
            reason="need_confirm_special_intent",
            params={
                "question_type": "confirm_new_intent",
                "context": {
                    "intent_desc": "先去厕所",
                    "original_intent": "INSERT_TASK",
                    "original_slots": {"task_type": "toilet"}
                }
            },
            narration=""  # 由 InquiryManager 生成
        )
```

**步骤 4: TTS 播报**

```python
# InquiryManager 生成问句
inquiry = inquiry_manager.build_question(
    question_type="confirm_new_intent",
    context={"intent_desc": "先去厕所"}
)

# 问句: "你希望我先带你去厕所，对吗？"
# TTS 播报
voice.speak(inquiry["question"])
```

---

### 3) 用户说："嗯，好的。"

#### 流程步骤：

**步骤 1: InquiryParser.parse**

```python
# 输入
text = "嗯，好的"
tpl = inquiry_templates.get("confirm_new_intent", {})

# 解析过程
1. 同义词匹配：命中"好" → "是" → "CONFIRM"
   → intent_name = "CONFIRM"
   → need_confirm = False

# 输出
ParsedIntent(
    intent_name="CONFIRM",
    slots={},
    source="inquiry",
    need_confirm=False,
    raw="嗯，好的"
)
```

**步骤 2: DecisionCore 接到 CONFIRM + 上下文**

```python
# DecisionCore 处理
if parsed_intent.intent_name == "CONFIRM":
    # 检查上下文
    context = previous_context  # 来自上一次 ASK_USER
    if context.get("original_intent") == "INSERT_TASK":
        # 构建任务规格
        task_spec = {
            "task_id": "go_to_toilet_1",
            "type": "go_to_toilet",
            "target": {"poi_type": "toilet"},
            "priority": 8,
            "nodes": [
                {"id": "find_toilet", "name": "寻找厕所"},
                {"id": "toilet_reached", "name": "到达厕所"}
            ],
            "metadata": {
                "source": "user_insert",
                "main_task_id": "nav_to_hospital_1"
            }
        }
        
        return DecisionOutput(
            action=DecisionAction.INSERT_TASK,
            reason="user_confirmed_insert_task",
            params={
                "main_task_id": "nav_to_hospital_1",
                "insert_task_spec": task_spec,
                "resume_strategy": "auto"
            },
            narration="好的，我先带你去厕所。"
        )
```

---

### 4) TaskChainManager.apply_decision

#### 流程步骤：

**步骤 1: 保存主任务状态**

```python
# 保存当前主任务进度
main_task_state = {
    "task": main_task,
    "node": active_node,  # "从家走到路口"
    "timestamp": time.time()
}
```

**步骤 2: 把主任务压入 sub_task_stack**

```python
# 注意：这里不压入 main_task，而是保存状态
# sub_task_stack 只存子任务
```

**步骤 3: active_task 切换为 toilet_task**

```python
active_task = toilet_task_spec
active_node = toilet_task_spec["nodes"][0]  # "find_toilet"
```

**步骤 4: 执行厕所导航任务链**

```python
# 开始执行厕所任务
# 导航到厕所
# 到达厕所
```

---

### 5) Toilet 任务完成

#### 流程步骤：

**步骤 1: TaskResult 返回**

```python
TaskResult(
    status="ok",
    reason="",
    task_id="go_to_toilet_1",
    task_type="go_to_toilet"
)
```

**步骤 2: TaskChainManager.complete_active_task**

```python
# 检查 sub_task_stack
if len(sub_task_stack) > 0:
    finished = sub_task_stack.pop()
    
    if finished["resume_strategy"] == "auto":
        # 自动恢复主任务
        return resume_main_task()
```

**步骤 3: resume_main_task**

```python
# 恢复主任务状态
active_task = main_task
active_node = main_task_state["node"]  # "从家走到路口"
main_task_state = None  # 清理（可选）
```

**步骤 4: TTS 播报**

```python
# 可选：播报恢复信息
narration = "已经处理完厕所，继续带你去医院。"
voice.speak(narration)
```

---

## 完整链路总结

```
"听懂插入要求 → 确认 → 插入任务 → 完成 → 恢复主线"
```

**全部可解释、可测试、可维护。**

---

## 验证点

### 1. 状态一致性
- [ ] 主任务状态正确保存
- [ ] 恢复后节点位置正确
- [ ] 子任务栈正确管理

### 2. 决策正确性
- [ ] 插入任务意图正确识别
- [ ] 二次确认正确触发
- [ ] 确认后正确执行插入

### 3. 任务流正确性
- [ ] 插入任务正确执行
- [ ] 完成后正确恢复
- [ ] 主任务继续执行

### 4. 日志完整性
- [ ] 所有关键步骤都有日志
- [ ] 日志格式符合规范
- [ ] 日志顺序正确

---

**文档状态**: ✅ 已完成  
**版本**: v1.4.3  
**最后更新**: 2025-12-05













