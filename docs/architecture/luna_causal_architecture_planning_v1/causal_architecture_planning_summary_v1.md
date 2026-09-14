# Causal Architecture Planning Summary v1

Status: PLANNING_CANDIDATE

This phase establishes Luna causal planning artifacts with candidate-only semantics and no runtime behavior.

Highlights:
- Canonical owner is frozen as Causal Governance with explicit legacy alias handling.
- Causal concept boundary explicitly separates observation, association, correlation, inference, causal hypothesis, support, conflict, uncertainty, and decision.
- Non-equivalence guards are frozen: temporal precedence and correlation cannot become causality automatically.
- Multi-hypothesis coexistence, competition, confounder, counterfactual, and unresolved uncertainty are first-class planning objects.
- Causal-to-Decision handoff is candidate-only and forbids final decision, action instruction, task creation, and execution request.
- 12 minimum scenarios are defined for direct fixture conversion in next stage.

Out of scope remains unchanged:
- no runtime causal engine
- no model call
- no database write
- no source mutation
- no decision or action execution
