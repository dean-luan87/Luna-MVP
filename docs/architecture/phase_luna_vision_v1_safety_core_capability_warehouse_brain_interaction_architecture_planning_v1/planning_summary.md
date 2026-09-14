# Planning summary

The selected architecture reuses Model Manager for model/provider identity
and admission, Capability Governance for capability registration and
lifecycle, Observation Gateway for evidence ingress, FPO/Active Observation
Control for task observation, System Maintenance for diagnostics/rollback,
and Brain Golden Baseline boundaries for candidate/truth continuity.

Safety Vision is mandatory but capability-identity agnostic. The Warehouse is
dynamic but cannot weaken mandatory safety slots. Safety and task observation
are distinct channels. SNSP is a standardized semantic prior, followed by
Field Rule reconciliation; it is not effective-rule or action authority.

Evidence Sufficiency remains owned by FPO/Active Observation Control. Semantic
Sufficiency and Minimum Sufficient Task Semantics move to future cross-modal
SRSK. Unknown/Partial-Known remains valid, and Learning Need requires SRSK gap
evaluation plus Brain task-blocking evaluation. No runtime implementation is
included.
