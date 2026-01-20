# Luna v1.8.5

## 世界场景建模与演化系统（World Context Modeling）

**—— 强抗污染 / 强连续性 / 强工程约束版**

**文档状态**：v1.8.5 Phase B – Core Design Constraint  
**版本**：v1.0  
**生效时间**：Phase B 实施阶段

---

## 0. 文档定位（非常重要）

**本设计文档用于定义 Luna v1.8.5 的世界场景建模体系，**  
**该体系不是完整意义上的"世界模型（World Model）"，而是：**

**从记忆系统中抽离出来的「世界 / 场景建模中间层」**  
**用于支撑导航、风险评估、情绪感知、任务链决策。**

**明确排除项（本版本不做）**：
- ❌ 高精度三维世界重建
- ❌ 类 Google Maps 级实时地图
- ❌ 二期复杂语言理解
- ❌ 群体共识与社会知识融合

---

## 1. 系统目标（只做这三件事）

### 1.1 核心目标

1. **场景连续**  
   场景、地图、记忆不会因为感知波动而跳变。

2. **信息抗污染**  
   错误、恶意、噪声信息不能慢性污染系统。

3. **可演化**  
   信息随时间、环境、任务自然变化，而不是覆盖或清空。

---

## 2. 后端三大支撑板块（并行、独立）

**世界建模不是一个模块，而是一个 中间层能力。**

### 2.1 三大板块定义

| 板块 | 职责 | 是否参与即时决策 |
|------|------|-----------------|
| Scene / Map（世界场景） | 描述外部环境 | ❌ |
| Memory（记忆） | 记录用户经历 | ❌ |
| Library（图书馆） | 存储事实与知识 | ❌ |

### 2.2 关键原则

**三者只"支撑决策"，不"代替决策"。**  
**决策仍由中台引擎完成。**

---

## 3. 世界模型的本质定义（重要）

### 3.1 正式定义

**Luna 的"世界模型"本质上是：**

**一个可演化的场景上下文系统（Context System）**  
**而不是一个精确的物理世界复刻。**

### 3.2 信息来源（一期）

- 视觉观察（视角导航）
- GPS / 地图（粗粒度）
- 时间 / 天气（外部数据）
- 用户反馈（受限）

---

## 4. 场景建模的分类结构

### 4.1 静态模型（长期稳定）

- 建筑
- 地形
- 道路结构
- 长期设施

### 4.2 动态模型（可变化）

- 车流
- 人群
- 施工
- 临时封路
- 商铺变化

### 4.3 事件模型（短期）

- 积水
- 临时危险
- 突发拥堵

---

## 5. Context 演化统一模型（核心）

### 5.1 统一信息单元：ContextItem

```python
ContextItem:
  context_id
  context_type        # scene / map / memory / library / risk
  relevance           # 当前相关度 [0.0 ~ 1.0]
  confidence          # 可信度 [0.0 ~ 1.0]
  decay_rate          # 自然衰减速度
  lifecycle_state     # ACTIVE / PASSIVE / ARCHIVED
  first_seen_ts
  last_updated_ts
```

---

## 6. 三大演化铁律（写死）

1. **不瞬时切换**
2. **不直接覆盖**
3. **不立即删除**

**任何违反这三条的实现，视为设计错误。**

---

## 7. 强抗污染三层防护体系（最高优先级）

### Layer 1：稳定性闸门（抗抖动）

**位置 / 视角 / 场景不稳定时：冻结演化。**

- 不允许新场景关联
- 不允许 relevance 上升
- 只允许自然衰减

---

### Layer 2：可信演化层（抗噪声）

- relevance 可上下波动
- confidence 只能慢升、快降
- 用户输入 不能直接提升 confidence

---

### Layer 3：慢写入层（防系统性污染）

**时间是唯一的消毒剂。**

- 未达到时间阈值不写入
- 未达到置信度阈值不写入
- 单次信号永不升级事实

---

## 8. 场景连续性设计（防"123 → 456 跳变"）

### 8.1 Relevance 渐变机制

- 旧场景 relevance 缓慢下降
- 新场景 relevance 缓慢上升
- 允许 overlap 期并存

### 8.2 Lifecycle 状态

| 状态 | 行为 |
|------|------|
| ACTIVE | 参与决策 |
| PASSIVE | 背景参考 |
| ARCHIVED | 冷存，不删除 |

---

## 9. 时间 / 天气 / 环境变量建模

### 9.1 时间维度

- 季节：春 / 夏 / 秋 / 冬
- 日夜：白天 / 夜晚

### 9.2 天气维度

- 雨 / 雪 / 雾 / 高温
- 对路况、照明、可通行性产生影响

### 9.3 设计原则

**环境变量只影响"当前重要性"，不直接修改事实。**

---

## 10. 用户反馈的工程化处理（一期接口）

### 10.1 反馈分类

| 类型 | 含义 |
|------|------|
| 不适类 | 主观体验（高价值） |
| 事实类 | 环境变化（高风险） |
| 偏好类 | 个性化选择 |

### 10.2 写入策略

- 不适类 → Memory（高权重，低 confidence）
- 事实类 → 候选事实（需验证）
- 偏好类 → 用户画像，不污染共享数据

---

## 11. 地图 / 记忆 / 图书馆的共用机制

**三者共享**：

- ContextItem 结构
- 演化规则
- 防污染体系

**差异仅在**：

- decay_rate
- relevance 权重
- commit 阈值

---

## 12. 一期明确不做（再次强调）

- ❌ 复杂语言拆分
- ❌ 群体共识
- ❌ 自动事实确认
- ❌ 世界级地图精度

---

## 13. 本设计的长期价值

