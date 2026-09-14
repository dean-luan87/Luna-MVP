# Luna — Navigation Rollback And Interruption Governance Decision Minimal Implementation v0（治理决策层：最小非动作实现版）

**文件**：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-29：Navigation Rollback And Interruption Governance Decision Minimal Implementation v0（只产出统一决策对象，不触发治理动作）  

关联：
- 治理决策层边界冻结：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_V0.md`
- 治理入口边界冻结：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_V0.md`
- 治理入口最小非动作实现版：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_IMPLEMENTATION_V0.md`
- 执行期监控闭环实现版：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_IMPLEMENTATION_V0.md`
- 执行器状态对象实现版：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- takeover 接线最小非动作实现版：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_WIRING_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是最小回退 / 中断治理决策层的**正式实现版文档**（最小非动作实现）。
- 当前目标：把治理决策层从冻结文档推进到“可产出统一治理决策结果对象”的最小实现。
- 当前不做真实回退动作。
- 当前不做真实中断治理动作。
- 当前不做真实释放控制权动作。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal/不触发中台真实迁移）。

---

## B. 为什么现在要先实现治理决策层

- governance entry 已有 implemented object（且可在主链产出）。
- executor status / monitoring status 都已有 implemented object。
- decision 结果集合与最小判断原则已冻结。
- 若没有最小实现，后续治理链仍会回到临时判断/散字段判断，破坏可回归与边界治理。
- 因此必须先把治理决策对象实现出来。
- 但当前仍不能触发真实治理动作（只产出决策对象）。

---

## C. implemented governance decision 的最小定义（写死）

- 它不是回退治理器。
- 不是中断治理器。
- 不是释放控制权执行器。
- 不是 formal decision。
- 它是“治理入口打开后的最小分类决策对象”的正式实现版。
- 作用：把入口内问题统一收束为建议性治理决策结果。

---

## D. 当前最小输入依据（写死）

当前只允许消费标准化对象：

1) implemented `navigation_rollback_and_interruption_governance_entry_v0`
   - 且 `governance_entry_status == "governance_entry_open"`
2) implemented `navigation_real_executor_status_v0`
3) implemented `navigation_execution_monitoring_status_v0`
4) 可选只读 `navigation_executor_takeover_wiring_v0`
   - 仅作接线状态一致性校验，不得扩权

并写死：

- 禁止直接读 `candidate / gate / stub / raw metadata`
- 没有合法治理入口对象时，不得产出治理决策

---

## E. 当前最小输出位（写死）

固定写入：

- `result.metadata["navigation_rollback_and_interruption_governance_decision_v0"]`

最小结构：

```json
{
  "governance_decision_attempted": true,
  "governance_decision_scope": "navigation_rollback_and_interruption_governance_decision_v0",
  "governance_decision_status": "hold_for_governance|recommend_interrupt|recommend_rollback|recommend_release_control|governance_decision_blocked",
  "reason": "..."
}
```

约束（写死）：

- 不加时间/空间字段
- 不膨胀成复杂对象
- 只表达“最小治理决策分类结果”

输出口径（写死一致）：

- 有合法 governance entry object 且 status==open 时：输出五态之一（或 blocked）
- 完全无入口对象时：relevant-only 不写

---

## F. 当前最小判断规则（克制）

- 明确失败 / 明确不可执行 → `recommend_rollback`
- 明确中断 / takeover 异常释放 → `recommend_release_control` 或 `recommend_interrupt`
- 退化 / 偏航 / 需上游介入但不足以判定回退 → `hold_for_governance` 或 `recommend_interrupt`
- 入口打开但对象不完整/一致性不足 → `governance_decision_blocked`

注意（写死）：

- 当前不扩复杂优先级树
- 先保证最小分类结果稳定

---

## G. 当前最小语义（写死）

当 `navigation_rollback_and_interruption_governance_decision_v0` 被产出时，只表示：

- 系统已能对治理入口内问题做最小分类决策
- 上游治理链未来可合法消费该决策对象
- 不表示真实回退已执行
- 不表示真实中断已执行
- 不表示控制权已真实释放
- 不表示路线已改变
- 不表示中台已真实迁移

---

## H. 当前不允许做什么（写死）

- 不允许真实回退动作
- 不允许真实中断动作
- 不允许真实释放控制权动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把任何 `recommend_*` 当治理已执行

---

## I. 落地位置（实现落点）

- builder：`capabilities/mid_platform/runtime/navigation_rollback_and_interruption_governance_decision_v0.py`
- metadata 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`

