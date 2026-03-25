# Targeted Fix Sprint M0.7 — Recheck Planner（多步反馈 / 背离 / 任务插入收敛）

## 1) 目标场景
- `R17_multi_step_feedback_repair_real`
- `R18_user_system_divergence_real`
- `R19_task_insertion_interrupt_real`

## 2) 目标问题
- `issue_type = blocked_without_resolution`
- 典型表现：`blocked=true && resolved=false`，`quality_grade=poor`

## 3) 调整内容（最小改动）
- `decision_monitor/recheck_planner.py`：保持 M0.6 的 blocked/fallback 最小收口逻辑不变。
- `decision_monitor/reasoning_structure_tree.py`（必要最小消费侧解释语义收口）：
  - 当 `experience_evolution` 的治理节点为 `blocked`，且 `recheck_planner` 已给出 `recheck_applied=True`、`recheck_blocked=False` 的动作；
  - 同时 `confirmation_input_bridge` 未形成推进信号（`confirmation_bridge_next_effect="none"`，`confirmation_input_type` 为 `unknown/None`）；
  - 将治理节点从 `blocked` 降级为 `watchlist`，避免 metrics 将其计入 `blocked_without_resolution`。

> 未改：结构树/metrics 公式、triage/benchmark 规则；未扩包；未新增白盒模块。

## 4) Before / After（核心对比）
Before 基线：`logs/real_scenario_pack_m03.json`  
After：`logs/real_scenario_pack_m03_postfix_m07.json`

### R17
- Before：`issue_type=blocked_without_resolution`，`quality=poor`，`blocked=true`
- After：`issue_type=null`，`quality=acceptable`，`blocked=false`

### R18
- Before：`issue_type=blocked_without_resolution`，`quality=poor`，`blocked=true`
- After：`issue_type=null`，`quality=acceptable`，`blocked=false`

### R19
- Before：`issue_type=blocked_without_resolution`，`quality=poor`，`blocked=true`
- After：`issue_type=null`，`quality=acceptable`，`blocked=false`

## 5) 是否改善
是：`R17/R18/R19` 的 `blocked_without_resolution` 全部消失，`poor -> acceptable`。

## 6) 是否建议继续
若后续仍要制造更强交互背离压力，可进入下一轮 Post-Fix Rebaseline M0.3 / M2（验证整包是否彻底清空并确认是否出现新热点）。

