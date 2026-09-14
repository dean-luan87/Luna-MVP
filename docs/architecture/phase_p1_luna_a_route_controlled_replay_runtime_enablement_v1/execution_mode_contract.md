# Execution Mode Contract

Modes are `SYNTHETIC_CONTROLLED`, `CONTROLLED_REPLAY_RUNTIME`, and `LIVE_RUNTIME`.

`synthetic_only` remains as a compatibility and safety assertion. It is true only for synthetic controlled execution and false for controlled replay. `LIVE_RUNTIME` is declared but rejected by the canonical mode validator.

