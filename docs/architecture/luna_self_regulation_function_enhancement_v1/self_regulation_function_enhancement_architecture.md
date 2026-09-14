# Luna Self Regulation Function Enhancement v1

## Position

This phase enhances the existing **Self Regulation Function**. It does not create a
new Homeostasis Layer or a second regulation owner.

```text
Self Constitution
        |
Self Regulation Function  (canonical owner)
        |-- Homeostasis Regulation
        |-- Resource Regulation
        |-- Cognitive Balance Regulation
        |-- Calibration Regulation
        |-- Adaptive Regulation
        `-- Stability Protection
```

Homeostasis, calibration, adaptation, and drift detection are internal mechanisms
of the function. They produce governed candidates; they do not become independently
activatable modules.

## Function boundary

The conceptual function is:

```text
R_t = f(Self_t, Resource_t, Constitution, State_t)
```

Inputs include self state, resources, current cognitive state, field scope,
measurement evidence, outcome/error evidence, active goals, and constitutional
constraints. Outputs are regulation strategy candidates, parameter candidates,
permission candidates, stability assessments, and defer/reject candidates.

The function may observe, evaluate, constrain, and propose. It may not execute
hardware or actions, invoke providers, switch models, rewrite identity, edit the
Constitution, or silently update parameters.

## Stability and growth

The function balances result quality with self stability. A high result score does
not justify excessive drift, unsafe resource use, or stable-core violation. The
evaluation order is:

```text
Constitution / Safety / Stable Core
        -> Homeostasis and range check
        -> Drift and resource check
        -> Calibration and adaptation candidate
        -> Self Review
        -> versioned candidate for an external application boundary
```

`Self Review` is a review gate, not a competing owner. Runtime remains the future
execution boundary, and all candidate applications require explicit governance.

## Absorption rule

The prior Cognitive Homeostasis and Adaptive Balance architecture is retained as
supporting evidence and contract material. Its canonical owner is remapped to the
existing Self Regulation Function through an explicit mapping; files are not moved,
renamed, deleted, or activated by this phase.

