# Cognitive State Transition Reducer Boundary v1

Reducer alone mutates admitted Field State. Cognitive State Transition does not mutate World State, Field State, Snapshot, history, temporal state, or Reducer inputs.

The layer may reference Field State/View and candidate changes, but cannot become a Reducer replacement or event-admission path.
