# risk_interrupt_v1 首个观察窗口结论归档（V1）

> 结论口径：本归档只允许三选一（维持 / 退回 Level 1 / 回到 Level 0），禁止出现“顺手扩大边界”的结论。

---

## 1. 观察窗口基本信息

- **窗口起止（UTC）**：`2026-04-09T05:52:50Z` → `2026-04-09T05:52:50Z`（受控窗口：基于回归脚本生成的 trace）
- **窗口时长**：`~秒级（受控）`
- **样本量口径**：以 `request_id` 为主键聚合
- **trace 来源**：
  - `logs/risk_interrupt_level2_pilot_v1_test.jsonl`
  - `logs/risk_interrupt_cancel_replace_v1_test.jsonl`
  - `logs/risk_interrupt_state_transition_v1_test.jsonl`
- **analyzer 输出**：
  - `logs/analyze_risk_interrupt_v1_pilot_20260409T055250Z.md`
  - `logs/analyze_risk_interrupt_v1_pilot_20260409T055250Z.json`
- **开关快照（窗口内，受控脚本驱动）**：
  - `LUNA_ENABLE_RISK_INTERRUPT_V1`: 发生过 `1 → 0`（用于验证 `any_to_level0` telemetry）
  - `LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT`: 发生过 `1 → 0`（用于验证 `level2a_to_level1` telemetry）
  - `LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT`: 保持开启（用于验证 Level2B 观测字段）
  - `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1`: 开启（用于产出主线 trace）

> 备注：本窗口是“首个可控窗口”（回归脚本组合），目的是验证观测面与聚合链路是否可用；不用于评价线上稳定性。

---

## 2. 核心指标（按 request_id 聚合）

（来自 `metrics_by_request_id`）

- **preempt_before_submit_count**：`2`
- **cancel_replace_attempt_count**：`5`
- **cancel_replace_chain_closed_rate**：`0.2`（1/5）
- **fallback_to_preempt_before_submit_count**：`2`
- **fallback_to_level1_count**：`2`
- **fallback_to_level0_count**：`1`
- **suspicious_count**：`3`

---

## 3. 样本复核结论

### 3.1 success 抽检（3 条）

抽样条目（来自 analyzer `success`）：

- Level2A：`request_id=5875ef86-0bb9-4384-8334-3073b4a27976`（risk_level=high, prompt）
- Level2B：`request_id=41745916-1275-458e-be13-9f93689647b3`（replacement_request_id 存在）
- Level2A：`request_id=9a616c25-2f9b-4649-a5c6-8e1356cdc8ad`（risk_level=high, prompt）

结论：

- 成功样本中两条路径均可在 trace 中被识别与聚合；Level2B 成功样本具备 `replacement_request_id`。
- 本窗口用于验证“可观测/可对账链路”而非稳定性阈值；success 样本符合预期形态。

### 3.2 fallback 抽检（4 条）

主要失败原因（来自 analyzer `fallback`）：

- `no_pending_request`：2 条（Level2B pending-only 的预期失败路径）
- `failure_reason=""`：2 条（链不闭合但 failure_reason 为空 → 进入 suspicious 复核）

结论：

- `no_pending_request` 属于试点边界内的“立即回退到 Level2A”的合理情况（pending-only 试点的常见路径）。
- failure_reason 为空的 fallback 样本需要继续追踪：这更像“观测字段/导出不足”或“测试输入未覆盖到明确原因”，不应被解释为扩边界的理由。

### 3.3 suspicious 复核（必须）

类型分布（3 条）：

- `cancel_replace_unclosed_without_reason`：2
- `cancel_replace_out_of_bounds_risk_level`：1（risk_level=low）

是否存在硬越界（本窗口结论）：

- **非 high/critical 触发**：本窗口出现 `risk_level=low` 的 cancel+replace “观测样本”。该样本来自受控脚本/回归输入，用于验证 P1 字段与越界检查能被 analyzer 捕获；未发现“低风险仍执行 cancel+replace 并链闭合”的事实。
- **非 prompt/confirmation 触发**：未观察到。

观测链断裂：

- `cancel_replace_unclosed_without_reason` 表示“链不闭合且 failure_reason 为空”，需要在后续真实窗口中优先关注其发生率与具体 request_trace 细节。

---

## 4. 单选结论（必须单选）

- [x] **继续维持当前试点**
- [ ] 退回 Level 1
- [ ] 回到 Level 0

### 4.1 结论理由（可对账）

- 本窗口的目标是验证“观测面可用性”而非稳定性：P0 回退 telemetry 与 P1 越界字段均已被 analyzer 消费，指标可落盘、可抽样复核。
- 可疑样本已被成功导出并分类（suspicious_count=3），说明“发现问题→导出样本→人工复核”的闭环成立。
- 本窗口内的 `fallback_to_level1_count / fallback_to_level0_count` 来自受控脚本的 `operator_toggle` 演练，不代表系统自动回退或不可控风险；因此不作为退回依据。

---

## 5. 禁止事项（再次写死）

- 不允许在本结论后提出“顺手扩大边界”
- 不允许放开 started playback
- 不允许扩大输出类型/旁路范围
- 不允许引入恢复/重播/多 request 编排

---

## 6. 附录

- analyzer 输出：
  - `logs/analyze_risk_interrupt_v1_pilot_20260409T055250Z.md`
  - `logs/analyze_risk_interrupt_v1_pilot_20260409T055250Z.json`

