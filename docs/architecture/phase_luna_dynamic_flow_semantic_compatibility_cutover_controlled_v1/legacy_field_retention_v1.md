# Legacy field retention

The following Dynamic Flow fields remain intentionally available:

- `current_minimum_need_ref`;
- `sufficiency_candidates`;
- `reconsiderations`;
- `final_disposition`;
- `next_step_disposition`;
- state-version lineage;
- stale requirement and non-materialized plan references;
- trace/provenance references.

They are computational/compatibility outputs. They are not removed while legacy fixtures, verifiers, and historical integrations consume them.
