# Luna Current Implemented Architecture Census v1

## 1. Scope / baseline / evidence convention

Static current-code census, not target architecture or deployment certification. Physical root `/Users/luanlei/Desktop/Luna-Core`; observed HEAD and supplied baseline `0a5b3128eb85aa6818bb627aaca66e8ab3de1d9d`. Working tree was already dirty. No tests, runners, verifiers, imports, or byte-code execution here. The only audit change is this document.

Evidence labels: **CF** inspected code fact; **DC** repository documentation or previous user-terminal result, not rerun; **IN** inference from inspected code; **U** unresolved. `ACTIVE_RUNTIME` means an inspected non-synthetic callable path reaches a real consumer, not that deployed operation was verified. `ACTIVE_CONTROLLED_ONLY` may include native effect under controlled integration. `ACTIVE_SYNTHETIC_ONLY` does not prove native effect. `PARTIALLY_ACTIVE` has working stages but no proven end-to-end closure. `DEFINED_BUT_NO_CONSUMER` requires a bounded inbound search, not merely a definition. Counts below refer to enumerated rows, not all 4,302 Python files under `capabilities`. This is broad, sampled reconnaissance, not exhaustive whole-repository proof.

## 2. Executive architecture summary

**CF** Three execution families must be distinguished: root Badge/MVP `main.py` imports `vision_pipeline` and local `core`/`runtime` components; midplatform controlled real provider execution uses FPO → Provider Runtime → Gateway → A-route; many midplatform/evaluation engines form candidate-only synthetic/dry-run outputs. The inspected root Badge entry does not import the midplatform Grant/Gateway chain. **CF** Owner boundaries exist for model/provider lifecycle reads, profile eligibility, Action/Safety currentness, Runtime Grant and authorization state, Gateway admission, and CState versions. **DC** Prior 06.5/user-terminal evidence reports MOIP 61/61, PR02 propagation 2 pass/7 fail (binding-preparation lineage and `None` grant), and real YOLO `RUNTIME_AUTHORIZATION_NOT_CURRENT`/`NOT_GO`. This audit does not repeat those runs. **IN** PR-ADMISSION-02 is unresolved; no complete production Brain→Organ→World→Cognition loop is established.

## 3. Current implemented architecture map

```text
Badge/MVP: main.py → vision_pipeline → scene/risk/memory → decision/speech/action
Controlled real: runner → FPO demand/request → scoped capability resolution
  → [incomplete binding/grant formation] → RealProviderExecutionEngine
  → authorized vision adapter/effect-time query → ProviderRuntimeResult
  → RuntimeObservation adapter → Gateway → Evidence/Observation → A-route/CState
Controlled downstream evaluation: Evidence fixture → Context → FieldEvent
  → FieldState candidate/projection → CurrentWorld candidate → cognitive stages
Synthetic product loop: candidate-only staged handoff refs; no native invocation
```

**CF** Generic `ProviderRuntimeObservationIngressEngineV1` applies the production lifecycle selector but manufactures its Provider result from a case (`provider_real_execution_verified=False`). Real native invocation is the separate `RealProviderExecutionEngineV1` path, gated by `controlled_integration_only` and runtime grant. No inspected general production entry stitches all four lines into one authoritative durable loop.

## 4–5. Domain / mechanism inventory and status matrix

`MP` = `capabilities/midplatform`; `EV` = `capabilities/evaluation`. Each row is one architecture-significant mechanism. Caller/consumer pairs are observed in code; where only controlled callers were seen, no production claim is made. State is also expanded in §7. Path names below are relative to MP or EV unless otherwise noted.

