# Baseline Readiness

`EvaluationRunCandidateV1` reserves `comparison_eligibility` and preserves Dataset/Sample/Case and Luna code/config version refs. This makes future same-case comparison structurally possible without calculating a global cognitive score.

Current synthetic fixture status is `planned` for comparison because it has no observed Luna code/config versions and no real cognition. A full baseline/comparison engine is deferred. Required future comparison identity is:

`same Cognitive Test Case + same Dataset/Sample version + comparable conditions + different Luna code/config version`.

Comparison must retain process deltas, failure attribution deltas, unavailable/incomparable states, and trace/profile refs. A benchmark winner must not become a runtime model choice.

