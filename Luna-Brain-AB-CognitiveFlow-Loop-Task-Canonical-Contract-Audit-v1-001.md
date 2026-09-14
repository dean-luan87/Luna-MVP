# Luna Brain / A-B / Cognitive Flow / Loop / Task Canonical Contract Audit

Phase: `Phase-Luna-Brain-AB-CognitiveFlow-Loop-Task-Canonical-Contract-Audit-v1-001`

Audit mode: READ-ONLY ARCHITECTURE / CONTRACT AUDIT

## 1. Inventory findings

当前工程存在三组并行的流程描述：

1. Brain Golden Baseline：`S3 → B1 → B2 → B3 → B4 → feedback/reconsideration`
2. A Route Product Loop：`Input → Observation → Context/Field → Cognitive State/Flow → Intent/Decision → Task → Action → Runtime → Outcome → Feedback`
3. Dynamic Cognitive Flow / Cognitive Loop：`Goal → Provisional Plan → Minimum Need → Requirement → Capability Candidate → Evidence → State Version → Sufficiency/Reconsideration`

这些路径部分复用相同候选类型，但没有发现已经实现的统一 `Brain → A/B Route → Cognitive Flow → Cognitive Loop` 调用合同。

## 2. Current owner matrix

| Semantic | Current owner | Authority / output | Finding |
|---|---|---|---|
| Cognitive subject | Brain 概念；无单一运行时 Brain owner | Goal/value/final evaluation 概念上由 Brain 保留 | AMBIGUOUS / CONTRACT_GAP |
| Baseline governance | Brain Golden Baseline Governance | 管理 baseline/index/evidence | KEEP |
| Goal | `CognitiveGoalCandidateV1` / Brain interface | candidate-only；最终 authority 未明确 | AMBIGUOUS |
| Intent | Intent Governance | Intent candidate 与治理 | KEEP |
| Task | Task Manager | lifecycle/readiness/cancel/recovery | KEEP |
| Role | Social Self / Role Layer | Role candidate / activation governance | KEEP |
| Perspective | Role/Perspective layer；独立 owner 不清晰 | read-only structural input | AMBIGUOUS |
| Field | Field State Reducer | Field state mutation authority | KEEP |
| Current World | Current World representation / Cognitive State Formation | CurrentWorld candidate；不是 World Truth | KEEP |
| Context | Context Foundation | Context candidate assembly | KEEP |
| Emotion | Emotion architecture/interface；统一 owner 不明确 | modulation candidate | AMBIGUOUS / CONTRACT_GAP |
| Attention | Cognitive Attention Governance | relevance/allocation candidate | KEEP |
| Hypothesis | Cognitive Hypothesis Governance | hypothesis/revision candidate | KEEP |
| Expectation | 独立 owner 未发现；Outcome Evaluation 接收 expectation | comparability input | AMBIGUOUS |
| Cognitive concern | Loop local envelope / Dynamic Flow concern refs | local process concern | KEEP |
| Need | Dynamic Flow current minimum Need；Observation Need 由 Outcome/FPO handoff | Need candidate | OVERLAP / AMBIGUOUS |
| Requirement | Capability Registry / Capability Governance | bounded Capability Requirement | KEEP |
| Observation request | FPO / Active Observation Control | Observation Need/Reobserve candidate | KEEP |
| Observation admission | Observation Gateway Governance | admission candidate | KEEP |
| Capability resolution | Capability Registry / Capability Governance | Scope/Resolution/Invocation candidate | KEEP |
| Provider/model selection | Model Manager / Provider Governance | provider mapping/admission | KEEP |
| Evidence update | Observation Gateway/B1 + Cognitive State Formation/Dynamic Flow | evidence/state candidate | KEEP |
| Sufficiency | Dynamic Flow produces candidate；最终 authority不明确 | GoalSufficiency candidate | AMBIGUOUS |
| Continuation | Cognitive Flow / Dynamic Flow | CONTINUE/REPLAN/REQUEST candidate | KEEP |
| Pause/Resume | Cognitive Flow cycle interrupts / Loop mapping | Suspend/Resume candidates | KEEP |
| Reconsideration | Outcome Evaluation emits；Cognitive Flow owns re-entry | Reconsideration candidate | KEEP |
| Branch/Merge | Loop reservation only | no runtime branch/merge | CONTRACT_GAP |
| Closure | Loop assessment；Brain/Cognitive Flow governance acceptance candidate | Closure record/outcome | KEEP / CONTRACT_GAP |
| Assimilation | Brain assimilation candidate boundary | candidate-only handoff | KEEP / CONTRACT_GAP |
| Decision | Decision Governance | Decision candidate/selection | KEEP |
| Behavior | Role/behavior candidates and Action boundary；独立 owner 未唯一定位 | behavior candidate | CONTRACT_GAP |
| Action | Action Governance | Action candidate/admission | KEEP |
| Experience | Cognitive Memory & Experience Governance | Experience candidate | KEEP |
| Memory | Cognitive Memory & Experience Governance | Memory candidate；无 mutation | KEEP |
| Resource | Existing Resource Governance references；统一 owner 未固定 | readiness/growth gate | AMBIGUOUS |
| Safety | Existing Safety/Permission owners；统一 owner 未固定 | admission/preemption gate | AMBIGUOUS |

