# Capability Multi-Capability Composition v1

A Requirement may logically require:

- one capability;
- sequential capabilities;
- alternative capabilities;
- multimodal capabilities;
- fallback candidates.

Capability Governance may describe logical composition and alternative slot
candidates. It must not become a Planner or Scheduler and must not execute
sequencing.

Execution order belongs to governed Task/Decision or a bounded execution
adapter. Runtime Admission assesses each executable candidate. Provider
Governance executes only through its own admission boundary.
