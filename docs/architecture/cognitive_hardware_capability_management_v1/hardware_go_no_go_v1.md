# Hardware Capability Management Go / No-Go v1

## Required readiness checks

- Hardware Registry Extension records Identity, Specification, Capability
  Profile, Resource Profile, Health State, Calibration State, and Limitation.
- Hardware Capability is distinct from Hardware State and Self Identity.
- Hardware Capability Profile describes Capability Contribution, output Evidence
  boundary, resource needs, confidence boundary, and limitations.
- Hardware State includes Available, Degraded, Limited, Failed, and Unknown.
- Hardware Diagnostics maps Hardware Issue → Hardware State Candidate → Self
  Capability Update Candidate.
- Hardware Adaptation produces candidates for Attention, Runtime, and Model
  Requirement; Hardware Manager does not decide or execute.
- Attention receives Capability Confidence and Observation Cost candidates.
- Runtime owns execution mechanics; Hardware Manager owns body state.
- Hardware Resource Profile informs Model Requirement and Model Admission;
  Model Manager manages implementation assets.
- Hardware replacement changes the Registry/Capability reference, not Identity.

## Explicit prohibitions

No hardware control, No driver development, No Camera connection, No sensor
connection, No Model Runtime, No Provider Runtime, No Action Runtime, No
Emotion, No Role, No Social Runtime, No automatic adaptation, No direct Reality
mutation, No direct Goal mutation, and No direct Decision mutation.

The Agent performs V0 static checks only, does not run the Final Phase
Verifier, and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.

Self Capability Update Candidate is required. No sensor connection, No Emotion,
and No direct Reality mutation are permitted.
