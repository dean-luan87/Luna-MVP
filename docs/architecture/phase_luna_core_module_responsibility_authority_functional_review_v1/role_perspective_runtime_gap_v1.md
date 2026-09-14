# Role / Perspective Runtime Gap v1

## Existing evidence

The repository contains:

- Working Envelope `role_refs` and `perspective_refs`;
- field-centric object-role inference that returns `candidate_only` and
  `not_fact` candidates;
- Self Reference candidates with `fact_admitted=False`, `persisted=False`,
  and no source mutation;
- Decision inputs that consume `role_refs` and expose role constraints;
- module contracts and adjudication docs naming a Role/Perspective owner,
  without a unified implementation.

## Gaps

| Gap | Classification |
|---|---|
| source-specific authoritative Role owner contract | OWNER_GAP / CONTRACT_GAP |
| unified Role version/invalidation propagation | ADAPTER_GAP |
| Perspective projection/adoption contract | CONTRACT_GAP |
| Role/Perspective runtime lifecycle | RUNTIME_GAP |
| field-centric object role versus social Role naming | TERMINOLOGY_GAP / LEGACY_OVERLAP |
| new Manager | NOT JUSTIFIED |

The owner gap is resolved architecturally by reassignment to existing source
owners plus a shared contract. No runtime owner is created in this phase.
