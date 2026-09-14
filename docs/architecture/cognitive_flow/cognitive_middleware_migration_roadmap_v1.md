# Cognitive Middleware Migration Roadmap v1

## Principle

Maximize reuse of existing Registry, Admission, Protocol, Lifecycle, Diagnostics, Trace/Replay, Model Manager, domain managers, and Model Test Lens assets. Do not create a parallel middleware estate.

| Phase | Scope | Legacy assets | Intended result |
|---|---|---|---|
| Phase 0 — Preserve | Freeze and isolate current baselines. | Capability Registry, manifests, lifecycle, baselines, admission, protocol governance, diagnostics, trace/replay, controlled skeleton. | Keep canonical governance and prevent A-route authority leakage. |
| Phase 1 — Adapt | Design/implement approved boundary adapters only after a future implementation phase. | Model Manager, Task Manager, Field Perception, Vision/OCR/Speech managers, adapters/normalizers. | CWO input and Provider/Middleware report projection without legacy goal/task authority. |
| Phase 2 — Replace | Replace only duplicated legacy control paths once adapters prove equivalent boundary behavior. | Model-first task/model selection paths, legacy result-to-conclusion paths, UI control endpoints. | CWO → capability requirement → Evidence → Neural feedback control flow. |
| Phase 3 — Deprecate | Freeze then retire superseded paths under explicit migration evidence and owner approval. | Fixed-loop legacy runtime integration, task/decision planning routes that bypass CWO, direct result paths. | No uncontrolled model-to-Brain/decision route remains. |

## Migration gates

Before any phase advances: contract compatibility, trace continuity, admission/lifecycle preservation, candidate-only boundary validation, replay/diagnostic coverage, explicit fallback behavior, and user-authorized implementation scope.

No phase in this roadmap authorizes deletion, code migration, Provider invocation, Runtime creation, or hardware/model integration by itself.
