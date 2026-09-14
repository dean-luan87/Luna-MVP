# Luna Cognitive Logic Conformance Test Contract v1

## Purpose

This reusable contract verifies that Luna's cognitive behavior conforms to its
intended logic in addition to checking that the software operated successfully.
It is documentation doctrine only; it adds no runtime owner, schema, fixture,
or verifier implementation.

Every core acceptance report must expose two independent dimensions:

```yaml
operational_result: PASS | FAIL
cognitive_logic_result: PASS | FAIL
final_decision: GO | NOT_GO
```

`final_decision=GO` is permitted only when both results are `PASS`. A verifier
or runner must not collapse these dimensions into one undifferentiated PASS.
Operational success with cognitive failure, and cognitive conformance with an
operational failure, are both valid intermediate states.

## Conformance dimensions

The following dimensions are mandatory when applicable. An inapplicable or
uninstrumented dimension is reported as `NOT_EVALUATED`, `NOT_OBSERVED`,
`NOT_INSTRUMENTED`, or `UNAVAILABLE`; it is not silently treated as PASS.

| ID | Dimension | Required conformance |
| --- | --- | --- |
| BRAIN | Brain positioning | Brain is a coordination/responsibility domain and does not absorb canonical governance ownership. |
| FIELD | Field cognition | Physical Field is distinct from role-conditioned interpretation and task-conditioned Current World Candidate. |
| ROLE | Role-conditioned cognition | A materially relevant role can affect attention, relations, relevance, needs, risk/permission interpretation, and decisions. |
| TASK | Task/Goal-conditioned cognition | Goal/task changes can affect attention, Information Need, relevance, sufficiency, stopping, and decisions before Task Manager. |
| CONTEXT | Context-conditioned cognition | Context is consumed as cognitive conditioning input where the case requires it, without becoming a hidden mutation source. |
| ATTENTION | Attention selection | Selection is need-, role-, task-, and context-relevant rather than an undifferentiated observation sweep. |
| NEED | Information Need formation | The active Goal/Intent/Concern is translated into an explicit need or an explicit unavailable state by the applicable owner. |
| EVIDENCE | Evidence handling | Observation output is handled as Evidence Candidate with relevance, conflict, missingness, and uncertainty preserved. |
| HYPOTHESIS | Hypothesis formation/revision | Hypotheses are candidates; materially relevant new evidence can cause canonical revision. |
| SUFFICIENCY | Minimum sufficient cognition | Sufficiency means enough relevant information for the active objective, not total visibility or certainty. |
| STOP | Stop logic | Stop follows canonical sufficiency/need completion and carries an explicit reason; missing required information cannot be silently stopped. |
| DECISION | Decision ownership | Decision semantics remain with Decision Governance and are not produced by Brain, Evaluation, or Cognitive State Formation. |
| TASK_OWNER | Task ownership | Task semantics remain with Task Manager and are not executed by Decision Governance, Brain, or cognition. |
| TRUTH | No World Truth promotion | Evidence, Hypothesis, and Current World Candidate never become World Truth by implication or confidence. |
| ECONOMY | No irrelevant over-observation | Irrelevant changes do not cause Field cognition to change, and observation does not continue after minimum sufficiency without a justified need. |

## Reusable assertion inventory

These identifiers are evaluated against actual runtime data and causal
references, not only a hard-coded summary boolean.

### Perspective and conditioning

- `role_changes_attention`
- `role_changes_relation_interpretation`
- `role_changes_evidence_relevance`
- `task_changes_information_need`
- `task_changes_sufficiency_threshold`
- `task_changes_stop_condition`
- `role_task_change_can_change_hypothesis`
- `role_task_change_can_change_current_world_candidate`
- `role_task_change_can_change_decision_candidate`
- `physical_field_not_mutated_by_role_change`
- `physical_field_not_mutated_by_task_change`
- `same_evidence_can_have_different_relevance`
- `irrelevant_change_does_not_change_field_cognition`

### Information and truth boundaries

- `evidence_not_promoted_to_fact`
- `hypothesis_not_promoted_to_truth`
- `current_world_candidate_not_promoted_to_world_truth`
- `missing_information_produces_gap`
- `material_new_evidence_can_trigger_revision`
- `sufficient_information_produces_stop`

For role/task assertions, the case must declare that the changed input is
materially relevant. Otherwise the result is `NOT_EVALUATED` or an explicitly
documented invariant, not a forced claim that cognition must differ.

## Information-processing semantics

The expected relation is:

```text
external capability output
  → Observation
  → Evidence Candidate
  → relevance / conflict / missingness / uncertainty
  → Hypothesis
  → Current World Candidate
  → Sufficiency
  → Gap / Revision / Re-observation / Stop
```

When an ingress supplies an explicit Evidence-to-information support binding,
coverage is derived only from admitted Evidence whose canonical relevance state
is `RELEVANT`. An `IRRELEVANT` Evidence candidate remains candidate-only and
cannot satisfy a required information ref. Inherited information from an
earlier governed observation cycle remains available through its own lineage;
it is not re-attributed to the new Evidence. Callers without an explicit
binding retain their existing declared-availability compatibility behavior.

