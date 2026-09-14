# Verification

The verifier requires exactly the two positive cases, canonical controlled
replay cognition, final Sufficiency and Stop, correct Case B Gap →
Re-observation → Revision linkage, and one final Decision handoff per case.

It also reuses the canonical Decision validators for read-only input refs,
Decision candidates, trace completeness, candidate handoff validity, and no
runtime side effects. Decision provenance is trace-backed: final cognition
execution, Sufficiency, Stop, hypothesis, and evidence refs must be present in
the Decision Governance trace.

The negative fixture `premature_decision_handoff_before_sufficiency` must be
rejected without invoking Decision Governance.

