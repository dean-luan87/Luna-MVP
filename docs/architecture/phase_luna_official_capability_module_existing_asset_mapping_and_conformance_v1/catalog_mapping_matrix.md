# Catalog and asset mapping

The executable metadata fixture is
`official_capability_catalog_governance_v1.py`. It records the required
mapping fields for every inspected important asset and exposes
`MAPPING_REVIEW_REQUIRED` in `mapped_capability_module` for unresolved
segmentation, VIO/pose/trajectory, and face-related capability identity.
`mapping_confidence` remains a confidence field; for `mobile_sam_v1` it is
`MEDIUM`. The current schema has no separate conformance-status field.

High-confidence catalog mappings are object detection, basic text recognition,
precise OCR, spatial mapping, and unknown-scene evidence because canonical
Registry entries and model/provider references exist. Safety environment and
visual sensor health are controlled foundation references and retain a medium
confidence source gap rather than being presented as production capability
records.

The VIO and face reference rows still use the older vocabulary value
`MAPPING_REVIEW_REQUIRED` in `mapping_confidence`. This is a non-blocking
metadata inconsistency retained for this remediation; a future schema may
separate `mapping_confidence` from mapping/conformance status.
