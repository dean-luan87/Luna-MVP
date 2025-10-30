# Luna Badge v1.4 - 最小任务引擎子系统架构文档

## 📚 设计目标

构建一个**可落地、可集成、可控缓存**的任务引擎子系统，专为视障场景打造，具备：

- ✅ 管理主线任务链 + 插入任务
- ✅ 控制任务状态切换（运行/暂停/完成/丢弃）
- ✅ 限制任务缓存数量，避免内存占用累积
- ✅ 可嵌入至主流程中逐步演化为完整 Task Hub

---

## 🧩 系统组成模块

| 模块 | 说明 |
|------|------|
| `task_engine.py` | 子系统入口，负责注册/执行/释放任务链 |
| `task_graph.json` | 每个任务链的数据结构 |
| `task_node_executor.py` | 节点执行器，调用实际模块执行（如导航/播报） |
| `task_state_manager.py` | 当前状态记录器（进度、插入任务、是否中断） |
| `task_cache_manager.py` | 仅保留 3个任务缓存（最新主任务 + 2个子任务） |
| `task_cleanup.py` | 超时/已完成任务自动释放 |
| `inserted_task_queue.py` | 插入任务排队机制，支持返回主任务点 |

---

## ⚙️ 运行机制

```
用户命令 → 触发任务链 → task_engine → task_graph_parser
                                    ↓
                        task_node_executor → 调用功能模块
                                    ↓
                           节点完成 → task_state_manager

插入语音 → inserted_task_queue → task_engine
                                   ↓
                           inserted_graph → task_node_executor

完成全部任务 → task_cleanup → task_cache_manager
```

---

## 🔧 多任务联动逻辑（v1.4 限制）

| 类型 | 限制条件 |
|------|----------|
| **主任务链** | 仅支持 1 个 active |
| **插入任务链** | 同时最多存在 2 个（进行中 + 暂停） |
| **恢复机制** | 插入任务完成后，回到主任务中断点 |
| **清理机制** | 已完成 / 丢弃任务 → 延迟 2 分钟后自动释放 |
| **超时任务** | 60分钟无进度 → 强制关闭（记录为异常） |

---

## 📁 文件与目录结构

```
luna_badge/
├── task_engine.py                  # 总入口
├── task_graphs/
│   └── hospital_visit.json         # 医院任务链
│   └── buy_snack.json              # 插入任务示例
├── task_node_executor.py
├── task_state_manager.py
├── inserted_task_queue.py
├── task_cache_manager.py
├── task_cleanup.py
└── __init__.py
```

---

## 🎯 核心功能

### 1. 任务引擎 (`task_engine.py`)

**职责**：总入口，负责任务链的注册、执行、释放

**主要方法**：
```python
- load_task_graph(graph_file): 加载任务图JSON文件
- register_task(task_graph): 注册任务链
- start_task(graph_id): 启动任务
- pause_task(graph_id): 暂停任务
- resume_task(graph_id): 恢复任务
- complete_task(graph_id): 完成任务
- insert_task(graph_id, inserted_graph, return_point): 插入任务
- get_task_status(graph_id): 获取任务状态
```

**限制**：
- 最多1个主任务（active状态）
- 最多2个插入任务（同时存在）

### 2. 节点执行器 (`task_node_executor.py`)

**职责**：调用实际模块执行节点任务

**支持节点类型**：
- `navigation`: 导航节点
- `interaction`: 用户交互节点
- `observation`: 观察识别节点
- `external_call`: 外部服务调用节点
- `memory_action`: 记忆操作节点
- `condition_check`: 条件检查节点

### 3. 状态管理器 (`task_state_manager.py`)

**职责**：记录任务执行状态（进度、节点、上下文）

**数据结构**：
```python
@dataclass
class TaskState:
    graph_id: str
    current_node: str
    progress: int  # 0-100
    started_at: float
    paused_at: float
    context: Dict[str, Any]
    interrupt_point: str
```

### 4. 插入任务队列 (`inserted_task_queue.py`)

**职责**：管理插入任务，记录父任务关系和返回点

**主要方法**：
```python
- add_inserted_task(parent_id, inserted_id, return_point): 添加插入任务
- get_parent_task(inserted_id): 获取父任务ID
- get_return_point(inserted_id): 获取返回点
- remove_inserted_task(inserted_id): 移除插入任务
```

### 5. 缓存管理器 (`task_cache_manager.py`)

**职责**：LRU缓存管理，最多保留3个任务

**缓存策略**：
- 最新访问的任务在最前面
- 超出容量时自动移除最旧的任务
- 提供缓存使用情况查询

### 6. 任务清理器 (`task_cleanup.py`)

**职责**：自动清理已完成/超时任务

**清理策略**：
- 已完成任务：延迟2分钟后释放
- 取消任务：立即释放
- 超时任务：60分钟无进度自动关闭
- 后台线程每10秒检查一次

---

## 🚀 使用示例

### 加载并执行任务

