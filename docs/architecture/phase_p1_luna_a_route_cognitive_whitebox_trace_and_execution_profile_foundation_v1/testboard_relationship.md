# TestBoard Relationship

`CognitiveWhiteBoxTraceV1`, `LunaCognitiveExecutionProfileV1`, and
`CognitiveFailureGapRefV1` can be referenced by the existing TestBoard
protected-artifact contract.

The TestBoard ref is durable evaluation evidence only. It is not an owner of
Attention, Evidence, Current World, Hypothesis, Sufficiency, Decision, or
runtime state. This phase does not change TestBoard UI or write TestBoard
records automatically.

Future executed phases must preserve the existing required protected records:
process, result summary, conclusion, artifact refs, protected marker, and
non-deletable notice.
