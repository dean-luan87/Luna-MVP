# Luna — Navigation Handoff Post-Bound Execution Plan v0（真实执行前承接层：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_PLAN_V0.md`  
**性质**：P4-1 执行前承接层方案（可冻结、可回归；不进入真实执行）  

关联（已存在）：
- P3-1 建议层：`docs/architecture/LUNA_NEED_NAVIGATION_ROUTING_V0.md`
- P3-2 消费契约：`docs/architecture/LUNA_NAVIGATION_NON_NAVIGATION_DISPATCH_CONSUMPTION_PLAN_V0.md`
- P3-3 中台消费 stub：`docs/architecture/LUNA_MID_PLATFORM_DISPATCH_CONSUMPTION_STUB_V0.md`
- 导航目标已绑定事实层：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_MATERIALIZATION_IMPL_V0.md`

---

## A. 文档定位（写死）

- 这是导航链“**真实执行前承接层**”的最小设计（P4-1）。
- 当前目标：定义执行前承接规则与门控边界，形成固定入口面。
- 当前不做：
  - 真实导航启动
  - 地图接入
  - 跨链自动切换
  - 语音/记忆驱动

---

## B. 为什么需要这一层

当前我们已经具备：
- `destination_bound_v0`（已确认目标的正式事实层）
- `navigation_handoff_consume_bound_v0`（handoff 已正式消费 bound fact 的观测）
- `need_navigation_routing_v0`（是否需要导航的只读建议）
- 中台分流消费 stub（只读接住建议结果）

但这些仍不足以直接进入真实执行，因为：
- 建议层与消费 stub **不是执行令**
- `destination_bound_v0` 单独也 **不是执行令**
- 真实执行前必须有一层“**承接与门控**”，否则会跨层越权（跳过安全/信息/任务有效性治理）

---

## C. 执行前承接层的最小定义（写死）

执行前承接层不是：
- 中台最终裁决器
- 地图规划器
- 真实导航执行器
- 语音驱动器

它是：
- 导航链在真实执行前的**正式接收位**
- 负责检查：
  - 导航任务是否成立（必须来自中台正式裁决，当前仅占位）
  - 目标是否已绑定（必须有 `destination_bound_v0`）
  - 当前是否满足执行前提（门控通过）
  - 是否仍需等待更多条件（pending）

---

## D. 未来可被承接的输入（白名单，写死）

执行前承接层未来只允许接收：
- **中台未来正式裁决结果**（当前未实现；仅占位说明）
- `destination_bound_v0`
- `navigation_handoff_consume_bound_v0`

并明确（写死）：
- `need_navigation_routing_v0` 本身不是执行启动令
- `mid_platform_dispatch_consumption_stub_v0` 本身不是执行启动令
- `destination_candidate_v0` / `destination_confirmation_fact_v0` / `destination_bound_upgrade_eval_v0` 等评估链条产物 **不能直接进入执行层**

---

## E. 执行前必须过的最小门控（只写门类与原则，不做实现）

### E1. 分流门控（Routing Gate）

- 中台必须已明确裁决“进入导航链”（占位：未来中台正式裁决输出）。
- 只读建议与消费 stub 不足以放行执行。

### E2. 目标门控（Destination Gate）

- 必须存在 `destination_bound_v0`（目标已正式绑定）。
- 且 handoff 已正式消费 bound fact（`navigation_handoff_consume_bound_v0` 为真/可观测）。

### E3. 信息充分性门控（Information Sufficiency Gate）

- 当前导航任务所需的最小信息必须齐备（例如目的地绑定信息等）。
- 若仍不足：不得执行，应进入 `execution_pending` 或 `execution_blocked`（由门控语义决定）。

### E4. 安全门控（Safety Gate）

- 当前不应处于高优先级安全抢占状态。
- 若风险过高：不得进入导航执行（blocked）。

### E5. 任务有效性门控（Task Validity Gate）

- 当前任务仍然有效：
  - 未被新任务覆盖
  - 未处于挂起/过期/失效
- 若任务无效：不得执行（blocked）。

写死：
- 本节只定义门类与原则，不做实际门控实现。

---

## F. 未来最小承接结果集合（只定义 3 类）

- `execution_ready`：前提齐备，未来可进入真实执行
- `execution_blocked`：明确不允许执行
- `execution_pending`：暂不能执行但非永久阻断，需要等待条件补齐

写死：这是“执行前承接层”的输出语义，当前可先文档冻结，不要求落代码。

---

## G. 与当前各层关系（写死）

### G1. 与中台主层

- 中台决定是否进入导航链（未来正式裁决）。
- 承接层不替代中台裁决；只做执行前门控与承接。

### G2. 与导航链

- 承接层是导航链真实执行前的入口。
- 不是导航执行本体。

### G3. 与视角链

- 视角链继续提供依据与候选。
- 不直接触发导航执行。

### G4. 与语音链

- 当前不直接联动。
- 未来若需播报，也必须在承接层/中台之后形成专门候选（不允许直连）。

---

## H. 当前不允许做什么（写死）

- 不允许直接启动导航
- 不允许把 `need_navigation_routing_v0` 当执行令
- 不允许把 `destination_bound_v0` 单独当执行令
- 不允许跳过安全/信息/任务有效性门控
- 不允许在本轮顺手做地图规划
- 不允许在本轮顺手做语音联动

---

## I. 下一步边界（写死）

- 本轮之后，下一步才考虑“执行前承接层的只读占位实现”
- 再之后才考虑“真实导航执行链”
- 当前不跨这两步

