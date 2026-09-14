# Luna — Navigation Handoff Post-Bound Execution Stub Consumption Plan v0（只读消费契约：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_CONSUMPTION_PLAN_V0.md`  
**性质**：Phase-Next-9：`navigation_handoff_post_bound_execution_stub_v0` 消费 formal decision 窄路径 `allow_progress` 的最小契约（只冻结消费语义，不做执行）  

关联：
- formal decision 窄路径 allow-progress：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_VNEXT_NARROW_ALLOW_PROGRESS_V0.md`
- 导航执行前承接层设计冻结：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_PLAN_V0.md`
- 导航执行前承接层 stub（只读占位）：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_V0.md`
- formal decision stub 实现（当前输出位）：`capabilities/mid_platform/runtime/mid_platform_formal_decision_stub_v0.py`
- 真实执行前最后门控（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_V0.md`
- 最后门控输入面（v0，占位承接）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_INPUTS_V0.md`
- 执行器接管层方案（冻结）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_PLAN_V0.md`

---

## A. 文档定位（写死）

- 这是 `navigation_handoff_post_bound_execution_stub_v0` **消费 `allow_progress`** 的最小设计文档。
- 当前目标：定义“放行结果到达下游占位层后如何被消费”的契约。
- 当前不做真实导航执行。
- 当前不做地图接入。
- 当前不驱动语音/记忆。
- 当前不把下游 stub 升级为执行器。

---

## B. 为什么现在要补这份文档

- formal decision 已经具备极窄范围 `allow_progress`。
- 且当前下游目标明确是 `navigation_handoff_post_bound_execution_stub_v0`。
- 若不定义下游如何消费该结果，allow-progress 仍然只是单边能力，无法形成稳定的“占位→占位”闭环。
- 因此必须先冻结下游消费契约。

---

## C. 下游 stub 当前可接收的最小输入（写死）

下游 stub **只允许**接收并用于消费判断的最小输入：

1) **formal decision 的窄路径放行结果**  
- `result.metadata["mid_platform_formal_decision_stub_v0"]`  
- 且 `decision_result == "allow_progress"`

2) **allow-progress 路径观测（用于确认下游目标）**  
- `result.metadata["formal_decision_allow_progress_path_v0"]`  
- 且 `downstream_placeholder_interface == "navigation_handoff_post_bound_execution_stub_v0"`

3) **既有承接链前置状态（事实/占位状态）**  
- `result.metadata["destination_bound_v0"]`  
- `result.metadata["navigation_handoff_consume_bound_v0"]`  
- `result.metadata["navigation_handoff_post_bound_execution_stub_v0"]`（当前 stub 自身既有状态）

写死：
- 这些输入都是“消费依据”，不是执行动作本身。
- 不允许缺一补一，不允许脑补，不允许伪造。

---

## D. 下游 stub 消费 `allow_progress` 的最小语义（写死）

当下游 stub 消费到 `allow_progress` 后，当前只允许得出以下语义之一：
- “formal decision 已允许进入下一占位阶段”
- “navigation handoff post-bound execution stub 已被授权继续进入下一个占位层”

并写死：这 **不表示**  
- 真实导航已经开始  
- 地图规划已经开始  
- 语音已经可以播报“开始导航”  
- 导航执行器已经接手  

---

## E. 当前最小消费结果集合（只定义 3 类，写死）

> 口径：这是“下游 stub 的消费结果”，不是执行结果。

1) **consumed_pending_execution**  
- 已成功消费 `allow_progress`  
- 但仍只进入下一占位阶段  
- 未进入真实执行器

2) **consumed_but_blocked**  
- 收到 `allow_progress`  
- 但下游自身发现仍有未满足条件  
- 因此不继续推进

3) **consumed_not_applicable**  
- 当前不是发给该 stub 的放行结果，或缺少最小消费依据  
- 因此不消费

---

## F. 当前最小消费前提（写死）

只有同时满足以下条件，stub 才允许把 `allow_progress` 视作“可消费”：

1) `mid_platform_formal_decision_stub_v0.decision_result == "allow_progress"`  
2) `formal_decision_allow_progress_path_v0.downstream_placeholder_interface == "navigation_handoff_post_bound_execution_stub_v0"`  
3) `destination_bound_v0` 存在  
4) `navigation_handoff_consume_bound_v0` 存在  

并明确（写死）：
- 这些只是“消费 `allow_progress` 的最小前提”
- 不是“真实执行前提”

---

## G. 当前仍然不能直接执行的原因（写死）

- 当前没有真实导航执行器接入
- 当前没有地图/路线规划接入
- 当前没有完整执行时门控
- 当前没有语音启动策略
- 当前没有执行期监控闭环
- 当前只有“占位层到占位层”的放行，不是“占位层到执行器”的放行

---

## H. 当前不允许做什么（写死）

- 不允许真实启动导航
- 不允许直接拉起地图
- 不允许直接切执行链
- 不允许直接对用户播报“开始导航”
- 不允许把 `consumed_pending_execution` 当执行完成
- 不允许绕过后续真实执行前门控

---

## I. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 是否需要一个“真实执行器前的最后占位层”
  - 或如何把当前占位消费结果接到真实导航执行器之前的最后门控层
- 当前不跨到真实导航执行

---

## J. 未来消费输出样例（仅说明，不实现）

```json
{
  "consumption_attempted": true,
  "consumption_scope": "navigation_handoff_post_bound_execution_stub_consumption_v0",
  "consumption_result": "consumed_pending_execution",
  "reason": "allow_progress_consumed_by_downstream_stub"
}
```

