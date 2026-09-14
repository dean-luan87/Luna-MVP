# Cognitive Execution Process Model v1

## Process definition

A Cognitive Execution Process Candidate is the runtime-facing form of a validated Cognitive Process Candidate. It describes what cognitive work could be performed within an admitted temporary context.

## Required references

- goal and context;
- attention allocation and Kernel constraints;
- capability bundle and resource budget;
- workspace, evidence, unknown, risk, and trace references;
- expected candidate outputs and recovery boundaries.

## Execution boundary

```text
Candidate -> Admission Candidate -> Runtime Instance Candidate
  -> Cognitive Execution Candidate -> Observation Candidate
  -> Evaluation Candidate -> Feedback Candidate
```

The word “execution” describes a future, bounded cognitive-runtime concern. No actual process execution, model invocation, sensor request, device control, decision, or action is introduced by this architecture.

## Separation

Process is not Action. Process is not Decision. Process is not State. Process does not bypass Attention Governance, Kernel validation, or Reducer authority.