## 3. Current architecture flow

### B5 baseline

`S3 real provider → B1 visual evidence / Observation Gateway / Current World → B2 Current World / Cognitive State / Cognitive Flow → B3 Intent / Decision / Task → B4 Outcome / Reconsideration / Reobserve → Cognitive Flow re-entry`

Evidence remains candidate-only and is not promoted to World Truth.

### A Route controlled product loop

`Product Input → Observation/FPO → Observation Gateway → Context/Field → Cognitive State/Flow → Intent/Causal/Decision → Task → Action → Runtime boundary → Controlled Result → Outcome Evaluation → Reconsideration/Reobserve`

这是 controlled handoff assembly，不是完整 runtime。

### B2/B3 direct adapters

B2 adapter 直接调用 Cognitive State Formation 与 Cognitive Flow；B3 adapter 直接调用 Intent、Decision 与 Task Manager。因此当前不只有 A Route 一个 integration caller。

## 4. Brain responsibilities

可以确认：

- 保持 goal/value/final evaluation authority 的概念责任；
- 接收 Attention、Emotion 等候选影响；
- 作为 Loop materialization governance 的概念 authority；
- 对 Cognitive Outcome Candidate 执行未来 assimilation governance。

无法确认：

- 是否存在实际 Brain runtime owner/API；
- Brain 如何选择 A Route/B Route；
- Brain 如何把 Goal 转成 Need；
- Brain 如何判断最终 Sufficiency；
- Brain 如何接收 Closure/Assimilation candidate。

结论：`AMBIGUOUS / CONTRACT_GAP`。

## 5. A Route responsibilities

Canonical owner：`A Route Orchestration Governance`。

当前负责 lifecycle staging、handoff acknowledgement、controlled route assembly、bounded defer/reconsideration 与 trace linkage。

明确不拥有 Context、Field Truth、Intent、Hypothesis、Decision、Task、Action、Memory、Learning 或 Provider semantics。

因此 A Route 是 orchestration owner，不应被认定为 Goal、Need、Requirement、Sufficiency 或 Loop 的 semantic owner。

## 6. B Route responsibilities

当前发现两种 B Route：

1. Future simulation/counterfactual route：future interface only，不覆盖 Current Reality/Decision。
2. Dual-perception Route B：VLM scene/attention/route candidate，planning-only，不执行真实模型。

两者不是同一合同。结论：`AMBIGUOUS / CONTRACT_GAP`。

## 7. Cognitive Flow responsibilities

Canonical owner：`Cognitive Flow Governance`。

负责 cycle state transition、candidate handoff、reconsideration re-entry、suspend/resume/abort、Dynamic Flow state version、current minimum Need 选择、Requirement staleness 与 sufficiency/continuation candidate。

不拥有 Context、PCN、Intent、Attention、Hypothesis、Current World、Field、Memory、Learning 或 Task execution。

## 8. Loop responsibilities

Cognitive Loop 是 Cognitive Flow 下的 candidate-only local process envelope，不是新的 global owner。

Loop local state 包括 identity、cognitive concern、local disposition、current Need、hypothesis lineage、pending candidates、state-version lineage、pause/wait reason、local sufficiency、closure state、trace/provenance。

