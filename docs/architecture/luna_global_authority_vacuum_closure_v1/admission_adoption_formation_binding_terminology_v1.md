# Admission, Adoption, Formation and Binding Terminology v1

| Term | Meaning | Authority implication |
|---|---|---|
| Formation | constructs a candidate or local-derived representation | producer owns construction correctness, not final use or source mutation |
| Validation | checks structure, version, provenance and declared compatibility | validator supplies evidence; it does not become lifecycle owner |
| Binding | connects separately owned states/contracts with refs and versions | one named binding lifecycle owner is required for a shared binding |
| Admission | authorizes a candidate/state transition into a governed state | named governance authority owns the transition and failure responsibility |
| Adoption | downstream reasoning/governance consumer chooses to use a valid candidate | consumer owns semantic/use consequence; it need not mutate the candidate |

## Application to the seven gaps

- Current World: formation plus validation; A adoption; no separate admission authority.
- Cognitive Snapshot: formation/alignment plus validation; A adoption; no separate admission authority.
- Semantic Outline: Semantic-owned local-derived lifecycle; A adoption.
- Capability↔Model: shared binding; Capability Governance owns binding lifecycle.
- Model↔Provider: shared binding; Provider Governance owns provider-facing binding lifecycle.
- Cross-constraint precedence: Brain owns the admission ordering contract; consumers enforce.
- Working Envelope: binding admission and refresh are Envelope governance responsibilities.

Terminology must not make a consumer’s “use” look like source mutation or make a candidate producer look like a governance authority.

