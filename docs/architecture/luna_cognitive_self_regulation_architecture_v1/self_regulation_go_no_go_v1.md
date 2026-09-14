# Self Regulation Go / No-Go v1

## V0 readiness

Ready only when observation, health, capability homeostasis, resource regulation, degradation, recovery, lifecycle, interfaces, and adaptation boundaries are represented and the verifier compiles.

## V2 decision contract

`LUNA_COGNITIVE_SELF_REGULATION_ARCHITECTURE_READY` is an architecture readiness signal. It does not activate live self-regulation, automatic model switching, provider calls, hardware control, Runtime Learning, model training, parameter updates, Emotion Runtime, Social Identity Runtime, or Action Runtime.

Failure output must be `LUNA_COGNITIVE_SELF_REGULATION_REMEDIATION_REQUIRED` or the verifier's blocked contract.

## Required gates

- Self Observation is read-only and non-decisional.
- Health state transitions preserve unknown and failure provenance.
- Self Regulation proposes; Capability Governance admits.
- Degradation is reversible and recovery requires validation.
- Adaptation Governance prevents Constitution, Value, Identity, Goal, Brain-rule, Emotion, and Social changes.
- Model Manager and Provider remain implementation sources, not self-regulation authorities.
