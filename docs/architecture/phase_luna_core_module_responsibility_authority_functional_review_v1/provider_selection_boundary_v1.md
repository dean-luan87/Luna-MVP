# Provider Selection Boundary v1

Capability Governance selects logical Capability. Model Manager owns model
asset/mapping metadata. Runtime Admission produces an Executable Capability
Candidate. Provider Governance admits and, where multiple compatible Providers
are already supplied by mapping/policy, selects or confirms the concrete
Provider for execution.

This is not a new Provider Selector Manager. Provider Governance cannot select
a Provider that violates Brain policy, Runtime Admission, Model mapping or
resource/safety constraints.
