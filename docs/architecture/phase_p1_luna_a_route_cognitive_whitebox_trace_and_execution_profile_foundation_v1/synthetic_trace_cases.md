# Synthetic Trace Cases

The Runner creates six candidate-only cases without model/provider data:

1. `obvious_target_single_cycle` — one cycle, sufficient candidate evidence,
   stop, Decision Governance handoff only.
2. `missing_information_requires_reobservation` — missing evidence,
   insufficient Sufficiency, Information Gap, targeted Re-observation.
3. `hypothesis_revision` — later evidence and explicit revision parent ref.
4. `conflicting_evidence` — conflict preserved and Sufficiency contested.
5. `premature_sufficiency_guard` — missing required evidence prevents
   `SUFFICIENT`.
6. `decision_governance_handoff` — sufficient cognition hands off without a
   Decision node.

Fixtures contain refs and bounded summaries only. They do not contain raw
Provider payloads, model output, semantic answer fixtures, World Truth, or
runtime state.