Evidence is not Fact. Hypothesis is not World Truth. Current World Candidate
is not World Truth. Confidence is not Truth. Conflicting evidence must not be
forced into a fact, and missing information must remain a Gap when it matters
to the active objective.

An A-Route may form a `Governed-condition-driven Minimum Relevant Cognitive
View` from available Self and External candidate information before downstream
Need or Observation Demand handling. Selection uses declared governed condition
coverage; object type does not create a second algorithm. Selected information
can form current cognitive coverage, while excluded information remains
recoverable. This does not claim generalized semantic relevance, autonomous
semantic Attention, or generalized meaning understanding.

Before that selection, A-Route may form a candidate-only set of currently
required cognitive conditions from explicit governed objective-condition rules
and the current selected cognitive situation. Objective applicability,
activation/suppression, coverage satisfaction, and minimum-set selection are
exact-reference operations; Goal, Context, Scenario, and Case strings are not
parsed. This formation is upstream of Information Need and is distinct from
both Goal Governance and `Required Conditions - Current Coverage` Need
formation. The bounded maturity claim is
`Governed State-Sensitive Required Cognitive Condition Formation`, not
autonomous Goal understanding or generalized planning.

A governed objective-condition rule may optionally declare explicit alternative
satisfaction basis references for one semantic requirement. In that bounded
case, any currently covered basis satisfies the requirement and only the actual
matched coverage reference is retained. Rules without alternatives preserve
legacy exact-coverage behavior. This does not introduce a Boolean sufficiency
language, evidence fusion, confidence algebra, or acquisition-path semantics.

## Reusable contrast categories

| Category | Controlled change | Expected observation |
| --- | --- | --- |
| `SAME_FIELD_DIFFERENT_ROLE` | Same physical Field, different materially relevant Role | Attention, relation interpretation, relevance, need, or downstream candidates may differ; physical Field does not mutate. |
| `SAME_FIELD_DIFFERENT_TASK` | Same physical Field, different Goal/Task | Task-relevant attention, Information Need, sufficiency/stop, or decision candidate may differ; physical Field remains unchanged. |
| `SAME_FIELD_DIFFERENT_ROLE_AND_TASK` | Same Field, both conditioning inputs changed | Combined perspective may change cognition; each change remains attributable and no candidate becomes truth. |
| `SAME_ROLE_TASK_IRRELEVANT_FIELD_CHANGE` | Same Role/Task, Field change irrelevant to the need | Field cognition and conclusions do not change merely due to irrelevant content; no over-observation. |
| `SAME_EVIDENCE_DIFFERENT_GOAL` | Same Evidence, different active Goal | Relevance and Information Need may differ without mutating Evidence or declaring a fact. |
| `SAME_GOAL_MISSING_EVIDENCE` | Same Goal, required evidence withheld | Canonical Gap/insufficiency is produced; successful Stop is invalid. |
| `SAME_GOAL_CONFLICTING_EVIDENCE` | Same Goal, materially conflicting evidence supplied | Conflict/uncertainty is preserved; no forced fact or World Truth promotion occurs. |

## Ownership and forbidden behavior

Brain may coordinate and reference, but must not:

- execute perception models or model/provider calls directly;
- mutate Physical Field, Memory, or Experience;
- declare World Truth;
- own Decision or Task semantics;
- execute Action or absorb an existing Governance owner;
- bypass Observation Gateway, Cognitive State Formation, or canonical
  Decision/Task boundaries.

Decision remains owned by Decision Governance, Task remains owned by Task
Manager, and cognition remains owned by its existing canonical owners. Missing
canonical ownership remains unresolved rather than being assigned to Brain for
test convenience.

## Evidence and result contract

For every applicable assertion, preserve source run, case, execution, cycle,
owner, and relevant candidate references. Multi-cycle tests must verify exact
causal identity continuity for Gap, Re-observation, next-cycle ingress,
revision, Sufficiency, and Stop.

Unknown measurements retain `NOT_OBSERVED`, `NOT_INSTRUMENTED`,
`UNAVAILABLE`, or `PLANNED`. Values such as `0` or `false` must not substitute
for unavailable metrics or unobserved stages.

Major E2E and full-regression reports should expose at least:

```yaml
operational_result: PASS | FAIL
cognitive_logic_result: PASS | FAIL
cognitive_logic_assertions:
  - assertion_id: role_changes_attention
    status: PASS | FAIL | NOT_EVALUATED | UNAVAILABLE
    evidence_refs: []
    owner_refs: []
    notes: ...
final_decision: GO | NOT_GO
```

`final_decision` must be derived from the two result dimensions and the
phase's independent artifact/acceptance rules. A single aggregate PASS is
insufficient. Phase documents reference this contract instead of duplicating
its full contents.
