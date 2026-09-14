# A3 Cognitive Analysis Runtime Validation Matrix v1

| coverage | source evidence | expected condition | validation boundary | failure level |
| --- | --- | --- | --- | --- |
| request | evidence trace references | Context, Evidence, Hypothesis, and Analysis Question refs are present and non-empty | reference shape only; no resolution | blocker |
| envelope | skeleton result | candidate, trace, uncertainty, warnings, flags, and issue-code fields exist | candidate remains `not_executed` | blocker |
| flags | top-level and nested Runtime Flags | all seven fixed zero-side-effect flags agree | no Runtime/model/network/database/writeback/Decision | blocker |
| references | evidence trace | references remain supplied identifiers, not raw values or handles | no fetch, mutation, or source replacement | blocker |
| permission | State/Decision flags | `state_writeback=false` and `decision_executed=false` | Reducer-only State mutation and no Decision execution | blocker |
| forbidden capability | DryRun declarations | model, network, database, external invocation absent | no external capability may be inferred | blocker |
| deterministic validation | raw source and validation output | canonical JSON reproduces exactly | verifier recomputes canonical form without Runner call | blocker |
