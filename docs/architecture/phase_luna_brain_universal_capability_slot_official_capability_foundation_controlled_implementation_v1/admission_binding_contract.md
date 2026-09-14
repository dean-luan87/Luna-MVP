# Admission and Binding Contract

The controlled flow is staged:

1. Module Definition Admission
2. Implementation Admission reference
3. Model/Provider Admission reference
4. Slot Compatibility Assessment
5. Module-to-Slot Binding Candidate
6. Governed Binding Result

The implementation explicitly distinguishes:

`AVAILABLE != ADMITTED != BOUND != INSTALLED != ACTIVE`

No installation or activation is executed. A binding result is a candidate
projection with `state_mutation_executed = false`.

Mandatory Safety admission additionally requires constitutional baseline,
approved provider, compatibility, integrity/provenance, resource, permission,
degradation, and rollback references.
