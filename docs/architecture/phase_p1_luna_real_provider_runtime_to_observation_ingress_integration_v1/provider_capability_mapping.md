# Provider and Capability Mapping

The integration uses the existing Field Perception Orchestrator demand/request/
capability candidates, the existing Universal Capability Slot resolver, and
the existing provider/capability registries.

| Observation capability | Canonical capability ref | Slot module | Provider registry result | Output candidate |
|---|---|---|---|---|
| `VISION_DETECTION` | `object_detection` | `object_detection` | `detection_v1` | `object_candidate` |
| `OCR_TEXT_EVIDENCE` | `text_recognition` | `text_recognition` | `ocr_v1` | `text_candidate` |
| `SLAM_SPATIAL_EVIDENCE` | `spatial_mapping` | `spatial_mapping` | `slam_v1` | `spatial_map_candidate` |

Capability resolution precedes provider selection. Provider/model identity is
not exposed to Cognitive State Formation as cognition semantics.
