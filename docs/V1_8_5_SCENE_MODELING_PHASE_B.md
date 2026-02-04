# v1.8.5 · Phase B

## Scene Modeling × GPS × Map（最小可控实现）

**Phase B 目标一句话**：
在不引入实时地图、不抬高成本、不破坏 v1.8.4/Phase A 冻结行为的前提下，让"场景"第一次拥有真实世界锚点，并具备连续性与可演化性。

---

## 📋 核心设计文档

**本实施指南基于以下核心设计文档**：

👉 **核心设计约束文档**：  
[`V1_8_5_WORLD_CONTEXT_MODELING.md`](./V1_8_5_WORLD_CONTEXT_MODELING.md)

**该文档定义了 v1.8.5 世界场景建模与演化系统的所有约束，**  
**后续任何实现不得违反该文档中的任何原则。**

---

## 一、Phase B 的定位（先把边界定死）

### Phase B 做什么

- ✅ 引入 GPS / 地图锚点（弱依赖）
- ✅ 建立**场景最小工程单位**（Scene Segment）
- ✅ 让场景具备**连续性、置信度、渐变切换**
- ✅ 为 Risk / Task / Emotion 提供**稳定、不过激的世界上下文**

### Phase B 不做什么

- ❌ 不做实时高精地图
- ❌ 不做 3D 地形建模
- ❌ 不做自动语义切分城市
- ❌ 不把 Scene 变成决策层

**结论**：Phase B 是"世界锚定 + 连续性机制"，不是"世界理解"。

---

## 二、Scene 的工程化最小单位（正式写入 Phase B）

这是核心问题的正式定义。

### ✅ Scene Segment（场景段）——Phase B 的最小单位

**Scene Segment = 一段在"决策约束上保持一致"的现实片段**

**它不是**：
- 一个 GPS 点
- 一个建筑
- 一个固定半径

**它是一个多锚点联合确认的稳定段。**

---

### Scene Segment 的 4 个工程锚点（并行）

#### 1️⃣ 几何锚点（L1）

- **来源**：GPS / 惯导 / 视觉推断
- **表示**：polyline / area
- **用途**：
  - Risk 距离判断
  - 通行性判断

👉 **上下坡 / 抖动 → 不会切段**

---

#### 2️⃣ 语义锚点（L2）

- **来源**：离线地图 / OCR / 视觉标识
- **表示**：place_type / building_id / zone
- **用途**：
  - Task 适配
  - 情绪基调

👉 **不是精确定位，是"这是哪一类地方"**

---

#### 3️⃣ 行为锚点（L3）

- **来源**：用户行为稳定性
- **示例**：
  - 一直直行
  - 停留
  - 往返

👉 **行为未变 → 场景不该跳**

---

#### 4️⃣ 记忆锚点（L4）

- **来源**：Scene Memory
- **示例**：
  - 来过
  - 发生过风险
  - 有任务相关点

👉 **记忆是场景连续性的"胶水"**

---

## 三、Phase B 如何解决"1234 → 4567 跳变"问题

### 核心原则（非常重要）

**注意事项不是 Scene 的属性，而是"上下文状态（Context State）"**

---

### Context Item（工程级定义）

```python
ContextItem:
  id: str
  source_scene_id: str
  relevance: float        # 0.0 ~ 1.0
  confidence: float
  decay_rate: float
  last_update_ts: float
```

**工程含义**：
- 场景切换 ≠ 清空
- `relevance` 是连续函数
- Scene 变化只改变 `relevance` 的演化方向

---

### Phase B 的平滑切换机制（落地版）

#### 1️⃣ Scene Overlap Window（场景重叠窗口）

**当前**:
```
Active Scene A (confidence 0.75)
Candidate Scene B (confidence 0.35)
```

**此时**：
- A 的 Context → `relevance` 逐步下降
- B 的 Context → `relevance` 逐步上升
- 系统对外表现 = 两者叠加

---

#### 2️⃣ Context 三态生命周期（必须进 Phase B）

| 状态 | 行为 |
|------|------|
| ACTIVE | 高权重，直接影响提示 |
| PASSIVE | 低权重，仅作背景 |
| ARCHIVED | 不影响，但不删除 |

