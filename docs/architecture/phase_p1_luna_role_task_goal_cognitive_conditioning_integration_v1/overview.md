# Role / Task / Goal Cognitive Conditioning

This implementation closes the previously confirmed Role/Task conditioning
surface gap for controlled replay. Reference-only Role, Task, Goal, Concern,
Information Need, and relation inputs now travel through the existing
Observation Gateway → A-Route → Cognitive State Formation path.

The implementation remains candidate-only and non-mutating. `LIVE_RUNTIME`,
models, providers, Field mutation, Decision/Task/Action execution, and durable
state promotion remain outside this phase.
