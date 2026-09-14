# Cognitive Existing Module Inventory v1

## Present packages

```text
cognitive/
  contracts/   candidate.py, signal.py, snapshot.py
  governance/  reducer_boundary.py
  runtime/     tick.py, controlled_execution.py, state_transition.py
  validation/  synthetic runners, validators, and trace schemas
```

## Module characterization

- `contracts/`: three focused immutable contracts; no fragmented type/helper sprawl.
- `governance/`: one focused Reducer-boundary adapter.
- `runtime/`: one Tick contract plus two explicitly synthetic-only controlled skeletons.
- `validation/`: phase-scoped controlled validators and JSON trace schemas; these are not runtime capabilities.

## Not present by design

No packages currently exist for `perception`, `evidence`, `context`, `attention`, `workspace`, `experience`, `evolution`, `kernel`, `organization`, `process`, or `capability`.

## Granularity finding

The current baseline is not prematurely fragmented. Future implementation should introduce complete capability components rather than flat helper/type files, for example `attention_controller/{contract,controller,validator}` only when a separately authorized skeleton phase requires it.

