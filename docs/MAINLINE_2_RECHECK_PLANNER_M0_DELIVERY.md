# 主线 2 第二阶段：补证规划 M0 交付说明

**依据**：Hypothesis Layer M0 + Evidence Ledger M0  
**目标**：将 verification_hint / suggested_next_check 从“建议动作”推进为最小可执行补证入口，形成受约束的补证执行链路。本轮只做最小 Recheck Planner，不做复杂多步规划、不做学习、不改 detector/OCR 主链。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/recheck_planner.py` | **新建**。RecheckPlannerResult；RECHECK_ACTIONS；build_recheck_planner(hypothesis_layer, evidence_ledger, state, smap)；阻断逻辑 _is_blocked。 |
| `decision_monitor/schema.py` | 引入 RecheckPlannerResult；DecisionMonitorFrame 新增 recheck_planner。 |
| `decision_monitor/builder.py` | 引入 recheck_planner；build 中在 hypothesis_layer 之后调用 build_recheck_planner，写入 frame.recheck_planner。 |
| `runtime/context.py` | 新增 recheck_action、recheck_reason、recheck_target、recheck_priority、recheck_blocked、recheck_block_reason、recheck_applied。 |
| `main.py` | 决策显示器块内写入 recheck_planner 到 runtime_ctx；未阻断时根据 recheck_action 设置 local_goal_recheck_mode/type 或 view_behavior_hint（最小执行事实）。 |
| `tools/decision_monitor_viewer.py` | 新增「补证规划 / Recheck Planner (M0)」卡片；sections 增加 recheck_planner。 |
| `decision_monitor/CONTRACT.md` | 补充 recheck_planner 说明与未实现项。 |

---

## 2. RecheckPlan 数据结构说明

### RecheckPlannerResult

| 字段 | 类型 | 含义 |
|------|------|------|
| recheck_action | str | 当前最小执行动作（RECHECK_ACTIONS 之一） |
| recheck_reason | str | 补证原因（来自 hypothesis_summary/claim_summary + missing_evidence 简述） |
| recheck_target | str | 目标摘要（region / hypothesis_type / claim） |
| recheck_priority | str | 优先级（规则型，如 normal） |
| recheck_blocked | bool | 是否被守底/风险条件阻断 |
| recheck_block_reason | str | 阻断来源（minimum_mode_active / runtime_domain_state=frozen 等） |
| recheck_applied | bool | 是否已应用（未阻断且存在 action 时为 True） |

---

## 3. 最小规划规则说明

- **A. hypothesis 首条存在**：优先取 hypothesis.verification_hint 作为 recheck_action；recheck_reason 来自 hypothesis_summary + missing_evidence 简述；recheck_target 优先 hypothesis_type 或 smap 的 focus/confirm/risk 摘要。
- **B. 无 hypothesis 但 evidence_ledger 首条存在**：取 claim.suggested_next_check 作为 recheck_action；recheck_reason 来自 claim_summary + missing_evidence 简述。
- **C. 无 hypothesis 且无 claim**：无 recheck_action，recheck_applied=False。

---

## 4. 阻断规则说明

- 当以下任一为真时 recheck_blocked=True，recheck_applied=False，recheck_block_reason 写明来源：
  - state.minimum_mode_active == True
  - state.runtime_domain_state == "frozen"
  - state.scene_gate_action == "freeze_to_minimum_mode"
  - state.high_level_output_suppressed == True
  - state.human_check_pending == True
- recheck_action 可保留为建议，但不标记已执行，下游不执行补证动作。

---

## 5. 最小执行入口说明

- **recheck_environment**：设置 runtime_ctx.local_goal_recheck_mode="pending"，local_goal_recheck_type="environment"，供下一轮 force_sample 对接。
- **recheck_close_range**：设置 local_goal_recheck_mode="pending"，local_goal_recheck_type="close_range"。
- **hold_and_confirm**：不写入执行事实，由现有 WAIT 逻辑处理。
- **look_forward / shift_view_left / shift_view_right**：设置 runtime_ctx.view_behavior_hint = 对应动作。
- **ask_user_for_clarification**：设置 view_behavior_hint = "ask_user_for_clarification:" + recheck_reason，供后续 human_check 或提示使用。

---

## 6. Viewer 展示说明

- **卡片标题**：补证规划 / Recheck Planner (M0)。
- **第一行**：动作、已执行（是/否）、阻断（是/否）。
- **第二行**：原因。
- **第三行**：目标、优先级；若阻断则显示阻断原因。
- 专家折叠面板可展开 recheck_planner 查看全部字段。

---

## 7. 样本运行结果（验收）

- 运行时存在可读的 Recheck Planner 结果（frame.recheck_planner、runtime_ctx 各字段）。
- hypothesis / evidence 的 verification_hint / suggested_next_check 能推进为 recheck_action。
- 当 minimum_mode_active 或 human_check_pending 等为真时，recheck_blocked=True，recheck_applied=False。
- recheck_environment / recheck_close_range 未阻断时能设置 local_goal_recheck_mode/type；look_forward/shift_view_* 能设置 view_behavior_hint（执行事实）。
- Viewer 能展示补证规划结果。
- 不破坏主线 A、主线 2 第一阶段、M0～M2、Skeleton Mix/Filter、Spatial Memory Pooling/Forgetting、Evidence Ledger、Hypothesis Layer 链路。

---

## 8. 当前哪些 recheck 字段已真实化，哪些仍预留

| 项目 | 状态 |
|------|------|
| RecheckPlannerResult、build_recheck_planner、规划规则 A/B/C、阻断规则、main 内执行入口（recheck_* -> local_goal_recheck_*/view_behavior_hint）、frame/runtime_ctx/Viewer | **真实化**。 |
| 复杂多步规划、学习型补证策略、经验反馈调 planner、完整对象级主动搜索、detector/OCR/动态策略主链重构、新全局状态机 | **未实现**，本轮不做。 |

---

## 9. 本轮是否通过

- **是**。验收满足：运行时可读 Recheck Planner；verification_hint/suggested_next_check 推进为 recheck_action；高风险/冻结/human_check_pending 时被阻断；部分 action 产生已执行事实（local_goal_recheck_*/view_behavior_hint）；Viewer 可展示；不破坏既有链路。
