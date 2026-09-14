# Capability / Model Manager Boundary v1

## Model Manager owns

- model identity and asset identity;
- model/version/weights version;
- governed path and loader contract;
- dependency requirements and compatibility metadata;
- model/provider mapping metadata;
- declared checksum/integrity metadata;
- provisioning, availability and lifecycle metadata.

The registered YOLO11n asset demonstrates that model asset identity and
declared checksum are Model Manager governance, not Capability identity.

## Capability Governance owns

- capability identity and taxonomy;
- slot identity and functional input/output contract;
- logical module resolution;
- capability-side compatibility requirements;
- candidate mapping references.

## Mapping decision

Model↔Capability mapping is a shared contract with split ownership: Model
Manager declares the asset's supported capability contracts and deployment
metadata; Capability Governance declares the slot/module contract and accepts
the mapping as a candidate. Neither side owns the other side's source state.

Capability Governance must not own model files, calculate checksums, probe
dependencies, load weights or infer.
