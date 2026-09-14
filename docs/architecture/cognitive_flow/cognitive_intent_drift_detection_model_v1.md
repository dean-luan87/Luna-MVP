# Cognitive Intent Drift Detection Model v1

## Drift classes

| Drift class | Definition | Example | Candidate response |
|---|---|---|---|
| Expansion drift | interpretation exceeds the bounded purpose without justified coverage value | safe-passage need becomes city-wide scan | resource/coverage warning candidate |
| Narrowing drift | interpretation removes a non-negotiable information need | safe passage becomes vehicle-only detection | missing-evidence candidate |
| Substitution drift | proxy, model metric, or local output replaces the cognitive purpose | OCR count replaces pharmacy-finding purpose | intent-alignment warning candidate |
| Transfer drift | work shifts from the subject need to an unrelated technical objective | user crossing support becomes model-accuracy optimization | purpose-mismatch candidate |
| Evidence drift | returned data does not support the stated evidence need | many advertisements returned for pharmacy location need | insufficient-support candidate |

## Detection inputs

`intent_contract_ref`, `interpretation_ref`, `requirement_ref`,
`capability_request_ref`, `evidence_ref`, `coverage_candidate`,
`unknown_candidate`, and `trace_ref`.

Drift Detection emits only Intent Drift Candidate information. It does not reject a request, rewrite a Goal, select a Provider, create a Decision/Action, or mutate State.
