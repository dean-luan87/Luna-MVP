# Authority Grant Runtime Boundary

## Three layers

1. Capability Boundary: immutable structural role/module capability.
2. Authority Contract: role eligibility for semantic authority.
3. Runtime Authority Grant: scoped permission for one Concern, Work and state
   version.

## Grant checks

Candidate validation checks:

- receiver role eligibility;
- authority subset of Capability Boundary;
- Concern and Work scope;
- source state version;
- Safety/Permission/Resource refs;
- responsibility binding;
- revocation and expiry.

The grant cannot expand a forbidden Capability Boundary.

## Brain/A/B

Brain normally issues A grants. B grants are derived from the A grant plus an
A B-request. B cannot self-delegate or recursively request B.

## Failure distinction

Capability Boundary violation is distinct from:

- authority not granted;
- scope mismatch;
- stale state;
- revoked grant;
- expired grant;
- invalid responsibility binding.
