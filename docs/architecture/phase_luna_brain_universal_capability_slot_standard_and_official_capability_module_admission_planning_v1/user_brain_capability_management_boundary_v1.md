# User and Brain capability management boundary

Both User and Brain may originate governed requests:

- `USER_REQUEST`
- `BRAIN_SELF_REGULATION`
- `SYSTEM_MAINTENANCE`
- `CONSTITUTIONAL_REQUIREMENT`
- `OFFICIAL_UPDATE`

Requests become candidates and pass Capability Governance, permission,
compatibility, resource, Safety Constitution, Model Manager, Provider, and
rollback checks. Neither actor directly mutates Slot, Module, implementation,
or active state. User management instructions cannot bypass the constitutional
minimum safety baseline.
