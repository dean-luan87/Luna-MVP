# Cognitive Process Manager Positioning v1

## Position

Cognitive Process Manager is the governance concept that supersedes a narrow Task
Manager. It organizes bounded cognitive process threads inside the operating
model; it is not a Goal owner and not a Scheduler Runtime.

## Thread classes

- **Task Thread:** current task context as a cognitive object;
- **Attention Thread:** an Attention Intent and Observation Requirement;
- **Monitoring Thread:** Neural Driven Monitoring scope;
- **Background Thread:** low-intensity maintenance and pattern observation.

Threads have owner, purpose, scope, priority candidate, resource budget,
lifecycle, and escalation path. They cannot create an independent Goal or bypass
Brain, A Route, Middleware, or the Reducer.

## Boundary

The Process Manager coordinates process metadata and candidate transitions. It does
not execute Action, dispatch a Provider, change Hardware, perform automatic
learning, or mutate State directly. Scheduling and Runtime implementation remain
out of scope for this architecture phase.
