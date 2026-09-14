# Dataset Ingress Contract

## Implementation

The minimum registry foundation is implemented under:

`capabilities/evaluation/dataset_registry/`

It contains four generic declaration types and an empty registry baseline.
No real dataset is registered in this phase.

## Required references

Dataset/sample declarations support identity/version, media refs, source and
provenance, source versions, content hash, annotation/GT refs, environment and
distribution refs, cognitive difficulty, expected observation requirements,
allowed evaluation usage, invalidation/deprecation, and Cognitive Test Case
refs.

The registry references Model, Capability, Provider, and binding identities;
it does not copy their declarations or image/base64 payloads.

## Fail-closed boundary

Registry validation rejects duplicate identity, missing owner/version/
provenance, invalid lifecycle/class/usage, runtime-enabled records,
World-Truth annotations, and malformed links. It does not load data, download
datasets, run models, or enter runtime.