```python
from task_engine import get_task_engine

# 获取任务引擎
engine = get_task_engine()

# 加载任务图
task_graph = engine.load_task_graph("task_graphs/hospital_visit.json")

# 注册任务
graph_id = engine.register_task(task_graph)

# 启动任务
engine.start_task(graph_id)

# 检查任务状态
status = engine.get_task_status(graph_id)
print(f"状态: {status['status']}, 进度: {status['progress']}%")
```

### 插入任务

```python
# 加载插入任务
inserted_graph = engine.load_task_graph("task_graphs/buy_snack.json")

# 在当前任务中插入
engine.insert_task(
    current_graph_id=main_graph_id,
    inserted_graph=inserted_graph,
    return_point="navigate_toilet"
)
```

### 检查缓存状态

```python
cache_info = engine.get_cache_info()
print(f"缓存使用: {cache_info['current_size']}/{cache_info['max_size']}")
print(f"活动任务: {cache_info['active_tasks']}")
print(f"已完成任务: {cache_info['completed_tasks']}")
```

---

# Luna Badge v1.4 - 最小任务引擎子系统

## 📚 项目概述

Luna Badge v1.4最小任务引擎子系统，专为视障场景打造，具备日志上传、缓存控制、插入任务支持等能力。

**设计原则：**
- ✅ 可落地：最小化实现，易于集成
- ✅ 可集成：独立模块，便于集成到主系统
- ✅ 可控缓存：严格限制资源占用

---

## 📁 目录结构

```
task_engine/
├── task_engine.py                  # ✅ 任务引擎入口
├── task_graph_loader.py           # ✅ 任务图加载器
├── task_node_executor.py          # ✅ 节点执行器
├── task_state_manager.py          # ✅ 状态管理器
├── task_cache_manager.py          # ✅ 缓存管理器
├── inserted_task_queue.py         # ✅ 插入任务队列
├── task_cleanup.py                # ✅ 任务清理器
├── task_report_uploader.py        # ✅ 报告上传器
├── __init__.py                    # 模块导出
├── README.md                      # 本文档
├── DEVELOPMENT_REPORT.md          # 开发报告
└── test_integration.py            # 集成测试

task_graphs/
├── hospital_visit.json             # ✅ 医院就诊任务链
└── sample_inserted_task.json      # ✅ 插入任务示例
```

---

## 🧩 模块说明

### 1. task_engine.py - 任务引擎入口

**职责：**调度任务图、加载执行器、控制状态、执行节点

**功能点：**
- 加载task_graph，初始化运行
- 遇到插入任务时暂停主任务
- 节点执行完毕写入状态
- 调用日志上传模块上报完成情况

**接口：**
```python
engine = get_task_engine()
graph = engine.load_task_graph("task_graphs/hospital_visit.json")
graph_id = engine.register_task(graph)
engine.start_task(graph_id)
status = engine.get_task_status(graph_id)
```

### 2. task_graph_loader.py - 任务图加载器

**职责：**从.json文件加载标准任务图对象

**功能点：**
- 校验字段完整性
- 支持预设路径或通过API获取图谱（预留）
- 返回结构化TaskGraph对象

**接口：**
```python
loader = get_graph_loader()
graph = loader.load_from_file("hospital_visit.json")
# 预留：graph = loader.load_from_api("graph_id")
```

### 3. task_node_executor.py - 节点执行器

**职责：**按类型调度对应功能模块（导航、播报、语音识别等）

**功能点：**
- 每个节点执行逻辑隔离
- 状态机控制：pending → running → complete
- 回传节点输出结果到状态管理器

**支持的节点类型：**
- `navigation`: 导航相关任务
- `interaction`: 与用户对话/问询
- `observation`: 视觉/语音识别
- `external_call`: 联动外部服务
- `memory_action`: 记忆写入/修改/调取
- `condition_check`: 判断环境/状态

### 4. task_state_manager.py - 任务状态记录器

**职责：**记录任务链执行状态、节点状态、插入点、恢复点

**功能点：**
- 支持序列化为JSON
- 支持系统恢复后重载
- 暂停后保留状态至task_cache_manager

**状态文件位置：**`data/task_states/`

### 5. task_cache_manager.py - 缓存管理器

**职责：**管理最多保留3条任务缓存（1主任务 + 2插入）

**功能点：**
- 清理已完成/废弃任务
- 时间戳过期自动回收
- LRU缓存策略

### 6. inserted_task_queue.py - 插入任务调度器

**职责：**处理用户中途插入的小任务（如如厕、购物）

**功能点：**
- 记录插入点位置
- 完成后跳回主任务
- 与task_engine联动切换任务上下文

### 7. task_cleanup.py - 超时与回收机制

**职责：**定时清理已完成/失败/超时任务

**功能点：**
- 2分钟内未访问自动移出缓存
- 每日清理任务日志
- 日志保留策略（30天）

### 8. task_report_uploader.py - 执行记录上传模块

**职责：**将任务运行数据上传至云端后台

**功能点：**
- 上传字段：task_id、user_id、图谱名、执行链路、失败节点、修正行为等
- 支持重试与失败本地保存
- API地址：`https://api.luna.ai/task/report`（占位）