|ID|Mechanism / path|Domain; kind; purpose|Owner / actual authority|State; inputs → outputs; caller → consumer|Effectiveness; evidence; gap/classification|
|---|---|---|---|---|---|
|M01|Root `main.py`|Product; orchestrator; camera/scene/decision/speech|Badge local controller, not midplatform authority|process-local scene/risk/memory; camera→decision/action; CLI→local components|PARTIALLY_ACTIVE CF; separate architecture|
|M02|Root `runtime/main_loop.py`|Runtime; loop/heartbeat/veto|local runtime|loop state; snapshot→decision/trace; local runner→veto|LEGACY CF; no midplatform Grant call|
|M03|Root `luna_backend/app.py`|Transport; Flask app factory|backend|HTTP→routes; deployment U|PARTIALLY_ACTIVE CF|
|M04|`field_perception_orchestrator/integration/field_perception_active_observation_control_engine_v1.py`|FPO; demand/request/session/control formation|FPO candidate formation, not Entry Admission|case/payload→FPO demand/request/requirement; real/generic ingress→scoped resolution|ACTIVE_CONTROLLED_ONLY CF; requester source unproven|
|M05|`model_manager/registries/universal_capability_slot/universal_capability_slot_resolution_v1.py`|Capability; scoped resolver|Capability governance projection|FPO requirement→resolution; ingress→selector/engine|ACTIVE_CONTROLLED_ONLY CF|
|M06|`core/cognitive_flow/observation_demand_formation_v1.py`|Cognition; cognitive observation-intent candidate|Cognitive Flow, no execution authority|strategy/coordination→demand; controlled cognitive callers|ACTIVE_SYNTHETIC_ONLY CF; explicitly never execution request|
|M07|`model_manager/registries/universal_capability_slot/observation_demand_capability_resolution_v1.py`|Capability; cognitive demand resolver|Capability governance projection|cognitive demand→resolution; controlled routing|PARTIALLY_ACTIVE CF; distinct from M05|
|M08|`model_manager/registry/provider_registry_loader_v1.py`|Provider; declaration loader/list/lookup|Provider declaration identity only|JSON→records; selector/Owner read→consumer|ACTIVE_RUNTIME CF; `get_provider_by_id(model_id)` naming drift|
|M09|`model_manager/lifecycle/model_current_state_read_v1.py`|Model; bounded lifecycle read|Model Owner|registry projection; model ref→view; closure→selector|ACTIVE_RUNTIME CF/DC; declaration-based currentness|
|M10|`model_manager/registry/provider_current_state_read_v1.py`|Provider; bounded lifecycle read|Provider Owner|registry projection; provider ref→view; closure→selector|ACTIVE_RUNTIME CF/DC|
|M11|`model_manager/engines/model_provider_routing_lifecycle_closure_v1.py`|Routing; cross-owner prerequisite filter|consumes M09/M10, no new Owner|candidate→bounded reason; ingress/OCR/multi-provider/identity eligible view|ACTIVE_RUNTIME CF/DC; not full eligibility|
|M12|`model_manager/lifecycle/model_registry_state_machine_v1.py`|Model; lifecycle policy|Model governance|registry/sandbox transition→status; processor/tests|PARTIALLY_ACTIVE CF; production write persistence U|
|M13|`provider_runtime_governance/provider_runtime_governance_registry_v1.py`|Provider; controlled/production profile|Provider Governance eligibility only|static profile; provider ref→profile; Grant validator|ACTIVE_CONTROLLED_ONLY CF/DC; not request authority|
|M14|`model_manager/registries/universal_capability_slot/official_capability_catalog_governance_v1.py`|Capability; profile|Capability Admission eligibility only|static profile; capability→profile; Grant validator|ACTIVE_CONTROLLED_ONLY CF/DC|
|M15|`provider_runtime_governance/provider_runtime_target_preparation_v1.py`|Provider; target mapping/formation|Provider Governance candidate proof|routing+compatibility+mapping→target; binding prep|ACTIVE_SYNTHETIC_ONLY CF; routing-shaped|
|M16|`provider_runtime_governance/provider_binding_runtime_preparation_v1.py`|Provider; binding preparation|Provider Governance lineage validator|target/context→prep; controlled runner→Grant input|PARTIALLY_ACTIVE CF/DC; lineage fails in prior test|
|M17|`provider_runtime_governance/provider_binding_candidate_v1.py`|Provider; binding candidate|Provider Governance, not final grant|prep/compatibility→candidate; allocation/Grant|PARTIALLY_ACTIVE CF; routing coupling|
|M18|`core/runtime_executor/runtime_allocation_preparation_candidate_v1.py`|Runtime; allocation/execution prep|Runtime candidate, not availability|binding/scope→prep; runner→Grant|PARTIALLY_ACTIVE CF; EA-GAP-02|
|M19|`permission_and_admission_manager/module/runtime_execution_grant_v1.py`|Permission; bounded final Grant|Permission/Admission Manager|writes M20; binding/prep/policy/scope→decision; runner→executor|ACTIVE_CONTROLLED_ONLY CF; mixed contract, PR02 incomplete|
|M20|`permission_and_admission_manager/module/runtime_authorization_state_v1.py`|Permission; current state/effect query|Permission/Admission Manager|in-process store; grant/scope→currentness; vision adapter→invocation|ACTIVE_CONTROLLED_ONLY CF/DC; unknown rejects|
|M21|`core/action_governance/action_admission_governance_v1.py`|Action; admission/current read|Action Governance|`_CURRENT`/`_HISTORY`; action/envelope→admission; Grant/effect query|ACTIVE_CONTROLLED_ONLY CF; not Entry Admission|
|M22|`core/action_governance/action_governance_engine_v1.py`|Safety/Action; prerequisite and action candidate|Action/Safety Governance|current safety records; scope→safety/action candidate; Grant/effect|ACTIVE_CONTROLLED_ONLY CF|
|M23|`core/cognitive_flow/integration/a_working_envelope_cognitive_requirement_bridge_controlled/working_envelope_governance_v1.py`|Action/Cognition; scope basis|working-envelope governance, not invocation authority|local current/version; requirement→envelope; Action/Grant|ACTIVE_CONTROLLED_ONLY CF|
|M24|`core/provider_runtime_to_observation_ingress/engine_v1.py`|Provider/Observation; synthetic ingress|M11 selector, no native authority|case→synthetic ProviderResult→Gateway/A-route|ACTIVE_SYNTHETIC_ONLY CF|
|M25|`core/provider_runtime_to_observation_ingress/real_provider_execution_engine_v1.py`|Provider/Observation; controlled real engine|delegates effect guard to M26|case+grant→ProviderResult/Gateway/A-route; real runner→result|ACTIVE_CONTROLLED_ONLY CF; PR02 not closed|
|M26|`field_perception_orchestrator/integration/field_perception_real_vision_provider_adapter_v1.py`|Provider; native executor adapter|consumes M20; no self-authorization|request+grant→native ProviderRuntimeResult; M25→M27|ACTIVE_CONTROLLED_ONLY CF/DC; effect query precedes invocation|
|M27|`core/provider_runtime_to_observation_ingress/provider_result_adapter_v1.py`|Observation; normalizer|no Evidence authority|ProviderResult→RuntimeObservation; M25/M24→M28|ACTIVE_CONTROLLED_ONLY CF; empty-success/provenance preserved|
|M28|`core/observation_gateway/observation_gateway_engine_v1.py`|Observation; Gateway admission|Gateway Owner|private in-process admission state; envelope→Evidence/Observation; M25/M24→A-route|ACTIVE_CONTROLLED_ONLY CF/DC; no Field write|
|M29|`core/a_route_orchestration/a_route_orchestration_engine_v1.py`|Cognition; handoff coordinator|explicitly no semantic state|Gateway output→CState/A stages|ACTIVE_CONTROLLED_ONLY CF|
|M30|`core/cognitive_state_formation/cognitive_state_formation_engine_v1.py`|Cognition; state version formation|CState Owner|in-process version registry; observation/context→CState; A-route→cognition|ACTIVE_CONTROLLED_ONLY CF; not world truth|
|M31|`core/context_foundation/context_foundation_skeleton_v1.py`|Context; candidate/snapshot|Context candidate only|Evidence refs→context; evaluation→Field|ACTIVE_SYNTHETIC_ONLY CF|
|M32|`core/evidence_to_field_event_adapter_v1.py`|Mapping; Evidence→Field candidate|no Field mutation|Evidence+caller field/time refs→candidate; evaluation→M33|ACTIVE_CONTROLLED_ONLY CF; general live caller not found|
|M33|`core/field_event_admission_api_v1.py`|Field; event admission|Field event validator|candidate→admitted event; evaluation→reducer|ACTIVE_CONTROLLED_ONLY CF|
|M34|`core/field_state_reducer/module/field_state_reducer_module_facade_v1.py`|Field; policy/reducer/projection|Field reduction candidate|event→FieldState/read projection; evaluation→CurrentWorld candidate|ACTIVE_CONTROLLED_ONLY CF; persistence U|
|M35|EV `evidence_context_field_current_world_controlled/engine_v1.py`|World; controlled integration|candidate projection only|Evidence fixture→Context/Field/CurrentWorld; eval runner→result|ACTIVE_CONTROLLED_ONLY CF; not called by M25|
|M36|`core/cognitive_flow/cognitive_flow_engine_v1.py`|Cognition; loop/reconsideration|candidate cognitive control|CState/context→branch/demand/feedback; controlled callers|ACTIVE_CONTROLLED_ONLY CF|
|M37|`core/intent_governance/intent_governance_skeleton_v1.py`|Intent; candidate handoff|Intent candidate only|cognitive refs→intent candidate; controlled decision|ACTIVE_SYNTHETIC_ONLY CF|
|M38|`core/task_manager/module/task_manager_module_facade_v1.py`|Task; lifecycle/dependency/capability routing|Task candidate governance|snapshot/local state; task input→task/capability refs; controlled action|ACTIVE_CONTROLLED_ONLY CF|
|M39|`core/decision_governance/decision_governance_engine_v1.py`|Decision; case judgement|Decision candidate|cognitive refs→decision; controlled Task|ACTIVE_CONTROLLED_ONLY CF|
|M40|`core/outcome_evaluation_governance/outcome_evaluation_engine_v1.py`|Outcome; evaluation/reconsideration|Outcome candidate|result→feedback; controlled cognition|ACTIVE_CONTROLLED_ONLY CF|
|M41|`core/cognitive_memory_experience/cognitive_memory_experience_engine_v1.py`|Memory; experience candidate|Memory candidate|outcome→memory refs; controlled learning|ACTIVE_CONTROLLED_ONLY CF; durability U|
|M42|`core/cognitive_learning/cognitive_learning_engine_v1.py`|Learning; candidate|Learning candidate|experience→learning; evaluation result|ACTIVE_CONTROLLED_ONLY CF; no model mutation proven|
|M43|`protocol_manager/module/protocol_manager_module_facade_v1.py`|Protocol; lookup/version/compat candidate|Protocol facade, no runtime binding|registry→candidate; controlled tests|PLANNING_ONLY CF; explicit runtime flags false|
|M44|`model_test_lens/local_runner_bridge/local_runner_bridge_service_v1.py`|Evaluation; local job/adapter|Lens job control only|local job/files; request→MobileSAM/SLAM artifacts|ACTIVE_CONTROLLED_ONLY CF; not product Grant|
|M45|`core/temporal_coordinate/temporal_coordinate_v1.py`|Temporal; type/comparison|representation, not currentness|time refs→coordinate; controlled consumers|PARTIALLY_ACTIVE CF; no Grant expiry proof|
|M46|`core/a_route_orchestration/integration/a_route_product_loop_integration_engine_v1.py`|Product; staged synthetic loop|candidate handoff only|synthetic input→handoff/result; test harness|ACTIVE_SYNTHETIC_ONLY CF; explicit synthetic gate|
|M47|`core/runtime_executor/runtime_executor_engine_v1.py`|Runtime; candidate final gate/idempotency|candidate gate only|local idempotency; booleans/request→candidate admission/result|ACTIVE_SYNTHETIC_ONLY CF|
|M48|`core/runtime_executor/runtime_allocation_execution_instance_v1.py`|Resource; allocation record|caller supplies resource outcome|binding+Grant+outcome→record; controlled chain|PARTIALLY_ACTIVE CF; not availability proof|
|M49|`core/a_route_orchestration/integration/a_route_product_loop_integration_engine_v1.py` `ControlledExecutionRequestV1`|Orchestration; request candidate|no Entry Admission authority|staged refs→request; synthetic product loop→result|ACTIVE_SYNTHETIC_ONLY CF; `real_execution=False` default|

