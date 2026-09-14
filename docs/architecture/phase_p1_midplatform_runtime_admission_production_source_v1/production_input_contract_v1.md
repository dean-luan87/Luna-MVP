# Production input contract

`RuntimeAdmissionProductionInputV1` requires supplied records and refs for:

- Capability Resolution;
- Capability↔Model binding;
- Model↔Provider binding;
- model/weights/loader/dependency declarations;
- Grant, Permission, Safety, Resource and Working Envelope refs;
- source versions, trace and provenance;
- repository declaration source files.

The integration source assembles these references. It does not issue source
identity, binding lifecycle, policy, Grant, or Provider authority.

The first no-runtime validation profile is explicitly named
`REPOSITORY_BACKED_DECLARATION_VALIDATION_NO_RUNTIME`. Its integrity and
readiness values are declaration-validation evidence only; no checksum,
dependency, device, or Provider probe is performed.