**接口：**
```python
uploader = get_report_uploader()
success = uploader.upload_task_report({
    "task_id": "graph_id",
    "user_id": "user_id",
    "graph_name": "任务名称",
    "execution_path": ["node1", "node2"],
    "failed_nodes": [],
    "duration": 1800,
    "status": "completed"
})
```

---

## 🔧 系统限制（v1.4）

| 类型 | 限制条件 |
|------|----------|
| **主任务链** | 仅支持 1 个 active |
| **插入任务链** | 同时最多存在 2 个（进行中 + 暂停） |
| **恢复机制** | 插入任务完成后，回到主任务中断点 |
| **清理机制** | 已完成 / 丢弃任务 → 延迟 2 分钟后自动释放 |
| **超时任务** | 60分钟无进度 → 强制关闭（记录为异常） |
| **缓存限制** | 最多3个任务（1主任务 + 2插入任务） |

---

## 📋 任务图JSON格式

```json
{
  "graph_id": "hospital_visit",
  "scene": "hospital",
  "goal": "完成一次挂号就诊",
  "name": "医院就诊流程",
  "description": "完整的医院就诊流程",
  "nodes": [
    {
      "id": "plan_route",
      "type": "navigation",
      "title": "规划路线",
      "input": "医院名称",
      "output": "路线信息",
      "fallback": "manual_ask",
      "config": {
        "destination": "虹口医院",
        "transport_mode": "walking"
      },
      "timeout": 300
    }
  ],
  "edges": [
    {"from": "plan_route", "to": "next_node"}
  ],
  "metadata": {
    "estimated_duration": 120,
    "complexity": "high"
  }
}
```

---

## 🚀 快速开始

### 基础使用

```python
from task_engine import get_task_engine

# 1. 获取任务引擎
engine = get_task_engine()

# 2. 加载任务图
task_graph = engine.load_task_graph("task_graphs/hospital_visit.json")

# 3. 注册任务
graph_id = engine.register_task(task_graph)

# 4. 启动任务
engine.start_task(graph_id)

# 5. 检查状态
status = engine.get_task_status(graph_id)
print(f"状态: {status['status']}, 进度: {status['progress']}%")
```

### 插入任务

```python
# 加载插入任务
inserted_graph = engine.load_task_graph("task_graphs/sample_inserted_task.json")

# 插入到当前任务
engine.insert_task(main_graph_id, inserted_graph, return_point="node_id")
```

### 暂停/恢复任务

```python
# 暂停任务
engine.pause_task(graph_id)

# 恢复任务
engine.resume_task(graph_id)
```

---

## 🧪 测试

运行集成测试：

```bash
cd Luna_Badge
python3 task_engine/test_integration.py
```

---

## 📊 数据存储

- **任务状态文件：** `data/task_states/*.json`
- **待上传报告：** `data/task_reports_pending.json`
- **任务日志：** `data/task_logs/*`（保留30天）

---

## 🔮 后续演进

1. **v1.5**: 增加语音控制接口
2. **v1.6**: 集成长期记忆系统
3. **v2.0**: 完整任务中心 + AI生成任务

---

## 📝 开发规范

- 所有模块需具备独立初始化函数，便于主控注册
- 每个模块需提供清晰的输入/输出接口
- 所有任务状态文件存入 `/data/task_states/`
- 任务日志上传接口统一为：`https://api.luna.ai/task/report`

---

## ✅ 验证结果

```
✅ 8/8 模块导入成功
✅ TaskEngine初始化成功
✅ TaskGraphLoader初始化成功
✅ TaskReportUploader初始化成功
✅ 缓存信息查询成功
✅ 集成测试通过
```

---

**Luna Badge v1.4 最小任务引擎子系统开发完成！** 🎉

### ✅ 轻量级
- 最小化依赖
- 简单的JSON任务定义
- 高效的内存管理

### ✅ 可控
- 严格的任务数量限制
- 自动超时检测
- 延迟清理机制

### ✅ 可扩展
- 支持自定义节点类型
- 灵活的任务图结构
- 易于集成到主系统

### ✅ 可靠
- 状态持久化
- 错误处理和恢复
- 后台自动清理

---

## 🔮 未来演进路径

当前v1.4 → 逐步演进为完整TaskHub

1. **v1.4**: 最小任务引擎（当前）
2. **v1.5**: 增加语音控制接口
3. **v1.6**: 集成长期记忆系统
4. **v2.0**: 完整任务中心 + AI生成任务

---

## 📊 测试结果

```
🚀 Luna Badge v1.4 任务引擎测试
✅ 任务图加载成功
✅ 任务注册成功
✅ 任务启动成功
✅ 任务状态查询正常
✅ 缓存管理正常
✅ 任务限制检查通过
```

---

## 🎯 总结

**Luna Badge v1.4 最小任务引擎子系统**已成功构建！

- ✅ 完整实现了任务引擎核心功能
- ✅ 支持多任务链管理和插入机制
- ✅ 严格的资源控制和自动清理
- ✅ 可落地的实现，易于集成
- ✅ 为未来扩展奠定了坚实基础

**可以开始集成到主系统，逐步演化为完整的Task Hub！** 🚀