**切换 = ACTIVE → PASSIVE → ARCHIVED**  
**而不是 delete。**

---

#### 3️⃣ Scene Confidence 的真正作用

- `confidence ↓` → 降权，不切换
- `confidence` 连续低于阈值 → 才允许 Scene Segment 退出

👉 **这正是遮挡 / GPS 漂移的解法。**

---

## 四、地图与 GPS：现实可行方案（重点）

### ✅ Phase B 地图策略（推荐）

#### 1️⃣ 离线地图为主（强烈建议）

- **OSM / 自建切片**
- **覆盖**：
  - 道路
  - 水体
  - 建筑轮廓
- **只做语义锚点，不做导航**

#### 2️⃣ GPS 作为弱锚点

- **只用于**：
  - 判断"是否可能进入新区域"
- **绝不直接切 Scene**

#### 3️⃣ 所有地图/GPS → SceneRegistry

**中台不直接碰地图/GPS。**

---

### 成本现实

- **离线地图**：一次性成本
- **实时地图**：
  - 不仅是钱
  - 还是架构锁死风险

👉 **Phase B 绝对不值得上实时地图。**

---

## 五、SceneRegistry 状态机（工程级定义）

### 定位一句话

**SceneRegistry 不是"世界理解"，而是世界稳定性管理器。**  
**它负责：什么时候该认为世界变了，什么时候不该。**

---

### 1️⃣ Scene Segment 的工程定义（再次定锚）

**Scene Segment = 在一段时间内，决策前提保持一致的现实段**

**它不是**：
- 一个 GPS 点
- 一个固定半径
- 一个视觉帧

**它是一个稳定段（Stable Segment），由多锚点共同支撑。**

---

### 2️⃣ SceneRegistry 的核心状态

**SceneRegistry 在任意时刻，只维护两个 Scene**：

- **Active Scene**（当前生效）
- **Candidate Scene**（候选，尚未确认）

**不存在第三个。**

---

### 3️⃣ Scene 状态结构（最小必需字段）

```python
SceneSegment:
  scene_id: str
  anchors:
    geometry_anchor      # polyline / area（粗）
    semantic_anchor      # place_type / building / zone
    behavior_anchor      # 行为稳定性（停/走/往返）
    memory_anchor        # 过往记忆摘要
  confidence: float      # 0.0 ~ 1.0
  first_seen_ts: float
  last_confirmed_ts: float
  lifecycle_state: ACTIVE | CANDIDATE | FADING
```

---

### 4️⃣ 状态机主流程（核心逻辑）

#### 🟢 初始状态

```
Active Scene = None
→ 第一段稳定输入 → 创建 Active Scene（confidence=0.3）
```

#### 🟢 正常运行（无明显变化）

```
新输入与 Active Scene 锚点一致
→ Active.confidence += small_gain
→ Candidate = None
```

#### 🟡 发现"可能的新场景"

**条件（满足其一即可）**：
- `semantic_anchor` 发生类别变化（室外→室内）
- `geometry_anchor` 连续偏离阈值
- 行为模式发生结构性变化（直行→反复停走）

**此时**：
```
Candidate Scene = 新建（confidence=0.2）
Active Scene 仍然保持
```

⚠️ **重要**：此时不切换，只是进入 overlap。

#### 🟠 重叠窗口（Scene Overlap Window）

```
Active.confidence   ↓（缓慢）
Candidate.confidence ↑（缓慢）

• 两者同时存在
• Context / 注意事项开始权重演化（不是替换）
```

#### 🔵 确认切换

**满足条件**：
- `Candidate.confidence ≥ SWITCH_THRESHOLD`（如 0.7）
- 且持续 `≥ MIN_STABLE_TIME`（如 5s）

**执行**：
```
Active → FADING
Candidate → ACTIVE
Candidate 清空
```

#### 🔴 回滚（误判）

**若**：
- `Candidate.confidence` 长期上不去
- 或外部数据冲突

**执行**：
```
Candidate 丢弃
Active.confidence 回升
```

