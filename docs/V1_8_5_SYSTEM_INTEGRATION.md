# v1.8.5 系统收敛与工程接入说明

（World / Scene / Memory / Library × Task × 中台）

---

## 一、v1.8.5 在整个系统中的"真实位置"

### 结论先行（一句话）

**v1.8.5 不是一个"决策系统"，而是一个"长期可持续的世界上下文生成器"。**

它的职责不是"告诉系统该怎么做"，而是：
- 让系统知道自己身处什么样的世界
- 让系统记住这个世界对用户意味着什么
- 让系统在任务执行时有连续、可靠的上下文

---

## 二、三大板块的最终定位（非常关键）

### 1️⃣ 世界模型（World / Scene / Map）

**职责**
- 建模"世界是什么样的"
- 提供场景连续性
- 提供客观约束（地形、时间、天气、风险）

**不做**
- ❌ 不直接下决策
- ❌ 不直接驱动播报
- ❌ 不执行任务

**输出给谁**
- → 任务链
- → 中台管理引擎（只读）

---

### 2️⃣ 记忆系统（Memory / Library）

**职责**
- Memory：记录主观体验 / 偏好 / 不适
- Library：记录慢确认事实（可退潮）

**不做**
- ❌ 不切 Scene
- ❌ 不直接影响即时决策
- ❌ 不覆盖世界模型

**输出给谁**
- → 世界模型（作为 bias / 修正）
- → 任务链（作为个性化权重）

---

### 3️⃣ 任务链（Task Chain）

**职责**
- 在给定上下文中选择"合适的行动"
- 消费 Scene / Map / Memory / Risk
- 输出行动计划（走哪、避开什么）

**不做**
- ❌ 不修改世界模型
- ❌ 不写记忆
- ❌ 不纠正事实

---

## 三、v1.8.5 如何接入"现在的工程"并真正生效

### 关键原则

**v1.8.5 以"被动输入 + 主动输出"的方式接入，不侵入原有决策链。**

---

### 1️⃣ 世界模型的输入方式（来自哪里）

#### 输入 1：中台感知结果（每帧）

```python
PerceptionFrame = {
    "position_state": PositionState,
    "visual_objects": [...],
    "visual_landmarks": [...],
    "motion_state": {...},
    "timestamp": float
}
```

- **来源**：视觉模型 / IMU / GPS
- **用途**：
  - `SceneRegistry.update()`
  - 风险计算
  - 冻结 gate 判断

---

#### 输入 2：任务上下文（事件型）

```python
TaskContextEvent = {
    "task_id": "...",
    "task_type": "navigation | purchase | wait | search",
    "goal": {...},
    "timestamp": float
}
```

- **来源**：任务链 / 中台调度
- **用途**：
  - Scene 语义强化
  - Memory 唤醒（相关体验）

---

#### 输入 3：用户反馈（结构化）

```python
UserReportEvent = {
    "user_id": "...",
    "report_type": "DISCOMFORT | FACT_CONFIRM | ...",
    "claim_type": "...",
    "tags": [...],
    "intensity": float,
    "timestamp": float
}
```

- **来源**：语言模型 / UI
- **用途**：
  - `MemoryRegistry`
  - `FactCandidatePool`

---

## 四、世界模型的"加工方式"（内部）

### 处理顺序（不可乱）

```
PositionState
   ↓
[Gate 判断]  ——> freeze / allow
   ↓
SceneRegistry.update()
   ↓
MapRegistry.lookup()
   ↓
MemoryRegistry.bias()
   ↓
RiskAdvisoryService.tick()
```

**关键点**
- Gate（冻结）优先级最高
- Scene 是唯一切换入口
- Memory / Library 永远不能越权

---

## 五、世界模型的输出方式（对外）

### 1️⃣ 输出给任务链（核心）

```python
ContextBundle = {
    "scene": Scene,
    "map_hint": MapHint,
    "memory_bias": ExperienceBias,
    "risk_bias": RiskBias,
    "emotional_context": Optional[EmotionalContext]  # Phase D Lite
}
```

**特点**
- 全部是软信号
- 全部可缺省
- 全部只读

---

### 2️⃣ 输出给中台管理引擎（只读）