Loop 只保存 Intent、Role、Field、Context、Current World、Attention、Task、Resource、Safety、Emotion、Experience、Memory、Provider/model 的 refs。

Loop 不得成为 Brain、Task、Intent、Provider、Decision、Action、Memory 或 Experience owner，也不得 autonomous spawn child Loop。

## 9. Task responsibilities

Task Manager 拥有 Task lifecycle、readiness、dependency waiting、pause/resume、cancel/terminate、failure recovery、completion/partial completion。

`task_manager_capability_router_v1.py` 可以把 capability requirements 映射为 execution request candidates，但不直接执行 Provider。

Task→Capability 是 candidate route；Task→Provider、Task→Loop semantic authority 均未发现。

## 10. A/B vs Loop overlap

| Capability | A Route | B Route | Cognitive Flow | Loop | Finding |
|---|---|---|---|---|---|
| Hypothesis | 编排/ref | simulation/scene candidate | 读取/反馈 | 保存 lineage | OVERLAP |
| Need | Observation demand | 未统一 | current minimum Need | 保存 current Need | OVERLAP / AMBIGUOUS |
| Requirement | 传递 candidate | 未统一 | 使用/筛选 | 保存 refs | OVERLAP |
| Observation | FPO/Gateway route | future input | next observation candidate | 保存 refs | KEEP |
| Evidence | Gateway/B1 output | candidate-only | state update | lineage | KEEP |
| Attention | ref | candidate | read-only | ref | KEEP |
| Context/Field/World | staging | 不覆盖现实 | read-only | refs | KEEP |
| Emotion | deferred/ref | 未定 | modulation input | modulation ref | AMBIGUOUS |
| Continuity | cycle trace | 未定 | lifecycle | local continuity | OVERLAP |
| Sufficiency | completion/feedback | simulation candidate | GoalSufficiency candidate | local state | AMBIGUOUS |
| Reconsideration | feedback route | future candidate | re-entry | stored candidate | KEEP |
| Capability routing | passes to FPO/capability boundary | no direct provider | Need→Requirement→Resolution | candidate path | OVERLAP |
| Pause/Resume | route control | 未定义 | cycle interrupt | local lifecycle | OVERLAP |
| Closure | cycle complete/abort | 未定义 | lifecycle candidate | closure record/package | CONTRACT_GAP |
| Outcome | output/feedback | simulation result | state feedback | Cognitive Outcome | OVERLAP |
| Assimilation | memory/learning refs | future return | no final owner | Brain candidate | CONTRACT_GAP |

## 11. State duplication audit

未确认 Loop 复制 authoritative state。`LoopIdentityCandidateV1` 明确包含 `authoritative_state_duplicated=False`。

以下是 local candidate state：

- local disposition；
- current minimum Need ref；
- hypothesis lineage；
- pending candidates；
- state versions；
- pause/wait reason；
- local sufficiency；
- closure state；
- trace/provenance。

以下属于 snapshot/reference，而非已确认 authoritative duplication：

- A Route request 的上下游 refs；
- ProductCycle 的 decision/task/action/outcome refs；
- B2/B3 adapter 的 Context/PCN/Intent/Field/Attention/Hypothesis/World refs；
- CurrentWorld candidate 的外部 owner refs。

Need、Observation Need、Task capability requirement、Capability Requirement 之间存在语义重叠，但尚未证明为 authoritative duplication。

## 12. Bypass audit

| Path | Current state | Classification |
|---|---|---|
| Brain→A/B/Flow | 无统一 concrete caller | CONTRACT_GAP |
| Brain→Capability | 未找到 direct provider selection contract | CONTRACT_GAP |
| Task→Capability | candidate route implemented | OVERLAP |
| Task→Loop | 仅 refs/handoff | CONTRACT_GAP |
| Role/Emotion/Field→Loop | read-only refs/signals | KEEP |
| A Route→Provider | controlled only | KEEP |
| B Route→Provider | 未发现 runtime | BLOCKED |
| Loop→Provider | explicit false | BLOCKED |
| Loop→Action/Task/Intent mutation | explicit guards | BLOCKED |
| Loop→Memory/Experience | candidate refs only | BLOCKED |
| Loop→child Loop | reservation only | BLOCKED |
| Decision→Action | canonical candidate handoff | KEEP |
| Task→Action | through Action Governance | KEEP |
| Action→Runtime | candidate handoff only | KEEP |

