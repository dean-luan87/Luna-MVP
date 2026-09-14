# Cognitive Foundation Architecture Risk Review v1

## Risk register

| Risk | Current evidence | Consequence | Required guard |
|---|---|---|---|
| Neural becomes a Scheduler | Neural exists only as docs; legacy task/orchestration assets could absorb it. | Neural may start selecting/executing providers. | Keep Neural outputs as CWO/signal/alignment candidates only; Middleware owns execution organization. |
| Middleware regains cognitive authority | Legacy Task Manager uses `task_goal/task_plan`; field perception has task context. | Goal/Attention/CWO semantics may be rewritten downstream. | CWO purpose immutable; legacy task goal replaced by CWO ref; Middleware reports feasibility only. |
| Provider directly affects Brain | Legacy result/runner/UI routes exist; no live A-route adapter. | Model output could become an unscoped conclusion. | Mandatory Evidence Adapter/Gateway and Middleware Report before Neural feedback. |
| Legacy Task pollutes CWO | Task decomposition/lifecycle semantics may be mistaken for cognitive work. | Task plan could replace Brain Intent. | Map task assets only after CWO into execution-candidate lifecycle. |
| Model result pollutes Reality | Legacy fusion/normalizer helpers may collapse outputs prematurely. | Evidence becomes Situation/Reality fact. | Preserve provenance/conflict/uncertainty; no internal Truth authority. |
| Whitebox precedes behavior | Existing UI is model/runner-oriented. | UI reproduces old control architecture. | Delay UI implementation until controlled Provider traces exist. |
| Registry treated as runtime brain | Rich registry metadata may be queried upstream. | Capability availability could create Goals/Attention. | Middleware-only access; baselines governance-only. |

## Risk result

No V0 blocker prevents planning the Controlled Provider Invocation Skeleton. The above risks become implementation gates: each must be tested explicitly before a real Provider is connected.
