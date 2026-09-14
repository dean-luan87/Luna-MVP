# Diagnostics Model Health Boundary v1

Model Manager owns model identity, declared asset, path, checksum, lifecycle,
provisioning, and registration. Diagnostics may observe file presence,
loadability evidence, environment compatibility, and current runtime health.
Runtime Admission combines those refs with permission, safety, resource,
provider, and source-version evidence. Provider execution remains downstream.

An observed model file is not model identity; a healthy check is not a
capability admission; a model-health mismatch is reported rather than repaired
or registered by Diagnostics.