## 13. Functional walkthrough summaries

### 13.1 寻找出口

Goal 概念上由 Brain 保留，但具体 Goal API 未知；A Route 表示 current-reality cognition，但 Brain→A Route 选择未定义。Role/Field/Task/Emotion/Context 可以通过现有 refs 进入 B1/B2/Flow/Loop。Dynamic Flow 可选择最小 Need，Capability bridge 形成 Requirement，Scope/Resolution/Resource/Permission/Safety/Observation admission 形成 candidate，Gateway/B1 接收 evidence，B2/Flow 形成新 state version，Sufficiency candidate 可产生 STOP_SUFFICIENT。Closure acceptance 与 Brain assimilation consumer 未明确。Decision/Task/Action 不由 Loop 自动触发。

### 13.2 预测当前方向能否到达目标

语义更接近 future B Route simulation。B Route 当前只能输出 simulation candidate，不能覆盖 Current Reality/Decision。Hypothesis、Expectation、simulation sufficiency、B→A→Loop 的完整调用路径均无法唯一确认。结论：CONTRACT_GAP。

### 13.3 已有 Task 但证据不足

Task Manager 保持 lifecycle/readiness；Task 可表达 observation/capability requirements。B4/Outcome Evaluation 可产生 Observation Need/Reobserve candidate，FPO/Active Observation Control 负责 admission，Cognitive Flow 负责 re-entry，Dynamic Flow 重新选择 Need。Task 不得直接触发 Provider。Task 与 Loop 之间没有统一 direct contract。Task completion 不等于 cognitive sufficiency。

### 13.4 insufficient→evidence→reconsideration→sufficient→closure→assimilation

Dynamic Flow 产生 v1 insufficient state；新 evidence 指向旧 state 并形成新 state version；hypothesis invalidation 可产生 RECONSIDER/REPLAN；达到 sufficiency 后产生 STOP_SUFFICIENT，未执行 candidates 不计为失败；Loop 先产生 closure assessment，再由治理 candidate 接受 closure；final state、Need、hypothesis、evidence、context/world、trace/provenance refs 可冻结；Cognitive Outcome 仍不是 World Truth/Decision/Action/Memory/Experience；BrainAssimilationCandidate 可保留、重规划或转发 Experience Governance，但实际 Brain consumer 未明确。

## 14. Contract gaps

1. 无统一 Brain runtime owner/API。
2. 无统一 Brain→A/B/Flow 入口。
3. A Route 与 B5 baseline 没有唯一组合合同。
4. B Route 术语有两种含义。
5. Goal→Need 与最终 Sufficiency authority 不明确。
6. Need、Observation Need、Task capability requirement、Capability Requirement 边界重叠。
7. Expectation owner 不明确。
8. Emotion integration owner 不明确。
9. Task→Loop contract 不明确。
10. Closure acceptance 与 Brain assimilation consumer 不明确。
11. Behavior owner 不明确。
12. Resource/Safety 统一 owner 名称未固定。
13. A Route protocol、Product Loop engine、B5 baseline 的阶段顺序未完全对齐。

## 15. Potential wrong-owner findings

- A Route 编排了 Cognitive State、Intent、Decision、Task、Action、Runtime、Memory/Experience、Learning stages，但 guards 明确禁止 semantic mutation：`POTENTIAL_WRONG_OWNER / AMBIGUOUS`。
- Task Manager capability router 生成 execution request candidates，可能被误读为 Capability owner：`OVERLAP / POTENTIAL_WRONG_OWNER`。
- Cognitive Flow 构造 Intent handoff，但只是 read-only candidate handoff，不构成 Intent owner 转移：`KEEP`。
- Loop 生成 closure assessment，但不能自授权 closure：`KEEP`。

## 16. Clean boundaries

当前较清晰且应保持不变的边界：