Inventory count: **49 mechanisms**, grouped into **18 audit domains** (Product/Transport, Observation Control, Capability, Cognition, Provider, Model, Routing, Runtime, Permission, Action, Safety, Gateway, Context, Field, World, Task, Protocol, Evaluation/Temporal). Grouping is for this audit, not a proposed canonical taxonomy. Mutation is limited to state/side effects identified above; candidate outputs never imply another Owner's state write. Identity/provenance handling is detailed in §§8–9.

## 6. Owner / authority matrix

|Authority|Declared / actual Owner; formation, state, query, invalidation|Downstream and boundary|
|---|---|---|
|Provider identity/lifecycle|Provider declaration loader and Provider Owner read; JSON projection; live transition writer not proven here|M11 production filter; explicit provider identity required [CF]|
|Model identity/lifecycle|Model registry/state machine and Owner read; JSON/sandbox; bounded read|M11; model identity must independently resolve [CF]|
|Capability eligibility|Official catalog governance static profile|Grant profile check and resolution; not per-request authority [CF]|
|Routing eligibility|M11 over both Owner reads|Production selector only; not invocation/full eligibility [CF]|
|Action admission/currentness|Action Governance `_CURRENT`/`_HISTORY`, issue/query/invalidate|Grant/effect check, distinct from execution Entry Admission [CF]|
|Safety currentness|Action/Safety Governance runtime safety records; issue/query/invalidate|Grant/effect guard [CF]|
|Runtime grant/currentness|Permission/Admission `form_runtime_execution_grants` registers state; public invalidation; M20 query|Authorized vision adapter; unknown/not-current rejects [CF]|
|Observation admission|Gateway private in-process admission state/query|A-route; not Field/world truth [CF]|
|Field event admission|Field Event API validation|Reducer; no persistent Field write solely by admission [CF]|
|Cognitive state version|CState in-process version registry/query/invalidate|Cognitive consumers; not physical world truth [CF]|
|Protocol/version candidate|Protocol Manager facade forms candidates, runtime flags false|Controlled/planning [CF]|
|Evaluation job control|Model Test Lens bridge/job store|Local artifacts only [CF]|
|Controlled execution Entry Admission|No authoritative decision/currentness surface proven in inspected path|PR02 gap; runner/case/profile cannot substitute [CF/IN]|
|Final phase verification|Governance standards reserve final verification to user terminal|This audit makes no GO claim [DC]|

