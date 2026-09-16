# Luna Contract Integrity Protocol v1

Status: normative cross-module engineering protocol.

This protocol governs structural contract handling at owner boundaries. It
does not create a runtime service or an authority layer:

- `PROTOCOL != RUNTIME MODULE`
- `PROTOCOL != VALIDATOR SERVICE`
- `PROTOCOL != AUTHORITY OWNER`

The contract chain is:

`Shape Truth → Semantic Meaning → Governed Authority`

Each layer has a separate responsibility. Structural validity does not imply
semantic validity, epistemic status, admission, authorization, or execution.

## P1. Invalid input is not semantic information

`INVALID_INPUT != UNKNOWN != UNRESOLVED != ABSENT != OPTIONAL_EMPTY != NOT_OBSERVED`.

Structural errors must be rejected as contract failures. They must not be
interpreted as world state or cognitive state.

## P2. Validate before semantic processing

The required boundary is:

`Raw / External / Reconstructed Input → Structural Validation → Typed Contract → Semantic Processing`.

Only structurally valid input may enter semantic processing.

## P3. Validate once, reference many times

The canonical contract validation owner performs the first authoritative
structural validation. A successful validation produces a typed contract.
Downstream consumers may defensively reject a local use, but may not upgrade
invalid input into a valid canonical contract.

## P4. Normalization is not repair

Normalization is permitted only when it preserves contract meaning, such as
trimming whitespace when the contract explicitly defines that rule. These
repairs are prohibited unless a contract explicitly defines tolerant
semantics:

- `7 → "7"`
- `INVALID_MAPPING → {}`
- `["valid", 7] → ["valid"]`

## P5. Invalid member invalidates the contract

For `Sequence[str]`, `["a", "b"]` is valid and `["a", 7]` is invalid.
Required typed collections must reject an invalid member as a whole. They
must not filter the member and continue.

## P6. Wrong type is not absence

`None` or an empty collection expresses optional absence only where the
contract explicitly permits it. A wrong scalar, string, mapping, or other
object type must not be defaulted to `None`, `{}`, `()`, or another valid
absence.

## P7. Adapter may map, not invent

An adapter may map fields, perform lossless representation conversion,
preserve provenance, and reject malformed adapter input. It may not invent
required information, filter malformed required information, convert invalid
input into epistemic `UNKNOWN`, manufacture provenance, admission, or
authority. Adapter rejection is not adapter semantic authority.

## P8. Deserialization does not restore validity

JSON, replay, cache, stored DTO, and IPC data must re-enter the relevant
structural validation boundary before canonical processing. Matching field
names do not prove that a reconstructed value satisfies the contract.

## P9. Structural validity does not imply admission

`Shape valid != semantic admission != truth != authorization != execution eligibility`.
Validation makes an input eligible for the next owner boundary; it does not
perform that boundary's semantic decision.

## P10. Validation does not create authority

A validator answers only whether an input satisfies its structural contract.
It cannot establish evidence truth, event admission, action approval,
runtime authorization, or an execution fact.

## P11. Preserve failure origin

Each local rejection representation must preserve the distinction between
malformed structure and semantic/epistemic absence. It should be able to
distinguish, where relevant:

- `INVALID_STRUCTURE`
- `MISSING_REQUIRED_FIELD`
- `INVALID_FIELD_TYPE`
- `INVALID_MEMBER_TYPE`
- `INVALID_NESTED_SHAPE`

Modules may use local exceptions, rejection results, status values, or
structured reasons. One repository-global enum is not required.

## P12. No validation-proof flags

Do not introduce `validated=True`, `is_valid=True`, `validation_token`, or
`validation_ref` as the canonical validity authority. Validity comes from
the owner boundary's validation and the controlled typed-contract lifecycle.

## P13. Fail closed at authority-relevant boundaries

If malformed structure could affect admission, canonical state, decision,
authorization, execution, or mutation, processing must stop when structure
cannot be proved valid. The boundary must not guess.

## P14. Defensive check is not a second final authority

A consumer may reject local processing or detect corruption. It may not
upgrade input that did not pass the canonical validation boundary, and its
defensive rejection does not make it the canonical semantic or authority
owner.

## P15. Contract changes require caller review

When a contract changes, review its producer, adapter, admission boundary,
consumer, replay/serialization path, verifier, and tests. Compatibility seams
must not silently repair old or malformed shapes.

## Reusable strictness rules

1. Collection contracts reject `str`, `bytes`, `bytearray`, scalars, and
   mappings unless mappings are explicitly allowed. Every member must satisfy
   the declared shape.
2. Required identifiers require their declared scalar type and non-empty
   semantics. Arbitrary values must not be repaired with `str(value)`.
3. Required mappings validate the mapping type, required keys, and defined
   nested members. Explicitly opaque payload mappings remain open-ended.
4. Optional absence is accepted only where declared. Wrong type is never
   absence.
5. `UNKNOWN`, `UNRESOLVED`, and `ABSENT` are formed only after structural
   validation succeeds.
6. Adapter normalization is lossless relative to the declared contract.
7. Downstream code may use defensive assertions without duplicating
   authoritative validation or changing semantic ownership.

## Validator contract fidelity

Validation targets MUST be derived from the canonical contract definition.
Validators MUST NOT invent required fields or treat an undeclared field as a
member of the accepted contract. The absence of an undeclared field is not an
`INVALID_INPUT` condition for that contract. Compatibility fields may be
validated only when they are actually part of the accepted contract. A
validator/contract mismatch must be corrected at the validator or contract
owner boundary; it must not be silently repaired with defaulting, `getattr`,
or conditional field omission.

## Ownership boundary

The contract definition owner defines the shape. The contract validation
owner rejects raw or reconstructed values at the first trusted boundary. The
formation owner creates candidates or records from the typed contract. The
semantic admission owner decides meaning or admission. The mutation owner
changes canonical state. Consumers may defensively reject local processing.

Structural validation does not transfer any of the latter authorities.

F-05 Gateway admission remains the source of governed evidence-admission
authority. F-07 Permission / Admission Manager authorization state remains
the source of runtime authorization. F-08 contract validation may reject
their malformed inputs but cannot manufacture either authority.
