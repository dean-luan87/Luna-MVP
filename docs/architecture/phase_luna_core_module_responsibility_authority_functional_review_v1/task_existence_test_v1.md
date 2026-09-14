# Task Existence Test v1

| Architecture | Finding |
|---|---|
| Independent Task module | preserves dependency/readiness/completion ownership and testability; preferred |
| Task merged into Intent | conflates purpose with execution organization |
| Task merged into Decision | makes “what” and “how organized” inseparable |
| Task embedded in Action | loses pre-execution dependency/readiness state |
| generic workflow/scheduler | risks global scheduling authority and hides Task responsibility |

Task deserves an independent canonical boundary, but the existing broad Task
Manager must be narrowed. It owns a bounded execution contract, not a global
Planner/Scheduler, cognition engine, or runtime executor.
