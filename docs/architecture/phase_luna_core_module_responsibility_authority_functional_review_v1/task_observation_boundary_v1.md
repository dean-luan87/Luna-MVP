# Task / Observation Boundary v1

Task may state that execution depends on condition or evidence X. It may carry
an observation dependency and freshness requirement.

The canonical separation is:

`Task dependency → A determines Cognitive Need when cognition is required →
Attention prioritizes a candidate → Observation/FPO acquires evidence`.

For non-cognitive execution dependencies, Decision/Capability/Action paths may
consume the requirement directly. Task cannot choose observation strategy,
schedule Attention, select a sensor/provider, or treat observation completion
as A Sufficiency.

Existing task-driven observation assets are therefore request-contract and
candidate-handoff assets. Their `request_allowed_now=False` and no camera/OCR
execution flags support narrowing rather than Task-owned acquisition.
