# Goal Architecture Implementation Plan v1

This is a planning-only contract. No Goal Runtime or automatic goal behavior is
implemented in this phase.

1. Reuse the existing cognitive goal/task continuity and Intent→Goal
   interfaces as references.
2. Reuse the existing Task Manager for task lifecycle; do not create a parallel
   Task Manager or Goal Manager.
3. Add a future adapter that carries Goal Candidate context into Task Manager
   and Brain review without granting execution authority.
4. Keep Self Goal Governance as the sole admission boundary and keep
   Constitution above it.
5. Validate future implementations with the contracts and negative guards in
   this directory before any Runtime activation.

Migration is mapping-first: existing assets remain unchanged, an owner and
compatibility adapter are identified first, and implementation is deferred to
an explicitly authorized phase.