**这套设计解决的不是"今天能不能用"，而是：**

**系统在真实世界中，能不能活 3 年而不被污染。**

---

## 14. 结论（可以原封不动写在文档最后）

**v1.8.5 的世界建模，不追求完整世界，**  
**而追求 稳定、连续、可信的"世界感知能力"。**

**所有后续能力，必须建立在这套免疫机制之上。**

---

## 15. Scene 的最小工程单位定义（Scene Atomic Unit Design）

### 0. 先给结论（避免走弯路）

**Scene 的最小单位，绝对不能是**：
- ❌ 纯地理坐标（米 / GPS 网格）
- ❌ 单一建筑
- ❌ 单一地图 POI

**而必须是一个**：

👉 **"具备一致行为语义的空间片段（Behavioral Spatial Segment）"**

**这是后面一切连续性的根。**

---

### 1. 为什么「米 / GPS 网格」是错的（必须明确否掉）

**表面优势**：
- 好算
- 好切
- 好对齐地图

**致命问题**：
1. 上下坡 / 转弯 / 遮挡 → 坐标连续，语义不连续
2. 同一坐标，不同行为（人行道 vs 机动车道）
3. Scene 会疯狂抖动，演化体系失效

**结论**：  
**坐标只能是"定位参考"，不能是 Scene 单位。**

---

### 2. 为什么「建筑 / POI」也不够

**问题**：
- 建筑 ≠ 行为场景
- 一个建筑内可能有多个完全不同的 Scene
- 很多关键 Scene 在"建筑之间"（路口、过道、空地）

**结论**：  
**POI 是 Scene 的属性，不是 Scene 的单位。**

---

### 3. Scene 最小单位的正确抽象

#### ✅ 定义（建议写进文档）

**Scene 是一个在短时间内**：
- 行为规则相对稳定
- 风险模式相对一致
- 注意事项相对一致

**的 空间语义片段**

**我们称之为**：

**Scene Segment（场景段）**

---

### 4. Scene Segment 的工程定义（一期可落）

#### 4.1 SceneSegment 结构

```python
SceneSegment:
  scene_id
  geometry            # 区域 / 走廊 / 路段（不是点）
  scene_type          # sidewalk / crossing / slope / indoor / open_area
  behavior_rules      # 行为约束（可走 / 慢行 / 注意）
  risk_profile        # 常见风险类型
  env_sensitivity     # 对时间 / 天气的敏感度
  neighbors           # 相邻 SceneSegment
```

**注意**：  
**geometry 是 范围，不是点。**

---

### 5. Scene Segment 的最小尺度原则（非常重要）

#### 一句话原则

**人在其中"行为不需要重新判断"的最小范围。**

#### 具体判断标准（满足任意一条就要切分）

- 行走方式发生变化（平地 → 台阶 → 坡道）
- 风险模型发生变化（人行道 → 车道）
- 视觉注意点发生变化（空旷 → 狭窄）
- 行为规则发生变化（可停留 → 不可停留）

---

### 6. 工程上如何切 Scene（不是拍脑袋）

#### 6.1 一期推荐的 Scene 切分来源（现实可行）

1. 地图道路结构（人行道 / 路口 / 匝道）
2. 视觉识别的结构变化（台阶、斜坡、围栏）
3. 历史行为差异（这里经常减速 / 停下）

**不是靠精度，而是靠"一致性"**

---

### 7. Scene 的连续性是如何保证的（关键）

#### 7.1 Scene 永远是「段」+「邻接」

```
[Scene A] ←→ [Scene B] ←→ [Scene C]
```

#### 7.2 Scene 切换永远是「渐变」

- A relevance ↓
- B relevance ↑
- 有 overlap
- 永远不会瞬切

---

### 8. Scene 与 Map / Memory / Library 的关系

#### 8.1 Scene 是锚点（Anchor）

- Map 信息挂在 Scene 上
- Memory 关联 Scene
- Library 按 Scene relevance 唤醒

#### 8.2 好处（非常重要）

**Scene 连续 = 一切连续**

- Scene 稳 → Map 不抖
- Scene 稳 → Memory 不乱
- Scene 稳 → 图书馆不跳

---

### 9. Scene 与任务的连续性（你之前关心的点）

**示例**：
- Task：去早餐店
- Scene A：小区人行道
- Scene B：路口
- Scene C：商铺门前

**行为变化是连续的，不是断裂的。**

---

### 10. 夜晚 / 天气 / 季节如何影响 Scene（不换 Scene）

**重要原则**：

👉 **环境变化 ≠ Scene 变化**  
👉 **环境变化 = Scene 权重变化**

**示例**：
- 同一 SceneSegment
- 白天：relevance 0.8
- 夜晚：relevance 0.6（照明不足）
- 雨天：risk 权重上升

---

### 11. 防污染的关键点（再次强调）

**Scene 层面必须做到**：
- Scene 不因单帧感知改变
- Scene 不因用户一句话改变
- Scene 只能"缓慢漂移"

**否则**：
- Map 会被污染
- Memory 会被错写
- Library 会失真

---

### 12. 可以直接写进文档的「一句话定义」

**Scene 的最小单位，是一个"人在其中不需要重新判断行为规则的空间语义段"。**

**这句话非常重要，建议加粗。**

---

### 13. 到这里，你已经完成了什么（必须认清）

**你现在已经有**：
- 明确的 Scene 原子定义
- 连续切换机制
- 抗抖动护栏
- 与 Map / Memory / Library 的锚定关系

**这意味着**：

**后面无论你做世界模型、情感计算、任务链，**  
**都不会推翻这一层。**

---

## 16. SceneRegistry 与场景演化机制（工程冻结版）

