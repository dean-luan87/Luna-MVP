# v1.8.5 World Context Modeling（世界 / 场景建模工程规范）

**状态**：✅ 工程冻结版  
**日期**：2024-12-XX  
**版本**：v1.8.5

---

## ⚠️ 本文档性质

本文档定义 v1.8.5 中**世界模型（World Model）**的工程边界、数据流向与防污染规则。

**该模型不是"真实世界的完整还原"，而是：**  
**从记忆系统中抽离"场景 / 空间 / 事实"的可计算表示，用于支撑决策中台与任务链。**

**本文档是工程约束文档，不是说明文。**  
**写完后，后面所有实现都只能"补充"，不能推翻。**

---

## 一、总体定位（必须统一认知）

### 1.1 世界模型不是"大一统模型"

**v1.8.5 的世界模型 不是**：
- ❌ Google 级地图引擎
- ❌ 全局 3D 世界模拟
- ❌ 自动纠错的真理机器

**而是**：

**一个"可追责、可演化、可抗噪声"的场景化建模后端**

**它的核心目标只有一个**：

**在真实世界噪声极大的情况下，保证系统长期不被污染、不失真、不跳变。**

---

## 二、核心架构（四个并行 Registry）

```
             ┌────────────┐
             │ SceneRegistry│  ← 场景连续性 / 锚点
             └──────┬─────┘
                    │
    ┌──────────┐    │     ┌────────────┐
    │ MemoryReg│────┼────▶│ FactCandidate│
    └──────────┘    │     │    Pool     │
          │          │     └──────┬─────┘
          │          │            │
          │          ▼            ▼
          │     ┌──────────┐  ┌──────────┐
          └────▶│MapRegistry│  │LibraryReg│
                └──────────┘  └──────────┘
```

### 2.1 四个模块的角色分工（写死）

| 模块 | 职责 | 是否可写事实 |
|------|------|------------|
| SceneRegistry | 场景锚点、连续性、切换 | ❌ |
| MemoryRegistry | 体验 / 偏好 / 事实信号整流 | ❌ |
| FactCandidatePool | 事实候选慢确认 | ❌ |
| LibraryRegistry | 已确认事实与规则 | ✅（但极慢） |
| MapRegistry | 权重聚合与偏置输出 | ❌ |

**只有 LibraryRegistry 允许写"事实"，且必须经过候选池。**

---

## 三、Scene：世界建模的最小连续单位

### 3.1 Scene 的工程定义

**Scene 是"连续决策上下文"的最小稳定单位**

**不是米，不是 GPS 点，而是**：
- 具有语义连续性
- 具有行为一致性
- 能承载记忆与事实的锚点

### 3.2 Scene 的切换原则（防跳变）

- ✅ Scene 切换 ≠ 清空上下文
- ✅ Scene 之间必须存在**过渡期（overlap）**
- ✅ 旧 Scene 的权重**渐退**
- ✅ 新 Scene 的权重**渐进**

**禁止出现**：
```
A 场景注意事项 = 1234
切换到 B 场景 → 1234 瞬间消失，变成 5678
```

---

## 四、MemoryRegistry：体验 ≠ 事实（核心分流）

### 4.1 Memory 的三类输入（必须分类）

| 类型 | 示例 | 是否可升级事实 |
|------|------|--------------|
| EXPERIENCE | 路滑、难走、不舒服 | ❌ |
| PREFERENCE | 喜欢人少、避开天桥 | ❌ |
| FACT_SIGNAL | 封路、积水、店铺关闭 | ❌（只能进候选池） |

### 4.2 体验记忆的价值定位

- ✅ 体验是**高价值信息**
- ✅ 但它只影响：
  - 舒适度推荐
  - 风险关注权重
- ❌ **永远不直接改变地图或事实**

---

## 五、FactCandidatePool：事实慢确认的防污染核心

### 5.1 为什么必须有候选池

**现实世界中**：
- 用户会误报
- 视觉会误判
- 环境会瞬变

**候选池是系统的"免疫系统"**

### 5.2 升级为 PROMOTABLE 的硬条件（写死）

- ✅ 支持次数 ≥ N
- ✅ 独立来源 ≥ M
- ✅ 时间跨度 ≥ T
- ✅ 冲突次数 ≤ K

**任何一条不满足，不能升级。**

**基线参数**：
- `N_support = 3`
- `N_sources = 2`
- `MIN_SPAN = 30min`（避免一次性误报）
- `MAX_CONFLICT = 1`

### 5.3 用户输入的限制（防恶意）

- ❌ `user_report` 不提升 confidence
- ✅ 只能作为支持信号之一
- ❌ 不能作为唯一来源

### 5.4 候选过期机制（P0.5，必须补）

**规则**（写死）：
```python
if now - last_seen_ts > CANDIDATE_TTL:
    status = REJECTED
    last_reason = "expired_no_recent_support"
```

**参数建议**：
- `CANDIDATE_TTL = 24h`（或 12h）

**这是防止旧候选长期霸占系统的关键。**

---

## 六、LibraryRegistry：事实与规则的唯一入口

### 6.1 Library 的定位

**Library 是"已确认但仍可回滚的事实资产层"**

### 6.2 Library 中的事实不是"真理"

**所有事实都有**：
- confidence
- 来源
- 最近验证时间

**所有事实都可能**：
- 降级
- 弃用
- 被替换

### 6.3 事实的生命周期

```
Candidate → Promotable → PASSIVE → ACTIVE → PASSIVE → DEPRECATED
```

**没有删除，只有弃用。**

### 6.4 Library 条目软回滚机制（保留机制）

**规则**（写死）：
```python
if now - last_verified_ts > VERIFY_TTL:
    lifecycle_state = PASSIVE
    confidence *= 0.85
```

