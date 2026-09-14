# Causal Governance Controlled Implementation Overview v1

Status: CONTROLLED_IMPLEMENTATION_CANDIDATE

Phase: Phase-Luna-Causal-Governance-Controlled-Implementation-v1-001

Execution boundary:
- candidate_only = true
- synthetic_fixture_only = true
- deterministic_logic_on_synthetic_fixtures = true
- runtime_executed = false
- source_mutation_executed = false
- no Decision/Action/Task output

Canonical owner:
- Causal Governance (unique mutation authority)
- Legacy alias Causal Reasoning Governance is reference-only and non-authoritative

Implemented pipeline:
input refs/evidence
-> hypothesis formation
-> support/opposition/conflict
-> state transition
-> uncertainty
-> provenance trace
-> candidate-only causal-to-decision handoff

Out of scope:
- real runtime event stream
- model invocation
- causal discovery engine against real data
- database write
- field/memory mutation
- final decision/action/task