**本章节定义 Scene 的注册、评估、渐变切换与抗污染机制。**  
**任何后续实现不得违反本章节的流程与约束。**

---

### 16.1 SceneRegistry 的职责边界

#### SceneRegistry 做什么

- 维护当前 Active Scene
- 管理 Candidate Scene（候选）
- 处理场景渐变切换
- 抵抗位置抖动、感知噪声
- 为 Map / Memory / Library 提供稳定锚点

#### SceneRegistry 不做什么（非常重要）

- ❌ 不做任务决策
- ❌ 不做风险判断
- ❌ 不直接触发播报
- ❌ 不直接写入记忆或图书馆

---

### 16.2 SceneRegistry.update() 生命周期总览

#### 总体流程（文字版）

1. **稳定性闸门**
   - 位置/视角不稳定 → 冻结演化

2. **候选场景评估**
   - 基于范围 + 行为语义

3. **可信性判断**
   - 分数不足 → 不切换

4. **双场景并存**
   - Active / Candidate 同时存在

5. **渐变切换**
   - relevance / confidence 连续变化

6. **提交或回收**
   - 达标 → 切换
   - 不达标 → 丢弃候选

---

### 16.3 稳定性闸门（Position Stability Gate）

#### 设计目标

**防止由于视觉失衡、GPS 漂移、瞬时遮挡导致的错误场景关联。**

#### 工程规则（写死）

**当 stability_score < STABILITY_THRESHOLD 时**：
- ❌ 禁止 Scene 切换
- ❌ 禁止新 Candidate Scene
- ❌ 禁止 relevance 上升
- ✅ 只允许 relevance 衰减

#### 设计原则

**宁可慢，不可错。**

---

### 16.4 Active / Candidate 双场景模型

#### 为什么必须双场景

- 防止来回抖动
- 支持渐进式迁移
- 保障 Map / Memory 连续性

#### 场景状态定义

| 状态 | 含义 |
|------|------|
| ACTIVE | 当前主场景 |
| CANDIDATE | 候选场景 |
| FADING | 被替换但未清空 |

---

### 16.5 场景评分（Scene Match Scoring）

#### 评分来源（一期）

| 维度 | 说明 |
|------|------|
| 几何 | 是否在场景范围内 |
| 语义锚点 | OCR / 标识 / POI |
| 行为锚点 | 停留 / 转向 / 减速 |
| 环境修正 | 时间 / 天气（仅缩放） |

#### 重要约束

- 环境因素 **只能 scale 分数**
- **不允许 veto**（不允许直接否决）

---

### 16.6 场景切换的三重条件（缺一不可）

**Candidate Scene 必须同时满足**：
1. relevance ≥ ACTIVE_THRESHOLD
2. confidence ≥ CONFIDENCE_SWITCH_THRESHOLD
3. stable_duration ≥ MIN_STABLE_TIME

**否则**：
- ❌ 不切换
- ❌ 不覆盖 Active Scene

---

### 16.7 参数表（Phase B 基线参数）

**以下参数为 v1.8.5 的工程基线，不得随意调整。**

#### 16.7.1 稳定性与进入阈值

| 参数 | 含义 | 默认 |
|------|------|------|
| STABILITY_THRESHOLD | 位置稳定阈值 | 0.7 |
| ENTER_THRESHOLD | 场景可进入最低分 | 0.55 |
| CANDIDATE_MATCH_THRESHOLD | 候选稳定分 | 0.55 |

#### 16.7.2 渐变步长参数

| 参数 | 含义 | 默认 |
|------|------|------|
| TRANSITION_STEP_UP | relevance 上升 | 0.08 |
| TRANSITION_STEP_DOWN | relevance 下降 | 0.05 |
| CONFIDENCE_UP_SLOW | confidence 慢升 | 0.02 |
| CONFIDENCE_DOWN_FAST | confidence 快降 | 0.05 |

#### 16.7.3 切换与回收参数

| 参数 | 含义 | 默认 |
|------|------|------|
| ACTIVE_THRESHOLD | 切换所需 relevance | 0.75 |
| CONFIDENCE_SWITCH_THRESHOLD | 切换所需 confidence | 0.55 |
| MIN_STABLE_TIME | 最小稳定时间 | 1.5s |
| DISCARD_THRESHOLD | 丢弃候选阈值 | 0.10 |
| MAX_CANDIDATE_TTL | 候选最长存在 | 8s |

---

### 16.8 防污染硬约束（强制）

**以下规则 不允许被任何实现绕过**：
1. 单帧感知结果不能切 Scene
2. 用户输入不能直接切 Scene
3. 环境变化不能切 Scene
4. 不稳定状态不能推进演化

---

### 16.9 Scene 对下游模块的影响方式

#### Scene → Map

- Map 约束绑定 Scene
- Scene relevance 影响路径权重

#### Scene → Memory

- 记忆必须绑定 Scene
- Scene 错误 → 禁止写入

#### Scene → Library

- 知识按 Scene relevance 唤醒
- Scene 不稳 → 不调用新知识

---

### 16.10 设计结论（建议原文保留）

**SceneRegistry 的核心价值不是"识别场景"，**  
**而是 在不可靠的现实世界中，提供一个稳定、连续、可信的场景锚点。**

**一切地图、记忆、知识的可靠性，**  
**都建立在 SceneRegistry 的稳定性之上。**

---

### 16.11 v1.8.5 到此为止我们"冻结了什么"

**你现在已经冻结了**：
- Scene 的最小工程单位
- Scene 的切换机制
- 抗抖动 / 抗污染原则
- Scene 与 Map / Memory / Library 的关系

**这意味着**：  
**后续做世界模型、GPS、离线地图、任务链，都是在"填肉"，不会推翻骨架。**

