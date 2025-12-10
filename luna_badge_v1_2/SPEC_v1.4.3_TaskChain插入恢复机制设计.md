# Luna Badge v1.4.3 - TaskChain 插入/恢复机制设计

**版本**: v1.4.3  
**创建日期**: 2025-12-05  
**状态**: 📋 设计文档  
**标准级别**: 最高工程标准

---

## 📋 概述

1.4.3 的核心升级是让系统具备"真实生活逻辑"：
- 正在去医院 → 用户突然说"先去厕所"
- 完成子任务 → 系统能自动回到医院导航
- 如果用户在插入任务过程中又问别的事 → 决策层也能处理，不会乱掉

这是智能导航 × 行为级任务管理的基础。

---

## 1. 任务链标准定义（TaskSpec）

### 1.1 TaskSpec 格式

所有任务（主任务/子任务）都必须使用统一格式，保证解耦性。

```python
TaskSpec = {
    "task_id": str,              # 任务唯一标识
    "type": str,                 # navigation / go_to_toilet / buy_item...
    "target": dict,              # 目标描述，如 {"poi": "toilet"}
    "priority": int,             # 1-10（插入任务通常更高）
    "nodes": list,               # 路径节点列表
    "metadata": dict             # 额外信息（如是否用户主动）
}
```

### 1.2 TaskSpec 示例

**主任务（导航到医院）**:
```python
{
    "task_id": "nav_to_hospital_1",
    "type": "navigation",
    "target": {"poi": "hospital"},
    "priority": 5,
    "nodes": [
        {"id": "start", "name": "起点"},
        {"id": "street_corner", "name": "街角"},
        {"id": "to_hospital_gate", "name": "医院大门"}
    ],
    "metadata": {
        "source": "user_request",
        "created_at": "2025-12-05T10:00:00Z"
    }
}
```

**子任务（去厕所）**:
```python
{
    "task_id": "go_to_toilet_1",
    "type": "go_to_toilet",
    "target": {"poi_type": "toilet"},
    "priority": 8,  # 插入任务优先级更高
    "nodes": [
        {"id": "find_toilet", "name": "寻找厕所"},
        {"id": "toilet_reached", "name": "到达厕所"}
    ],
    "metadata": {
        "source": "user_insert",
        "main_task_id": "nav_to_hospital_1",
        "created_at": "2025-12-05T10:05:00Z"
    }
}
```

### 1.3 TaskBuilder（1.4.3 暂不实现）

在 1.4.3 中，"任务生成器（TaskBuilder）"不做，只在 TaskChain 内部建 stub。

---

## 2. TaskChainManager 状态机设计（核心）

### 2.1 状态机定义

任务链必须支持：
- 主任务（Main Task）
- 插入任务栈（Interrupt Stack）
- 自动恢复主任务

**状态机**:
```
ACTIVE_MAIN_TASK → INSERT_TASK → ACTIVE_SUB_TASK
ACTIVE_SUB_TASK → SUB_TASK_FINISHED → RESUME_MAIN_TASK
```

### 2.2 内部结构

```python
class TaskChainManager:
    def __init__(self):
        self.main_task: Optional[TaskSpec] = None
        self.sub_task_stack: List[Dict] = []  # 插入任务栈
        self.active_task: Optional[TaskSpec] = None  # 当前执行的任务
        self.active_node: Optional[Dict] = None  # 当前节点
        self.main_task_state: Optional[Dict] = None  # 主任务状态缓存
```

### 2.3 状态说明

- **main_task**: 主任务（永远不被销毁，只能暂停）
- **sub_task_stack**: 插入任务栈（支持多层嵌套）
- **active_task**: 当前执行的任务（只允许有一个）
- **active_node**: 当前节点
- **main_task_state**: 主任务状态缓存（用于恢复）

---

## 3. 插入任务流程（INSERT_TASK）

### 3.1 DecisionCore 输出

