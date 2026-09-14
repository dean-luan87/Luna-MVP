# Cognitive Interrupt Recovery Model v1

## Purpose

This model extends the existing Interrupt Candidate boundary with lifecycle and recovery handling for an admitted Runtime Instance Candidate.

## Flow

```text
Interrupt Candidate
  -> Attention Arbitration Candidate
  -> Process Adjustment / Continue / Suspend / Defer Candidate
  -> Runtime Instance Update Candidate
  -> Observation and Feedback Candidate
```

## Constraints

- an interrupt must identify source, urgency, affected process, context, and recovery scope;
- it is arbitrated through Attention Governance and Kernel constraints;
- it may narrow, suspend, resume, or recompose a process candidate;
- it must not automatically cancel every process or mutate persistent State.

## Boundary

Interrupt is not Action. Recovery is not Decision. Runtime Instance Update is not State Mutation. Safety relevance changes candidate priority and admission scope only.