---

### 5️⃣ 上下坡 / 遮挡 / GPS 漂移的解法

**在这个状态机里**：
- **遮挡 / GPS 抖动** → 只影响 confidence → 不会直接触发 Candidate
- **上下坡** → geometry_anchor 连续 → 仍是同一 Scene

**原则写死**：

**低置信度 ≠ 新场景**  
**新场景 = 持续一致的"结构性变化"**

---

## 六、Phase B 工程任务清单（Cursor 可拆）

### 🧩 B1. SceneSegment 数据结构

**文件**：`core/scene/scene_segment.py`

**内容**：
- `SceneSegment` dataclass
- `Anchor` 结构（先用 dict / enum 占位）

---

### 🧩 B2. SceneRegistry v1（核心）

**文件**：`core/scene/scene_registry.py`

**接口最小集**：

```python
class SceneRegistry:
    def update(self, inputs: SceneInputs) -> SceneState
    def get_active_scene(self) -> SceneSegment
    def get_candidate_scene(self) -> Optional[SceneSegment]
```

**内部只做**：
- confidence 演化
- Active / Candidate 管理
- 切换判定

**❌ 不做**：
- 风险判断
- 任务决策
- 播报

---

### 🧩 B3. SceneInputs（输入统一封装）

**文件**：`core/scene/scene_inputs.py`

**示例字段**：

```python
SceneInputs:
  geometry_hint
  semantic_hint
  behavior_hint
  timestamp
```

**后续 GPS / Map / Vision 都只喂 SceneInputs。**

---

### 🧩 B4. Debug Snapshot 扩展

**在 RiskDebugSnapshot / SceneDebugSnapshot 中增加**：

```json
"scene_registry": {
  "active_scene_id": "...",
  "active_confidence": 0.82,
  "candidate_scene_id": "...",
  "candidate_confidence": 0.41
}
```

**只读，不参与决策。**

---

### 🧩 B5. 文档补充（必须）

**文档**：`docs/V1_8_5_SCENE_MODELING_PHASE_B.md`（本文档）

**新增章节**：
1. Scene Segment 定义与连续性原则
2. SceneRegistry 状态机与误判回滚机制

---

## 七、Environment Context（时间 × 天气）与 Scene 的关系

### 1️⃣ 时间 & 天气在系统中的"正确身份"

**时间 / 天气不是场景切换条件，而是"环境修正因子"**

**它们能做什么**：
- 改变风险权重（夜晚 + 无照明 → Risk confidence ↓）
- 改变通行可信度（雨/雪 → 路面 hazard_multiplier ↑）
- 改变任务建议倾向（冬季 + 东北 → 结冰概率 ↑）

**它们不能做什么**：
- ❌ 直接切 Scene
- ❌ 直接生成新 SceneSegment

### 2️⃣ 数据结构（Phase B 已落地）

```python
@dataclass
class EnvironmentContext:
    season: Optional[str] = None      # SPRING / SUMMER / AUTUMN / WINTER
    time_of_day: Optional[str] = None # DAY / NIGHT / DUSK / DAWN
    weather: Optional[str] = None     # CLEAR / RAIN / SNOW / FOG / WINDY
    temperature: Optional[float] = None  # 摄氏度
```

并作为 `SceneInputs` 的一部分。

### 3️⃣ 工程级影响规则（写死在文档里）

**示例规则（非代码）**：

- **夜晚 + 无照明**
  - Risk：confidence ↓
  - Task：不建议行走类任务
  
- **雨 / 雪**
  - Risk：路面 hazard_multiplier ↑
  - Scene：不切换
  
- **冬季 + 东北**
  - Risk：结冰概率 ↑
  - Task：慢行 / 回避建议 ↑

**这些规则的计算不在 SceneRegistry 内**。  
**SceneRegistry 只负责**：👉 把"当前环境状态"稳定地提供出去。

### 4️⃣ match() 的关键原则（非常重要）

