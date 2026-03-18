# 主线 2 第二阶段：Object Temporal Ledger M1 交付说明

**依据**：Object Temporal Ledger M0 已完成；主线 2 第二阶段 M1 目标  
**目标**：将单对象时空账本从“最小载体”推进为“可支撑对象级时空推断的增强版”，重点增强事件链表达、容器状态表达、用户确认写回、**最后可信位置与当前候选位置分离**。本轮仍为单对象优先，不做多对象全场账本、复杂 re-id、长期持久化与经验沉淀。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/object_temporal_ledger.py` | **M1 升级**。ObjectTemporalEntry 新增 last_confirmed_ts、current_candidate_location、current_candidate_ts、current_container_confidence、user_confirmed_location、user_confirmed_ts；EVENT_TYPES 扩展 object_carried/object_placed/container_closed/user_confirmed_location/user_denied_location；VISIBILITY_STATUSES 增加 confirmed_visible；ObjectTemporalLedger 新增 ledger_state_summary；build 增加 prev_last_confirmed_*、object_user_confirmed_location、object_user_denied_location 参数，实现用户确认/否认写回与 last_confirmed/current_candidate 分离；事件规则 object_seen/object_lost_visibility/object_candidate_in_container/container_opened 占位；events 最多 8 条。 |
| `decision_monitor/builder.py` | 调用 build_object_temporal_ledger 时传入 prev_last_confirmed_location/ts、object_user_confirmed_location、object_user_denied_location（来自 ctx）。 |
| `runtime/context.py` | 新增 object_last_confirmed_ts、object_current_candidate_location；注释明确 last_confirmed=可信、candidate=候选。 |
| `main.py` | 对象账本写回 runtime_ctx 时增加 object_last_confirmed_ts、object_current_candidate_location。 |
| `tools/decision_monitor_viewer.py` | 卡片升级为 M1：展示最后可信位置+ts、当前候选位置+ts、容器候选+置信度、visibility、ledger_confidence、状态摘要、最近 3～5 条事件；sections 增加 ledger_state_summary。 |
| `decision_monitor/CONTRACT.md` | object_temporal_ledger 段落更新为 M0/M1；已支持最小用户确认写回与最后可信 vs 当前候选分离；未实现项更新。 |
| `docs/MAINLINE_2_OBJECT_TEMPORAL_LEDGER_M1_DELIVERY.md` | **新建**。本文档。 |

---

## 2. M1 数据结构升级说明

### ObjectTemporalEntry（M1）

| 字段 | 类型 | 含义 |
|------|------|------|
| object_label | str | 对象标签 |
| object_profile_summary | str | 简要画像 |
| **last_confirmed_location** | str | **最后可信位置**（仅用户确认或强支持更新） |
| **last_confirmed_ts** | float | 最后可信位置时间戳 |
| **current_candidate_location** | str | **当前候选位置**（假设/推断，不写回 last_confirmed） |
| **current_candidate_ts** | float | 当前候选时间戳 |
| last_seen_ts | float | 兼容 M0 |
| visibility_status | str | visible / occluded / lost / container_candidate / confirmed_visible / unknown |
| current_container_candidate | str | 当前容器候选 |
| **current_container_confidence** | float | 容器候选置信度 |
| current_hypothesis_summary | str | 当前假设摘要 |
| ledger_confidence | float | 账本置信度 |
| **user_confirmed_location** | str | 用户确认的位置（可选） |
| **user_confirmed_ts** | float | 用户确认时间戳（可选） |

### LedgerEvent（M1 事件类型）

- object_seen / object_picked / object_carried / object_placed  
- object_lost_visibility  
- container_opened / container_closed  
- object_candidate_in_container  
- user_confirmed_location / user_denied_location  

### ObjectTemporalLedger（M1）

| 字段 | 类型 | 含义 |
|------|------|------|
| focus_object_entry | ObjectTemporalEntry | 当前关注单对象条目 |
| events | List[LedgerEvent] | 事件链（最多 8 条） |
| ledger_reason | str | 生成原因 |
| **ledger_state_summary** | str | **可读状态摘要**（最后可信/候选/可见性/事实已确认或候选中） |

---

## 3. 事件链增强规则说明

- **object_seen**：存在 focus/confirm/interaction/path 相关支持且对象位置可引用时生成。  
- **object_lost_visibility**：hypothesis 为 occluded_object_candidate 或 evidence/pools 显示对象缺失时生成。  
- **object_candidate_in_container**：hypothesis_type == container_candidate 时生成，并更新 current_container_candidate、current_candidate_location（若可推）。  
- **container_opened / container_closed**：当前阶段基于 hypothesis（如 container_candidate 时生成 container_opened 占位）的弱规则占位；不要求真实视觉识别开关门动作。  
- **user_confirmed_location / user_denied_location**：由 ctx 注入 object_user_confirmed_location、object_user_denied_location 触发，写入事件链并更新账本。

每帧至多新增有限数量事件，events 保留最近 8 条，避免事件洪水。

---

## 4. 用户确认写回规则说明

- **ctx.object_user_confirmed_location 存在时**：  
  - 更新 last_confirmed_location、last_confirmed_ts、user_confirmed_location、user_confirmed_ts；  
  - visibility_status 可提升为 confirmed_visible 或保持 visible；  
  - 追加 event：user_confirmed_location。  

- **ctx.object_user_denied_location 存在时**：  
  - 若与 current_candidate_location 或 current_container_candidate 冲突，则降低候选置信度或清空候选；  
  - 追加 event：user_denied_location。  

当前阶段仅做最小写回，不做复杂冲突传播。

---

## 5. 最后可信位置 vs 当前候选位置分离规则说明

- **last_confirmed_*** 仅在以下情况更新：  
  - 用户通过 ctx 提供 object_user_confirmed_location；或  
  - 无上一帧 last_confirmed 且当前有强支持（visible + location + working）时首帧写入 smap 位置。  
- **current_candidate_*** 由 hypothesis/container_candidate/path 推断更新，**不得**用弱候选覆盖 last_confirmed。  
- 上一帧的 last_confirmed_* 通过 ctx（runtime_ctx 写回）传入 build，实现跨帧持久化。

---

## 6. Viewer 展示说明

- **卡片标题**：对象时空账本 / Object Temporal Ledger (M1)。
- **第一行**：关注对象、可见性、账本置信度。  
- **第二行**：**最后可信位置** @ ts、**当前候选位置** @ ts。  
- **第三行**：容器候选（截断）+ 置信度。  
- **第四行**：状态摘要（ledger_state_summary）。  
- **第五行**：最近事件（最近 3～5 条 event_type @ timestamp summary）。  
- **第六行**：ledger_reason。  
- sections 保留完整展开，含 focus_object_entry、events、ledger_reason、ledger_state_summary。

---

## 7. runtime_ctx 最小接入

| 字段 | 含义 |
|------|------|
| object_last_confirmed_location | 最后可信位置（优先表示可信） |
| object_last_confirmed_ts | 最后可信时间戳 |
| object_current_candidate_location | 当前候选位置 |
| object_visibility_status | 可见性状态 |
| object_container_candidate | 容器候选 |
| object_ledger_confidence | 账本置信度 |

若已有同名字段，语义已更新为：last_confirmed_* = 可信位置，candidate_* = 当前候选。

---

## 8. 当前真实化与预留

| 项目 | 状态 |
|------|------|
| ObjectTemporalEntry 全部 M1 字段 | 真实化 |
| LedgerEvent 扩展事件类型 | 真实化（规则型生成，非视觉动作识别） |
| last_confirmed 与 current_candidate 分离 | 真实化 |
| 用户确认/否认 ctx 写回 | 真实化（最小写回） |
| ledger_state_summary | 真实化 |
| Viewer 最后可信/当前候选/事件/状态摘要 | 真实化 |
| container_opened/container_closed | 弱规则占位 |
| object_picked/object_carried/object_placed | 类型已支持，生成规则可后续按需扩展 |
| 多对象全场账本、复杂 re-id、长期持久化、经验沉淀 | 未实现（本轮不做） |

---

## 9. 验收与约束

- **验收**：运行时可读 Object Temporal Ledger M1；last_confirmed_location 与 current_candidate_location 已分离；至少数种事件类型在事件链中体现；支持 ctx 注入用户确认/否认写回；Viewer 能清晰展示“最后可信位置 vs 当前候选位置”；不破坏 M0、主线 A、主线 2 第一阶段、Skeleton Mix/Filter、Spatial Memory、Evidence Ledger、Hypothesis、Recheck 等链路。  
- **约束**：不做多对象全场账本、复杂 re-id、持久化数据库、经验沉淀、复杂容器视觉识别、detector/OCR/动态策略主链改造、新全局状态机。

---

**本轮是否通过**：待运行测试与人工确认后标注。
