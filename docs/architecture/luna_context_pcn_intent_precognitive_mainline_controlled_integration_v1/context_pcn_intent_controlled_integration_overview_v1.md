# Context-PCN-Intent Pre-Cognitive Mainline Controlled Integration v1

## Phase
- Phase: Phase-Luna-Context-PCN-Intent-PreCognitive-Mainline-Controlled-Integration-v1-001
- Scope: Context Foundation -> PCN -> Intent Governance (synthetic only)
- Integration role: mapping, compatibility, trace/provenance linking, idempotency, boundary validation

## Non-goals
- No new cognitive owner
- No Context/PCN/Intent owner rewrite
- No runtime execution
- No source state mutation

## Reuse Source Of Truth
- Context->PCN handoff contract: docs/architecture/luna_context_foundation_module_closure_v1/context_to_pcn_handoff_contract_candidate.json
- PCN->Intent handoff contract: docs/architecture/luna_personal_cognitive_network_module_closure_v1/pcn_to_intent_handoff_contract_candidate_v1.json

## Mainline
- Context synthetic input -> Context envelope candidate
- Context->PCN handoff mapping + compatibility gate
- PCN processing -> projection candidate
- PCN->Intent handoff mapping + compatibility gate
- Intent Governance run_case -> Intent candidate

## Authority
- Context Foundation owns Context candidate
- Personal Cognitive Network Governance owns PCN candidate
- Intent Governance owns Intent candidate
- Integration owns no cognitive state and no mutation authority
