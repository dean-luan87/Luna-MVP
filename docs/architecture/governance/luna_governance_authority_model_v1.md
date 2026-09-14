# Luna Governance Authority Model v1

## Authority Order

```text
L0 Constitution Authority
        ↓
L1 Protocol Governance Authority
        ↓
L1 Permission / Admission Authority
        ↓
Governed Capability Authority

L1 Capability Registry Authority and L1 Diagnostics Authority
support the chain; neither may override the order above.
```

The decisive precedence rule is: **Constitution > Protocol > Permission/Admission > Capability**.

## L0 Constitution Authority

- **owns:** non-negotiable cognitive, mutation, candidate/Fact, and external-model boundaries.
- **allows:** only designs and contracts consistent with constitutional principles.
- **denies:** Evidence/Model output becoming Fact by default; any bypass of Reducer mutation authority; candidate-to-Decision/Action/State/Memory shortcuts.
- **cannot_override:** a specific Fact admission, permission request, Registry lifecycle record, or Capability transformation; it defines their maximum authority, not their individual outcomes.

## L1 Protocol Governance Authority

- **owns:** Contract identity/version, input/output symmetry, traceability, allowed object categories, Negative Guard inventory, and boundary-compatible serialization.
- **allows:** a Capability route whose declared input/output Contract remains constitutionally valid.
- **denies:** protocol drift, missing trace/provenance, incompatible schemas, undeclared output categories, and a parallel Capability-owned protocol.
- **cannot_override:** L0 principles, a denied Permission/Admission decision, Registry ownership, or domain semantics.

## L1 Permission / Admission Authority

- **owns:** request eligibility, permission scope references, input admission eligibility, and future output handoff eligibility.
- **allows:** a request only within an existing governed scope after Protocol conditions are met.
- **denies:** self-granted access, consumer overreach, ungoverned input, premature Fact/Decision/Action handoff, and unauthorized write behavior.
- **cannot_override:** L0/L1 Protocol constraints, Registry lifecycle rules, or Reducer State authority.

## L1 Capability Registry Authority

- **owns:** Capability identity, owner, lifecycle, manifest/record reference, declared dependencies, and lifecycle state.
- **allows:** discoverability and lifecycle eligibility only through the existing Registry route.
- **denies:** duplicate identity, self-registration, self-promotion, undeclared owner/dependencies, and lifecycle bypass.
- **cannot_override:** Constitution, Protocol compatibility, Permission/Admission, or the domain authority of a registered Capability.

## L1 Diagnostics Authority

- **owns:** reporting of Contract drift, validation evidence, permission/admission status, boundary violations, and lifecycle signals.
- **allows:** observable governance evidence for review and remediation.
- **denies:** silent boundary failure and hidden validation drift through required reporting.
- **cannot_override:** any authorization, protocol decision, Registry lifecycle, Capability behavior, or constitutional rule.

