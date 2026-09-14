# Reality Cognition Simulation Scenario Registry Model v1

## Purpose

The Scenario Registry is a planning taxonomy for a future controlled
simulation-test phase. It is not a runtime registry, fixture implementation,
world simulator, or model benchmark.

| Scenario class | Required architectural coverage |
|---|---|
| Basic | obstacle avoidance, route finding, object finding, information acquisition |
| Complex | information insufficiency, conflicting goals, capability limitation, user requirement change |
| Extreme | resource insufficiency, sensor anomaly, material environment change |

Each future registry entry must declare: scenario input envelope, required
self capability/resource context, expected Situation/Decision trace coverage,
outcome injection boundary, expected failure-locality coverage, and forbidden
runtime side effects.

The registry tests whether Luna follows its cognitive-loop contracts. It does
not test whether an AI is generally intelligent, call a real model, or execute
hardware behavior.

The Scenario Registry does not test whether an AI is generally intelligent.