- Cognitive Flow 不拥有 Context/PCN/Intent/Attention/Hypothesis/Field/Memory/Learning；
- Intent 不创建 Decision/Task/Action；
- Decision 不执行 Action、不创建 Task；
- Task 不执行 Action；
- Observation Gateway 不产生 World Truth；
- Current World 不等于 Field Truth；
- Provider result 不等于 semantic authority；
- Plan 不等于 execution queue；
- stale Requirement 不得强制 invocation；
- Loop 不直接调用 Provider；
- Loop 不生成 Action/Task/Intent mutation；
- Outcome Evaluation 不 mutate Task/Action/Decision/Intent/Field/Memory；
- Memory/Experience 为 candidate-only；
- B Route 不覆盖 Current Reality/Decision；
- A Route orchestration 无 semantic authority。

## 17. Architectural decisions requiring discussion

1. Brain 是否需要独立 canonical subject/governance contract？
2. A Route 是 canonical caller、adapter，还是仅 orchestration layer？
3. Cognitive Flow 与 A Route lifecycle authority 如何组合？
4. B Route 的唯一语义与命名是什么？
5. Goal、Need、Requirement、Sufficiency 的 authority chain 如何确认？
6. Task capability requirements 与 Cognitive Need→Capability Requirement 如何区分？
7. Expectation、Behavior、Emotion、Resource、Safety 的 owner 是否需要固定？
8. Closure→Outcome→Brain Assimilation 的实际 consumer 和 allowed transitions 是什么？
9. Branch/Merge reservation 后续是否仍由 Brain materialization governance 处理？

## 18. Files/contracts inspected

主要 inspected source：

- `cognitive_flow_registry_v1.py`
- `cognitive_flow_io_types_v1.py`
- `cognitive_flow_engine_v1.py`
- `cognitive_dynamic_loop_types_v1.py`
- `cognitive_dynamic_loop_engine_v1.py`
- `a_route_orchestration_protocol_v1.py`
- `a_route_product_loop_integration_engine_v1.py`
- `cognitive_loop_continuity_candidate_types_v1.py`
- `cognitive_loop_continuity_candidate_engine_v1.py`
- `cognitive_loop_lifecycle_closure_types_v1.py`
- B1/B2/B3/B4 integration adapters and types
- Intent / Decision / Action / Outcome / Observation / Capability / Task / Memory / Experience owners and guards

主要 inspected architecture：

- `luna_brain_b5_real_evidence_cognitive_loop_golden_baseline_planning_v1/`
- `luna_brain_integrated_golden_baseline_closure_v1/`
- `luna_brain_b4_task_outcome_feedback_reconsider_reobserve_integration_planning_v1/`
- `luna_a_route_runtime_product_loop_integration_planning_v1/`
- `luna_cognitive_a_route_integration_architecture_v1/`
- `luna_role_architecture_v1/`
- `cognitive_attention_global_architecture_v1/`
- `cognitive_hypothesis_belief_architecture_v1/`
- `cognitive_emotion_engine_v1/`
- `phase_luna_dynamic_cognitive_flow_governed_multi_loop_observation_planning_v1/`

`_eval_out`、`_tmp_eval_out` 与 smoke output 未作为 canonical source。

## 19. Contradictions

1. A Route planning declares A Route as canonical loop caller，而 Dynamic Loop semantic owner 是 Cognitive Flow Governance。
2. A Route architecture-only docs 与 controlled product-loop implementation 状态不同。
3. B Route 有 future simulation 与 perception Route B 两种定义。
4. A Route protocol 的 Dynamic Regulation stage 与 Product Loop engine 的 Intent/Causal/Decision stage 顺序不同。
5. B5 S3/B1/B2/B3/B4 route 与 A Route Product Loop route 尚未合并为唯一 current flow。
6. B5 inventory 中 B4 的 repository status 与外部终端验证状态不能自动互相替代。

## 20. Discussion order

1. 确认 Brain canonical subject/governance contract。
2. 确认 A Route 的 caller/adapter/orchestration 身份。
3. 固定 B Route 语义和命名空间。
4. 明确 Goal、Need、Requirement、Sufficiency 的 authority chain。
5. 对齐 Cognitive Flow、Cognitive Loop、Task Manager 边界。
6. 对齐 A Route、B5 baseline、B2/B3/B4 的阶段顺序。
7. 固定 Closure→Outcome→Brain Assimilation contract。
8. 最后处理 Behavior、Emotion、Resource、Safety、Branch/Merge。

本轮没有修改 canonical types、canonical owners 或其他工程文件。

AUDIT_COMPLETE_WAITING_FOR_ARCHITECTURAL_REVIEW
