# Diagnostics Configuration and Manifest Drift v1

Diagnostics may compare observed configuration/registry/manifest state with a
governed reference and report missing declarations, stale mappings, undeclared
assets, or source-set mismatch. The registry, manifest, configuration, or
Model/Capability owner remains source of truth for its domain. A mismatch is a
finding, not permission to rewrite either side.
