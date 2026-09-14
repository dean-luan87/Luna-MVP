# Provider binding relationship

The grant consumes Provider Binding Candidate, Runtime Allocation Preparation
Candidate, and Execution Instance Preparation Candidate. It does not perform
provider matching, provider ranking, binding, model selection, or fallback.

Provider Governance remains the owner of provider eligibility and binding
responsibility. The controlled input status `provider_binding_status=ELIGIBLE`
means the referenced candidate is acceptable to the grant boundary; it does
not set `provider_bound=true`. A provider-denied input produces a denied grant
with Provider Governance as failure owner.

`source_model_ref` remains optional. An explicit model reference may be carried
through the immutable lineage, but no model is inferred or selected when it is
absent.
