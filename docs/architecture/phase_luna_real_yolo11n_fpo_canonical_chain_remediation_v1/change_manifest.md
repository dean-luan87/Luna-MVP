# Change Manifest

## Added

- FPO canonical binding compatibility seam.
- Fail-closed upstream context builder requiring governed records.
- Static real-caller wiring inspection.
- Remediation documentation package.

## Modified

- FPO Provider admission input gained reference-only canonical binding,
  Runtime Admission, invalidation, and validation fields.
- YOLO11n single-frame real entrypoint consumes the compatibility seam.
- A-Route S3 real-case path constructs context from explicit upstream records
  and consumes the same seam.
- Context builder rejects missing upstream records; it does not manufacture
  binding or admission success.
- Shared FPO Provider adapter fail-closes real invocation without validated
  canonical references.

## Not changed

- canonical owners;
- canonical enums;
- canonical binding lifecycle implementations;
- Model/Provider loading implementation;
- Field/Current World/Brain state;
- Runtime execution semantics outside the guard.
