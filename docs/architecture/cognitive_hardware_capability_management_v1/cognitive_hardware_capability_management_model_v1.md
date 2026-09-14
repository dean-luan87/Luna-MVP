# Cognitive Hardware Capability Management Model v1

## Purpose

Hardware Capability Management is the body/self-awareness foundation for Luna.
It describes what physical resources exist, what capability they can
contribute, and how reliable they currently are. It does not control hardware,
execute a Driver, or become a cognitive subject.

```text
Hardware Identity
        ↓
Hardware Capability Profile
        ↓
Resource / Health / Calibration / Limitation
        ↓
Capability State Candidate
        ↓
Self Capability Awareness
        ↓
Attention / Runtime / Model Requirement Candidates
```

## Hardware Capability object

```text
Hardware Capability
├── Identity
├── Specification
├── Capability Profile
├── Resource Profile
├── Health State
├── Calibration State
└── Limitation
```

Camera, Microphone, IMU, GPS, Display, Battery, Storage, and Network are
future registry categories. A camera entry describes Vision Sensor Capability,
resolution, FOV, low-light boundary, health, and confidence impact; it does not
open a camera or produce Reality directly.

## State and diagnostics

Hardware Capability is distinct from Hardware State. State values are
Available, Degraded, Limited, Failed, and Unknown. A blocked lens changes
Hardware State and Capability Confidence Candidate; it does not erase the
capability identity or alter Self Identity.

```text
Hardware Issue
      ↓
Diagnostics
      ↓
Hardware State Candidate
      ↓
Self Capability Update Candidate
      ↓
Attention Reallocation Candidate
```

## Adaptation and governance

Low battery, high GPU temperature, memory pressure, or sensor degradation may
produce Adaptation Candidate: lower observation frequency, choose a smaller
Model requirement, defer background work, or request another Evidence source.
Hardware Manager does not close a Task, change a Goal, choose a Decision, or
execute adaptation.

Hardware Resource Profile informs Model Requirement and Model Admission. Model
Manager manages implementation assets; Hardware Manager describes body state.

## Prohibitions

No hardware control, driver development, Camera connection, Sensor connection,
Model Runtime, Provider Runtime, Action Runtime, Emotion, Role, Social Runtime,
automatic adaptation, or external operation is implemented.

Low battery may request a smaller Model requirement. Hardware Manager does not
change a Goal or choose a Decision. No driver development, No Camera, No
Sensor, No Model Runtime, No Provider Runtime, No Action Runtime, No Emotion,
No Role, and No Social Runtime are implemented.

The low battery condition is explicit. Hardware Manager does not change a Goal
and does not choose a Decision. No Sensor is implemented.
