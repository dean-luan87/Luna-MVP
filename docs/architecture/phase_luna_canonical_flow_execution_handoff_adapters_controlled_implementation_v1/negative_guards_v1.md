# Negative Guards v1

The synthetic package preserves:

- A does not own final Attention priority;
- Attention does not create or mutate Need;
- Runtime Admission does not own Observation lifecycle;
- Decision and Task do not execute or admit Action;
- Action Result does not complete Task or set A Sufficiency;
- no model/Provider selection by A or Task;
- no Observation, Action, Provider or Runtime execution;
- no source mutation, World Truth, Scheduler, Planner or retry engine.

