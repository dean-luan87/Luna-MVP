# Temporal Scenario Registry v1

## Purpose

The registry defines future controlled cases for representation, compression,
and storage-boundary review. It is not a Runtime registry or time database.

| Scenario | Input pattern | Expected temporal candidate | Retention expectation | Guard |
|---|---|---|---|---|
| stable_environment | repeated insignificant readings | Stability Candidate with high no-change relevance | discard low-value detail | no meaningless record |
| gradual_resource_decline | governed battery observations decrease | Trend Candidate and Temporal Uncertainty | Working Temporal Context candidate | no automatic resource action |
| abrupt_obstacle_change | obstacle appears between observations | abrupt Transition Pattern Candidate | transient + situation-relevant candidate | no Action or provider call |
| cyclic_illumination | day/night references recur | cyclic Temporal Pattern Candidate | long-term pattern candidate only | no future fact claim |
| subject_difference | same decline with different Self Capability | different Temporal Situation Enhancement Candidate | same evidence, different situated significance | no Self Model mutation |

## Required trace fields

`scenario_id`, `previous_reference`, `current_state_reference`,
`change_delta_candidate`, `stability_or_pattern_candidate`,
`temporal_uncertainty`, `compression_candidate`, `retention_level_candidate`,
and `trace_ref`.

Every future case must demonstrate no full-history storage, prediction model,
Scheduler, Hardware Tempo Control, B Reflection, online learning, Action, or
State mutation.
