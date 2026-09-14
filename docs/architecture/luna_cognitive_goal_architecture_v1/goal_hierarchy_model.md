# Goal Hierarchy Model v1

Goals are organized by the time scale and subject scope they protect. A lower
level may refine a higher level, but cannot violate its constraints.

| Level | Name | Example | Owner context |
| --- | --- | --- | --- |
| 0 | Existence Goal | keep the system running and avoid irreversible damage | Self |
| 1 | Capability Goal | maintain healthy visual understanding | Self Regulation / capability context |
| 2 | Social Goal | support a user and preserve respectful interaction | Social Self context |
| 3 | Task Goal | help the user reach a destination | Goal Layer + Task Manager reference |

`Task Goal` is the goal-side direction for a bounded task; it is not a Task
Manager replacement. The Task Manager owns task lifecycle and progress, while
the Goal Layer preserves the reason and desired state. No hierarchy level
directly executes an Action.

Goal admission is explicit. A lower-level candidate is rejected or deferred
when it conflicts with a higher-level stability, capability, or constitutional
constraint. This phase defines the relation only; it does not perform
prioritization or autonomous goal generation.
