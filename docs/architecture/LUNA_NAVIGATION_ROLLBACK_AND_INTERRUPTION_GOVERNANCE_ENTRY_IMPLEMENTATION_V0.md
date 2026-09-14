# Luna — Navigation Rollback And Interruption Governance Entry Minimal Implementation v0（治理入口：最小非动作实现版）

**文件**：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-27：Navigation Rollback And Interruption Governance Entry Minimal Implementation v0（只产出统一入口对象，不触发治理动作）  

关联：
- 治理入口边界冻结：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_V0.md`
- 执行期监控闭环实现版：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_IMPLEMENTATION_V0.md`
- 执行器状态对象实现版：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- takeover 接线最小非动作实现版：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_WIRING_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是最小回退 / 中断治理入口的**正式实现版**文档（最小非动作实现）。
- 当前目标：把治理入口从冻结文档推进到“可产出统一治理入口结果对象”的最小实现。
- 当前不做真实回退动作。
- 当前不做真实中断治理动作。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal/不驱动迁移）。

---

## B. 为什么现在要先实现治理入口

- executor status object 已有 implemented object。
- monitoring status object 已有 implemented object。
- governance entry 设计边界已冻结。
- 若没有最小实现，后续治理链仍会回到“临时判断/散字段判断”，破坏可回归与越权边界。
- 因此必须先把入口对象实现出来。
- 但当前仍不能触发任何真实治理动作（只产出入口结果对象）。

---

## C. implemented governance entry 的最小定义（写死）

- 它不是回退治理器。
- 不是中断治理器。
- 不是 formal decision。
- 它是“是否打开治理入口”的最小非动作实现。
- 作用：把执行器/监控链上的异常与治理候选信号，收束成统一入口结果。

---

## D. 当前最小输入依据（写死）

当前只允许消费标准化对象：

1) implemented `navigation_real_executor_status_v0`  
2) implemented `navigation_execution_monitoring_status_v0`  
3) 可选只读 `navigation_executor_takeover_wiring_v0`
   - 仅作接线状态一致性校验，不得扩权

并写死：

- 禁止直接读 `candidate / gate / stub / raw metadata`
- 缺少最小标准化对象时，不得打开治理入口

---

## E. 当前最小输出位（写死）

固定写入：

- `result.metadata["navigation_rollback_and_interruption_governance_entry_v0"]`

最小结构：

```json
{
  "governance_entry_attempted": true,
  "governance_entry_scope": "navigation_rollback_and_interruption_governance_entry_v0",
  "governance_entry_status": "governance_entry_open|governance_entry_not_applicable|governance_entry_blocked",
  "reason": "..."
}
```

约束（写死）：

- 不加时间/空间字段
- 不膨胀成复杂对象
- 只表达“治理入口是否打开”

输出策略（写死一致口径）：

- 当 executor status + monitoring status 两个标准化对象都存在且合法时：输出三态之一
- 当两个标准化对象都不存在：relevant-only 不写

---

## F. 当前最小判断规则（非常克制）

规则 1：出现有资格进入治理入口的事件 → `governance_entry_open`

最小支持集合（来自 implemented 对象的明确语义 token）：

- `execution_failed`
- `execution_interrupted`
- `execution_degraded`
- 明确偏航（`explicit_offroute`）
- 明确不可执行（`explicit_unexecutable`）
- takeover 异常释放（`takeover_abnormal_release`）
- 其他明确要求上游介入（`requires_upstream_intervention`）

规则 2：对象存在但条件不足 / 一致性不满足 → `governance_entry_blocked`

例如：

- scope / object_kind 不合法
- 标准化对象缺失（仅存在其一）
- wiring 结果存在但明显不一致（仅作一致性校验）

规则 3：对象存在但没有治理入口事件 → `governance_entry_not_applicable`

注意（写死）：

- 当前不扩复杂原因树
- 先保证治理入口结果统一输出

---

## G. 当前最小语义（写死）

当 `navigation_rollback_and_interruption_governance_entry_v0` 被产出时，只表示：

- 系统已能识别“是否应打开治理入口”
- 上游治理链未来可合法消费该结果
- 不表示真实回退已发生
- 不表示真实中断治理已发生
- 不表示路线已改变
- 不表示中台已迁移状态

---

## H. 当前不允许做什么（写死）

- 不允许真实回退动作
- 不允许真实中断治理动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `governance_entry_open` 当治理已执行

---

## I. 落地位置（实现落点）

- builder：`capabilities/mid_platform/runtime/navigation_rollback_and_interruption_governance_entry_v0.py`
- metadata 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`