Authority hazards: **CF** M19 has reference-string inputs and a default `requester_ref`, so a nonempty ref is not proof of requester provenance. M19 issues the decision; M20 independently checks the registered decision at effect time. M47's candidate “final gate” is not a second final runtime authority. **U** This sample cannot prove the absence of all other authority writers in the repository. No proven additional final-authority leak was classified.

## 7. State architecture

|State / record|Owner; mutation; currentness; lifetime; invalidation; persistence; consumers|
|---|---|
|Provider/model JSON declarations|respective governance Owners; file change outside runtime; bounded Owner reads project current lifecycle; file persistence; M11. Raw declaration ≠ current execution decision [CF].|
|Controlled provider/capability profiles|respective governance Owners; static eligibility declarations; no per-request currentness; M19 validator [CF].|
|Runtime authorization state|Permission/Admission Owner; M19 registers in-process store; invalidation and effect query; process lifetime, no durable store shown; M26 [CF].|
|Action admission state|Action Governance `_CURRENT`, `_HISTORY`, action→profile map; issue/query/invalidate; process-local; M19/M20 [CF].|
|Safety runtime state|Action/Safety Owner current runtime safety records; issue/query/invalidate; process-local; M19/M20 [CF].|
|Gateway admission state|Gateway private in-process runtime state; transition/query; A-route [CF].|
|CState version state|CState Owner in-process registry; issue/query/invalidate; cognitive consumers [CF].|
|Task lifecycle snapshot|Task facade/local registry projection; controlled task consumers; durable operational source U [CF/U].|
|FieldState / CurrentWorld candidates|Field reducer/evaluation build candidate/projection; authoritative durable world writer not demonstrated by M35 [CF].|
|Runtime allocation record|M48 records caller-supplied allocation outcome; not independent physical resource availability [CF].|
|Model Test Lens job files|Lens bridge local job/manifest persistence; evaluation consumer only [CF].|
|Badge scene/memory/risk|Badge process-local state; no inspected bridge into midplatform Owner stores [CF/U].|

State hazards, not verified corruption: registry snapshot treated as lifecycle authority; allocation preparation/record treated as physical availability; Field/CurrentWorld candidate projection treated as persisted truth; local currentness assumed globally durable. No dual-write pair was proven. Restart recovery/reconciliation is unresolved.

## 8. Protocol inventory

Cross-domain typed call/validation boundaries count as protocol candidates even without “protocol” in filenames. `v1` is file/DTO version where present; migration rules are mostly **U**. No authority transfers unless an Owner forms/adopts a new decision.

