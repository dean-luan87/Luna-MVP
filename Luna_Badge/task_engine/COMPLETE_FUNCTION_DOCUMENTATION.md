# Luna Badge v1.4 - 完整功能文档

## 📚 模块总览

Luna Badge v1.4 任务引擎子系统包含以下核心模块：

| 模块 | 文件名 | 代码量 | 核心职责 |
|------|--------|--------|----------|
| 任务引擎入口 | task_engine.py | 426行 | 任务调度、执行控制 |
| 任务图加载器 | task_graph_loader.py | 239行 | JSON加载、字段校验 |
| 节点执行器 | task_node_executor.py | 532行 | 按类型调度功能模块 |
| 状态管理器 | task_state_manager.py | 592行 | 状态追踪、持久化、恢复 |
| 缓存管理器 | task_cache_manager.py | 419行 | 缓存管理、TTL、快照 |
| 插入任务队列 | inserted_task_queue.py | 404行 | 插入任务管理、嵌套保护 |
| 任务清理器 | task_cleanup.py | 207行 | 超时检测、延迟清理 |
| 报告上传器 | task_report_uploader.py | 233行 | 执行记录上传、重试 |
| 故障安全触发器 | failsafe_trigger.py | 400行 | 心跳监测、强制恢复 |
| 重启恢复引导 | restart_recovery_flow.py | 441行 | 重启后任务恢复引导 |

**总计：** 10个核心模块 + 1个测试模块 = 4,013行代码

---

## 🎯 核心功能详细说明

### 1. 任务图加载 (task_graph_loader.py)

#### 功能
- 从JSON文件加载任务图定义
- 字段完整性校验
- 兼容新旧格式（scene_type/scene）
- 支持API加载（预留接口）

#### 接口
```python
from task_engine.task_graph_loader import TaskGraphLoader

loader = TaskGraphLoader(base_path="task_engine/task_graphs")
graph = loader.load_from_file("hospital_visit.json")

# 获取任务信息
print(graph.graph_id)      # 任务ID
print(graph.scene)         # 场景类型
print(graph.goal)          # 任务目标
print(len(graph.nodes))    # 节点数量
```

#### 支持的场景类型
- `hospital` - 医院场景
- `government` - 政务服务
- `retail` - 零售购物
- `transport` - 交通出行
- `emergency` - 紧急场景
- `custom` - 自定义场景

---

### 2. 节点执行器 (task_node_executor.py)

#### 功能
- 按节点类型调用对应功能模块
- 状态流转：pending → running → complete/failed
- fallback机制
- Mock支持（模块不存在时降级）

#### 支持的节点类型

| 类型 | 功能 | 调用模块 |
|------|------|----------|
| `interaction` | 用户交互 | voice_interaction.ask_user() |
| `navigation` | 导航任务 | ai_navigation.navigate_to() |
| `observation` | 观察识别 | vision + OCR |
| `condition_check` | 条件检查 | condition_checker.check() |
| `external_call` | 外部服务 | external_services.call() |
| `memory_action` | 记忆操作 | memory_manager.write/read() |
| `environmental_state` | 环境状态 | environment_checker.observe() |
| `scene_entry` | 场景进入 | scene_controller.enter() |
| `decision` | 决策路由 | decision_router.route() |

#### 接口
```python
from task_engine import TaskNodeExecutor

executor = TaskNodeExecutor(state_manager=state_mgr)

# 执行节点
result = executor.execute_node(node, context)

# 结果包含：
# {
#   "node_id": "plan_route",
#   "status": "complete",
#   "success": True,
#   "output": {...},
#   "duration": 1.23,
#   "timestamp": "2025-10-30T15:00:00"
# }
```

---

### 3. 状态管理器 (task_state_manager.py)

#### 功能
- 初始化任务状态
- 更新节点状态
- 记录节点输出
- 插入任务挂起/恢复
- 状态持久化（JSON文件）
- 状态摘要生成

#### 数据结构

