# Cognitive State Formation Runtime Contract

Replay requests invoke the existing `CognitiveStateFormationEngineV1.run_case` with read-only typed refs, `CONTROLLED_REPLAY_RUNTIME`, a replay identity, and an A-Route execution identity.

The engine executes its existing formation logic and returns `runtime_executed=true` only for this validated replay path, together with an execution ref, canonical owner ref, and transition refs. Candidate-only, no-mutation, no-truth, and no-model/provider guards remain active.