|ID|Source → target; object/contract; Owner, failure, status|
|---|---|
|P01|FPO→Capability: scoped requirement→resolution; Capability resolver; unknown cannot select; controlled [CF].|
|P02|Cognitive Flow→Capability: cognitive demand→demand-derived resolution; distinct source contract; partial [CF].|
|P03|Capability/Model/Provider→production selector: explicit refs→Owner reads→M11; active/admitted, unknown rejects; active selector [CF].|
|P04|Cognitive routing→admission compatibility→Provider target: routing/compatibility/mapping refs, lineage required; Provider Governance candidate [CF].|
|P05|Provider target→binding prep→binding candidate: identity/scope/lineage matching; controlled-direct FPO formation incomplete [CF].|
|P06|Binding→allocation/execution prep→Permission/Admission: candidate refs, Action/envelope, permission/safety/protocol/scope; only valid input forms registered Grant [CF].|
|P07|Grant→authorized provider adapter: grant identity/scope/current Owner state at effect time; unknown blocks native invocation [CF].|
|P08|ProviderRuntimeResult→RuntimeObservation: normalization preserves identity, error/empty-success/provenance; no truth transfer [CF].|
|P09|RuntimeObservation→Gateway: bounded envelope→Evidence/Observation admission; invalid input rejected [CF].|
|P10|Gateway→A-route→CState: admitted observation handoff; A-route does not acquire semantic authority [CF].|
|P11|Evidence→Context→FieldEvent: context/field refs mapped, Field event separately admitted; controlled evaluation in inspected chain [CF].|
|P12|FieldEvent→reducer→CurrentWorld: policy/reduction→state candidate/read projection→world candidate; controlled [CF].|
|P13|CurrentWorld/CState→Cognitive Flow: version and cognitive candidate handoff; product deployment U [CF/U].|
|P14|Decision→Task→Action: candidate judgement, task routing/lifecycle, Action Governance; controlled [CF].|
|P15|Action/working envelope→Grant: Action/Safety current query and bounded scope; controlled [CF].|
|P16|Outcome→reconsideration/re-observation: feedback and depth gates; controlled/synthetic [CF].|
|P17|Cognitive outcome→Memory/Experience/Learning: candidate handoff; durable assimilation U [CF/U].|
|P18|Evaluation→local runner/artifacts: Lens job/manifest/adapter, not product Runtime Grant [CF].|
|P19|Brain↔Organ: scattered handoffs/candidate bridges, no inspected single deployed bidirectional effect protocol; PARTIAL/UNRESOLVED [IN].|
|P20|Protocol Manager registry→candidate compatibility/version: explicit no runtime binding/mutation; planning [CF].|

Task↔Capability is M38 plus M05/M07, not one universal route. Capability↔Model and Model↔Provider bindings have registry/candidate facts, but complete final Grant current recheck is **U** (EA-GAP-01). Observation↔Evidence P09; Evidence↔Context P11; Context↔Field P11–P12; Field↔CurrentWorld P12; CurrentWorld↔Cognition P13; Decision↔Task P14; Action↔Runtime P06/P07/P15; Runtime↔Observation P08; Outcome↔Cognition P16; Cognition↔Memory P17. Badge↔midplatform transport/deployment protocol was not proven.

## 9. Mapping / bridge inventory

|ID|Source semantic role → target role; transformation; identity, provenance and authority|
|---|---|
|X01|FPO payload/case→FPO demand/request/requirement: **materialization**; derived IDs linked, not requester identity; provenance strings, no Entry Admission [CF].|
|X02|Cognitive strategy+coordination→cognitive demand: **derivation**; problem/branch lineage retained, no execution request [CF].|
|X03|FPO requirement→scoped capability resolution: **resolution**; requirement/capability linked, no provider authority [CF].|
|X04|Cognitive demand→demand-derived resolution: **resolution** with different source semantics; X03/X04 identities not interchangeable [CF].|
|X05|Provider declaration→Provider current view: **projection/guard**; explicit identity and source basis; no Model truth [CF].|
|X06|Model declaration→Model current view: **projection/guard**; explicit identity; M11 consumes [CF].|
|X07|Provider+Model current views→routing closure: **prerequisite admission**; no final execution authority [CF].|
|X08|Routing+compatibility+mapping→runtime target: **formation**; routing lineage structural, no fake refs allowed [CF].|
|X09|Target→binding prep→binding: **binding/refinement**; identity/scope/lineage linked, no invocation authority; missing lineage rejects [CF/DC].|
|X10|Binding→allocation/execution prep: **preparation**, not actual allocation; refs/provenance carried [CF].|
|X11|Grant input→Grant decision→current state: **authorization** created by Permission Owner and registered; input ref alone is not grant [CF].|
|X12|Provider result→RuntimeObservation: **normalization**; provider/model/execution identity and empty-success preserved; no world truth [CF].|
|X13|RuntimeObservation→Gateway evidence/observation: **admission/materialization**; Gateway authority bounded to observation [CF].|
|X14|Evidence + caller field/context/time refs→FieldEventCandidate: **mapping**; added refs caller-supplied, not inferred authority [CF].|
|X15|Admitted FieldEvent→reducer/read projection: **adapter/projection**; Field validation separate [CF].|
|X16|Controlled FieldState candidate→CurrentWorld candidate→CState: **projection/refinement**; persistent world authority U [CF/U].|
|X17|Task input mapping→task facade: **adapter**; invalid shape rejects, no direct Runtime Grant [CF].|
|X18|Model Test Lens runner artifacts→evaluation envelope: **evaluation adapter**, not runtime Evidence authority [CF].|

Mappings preserve or link the source identities specified above; none silently transfers source authority to target Owner. No full identity-preserving proof is asserted for the whole chain. Direct field copying is especially risky at X01/X08/X14: same string field name or nonempty ref is not semantic/authenticity equivalence. A provider result is a record, not a world state; a candidate is not an admitted fact.

## 10. Management / control plane inventory

