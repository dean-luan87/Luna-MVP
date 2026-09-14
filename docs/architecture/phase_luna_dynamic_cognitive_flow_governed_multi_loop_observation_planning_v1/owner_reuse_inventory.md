# Owner and asset reuse inventory

This inventory is aligned to the Brain-subject / subordinate-Loop baseline.

## Classification

- **Already reusable**: existing owner and candidate type can be referenced
  without semantic change.
- **Reusable with minimal extension**: the next controlled implementation may
  add a candidate-only envelope or mapping field, but must preserve the owner.
- **Missing for next implementation**: an explicit Loop-local reference or
  assessment record is not yet present.
- **Deferred**: intentionally outside this phase.
- **Conflict**: an apparent parallel owner or authoritative-state duplication
  that must be rejected.

## Canonical owners

| Concern | Canonical owner | Reused asset | Phase use |
|---|---|---|---|
| Cognitive Loop identity and lifecycle envelope | Cognitive Flow Governance | `cognitive_flow_registry_v1.py`, `CognitiveCycleStateCandidateV1` | Reusable with minimal extension; no new owner |
| Dynamic state transition | Cognitive Flow Governance | `DynamicCognitiveFlowEngineV1`, `DynamicCognitiveLoop*V1` | Reuse state-version, sufficiency, reconsideration, stale Requirement behavior |
| State formation and state versions | Cognitive State Formation Governance | `CognitiveStateVersionCandidateV1`, B2 integration | Loop stores references; it does not own state formation |
| Intent | Intent Governance | intent lifecycle/resource/handoff types | Loop stores `intent_refs`; resume never recreates Intent |
| Reconsideration | Cognitive Flow / Outcome Evaluation consumers | `ReconsiderationCandidateV1` | `REQUEST_MORE_EVIDENCE` enters reassessment, not execution |
| Need to Requirement | Capability Requirement Bridge | `CognitiveNeedCandidateV1`, `CapabilityRequirementFormationCandidateV1` | Only the current minimum Need may form a new Requirement |
| Scope / Resolution / Invocation Candidate | Capability Governance / Universal Capability Slot | existing scope, resolution, invocation candidate types | Candidate checks remain mandatory on continuation |
| Evidence admission | Observation Gateway | `ObservationCandidateV1`, gateway admission states | Output is candidate evidence, never World Truth |
| Observation continuation | Field Perception Orchestrator / Active Observation Control | B4 `ReobserveCandidateV1` | Creates a governed observation candidate only |
| Task lifecycle | Task Manager | `TaskState`, `TaskReadiness`, task lifecycle module | Task remains distinct; loop does not mutate it |
| Safety / Survival | existing Safety / Survival governance | safety and permission/resource boundary contracts | Safety can produce priority/preemption candidates |
| Resource constraints | Intent Governance and existing resource governance | `IntentResourceConstraintV1`, resource references | Shared resources are references; allocation algorithm is deferred |
| Attention | Cognitive State Formation Governance | `AttentionCandidateV1` | Attention refs are loop context, not loop-owned attention |
| Context / Field / Current World | Context Foundation / Field State owners | `CurrentWorldCandidateV1`, context and field refs | Loop keeps versioned read-only refs |
| Brain baseline and Loop materialization | Brain / existing Brain Governance | Brain Golden Baseline and Brain boundary architecture | Reusable governance boundary; Brain decides whether a persistent Loop is warranted |
| Role / Perspective | existing Role / Perspective governance | Intent handoff `role_refs`, Brain perspective/context contracts | Reusable read-only continuity and relevance refs |
| Emotion modulation | existing Emotion / Personality governance | emotion reference and modulation boundary contracts | Reusable input; no Loop-owned emotion state or Truth mutation |
| Experience / Memory | Cognitive Memory/Experience | `ExperienceCandidateV1`, `MemoryCandidateV1` | Reusable future bridge only; mutation deferred |
| Spatial / Temporal continuity | Field / Context / outcome temporal owners | Current World temporal refs, outcome spatial/temporal scope | Reusable references; explicit Loop continuity assessment is a minimal extension |
| Hive | future indirect Experience / Cognitive Prior source | no Loop runtime asset | Deferred; Hive cannot control Loop runtime |

## Authority versus Loop-local state

| Category | Examples | Loop treatment |
|---|---|---|
| Authoritative data | Intent, Role, Field, Safety, Resource, Memory, Emotion, Provider identity | Store read-only refs and source versions; never duplicate or mutate |
| Source-owned candidates | Current World candidate, Task/Behavior state, Attention, Observation evidence, Capability Scope/Resolution | Preserve owner refs and source versions; never promote to World Truth or duplicate authority |
| Loop-local state | local disposition, current Need, hypothesis lineage, pending candidates, state versions, pause/wait reason | Loop may own candidate-only state for its one concern |
| Read-only references | Context, Attention, Evidence, Requirement, Observation, Task/Behavior, priority, continuity, trace/provenance | Preserve refs and versions; reassess on resume |

## Capability classification

