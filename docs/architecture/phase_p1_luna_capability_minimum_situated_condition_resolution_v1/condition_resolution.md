# Minimum condition resolution

`CapabilityPreconditionDefinitionV1` declares:

- `supported_condition_refs`;
- optional condition dimensions;
- abstract adjustment mappings.

`MinimumSituatedConditionRequirementV1` is the current-use result. It records
the Capability Requirement, Information Need, Goal, required and optional
condition references, source, provenance, and candidate-only status.

The resolver currently has two controlled OCR policies:

- `information:text-presence:v1` → `condition:target-visible:v1`;
- `information:primary-transit-sign-text:v1` → target visible, target complete,
  adequate target scale, and stable relation.

These are controlled, categorical policies. No numeric threshold is introduced.
Unknown Information Need policy fails closed rather than inheriting a stronger
or global default.

