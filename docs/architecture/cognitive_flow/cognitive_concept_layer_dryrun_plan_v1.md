# Cognitive Concept Layer Controlled DryRun Plan v1

## Phase scope

Phase-A3-Cognitive-Concept-Layer-DryRun-v1-001 verifies the existing Concept Controlled Skeleton with six frozen, abstract Primitive-reference fixtures. It is a structural and governance check only; it does not create concepts by inference.

## Fixed fixture scope

| Case | Fixed input cluster | Expected candidate type |
| --- | --- | --- |
| 1 | Primitive Pattern | `pattern_concept_candidate` |
| 2 | Primitive Situation | `situation_concept_candidate` |
| 3 | Primitive Relation | `relationship_concept_candidate` |
| 4 | Risk Primitive Cluster | `risk_candidate_concept` |
| 5 | Context Primitive Cluster | `context_concept_candidate` |
| 6 | Goal Primitive Cluster | `goal_candidate_concept` |

## Non-goals

No Runtime, provider, model, real Evidence, Field Kernel, Reducer, Hive, Learning System, decision, action, fact admission, or state mutation is introduced. The runner uses only fixed identifiers and calls only the existing Concept Skeleton.

## Evidence flow

`fixed Primitive references -> Concept Skeleton -> serialized Concept Candidate envelopes -> independent serialized-output Verifier`.

The executor and verifier are intentionally separated: the verifier reads JSON evidence and imports neither Runner nor Skeleton.
