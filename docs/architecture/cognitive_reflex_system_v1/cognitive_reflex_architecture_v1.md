# Cognitive Reflex Architecture v1

## Position

Reflex System is Luna's fast response mechanism for explicit safety rules and
validated experience. It is not Decision, a Shortcut Brain, or a low-level
Agent. Reflex produces a Response Candidate or an Attention Adjustment
Candidate under a bounded Condition, Field Context, Role, and Safety
Constraint.

```text
Condition + Field Context + Active Role + Risk + Safety Constraint
                              ↓
                         Reflex Candidate
                              ↓
                 Response Candidate / Attention Boost
                              ↓
                    Brain Escalation if complex
```

## Innate Reflex

Innate Reflex is sourced from Constitution. It is fixed, high priority, does not learn, and cannot modify Constitution. Examples include a hardware over-temperature protection candidate, a user-protection candidate, and an
extreme-low-battery energy reduction candidate. An Innate Reflex may bypass the
ordinary cognitive path as a candidate, but it is not an automatic action.

## Learned Reflex

Learned Reflex is sourced from Learning System Experience and Pattern Candidates. It requires validation, Governance Admission, context binding,
feedback, and revocation. It must remain below the safety boundary and cannot
become a permanent reflex from one episode.

```text
Experience → Pattern → Learned Reflex Candidate → Validation
           → Governance Admission → Learned Reflex
           → Future Response → Feedback
```

## Field and Role binding

Reflex Trigger is `Condition + Field Context + Risk`. Active Role is also
required where the response candidate depends on social position. The same
event may produce different candidates for a regular participant and a Safety Observer; this is a contextual difference, not Identity or Personality Switching.

## Attention and Workspace interfaces

Many reflexes adjust Attention instead of proposing a response. The permitted
path is `Reflex → Attention Adjustment Candidate → Workspace Update`. Reflex
does not allocate Attention, own Workspace, or make a Decision.

## Brain escalation

Simple, validated candidates may continue as a Response Candidate. Ambiguous,
high-impact, conflicting, or low-confidence candidates enter the Reflex Escalation Interface for Brain Review. Brain retains Goal and final Decision authority.

## Lifecycle and governance

`Candidate → Review → Active → Triggered → Feedback → Adjusted → Deprecated`.
Governance Admission is required before a Learned Reflex becomes Active.
Incorrect learned reflexes are revocable. No Reflex may automatically modify
Safety Rules, Value, Identity, Goal, Decision, or Action.

## Explicit non-goals

No automatic Action, Automatic Action, automatic safety-rule modification, automatic Value change, automatic Personality change, Emotion Runtime, B Runtime, Prediction Runtime, or model training is included.