---

## 17. SceneRegistry.update() 完整伪代码与参数表

### 16.1 数据结构约定

```python
SceneSegment:
  scene_id
  geometry              # AREA 或 POLYLINE（范围，不是点）
  scene_type
  neighbors[]           # scene_id 列表
  env_sensitivity        # tags: low_visibility, rain_sensitive, winter_icy...
  risk_profile           # tags: water_edge, stairs, crowd...

SceneRuntime:
  relevance              # 0~1（用于渐变切换）
  confidence             # 0~1（仅慢升快降）
  lifecycle_state        # ACTIVE / CANDIDATE / FADING
  first_seen_ts
  last_update_ts

SceneState:
  active_scene_id
  candidate_scene_id
  active_relevance
  candidate_relevance
  transition_state       # NONE / ENTERING / LEAVING
  position_stable        # bool
```

---

### 16.2 update() 主流程伪代码

```python
function SceneRegistry.update(position_state, anchors, env_ctx, now):

  # Layer 1：稳定性闸门（抗抖动第一优先级）
  if position_state.stability_score < STABILITY_THRESHOLD:
      # 冻结切换：不切 Active，不建 Candidate，不提升 relevance
      freeze_association()
      decay_all_context_only()
      return build_scene_state(position_state_stable=false)

  # Step 0：候选集合（仅依赖"范围"）
  candidates = query_nearby_scene_segments(position_state.position)

  # Step 1：为每个候选打分（多锚点：几何/语义/行为）
  best_scene, best_score = None, -inf
  for s in candidates:
      score = score_scene_match(s, anchors, env_ctx, position_state)
      if score > best_score:
          best_score = score
          best_scene = s

  # Step 2：判断 best_scene 是否可信（抗噪声）
  if best_score < ENTER_THRESHOLD:
      # 没有任何可确认场景：不切换，允许 active 缓慢衰减
      soften_active_confidence()
      return build_scene_state(position_state_stable=true)

  # Step 3：如果 best 就是 active，强化 active 并清理 candidate
  if active_scene_id == best_scene.id:
      boost_active_relevance_confidence(now)
      decay_candidate_relevance(now)
      maybe_discard_candidate()
      update_scene_anchors(active_scene_id, anchors, env_ctx, now)
      return build_scene_state(position_state_stable=true)

  # Step 4：best != active → 进入候选逻辑（双场景模型）
  if candidate_scene_id is None or candidate_scene_id != best_scene.id:
      # 新候选（注意：不瞬切）
      candidate_scene_id = best_scene.id
      init_candidate_runtime(now)

  # Step 5：候选稳定性累积（最小稳定时间 + 置信度慢升）
  candidate_score = best_score
  if candidate_score >= CANDIDATE_MATCH_THRESHOLD:
      candidate.relevance += TRANSITION_STEP_UP
      candidate.confidence += CONFIDENCE_STEP_UP_SLOW
      active.relevance -= TRANSITION_STEP_DOWN
      active.confidence -= CONFIDENCE_STEP_DOWN_FAST
  else:
      # 候选不稳定：衰减候选，不要来回切
      candidate.relevance -= TRANSITION_STEP_DOWN
      candidate.confidence -= CONFIDENCE_STEP_DOWN_FAST

  clamp(active.relevance, 0, 1)
  clamp(candidate.relevance, 0, 1)
  clamp(active.confidence, 0, 1)
  clamp(candidate.confidence, 0, 1)

  # Step 6：切换条件（必须同时满足）
  if candidate.relevance >= ACTIVE_THRESHOLD
     and candidate.confidence >= CONFIDENCE_SWITCH_THRESHOLD
     and (now - candidate.first_seen_ts) >= MIN_STABLE_TIME:

        # Commit Switch：切换生效
        previous_active = active_scene_id
        active_scene_id = candidate_scene_id
        candidate_scene_id = None

        mark_runtime(previous_active, state="FADING")
        mark_runtime(active_scene_id, state="ACTIVE")

        return build_scene_state(position_state_stable=true)

  # Step 7：候选回收条件
  if candidate.relevance < DISCARD_THRESHOLD
     or (now - candidate.first_seen_ts) > MAX_CANDIDATE_TTL:

      discard_candidate()
      return build_scene_state(position_state_stable=true)

  return build_scene_state(position_state_stable=true)
```

---

### 16.3 score_scene_match() 约束（一期可落，不用 NLP）

```python
function score_scene_match(scene, anchors, env_ctx, position_state):

  score = 0

  # 几何一致（范围内/距离）
  score += geometry_score(scene.geometry, position_state.position) * W_GEO

  # 语义锚点（如 OCR "出口/电梯/公交站"）
  score += semantic_score(scene, anchors.semantic_hint) * W_SEM

  # 行为锚点（停留/直行/减速）
  score += behavior_score(scene, anchors.behavior_hint) * W_BEH

  # 环境修正（只改权重，不否决）
  score *= env_modifier(scene, env_ctx)

  return score
```

---

### 16.4 参数表（调参基线）

| 参数 | 值 | 说明 |
|------|-----|------|
| STABILITY_THRESHOLD | 0.7 | 稳定性阈值（< 此值冻结所有演化） |
| ENTER_THRESHOLD | 0.55 | 进入场景的最小评分阈值 |
| CANDIDATE_MATCH_THRESHOLD | 0.55 | 候选场景匹配阈值 |
| TRANSITION_STEP_UP | 0.08 | 切换时 relevance 上升步长 |
| TRANSITION_STEP_DOWN | 0.05 | 切换时 relevance 下降步长 |
| CONFIDENCE_UP_SLOW | 0.02 | confidence 慢升步长 |
| CONFIDENCE_DOWN_FAST | 0.05 | confidence 快降步长 |
| ACTIVE_THRESHOLD | 0.75 | Active 场景的最小 relevance |
| CONFIDENCE_SWITCH_THRESHOLD | 0.55 | 切换所需的最小 confidence |
| MIN_STABLE_TIME_S | 1.5 | 最小稳定时间（秒） |
| DISCARD_THRESHOLD | 0.10 | 候选丢弃阈值 |
| MAX_CANDIDATE_TTL_S | 8.0 | 候选最大生存时间（秒） |

