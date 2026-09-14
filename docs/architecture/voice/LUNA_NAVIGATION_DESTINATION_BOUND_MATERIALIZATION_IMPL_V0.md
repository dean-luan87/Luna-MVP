# Navigation Destination Bound Materialization — Minimal Implementation Design v0

**文件**：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_MATERIALIZATION_IMPL_V0.md`  
**性质**：destination_bound 正式写入的最小实现设计（规则 + 最小落地，可冻结、可回归）  

上位约束（必须服从）：
- `docs/architecture/LUNA_WORLD_ENTRY_PRINCIPLE_V0.md`
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_SUFFICIENCY_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BINDING_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_FACT_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_CONFIRMATION_FACT_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_UPGRADE_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_MATERIALIZATION_V0.md`

并写死（继续成立）：
- **No Fabrication Rule**：不允许自动构造 `place_id/destination_id/...`；只能消费 `proposal` 中已有显式绑定字段；不得在本专题里做地点解析/检索。
- **统一时空锚点原则**：不新增任何模块自造时间/空间字段。
- **主链事实高于辅助信号**：语义/记忆/视觉只能做观测与阻断，不能替代写入依据。

---

## A. 文档定位

- 本文是 **destination_bound 正式写入** 的最小实现设计。
- 当前目标：把“正式事实层写入”落地（写入 `destination_bound_v0`），让主链第一次拥有“已确认导航目标”的正式事实层。
- 当前不做：
  - 真实导航启动（handoff 不执行）
  - 地图接入/地点解析/地点检索
  - 历史记忆/视觉补地点
  - 多轮导航对话扩展

---

## B. 当前写入前提（写死）

只有在以下前提**全部满足**时，才允许写入 `destination_bound_v0`：
- `proposal.task_action == "start_navigation"`
- `destination_candidate_v0.candidate_present == true`
- `destination_confirmation_fact_v0.confirmation_ready == true`
- `destination_bound_check_v0.bound_ready == true`
- `destination_bound_upgrade_eval_v0.eligible == true`
- `destination_bound_materialization_eval_v0.materialize_ready == true`

并写死：
- 任一不满足，都不得写入（本 v0 建议 relevant-only：不写该字段）。

---

## C. destination_bound 最小结构（写死）

写入位置：`result.metadata["destination_bound_v0"]`

最小结构（可冻结）：

```json
{
  "destination_bound": true,
  "binding_key": "destination_id",
  "binding_value": "dest_123",
  "binding_reason": "candidate_confirmed_and_materialization_ready",
  "bound_scope": "navigation_start_v0"
}
```

约束（写死）：
- 不加时间/空间字段
- 不混入地图状态/执行状态
- `binding_value` 只能来自 `proposal` 上已有显式绑定字段值

---

## D. 写入位置建议（只选一个）

**唯一推荐落点**：`dispatch_voice_final_text(...)` 的 `short_controlled_input` 分支中，紧跟 `destination_bound_materialization_eval_v0` 之后：
- 若满足 §B 全部硬条件，则写入 `result.metadata["destination_bound_v0"]`。

理由：
- 最连续：紧贴已完成的完整评估链（candidate→confirm→bound_check→upgrade_eval→materialization_eval）。
- 最不易失控：只写 metadata 事实位，不改 route/proposal/handoff/submit。
- 最可回归：写入条件完全由现有评估层硬结果决定，便于脚本化验证。

---

## E. 与 handoff 的关系（写死）

- 本轮即使写入 `destination_bound_v0`，也**不自动触发真实导航启动**。
- `navigation_handoff_v0` 本轮保持原状（可继续是 stub 的 not_ready/not_implemented），不改执行语义。
- 口径：**先有正式事实层，再谈 handoff 消费切换**（下一步专题）。

---

## F. 当前明确禁止项（写死）

- 不允许因为前置 eval 看起来都对了就顺手启动真实导航
- 不允许在本轮顺手把 handoff 改成真正执行
- 不允许自动构造新的 `destination_id` / `place_id`
- 不允许从地图/记忆/视觉补 `binding_value`
- 不允许把本专题做成完整导航启动系统

---

## G. 最小验证方案（写死）

最小需要验证：
- **写入**：全部硬条件满足时会写出 `destination_bound_v0`
- **不写入**：任一条件缺失时不写
- **不改变行为**：写入后仍不改变 `route / proposal / submit / handoff` 语义
- **回归**：`tools/verify_voice_v1_minimal_flow.py` 仍 ALL_OK

---

## H. 下一步边界（写死）

- 本轮之后，下一步才是“handoff 如何消费 `destination_bound_v0`”
- 再之后才是“是否进入真实导航启动”
- 不允许在本轮跨过这两步

执行前承接层（P4-1 设计冻结）：
- `docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_PLAN_V0.md`

