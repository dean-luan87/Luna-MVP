# Task / Cognitive Loop Boundary v1

Task owns execution-organization lifecycle. Loop owns mechanical persistence
of admitted cognitive work. They may pause independently: Task can wait while
Loop remains active, and Loop can pause while Task remains active.

Task completion must not automatically close Loop. Loop closure must not
automatically complete Task. Only governed handoffs may carry Task refs,
Loop refs, state versions, completion evidence, or closure consequences.

Task cannot issue semantic Loop commands or infer Concern lifecycle. Loop may
store Task refs mechanically but cannot judge Task completion.
