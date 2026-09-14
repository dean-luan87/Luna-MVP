# Hardware Capability Management Whitebox v1

## Body/self-awareness trace

```text
Hardware Registry Entry
        ↓
Hardware Capability Profile
        ↓
Resource / Health / Calibration / Limitation
        ↓
Diagnostics Candidate
        ↓
Hardware State Candidate
        ↓
Self Capability / Confidence Candidate
        ↓
Attention / Runtime / Model Requirement Candidate
```

## Assertions

- Hardware identity is distinct from Hardware Capability and Hardware State.
- Capability Contribution produces Evidence support, not Understanding or
  Decision.
- Health values are Available, Degraded, Limited, Failed, or Unknown.
- Hardware Manager reports body state; Runtime owns execution mechanics.
- Attention may reallocate observation; it does not control hardware.
- Model Manager manages implementation assets; Hardware Manager manages body
  state and resource profile.
- Adaptation is a candidate: lower frequency, smaller model, defer background,
  or alternative evidence.
- Reducer remains the sole State mutation authority.

No hardware control, driver, Camera connection, Sensor connection, Model
Runtime, Action Runtime, Emotion, Role, Social, B, or external operation is
included.

No driver is implemented. No Camera, No Sensor, No Model Runtime, No Action
Runtime, No Emotion, No Role, No Social, and No B are included.

No Action Runtime is included.
