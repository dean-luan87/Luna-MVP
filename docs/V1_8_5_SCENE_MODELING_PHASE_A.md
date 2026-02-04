# v1.8.5 · Phase A

## 场景建模层 × 中台读取边界 × 工程任务清单

**目标**：
在不破坏 v1.8.4 冻结行为的前提下，引入 Scene Modeling Layer 的数据结构、接口与读取边界，为后续 Phase B/C 留好接口。

---

## 一、SceneState × 各中台「读取字段对照表」

**这一部分的作用只有一个：防止 Scene 层被滥用成"隐形决策层"。**

**原则**：Scene 只提供事实，中台自己判断。

---

### 1️⃣ Risk 中台（v1.8.5）

#### 允许读取（只读）

| Scene 字段 | 用途 | 说明 |
|-----------|------|------|
| `scene_type` | 风险类型参考 | 湖畔 / 道路 / 商场 |
| `static_model.structures` | hazard 修正 | 是否存在护栏、台阶 |
| `dynamic_model.temporary_events` | dynamic active | 施工 / 拥堵 |
| `dynamic_model.crowd_density` | 弱权重修正 | 不直接触发 |
| `confidence` | 置信度降权 | 低置信度只能降权 |

#### 明确禁止

- ❌ 读取 `scene_memory`
- ❌ 读取 `visited_count`
- ❌ Scene 直接返回 `risk_level` / `should_warn`

---

### 2️⃣ 任务链中台（Task Chain）

#### 允许读取

| Scene 字段 | 用途 |
|-----------|------|
| `scene_type` | 任务适配（是否适合当前任务） |
| `dynamic_model.scene_phase` | 时段判断 |
| `scene_memory.useful_places` | 任务补全（早餐 / 商店） |
| `scene_memory.observed_risks` | 任务注意点 |

#### 禁止

- ❌ 读取 `static_model.structures.geometry`
- ❌ 直接控制任务流转（只能建议）

---

### 3️⃣ 情绪计算中台（Emotion）

#### 允许读取

| Scene 字段 | 用途 |
|-----------|------|
| `scene_type` | 情绪基调（室外 / 室内） |
| `scene_memory.visited_count` | 熟悉度 |
| `dynamic_model.crowd_density` | 压迫 / 放松 |
| `dynamic_model.traffic_level` | 紧张度 |

#### 禁止

- ❌ 读取具体结构几何
- ❌ 推断风险结论

---

## 二、v1.8.5 Phase A 工程任务清单（Cursor 级）

**注意**：
- Phase A = 只有 Schema + Stub + Debug
- ❌ 不接地图
- ❌ 不接 GPS
- ❌ 不改 Risk 行为

---

### 🧩 Task A1：定义 SceneState Schema（核心）

**文件**：`core/scene/schema.py`

**内容**：
- `SceneState`
- `StaticScene`
- `DynamicScene`
- `SceneMemory`

**要求**：
- 全字段 Optional
- dataclass / pydantic 均可
- 明确字段注释（来源 / 生命周期）

---

### 🧩 Task A2：Scene Registry（最小 Stub）

**文件**：`core/scene/scene_registry.py`

**功能**：
- `get_current_scene() -> SceneState`
- 暂时返回空结构 + scene_id
- 支持未来替换实现

---

### 🧩 Task A3：Scene Debug Snapshot 扩展

**修改**：`RiskDebugSnapshot`

**新增字段（只读）**：

```json
"scene": {
  "scene_id": "...",
  "scene_type": "...",
  "confidence": 0.7
}
```

**要求**：
- 不参与任何判断
- 仅用于可观测性

---

### 🧩 Task A4：中台读取接口封装（防越权）

**文件**：`core/scene/scene_read_adapter.py`

**示例**：

```python
get_scene_for_risk(scene_state)
get_scene_for_task(scene_state)
get_scene_for_emotion(scene_state)
```

**目的**：
- 显式限制每个中台能读什么
- 防止直接滥读 SceneState

---

### 🧩 Task A5：文档与冻结标记

**文档**：`docs/V1_8_5_SCENE_MODELING_PHASE_A.md`（本文档）

**内容**：
- Phase A 范围
- 不做清单
- 与 v1.8.4 的边界说明

**状态**：✅ 已完成

---

## 三、Phase A 完成后的系统状态（你应该看到的）

