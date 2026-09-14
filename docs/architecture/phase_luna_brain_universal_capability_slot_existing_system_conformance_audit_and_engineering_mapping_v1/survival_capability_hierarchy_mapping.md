# Survival Capability Hierarchy Mapping

## Existing vocabulary

The general Capability Governance contract uses Candidate, Registered,
Testing, Active, Degraded, Suspended, and Retired. The visual reference uses
`mandatory_or_optional` and a `MANDATORY` lifecycle value. These structures
do not yet provide a universal three-level requirement hierarchy.

## Recommended semantic hierarchy

| Standard class | Existing conformance | Future meaning |
|---|---|---|
| `SURVIVAL_BASELINE` | EXTENSION_REQUIRED | Constitutional minimum that cannot be removed below baseline by Brain or user. |
| `SYSTEM_REQUIRED` | EXISTING_PARTIAL | Required for normal system integrity but conceptually distinct from survival minimum. |
| `OPTIONAL` | EXISTING_PARTIAL | May be suspended, released, or implementation-uninstalled when governance permits. |

Do not rename existing enums automatically. A future Module requirement class
may add these semantics while retaining a backward-compatible mapping from
legacy `MANDATORY` declarations.

## Safety rule

`SURVIVAL_BASELINE` is a Module governance classification, never a Slot type.
Safety Constitution and Survival Governance retain final authority. A safety
Module may degrade or enter recovery governance, but the system must not
silently fall below the minimum configuration.
