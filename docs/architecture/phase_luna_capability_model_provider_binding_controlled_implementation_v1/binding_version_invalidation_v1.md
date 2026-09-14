# Binding Version / Invalidation v1

Each binding has its own `binding_id` and `binding_version`; there is no
global model or capability version.

Binding inputs preserve source version refs and invalidation refs. Capability,
Slot, Model, weights, loader, Provider contract, adapter or compatibility
changes make the affected candidate stale or superseded. The package rejects
stale candidates and does not auto-refresh or rewrite historical bindings.

