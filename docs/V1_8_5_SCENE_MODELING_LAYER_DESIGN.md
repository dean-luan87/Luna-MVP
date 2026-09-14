# v1.8.5 设计文档

## Scene Modeling Layer（场景建模层）

**版本状态**：Design Draft  
**依赖版本**：Risk v1.8.4（已冻结）  
**设计目标**：从记忆系统中抽离"世界 / 场景"这一维度，构建一个可被多中台共用的场景建模层，用于支撑风险告知、视角导航、情绪计算与任务链，但不直接参与中台决策与执行。

---

## 1. 设计动机（Why）

在 v1.8.4 之前：
- 世界信息（地图、GPS、视觉观察）混杂在记忆或具体功能中
- 无法被 risk / 导航 / 情绪计算统一消费
- 难以进行场景级复用与长期修正

**核心问题不是"缺少世界模型"，而是：**

**缺少一个以场景为中心的、结构化的现实事实层。**

因此引入 Scene Modeling Layer（场景建模层），作为一个独立后端板块。

---

## 2. 定位与边界（What / What Not）

### 2.1 场景建模层是什么

- 是一个 **场景事实层（Scene Fact Layer）**
- 描述：
  - 我现在处于什么场景
  - 这个场景有哪些稳定事实 / 动态变化
  - 这些事实对"我"是否有历史关联

### 2.2 场景建模层不是什么（明确禁止）

- ❌ 不做决策
- ❌ 不触发告警
- ❌ 不执行任务
- ❌ 不预测行为
- ❌ 不做完整物理世界模拟（非 Google 路线）

---

## 3. 总体架构

```
┌───────────────┐
│  外部数据      │  地图 / GPS / 天气
└───────────────┘
        ↓
┌───────────────┐
│  感知输入      │  视觉 / 姿态 / 视角导航
└───────────────┘
        ↓
┌──────────────────────────────┐
│      Scene Modeling Layer     │
│  ┌────────┐ ┌────────┐ ┌────┐│
│  │ Static │ │ Dynamic│ │Mem ││
│  └────────┘ └────────┘ └────┘│
└──────────────────────────────┘
        ↓（只读）
┌───────────────┐
│ 中台决策引擎   │  Risk / Task / Emotion
└───────────────┘
        ↑（反写）
┌───────────────┐
│ 记忆 / 修正    │
└───────────────┘
```

---

## 4. 核心数据结构

### 4.1 SceneState（统一对外接口）

```json
SceneState {
  "scene_id": string,
  "scene_type": string,           // lake_side / road / mall / hospital / home
  "geo_anchor": {
    "lat": float?,
    "lng": float?,
    "area_id": string?
  },

  "static_model": StaticScene,
  "dynamic_model": DynamicScene,
  "scene_memory": SceneMemory,

  "confidence": float,             // 0~1
  "timestamp": float
}
```

---

### 4.2 StaticScene（静态场景模型）

**长期不变或变化极慢的现实结构**

```json
StaticScene {
  "terrain_type": string,          // road / slope / stairs / water
  "structures": [
    {
      "type": "guardrail | stairs | building | bridge",
      "geometry": "POINT | LINE | AREA",
      "confidence": float
    }
  ],
  "source": "offline_map | vision | manual"
}
```

**特点**：
- 生命周期长
- 可缓存
- 更新频率低

---

### 4.3 DynamicScene（动态场景模型）

**与时间、事件强相关的变化**

```json
DynamicScene {
  "traffic_level": "low | medium | high",
  "crowd_density": "sparse | normal | dense",
  "temporary_events": [
    "construction",
    "road_block",
    "market"
  ],
  "scene_phase": "morning_peak | daytime | night",
  "expires_at": float?
}
```

**特点**：
- 强时效
- 允许失效
- 有衰减逻辑

---

### 4.4 SceneMemory（场景绑定记忆）

**"这个场景对我来说意味着什么"**

```json
SceneMemory {
  "visited_count": int,
  "last_visited": float,
  "observed_risks": [
    "heavy_traffic",
    "confusing_path"
  ],
  "useful_places": [
    {
      "type": "breakfast_shop",
      "confidence": float
    }
  ],
  "notes": string?
}
```

**说明**：
- 不是全局记忆
- 强绑定 scene_id
- 可反向修正 Static / Dynamic

---

## 5. 地图与 GPS 策略（工程现实解）

### 5.1 地图定位

- **离线地图为主**
  - 场景级精度
  - 用于 scene_id / scene_type 判定
- **实时地图为辅（可选）**
  - 仅在：
    - 离线缺失
    - 用户明确导航
    - 特殊任务

### 5.2 GPS 的角色

- 场景锚点
- 场景切换触发器
- SceneMemory 的索引 key

---

## 6. 与各中台的关系（只读原则）

### 6.1 Risk（v1.8.5）

- SceneState → 提供事实
- Risk Adapter → 转换为弱证据
- ❌ Scene 不触发 risk

### 6.2 任务链（Task Chain）

- SceneState → 提供：
  - 是否适合当前任务
  - 是否存在辅助信息（早餐店、车多等）
- ❌ Scene 不决定任务流转

### 6.3 情绪计算

- Scene 作为情绪上下文
- 例如：
  - 熟悉场景 → 安全感
  - 拥挤场景 → 压迫感

---

## 7. 生命周期与数据流

1. **进入新地理区域**
   → 创建 / 匹配 Scene

2. **视觉 / GPS / 外部数据更新**
   → 更新 Static / Dynamic

3. **中台执行任务 / 风险告知**
   → 反写 SceneMemory

4. **时间衰减**
   → DynamicScene 自动失效

---

## 8. v1.8.5 实施阶段划分（不一次做完）

### Phase A（当前）

- Schema 定义
- Stub 接口
- Debug Snapshot 扩展

### Phase B

- 离线地图 + GPS 接入
- 基础 Scene 切换

### Phase C

- 视觉观察补充
- SceneMemory 反写

---

## 9. 明确不做清单（防止架构失控）

- ❌ 不做强预测
- ❌ 不做自动路径规划
- ❌ 不做全量世界重建
- ❌ 不在 Scene 层做策略判断

---

## 10. 总结（一句话）

**Scene Modeling Layer 不是为了"理解整个世界"，而是为了"让系统知道自己身处哪个场景，以及这个场景对我意味着什么"。**

---

## 📚 相关文档

- `docs/V1_8_4_FREEZE_DECLARATION.md` - v1.8.4 冻结声明
- `docs/V1_8_4_RISK_ADVISORY_SYSTEM_DESIGN.md` - Risk 系统设计

---

**文档状态**：Design Draft  
**创建时间**：2024-12-31  
**维护者**：Luna Badge MVP Team


