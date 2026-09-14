# Field Event Model Definition v1

| Field | Meaning | Boundary |
| --- | --- | --- |
| `event_id` | Stable governance-supplied candidate identity | No automatic identity or fact lifecycle |
| `event_type` | One planned candidate type | Not an admitted/reduced event type |
| `source_field_view_ref` | Current Field View scope | View is not Event authority |
| `before_reference`, `after_reference` | Candidate/reference comparison points | Not State values or mutation commands |
| `change_pattern` | Possible observed change description | Not causal explanation or final conclusion |
| `temporal_scope` | Event/observation/context time references plus uncertainty | No State Valid Time rewrite |
| `confidence`, `uncertainty` | Candidate metadata and limitations | No admission/Fact authority |
| `provenance`, `trace_ref` | Full source and derivation lineage | Mandatory, append-only |
| `candidate_status` | `candidate`, `incomplete`, `conflicting`, or `stale` | Never `fact`, `admitted`, or `reduced_state` |

The object fixes `candidate_only=true`, `not_fact=true`, and `not_state=true`. It has no State update, History write, Temporal rewrite, Decision, Action, or Memory target.
