# Cognitive Analysis Lifecycle and Failure Semantics v1

## 1. Lifecycle and version preservation

Each A3 result is immutable with respect to its source Context version. A
subsequent Context, Evidence, or assessment update creates a new analysis
object linked through `previous_analysis_ref` and `supersedes_analysis_ref`;
it does not overwrite or delete the earlier analysis.

```text
Context admitted
  -> Frame created
  -> hypotheses / assessments / gaps created
  -> sufficiency evaluated
  -> Result emitted
  -> stale | refresh_required | superseded | archived reference state
```

Required version relationship fields are `analysis_version`,
`source_context_ref`, `source_context_version`, `previous_analysis_ref`,
`supersedes_analysis_ref`, `hypothesis_version`, and
`evidence_assessment_version`.

## 2. Stale, refresh, supersede, and revoked Evidence

| Condition | Required planned handling | Prohibited handling |
| --- | --- | --- |
| Context updated | Preserve earlier analysis; create a new analysis against the new Context version or mark the earlier result `stale` / `refresh_required`. | Silent replacement of old analysis. |
| Context stale | Lower Admission or block a current conclusion. | Treating it as current without disclosure. |
| Context refresh required | Emit a condition, gap refinement, or blocked/provisional result. | Refreshing Context inside A3. |
| Evidence revoked | Reassess linked Hypotheses and Results; mark affected result stale or refresh-required. | Delete historical analysis/evidence references. |
| Contradictory evidence | Retain competing candidates and contradiction assessments. | Delete the contradicted evidence or force one hypothesis. |

## 3. Failure codes and required semantics

| Failure code | Meaning | Required result posture |
| --- | --- | --- |
| `context_missing` | No direct Context input is available. | `rejected` or `blocked`; no Frame. |
| `context_stale` | Context cannot be treated as current. | conditional/blocking admission; no silent current claim. |
| `context_refresh_required` | Context declares refresh required. | condition or block; emit refresh-related gap if material. |
| `context_insufficient` | A2 sufficiency does not permit conclusion. | blocked/insufficient; no valid analysis conclusion. |
| `context_permission_restricted` | A3 cannot read required Context material. | blocked; preserve restriction. |
| `source_snapshot_unavailable` | Snapshot reference is not traceable through Context. | rejected/blocked; no synthetic replacement. |
| `evidence_missing` | Declared evidence is unavailable. | gap/insufficient; never contradiction by absence. |
| `evidence_revoked` | Evidence is no longer usable for current assessment. | reassess; stale/refresh-required result. |
| `evidence_conflict` | Evidence supports incompatible interpretations. | competing set or underdetermined status. |
| `temporal_validity_unknown` | Relevant timing cannot be established. | conditional/unknown, preserving uncertainty. |
| `hypothesis_underdetermined` | Evidence does not discriminate alternatives. | preserve multiple hypotheses. |
| `competing_hypotheses_unresolved` | No justified dominant candidate exists. | unresolved set; dominant ref may be empty. |
| `critical_information_gap` | Material missing information blocks analysis. | blocked or insufficient; optional refinement only. |
| `analysis_blocked` | A governance condition prevents analysis. | no Result claiming completion. |
| `analysis_stale` | Result refers to obsolete Context/Evidence conditions. | retain with stale status; do not overwrite. |
| `provenance_incomplete` | Required lineage is absent. | reject/block. |
| `trace_incomplete` | Required trace is absent. | reject/block. |
| `unknown` | Status cannot be safely determined. | preserve `unknown`; do not coerce to false. |

## 4. Negative semantics

A3 must not silently complete missing information, force a unique Hypothesis,
turn `unknown` into `false`, turn no evidence into a low-confidence fact, or
substitute model output for governed Context. The only allowed response to a
material unknown is explicit uncertainty, an Information Gap Refinement, or an
Observation Request Candidate without execution.
