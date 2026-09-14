# Executable Capability Candidate Boundary

An `ExecutableCapabilityCandidateV1` is produced only when the assessment
status is `READY_FOR_EXECUTABLE_CANDIDATE` and all required admitted refs are
present.

It retains the admission ref, logical refs, admitted model/provider refs,
source/state refs, permission/resource/safety refs, expiry/staleness refs and
trace/provenance.

It remains `candidate_only=True` and
`provider_invocation_executed=False`. It is not a Provider authorization and
does not load a model.

