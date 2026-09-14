# Cognitive Attention Arbitration Model v1

Attention Arbitration Candidate compares competing requests under current Goal/Context/Risk/Resource/Sufficiency constraints.

Example request envelope:

```text
source: Risk
target: Traffic Light
reason: Potential Safety Issue
requested_depth: medium
requested_duration: 10s
expected_value: high
```

The resulting candidate may propose reduced depth/duration or defer a request when it conflicts with an active task. Arbitration != truth vote, priority fact, source suppression, Decision, or Action.
