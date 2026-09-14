# Middleware Cognitive Bridge Contract v1

## Middleware role

Middleware is Luna's resource and capability governance interface. It coordinates
Capability Registry, Model Manager, Protocol Manager, Diagnostics, and Resource
Management. Resource Management is an explicit Middleware responsibility. It
translates a Cognitive Requirement into a Capability Requirement
and returns a Capability Selection Candidate or a constrained failure candidate.

```text
Cognitive Requirement
  ↓
Capability Requirement
  ↓
Capability Registry / Admission
  ↓
Provider Candidate
  ↓
Evidence Response
```

## Boundary

Middleware does not understand the world, form Reality, own a Goal, interpret a
Situation, make a Decision, or control Hardware. Model Manager supplies Provider
governance only. Protocol Manager validates request and response contracts.
Diagnostics reports localized failures and does not rewrite cognition.

## Resource governance

Middleware may evaluate availability, resource profile, capability envelope,
latency, power, and failure status. It returns an allowed capability boundary to
Neural and Brain; it does not silently convert a shortage into a fact or a Goal.
