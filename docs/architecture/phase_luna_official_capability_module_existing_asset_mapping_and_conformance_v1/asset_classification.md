# Asset classification

The catalog distinguishes what Luna can do from what implements or supports
it.

- `CAPABILITY_MODULE`: a problem-solving capability identity, such as
  `object_detection` or `spatial_mapping`.
- `IMPLEMENTATION`: OCR Manager, spatial adapters, and capability runtime
  integration.
- `MODEL`: `detection_v1`, `ocr_v1`, `slam_v1`, `mobile_sam_v1`, and model
  registry entries.
- `PROVIDER`: bounded YOLO11n/provider integration and provider boundary
  adapters.
- `SUPPORTING_ASSET`: registries, Gateway/FPO envelopes, diagnostics, runners,
  and the visual reference package.
- `KNOWLEDGE_REFERENCE`: only dependency references; no Knowledge architecture
  is created.

`segmentation`, `vio_pose_trajectory`, and `face_related` remain
`MAPPING_REVIEW_REQUIRED` when no authoritative official Module record was
found. No missing Module is invented to fill the catalog.