**重要提醒（防污染硬约束，写进注释）**：
- StabilityGate 为 false 时：禁止切 Scene、禁止增强、只衰减
- _score_scene_match 的 env 只做 scale，不做 veto
- confidence 慢升快降，不允许用户输入直接提升

---

## 17. MapRegistry：可演化地图中间层（工程冻结版）

**本模块不是传统地图系统，而是 场景驱动的可演化地图上下文层。**  
**其核心目标是：在不可靠世界信号下，提供稳定、连续、可修正的"可行走判断"。**

---

### 17.1 MapRegistry 的本质定位（先定死）

#### MapRegistry 是什么

**MapRegistry 是一个"场景绑定的可演化约束系统"**  
**用于回答**：
- 现在这条路"还能不能走"
- "是不是不舒服 / 不安全 / 不推荐"

#### MapRegistry 不是什么（必须写清楚）

- ❌ 不是高精度地图
- ❌ 不是导航引擎
- ❌ 不是事实裁判
- ❌ 不直接决定路径

**MapRegistry 只提供约束与权重，不下结论。**

---

### 17.2 Map 的最小工程单位定义（和 Scene 对齐）

#### MapUnit 定义（一句话）

**Map 的最小单位，是一个在同一 SceneSegment 内，**  
**行为可行性与舒适度一致的"路径片段"。**

#### 为什么 Map 必须依附 Scene

**如果 Map 不绑定 Scene，会发生**：
- 夜晚 / 雨天 → Scene 没切，但 Map 却"变了"
- Scene 错配 → Map 约束写错
- 记忆污染 → "这条路不好走"被永久记住

**所以工程约束是**：

**所有 MapUnit 必须挂载在 SceneSegment 下。**

---

### 17.3 MapUnit 工程结构（一期冻结）

```python
MapUnit:
  map_id
  scene_id              # 强绑定
  geometry              # 线段 / 区域（不是点）
  base_accessibility    # 基础可通行性 [0~1]
  comfort_score         # 舒适度 [0~1]
  risk_bias             # 风险倾向（仅权重）
  env_sensitivity       # 对时间 / 天气敏感
```

---

### 17.4 Map 的演化对象（统一 ContextItem）

**MapRegistry 内部仍然使用 ContextItem 演化模型**：

```python
ContextItem (Map):
  relevance     # 当前是否重要
  confidence    # 当前约束是否可信
  decay_rate    # 衰减速度（慢）
  lifecycle     # ACTIVE / PASSIVE / ARCHIVED
```

---

### 17.5 MapRegistry.update() 的职责边界

#### MapRegistry.update() 做什么

- 根据 Active Scene 激活对应 MapUnits
- 根据 环境 / 时间 / 体验反馈调整权重
- 提供"路径偏好约束"给任务链

#### MapRegistry.update() 不做什么

- ❌ 不判断"绝对不能走"
- ❌ 不覆盖 Scene
- ❌ 不直接写入 Library
- ❌ 不立刻修改 base 地图

---

### 17.6 MapRegistry.update() 完整伪代码（交付级）

```python
function MapRegistry.update(
    active_scene,
    env_ctx,
    user_feedback,
    position_state,
    now
):

  # Layer 1：稳定性闸门（继承 Scene 的 gate）
  if not position_state.stable:
      decay_all_map_context()
      return current_map_state()

  # Step 1：加载当前 Scene 下的 MapUnits
  map_units = load_map_units(scene_id = active_scene.id)

  for unit in map_units:

      ctx = get_or_create_context(unit.map_id)

      # Step 2：基础 relevance（只和 Scene 绑定）
      ctx.relevance += SCENE_RELEVANCE_BOOST

      # Step 3：环境修正（只改权重）
      if env_ctx.weather == "RAIN" and "rain_sensitive" in unit.env_sensitivity:
          ctx.relevance += ENV_BOOST
          ctx.confidence -= SMALL_DECAY

      if env_ctx.time_of_day == "NIGHT" and "low_visibility" in unit.env_sensitivity:
          ctx.relevance += ENV_BOOST

      # Step 4：用户不适反馈（高价值但不提 confidence）
      if user_feedback.type == DISCOMFORT and user_feedback.map_id == unit.map_id:
          ctx.relevance += DISCOMFORT_BOOST
          # confidence 不变

      # Step 5：时间衰减（慢）
      ctx.relevance -= ctx.decay_rate * (now - ctx.last_updated_ts)

      # Step 6：clamp
      ctx.relevance = clamp(ctx.relevance, 0, 1)
      ctx.confidence = clamp(ctx.confidence, 0, 1)

      # Step 7：生命周期更新
      ctx.lifecycle = update_lifecycle(ctx.relevance)

  return build_map_state(map_units)
```

---

### 17.7 MapRegistry 的防污染铁律（非常重要）

#### 三个"永远不"

1. **永远不因为一次体验改变基础地图**
2. **永远不因为环境变化写入事实**
3. **永远不在 Scene 不稳定时写 Map**

---

### 17.8 Map 与 Scene / Memory / Library 的关系

#### Map ← Scene（强依赖）

