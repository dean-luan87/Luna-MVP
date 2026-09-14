# Cognitive Attention Lifecycle State Model v1

Lifecycle State Candidates describe the current handling level of an Attention Candidate:

- `active`: currently consumes bounded cognitive allocation;
- `maintained`: task remains relevant, with reduced immediate processing;
- `background`: low-cost safety/monitoring relevance remains visible;
- `dormant`: valuable but currently not allocating cognitive resources;
- `reduced`: allocation has been lowered due to current validity/resource conditions;
- `suspended`: temporarily paused pending a trigger or constraint change; and
- `closed`: current lifecycle is complete.

These are not persistent system states, memory states, facts, or action commands. An airport gate attention may become maintained/background after discovery rather than deleted.
