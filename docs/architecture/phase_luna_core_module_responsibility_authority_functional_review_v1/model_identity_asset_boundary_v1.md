# Model Identity and Asset Boundary v1

Model Governance authoritatively owns `model_asset_id`, family, variant/name,
declared model version, weights version, asset type, declared source,
provenance, lifecycle, and governed metadata.

The declared asset is distinct from the physical file and the runtime-loaded
instance. Filesystem/runtime sources report observed existence; Diagnostics
classifies observed health; Runtime Admission decides executable consequence.

Identity collision, incorrect registration, invalid version lineage, and
asset metadata corruption are Model Governance failures.
