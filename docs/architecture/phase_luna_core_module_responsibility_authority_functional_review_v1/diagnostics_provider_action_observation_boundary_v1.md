# Diagnostics Provider, Action, and Observation Boundary v1

Observation and Action consume health evidence at their own admission points:
a degraded camera can block/degrade Observation, and an unavailable speaker
can block a speech Action. Provider Governance validates provider admission and
invocation; Action/Observation retain their distinct contracts.

Diagnostics does not invoke Provider, open sensors, execute Actions, declare
evidence, or decide semantic retry/fallback. A diagnostic alert may become an
Action/Notification candidate through governed downstream paths only.