|Managed object → controller|Input/state/decision/effect boundary and effectiveness|
|---|---|
|Model lifecycle → Model registry/state machine/read|registry/transition→bounded current view; production routing gate, not execution [CF].|
|Provider lifecycle → Provider registry/read|explicit provider identity→bounded current view; M11 routing gate [CF].|
|Capability eligibility → official catalog|declaration→controlled/production profile, not per-request admission [CF].|
|Protocol/version → Protocol Manager facade|registry→compatibility candidate; no runtime load/bind/mutation [CF].|
|Provider target/binding → Provider Governance|routing/compatibility/identity→candidate, lineage check; not Grant [CF].|
|Permission/Admission → Grant+current state|Action/Safety/permission/scope/binding/prep→decision, register/query/invalidate; effect guarded by M20 [CF].|
|Action/Safety → Action Governance|action/envelope/safety→current records; Grant/effect prerequisites [CF].|
|Observation → FPO/Gateway|FPO creates bounded request/control; Gateway separately admits observation [CF].|
|Field → Field Event API/reducer|event admission then candidate reduction; live durable mutation not proven [CF].|
|Currentness → Owner-local stores|Action/Safety, Grant, Gateway, CState own domain currentness; no global currentness authority shown [CF].|
|Evaluation → Lens/controlled runners|jobs/artifacts/recorded cases; real effect only with current Grant, otherwise candidate [CF].|
|Diagnostics/deployment → runners/verifiers/Badge/backend|manifest/status are records, not Owner state; topology U [CF/U].|

Control/data-plane separation is uneven. Real YOLO runner assembles routing-shaped governance candidates while coordinating native execution; prior lineage rejection is a responsibility leak, not authority to issue a Grant. Registry declarations and evaluation job files must not be promoted to authority.

## 11. Runtime path reconstruction

|Path|Status / inspected call chain / limitation|
|---|---|
|Cognitive-driven observation|PARTIAL: M06→M07→routing/compatibility candidate→M15–M19 in controlled/sandbox formation; deployed real invocation unproven [CF/U].|
|Re-observation|PARTIAL: M04 request/control and M36/M46 feedback/depth gates; native closed loop U [CF/U].|
|Task-driven capability|PARTIAL: M38 task capability routing plus M05/M07 resolution; exact production Task→Provider edge U [CF/U].|
|Action→runtime|CONTROLLED/PARTIAL: M21/M22/M23→M19→M20/M26; M47 is separate candidate gate [CF].|
|Provider real execution|CONTROLLED: real runner→M25/M26→M27/M28; authorization/lineage failure in prior evidence [CF/DC].|
|Observation→Evidence|CONTROLLED: M27→M28; real and synthetic result entry guarded [CF].|
|Evidence→Context→Field→CurrentWorld|CONTROLLED: M35 stitches M31–M34; M25→M35 call not found [CF].|
|CurrentWorld→cognition|CONTROLLED/PARTIAL: M35 candidate and M30/M36 controlled adapters; deployed state handoff U [CF/U].|
|Controlled real-provider evaluation|BROKEN end-to-end authority: M04/M16–M20/M25–M29; prior YOLO NOT_GO, focused lineage failures [CF/DC].|
|Model/provider production routing|IMPLEMENTED prerequisite: M08–M11 consumed by selector/OCR/multi-provider; not full production eligibility [CF/DC].|
|Outcome/reconsideration|CONTROLLED/SYNTHETIC: M40/M36/M46 feedback; autonomous deployed loop unproven [CF].|
|Memory/Experience handoff|CONTROLLED: M41/M42 candidate stages; durable assimilation U [CF/U].|

## 12. Effective / partial / dormant mechanisms

Effective **within inspected boundaries**: bounded lifecycle reads and MOIP selector prerequisite; Gateway bounded observation admission; effect-time authorization rejection; Provider result normalization; Lens local evaluation job processing. Partial: controlled real YOLO grant/lineage, Field→CurrentWorld production continuation, resource availability, Cognitive→native effect loop, process-restart currentness. Synthetic/candidate: product loop, RuntimeExecutor case gate, Cognitive demand/Intent, Protocol facade. `DEFINED_BUT_NO_CONSUMER` is not asserted for any named major mechanism: sampled inbound searches cannot establish repository-wide absence. No significant mechanism was marked `TEST_ONLY` merely because a test exists.

## 13. Orphan / under-specified mechanism inventory

|ID / classification|Code fact and impact|
|---|---|
|O01 IMPLEMENTED_BUT_ARCHITECTURALLY_ORPHANED|Badge/MVP entry has no inspected import edge to midplatform Grant/Gateway; deployment relationship U [CF/U].|
|O02 CANONICAL_BUT_UNDER_SPECIFIED|Controlled FPO request has refs but no proven Owner-governed specific execution-entry decision [CF/IN].|
|O03 RESPONSIBILITY_LEAK|Real provider runner constructs routing-shaped target/binding refs from case/trace/request; prior lineage validator rejects [CF/DC].|
|O04 CANONICAL_BUT_UNDER_SPECIFIED|Grant current model/binding compatibility recheck not demonstrated, EA-GAP-01 [CF/U].|
|O05 CANONICAL_BUT_UNDER_SPECIFIED|Allocation prep/record is not actual resource availability/currentness, EA-GAP-02 [CF].|
|O06 CANONICAL_BUT_UNDER_SPECIFIED|Expiry ref exists but temporal interpretation at effect time not demonstrated, EA-GAP-03 [CF/U].|
|O07 IMPLICIT_MAPPING|Evidence→Field needs caller-supplied field/time/context; no inspected authoritative live mapping [CF].|
|O08 LEGACY_OR_TRANSITIONAL|Protocol facade declines runtime binding/mutation while separate runtime uses direct adapters [CF].|
|O09 CANONICAL_BUT_UNDER_SPECIFIED|CState local version and CurrentWorld evaluation candidate are not a proven shared persistent world state [CF/U].|

