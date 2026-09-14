# Logical Resolution → Runtime Admission Flow

The trial now forms the existing logical Capability Requirement/Resolution
candidate before constructing the Runtime Admission input. The compatibility
helper consumes the supplied model admission and model contract candidates;
it does not probe or recompute them.

The Provider path is reachable only when:

```text
logical_resolution.status == READY_CANDIDATE
and runtime_admission.status == READY_FOR_EXECUTABLE_CANDIDATE
and executable_candidate exists
```

Otherwise the existing Provider adapter receives a non-authorized admission
candidate and returns structured blocked diagnostics with invocation count 0.

