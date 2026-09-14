# Scenario mapping

The controlled suite contains 35 cases across OCR, object detection, spatial
mapping, unsupported scope, authority/contract rejection, readiness, Self
scope visibility, Gap Candidate, and Gateway/FPO invocation boundaries.

All cases are candidate-only. No case invokes a Provider or Model.

`scope_fixture_contract_reconciliation_v1.json` records the exact requirement
and Module contract shape for CSR-01..CSR-35, including the shared
`text_recognition` dependency used by readiness cases CSR-02 and CSR-20,
CSR-22..CSR-26.