These are classifications, not decisions to deprecate or consolidate.

## 14. Duplicate / overlap inventory

|ID|Semantic / implementations / current effect / ownership status|
|---|---|
|D01|“Observation demand”: Cognitive M06 vs FPO M04; **different loop levels**, not same identity; real bridge/refinement unproven [CF].|
|D02|Capability resolution: M07 cognitive demand-derived vs M05 FPO scoped; different sources, overlapping outcome; unification U [CF].|
|D03|Admission: Action M21, Gateway M28, Field M33, Grant M19, M47 candidate gate; distinct effects but naming invites final-authority collapse [CF].|
|D04|Currentness: Model/Provider projections, Action/Safety, Grant, Gateway/CState; domain-local, not necessarily duplicate truth; cross-state consistency U [CF/U].|
|D05|Provider selection: M11 production prerequisite vs controlled explicit real-provider M25; controlled grant cannot imply production admission [CF].|
|D06|Execution: Badge M01/M02, midplatform real M25, synthetic M24/M46/M47; separate scopes, no unified deployed seam proven [CF/U].|
|D07|State/CurrentWorld: Badge scene, FieldState evaluation candidate, CState version, CurrentWorld candidate; semantic relation under-specified [CF/U].|

Need/requirement/request/requester and closure/sufficiency/outcome recur across code, but this sample is insufficient to count every variant; these are unresolved rather than invented duplicates.

## 15. Semantic drift findings

|ID|Finding|
|---|---|
|S01|`get_provider_by_id(model_id)` matches provider record `model_id` despite function name; identity role easy to misread [CF].|
|S02|FPO `source_owner` and `case_id` are not governed requester identity; controlled YOLO upstream source remains unproven [CF/IN].|
|S03|Cognitive `ObservationDemandCandidateV1` says never execution request; FPO same-named demand is execution-layer [CF].|
|S04|Product-loop `ControlledExecutionRequestV1` is synthetic/candidate, `real_execution=False`; name does not make real Entry Admission [CF].|
|S05|Runner's nonempty trace/request refs were used as routing/compatibility lineage but failed validator; ref ≠ authenticity [CF/DC].|
|S06|Allocation preparation/record naming can imply held resources; code records preparation/caller outcome, not availability [CF].|
|S07|Protocol Manager compatibility/admission candidates are not runtime binding/final authority; explicit false flags [CF].|
|S08|Gateway OCR empty-success has modality-specific guard; native result ≠ world truth [CF/DC].|

## 16. Architecture debt inventory — no remediation proposed

|ID / class|Observed boundary|
|---|---|
|A01 MISSING_AUTHORITY_BOUNDARY|Controlled real formation Entry Admission Owner decision/currentness unproven; PR02 [CF/IN].|
|A02 PATH_SPECIFIC_ASSUMPTION|Binding/Grant inputs structurally require routing-shaped lineage despite controlled FPO entry; prior rejection [CF/DC].|
|A03 MISSING_CURRENTNESS|Final model/binding compatibility recheck not shown, EA-GAP-01 [U].|
|A04 MISSING_AUTHORITY_BOUNDARY|Preparation/record vs actual resource availability, EA-GAP-02 [CF/U].|
|A05 MISSING_CURRENTNESS|Expiry boundary temporal interpretation not shown, EA-GAP-03 [CF/U].|
|A06 MISSING_MAPPING|No inspected real Gateway Evidence→Field/CurrentWorld authoritative continuation; evaluation bridge exists [CF].|
|A07 IMPLICIT_CONTRACT|Governed controlled requester/source object absent in inspected YOLO entry; case/runner not request authority [CF/IN].|
|A08 LEGACY_COUPLING|Badge and midplatform independent loop/runtime families; deployment relationship U [CF/U].|
|A09 UNUSED_ARCHITECTURE|Protocol Manager runtime flags false; planning consumer exists, production consumer unproven [CF].|
|A10 MISSING_PROTOCOL|Unified Brain↔Organ and Outcome↔live cognition deployment contract not established [U].|

## 17. Known working mechanisms and verification state

**CF** Gateway has explicit bounded admission and empty-success handling; real vision adapter queries current effect eligibility before invocation; MOIP closure is consumed by production-style selector and OCR/multi-provider/identity views; Field Event admission and reducer have a controlled validation/candidate chain; CState Owner maintains version/query/invalidation. **DC** Existing local retrospective `docs/architecture/governance/luna_repository_rebaseline_v1/external_sensory_engineering_retrospective_06_5_r02_v1.md` and prior user-terminal evidence report: MOIP focused 61/61 PASS; profile governance 12/12 PASS; existing authorization regression 84/84 PASS; PR02 focused propagation 2 PASS / 7 FAIL; real YOLO `RUNTIME_AUTHORIZATION_NOT_CURRENT` and verifier `NOT_GO`. Those historical results were not rerun here. **IN** Component behavior does not establish full production readiness. PR-ADMISSION-02 remains `PAUSED_PENDING_ARCHITECTURE_COMPLETENESS_REVIEW`, not fixed.

## 18. Unknown / unresolved areas