- ✅ 系统行为 100% 与 v1.8.4 一致
- ✅ Risk Snapshot 中可看到 `scene_id` / `scene_type`
- ✅ Task / Emotion 可读取 Scene（但还没有真实数据）
- ✅ 所有实现点都可被后续替换

**这一步的价值在于：先把"接口权力"定死，再慢慢填数据。**

---

## 四、Phase A 实现状态

**实现时间**：2024-12-31  
**状态**：✅ **已完成**

### 已实现内容

- ✅ **A1: Schema 定义** - `core/scene/schema.py`
  - SceneState / StaticScene / DynamicScene / SceneMemory
  - 所有字段 Optional，明确注释

- ✅ **A2: Scene Registry Stub** - `core/scene/scene_registry.py`
  - 最小实现，返回空结构 + scene_id
  - 可被后续实现整体替换

- ✅ **A3: Scene Read Adapter** - `core/scene/scene_read_adapter.py`
  - get_scene_for_risk() / get_scene_for_task() / get_scene_for_emotion()
  - 显式限制各中台读取权限

- ✅ **A4: RiskDebugSnapshot 扩展** - `core/risk/risk_debug.py`
  - 新增 scene 字段（只读，不参与判断）
  - RiskAdvisoryService 集成场景信息

- ✅ **A5: 文档** - `docs/V1_8_5_SCENE_MODELING_PHASE_A.md`
  - Phase A 范围、不做清单、边界说明

### 验收结果

- ✅ **行为一致性**：与 v1.8.4 输出完全一致（Risk/Task/Emotion 不变）
- ✅ **可观测性**：RiskDebugSnapshot 中出现 scene（即便为空）
- ✅ **防越权**：中台无直接读取 SceneState 的路径（必须通过 Adapter）
- ✅ **可替换性**：SceneRegistry 可被未来实现整体替换
- ✅ **无真实依赖**：不接地图/GPS/视觉

---

## 四、你现在可以直接给 Cursor 的指令（最终版）

**开始 v1.8.5 Phase A**：

1. 新增 Scene Modeling Layer（仅 Schema + Registry Stub）
2. 定义 SceneState / StaticScene / DynamicScene / SceneMemory 数据结构
3. 扩展 RiskDebugSnapshot，增加只读 scene 摘要
4. 为 Risk / Task / Emotion 提供受限读取 Adapter
5. 不接地图、不接 GPS、不改 risk 行为、不新增决策逻辑

**目标**：完成 v1.8.5 Phase A 的结构性准备。

---

## 五、与 v1.8.4 的边界说明

### 冻结保证

- ✅ **Risk 行为逻辑**：完全不变
- ✅ **决策优先级**：完全不变
- ✅ **触发判定**：完全不变
- ✅ **测试框架**：完全不变

### Phase A 新增内容

- ✅ **数据结构**：SceneState / StaticScene / DynamicScene / SceneMemory
- ✅ **接口 Stub**：SceneRegistry（返回空结构）
- ✅ **读取边界**：Scene Read Adapter（限制各中台读取权限）
- ✅ **调试扩展**：RiskDebugSnapshot 增加 scene 字段（只读）

### 明确不做（Phase A）

- ❌ 不接地图数据
- ❌ 不接 GPS 数据
- ❌ 不修改 Risk 计算逻辑
- ❌ 不新增决策 action
- ❌ 不触发任何播报

---

## 六、后续阶段预览

### Phase B（计划中）

- 离线地图 + GPS 接入
- 基础 Scene 切换
- SceneState 填充真实数据

### Phase C（计划中）

- 视觉观察补充
- SceneMemory 反写
- 长期记忆修正

---

## 📚 相关文档

- `docs/V1_8_5_SCENE_MODELING_LAYER_DESIGN.md` - v1.8.5 设计文档
- `docs/V1_8_4_FREEZE_DECLARATION.md` - v1.8.4 冻结声明

---

**文档状态**：Execution Blueprint  
**创建时间**：2024-12-31  
**维护者**：Luna Badge MVP Team

---

## 💡 重要评价

**你现在这套推进方式，不是"写功能"，而是在"冻结权力结构"。这比"早点跑起来"要难得得多。**

等 Phase A 完成，我们再进入 Phase B（离线地图 + GPS），那时候你会发现：

**所有东西都有地方接，不需要推翻任何已有设计。**

