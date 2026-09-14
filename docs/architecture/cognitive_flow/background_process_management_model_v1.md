# Background Process Management Model v1

## Background threads

Background Process Management governs low-intensity Task Threads, Monitoring
Threads, and Background Threads. A background process declares purpose, scope,
resource budget, freshness requirement, lifecycle, and escalation path.

## Promotion and suspension

Temporal urgency, risk, unknown growth, process dependency, or user relevance may
produce a Promotion Candidate. Resource pressure may produce a Suspension or
Reduction Candidate. These are governed candidates, not automatic execution.

## Boundary

Background Process Management is not a Scheduler and not an Action Runtime. It
does not invoke a Provider, control Hardware, mutate State directly, or create an
independent Goal. The Reducer remains the sole State mutation authority.
