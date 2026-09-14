# Change Manifest

## Files created

### Implementation

capabilities/midplatform/core/cognitive_flow/integration/authority_grant_mechanical_command_controlled/

- __init__.py
- authority_grant_mechanical_command_types_v1.py
- authority_grant_mechanical_command_registry_v1.py
- authority_grant_mechanical_command_engine_v1.py
- authority_grant_mechanical_command_fixture_v1.py
- authority_grant_mechanical_command_adapter_v1.py
- run_candidate_only_authority_grant_and_mechanical_command_adapter_v1.py
- verify_candidate_only_authority_grant_and_mechanical_command_adapter_v1.py

### Documentation

docs/architecture/phase_luna_cognitive_capability_authority_grant_controlled_implementation_v1/

- phase_contract.md
- implementation_overview_v1.md
- authority_grant_runtime_boundary_v1.md
- loop_mechanical_validation_v1.md
- derived_b_grant_v1.md
- scenario_mapping_v1.json
- negative_guards_v1.md
- change_manifest.md

## Files modified

None outside the new implementation and documentation directories.

## Canonical impact

- canonical types changed: no;
- canonical enums changed: no;
- canonical owners changed: no;
- verified Dynamic Flow/Loop engines changed: no;
- runtime/provider/model executed: no;
- Brain/Authority/Permission Manager created: no.

## Verification ownership

Runner and Verifier are provided for later user-terminal execution. They were
not executed in this phase.