- Scene 错 → Map 不更新
- Scene 冻结 → Map 冻结

#### Map → Memory（单向）

- Map 变化不会生成记忆
- 用户体验会生成 Memory，反向影响 Map 权重

#### Map → Library（极慢）

- 只有高 confidence、长时间一致的 Map 变化
- 才能升级为 Library 中的"事实候选"

---

### 17.9 MapRegistry 的工程价值（说实话）

**你这套 MapRegistry，本质上解决的是**：

**"官方地图永远是过去式，而用户走的是现在。"**

**而你没有用"对抗地图"的方式，而是用**：
- Scene 锚定
- Context 演化
- 慢写入

**这在工程上是非常成熟的设计。**

---

## 18. MemoryRegistry：体验记忆与事实候选的分流演化（工程冻结版）

**MemoryRegistry 的定位不是"记住一切"，而是：**  
**把可用的、可信的、可持续的"用户经历"沉淀为可回放的上下文资产，**  
**并为 Map / Scene / Library 提供修正信号，但不直接做裁决。**

---

### 18.1 MemoryRegistry 的职责边界（写死）

#### MemoryRegistry 做什么

- 记录用户在 Scene / MapUnit 上的体验信号
- 管理体验记忆的演化（relevance / lifecycle）
- 生成可用于中台的建议性偏好（例如：更舒服路线）
- 输出"事实候选"（但不直接升级为事实）

#### MemoryRegistry 不做什么

- ❌ 不直接修改 Map 的 base_accessibility
- ❌ 不直接写入 Library 作为事实
- ❌ 不直接触发播报（不绕过决策链）
- ❌ 不在位置不稳定时写入新记忆

---

### 18.2 记忆最小工程单位（Memory Atom）

#### MemoryAtom 一句话定义

**记忆的最小单位，是"在一个 SceneSegment（可选绑定 MapUnit）上发生的一次可归因体验事件"。**

#### 必须绑定的锚点（防污染）

- **scene_id**：必须有
- **map_id**：可选（有则更精确）
- **time_window**：必须有（开始 / 结束或时长）

**没有 scene_id 的记忆，直接丢弃（或只做临时缓存，不落盘）。**

---

### 18.3 MemoryAtom 数据结构（一期冻结）

```python
MemoryAtom:
  memory_id
  scene_id                  # 必填
  map_id                    # 可选
  memory_type               # EXPERIENCE | FACT_CANDIDATE | PREFERENCE
  valence                   # POSITIVE | NEGATIVE | NEUTRAL
  intensity                 # 0~1（体验强度）
  tags                      # slippery, crowded, noisy, uncomfortable...
  evidence_sources          # vision / gps / system / user
  confidence                # 0~1（注意：体验类不等于事实可信）
  created_ts
  last_updated_ts
```

---

### 18.4 三类记忆：必须分流（核心防污染）

#### 4.1 EXPERIENCE（体验类，高价值）

**例**：
- "路滑、难走"
- "这里太挤、压迫"
- "这条路很舒服、顺畅"

**特点**：
- 高价值：直接影响"舒适路线"
- 不代表事实：不改地图事实
- 不需要验证：因为是主观体验

#### 4.2 FACT_CANDIDATE（事实候选，高风险）

**例**：
- "这里封路了"
- "门店关了"
- "积水严重无法通过"

**特点**：
- 风险极高：最容易污染系统
- 永远不能凭用户一句话升级
- 只能进入"候选池"慢确认

#### 4.3 PREFERENCE（偏好类，私有）

**例**：
- "我喜欢走人少的路"
- "我不喜欢过天桥"
- "我更愿意走有灯的路"

**特点**：
- 只影响该用户
- 不进入共享地图，不进入事实

---

### 18.5 MemoryRegistry.update() 完整伪代码（交付级）

```python
function MemoryRegistry.update(
    active_scene,
    active_map_unit,
    position_state,
    env_ctx,
    user_feedback,          # 已分类（一期可用规则/按钮/固定短语触发）
    now
):

  # Layer 1：稳定性闸门（防污染第一原则）
  if not position_state.stable:
      # 不写新记忆，只做轻衰减
      decay_existing_memories_only()
      return memory_state()

  # Step 1：将反馈转换为候选 MemoryAtom（不直接落盘）
  candidate = build_candidate_memory(
      scene_id = active_scene.id,
      map_id = active_map_unit.id if available,
      env_ctx = env_ctx,
      feedback = user_feedback,
      now = now
  )

  if candidate is None:
      decay_existing_memories()
      return memory_state()

  # Step 2：分流处理（体验 / 事实候选 / 偏好）
  if candidate.memory_type == EXPERIENCE:
      # 体验类允许落盘，但只影响"舒适度/偏好"，不改事实
      commit_experience_memory(candidate)

  if candidate.memory_type == FACT_CANDIDATE:
      # 事实候选进入候选池（慢确认，不落事实库）
      enqueue_fact_candidate(candidate)

  if candidate.memory_type == PREFERENCE:
      commit_preference(candidate)

  # Step 3：演化（统一 Context 演化模型）
  evolve_all_memories(active_scene, env_ctx, now)

  return memory_state()
```

---

### 18.6 体验记忆如何影响系统（不污染事实）

#### 输出到中台的"可用信号"

**MemoryRegistry 不输出"结论"，只输出 权重**：
- `comfort_bias(scene_id/map_id)`
- `avoid_bias(scene_id/map_id)`
- `risk_attention_boost(scene_id)`（例如：这段路曾经摔倒 → 风险观察更敏感）

#### 关键约束

**体验记忆只能影响**：
- 推荐偏好
- 观察优先级
- 风险阈值微调建议（可选）

