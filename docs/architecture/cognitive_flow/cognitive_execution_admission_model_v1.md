# Cognitive Execution Admission Model v1

## Purpose

Admission Control determines whether a Cognitive Process Candidate is sufficiently bounded to create a future Runtime Instance Candidate. It does not execute the process.

## Inputs

- Goal and Context Candidates;
- Risk, Unknown, and Self State Candidates;
- Attention Allocation Candidate;
- Kernel Constraint and Consistency Candidates;
- Capability Availability and Capability Bundle Candidates;
- Resource Budget Candidate.

## Flow

```text
Process Candidate + Admission Inputs
  -> Admission Evaluation Candidate
  -> Admit / Adjust / Defer / Reject Candidate
  -> Runtime Instance Creation Candidate
```

## Example

```text
Need: road-obstacle understanding candidate
Bundle A: visual evidence candidate
Bundle B: visual + depth candidate
Resource constraint: insufficient candidate
  -> Bundle A Admission Candidate
```

The result is only a proposed bounded process context. It does not call a camera, model, device, scheduler, decision runtime, or action runtime.

