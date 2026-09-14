# Protocol Governance Standard Index V1

## Scope

Canonical governance for Luna protocols: add, update, deprecate, validate, reference.

## Required Fields Per Protocol

- `protocol_id`
- `canonical_path`
- `version`
- `owner`
- `validation_plan`
- `reference_policy`

## Lifecycle

1. **Add** — standardization phase + usage note + test board  
2. **Update** — standard patch phase; bump version  
3. **Deprecate** — manifest status + successor ref  
4. **Validate** — canonical validation once; drift checks thereafter  
5. **Reference** — cite id/path; no scatter in business code

## Forbidden

- Protocol definitions only in runtime/business modules  
- Silent protocol changes without patch phase  
- Missing owner or validation record

## Usage Note

Any new protocol must register in governance_standards before production reference.