```python
WorldSnapshot = {
    "scene_id": "...",
    "scene_semantics": [...],
    "position_stable": bool,
    "risk_level": float,
    "memory_summary": {...},
    "library_active_items": [...]
}
```

**用途**
- 调度策略
- Debug
- 监控与回放

---

## 六、世界模型 ↔ 中台管理引擎 的互动边界

### 世界模型能影响什么
- ✅ 任务选择偏好
- ✅ 路径规划权重
- ✅ 风险规避策略
- ✅ 个性化体验

### 世界模型不能影响什么
- ❌ 中台的最终裁决权
- ❌ 系统级安全规则
- ❌ 硬实时行为（如紧急刹停）

---

## 七、前端模型需要输出什么（现在就要定义）

### 1️⃣ 视觉模型（必须）

```python
VisionOutput = {
    "objects": [
        {"type": "person", "bbox": ..., "confidence": 0.92},
        {"type": "water_edge", "confidence": 0.88}
    ],
    "landmarks": [
        {"type": "crosswalk", "confidence": 0.90}
    ],
    "visual_quality": {
        "blur": 0.1,
        "occlusion": 0.3,
        "lighting": "low"
    }
}
```

**要求**
- 要有置信度
- 要有质量评估（为 drift 判定）

---

### 2️⃣ 语言模型（一期只做结构化输出）

```python
LLMOutput = {
    "intent": "user_report",
    "report_type": "DISCOMFORT",
    "claim_type": None,
    "tags": ["slippery"],
    "intensity": 0.8,
    "raw_text": "这条路太滑了"
}
```

**要求**
- 不直接写系统
- 必须走 `UserReportRouter`
- 二期再强化解析

---

## 八、外部数据（地图 / 天气 / 时间）

### 地图（v1.8.5）
- 离线地图为主
- 提供：
  - `road_type`
  - `slope`
  - `lighting_at_night`
- 不实时更新

### 天气 / 时间

```python
EnvironmentContext = {
    "season": "winter",
    "weather": "snow",
    "time_of_day": "night"
}
```

- 作为 `MapHint` 的修正因子
- 不直接切 Scene
- 不写事实

---

## 九、为什么这样设计是"干净的"

1. **世界模型不争权**
   - → 不和中台、任务链打架

2. **信息单向流动**
   - → 感知 → 世界 → 任务
   - → 决策结果只写 Memory（体验）

3. **所有高风险输入都有 Gate**
   - → drift / relocalization / rate limit / TTL

4. **二期、三期不会推翻一切**
   - → 只增强输入解析和权重计算

---

## 十、v1.8.5 最终状态总结（给自己看的）

**v1.8.5 是一个"不会自毁"的世界上下文系统。**

它现在：
- 不聪明，但稳定
- 不炫技，但可演化
- 不抢权，但影响深远

**这是一个长期产品正确的中间态。**

---

## 附录：工程接入检查清单

### 输入接口
- [ ] `PerceptionFrame` 每帧输入到 `SceneRegistry.update()`
- [ ] `PositionState` 包含 `drift_suspected` / `relocalizing` 字段
- [ ] `UserReportEvent` 通过 `UserReportRouter` 路由
- [ ] `TaskContextEvent` 用于 Scene 语义强化

### 输出接口
- [ ] `ContextBundle` 提供给 `TaskPlanner.choose_path()`
- [ ] `WorldSnapshot` 提供给中台管理引擎（只读）
- [ ] `RiskBias` 通过 `RiskAdvisoryService.get_current_risk_bias()` 获取

### 护栏检查
- [ ] `should_freeze_world_writes()` 在所有写入点生效
- [ ] `RateLimiter` 在 `UserReportRouter` 中生效
- [ ] `EmotionalSignal` 默认关闭（`ENABLE_EMOTION_INFLUENCE = False`）

### 数据流验证
- [ ] Scene 切换只通过 `SceneRegistry.update()`
- [ ] Memory 写入只通过 `MemoryRegistry.update()`
- [ ] Library 消费只通过 `LibraryRegistry.update()`
- [ ] 任务链不直接修改世界模型

---

## 下一步（等你确认）

你可以下一步做三选一（不急）：
1. 把这套整理成 **对外架构白皮书**
2. 设计 **二期语言/情感的解析路线**
3. 直接讨论 **商业化/产品形态如何用这套能力**

你只要说一句："下一步做 X"，我继续。