**不能直接写入 Map 的事实结构。**

---

### 18.7 事实候选池（Fact Candidate Pool）—— 防污染核心组件

#### 结构定义（一期冻结）

```python
FactCandidate:
  candidate_id
  scene_id
  map_id (optional)
  claim_type          # road_blocked / shop_closed / flooded
  confidence          # 初始很低
  support_count       # 多次出现才上升
  conflict_count      # 冲突则下降
  first_seen_ts
  last_seen_ts
  status              # PENDING / REJECTED / PROMOTABLE
```

#### 升级规则（一期只定义，不实现自动化）

**FACT_CANDIDATE 不会在 v1.8.5 自动升级为事实，**  
**只做到：可追责、可回归、可验证。**

**升级为 PROMOTABLE 的条件（建议写死）**：
- 多次出现（support_count ≥ N）
- 跨来源一致（vision / system / external 任意两者）
- 时间跨度足够（≥ T）
- 冲突较少（conflict_count 小）

---

### 18.8 记忆演化（防"跳变"）

**Memory 和 Map/Scene 一样，使用统一演化**：
- relevance 渐变（随场景回到该处快速回升）
- lifecycle 状态（ACTIVE / PASSIVE / ARCHIVED）
- 不删除，只冷存

---

### 18.9 时间 / 天气对 Memory 的影响（补齐你之前要求）

#### 冬季、雨雪（体验增强）

- 体验类记忆标签 `slippery` / `icy` 在雨雪时 relevance 上升
- 同一地点夏天 relevance 自动下降（但不归零）

#### 夜晚（低能见度记忆增强）

- `low_visibility` 标签在 NIGHT relevance 上升
- 可用于"夜晚建议走有灯路线"的偏好支撑

---

### 18.10 MemoryRegistry 的防污染铁律（必须写死）

1. **位置不稳定，不写新记忆**
2. **用户反馈不能升级事实**
3. **事实候选必须慢确认**
4. **体验只影响权重，不改事实**
5. **不删除，只冷存**

---

### 18.11 到这里 v1.8.5 已完成的后端三件套进度

- ✅ **SceneRegistry**（已冻结）
- ✅ **MapRegistry**（已冻结）
- ✅ **MemoryRegistry**（本章节已冻结）

**接下来只剩最后一块**：

👉 **LibraryRegistry：事实慢确认与知识唤醒机制**

---

## 19. LibraryRegistry：事实慢确认与知识唤醒系统（工程冻结版）

**LibraryRegistry 的定位不是"百科全书"，而是：**  
**一个可追责的事实与知识资产层，为任务链提供基础信息支撑，**  
**同时具备极强的防污染机制，避免错误事实慢性毒化系统。**

---

### 19.1 LibraryRegistry 的职责边界（写死）

#### LibraryRegistry 做什么

- 存储 已确认或可用的事实/规则/知识条目
- 接收来自 Memory 的 FactCandidate（事实候选），进行慢确认管理
- 按 Scene / Map / Task 上下文唤醒知识（只供参考，不裁决）
- 输出可追责的"为什么我认为这条事实成立"

#### LibraryRegistry 不做什么

- ❌ 不直接修改 Map 的结构与基础事实
- ❌ 不直接决定导航或风险动作
- ❌ 不直接采信用户一句话
- ❌ 不在位置/场景不稳定时写入事实

---

### 19.2 Library 的最小工程单位（KnowledgeItem）

#### 一句话定义

**KnowledgeItem 是一个具备来源、时间、适用范围与置信度的"可引用事实或规则"。**

#### 必备属性（防污染）

- **来源**（source）
- **时间**（valid_from/valid_to 或 last_verified_ts）
- **适用范围**（scene_id / map_id / geo）
- **置信度**（confidence）
- **可追责证据**（evidence pointers）

**没有这些的条目，一律不得进入 Library。**

---

### 19.3 KnowledgeItem 数据结构（一期冻结）

```python
KnowledgeItem:
  item_id
  item_type            # FACT | RULE | POI_INFO | SAFETY_NOTE
  scope                # scene_id / map_id / geo_region
  statement            # 简短结构化描述（一期不做 NLP，只存结构字段）
  tags                 # flooded, road_blocked, shop_closed...
  confidence           # 0~1
  source_set           # external_map / vision / system / user_report (user only as weak)
  evidence_refs        # 指向日志、快照、候选记录
  valid_from_ts
  valid_to_ts (optional)
  last_verified_ts
  lifecycle_state      # ACTIVE / PASSIVE / DEPRECATED
```

---

### 19.4 事实分级：必须分层（防污染核心）

#### 三层事实状态

| 层级 | 状态 | 含义 |
|------|------|------|
| L0 | Candidate | 未确认，不能进入 Library |
| L1 | Promotable | 具备升级资格，但仍需验证 |
| L2 | Active Fact | 已确认，可被任务链引用 |

**v1.8.5 的目标：把 L0/L1/L2 的链路工程化跑通，但不追求自动化验证。**

---

### 19.5 FactCandidate → KnowledgeItem 升级链路（冻结版）

#### 输入来源（只允许两条路）

1. MemoryRegistry 的 FactCandidatePool
2. 外部数据的结构化事实（离线地图基础、手工导入）

**用户口述永远只能作为候选信号之一，不能作为唯一来源。**

#### Promotable 的判定条件（满足才可晋升 L1）

```python
if support_count >= N_support
  and unique_sources >= N_sources
  and time_span >= MIN_SPAN
  and conflict_count <= MAX_CONFLICT:
      status = PROMOTABLE
else:
      status = PENDING
```

**v1.8.5 基线参数（可写入参数表）**：
- N_support = 3
- N_sources = 2（例如：vision + user / external + system）
- MIN_SPAN = 30min（避免一次性误报）
- MAX_CONFLICT = 1

