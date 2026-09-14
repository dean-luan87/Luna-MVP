# Safety / Action / Provider Boundary v1

Action Admission is a hard external-side-effect enforcement point. Provider
Admission may refuse, cancel, terminate, or report an unsafe runtime condition
under supplied policy.

Neither Action nor Provider defines semantic Safety Policy. Stale policy,
changed target, new risk, or revoked authorization requires recheck/block;
semantic consequence returns to A/Decision/Brain.