```python
function match(inputs, scene):
  geometry_ok  = geometry_similarity(inputs.geometry, scene.geometry) > T1
  semantic_ok  = semantic_similarity(inputs.semantic, scene.semantic) > T2
  behavior_ok  = behavior_similarity(inputs.behavior, scene.behavior) > T3

  # ⚠️ 时间 & 天气只影响权重，不直接否定匹配
  environment_modifier = compute_env_modifier(inputs.time, inputs.weather)

  score = weighted_sum(
            geometry_ok,
            semantic_ok,
            behavior_ok
          ) * environment_modifier

  return score > MATCH_THRESHOLD
```

**写死一条铁律**：
- ❌ 夜晚 ≠ 新场景
- ❌ 下雪 ≠ 新场景
- ✅ 它们只会降低 confidence / 提升风险权重

### 5️⃣ 在系统中的位置

**必须补充的位置**：
1. **v1.8.5 Phase B 设计文档**（本文档）
   - 新增章节：《Environment Context（时间 × 天气）与 Scene 的关系》
2. **SceneInputs**
   - 明确 time / weather 是输入，但不触发切换
3. **Risk / Task Adapter**
   - 未来可以读取 environment_context 做修正

---

## 八、验收标准（非常重要）

- ✅ 同一段路上下坡 → `scene_id` 不变
- ✅ 单帧异常 → candidate 出现但不切换
- ✅ 持续变化 → 平滑切换
- ✅ Risk / Task / Emotion 行为**完全不变**
- ✅ Debug 中可清晰看到 confidence 演化
- ✅ 夜晚/恶劣天气 → confidence 降低但不切换场景
- ✅ 环境上下文只影响权重，不触发场景切换

---

## 九、相关设计文档

### 9.1 Scene Segment 连续性设计

**文档**：详见 [`V1_8_5_SCENE_SEGMENT_CONTINUITY_DESIGN.md`](./V1_8_5_SCENE_SEGMENT_CONTINUITY_DESIGN.md)

**内容**：
- Scene Segment 的工程化最小单位定义
- 多锚点结构（几何 / 语义 / 行为 / 记忆）
- SceneRegistry 的连续性与切换原则
- Environment Context 的作用边界
- Scene × Context 连续性原则

**文档状态**：v1.8.5 Phase B – Structural Constraint  
**后续实现与调参** 不得违反该文档中的原则。

---

### 9.2 User Feedback 分层接纳设计

**文档**：详见 [`V1_8_5_USER_FEEDBACK_DESIGN.md`](./V1_8_5_USER_FEEDBACK_DESIGN.md)

**内容**：
- 三层事实模型（World Fact / System Belief / User Claim）
- 用户反馈的结构化接纳（一期）
- 用户反馈的三类工程语义（A/B/C 类）
- 抗恶意与系统免疫机制
- 二期接口预留（语言理解、情感计算）

**文档状态**：v1.8.5 Phase B – Structural & Interface Constraint  
**二期实现**不得突破该文档的写权限与分层约定。

**核心原则**：
- 用户输入永远只写入 User Claim 层
- 一期不做语义理解，只做结构化接纳
- 所有 Claim 都有"安全的容器"和"正确的去向"

---

### 9.3 Context Evolution Engine（CEE）

**文档**：详见 [`V1_8_5_CONTEXT_EVOLUTION_ENGINE.md`](./V1_8_5_CONTEXT_EVOLUTION_ENGINE.md)

**内容**：
- ContextItem 统一结构（可演化信息单元）
- 演化机制的三大核心维度（Relevance / Confidence / Lifecycle）
- Scene / Map / Memory / Library 共用机制
- 演化的五条工程铁律
- 一期明确做什么 / 不做什么

**文档状态**：v1.8.5 Phase B – Structural & Evolution Constraint  
**后续实现**不得违反该文档的演化原则与生命周期约定。

**核心原则**：
- 不做瞬时切换、不做集合替换、不做直接删除
- 任何新信息都先从 PASSIVE 开始
- 让系统具备"记忆的弹性"和"认知的惯性"

---

## 六、Scene Segment × Context 连续性设计

### 为什么不能瞬切

**问题**：GPS 从 (1234, 5678) 跳到 (4567, 8901)，Scene 是否应该立即切换？

**答案**：不应该。

