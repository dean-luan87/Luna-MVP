# 主线 2 第二阶段 M2：Local Goal Spatial Map 区域关系化交付说明（最小版）

**依据**：M1.5 标尺层 + `docs/LOCAL_SPATIAL_SCALE_CONSTITUTION.md` v1.0  
**范围**：仅最小区域关系层，不做 3D、occupancy 网格、语义拓扑、对象级关系、长时记忆。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/local_goal_spatial_relations.py` | **新建**。SpatialRelation 数据结构；RELATION_TYPES 四类；SECTOR_NEIGHBORS、DISTANCE_BAND_ORDER；build_relations(smap) 规则型生成 adjacent_to / overlaps_with / supports / conflicts_with |
| `decision_monitor/schema.py` | 引入 SpatialRelation；DecisionMonitorFrame 新增 local_goal_spatial_relations: Optional[List[SpatialRelation]] |
| `decision_monitor/builder.py` | 引入 local_goal_spatial_relations；build 中调用 build_relations(local_goal_spatial_map)，写入 frame |
| `tools/decision_monitor_viewer.py` | 新增卡片「局部空间关系 / Local Goal Spatial Relations (M2)」；展示 source → target、relation_type、confidence、reason；sections 增加 local_goal_spatial_relations |
| `decision_monitor/CONTRACT.md` | 补充 local_goal_spatial_relations（M2）字段与四类关系规则说明 |

---

## 2. 关系数据结构说明

### 2.1 SpatialRelation（单条关系）

| 字段 | 类型 | 含义 |
|------|------|------|
| source_region_type | str | 源区域类型：focus_region / traversable_region / risk_region / confirm_region |
| source_priority_rank | int | 源区域优先级 1/2/3 |
| target_region_type | str | 目标区域类型 |
| target_priority_rank | int | 目标区域优先级 |
| relation_type | str | adjacent_to / overlaps_with / supports / conflicts_with |
| confidence | float | 0~1 |
| reason | Optional[str] | 规则原因说明 |

### 2.2 关系类型仅限四类

- **adjacent_to**：空间邻接（扇区邻接 + 距离带接近）
- **overlaps_with**：空间重叠（同扇区或扇区接近且距离带一致）
- **supports**：支撑（confirm 支撑 focus；traversable 支撑 goal）
- **conflicts_with**：冲突（risk 与 traversable 在相近扇区/带；risk 与 focus/confirm 冲突）

---

## 3. 四类关系最小规则说明

| 关系类型 | 触发条件 | 说明 |
|----------|----------|------|
| **adjacent_to** | 不同 region_type 的两区域，sector 在 SECTOR_NEIGHBORS 中邻接，且 distance_band 同带或相邻带（immediate/near, near/mid, mid/far） | 基于 M1.5 的 sector + distance_band |
| **overlaps_with** | 两区域同 sector 且 distance_band 接近 | 同扇区同/近带 |
| **supports** | confirm_region 与 focus_region 扇区重叠 → confirm 支撑 focus；traversable_region 与 focus 主区扇区重叠 → traversable 支撑 goal（以 focus 主区代理） | 规则型，无对象级 |
| **conflicts_with** | risk_region 与 traversable_region 扇区重叠且距离带接近 → risk 与 traversable 冲突；risk_region 与 focus_region/confirm_region 扇区重叠 → risk 与 focus/confirm 冲突（置信度参与 confidence） | 高 urgency 风险对当前 focus/confirm 的冲突 |

关系数量上限 20 条，避免爆炸。

---

## 4. 样本运行结果（测试）

- 见下方「本轮是否通过」；验收包含：至少生成 supports / conflicts_with 两类有效关系；relations 进入 frame / viewer；不同 goal/state 下关系会变化；不破坏 M0/M1/M1.5 链路。

---

## 5. 当前哪些关系字段已真实化，哪些仍规则型占位

| 项目 | 状态 |
|------|------|
| source/target region_type、priority_rank | **真实化**：来自 LocalGoalSpatialMap 四类区域与 priority_rank |
| relation_type、confidence、reason | **规则型占位**：由 build_relations 内规则与 sector/band 计算得出，非上游感知/推理直接输出 |
| 扇区邻接、距离带接近 | **规则型**：SECTOR_NEIGHBORS、DISTANCE_BAND_ORDER 固定表；未接真实几何/occupancy |

---

## 6. 本轮是否通过

- **是**。验收满足：  
  1）至少能生成 supports、conflicts_with 两类有效关系（有 confirm/focus 或 risk/traversable 时即会产生）；  
  2）local_goal_spatial_relations 进入 frame，Viewer 卡片与 sections 可展示 source、target、relation_type、confidence、reason；  
  3）不同 goal/state（如 detector_floor_due、risk_score 高、recheck_required）下区域集合变化，关系随之变化；  
  4）未改动 Dynamic Policy / Scene Gate / B2 / detector / OCR；主线 A、主线 2 第一阶段、M0、M1、M1.5 既有链路与单测未破坏。
