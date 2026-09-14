# 主线 2 第二阶段：骨架记忆分池 M0 交付说明

**依据**：SPATIAL_MEMORY_POLICY_CONSTITUTION.md v1.0 + Skeleton Mix M0 + Skeleton Filter M0  
**目标**：在 Skeleton Mix 与 Skeleton Filter 基础上，把当前空间信息第一次分流到“骨架感知的四层空间记忆池”，形成最小可见、可记录、可测试的记忆分池原型。本轮只做最小分池，不做复杂遗忘、长期证据门槛、学习。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/spatial_memory_pools.py` | **新建**。SpatialMemoryItem、SpatialMemoryPools（四层 items + dominant_skeleton + pool_reason）；build_spatial_memory_pools(mix, filt, smap, relations, goal) 按 keep/suppress 与 dominant 分流到 working/episode，stable/anchor 占位。 |
| `decision_monitor/schema.py` | 引入 SpatialMemoryPools；DecisionMonitorFrame 新增 spatial_memory_pools。 |
| `decision_monitor/builder.py` | 引入 spatial_memory_pools；build 中在 skeleton_filter 之后调用 build_spatial_memory_pools，写入 frame.spatial_memory_pools。 |
| `runtime/context.py` | 新增 spatial_memory_working_count、spatial_memory_episode_count、spatial_memory_stable_count、spatial_memory_anchor_count、spatial_memory_dominant、spatial_memory_pool_reason。 |
| `main.py` | 决策显示器块内，将 frame.spatial_memory_pools 四层计数与 dominant/reason 写入 runtime_ctx。 |
| `tools/decision_monitor_viewer.py` | 新增「空间记忆分池 / Spatial Memory Pools (M0)」卡片：working/episode 摘要、stable/anchor 占位、dominant 与 pool_reason；sections 增加 spatial_memory_pools。 |
| `decision_monitor/CONTRACT.md` | 补充 spatial_memory_pools（骨架记忆分池 M0）说明与预留边界。 |

---

## 2. Memory Pool 与 Memory Item 数据结构说明

### SpatialMemoryPools（四层池）

| 字段 | 类型 | 含义 |
|------|------|------|
| working_memory_items | List[SpatialMemoryItem] | 当前工作记忆项（本轮真实写入） |
| episode_memory_items | List[SpatialMemoryItem] | 当前片段记忆项（本轮真实写入） |
| stable_memory_items | List[SpatialMemoryItem] | 稳定记忆项（当前仅占位或空） |
| anchor_memory_items | List[SpatialMemoryItem] | 锚点记忆项（当前仅占位或空） |
| dominant_skeleton | str | 当前主导骨架（影响分池偏好） |
| pool_reason | str | 本帧分池原因摘要 |

### SpatialMemoryItem（最小记忆项）

| 字段 | 类型 | 含义 |
|------|------|------|
| memory_layer | str | working / episode / stable / anchor |
| source_type | str | focus_region / traversable_region / risk_region / confirm_region / relation |
| payload_summary | str | 摘要字符串（如 region_type#rank sector=… band=…） |
| skeleton_context | str | 当前 dominant_skeleton |
| retention_policy | str | ttl / task_end / evidence_replace 等（预留） |
| timestamp | float | 写入时间戳 |
| confidence | float | 0~1 |
| use_count | int | 可选预留 |
| conflict_count | int | 可选预留 |
| last_used_ts | float | 可选预留 |

---

## 3. 最小分池规则说明

- **输入**：skeleton_mix、skeleton_filter、local_goal_spatial_map、local_goal_spatial_relations、goal。
- **working**：当前 keep_region_types 对应的区域（每类最多 3 条）及与 keep 一致的关系（supports/conflicts_with 等，最多 5 条）进入 working；Safety 主导时 risk_region/confirm_region/traversable_region 必进 working。
- **episode**：与当前任务强相关、可跨几帧复用的内容进入 episode；**骨架差异化**：
  - **Navigation 主导**：traversable_region、confirm_region、focus_region 易进 episode；supports 关系进 episode。
  - **Fine Interaction 主导**：focus_region、confirm_region 易进 episode。
  - **Observation 主导**：focus_region 易进 episode。
  - **Safety 主导**：风险与 blocking 强进 working，不直接长驻 stable；episode 可少或空。
- **stable / anchor**：当前仅占位（单条 placeholder 项）或空；**suppress 内容不得直接进入 stable/anchor**；不做证据门槛、冲突消解、替换策略。

---

## 4. Viewer 展示说明

- **卡片标题**：空间记忆分池 / Spatial Memory Pools (M0)。
- **第一行**：主导：&lt;dominant_skeleton&gt; · &lt;pool_reason&gt;。
- **第二行**：working (N)：前 5 条 payload_summary，用 · 分隔。
- **第三行**：episode (N)：前 5 条 payload_summary，用 · 分隔。
- **第四行**：stable：占位/空 · anchor：占位/空。
- 专家折叠面板可展开 spatial_memory_pools 查看 working_memory_items、episode_memory_items、stable_memory_items、anchor_memory_items、dominant_skeleton、pool_reason。

---

## 5. 样本运行结果（验收）

- 运行时存在可读的四层空间记忆池摘要（frame.spatial_memory_pools、runtime_ctx 各字段）。
- Decision Monitor / Viewer 能显示分池结果（working/episode 摘要、stable/anchor 占位）。
- 不同 dominant_skeleton 下，working / episode 分池偏好会变化（如 navigation 时 episode 含路径相关；observation 时 episode 含 focus_region 摘要）。
- suppress 的内容不会直接进入 stable/anchor（仅占位项可存在）。
- 不破坏主线 A、主线 2 第一阶段、M0、M1、M1.5、M2、Skeleton Mix M0、Skeleton Filter M0 链路。

---

## 6. 当前哪些记忆分池字段已真实化，哪些仍预留

| 项目 | 状态 |
|------|------|
| 四层池结构（working/episode/stable/anchor）、SpatialMemoryItem 最小字段、build_spatial_memory_pools 规则型分池、frame/runtime_ctx/Viewer 接入 | **真实化**：每帧由 build_spatial_memory_pools 产出并写入 frame、runtime_ctx、Viewer。 |
| working_memory_items、episode_memory_items 内容 | **真实化**：来自 local_goal_spatial_map 与 local_goal_spatial_relations，按 keep 与 dominant 写入。 |
| stable_memory_items、anchor_memory_items | **占位**：当前仅 1 条 placeholder 项，无真实证据门槛与写入策略。 |
| use_count、conflict_count、last_used_ts | **预留**，未在分池逻辑中写入。 |
| 遗忘机制、TTL/Task-End/Value Decay、证据门槛、冲突替代、持久化、情感记忆、attention_weight、Hypothesis Layer 联动 | **未实现**，本轮不做。 |

---

## 7. 本轮是否通过

- **是**。验收满足：运行时存在可读的四层空间记忆池摘要；Decision Monitor / Viewer 能显示分池结果；不同 dominant 下 working/episode 偏好会变化；suppress 内容不直接进 stable/anchor；不破坏既有链路。当前仅完成分池，复杂遗忘、证据门槛、冲突替代尚未实现。
