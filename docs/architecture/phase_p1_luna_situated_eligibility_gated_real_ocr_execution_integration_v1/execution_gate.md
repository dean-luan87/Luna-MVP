# Execution Gate

`SituatedCapabilityExecutionAdmissionV1` is a narrow bridge contract.  Its
`provider_execution_admitted` value is derived from
`eligibility.eligible_now`; it is not a second Provider Runtime admission
owner.

The orchestration order is fail-closed:

1. derive Situated Condition Candidates;
2. evaluate existing Necessity, Feasibility, Opportunity, and Eligibility;
3. materialize the execution admission;
4. return without calling OCR when admission is false;
5. call `RealOCRProviderExecutionEngineV1.run(...)` only when admission is
   true.

Existing Provider Runtime governance remains required after the situated gate.
`eligible_now=true` means permitted to attempt the existing runtime; it does
not itself prove provider or model execution.
