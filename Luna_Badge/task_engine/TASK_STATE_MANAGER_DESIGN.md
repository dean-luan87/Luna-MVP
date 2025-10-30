# task_state_manager.py 模块设计文档

## 📚 模块概述

`task_state_manager.py` 是任务执行系统中的状态记录中枢，负责统一管理任务图中所有节点的执行状态、任务整体状态、插入任务记录与恢复点信息，为任务引擎提供可恢复性与流程追踪能力。

---

## 🧩 核心功能

### 1. 状态管理

| 功能 | 方法 | 说明 |
|------|------|------|
| 初始化任务状态 | `init_task_state()` | 初始化任务图和所有节点状态 |
| 更新节点状态 | `update_node_status()` | 更新节点状态（pending→running→complete/failed） |
| 查询节点状态 | `get_node_status()` | 返回节点当前状态 |
| 记录节点输出 | `record_node_output()` | 存储节点执行结果 |
| 获取节点输出 | `get_node_output()` | 读取节点输出数据供下游使用 |
| 设置任务状态 | `set_task_status()` | 设置任务整体状态 |
| 获取任务状态 | `get_task_status()` | 返回任务整体状态 |

### 2. 插入任务支持

| 功能 | 方法 | 说明 |
|------|------|------|
| 暂停主任务 | `pause_for_inserted_task()` | 暂存当前进度，记录恢复点 |
| 恢复主任务 | `resume_from_inserted_task()` | 插入任务完成后恢复执行 |

### 3. 持久化

| 功能 | 方法 | 说明 |
|------|------|------|
| 保存状态 | `persist_state_to_file()` | 将状态写入JSON文件 |
| 加载状态 | `load_state_from_file()` | 从文件恢复任务状态 |
| 批量保存 | `save_all_to_directory()` | 保存所有任务状态 |
| 批量加载 | `load_all_from_directory()` | 从目录加载所有状态 |

### 4. 状态摘要

| 功能 | 方法 | 说明 |
|------|------|------|
| 获取摘要 | `get_state_summary()` | 生成用于日志上报的状态摘要 |

---

## 📊 数据结构

### TaskState（任务状态）

```python
{
    "task_id": "hospital_visit",
    "graph_status": "running",  # pending/running/complete/paused/error
    "current_node_id": "goto_department",
    "nodes": {
        "plan_route": {
            "status": "complete",
            "output": {"eta": "18min", "mode": "bus"},
            "timestamp": "2025-10-30T15:00:01"
        },
        "goto_department": {
            "status": "running",
            "output": null,
            "timestamp": "2025-10-30T15:05:30"
        }
    },
    "inserted_task": {
        "is_active": false,
        "paused_main_node": null,
        "inserted_task_id": null,
        "pause_time": null
    },
    "progress": 33,
    "started_at": 1698656400.0,
    "paused_at": null,
    "completed_at": null,
    "context": {}
}
```

---

## 🔄 状态流转

```
pending → running → complete
         ↓
       failed
         ↓
       (fallback)
```

### 节点状态

- `pending`: 待执行
- `running`: 执行中
- `complete`: 已完成
- `failed`: 执行失败
- `skipped`: 跳过（可选）

### 任务状态

- `pending`: 待启动
- `running`: 运行中
- `complete`: 已完成
- `paused`: 已暂停（插入任务）
- `error`: 错误/失败

---

## 💾 持久化机制

### 存储位置

```
data/task_states/
├── hospital_visit_20251030T150001.json
├── government_service_20251030T151500.json
└── shopping_mall_20251030T152000.json
```

### 文件格式

- 文件名格式：`{task_id}_{timestamp}.json`
- 内容格式：JSON（UTF-8编码，2空格缩进）
- 自动时间戳：每次保存时生成新的时间戳

### 恢复机制

1. 系统启动时调用 `load_all_from_directory()`
2. 自动检测 `data/task_states/` 目录中的所有 `.json` 文件
3. 恢复任务状态到内存
4. 支持任务断点续传

---

## 🔧 使用示例

### 1. 初始化任务

```python
from task_engine import TaskStateManager

manager = TaskStateManager()

# 初始化任务状态
node_ids = ["plan_route", "goto_department", "wait_for_call"]
manager.init_task_state("hospital_visit", node_ids)
```

