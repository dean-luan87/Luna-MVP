# Scenario mapping

The controlled catalog suite contains 25 cases: schema and CSA completeness,
authority/deferred semantic guards, mandatory safety generic Slot behavior,
model/provider separation, object/OCR/spatial mappings, sensor-health and
unresolved segmentation/VIO/face gaps, Slot compatibility, Self references,
Market deferral, and no runtime execution.

CAT-16 treats `mapping_confidence` as confidence only. It uses the explicit
`MAPPING_REVIEW_REQUIRED:segmentation` module-mapping marker, the MODEL
classification, non-empty rationale/gap, absent CSA, and absent Catalog entry
to prove that MobileSAM has not become a segmentation Module. CAT-17/CAT-18
retain their pre-existing review-status vocabulary in `mapping_confidence`;
that inconsistency is documented for later cleanup and does not alter this
remediation.

The suite is metadata-only and does not prove real provider execution or
capability activation.

`contract_shape_reconciliation_v1.json` records the CAT-01..CAT-25 object,
field, constructor, collection, and semantic-layer audit. Every `_case`
invocation supplies `case_id`, `title`, `passed`, and `details`.
