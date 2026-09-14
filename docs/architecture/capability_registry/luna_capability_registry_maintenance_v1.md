# Luna Capability Registry Maintenance Standard v1

## Purpose

Define how capability modules are registered, upgraded, replaced, and deprecated with evidence-gated governance.

## Registration Rules

- New module must be added to capabilities/registry/luna_capability_registry_v1.json.
- capability_id must be unique and stable.
- Required manifest fields must be present.
- implementation_path and runner path must be real if declared.

## Status Upgrade Rules

Allowed progression:

- planned
- skeleton_ready
- building
- integration_ready
- functional_module_ready

Upgrade requires corresponding evidence. Direct skip without evidence is forbidden.

## Status Change Authority

- Registry maintainers can edit planned/skeleton/building/integration_ready.
- functional_module_ready changes require explicit ready_evidence updates.
- degraded/blocked/deprecated/retired updates require reason and timestamp.

## Replacement Rules

- Replacement must preserve capability_id lineage by registry record.
- replacement_policy must be declared before replacement execution.
- dependents impact must be updated in dependency map.

## API Version Change Rules

- Backward-compatible change: module_version increment allowed, api_version unchanged.
- Breaking contract change: api_version increment required.
- Breaking changes require dependent review entries.

## Dependency Update Rules

- All dependency updates must be reflected in luna_capability_dependency_map_v1.json.
- Confidence must be marked as confirmed, inferred, or planned.
- Strong dependencies cannot be declared without interface reference.

## Deprecation Rules

- deprecated allows compatibility reads only.
- deprecated modules cannot accept new dependents.
- retired modules cannot be called.

## Ready Evidence Update Rules

- Ready evidence must include latest integration results.
- Evidence path must exist and be parseable.
- If evidence is stale or missing, lifecycle must be downgraded.

## Integration Failure Downgrade Rules

- If a functional_module_ready module fails its module integration runner:
  - immediate status downgrade to degraded or blocked based on failure severity
  - registry entry must include failure reason in known_limitations
  - ready_evidence must be refreshed after remediation

## Baseline Operating Modes

### NORMAL_DEVELOPMENT

- Read existing baseline from capability baseline registry.
- Do not execute full repository inventory.
- Do not rebuild baseline.
- Baseline is governance reference only, not runtime request input.

### CALIBRATION

- Triggered only by calibration standard events.
- Load baseline in anomaly diagnostic workflow only.
- Compare formal mainline, API, contracts, dependencies, lifecycle, and evidence.
- Calibrate only the anomalous module scope.

### REBASELINE

- Triggered when major mainline change, major version change, module split/merge, or baseline proven wrong.
- Create a new baseline_version.
- Preserve historical baseline versions.
- Update baseline registry entry to point to the newest active baseline.

## Baseline Runtime Boundary

- normal_runtime_load_allowed must remain false.
- anomaly_diagnostic_load_allowed must remain true.
- Baseline must not be auto-loaded in normal runtime flows.
