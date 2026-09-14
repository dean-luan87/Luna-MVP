# Intent / Task Boundary v1

Intent is a governed purpose/orientation. Task is execution organization with
behavior constraints, dependencies, readiness and completion conditions.

One Intent may support multiple Tasks. A Task may carry multiple Intent refs
only when that relationship is explicit, versioned and governed; a Task must
not infer or mutate Intent. Task completion is not Intent completion, and an
Intent closing does not automatically mark every Task complete.

Task Manager may propose an Intent change when execution reality conflicts
with purpose, but the proposal returns to Intent Governance. Capability
routing remains downstream of A's Requirement and Capability Governance;
task-driven routing must not become an implicit Intent owner.