### 2. 更新节点状态

```python
# 节点开始执行
manager.update_node_status("hospital_visit", "plan_route", "running")

# 节点执行完成
manager.update_node_status("hospital_visit", "plan_route", "complete", 
                           output={"destination": "虹口医院", "eta": "30min"})
```

### 3. 插入任务处理

```python
# 暂停主任务
pause_point = manager.pause_for_inserted_task(
    "hospital_visit", 
    "toilet_task", 
    "goto_department"
)

# 执行插入任务...

# 恢复主任务
resume_point = manager.resume_from_inserted_task("hospital_visit")
```

### 4. 状态持久化

```python
# 保存状态
filepath = manager.persist_state_to_file("hospital_visit")

# 加载状态
state = manager.load_state_from_file(filepath)
```

### 5. 获取状态摘要（用于日志上报）

```python
summary = manager.get_state_summary("hospital_visit")

# 输出：
# {
#   "task_id": "hospital_visit",
#   "timestamp": "2025-10-30T15:00:00",
#   "graph_status": "running",
#   "completed_nodes": ["plan_route", "goto_department"],
#   "failed_nodes": [],
#   "current_node": "wait_for_call",
#   "inserted_task_active": False,
#   "progress": 66,
#   "nodes_total": 13
# }
```

---

## 📋 API参考

### 核心方法

#### init_task_state(task_id: str, node_ids: List[str]) -> None

初始化任务状态。

**参数：**
- `task_id`: 任务ID
- `node_ids`: 所有节点ID列表

#### update_node_status(task_id: str, node_id: str, status: str, 
                   output: Optional[Dict] = None) -> None

更新节点状态。

**参数：**
- `task_id`: 任务ID
- `node_id`: 节点ID
- `status`: 新状态
- `output`: 节点输出（可选）

#### pause_for_inserted_task(task_id: str, inserted_task_id: str, 
                           current_node: str) -> str

暂停主任务执行插入任务。

**返回：**
- 恢复点（当前节点ID）

#### resume_from_inserted_task(task_id: str) -> Optional[str]

插入任务结束后恢复主任务。

**返回：**
- 恢复点（节点ID）

#### persist_state_to_file(task_id: str) -> str

持久化任务状态到文件。

**返回：**
- 文件路径

#### load_state_from_file(filepath: str) -> Optional[Dict]

从文件加载任务状态。

**返回：**
- 状态字典

#### get_state_summary(task_id: str) -> Dict[str, Any]

获取任务状态摘要（用于日志上报）。

**返回：**
- 包含task_id、timestamp、graph_status、completed_nodes、failed_nodes等字段的字典

---

## 🎯 集成点

### 与 task_engine.py 集成

```python
# task_engine.py
from .task_state_manager import TaskStateManager

class TaskEngine:
    def __init__(self):
        self.state_manager = TaskStateManager()
    
    def _execute_task(self, task_id: str):
        # 执行节点前更新状态
        self.state_manager.update_node_status(task_id, node_id, "running")
        
        # 执行节点...
        
        # 执行后更新状态
        self.state_manager.update_node_status(task_id, node_id, "complete", result)
```

### 与 task_report_uploader.py 集成

```python
# task_engine.py
def complete_task(self, task_id: str):
    # 获取状态摘要
    summary = self.state_manager.get_state_summary(task_id)
    
    # 上传执行报告
    self.report_uploader.upload_task_report(summary)
```

---

## ✅ 测试结果

```
✅ 初始化任务状态 - 通过
✅ 更新节点状态 - 通过
✅ 查询节点状态 - 通过
✅ 插入任务暂停/恢复 - 通过
✅ 状态持久化/加载 - 通过
✅ 获取状态摘要 - 通过
```

---

## 🔮 扩展建议

1. **增量持久化** - 只保存变更的节点，减少IO
2. **状态压缩** - 长时间运行的任务状态可能很大
3. **状态版本控制** - 支持状态回滚
4. **分布式状态** - 支持多进程/多机状态同步

---

**task_state_manager.py 模块设计与实现完成！** ✅

