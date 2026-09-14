# LunaCognitiveExecutionProfileV1 Contract

## Role

The profile summarizes one cognitive evaluation run. It is not Field state,
Current World source-of-truth, runtime state, or semantic closure.

## Covered sections

- identity and task/Goal/Concern/Role/Environment;
- entry Context/Field/prior cognition refs;
- Attention targets and observed transition availability;
- Information Need, Observation Demand/Request, Capability Requirement,
  cycles, and ROI;
- total/relevant/irrelevant/conflicting/uncertain/missing Evidence;
- Current World/Hypothesis/Sufficiency/Information Gap refs;
- Hypothesis revision and Sufficiency transition history;
- Re-observation reason/target/capability/ROI changes;
- stop reason, Decision Governance handoff, outcome candidate;
- cognitive transition count, latency, resource usage;
- trace/provenance/source-version/invalidation/TestBoard refs.

## Availability rule

Counts and measurements use an explicit availability state. Unobserved
latency/resource/ignored-target fields are not encoded as zero or false.

## Boundary flags

The profile is candidate-only and carries false flags for cognition mutation,
Field mutation, authoritative Current World write, World Truth, model/provider
invocation, observation/action execution, and dataset download.