**参数建议**：
- `VERIFY_TTL = 7d`（环境事实）
- `VERIFY_TTL = 30d`（规则型）

**这是防止旧事实长期霸占系统的关键。**

---

## 七、MapRegistry：只输出权重，不输出结论

### 7.1 MapRegistry 的唯一输出

```python
MapBias:
  comfort_bias           # -1.0 ~ +1.0
  avoid_bias             # 0.0 ~ 1.0
  risk_attention_boost   # 0.0 ~ 1.0
  reasons[]              # 可追责来源
```

### 7.2 MapRegistry 的铁律

- ❌ 不写数据库
- ❌ 不记忆历史
- ❌ 不学习
- ❌ 不放大噪声

**MapRegistry 是"计算层"，不是"认知层"。**

### 7.3 MapRegistry 对噪声的天然免疫

- ✅ LibraryHint 本身已经：慢确认、有 confidence、有生命周期
- ✅ MapRegistry 只做**线性加权 + clamp**，不放大、不学习、不记忆
- ✅ 即使 Library 里有一条错的事实，也只会产生有限影响，并会随回滚自然消失

---

## 八、时间 / 天气 / 环境的影响规则

### 8.1 时间尺度

| 时间 | 影响 |
|------|------|
| 季节 | 长期风险规则（结冰、暴雨） |
| 昼夜 | 可行性、舒适度 |
| 实时天气 | risk_attention_boost |

### 8.2 天气不改变事实，只改变 relevance

- ✅ "该路段易结冰"是**长期事实**
- ✅ 冬季 relevance 上升
- ✅ 夏季 relevance 下降
- ❌ **事实本身不消失**

---

## 九、抗噪声与防污染铁律（最高优先级）

### 9.1 稳定性闸门（所有 Registry 通用）

- ❌ 位置 / 视角不稳定 → **不写新信息**
- ✅ 只允许衰减旧信息

### 9.2 慢写入原则

- ✅ Memory 可写（体验）
- ✅ Fact 必须慢
- ✅ Library 更慢

### 9.3 单向数据流

```
Memory → Candidate → Library → Map
```

**禁止反向写入。**

### 9.4 防污染铁律（必须写死）

1. **用户输入不能直接入库**
2. **事实必须有多源或时间跨度**
3. **置信度慢升快降**
4. **不删除，只弃用（DEPRECATED）**
5. **Scene/位置不稳定时，不升级事实**
6. **跳过 FactCandidatePool 直接写 Library** ❌
7. **在 position_state.stable=False 时升级事实** ❌
8. **Library 反向写 Memory 或 Map** ❌

**这 8 条如果破坏，系统一定会被污染。**

---

## 十、v1.8.5 冻结声明（工程级）

### 10.1 允许的修改

- ✅ 参数调优（N_support / min_span / confidence step）
- ✅ 字段补充（不破坏主键和状态机）
- ✅ 性能优化（索引、批处理）
- ✅ 数据源接入（GPS / 地图 / 视觉）

### 10.2 禁止的修改（破坏会导致系统污染）

- ❌ **跳过 FactCandidatePool 直接写 Library**
- ❌ **用户输入直写事实**
- ❌ **Scene 切换清空上下文**
- ❌ **Map 写事实**
- ❌ **在 position_state.stable=False 时升级事实**
- ❌ **Library 反向写 Memory 或 Map**

**这 6 条如果破坏，系统一定会被污染。**

---

## 十一、Phase 2 预留接口（不实现）

以下功能在 v1.8.5 中**不实现**，但预留接口：

- 用户自然语言修正事实（需二期 NLP）
- 群体共识建模
- 多用户事实融合
- 外部地图 API 接入策略（离线优先）

---

## 十二、当前工程状态总结（一句话）

**v1.8.5 已具备：在真实世界噪声环境下，长期稳定运行的世界建模后端骨架。**

### 12.1 已完成模块

| 模块 | 状态 |
|------|------|
| SceneRegistry | ✅ 已设计（锚点/连续性） |
| MemoryRegistry | ✅ 工程骨架完成 |
| FactCandidatePool | ✅ 工程完成 + 抗污染 |
| LibraryRegistry | ✅ 工程完成 + 慢确认 |
| MapRegistry | ✅ 工程骨架完成 |
| 防污染护栏 | ✅ 稳定闸门 / TTL / 回滚规则 |

### 12.2 核心价值

**你现在做的不是"功能堆叠"，而是在做一件更难、也更值钱的事：**

**让系统在真实世界里"长期不发疯"。**

**这是 90% AI 产品翻车的地方，而你已经提前踩了刹车。**

---

## 十三、下一步（按你之前说的）

接下来只剩两步，而且都很"干净"：

1. **跑一个完整 demo**
   - Memory → Candidate → Library → MapBias
   - （雨天 + 夜晚 + 临时封路）

2. **再做一次文档回顾，确认无遗漏后冻结 v1.8.5**

---

## 附录：数据流向图（完整版）

```
Vision / GPS / System / User Feedback
              ↓
        MemoryRegistry
        ├── EXPERIENCE → experience_memories（体验资产）
        ├── PREFERENCE → preferences（偏好）
        └── FACT_SIGNAL → FactCandidatePool
                                ↓
                         LibraryRegistry
                                ↓
                         MapRegistry（只读）
                                ↓
                         MapBias（输出给任务链）
```

**关键约束**：
- MemoryRegistry 是"入口整流器"，不是事实源
- 只有 LibraryRegistry 允许写"事实"，且必须经过候选池
- MapRegistry 永远只读，不写任何事实

---

**文档版本**：v1.8.5 工程冻结版  
**最后更新**：2024-12-XX  
**状态**：✅ 已冻结


