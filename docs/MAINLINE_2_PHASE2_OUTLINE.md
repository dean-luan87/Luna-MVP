# 主线 2 第二阶段设计总纲（仅定义，不实现）

**阶段名称（建议）**：主线 2 第二阶段 — Local Goal Spatial Map（局部目标空间图）  
**目标**：把第一阶段的 `LocalGoalState` 从“文本/标签状态核”推进为“带空间结构的局部世界状态”。  
**注意**：依然是**局部**，不是全局地图；依然克制，不做 2.5D/3D 大工程。

---

## 1. 为什么现在进入第二阶段

第一阶段已经证明：局部目标状态可以稳定地驱动“做什么 / 何时复核 / 看哪里（优先级）”。  
第二阶段要解决的是：把“看哪里/通行哪里/风险在哪里/确认哪里”从文本提示，推进为**结构化的局部空间表达**，为后续更强的视角策略与复核策略提供更坚实的数据面。

---

## 2. 本阶段做什么（写死范围）

### 2.1 四类结构化区域（局部、短时）

- **focus_region_map**：关注区域结构化（目标相关的区域）
- **traversable_region_map**：通行区结构化（可通行/存疑/不可通行）
- **risk_region_map**：风险区结构化（风险来源/强度/持续性）
- **confirm_region_map**：关键确认区结构化（需要复核/需要 close-range 的区域）

> 第一版不要求几何精确；允许用**离散扇区/象限 + 置信度**表示（工程友好、可测）。

### 2.2 空间表达建议（工程化、最小）

建议用“视野扇区 + 置信度”的结构，而不是点云/三维：

- `sector`: {forward, left_front, right_front, near, unknown}
- `weight/confidence`: 0~1
- `evidence`: 来自 view_guard / scene_gate / runtime_domain_guard / navigation_result（可选）
- `ttl_ms`: 有效期（短时）

---

## 3. 最小数据结构（提案）

> 目标：可序列化、可在 Viewer 里直观看懂、可被主循环轻量消费。

### 3.1 LocalGoalSpatialMap（建议新结构）

- `goal_id`
- `goal_type`
- `produced_ts`
- `staleness_ms`
- `focus_sectors`: List[{sector, confidence, reason}]
- `traversable_sectors`: List[{sector, state, confidence, reason}]  # state: traversable/uncertain/blocked
- `risk_sectors`: List[{sector, risk_level, confidence, reason}]
- `confirm_sectors`: List[{sector, confirm_type, confidence, reason}]  # confirm_type: close_range/environment
- `summary`

### 3.2 与 LocalGoalState 的关系（写死）

- 第二阶段不替代 `LocalGoalState`，而是为其提供**结构化证据面**：
  - `LocalGoalState.goal_focus_region` 可来自 focus_sectors 的 top-1
  - `local_goal_view_priority` 可来自 focus/traversable/confirm 的组合规则
  - recheck 类型可来自 confirm_sectors 的 top-1

---

## 4. 本阶段不做什么（写死禁止项）

- 不做全局地图（global map）
- 不做长时记忆（long-term memory）
- 不做复杂对象跟踪（multi-object tracking）
- 不做 3D 重建 / 点云 / SLAM
- 不做通用 planner / 多目标竞争系统
- 不重构 Dynamic Policy / Scene Gate / B2
- 不接真实镜头硬控闭环（云台/自动转向）

---

## 5. 最小接入点（建议）

### 5.1 生成入口

- 在 `decision_monitor` 侧新增 `local_goal_spatial_map_builder.py`（只读汇聚）
- 输入：`LocalGoalState + state(view_guard/runtime_domain/scene_gate) + inputs(delta_t) + pipeline route_result(可选)`
- 输出：`LocalGoalSpatialMap`

### 5.2 消费入口（轻量）

- 主循环：像 2.1/2.2/2.3 一样，先写入 runtime_ctx，**只作为偏好层/证据层**被消费。
- Viewer：新增卡片“Local Goal Spatial Map（扇区图/条形权重）”，优先可读而非精确。

---

## 6. 最小验收标准（第一版 4 条）

1. 不同 goal 下，focus_sectors/confirm_sectors 分布不同（不是固定模板）
2. 随 view_guard/scene_gate 状态变化，sectors 会更新（短时、可解释）
3. 能支撑现有 2.3 的 view_priority 推导，并在 Viewer 中可复盘来源
4. 不破坏主线 A 与主线 2 第一阶段（2.0–2.3）链路与测试

---

## 7. 一句话

第二阶段要做的不是“更大世界”，而是把“局部行动内核”的证据面结构化：**把哪里重要/哪里可走/哪里风险/哪里需确认**变成可读可测的局部空间图。