```python
DecisionOutput(
    action=DecisionAction.INSERT_TASK,
    reason="user_insert_task",
    params={
        "main_task_id": "nav_to_hospital_1",
        "insert_task_spec": {
            "type": "go_to_toilet",
            "target": {"poi_type": "toilet"},
            "priority": 8
        },
        "resume_strategy": "auto"  # 或 "ask"
    }
)
```

### 3.2 TaskChainManager 接口规范

```python
def insert_task(
    self,
    task_spec: Dict[str, Any],
    resume_strategy: str
) -> Dict[str, Any]:
    """
    插入子任务
    
    Args:
        task_spec: 子任务规格
        resume_strategy: "auto" | "ask"
        
    Returns:
        dict: {"status": "ok", "task": task_spec}
    """
    # 1. 保存当前主任务进度
    self._save_main_task_state()
    
    # 2. 将插入任务压入 sub_task_stack
    self.sub_task_stack.append({
        "task": task_spec,
        "resume_strategy": resume_strategy
    })
    
    # 3. 切换 active_task
    self.active_task = task_spec
    self._reset_active_node(task_spec)
    
    return {"status": "ok", "task": task_spec}
```

### 3.3 关键设计说明（工程级）

#### 3.3.1 主任务永远不被销毁

- 只能暂停，但状态保留
- `main_task` 对象始终存在
- 通过 `main_task_state` 缓存当前进度

#### 3.3.2 只允许有一个 active task

- 保证执行链永远清晰
- `active_task` 只有一个
- 切换时立即更新

#### 3.3.3 支持多层嵌套

- `sub_task_stack` 是一个真正的 stack
- 支持：厕所 → 又买水 → 再回主任务
- 后进先出（LIFO）恢复顺序

### 3.4 辅助方法

```python
def _save_main_task_state(self) -> None:
    """保存主任务状态"""
    if self.main_task and self.active_task == self.main_task:
        self.main_task_state = {
            "task": self.main_task,
            "node": self.active_node,
            "timestamp": time.time()
        }

def _reset_active_node(self, task_spec: Dict[str, Any]) -> None:
    """重置当前节点为新任务的首节点"""
    if task_spec.get("nodes"):
        self.active_node = task_spec["nodes"][0]
    else:
        self.active_node = None
```

---

## 4. 子任务完成流程（SUB_TASK_FINISHED）

### 4.1 完成接口

```python
def complete_active_task(self) -> Dict[str, Any]:
    """
    完成当前活动任务
    
    Returns:
        dict: 恢复信息或询问信息
    """
    if not self.sub_task_stack:
        # 没有子任务，可能是主任务完成
        return self._handle_main_task_complete()
    
    # 弹出完成的子任务
    finished = self.sub_task_stack.pop()
    
    if finished["resume_strategy"] == "auto":
        return self._resume_main_task()
    
    if finished["resume_strategy"] == "ask":
        return {
            "action": "ASK_USER",
            "question": "是否继续之前的任务？",
            "resume_context": self.main_task_state
        }
```

### 4.2 恢复主任务

```python
def _resume_main_task(self) -> Dict[str, Any]:
    """
    恢复主任务
    
    Returns:
        dict: {"status": "resumed", "task": self.main_task}
    """
    if not self.main_task or not self.main_task_state:
        return {
            "status": "error",
            "reason": "no_main_task_to_resume"
        }
    
    # 恢复缓存的主任务状态
    self.active_task = self.main_task
    self.active_node = self.main_task_state["node"]
    
    # 清理状态缓存（可选）
    # self.main_task_state = None
    
    return {
        "status": "resumed",
        "task": self.main_task,
        "node": self.active_node
    }
```

### 4.3 主任务完成处理

```python
def _handle_main_task_complete(self) -> Dict[str, Any]:
    """处理主任务完成"""
    return {
        "status": "main_task_complete",
        "task": self.main_task
    }
```

---

## 5. TaskChainManager 与 DecisionCore 的协作模式

### 5.1 完整链路