1. Exact deployed entry points, process topology, and whether Badge/backend and midplatform share any Owner state.
2. Repository-wide inbound consumers for every protocol, policy, candidate, schema, and adapter; no-use claims need broader call-graph verification.
3. Durable Field/CurrentWorld mutation, replay, concurrency, crash recovery, and cross-process currentness.
4. Full Cognitive Demand→FPO execution materialization and native re-observation loop.
5. Governed controlled evaluation source/requester object and per-request Entry Admission decision/currentness.
6. Model identity and capability↔model↔provider compatibility recheck at Grant/effect boundary; actual resource availability; temporal expiry enforcement.
7. Production deployment of protocol/version, safety/resource/diagnostic/evaluation mechanisms beyond sampled consumers.
8. JSON schema/version migrations and transport compatibility; generalized Brain–Organ seam beyond inspected adapters.
9. Local-vs-Hive authority topology; no remote requirement is inferred.

## 19. Files inspected / source index

The following index names **63 distinct paths** (including the nine mandatory governance assets and the 06.5 ledger) consulted by direct source read or targeted `rg` line matches; it is not a claim that all 63 files were read end-to-end. Some batched tool output was truncated. The 49 mechanism rows give the named implementation coverage; this index adds controls and context. All paths are relative to the physical root.

- Root: `main.py`, `runtime/main_loop.py`, `luna_backend/app.py`; repository `AGENTS.md`; nine mandatory assets under `docs/architecture/governance/luna_engineering_execution_and_verification_governance_v1/` (phase role, verification authority, mode matrix, required fields, instruction template, naming, status, failure classification, compliance contract).
- `capabilities/midplatform/core/provider_runtime_to_observation_ingress/`: `engine_v1.py`, `real_provider_execution_engine_v1.py`, `real_provider_execution_runner_v1.py`, `provider_result_adapter_v1.py`, `real_provider_execution_verifier_v1.py`.
- `capabilities/midplatform/field_perception_orchestrator/integration/`: `field_perception_active_observation_control_engine_v1.py`, `field_perception_real_vision_provider_adapter_v1.py`, `perception_routing_admission_compatibility_v1.py`.
- `capabilities/midplatform/core/observation_gateway/observation_gateway_engine_v1.py`; `core/a_route_orchestration/a_route_orchestration_engine_v1.py`; `core/a_route_orchestration/integration/a_route_product_loop_integration_engine_v1.py`; `core/cognitive_state_formation/cognitive_state_formation_engine_v1.py`.
- `capabilities/midplatform/model_manager/registry/`: `provider_registry_loader_v1.py`, `provider_current_state_read_v1.py`; `model_manager/lifecycle/`: `model_current_state_read_v1.py`, `model_registry_state_machine_v1.py`; `model_manager/engines/model_provider_routing_lifecycle_closure_v1.py`.
- `capabilities/midplatform/model_manager/registries/universal_capability_slot/`: `universal_capability_slot_resolution_v1.py`, `observation_demand_capability_resolution_v1.py`, `official_capability_catalog_governance_v1.py`.
- `capabilities/midplatform/provider_runtime_governance/`: `provider_runtime_governance_registry_v1.py`, `provider_runtime_target_preparation_v1.py`, `provider_binding_runtime_preparation_v1.py`, `provider_binding_candidate_v1.py`; `permission_and_admission_manager/module/`: `runtime_execution_grant_v1.py`, `runtime_authorization_state_v1.py`.
- `capabilities/midplatform/core/action_governance/`: `action_admission_governance_v1.py`, `action_governance_engine_v1.py`; `core/cognitive_flow/integration/a_working_envelope_cognitive_requirement_bridge_controlled/working_envelope_governance_v1.py`.
- `capabilities/midplatform/core/runtime_executor/`: `runtime_allocation_preparation_candidate_v1.py`, `runtime_allocation_execution_instance_v1.py`, `runtime_executor_engine_v1.py`.
- `capabilities/midplatform/core/`: `context_foundation/context_foundation_skeleton_v1.py`, `evidence_to_field_event_adapter_v1.py`, `field_event_admission_api_v1.py`, `field_state_reducer/module/field_state_reducer_module_facade_v1.py`.
- `capabilities/midplatform/core/cognitive_flow/`: `observation_demand_formation_v1.py`, `cognitive_flow_engine_v1.py`, `cognitive_dynamic_loop_engine_v1.py`; `core/intent_governance/intent_governance_skeleton_v1.py`; `core/task_manager/module/task_manager_module_facade_v1.py`.
- `capabilities/midplatform/core/`: `decision_governance/decision_governance_engine_v1.py`, `outcome_evaluation_governance/outcome_evaluation_engine_v1.py`, `cognitive_memory_experience/cognitive_memory_experience_engine_v1.py`, `cognitive_learning/cognitive_learning_engine_v1.py`, `temporal_coordinate/temporal_coordinate_v1.py`.
- `capabilities/midplatform/protocol_manager/module/protocol_manager_module_facade_v1.py`; `model_test_lens/local_runner_bridge/local_runner_bridge_service_v1.py`; `capabilities/evaluation/evidence_context_field_current_world_controlled/engine_v1.py`; existing 06.5 retrospective noted above. Focused test paths were searched for historical context, never executed.

## 20. Final census summary

This sampled census identifies **49 named mechanisms, 18 grouped domains, 20 protocol candidates, 18 mappings/bridges, 12 control-plane rows, and 12 state rows**. It records **9** under-specified/orphan findings, **7** overlap topics, **1** specific runner responsibility leak, **0 proven additional final-authority leaks**, **8** semantic-drift findings, **1** consequential implicit mapping (Evidence→Field), and **1** unowned pre-Grant entry protocol gap. At least **9** broad areas remain unresolved. These are table counts, not exhaustive global counts or a target architecture. No remediation, new Owner, or production-readiness claim is made. Architecture reconciliation should independently adjudicate target architecture using these code-side findings.
