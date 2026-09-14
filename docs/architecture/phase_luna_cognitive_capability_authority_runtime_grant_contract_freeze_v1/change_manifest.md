# Change Manifest

## Phase

Phase-Luna-Cognitive-Capability-Authority-Runtime-Grant-Contract-Freeze-v1-001

## Files created

- phase_contract.md
- capability_authority_grant_model_v1.md
- cognitive_authority_grant_schema_v1.json
- authority_responsibility_binding_v1.md
- ab_delegated_authority_contract_v1.md
- loop_capability_boundary_v1.md
- change_manifest.md

## Files modified

None outside this new contract-freeze directory.

## Canonical impact

- canonical types changed: no;
- canonical enums changed: no;
- canonical owners changed: no;
- runtime behavior changed: no;
- verified Loop engines changed: no;
- Brain runtime implemented: no;
- Permission Manager created: no;
- Authority Manager created: no;
- Provider/model/OCR/camera invoked: no.

## Frozen contract decisions

- Capability Boundary is structural and immutable for the grant context;
- Authority Contract maps eligible role classes to semantic authority;
- Runtime Authority Grant is scoped, revocable and expiring;
- Brain normally issues the A grant;
- B receives only a derived bounded grant from Brain-governed A authority and
  an A B request;
- Loop may receive mechanical grants only;
- responsibility, result receiver, error owner, expiry and revocation authority
  are mandatory accountability metadata;
- no grant can exceed Capability Boundary.

## Relation to previous phase

The previous authority freeze remains valid. This phase adds the distinction
between canonical authority ownership, role eligibility and concrete runtime
permission. It does not replace Brain/A/B/Loop semantic ownership.

## Verification ownership

No Runner, Verifier or runtime validation command was executed. Architecture
review and future terminal verification remain user-owned.

## Status

Contract freeze documents created. Do not claim GO or PASS.