#### 场景：用户说"先去厕所"

**步骤 1: 用户意图输入**
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

**步骤 2: DecisionCore 决策**
```python
DecisionOutput(
    action=DecisionAction.INSERT_TASK,
    reason="user_insert_task",
    params={
        "main_task_id": "nav_to_hospital_1",
        "insert_task_spec": {...},
        "resume_strategy": "auto"
    }
)
```

**步骤 3: TaskChainManager 插入任务**
```python
result = task_chain_manager.insert_task(
    task_spec=params["insert_task_spec"],
    resume_strategy=params["resume_strategy"]
)
# result = {"status": "ok", "task": {...}}
```

#### 场景：完成厕所任务

**步骤 1: 任务节点完成事件**
```python
DecisionInput(
    event_type=EventType.TASK_NODE_COMPLETE,
    event_payload={"node_id": "toilet_reached"},
    task_context={
        "task_id": "go_to_toilet_1",
        "active_node": {"id": "toilet_reached"},
        "is_subtask": True
    },
    ...
)
```

**步骤 2: DecisionCore 决策**
```python
DecisionOutput(
    action=DecisionAction.CONTINUE_TASK,
    reason="subtask_complete_resume_main",
    params={
        "task_id": "go_to_toilet_1",
        "should_resume": True
    }
)
```

**步骤 3: TaskChainManager 完成并恢复**
```python
result = task_chain_manager.complete_active_task()
# result = {"status": "resumed", "task": main_task, "node": {...}}
```

**步骤 4: 恢复主任务后继续**
```python
# active_task 已切回 main_task
# active_node 已恢复为之前保存的节点
# 继续推进主任务节点
```

---

## 6. 错误处理机制（最高标准必备）

### 6.1 插入任务失败

**场景**: 如果插入任务本身失败（如厕所无法到达）

**TaskChainManager 返回**:
```python
{
    "status": "failed",
    "reason": "navigation_failed",
    "task": task_spec
}
```

**DecisionCore 自动触发**:
```python
DecisionOutput(
    action=DecisionAction.ASK_USER,
    reason="subtask_failed",
    params={
        "question_type": "subtask_failed",
        "failed_task": task_spec,
        "main_task_context": main_task_state
    }
)
```

### 6.2 用户在子任务中改目的地

**场景**: 如果用户在子任务中突然改目的地

**DecisionCore 直接输出**:
```python
DecisionOutput(
    action=DecisionAction.REPLACE_TASK,
    reason="user_change_dest_during_subtask",
    params={
        "old_task_id": "go_to_toilet_1",
        "new_task_spec": {
            "type": "navigation",
            "target": {"poi": "home"}
        }
    }
)
```

**TaskChainManager 处理**:
```python
def replace_task(self, old_task_id: str, new_task_spec: Dict) -> Dict:
    """替换任务（清空子任务栈）"""
    # 清空 sub_task_stack
    self.sub_task_stack.clear()
    
    # 取消主任务
    if self.main_task and self.main_task["task_id"] == old_task_id:
        self.main_task = None
        self.main_task_state = None
    
    # 创建新任务
    self.main_task = new_task_spec
    self.active_task = new_task_spec
    self._reset_active_node(new_task_spec)
    
    return {"status": "replaced", "task": new_task_spec}
```

### 6.3 多层嵌套恢复错误

**场景**: 如果恢复主任务时状态丢失

**处理**:
```python
def _resume_main_task(self) -> Dict[str, Any]:
    if not self.main_task or not self.main_task_state:
        return {
            "status": "error",
            "reason": "no_main_task_to_resume",
            "action": "ASK_USER",
            "question": "主任务状态已丢失，是否重新开始？"
        }
    # ... 正常恢复逻辑
```

---

## 7. 与 1.4.3 多模型调度器的联动

### 7.1 插入任务时的模型选择

```python
# 插入任务时
model = model_scheduler.select_model(
    task_type=task_spec["type"],
    context={
        "is_subtask": True,
        "main_task_type": self.main_task["type"]
    }
)

# 选择对应模型即可，不需要复杂逻辑
```

