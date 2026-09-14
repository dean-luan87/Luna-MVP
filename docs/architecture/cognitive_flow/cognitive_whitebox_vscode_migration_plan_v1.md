# Cognitive Whitebox VS Code Migration Plan v1

## Objective

Use the Luna workspace and VS Code as the single engineering entry point for future Cognitive Whitebox work. Existing Model Test Lens remains the reusable local static-site/test-lens asset; no parallel Cursor-specific control surface or new frontend root is created.

## Current asset layout

| Concern | Existing location | Future VS Code role |
|---|---|---|
| Static whitebox UI | `capabilities/midplatform/model_test_lens/static_site/` | Cognitive Whitebox visual shell, migrated incrementally by panels. |
| Local bridge | `capabilities/midplatform/model_test_lens/local_runner_bridge/` | Test-only bridge; never Cognitive Runtime. |
| UI adapters/panels | `model_test_lens/adapters/`, `model_panels/`, `multi_model_interaction/`, `observation_attention/`, `perception_hud/` | Read-only trace projections mapped to CWO/capability/evidence lifecycle. |
| Trace/replay/diagnostics | Model Manager, domain managers, tools evaluation, controlled cognitive validation. | Unified trace-read model for whitebox panes. |
| Architecture contracts | `docs/architecture/cognitive_flow/` | Source of authority/boundary semantics, reviewed beside implementation. |

## Future migration sequence

1. **Trace schema alignment:** map existing model/runner trace data to Intent, CWO, capability requirement, provider/session, evidence, middleware report, and Neural feedback references.
2. **Read-only panels:** introduce cognitive-projection panes without changing existing provider panels' execution behavior.
3. **Legacy panel re-labeling:** convert model activation, result, and planning panels into capability/evidence/feedback views.
4. **Controlled fixture integration:** only after approved Provider Invocation Skeleton, connect static test fixtures through the existing test-only bridge.
5. **Regression observability:** retain existing diagnostics and replay views as nested execution details.

## Constraints

- No UI route may call a model or create a CWO/Goal/Attention allocation.
- No UI state is a cognitive state source.
- No new top-level frontend/backend/whitebox directory is created without explicit approval.
- Existing static site is preserved until a tested migration slice supersedes a panel.

This phase is documentation only; no VS Code configuration, site code, bridge code, or data interface is changed.
