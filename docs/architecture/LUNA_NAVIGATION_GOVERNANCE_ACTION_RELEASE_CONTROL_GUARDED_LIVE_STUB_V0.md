# Luna — Navigation Governance Action Release Control Guarded Live Stub v0（准 live 态受控 stub）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_GUARDED_LIVE_STUB_V0.md`  
**性质**：Phase-Next-74：把 `minimal live execution definition` 推进为“可进入 live candidate、但默认不放行真实 side effect”的 guarded live stub（落代码；不触发真实动作）

关联：
- minimal live execution definition（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_LIVE_EXECUTION_DEFINITION_V0.md`
- minimal runtime contract / stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_STUB_V0.md`
- minimal executor（冻结/骨架）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_SKELETON_V0.md`
- executor input bridge（冻结/最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_IMPLEMENTATION_V0.md`
- execution state / result（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`
- live release gate（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 的 guarded live stub 设计与落地文档。
- 当前目标：把 minimal live execution definition 推进到 guarded live stub（准 live 候选承载位）。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不触发中台真实迁移。
- 当前不改变现有主线行为（不改 route/proposal）。

---

## B. 为什么现在要做 guarded live stub

- live execution definition 已冻结，runtime stub 已存在。
- 若没有 guarded live stub，后续会直接从 runtime stub 跨到真实 live execution，缺少一层关键验证：
  - 能否识别并进入 live candidate
  - guardrail 是否能把所有真实 side effect 全部压住
  - execution state / result / failure path 是否仍按合同顺序占位
- 因此必须先有“可进入 live candidate、但 side effect 仍被压住”的过渡层。

---

## C. guarded live stub 的最小定义（写死）

- 它不是可运行的真实 `release_control`。
- 它不是 minimal executor 本体。
- 它只是“未来真实 live execution 之前的受控 live 候选入口”。
- 只负责占住 live candidate 态与 guardrail，不负责真实 side effect。

---

## D. guarded live stub 最小能力面（写死 5 个）

1) **live stub 身份**  
- 固定 identity / scope

2) **live candidate 输入接口占位**  
- 未来只接受 bridge-ready 的最终执行输入  
- 当前不真实消费；默认仍不放行真实 side effect

3) **execution state safe update 接口占位**  
- 未来按 live contract 推进  
- 当前只允许 safe placeholder update

4) **result object safe update 接口占位**  
- 未来按 live contract 写结果  
- 当前只允许 safe placeholder update

5) **blocked / failure path 占位**  
- 未来在 guardrail 不放行时负责收口  
- 当前只回 placeholder-safe / blocked-safe / reported-placeholder

---

## E. 默认行为（写死）

- 默认可以识别 “live candidate”
- 默认不放行真实 `release_control`
- 默认不放行 route / voice / memory / migration side effect
- 默认只返回 guarded / blocked / not_implemented / placeholder-safe

---

## F. 与现有链路的关系（写清）

与 runtime stub：
- runtime stub 是更底层的不可执行运行态占位  
- guarded live stub 是更接近 live 的受控过渡层  
- 两者职责不同，不能混用

与 executor input bridge：
- bridge 决定最终输入包是否可形成  
- guarded live stub 未来只接受 bridge-ready 输入  
- 当前不真实消费 bridge（只做观测与 guard）

与 execution state / result object：
- guarded live stub 未来仍必须通过这两个标准面回传  
- 当前只允许 safe placeholder update（不声称 started/completed）

---

## G. 当前不允许做什么（写死）

- 不允许真实 `release_control`
- 不允许借 guarded live stub 顺手做 `rollback` / `interrupt`
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许越过 minimal live execution definition / runtime contract

---

## H. 代码落点（本轮落地）

- `capabilities/governance/runtime/navigation_governance_action_release_control_guarded_live_stub_v0.py`

