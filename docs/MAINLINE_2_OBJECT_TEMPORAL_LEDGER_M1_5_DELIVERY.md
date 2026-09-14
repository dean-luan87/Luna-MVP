# 主线 2 第二阶段：Object Temporal Ledger M1.5 交付说明（容器逻辑增强）

**依据**：Object Temporal Ledger M1 已完成（最后可信 vs 当前候选分离、最小事件链、用户确认写回）  
**目标**：将单对象对象账本从“有容器候选”推进为“具备最小容器逻辑”，重点增强容器状态表达、对象进入容器候选规则、容器候选置信度更新、用户否认后的候选回退，以及最后可信位置与容器候选位置的叙事一致性。  
**约束**：单对象优先；不做多对象全场账本、不做复杂视觉容器识别、不做长期持久化、不做经验沉淀、不改 detector/OCR/Dynamic Policy 主链、不新增全局状态机。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/object_temporal_ledger.py` | M1.5：新增 CONTAINER_STATES、CANDIDATE_LOCATION_TYPES；ObjectTemporalEntry 新增 container_state/container_last_event_ts/candidate_location_type；build 增加 prev_container_* 等输入并实现容器状态推进/回退与叙事一致性。 |
| `decision_monitor/builder.py` | build_object_temporal_ledger 传入上一帧容器候选/置信度/状态/容器事件时间戳与上一帧可见性。 |
| `runtime/context.py` | 新增 object_candidate_location_type、object_container_confidence、object_container_state、object_container_last_event_ts。 |
| `main.py` | monitor_ctx 增加上一帧容器状态字段；写回 runtime_ctx 增加 candidate_location_type/container_state/container_confidence/container_last_event_ts。 |
| `tools/decision_monitor_viewer.py` | 卡片升级为 M1.5：展示 candidate_location_type、container_state、container_confidence。 |
| `decision_monitor/CONTRACT.md` | object_temporal_ledger 段落更新为 M0/M1.5，写清最小容器逻辑与未实现项。 |
| `docs/MAINLINE_2_OBJECT_TEMPORAL_LEDGER_M1_5_DELIVERY.md` | **新建**。本文档。 |
| `tests/test_decision_monitor.py` | 新增/更新 M1.5 最小行为测试（见下文）。 |

---

## 2. M1.5 数据结构升级说明

### ObjectTemporalEntry（新增/明确）

- **current_container_candidate**：当前最可能的容器名/摘要（仍为字符串摘要）  
- **current_container_confidence**：容器候选置信度 \(0~1\)  
- **container_state**（枚举）：none / container_open_candidate / container_closed_candidate / object_inside_candidate / object_inside_confirmed（允许占位）  
- **container_last_event_ts**：最近一次容器状态相关事件时间戳  
- **candidate_location_type**（枚举）：direct_location / container_candidate / unknown，用于区分当前候选位置叙事

---

## 3. 容器逻辑增强规则说明（最小）

### 3.1 container_opened（弱规则）

- 当出现 hypothesis_type==container_candidate 时，生成 **container_opened（container_open_candidate 占位）**，并进入 container_open_candidate（若之前为 none 或 closed）。

### 3.2 object_candidate_in_container（推动 object_inside_candidate）

- 当 hypothesis_type==container_candidate：  
  - 更新 current_container_candidate/current_container_confidence  
  - current_candidate_location 叙事对齐到容器名/容器内候选  
  - candidate_location_type=container_candidate  
  - container_state 至少进入 object_inside_candidate

### 3.3 container_closed（弱规则占位）

- 当 container_state 已为 open_candidate 或 inside_candidate，且对象持续不可见（lost/occluded/container_candidate）并且 recheck_applied=True：  
  - 生成 container_closed（container_closed_candidate 占位）  
  - container_state→container_closed_candidate

### 3.4 候选优先级（容器候选优先）

- 当对象 lost/occluded 且存在容器候选：  
  - candidate_location_type 优先设置为 container_candidate  
  - direct_location 弱候选让位于容器叙事

---

## 4. 用户确认/否认下的容器回退规则说明

### 用户否认（user_denied_location）

- 若否认与 current_candidate_location 或 current_container_candidate 冲突：  
  - current_container_confidence 降低；低于阈值时清空 current_container_candidate  
  - 若 container_state 为 object_inside_candidate，则回退到 container_closed_candidate 或 none  
  - 必要时清空 current_candidate_location 与 candidate_location_type  
  - 追加事件 user_denied_location

### 用户确认（user_confirmed_location）

- 若确认位置文本指向“容器型位置”（最小启发式：含 抽屉/柜/盒/包/口袋/箱 等关键词）：  
  - current_container_candidate=current_candidate_location=该确认位置  
  - 提升 current_container_confidence  
  - candidate_location_type=container_candidate  
  - container_state 可进入 object_inside_confirmed（允许占位）  
- 同时按 M1 规则更新 last_confirmed_location/ts（用户明确确认）

---

## 5. 最后可信位置 vs 当前容器候选分离规则说明

- **last_confirmed_***：仅用户确认或强支持首帧写入更新；容器逻辑不得覆盖。  
- **容器逻辑**：仅更新 current_candidate_* 与容器状态字段，保持叙事一致性。

---

## 6. Viewer 展示说明

- 展示：last_confirmed_location+ts、current_candidate_location+ts、candidate_location_type、current_container_candidate+confidence、container_state、visibility_status、ledger_confidence、ledger_state_summary、最近 5 条事件。  
- sections 保留完整展开（focus_object_entry/events/ledger_reason/ledger_state_summary）。

---

## 7. runtime_ctx 最小接入

新增/同步字段：

- object_current_candidate_location
- object_candidate_location_type
- object_container_candidate
- object_container_confidence
- object_container_state
- object_container_last_confirmed_location（沿用 object_last_confirmed_location）
- object_last_confirmed_ts

语义：last_confirmed 仍表示可信位置；container_candidate/candidate_* 表示候选与容器叙事。

---

## 8. 当前哪些字段已真实化，哪些仍预留

| 项目 | 状态 |
|------|------|
| container_state/container_last_event_ts/candidate_location_type | 真实化（规则型推断） |
| container_opened/container_closed 事件 | 弱规则占位（非视觉识别） |
| object_inside_confirmed | 占位（由用户确认可触发） |
| 多对象、复杂 re-id、持久化、复杂容器视觉识别、经验沉淀 | 未实现（本轮不做） |

---

## 9. 验收

- 运行时可读 Object Temporal Ledger M1.5  
- 容器字段具备最小状态表达（candidate/confidence/state）  
- container_candidate 证据存在时可进入 object_inside_candidate  
- 用户否认可触发容器候选回退  
- last_confirmed 与 container_candidate/current_candidate 分离  
- Viewer 清晰展示最后可信 vs 当前容器候选状态  
- 不破坏既有主线与 M0/M1 链路

