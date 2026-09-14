# Luna — Navigation Executor Takeover Wiring v0（takeover → executor skeleton 接线：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_WIRING_V0.md`  
**性质**：Step 5：Navigation Executor Takeover Wiring v0（冻结 takeover → executor skeleton 的真实接线边界；接到壳子前，不进入动作执行）  

关联：
- 执行器接管层方案（冻结）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_PLAN_V0.md`
- 执行器本体最小定义（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 执行器本体模块骨架（不可执行）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 输入对象实现版：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`
- 状态对象实现版：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 监控闭环实现版：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_IMPLEMENTATION_V0.md`
- 最小接入顺序（冻结）：`docs/architecture/LUNA_REAL_EXECUTOR_MINIMAL_INTEGRATION_SEQUENCE_V0.md`

---

## A. 文档定位（写死）

- 这是“**takeover → executor skeleton 真实接线**”的设计文档。
- 当前目标：冻结接线边界与接线后**最小安全状态**（可冻结、可回归）。
- 当前不做真实动作执行。
- 当前不做地图接入。
- 当前不做语音联动。
- 当前不做中台真实治理动作。
- 当前不改变现有主线裁决边界（formal decision/readiness/takeover 的职责边界不变）。

---

## B. 为什么现在要先定义接线而不是直接执行

- 前 4 步已经补齐：
  - 执行器本体 skeleton（可导入、可接线、不可执行）
  - 输入对象实现版（implemented `navigation_real_executor_input_v0`）
  - 状态对象实现版（implemented `navigation_real_executor_status_v0`，不伪装运行事实）
  - 监控闭环实现版（implemented `navigation_execution_monitoring_status_v0`，不触发治理）
- 但如果不先冻结 takeover → executor 的接线边界，后续很容易从“占位链”直接跳到“动作链”，造成：
  - 接线即越权（把接线当执行授权）
  - 接线即不可观测（监控虽在位但消费面漂移）
  - 接线即不可回归（接线口径不稳定）
- 所以必须先写死“怎么接、接到哪里为止、接完后还不能干什么”。

---

## C. takeover → executor 的最小合法入口（写死，缺一不可）

以下 8 项缺一不可；少任一项则**不允许真实接线**：

1) `mid_platform_formal_decision_stub_v0.decision_result == "allow_progress"`
2) `formal_decision_allow_progress_path_v0.downstream_placeholder_interface == "navigation_handoff_post_bound_execution_stub_v0"`
3) 下游 post-bound consumption 已进入“可继续推进占位阶段”
4) `navigation_real_execution_readiness_gate_stub_v0.readiness_status == "ready_candidate"`
5) `navigation_executor_takeover_stub_v0.takeover_status == "ready_to_takeover"`
6) implemented `navigation_real_executor_input_v0` 已存在
7) implemented `navigation_real_executor_status_v0` 已存在
8) implemented `navigation_execution_monitoring_status_v0` 已存在

并写死：

- 少任一项，都不允许真实接线。
- 这些只是**接线前提**，不是动作执行授权。
- `allow_progress` / `ready_candidate` / `ready_to_takeover` 均不等同于“允许执行动作”。

---

## D. 接线后的最小安全状态（保守写死）

接线完成后，executor skeleton 最多只能进入以下安全状态之一：

- `wired_inactive`
- `wired_ready_to_takeover`

禁止进入：

- `active`
- `running`
- `executing`

并写死三句：

- 接线完成 ≠ 接管完成
- 接管完成 ≠ 动作开始
- 动作开始需要后续更高门槛（且不在本轮范围）

---

## E. 接线层最小职责（写清）

接线层只负责：

- 把 takeover 结果合法连接到 executor skeleton（只到壳子边界）
- 验证输入对象 / 状态对象 / 监控对象是否都已到位（implemented 版本）
- 把 executor skeleton 带入“可被后续接管但不执行”的安全接线态（`wired_inactive` 或 `wired_ready_to_takeover`）

接线层不负责：

- 产生真实动作
- 触发地图规划
- 触发语音播报
- 决定继续/中断/回退
- 替代 formal decision / readiness / monitoring

---

## F. 接线失败时的最小原则（写死）

- 若任一前提不满足，则不得接线。
- 接线失败时控制权必须留在上游控制链（formal decision/readiness/takeover 链）。
- 不允许“半接线半执行”。
- 不允许 executor skeleton 在失败时进入不明状态（必须保持未接线或 `wired_inactive`）。

---

## G. 与现有链路的关系（写清）

### 与 formal decision

- formal decision 决定是否允许推进到 takeover 的候选阶段
- 不直接负责 executor 接线

### 与 readiness gate

- readiness gate 只证明最后门控候选就绪（ready_candidate）
- 不直接负责 executor 接线

### 与 takeover stub

- takeover stub 证明接管层前置条件成立（ready_to_takeover）
- 真实接线发生在其后（接到 executor skeleton 壳子边界）

### 与 executor skeleton

- 这是 executor skeleton 第一次被正式接入控制链
- 但仍然不允许它执行真实动作（保持 not_implemented/no-op）

### 与 monitoring implementation

- 监控实现版必须已在位，才能允许接线
- 否则不允许把 executor skeleton 接入链路（避免不可观测/不可回收）

---

## H. 当前仍然不能做什么（必须写死）

- 不允许真实导航动作执行
- 不允许真实地图接入
- 不允许真实语音启动
- 不允许真实中台治理动作
- 不允许把 `wired_ready_to_takeover` 当执行开始
- 不允许绕过后续回退/中断治理入口

---

## I. 当前阶段结论（写死一句）

**当前阶段只适合冻结 takeover → executor 的真实接线边界；即使未来允许做最小接线实现，也只能先把 executor 带入安全接线态，不能进入真实动作态。**

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - takeover wiring 的最小非动作实现
- 再之后才考虑：
  - 回退/中断治理入口的最小实现
- 当前不跨这两步

---

## K. 未来接线结果样例（仅说明，不落代码）

```json
{
  "wiring_attempted": true,
  "wiring_scope": "navigation_executor_takeover_wiring_v0",
  "wiring_status": "wired_ready_to_takeover|wired_inactive|blocked|not_applicable",
  "reason": "..."
}
```