**原因**：
1. **GPS 漂移**：GPS 本身有误差，单点跳变可能是噪声
2. **场景连续性**：真实场景切换是渐进的，不是瞬时的
3. **用户体验**：瞬切会导致上下文丢失，影响决策质量

**解法**：
- 使用**多锚点联合确认**（几何 + 语义 + 行为 + 记忆）
- 使用**confidence 演化**（连续低于阈值才切换）
- 使用**Scene Overlap Window**（重叠窗口期间两者共存）

---

### 为什么不用 GPS 米级切分

**问题**：是否应该用 GPS 坐标的微小变化来切分 Scene？

**答案**：不应该。

**原因**：
1. **GPS 精度限制**：民用 GPS 精度约 3-5 米，米级切分不可靠
2. **场景语义**：场景切换应该基于语义变化，而非坐标变化
3. **计算成本**：米级切分会导致频繁切换，增加计算负担

**解法**：
- 使用**语义锚点**（place_type / building_id / zone）
- 使用**行为锚点**（用户行为稳定性）
- 使用**记忆锚点**（历史关联）

---

### 为什么 Context 不随 Scene 删除

**问题**：Scene 切换时，是否应该删除旧 Scene 的 Context？

**答案**：不应该。

**原因**：
1. **连续性需求**：某些 Context（如"注意台阶"）在场景切换后仍可能相关
2. **平滑过渡**：Context 的 `relevance` 应该逐渐衰减，而不是突然消失
3. **历史关联**：记忆锚点需要保留历史 Context 以维持连续性

**解法**：
- 使用**Context 三态生命周期**（ACTIVE → PASSIVE → ARCHIVED）
- 使用**relevance 演化**（连续函数，而非离散切换）
- 使用**decay_rate**（控制衰减速度）

---

## 七、Phase B 完成后的系统状态

### 应该看到的

- ✅ Scene 拥有真实世界锚点（GPS / 地图）
- ✅ Scene 具备连续性（不会瞬切）
- ✅ Context 具备平滑切换（relevance 演化）
- ✅ Risk / Task / Emotion 可读取稳定上下文
- ✅ 系统行为与 v1.8.4 完全一致（不破坏冻结）

### 不应该看到的

- ❌ Scene 频繁切换
- ❌ Context 突然消失
- ❌ GPS 漂移导致场景跳变
- ❌ 实时地图依赖

---

## 八、与 v1.8.4 / Phase A 的边界说明

### 冻结保证

- ✅ **Risk 行为逻辑**：完全不变
- ✅ **决策优先级**：完全不变
- ✅ **触发判定**：完全不变
- ✅ **测试框架**：完全不变

### Phase B 新增内容

- ✅ **Scene Segment**：场景最小工程单位
- ✅ **4 个工程锚点**：几何 / 语义 / 行为 / 记忆
- ✅ **Context State**：上下文状态容器
- ✅ **平滑切换机制**：Scene Overlap Window + Context 三态生命周期
- ✅ **GPS / 地图接入**：离线地图为主，GPS 为弱锚点

### 明确不做（Phase B）

- ❌ 实时高精地图
- ❌ 3D 地形建模
- ❌ 自动语义切分城市
- ❌ Scene 变成决策层

---

## 九、后续阶段预览

### Phase C（计划中）

- 视觉观察补充
- SceneMemory 反写
- 长期记忆修正

---

## 📚 相关文档

- `docs/V1_8_5_SCENE_MODELING_LAYER_DESIGN.md` - v1.8.5 设计文档
- `docs/V1_8_5_SCENE_MODELING_PHASE_A.md` - Phase A 执行蓝图
- `docs/V1_8_4_FREEZE_DECLARATION.md` - v1.8.4 冻结声明

---

**文档状态**：Design Draft  
**创建时间**：2024-12-31  
**维护者**：Luna Badge MVP Team

---

## 💡 最终总结

**你现在做的 Phase B，本质是：**

**把"世界理解"拆成"锚定 + 连续性 + 置信度"，而不是"判断对错"。**

**这条路是长期可维护、个人开发者也扛得住的路线。**

