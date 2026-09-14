# risk_interrupt_v1 试点观察窗口结论模板（V1）

> 用途：每次跑完一个观察窗口后，基于既有 trace + analyzer + telemetry，快速收敛到一个**单选结论**：维持 / 退回 Level 1 / 回到 Level 0。  
> 约束：本模板**不讨论扩边界**，禁止出现“顺手扩大一点”的结论口径。

---

## 1. 观察窗口基本信息

- **窗口起止（UTC）**：`<YYYY-MM-DDTHH:MM:SSZ>` → `<YYYY-MM-DDTHH:MM:SSZ>`
- **窗口时长**：`<N days/hours>`
- **样本量口径**：以 `request_id` 为主键统计
- **trace 来源（文件/位置）**：
  - `<path-or-location-1>`
  - `<path-or-location-2>`
- **使用的聚合工具版本**：`tools/analyze_risk_interrupt_v1_pilot.py`（当前输出文件名：`logs/analyze_risk_interrupt_v1_pilot_<UTC>.{md,json}`）
- **试点开关快照（窗口内）**：
  - `LUNA_ENABLE_RISK_INTERRUPT_V1=<0/1>`
  - `LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT=<0/1>`
  - `LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT=<0/1>`
  - `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1=<0/1>`

---

## 2. 核心指标（填写区）

> 从 analyzer 的 `metrics_by_request_id` 中复制即可；所有指标必须以 `request_id` 聚合口径为准。

- **preempt_before_submit_count**：`<int>`
- **cancel_replace_attempt_count**：`<int>`
- **cancel_replace_chain_closed_rate**：`<float or null>`
- **fallback_to_preempt_before_submit_count**：`<int>`
- **fallback_to_level1_count**：`<int>`
- **fallback_to_level0_count**：`<int>`
- **suspicious_count**：`<int>`（定义：analyzer 输出的 suspicious 样本条数；若有去重规则请注明）

---

## 3. 样本复核结论（填写区）

### 3.1 success 样本抽检

- **抽检样本数**：`<N>`
- **结论**：
  - `<要点 1>`
  - `<要点 2>`

### 3.2 fallback 样本抽检

- **抽检样本数**：`<N>`
- **主要失败原因分布**（按 reason / failure_reason 聚类）：
  - `<reason A>: <count>`
  - `<reason B>: <count>`
- **结论**：
  - `<要点 1>`
  - `<要点 2>`

### 3.3 suspicious 样本复核（必须）

- **suspicious 类型分布**（按 `problem` 聚类）：
  - `<problem A>: <count>`
  - `<problem B>: <count>`
- **是否存在越界（硬约束违背）**：
  - 非 `high/critical` 触发：`<yes/no>`
  - 非 `prompt/confirmation` 触发：`<yes/no>`
- **是否存在观测链断裂导致不可对账**：`<yes/no>`
- **复核结论**：
  - `<要点 1>`
  - `<要点 2>`

---

## 4. 单选结论区（必须单选）

> 只允许以下三项之一；不得添加“顺手扩大边界”的备注。

- [ ] **继续维持当前试点**
- [ ] **退回 Level 1**
- [ ] **回到 Level 0**

### 4.1 结论理由（1–3 条，必须可对账）

- `<理由 1：引用关键指标 + 样本复核事实>`
- `<理由 2：引用关键指标 + 样本复核事实>`
- `<理由 3（可选）>`

---

## 5. 不允许写入的内容（写死）

- 不允许写“感觉还行，顺手扩大边界”
- 不允许提出“放开 started playback”
- 不允许放开到更多输出类型
- 不允许扩到其他旁路
- 不允许引入恢复/重播/多 request 编排

---

## 6. 附录（可选）

- analyzer 输出文件：
  - `<logs/analyze_risk_interrupt_v1_pilot_<UTC>.md>`
  - `<logs/analyze_risk_interrupt_v1_pilot_<UTC>.json>`
- 关键样本 `request_id` 列表（用于复盘）：
  - success：`[...]`
  - fallback：`[...]`
  - suspicious：`[...]`

