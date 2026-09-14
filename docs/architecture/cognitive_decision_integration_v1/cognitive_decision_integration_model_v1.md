# Cognitive Decision Integration Model v1

## Purpose

Decision Integration formally connects the completed Situation and Option
layers to Brain Review. It aggregates and submits a Decision Candidate Package,
tracks the review result, and supports a governed revision loop. It does not
rebuild Decision Logic and does not execute an Action.

```text
Situation Candidate
        ↓
Option Candidate Space
        ↓
Option Evaluation Candidates
        ↓
Decision Context Package
        ↓
Decision Candidate
        ↓
Brain Review
        ↓
Accepted / Modified / Rejected / More Information Candidate
```

## Decision Context Package

The package includes Situation, Options, Constraints, Risk, Unknown,
Capability, Self State, Confidence, Evidence Support, Experience Reference,
and provenance. It identifies whether the package is complete, requires
re-observation, or contains a conflict candidate.

The package is not an Action Command. It does not imply execution, outcome, or
final value approval. Brain receives a structured basis rather than raw world
input and retains final judgment authority. Brain retains final judgment authority.

## Integration responsibilities

Decision Integration may aggregate, submit, trace, compare revisions, preserve
rejected options, and request more information. It may not change Goal, Value,
Reality, Self Identity, or State directly. It does not change Goal. It may not
execute Action, select a Provider, or bypass the Brain Review Interface. It does
not execute Action. It does not execute Action. It cannot select a Provider. The Reducer remains the sole State mutation authority.
