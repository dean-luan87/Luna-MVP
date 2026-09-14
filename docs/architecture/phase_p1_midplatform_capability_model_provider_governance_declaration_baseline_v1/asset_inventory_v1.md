# Asset Inventory

Reused canonical locations:

- Capability Registry: `model_manager/registries/capability_registry_v1.json`
- Model Registry: `model_manager/registries/model_registry_v1.json`
- Provider Registry: `model_manager/registry/provider_registry_v1.json`
- Model Contract Repository: `model_contract_repository/`
- Universal Slot types/resolution: `registries/universal_capability_slot/`

New declaration registries are limited to cross-domain bindings because no
existing binding registry was present:

- `capability_model_binding_registry_v1.json`
- `model_provider_binding_registry_v1.json`

Fixture registries, dryrun registries, and legacy routing assets are not used
as canonical declaration sources.

