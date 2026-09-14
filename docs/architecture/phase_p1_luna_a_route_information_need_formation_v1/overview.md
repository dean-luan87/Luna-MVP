# Phase-P1 Luna A-Route Information Need Formation v1

状态：`GO — VERIFIED — PHASE CLOSED`

`INFORMATION_NEED_FORMATION_GAP = CLOSED`。

用户终端真实验证：`all_checks_passed=true`、`check_count=99`、
`cognitive_logic_result=PASS`、`operational_result=PASS`、
`failed_checks=[]`、`final_decision=GO`。

本 Phase 只实现 A-Route 的最小 Information Need Formation 边界，针对已确认的
`INFORMATION_NEED_FORMATION_GAP`。它把治理后的目标条件与当前 Current World
覆盖进行只读差集计算，并在差集非空时复用既有 `CognitiveNeedCandidateV1`
形成 candidate。

```text
GoalContextV1.success_condition_refs
  + governed role/objective condition signals
  - Current World cognitive coverage
  → necessary unknowns
  → CognitiveNeedCandidateV1
```

这不是 `Goal → Need` 静态查表。adapter 不解析 Goal、Role 或 Context 字符串，
不使用 `scenario_id`，也不把已经存在的 `information_need_ref` 或
`required_information_refs` 重新包装成 Need。目标条件必须来自已有的
`GoalContextV1` 或明确的 governed condition signal；Current World coverage 是
调用方提供的只读语义投影。

Formation owner 是 `A-Route Cognitive Responsibility`。输出仅为
candidate-only cognition input：不修改 Goal、Intent、Concern、Field 或
Current World，不形成 Observation Demand，不选择 Capability，不执行
Provider/Model，也不进入 Decision、Task、Action、Memory 或 PCN。

本阶段到 Information Need 为止。Observation Demand Formation 仍是后续边界，
Information Gap 仍由既有 owner 负责。

验证资产标记为：
`CONTROLLED_A_ROUTE_INFORMATION_NEED_FORMATION_TEST`，不宣称 LIVE Runtime。

成熟度边界：本次只确认 governed objective conditions 减去 Current Cognitive
Coverage 的状态敏感 Need formation。尚未证明 Self 参与 cognitive objective
formation、Goal-conditioned Minimum Self/External View、required cognitive
conditions 的更上游自主形成、pre-observation Attention 或 Observation Demand
Formation。不启动 `OBSERVATION_DEMAND_FORMATION_GAP` implementation。