### 7.2 模型状态检查

```python
# 在插入任务前检查模型状态
if not model_scheduler.is_model_available(task_spec["type"]):
    return {
        "status": "error",
        "reason": "model_unavailable"
    }
```

---

## 8. 与 PlanB 的联动（仅触发，不执行）

### 8.1 子任务中模型故障

**场景**: 如果在子任务中视觉/语音模型挂掉

**DecisionCore 直接输出**:
```python
DecisionOutput(
    action=DecisionAction.TRIGGER_PLANB,
    reason="planB_condition_matched",
    params={
        "context_snapshot": {
            "active_task": self.active_task,
            "sub_task_stack": self.sub_task_stack,
            "main_task_state": self.main_task_state,
            "model_status": {...}
        }
    }
)
```

### 8.2 TaskChainManager 进入暂停状态

```python
def pause_for_planb(self) -> Dict[str, Any]:
    """进入 PlanB 暂停状态"""
    # 保存所有状态
    self._save_all_states()
    
    # 标记为暂停
    self._paused = True
    
    return {
        "status": "paused",
        "active_task_state": {
            "task": self.active_task,
            "node": self.active_node
        },
        "sub_task_stack": self.sub_task_stack,
        "main_task_state": self.main_task_state
    }
```

**等待 1.5+ 或三期真正的 PlanB 介入**

---

## 9. 完整接口定义

### 9.1 TaskChainManager 公共接口

```python
class TaskChainManager:
    # 任务管理
    def create_task(self, task_spec: Dict) -> Dict[str, Any]
    def start_task(self, task_id: str) -> Dict[str, Any]
    def pause_task(self, task_id: str) -> Dict[str, Any]
    def cancel_task(self, task_id: str) -> Dict[str, Any]
    
    # 插入/恢复
    def insert_task(self, task_spec: Dict, resume_strategy: str) -> Dict[str, Any]
    def complete_active_task(self) -> Dict[str, Any]
    def _resume_main_task(self) -> Dict[str, Any]
    
    # 任务替换
    def replace_task(self, old_task_id: str, new_task_spec: Dict) -> Dict[str, Any]
    
    # 状态查询
    def get_active_task(self) -> Optional[Dict]
    def get_main_task(self) -> Optional[Dict]
    def get_sub_task_stack(self) -> List[Dict]
    def is_main_task_active(self) -> bool
    
    # PlanB
    def pause_for_planb(self) -> Dict[str, Any]
```

---

## 10. 数据结构定义

### 10.1 TaskSpec

```python
@dataclass
class TaskSpec:
    task_id: str
    type: str
    target: Dict[str, Any]
    priority: int  # 1-10
    nodes: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### 10.2 SubTaskEntry

```python
@dataclass
class SubTaskEntry:
    task: TaskSpec
    resume_strategy: str  # "auto" | "ask"
    inserted_at: float  # timestamp
```

### 10.3 MainTaskState

```python
@dataclass
class MainTaskState:
    task: TaskSpec
    node: Dict[str, Any]
    timestamp: float
```

---

## 11. 设计原则总结

### 11.1 核心原则

1. **主任务永远不被销毁** - 只能暂停，状态保留
2. **只允许有一个 active task** - 保证执行链清晰
3. **支持多层嵌套** - sub_task_stack 是真正的 stack
4. **状态可恢复** - 所有状态都可以恢复
5. **错误可处理** - 所有错误都有明确的处理路径

### 11.2 工程标准

1. **接口统一** - 所有方法返回统一格式
2. **状态可查询** - 所有状态都可以查询
3. **错误可追踪** - 所有错误都有日志
4. **可测试性** - 所有方法都可以独立测试

---

**文档状态**: ✅ 已完成  
**版本**: v1.4.3  
**标准级别**: 最高工程标准  
**最后更新**: 2025-12-05


