# Implementation routes

## Route A — small canonical Brain Runtime Coordinator

Create a new canonical Brain owner that accepts requests, starts loops, tracks
local state, and accepts closure.

Impact: requires a new authority decision, owner registry entry, API contract,
mutation model, lifecycle integration, and migration of current unresolved
Brain boundaries.

## Route B — protocol/orchestration domain

Keep Brain as a responsibility and protocol domain over existing owners. Use
reference-only coordination envelopes and existing Cognitive Flow/A-Route
mechanics.

Impact: smallest migration; no new owner or source-of-truth state. Closure
acceptance and assimilation remain unresolved until separately authorized.

## Route C — hybrid coordinator plus independent Governance owners

Create a small Brain coordinator while preserving all existing Governance
owners.

Impact: can eventually support local coordination state, but still requires
the owner/API decision and careful anti-monolith controls. It is not safe to
implement until Route A's authority questions are resolved.
