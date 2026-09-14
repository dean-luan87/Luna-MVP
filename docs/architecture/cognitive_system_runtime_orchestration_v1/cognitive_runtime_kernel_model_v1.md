# Cognitive Runtime Kernel Model v1

## Position

The Cognitive Runtime Kernel is the persistent environment that keeps Luna's
cognitive cycle coherent. It is not Brain, not a Scheduler, and not a decision
engine. It does not understand Reality, evaluate values, or choose actions.

```text
World Event
    ↓
Reality Update Candidate
    ↓
Field Update Candidate
    ↓
Attention Allocation Candidate
    ↓
Observation / Cognition Candidates
    ↓
Brain Evaluation when escalated
    ↓
Experience Update Candidate
    ↓
Next Cycle
```

## Kernel responsibilities

The Kernel maintains Cognitive Tick references, module wake-up candidates,
state synchronization, process lifecycle envelopes, and resource boundaries.
It records what is active, waiting, suspended, or stale; it does not assert
what Luna should do.

## Residency and authority

Reality State, Self State, and safety monitoring may be resident contracts.
Attention remains continuous as a governance layer. Brain is event-driven,
Capability is on-demand, and Experience is background. These are wake-up
candidates, not Runtime execution.

The Reducer remains the sole State mutation authority. The Kernel cannot modify
Reality, Field, Goal, Decision, Self Identity, or Action state directly.

## Current boundary

This phase defines no real Runtime, no Scheduler implementation, no Hardware
Runtime, no Action, no model call, no Emotion, no Role, no Social Runtime, and
no B Simulation. No real Runtime, No Scheduler implementation, No Hardware Runtime,
and No Action are enabled. The Kernel does not modify Reality and does not modify Goal.
