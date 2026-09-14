# Cognitive Analysis Object Contract v1

## 1. Contract posture

This document plans object meaning and fields; it is not a Python API, JSON
Schema, persistence contract, or runtime protocol. All A3 objects are
candidate/read-side objects. They preserve `provenance` and `trace`, and none
has Field State mutation authority.

## 2. Planned objects

### 2.1 CognitiveAnalysisAdmissionResultV1

| Item | Planned contract |
| --- | --- |
| Input | One `CurrentCognitiveContextV1` and declared permission context. |
| Required assessment | context existence, stale/refresh state, Context Sufficiency, critical gaps, read permission, provenance/trace completeness, source-Snapshot traceability. |
| Status | `admitted`, `conditionally_admitted`, `rejected`, `blocked`, `unknown`. |
| Output | Admission status, reason codes, source context/version reference, condition refs, provenance, trace. |
| Forbidden | Context refresh, state change, Fact admission, model call. |

### 2.2 CognitiveAnalysisFrameV1

Required fields: `analysis_id`, `source_context_ref`, `analysis_subject_ref`,
`task_ref`, `goal_ref`, `analysis_scope`, `temporal_scope`,
`selected_evidence_refs`, `selected_relation_refs`, `known_constraints`,
`unknowns`, `admission_ref`, `provenance`, and `trace`.

The Frame marks one traceable read boundary. It is neither Working Memory nor a
Context duplicate, cannot hide its Context source, and cannot become a
long-term world-state store.

### 2.3 HypothesisCandidateV1

Required fields: `hypothesis_id`, `hypothesis_type`, `statement`,
`source_context_ref`, `source_evidence_refs`, `supporting_evidence_refs`,
`contradicting_evidence_refs`, `assumption_refs`, `uncertainty`,
`confidence_candidate`, `status`, `provenance`, and `trace`.

Planned `hypothesis_type` values: `state_interpretation`,
`relation_interpretation`, `change_explanation`, `intent_candidate`,
`risk_explanation`, `task_relevance`, `causal_candidate`, and `unknown`.

Planned status values: `proposed`, `supported`, `contradicted`,
`underdetermined`, `superseded`, `rejected`, and `unknown`.

A Hypothesis Candidate is not a Fact. High `confidence_candidate` never
promotes it automatically to Field State or Fact.

### 2.4 CompetingHypothesisSetV1

Required fields: `set_id`, `analysis_question`, `source_context_ref`,
`hypothesis_refs`, `compatibility_matrix`, `dominant_candidate_ref`,
`unresolved_reason_codes`, `evidence_coverage`, `status`, `provenance`, and
`trace`.

`dominant_candidate_ref` may be empty. The compatibility matrix distinguishes
mutual exclusion, partial overlap, and permitted coexistence. Planned statuses
are `unresolved`, `partially_resolved`, `provisionally_resolved`,
`contradicted`, and `unknown`; no status requires a unique explanation.

### 2.5 AnalysisEvidenceAssessmentV1

Required fields: `assessment_id`, `evidence_ref`, `hypothesis_ref`,
`relation`, `strength`, `reliability`, `temporal_relevance`,
`scope_relevance`, `contradiction_reason`, `uncertainty`, `provenance`, and
`trace`.

Planned `relation` values: `supports`, `contradicts`, `neutral`,
`insufficient`, `unavailable`, `revoked`, and `unknown`.

This object evaluates a relationship; it must not modify original Evidence,
Context Inclusion Records, or contradicted Evidence. Missing Evidence is not
automatically contradiction.

### 2.6 InformationGapRefinementV1

Required fields: `refinement_id`, `source_gap_ref`, `source_analysis_ref`,
`refined_question`, `required_information_type`, `target_field_refs`,
`target_relation_refs`, `priority_candidate`, `blocking_level`,
`recommended_observation_scope`, `resolution_criteria`, `provenance`, and
`trace`.

Planned refined gap categories are `known_missing`, `conflicting_information`,
`stale_information`, `revoked_evidence`, `insufficient_resolution`,
`temporal_unknown`, `relation_unknown`, `permission_restricted`, and
`unknown`. It may emit a Gap Refinement or Observation Request Candidate only;
neither executes observation.

### 2.7 CognitiveAnalysisSufficiencyResultV1

Required fields: a result reference, source Context/Frame references, status,
reason codes, evidence-coverage references, contradiction-level references,
critical-gap references, temporal-validity references, revoked-evidence
references, permission-restriction references, hypothesis-stability references,
trace-completeness reference, provenance, and trace.

Planned statuses: `sufficient`, `conditionally_sufficient`, `insufficient`,
`blocked`, and `unknown`. It measures analysis admission/output governance,
not factual correctness.

### 2.8 CognitiveAnalysisResultV1

Required fields: `analysis_result_id`, `source_context_ref`,
`analysis_frame_ref`, `hypothesis_candidate_refs`,
`competing_hypothesis_set_refs`, `evidence_assessment_refs`,
`information_gap_refinement_refs`, `sufficiency_ref`,
`provisional_interpretation`, `unresolved_questions`, `result_status`,
`provenance`, and `trace`.

Planned `result_status` values: `complete`, `provisional`, `incomplete`,
`blocked`, `stale`, and `unknown`. A Result is not Field State, Decision,
Action, Context writeback, Snapshot writeback, or Fact.

## 3. Reference and version rule

Every planned object must identify its source Context and source Context
version. The planned version references are `analysis_version`,
`source_context_ref`, `source_context_version`, `previous_analysis_ref`,
`supersedes_analysis_ref`, `hypothesis_version`, and
`evidence_assessment_version`.
