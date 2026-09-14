# Temporal Compression Policy v1

## Principle

Temporal compression retains change structures that may matter to the subject’s
future situated understanding; it is not a time database, telemetry archive, or
lossless event log.

## Compression factors

| Factor | Candidate question |
|---|---|
| Goal relevance | could this change affect the active goal or a bounded future context? |
| Survival impact | could it affect safety, capability continuity, or resource envelope? |
| Change magnitude | is the delta materially different from ordinary jitter? |
| Repetition | is a similar transition recurring under traceable conditions? |
| Future value | could a later Situation benefit from a compact reference? |
| Uncertainty | is the evidence sufficient, or should the candidate remain weak or transient? |

## Examples

- A minute-by-minute temperature change from 25.0 to 25.1 degrees is normally
  discarded as low-value transient detail.
- Rapid environmental temperature increase that may affect embodiment capacity
  may form a Temporal Pattern Candidate, with uncertainty retained.
- A first visit to a novel region may retain a bounded Working Temporal Context;
  it does not automatically form long-term Memory.

## Boundary

Compression policy proposes retain, discard, or candidate-escalation outcomes.
It does not write Memory, create Knowledge, train a model, alter Strategy, or
change a Decision, Action, Attention Runtime, Resource State, or Reducer State.

