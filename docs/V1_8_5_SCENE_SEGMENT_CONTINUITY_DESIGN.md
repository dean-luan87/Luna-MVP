# v1.8.5 · Phase B

## Scene Segment 连续性 × Environment Context 设计补充

**文档状态**：v1.8.5 Phase B – Structural Constraint  
**版本**：v1.0  
**生效时间**：Phase B 实施阶段

---

**本章节用于补充 v1.8.5 Phase B 中 Scene 建模的最小工程单位、连续性规则，以及时间/天气等环境变量的作用边界。**  
**本章节属于结构性设计约束，不涉及具体算法精度与实现优化。**

---

## 1. Scene 的工程化最小单位定义

### 1.1 定义结论

**Scene 的最小工程单位不是"位置点"，也不是"建筑"，而是一个「稳定场景段（Scene Segment）」。**

**Scene Segment**  
指在一段时间内，系统在"风险评估、通行判断、任务约束"等关键决策前提上无需发生结构性切换的一段现实状态。

---

### 1.2 为什么不能用单一尺度定义 Scene

| 定义方式 | 问题 |
|---------|------|
| 米 / 距离 | GPS 漂移、上下坡、遮挡会导致频繁切换 |
| 建筑 / POI | 室外连续区域、道路、湖畔无法覆盖 |
| 固定区域 | 城市尺度变化过大，不具备连续性 |

**结论**：  
Scene 必须是一个 **多锚点确认的稳定段**，而不是单一空间尺度。

---

## 2. Scene Segment 的多锚点结构（Phase B 级别）

Scene Segment 在 Phase B 中由 **四类锚点**共同支撑：

### 2.1 几何锚点（Geometry Anchor）

- **来源**：GPS / 惯导 / 视觉推断
- **表示**：polyline / area（粗粒度）
- **用途**：
  - 风险距离判断
  - 通行连续性判断

**工程约束**：
- 上下坡、轻微偏移 → 不构成新 Scene
- 几何锚点变化必须 **持续且结构性** 才可能触发候选 Scene

---

### 2.2 语义锚点（Semantic Anchor）

- **来源**：离线地图 / OCR / 视觉标识
- **表示**：place_type / building / zone
- **用途**：
  - 任务适配
  - 情绪基调判断

**工程约束**：
- 语义变化 ≠ 立即切换
- 仅作为候选 Scene 的增强信号

---

### 2.3 行为锚点（Behavior Anchor）

- **来源**：用户行为模式
- **示例**：
  - 持续直行
  - 停留
  - 往返 / 犹豫

**工程约束**：
- 行为未发生结构性变化 → Scene 不应切换
- 行为是场景连续性的强稳定因子

---

### 2.4 记忆锚点（Memory Anchor）

- **来源**：Scene Memory
- **示例**：
  - 是否来过
  - 是否发生过风险
  - 是否存在任务相关点

**工程约束**：
- 记忆是 Scene 连续性的"胶水"
- 不作为切换触发条件，仅作为确认与权重修正因子

---

## 3. SceneRegistry 的连续性与切换原则

### 3.1 Active / Candidate 双 Scene 模型

在任意时刻，SceneRegistry 只维护两个 Scene：
- **Active Scene**：当前生效场景
- **Candidate Scene**：候选场景（尚未确认）

**禁止出现多候选场景并行。**

---

### 3.2 Scene 切换不是瞬时行为

Scene 切换必须满足以下条件：
1. Candidate Scene 的匹配度持续成立
2. Candidate Scene 的 confidence 连续增长
3. 满足最小稳定时间（MIN_STABLE_TIME）

**否则**：
- Candidate Scene 被视为噪声并回收
- Active Scene 不切换

---

### 3.3 置信度（confidence）的工程含义

| 状态 | 行为 |
|------|------|
| confidence 下降 | 降权，不切换 |
| confidence 低 | 表示"不确定"，不是"新场景" |
| confidence 持续高 | 允许切换 |

**铁律**：

**低置信度 ≠ 新 Scene**  
**新 Scene = 持续、结构性、稳定变化**

---

## 4. 时间 × 天气 × 环境变量（Environment Context）

### 4.1 定位结论

**时间与天气不是 Scene 切换条件，而是"环境修正因子（Environment Modifier）"。**

它们可以影响：
- 风险权重
- 通行可信度
- 任务建议倾向

**但不允许直接触发 Scene Segment 切换。**

---

### 4.2 Environment Context 建议字段

```python
EnvironmentContext:
  season        # SPRING / SUMMER / AUTUMN / WINTER
  time_of_day   # DAY / NIGHT / DUSK
  weather       # CLEAR / RAIN / SNOW / FOG
  temperature   # Optional
```

作为 `SceneInputs` 的一部分输入 `SceneRegistry`，但仅用于：
- confidence 修正
- 下游模块读取

---

### 4.3 典型影响规则（设计级）

| 条件 | 影响 |
|------|------|
| 夜晚 + 照明不足 | 风险权重 ↑，confidence ↓ |
| 雨 / 雪 | 路面 hazard ↑，通行可信度 ↓ |
| 冬季（北方） | 结冰概率 ↑，风险敏感度 ↑ |

**工程约束**：
- 以上规则只改变权重，不产生新 Scene
- SceneRegistry 不做风险判断，仅稳定提供环境状态

---

## 5. Scene × Context 连续性原则（防"1234 → 4567 跳变"）

### 5.1 注意事项不是 Scene 的属性

所有注意事项 / 风险 / 提示必须被建模为 **Context Item**，而不是 Scene 的固定字段。

Scene 变化时：
- Context relevance 连续变化
- 不允许集合式替换

---

### 5.2 Scene 切换的正确行为

- 原 Scene Context → relevance 逐步衰减
- 新 Scene Context → relevance 逐步上升
- 中间存在重叠窗口（Overlap Window）

---

## 6. Phase B 的明确边界

### Phase B 必须完成

- Scene Segment 连续性结构
- SceneRegistry 状态机
- Environment Context 的结构定义
- 文档级约束明确

### Phase B 明确不做

- 高精地图
- 3D 地形建模
- 精准气象预测
- 自动语义分割城市

---

## 7. 本章节的工程目标总结

**Phase B 的目标不是"更准地理解世界"，**  
**而是：**  
**在不确定、噪声、信息不全的现实中，保持系统状态的连续与理性。**

---

## ✅ 文档状态建议

- **标记为**：v1.8.5 Phase B – Structural Constraint
- **后续实现与调参** 不得违反本章节原则

---

## 下一步

这一步完成后，你的系统在架构层面已经具备了：
- 抵抗现实噪声的能力
- 不被 GPS / 视觉牵着走的稳定性
- 为后续 Context 演化、任务推理、情绪系统提供"平滑地基"

**下一步**：Context / 注意事项的演化机制（relevance 曲线、生命周期）


