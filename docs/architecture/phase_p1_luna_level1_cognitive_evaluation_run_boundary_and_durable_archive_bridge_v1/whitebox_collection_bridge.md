# White-box Collection Bridge

The module reuses `CognitiveWhiteBoxTraceV1`, `LunaCognitiveExecutionProfileV1`, and their existing validators. `WhiteBoxAttachmentV1` only binds refs and validates that a supplied trace/profile came from the existing V1 foundation.

No V2 type or parallel collector is created. A missing runtime signal remains unavailable/not observed. The synthetic fixture uses an existing candidate-only trace fixture to test attachment; it does not claim that the trace came from a real Luna cognitive execution.

TestBoard refs remain protected evidence references. They are non-authoritative and cannot mutate cognition or define archive truth.

