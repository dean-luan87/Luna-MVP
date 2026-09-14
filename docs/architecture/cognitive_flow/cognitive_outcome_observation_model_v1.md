# Outcome Observation Model v1

## Purpose

Outcome Observation records what is represented as having happened after a
future execution boundary. Outcome is not a binary success/failure verdict and
is not Evaluation.

| Observation dimension | Candidate question |
|---|---|
| Goal progress | what portion of the intended goal appears reached? |
| Environment change | what relevant represented world change followed? |
| User feedback | what user-provided response/constraint is observed? |
| Resource consumption | what candidate time, compute, energy, attention, or embodiment use occurred? |
| Unexpected event | what unplanned evidence, conflict, or unknown appeared? |

Example: reaching a mall can yield `goal_progress: reached` while also
yielding `time_cost: increased` and an efficiency-degradation candidate. The
observation preserves evidence provenance, temporal bounds, uncertainty, and
missing coverage. It cannot declare success, select a correction, or update
World/Self/Strategy/State.
