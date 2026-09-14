# Canonical Version and Invalidation Flow v1

## Identity domains

Concern, Grant, Envelope, A cycle, Observation Request, Provider Invocation, Evidence, Decision, Task, Action execution, Outcome Candidate, Brain adjudication and Loop record each have distinct identities. Concern and Grant scope persist across A cycles until Brain changes them. Other identities are per request, execution, candidate or mechanical record.

## No global version

Each source owner versions its domain: Brain, Intent, Role/Perspective, Field, Context, Current World, Task, Capability, Model, Provider, Observation, Evidence, Decision, Action, Outcome, Envelope, Diagnostics and Protocol.

## Invalidation

`source change → versioned invalidation ref → affected candidate/binding marks stale or rejects → new candidate/binding where permitted → downstream consumer decides consequence.`

Grant revocation, policy change, permission revocation, resource degradation, Model retirement, Provider unavailability, Protocol supersession, stale Evidence, Field/World refresh and Task/Decision changes must not directly mutate another owner. Historical Loop traces retain original versions.

