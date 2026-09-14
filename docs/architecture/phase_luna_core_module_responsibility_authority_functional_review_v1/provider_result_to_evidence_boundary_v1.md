# Provider Result → Evidence Boundary v1

Evidence mapping should normalize Provider Result, attach request/provider/
source refs, preserve confidence/uncertainty, validate expected evidence type,
attach timestamps and provenance, and mark candidate/non-truth status.

This responsibility belongs to Observation/FPO plus domain-specific evidence
adapters or Gateway, not Provider. Provider only reports runtime output.
