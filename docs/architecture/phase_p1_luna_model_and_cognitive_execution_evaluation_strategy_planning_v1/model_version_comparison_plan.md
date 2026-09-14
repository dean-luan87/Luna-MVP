# Model Version Comparison Plan

## Comparison unit

Use a fixed, versioned Test Case Suite and preserve each run as an immutable
evaluation record. Example comparison:

`Model A v1`, `Model A v2`, `Model A v3`, `Model B v1`.

Each result retains model registry ref/version, provider/binding version,
dataset/sample/annotation versions, trace, and TestBoard artifact refs.

## Required deltas

- accuracy/task metric delta;
- evidence quality and stability delta;
- latency delta;
- resource delta;
- observation-cycle and re-observation delta;
- cognitive-burden delta;
- task-success candidate delta;
- failure-mode appearance/disappearance and severity delta;
- regression detection against prior version and baseline.

## Comparison rules

- Keep identical task, sample, condition, and expected observation contract
  when claiming a version delta.
- Separate dataset/annotation drift from model change.
- Report unavailable metrics explicitly.
- Do not overwrite old profiles or declare a benchmark winner to be a runtime
  selection.
