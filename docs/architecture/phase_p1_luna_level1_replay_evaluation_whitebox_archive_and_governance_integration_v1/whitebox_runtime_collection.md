# White-box Runtime Collection

`runtime_collector_v1.py` is observational. It converts canonical A-Route execution evidence into existing `CognitiveWhiteBoxTraceV1` and `LunaCognitiveExecutionProfileV1` records. It creates no authoritative state and does not mutate cognition.

Only emitted refs are represented. Missing Sufficiency, Gap, Stop, and Decision handoff data remains `not_observed`; latency and resource usage remain unavailable.