```python
TaskState {
    task_id: str
    graph_status: "pending" | "running" | "complete" | "paused" | "error"
    current_node_id: str
    nodes: {
        node_id: {
            status: "pending" | "running" | "complete" | "failed"
            output: {...}
            timestamp: "2025-10-30T15:00:00"
        }
    }
    inserted_task: {
        is_active: bool
        paused_main_node: str
        inserted_task_id: str
    }
    progress: int  # 0-100
}
```

#### 接口
```python
from task_engine import TaskStateManager

manager = TaskStateManager()

# 初始化
manager.init_task_state("hospital_visit", ["node1", "node2"])

# 更新状态
manager.update_node_status("hospital_visit", "node1", "complete", {"eta": "30min"})

# 插入任务
pause_point = manager.pause_for_inserted_task("hospital_visit", "toilet_task", "node2")
resume_point = manager.resume_from_inserted_task("hospital_visit")

# 持久化
filepath = manager.persist_state_to_file("hospital_visit")

# 获取摘要
summary = manager.get_state_summary("hospital_visit")
```

---

### 4. 缓存管理器 (task_cache_manager.py)

#### 功能
- Key-Value缓存（带TTL）
- 自动过期清理
- 快照和恢复
- LRU策略
- 缓存隔离

#### 接口
```python
from task_engine import TaskCacheManager

cache = TaskCacheManager(default_ttl=600)  # 10分钟过期

# 基础操作
cache.set_cache("plan_route.eta", "30分钟", ttl=300)
value = cache.get_cache("plan_route.eta")
has = cache.has_cache("plan_route.eta")
cache.clear_cache("plan_route.eta")

# 快照功能
cache.snapshot_current_state("snapshot_id", prefix="plan_route.")
cache.restore_from_snapshot("snapshot_id")

# 清理
cache.clear_expired_cache()
cache.clear_all_cache()

# 信息
info = cache.get_cache_info()
```

---

### 5. 插入任务队列 (inserted_task_queue.py)

#### 功能
- 注册插入任务
- 暂停主任务
- 嵌套保护
- 超时自动终止
- 完成/取消恢复

#### 接口
```python
from task_engine import InsertedTaskQueue

queue = InsertedTaskQueue(state_manager=state_mgr)

# 注册插入任务
queue.register_inserted_task(
    parent_id="hospital_visit",
    inserted_id="toilet_task",
    resume_node_id="goto_department",
    timeout=300
)

# 检查活跃
is_active = queue.is_inserted_task_active()

# 完成任务
resume_point = queue.complete_inserted_task("toilet_task")

# 取消任务
resume_point = queue.cancel_inserted_task("toilet_task")

# 获取信息
info = queue.get_inserted_task_info()
status = queue.get_queue_status()
```

#### 嵌套保护
- ✅ 不允许嵌套插入任务
- ✅ 已有插入任务时拒绝新的插入请求
- ✅ 提示："不支持嵌套插入任务，请先完成当前插入任务"

---

### 6. 故障安全触发器 (failsafe_trigger.py)

#### 功能
- 心跳监测（Watchdog）
- 模块超时检测
- 故障记录
- 强制恢复机制

#### 接口
```python
from task_engine import FailsafeTrigger

failsafe = FailsafeTrigger(state_manager=state_mgr, cache_manager=cache_mgr)

# 注册并监控
failsafe.monitor_heartbeat("ai_navigation", interval=5)

# 发送心跳
failsafe.record_heartbeat("ai_navigation")

# 触发故障（手动）
failsafe.trigger_failsafe("AI导航模块无响应", module_name="ai_navigation")

# 获取恢复状态
status = failsafe.get_recovery_status()
# {
#   "failsafe_mode": True,
#   "has_recovery": True,
#   "recovery_info": {...}
# }
```

---

### 7. 重启恢复引导 (restart_recovery_flow.py)

#### 功能
- 检查恢复上下文
- 提示用户是否恢复
- 执行恢复流程
- 重置系统
- 记录恢复日志

