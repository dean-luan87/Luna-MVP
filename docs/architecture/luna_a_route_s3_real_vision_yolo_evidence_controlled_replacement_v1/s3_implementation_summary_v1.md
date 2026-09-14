# S3 Implementation Summary

S3 adds a narrow Vision/YOLO provider integration under the existing Field
Perception Orchestrator integration directory. It reuses the existing gated
local YOLO candidate adapter for provider execution and detection mapping.

Provider invocation requires an observation demand, observation request,
`VISION_DETECTION` capability requirement, bounded provider session, model
admission reference, raw frame reference, and trace/provenance. Synthetic
fixtures exercise the same contract without model execution.

Provider-native detections are mapped to `VisualDetectionEvidenceCandidateV1`.
They retain class, bbox, confidence, provider/model/frame references and
lineage. They remain candidate-only, non-fact, non-authoritative evidence.

S0, S1 and S2 regression helpers remain available. OCR, SLAM/VIO, VLM,
semantic interpretation, semantic compression, Field/World mutation and real
runtime remain outside S3.
