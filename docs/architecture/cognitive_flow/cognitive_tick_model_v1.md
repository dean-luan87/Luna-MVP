# Cognitive Tick Model v1

Cognitive Tick Candidate is an event-driven candidate for initiating or revisiting a cognitive cycle. It is not a fixed interval such as a 100ms loop and not a Runtime scheduler.

Permitted trigger candidates include:

- Field Change Trigger;
- Cognitive Need Trigger;
- Goal Change Trigger;
- Risk Change Trigger;
- Context/Information/Time/Resource change trigger.

A tick candidate may request candidate updates only. It does not invoke sensors/models, execute a cycle, make a Decision, grant Permission, or mutate State.