#### 接口
```python
from task_engine import RestartRecoveryFlow

recovery = RestartRecoveryFlow(
    state_manager=state_mgr,
    cache_manager=cache_mgr,
    failsafe_trigger=failsafe
)

# 检查恢复上下文
has_context = recovery.check_restart_context()

# 获取恢复上下文
context = recovery.get_restart_context()

# 执行恢复流程
success = recovery.run_recovery_flow()

# 或者手动执行
context = recovery.get_restart_context()
if recovery.prompt_user_for_recovery(context):
    recovery.execute_recovery(context)
else:
    recovery.reset_to_fresh_state()
```

---

### 8. 任务清理器 (task_cleanup.py)

#### 功能
- 延迟清理（2分钟）
- 超时检测（60分钟）
- 日志清理（保留30天）

#### 接口
```python
from task_engine import TaskCleanup

cleanup = TaskCleanup(task_engine)

# 启动清理线程
cleanup.start()

# 计划清理
cleanup.schedule_cleanup("task_id", immediate=False)

# 停止
cleanup.stop()
```

---

### 9. 报告上传器 (task_report_uploader.py)

#### 功能
- 执行记录上传
- 重试机制
- 本地保存

#### 接口
```python
from task_engine import get_report_uploader

uploader = get_report_uploader()

success = uploader.upload_task_report({
    "task_id": "hospital_visit",
    "user_id": "user_001",
    "graph_name": "医院就诊流程",
    "execution_path": ["plan_route", "goto_department"],
    "failed_nodes": [],
    "duration": 1800,
    "status": "completed"
})

# 重试待上传
retry_count = uploader.retry_pending_uploads()
```

---

## 🎯 完整使用流程

### 场景：用户要去医院

```python
from task_engine import get_task_engine

# 1. 初始化
engine = get_task_engine()

# 2. 加载任务图
task_graph = engine.load_task_graph("task_engine/task_graphs/hospital_visit.json")

# 3. 注册任务
graph_id = engine.register_task(task_graph)

# 4. 启动任务
engine.start_task(graph_id)

# 5. 任务自动执行
# - plan_route 节点：规划路线
# - confirm_materials 节点：确认证件
# - start_navigation 节点：开始导航
# ...

# 6. 用户说："我想先去洗手间"
# - 注册插入任务
# - 暂停主任务
# - 执行插入任务
# - 完成后恢复主任务

# 7. 如果出现故障
# - failsafe_trigger 检测并记录
# - 系统重启后
# - restart_recovery_flow 引导恢复

# 8. 任务完成
# - 上传执行报告
# - 清理缓存
```

---

## 📋 系统限制

| 限制类型 | 数值 |
|---------|------|
| 主任务链 | 1个active |
| 插入任务链 | 2个（进行中+暂停） |
| 缓存大小 | 1000条（可配置） |
| 心跳超时 | 10秒 |
| 任务超时 | 60分钟 |
| 清理延迟 | 2分钟 |
| 日志保留 | 30天 |
| 嵌套插入 | 不支持 |

---

## 🔄 完整恢复流程

```
[主任务执行中]
    ↓
[异常/卡死] → failsafe_trigger.monitor_heartbeat() 检测
    ↓
trigger_failsafe() → 保存状态 + 记录故障
    ↓
[系统重启]
    ↓
restart_recovery_flow.check_restart_context()
    ↓
prompt_user_for_recovery()
    ↓
用户选择
    ↓ YES                  ↓ NO
execute_recovery()      reset_to_fresh_state()
    ↓                         ↓
恢复任务状态                清除所有状态
恢复缓存快照                重新开始
继续执行                    开始新任务
```

---

## 📊 测试覆盖

- ✅ 模块导入测试
- ✅ 任务图加载测试
- ✅ 节点执行测试
- ✅ 状态管理测试
- ✅ 缓存管理测试
- ✅ 插入任务测试
- ✅ 故障安全测试
- ✅ 恢复流程测试

---

**Luna Badge v1.4 完整功能文档** ✅

