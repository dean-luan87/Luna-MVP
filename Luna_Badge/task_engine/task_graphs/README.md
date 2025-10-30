# 任务图文件标准格式说明

## 📋 任务图JSON文件结构

所有任务图文件（`.json`）必须遵循以下标准格式，以便任务引擎正确加载和执行。

---

## 🏗️ 文件结构

### 顶层字段

```json
{
  "graph_id": "unique_task_id",      // 必需：任务链唯一标识
  "scene_type": "scene_category",     // 必需：场景类别
  "goal": "任务目标描述",              // 必需：任务目标
  "entry_trigger": "触发条件",         // 可选：触发任务的用户语句
  "target": {                         // 可选：目标信息
    "location": "目标地点",
    "service_type": "服务类型"
  },
  "nodes": [...],                     // 必需：任务节点列表
  "edges": [...],                     // 可选：节点连接关系
  "metadata": {...}                   // 可选：元数据
}
```

---

## 📦 节点（Node）结构

### 必需字段

```json
{
  "id": "node_unique_id",            // 节点唯一标识
  "type": "node_type",                // 节点类型（见下方）
  "title": "节点标题",                 // 用户可感知的任务标题
  "status": "pending"                 // 节点状态（pending/running/completed/failed）
}
```

### 可选字段

```json
{
  "expected_input": "期望输入",        // 节点期望的输入
  "output": "输出结果",               // 节点输出
  "input": "输入数据",                // 输入数据（与expected_input等价）
  "trigger": "触发条件",              // 触发条件（用于environmental_state类型）
  "fallback_action": "容错行为",       // 失败时的容错行为
  "timeout": 300,                     // 超时时间（秒）
  "config": {                         // 节点配置
    // 根据节点类型不同，配置内容不同
  }
}
```

---

## 🎯 节点类型（Node Type）

| 类型 | 说明 | 典型用途 | 配置示例 |
|------|------|----------|---------|
| `interaction` | 用户交互 | 询问用户、获取确认 | `{"question": "问题", "options": ["选项"]}` |
| `navigation` | 导航任务 | 规划路线、执行导航 | `{"destination": "地点", "transport_mode": "walking"}` |
| `observation` | 观察识别 | OCR识别、视觉检测 | `{"type": "ocr", "target": "signboard"}` |
| `condition_check` | 条件检查 | 检查前置条件 | `{"condition": "条件", "required_items": []}` |
| `external_call` | 外部服务 | 调用外部API/服务 | `{"service": "service_name"}` |
| `memory_action` | 记忆操作 | 保存/读取记忆 | `{"action": "save", "memory_type": "type"}` |
| `environmental_state` | 环境状态 | 监听环境变化 | `{"trigger": "触发条件"}` |

---

## 🔗 边（Edge）结构

```json
{
  "from": "source_node_id",          // 源节点ID
  "to": "target_node_id"             // 目标节点ID
}
```

**说明：**
- 如果未提供`edges`字段，系统将按节点顺序自动连接
- 支持条件分支（通过`condition`字段，未来扩展）

---

## 📊 元数据（Metadata）

```json
{
  "estimated_duration": 120,         // 预计时长（分钟）
  "complexity": "high",              // 复杂度：low/medium/high
  "user_interaction_level": "high",  // 用户交互级别：low/medium/high
  "ai_assistance_level": "high",     // AI辅助级别：low/medium/high
  "insertable_tasks": ["toilet", "snack"],  // 可插入的任务类型
  "version": "1.0"                   // 版本号
}
```

---

## 📝 字段说明

### 核心字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `graph_id` | string | ✅ | 任务链唯一标识 |
| `scene_type` | string | ✅ | 场景类别：hospital/government/retail/transport等 |
| `goal` | string | ✅ | 任务目标描述 |
| `entry_trigger` | string | ❌ | 触发任务的用户语句或事件 |
| `target` | object | ❌ | 目标信息（地点、服务类型等） |
| `nodes` | array | ✅ | 任务节点列表（至少1个） |
| `edges` | array | ❌ | 节点连接关系（可选，默认顺序连接） |
| `metadata` | object | ❌ | 元数据信息 |

### 节点字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `id` | string | ✅ | 节点唯一标识 |
| `type` | string | ✅ | 节点类型 |
| `title` | string | ✅ | 节点标题 |
| `status` | string | ✅ | 节点状态 |
| `expected_input` | string | ❌ | 期望输入 |
| `output` | string | ❌ | 输出结果 |
| `input` | string | ❌ | 输入数据（与expected_input等价） |
| `trigger` | string | ❌ | 触发条件 |
| `fallback_action` | string | ❌ | 容错行为 |
| `timeout` | number | ❌ | 超时时间（秒） |
| `config` | object | ❌ | 节点配置 |

---

## 📋 场景类型（Scene Type）

| 场景类型 | 说明 | 示例 |
|----------|------|------|
| `hospital` | 医院场景 | 挂号、就诊、取药 |
| `government` | 政务服务 | 办证、办事 |
| `retail` | 零售购物 | 超市、商场 |
| `transport` | 交通出行 | 公交、地铁、步行 |
| `custom` | 自定义场景 | 用户自定义任务 |

---

## 🎯 使用示例

### 完整示例

参考 `hospital_visit.json`、`government_service.json`、`shopping_mall.json`

### 创建新任务图

1. 复制 `task_graph_template.json`
2. 修改 `graph_id`、`scene_type`、`goal`
3. 添加/修改节点列表
4. 定义节点连接关系（edges）
5. 填写元数据

---

## ✅ 验证检查清单

创建任务图文件后，请检查：

- [ ] `graph_id` 唯一且有意义
- [ ] `scene_type` 符合标准类型
- [ ] `goal` 清晰描述任务目标
- [ ] `nodes` 至少包含1个节点
- [ ] 每个节点都有 `id`、`type`、`title`、`status`
- [ ] 节点类型符合支持的类型
- [ ] `edges` 中的节点ID在 `nodes` 中存在
- [ ] `timeout` 值合理（不宜过大）
- [ ] `metadata` 包含必要的元信息

---

## 🔧 工具支持

使用 `task_graph_loader.py` 可以：
- ✅ 自动校验字段完整性
- ✅ 加载JSON文件为TaskGraph对象
- ✅ 从API加载（预留接口）

---

## 📚 参考文件

- `hospital_visit.json` - 医院就诊流程（完整示例）
- `government_service.json` - 政务服务流程
- `shopping_mall.json` - 购物流程
- `task_graph_template.json` - 模板文件

---

**遵循此标准格式，可确保任务图文件与任务引擎完美兼容！** ✅
