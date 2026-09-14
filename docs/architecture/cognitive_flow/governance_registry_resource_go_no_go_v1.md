# Cognitive Governance Registry and Resource Architecture Go/No-Go v1

## Required checks

- Cognitive Process contains intent, context, state, resource, priority, authority, and lifecycle.
- Lifecycle includes Created, Active, Background, Suspended, Completed, and Archived.
- Resource Budget covers compute, battery, attention, memory, and network.
- Resource Management is not a Scheduler.
- Capability Registry describes what Luna can do and only returns an evidence boundary.
- Model Registry identifies providers and does not become a cognitive subject.
- Hardware Registry describes body structure, health, capability, and lifecycle.
- Authority Registry defines allowed and forbidden operations.
- Diagnostics provides Self Capability State Candidates, not decisions.
- Self Awareness Infrastructure feeds Self Capability Context.
- Self Capability = Hardware Capability + Software Capability + Model Capability + Resource Availability.
- Hardware Manager does not directly control Hardware.
- Reducer remains the sole State mutation authority.

## Hard prohibitions

No real model, No OCR, No SLAM, no Hardware Runtime, no Action Runtime, no B
Reflection, no Emotional Engine, no online learning, no Scheduler Runtime, no
direct Provider execution, and no direct State mutation. Registry entries cannot
change Identity, create an independent Goal, interpret Reality, or make a
Decision.

## Verification handoff

The agent performs planning and V0 static checks only. User Terminal runs the
phase verifier and returns all required sections. The agent stops at
`WAITING_FOR_USER_TERMINAL_VERIFICATION`.

Target output: `COGNITIVE_GOVERNANCE_REGISTRY_AND_RESOURCE_ARCHITECTURE_READY_WITH_NOTES`.
