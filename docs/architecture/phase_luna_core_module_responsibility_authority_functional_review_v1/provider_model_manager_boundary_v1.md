# Provider / Model Manager Boundary v1

Model Manager owns model identity, asset, version, path, loader, checksum,
provisioning and model compatibility metadata.

Provider Governance owns the runtime interface, Provider family/instance
admission, invocation identity and Provider-specific execution status. A
shared contract maps `Model Asset ↔ Provider Adapter/Family`; Model Manager
does not invoke Provider and Provider does not own files or checksums.