| Capability | Classification | Alignment |
|---|---|---|
| Brain materialization decision | Already reusable | Brain remains subject and governance authority |
| Loop-local identity envelope | Reusable with minimal extension | No new owner; candidate-only reference envelope |
| Lifecycle mapping | Reusable with minimal extension | Reuse Suspend/Resume/Reconsideration/DEFER/COMPLETED; document gaps |
| Continuity assessment record | Missing for next implementation | Add candidate-only assessment, not a continuity owner |
| Need-driven multi-capability reservation | Missing for next implementation | Add mapping/fixture fields; no execution |
| Branch/sub-loop derivation reservation | Missing for next implementation | Reference-only fields; Brain-owned creation |
| Loop Closure / Outcome bridge | Missing for next implementation | Candidate package only; Experience mutation deferred |
| Autonomous arbitration/scheduling | Deferred | Existing global governance refs only |

## Required capability classification matrix

| Required concern | Classification | Alignment decision |
|---|---|---|
| Dynamic Cognitive Flow | 1. already reusable | Keep `DynamicCognitiveFlowEngineV1` as the transition owner |
| Cognitive State / state version | 1. already reusable | Reuse state-version candidates and source-version checks |
| Intent Governance | 1. already reusable | Loop stores refs; Intent remains authoritative |
| Reconsideration | 1. already reusable | Reuse `ReconsiderationCandidateV1` |
| Suspend / Resume | 1. already reusable | Reuse `SuspendCandidateV1` / `ResumeCandidateV1` |
| Need → Requirement Bridge | 1. already reusable | Current minimum Need remains the only binding demand |
| Capability Scope / Resolution / Invocation | 1. already reusable | Re-enter gates for every new capability candidate |
| Observation Gateway / FPO / Active Observation Control | 1. already reusable | Reuse `ObservationCandidateV1` and `ReobserveCandidateV1` |
| Attention | 1. already reusable | Preserve read-only Attention refs |
| Current World / Context / Field | 1. already reusable | Preserve source-owned refs and versions; no Loop mutation |
| Task Manager / Task-Behavior continuity | 2. reusable with minimal extension | Add continuity refs only; no Task lifecycle ownership |
| Safety / Survival governance | 1. already reusable | Safety priority may preempt, never bypass gates |
| Resource Governance | 2. reusable with minimal extension | Add resource envelope and resume reassessment refs |
| Role / Perspective continuity | 2. reusable with minimal extension | Reuse role refs and add continuity assessment candidate |
| Emotion modulation | 2. reusable with minimal extension | Reuse modulation refs; no Emotion ownership or Truth mutation |
| Loop identity envelope | 2. reusable with minimal extension | Add candidate-only envelope around existing Flow types |
| Continuity assessment | 3. missing but required for next implementation | Add six-signal candidate assessment |
| Multiple capability reservation | 3. missing but required for next implementation | Add Need-driven candidate chain without execution |
| Branch / sub-Loop reservation | 3. missing but required for next implementation | Add refs only; Brain owns derivation |
| Cognitive Outcome / Loop Package bridge | 3. missing but required for next implementation | Add closure/output candidate refs only |
| Experience / Memory mutation | 4. deferred | Preserve existing candidate types; no mutation |
| Hive runtime control | 4. deferred | Future indirect Prior source only |
| Autonomous scheduling / arbitration algorithm | 4. deferred | Priority and arbitration refs only |
| Parallel Loop owner or second governance layer | 5. conflicts with clarified architecture | Explicitly prohibited |

## Closure-phase reuse update

The lifecycle closure extension reuses the existing `LoopClosureRecordCandidateV1`,
`CognitiveOutcomeCandidateV1`, and `LoopPackageReservationCandidateV1` as
record/output/reservation primitives. New same-package envelopes provide only
the missing assessment-versus-acceptance, final-state-freeze, assimilation,
and history-boundary metadata. `ExperienceCandidateV1` and `MemoryCandidateV1`
remain read-only future references; Task Manager, Intent Governance, Brain
Golden Baseline, Safety, Resource, Field, Current World, and Capability
Governance remain external canonical owners.

## Important existing semantics

`ReconsiderationCandidateV1` already carries a `cycle_id`, source stage, target
stage, reason, related refs, candidate-only status, runtime-execution guard,
and trace. The proposed `loop_id` is the stable identity used to scope that
cycle reference; it does not replace the canonical reconsideration type.

`SuspendCandidateV1` and `ResumeCandidateV1` already express controlled
pause/resume candidates. They are read-only proposals and do not perform a
runtime suspend or resume.

`CognitiveCycleSnapshot` already carries Context, PCN, Intent, state formation,
Attention, Hypothesis, Current World, state vector, regulation, Field, and
provenance references. The new loop identity contract should reuse this shape
for loop-local reference preservation rather than introducing another world
snapshot model.

## Conflicts rejected

- No Loop Brain, Loop Manager, Loop Planner, or second Cognitive Governance
  owner.
- No Loop-owned Intent, Role, Field, Emotion, Safety, Resource, Memory,
  Experience, Action, World Truth, or Provider identity.
- No autonomous recursive Loop spawning or cross-loop state merge.
