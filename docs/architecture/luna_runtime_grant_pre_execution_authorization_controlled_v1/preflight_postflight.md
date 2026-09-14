# Preflight and postflight

The evaluation follows:

`Governance Profile → applicable-rule resolution → preflight → grant
formation → postflight → unified final decision`.

Preflight blocks malformed profiles, unresolved rules, unresolved protocol
refs, and authority/responsibility inconsistencies before business formation.
Postflight checks that grant formation did not allocate resources, create an
execution instance, start a provider session, submit Gateway work, invoke a
provider/model, or declare truth. It also checks requester/executor and
failure-ownership boundary payloads.

The phase profile is authoritative only for the permission decision; it is
`runtime_level=NONE`, has no runtime or truth authority, and remains
non-mutating.