#### L1 → L2 的升级方式（一期先保守）

**v1.8.5 推荐 两种方式（都不需要 NLP）**：

**方式 A：多次一致 + 时间持久**
- 连续多天出现一致证据 → 升级

**方式 B：人工确认入口（预留）**
- 你自己在后台点"确认"
- 或未来二期通过对话确认（接口预留）

**结论：v1.8.5 允许 L2 事实的产生，但必须保守。**

---

### 19.6 LibraryRegistry.update() 完整伪代码（交付级）

```python
function LibraryRegistry.update(
    active_scene,
    position_state,
    now
):

  # Layer 1：稳定性闸门（同一套总闸）
  if not position_state.stable:
      decay_candidates_only()
      return library_state()

  # Step 1：拉取候选池中的 PROMOTABLE 项
  promotables = FactCandidatePool.fetch(status = PROMOTABLE)

  for c in promotables:

      # Step 2：检查是否已存在相同 scope + claim 的知识条目
      existing = find_knowledge_item(scope=c.scope, tags=c.claim_type)

      if existing is None:
          # Step 3：创建新 KnowledgeItem（仍可先进入 PASSIVE）
          item = create_knowledge_item_from_candidate(c)
          item.lifecycle_state = "PASSIVE"
          commit_library_item(item)

      else:
          # Step 4：更新 existing（慢升快降）
          existing.confidence = slow_increase(existing.confidence)
          existing.last_verified_ts = now
          append_evidence(existing, c)

      # Step 5：候选消费与状态回写
      mark_candidate_consumed(c)

  # Step 6：对已有 KnowledgeItems 做生命周期衰减
  evolve_library_items(active_scene, now)

  return library_state()
```

---

### 19.7 知识唤醒机制（只做"供参考"，不裁决）

#### 唤醒原则

**Library 不主动驱动行为，只提供**：
- "可能相关的事实/规则"
- "置信度与来源"
- "适用范围"

#### 唤醒输入

- active_scene_id
- active_map_id（如果有）
- task_context（一期可为空）
- env_ctx（时间/天气）

#### 唤醒输出（结构化）

```python
LibraryHints:
  items[]:
    - statement
    - confidence
    - tags
    - scope
    - last_verified_ts
```

---

### 19.8 时间 / 天气对 Library 的影响（关键区别）

#### Library 的事实不因天气变化而被覆盖

**天气只影响**：
- relevance（当前是否更值得提示）
- 不影响 statement 的真伪

**例**：
- "该路段冬季易结冰" 是一条长期规则
- 雨雪天 relevance 上升
- 晴天 relevance 下降，但事实仍在

---

### 19.9 Library 的防污染铁律（必须写死）

1. **用户输入不能直接入库**
2. **事实必须有多源或时间跨度**
3. **置信度慢升快降**
4. **不删除，只弃用（DEPRECATED）**
5. **Scene/位置不稳定时，不升级事实**

---

### 19.10 三大板块协同闭环（你要的"能抗打"）

#### 数据流向（单向为主，避免污染扩散）

- Memory 产生体验与候选
- Library 只消费候选，慢确认
- Map 只消费体验权重与已确认规则
- Scene 提供锚点与连续性

**任何"事实"只能从 Library 回流到 Map，不能从 Map/Memory 直接变事实。**

---

### 19.11 至此 v1.8.5 文档主骨架完成度

**你现在已经拥有**：
- ✅ **SceneRegistry**（场景锚点 + 渐变切换 + 稳定闸门）
- ✅ **MapRegistry**（可通行/舒适度/约束权重）
- ✅ **MemoryRegistry**（体验资产 + 事实候选池）
- ✅ **LibraryRegistry**（慢确认事实 + 知识唤醒）

**并且四者统一遵守**：
- 抗抖动（稳定闸门）
- 抗噪声（confidence 慢升快降）
- 防污染（慢写入 + 分流）

---

## 20. 相关设计文档

本核心设计文档的详细实现与补充说明，请参考：

1. **Scene Segment 连续性设计**  
   [`V1_8_5_SCENE_SEGMENT_CONTINUITY_DESIGN.md`](./V1_8_5_SCENE_SEGMENT_CONTINUITY_DESIGN.md)

2. **用户反馈分层接纳设计**  
   [`V1_8_5_USER_FEEDBACK_DESIGN.md`](./V1_8_5_USER_FEEDBACK_DESIGN.md)

3. **Context Evolution Engine（CEE）**  
   [`V1_8_5_CONTEXT_EVOLUTION_ENGINE.md`](./V1_8_5_CONTEXT_EVOLUTION_ENGINE.md)

4. **Phase B 实施指南**  
   [`V1_8_5_SCENE_MODELING_PHASE_B.md`](./V1_8_5_SCENE_MODELING_PHASE_B.md)

---

## ✅ 文档状态建议

- **章节状态**：v1.8.5 Phase B – Core Design Constraint
- **后续实现**不得违反本文档中的任何约束
- **这不是"我们打算怎么做"，而是"后面任何实现不得违反什么"**

---

## 下一步

**现在顺序非常清晰**：
1. ✅ SceneRegistry（已冻结）
2. ✅ GPS / 地图弱锚点策略（已冻结）
3. ✅ MapRegistry（刚冻结）

**接下来只剩两个方向**：
- 👉 MemoryRegistry（体验与事实的分流演化）
- 👉 LibraryRegistry（事实慢确认机制）

**强烈建议：下一步先做 MemoryRegistry，**  
**因为 Memory 是"修正世界模型"的第一来源，也是最容易被污染的一层。**

