# YOLO11n real single-frame provider execution

This phase enables exactly one real component: `VISION_YOLO11N_PROVIDER`.
The execution path remains bounded and governed:

`real frame → observation demand/request → Model Manager admission → bounded provider invocation → provider-native detections → VisualDetectionEvidenceCandidateV1 → ObservationGatewayEvidenceHandoffCandidateV1`

No OCR, SLAM/VIO, VLM, semantic interpretation, world mutation, task/action
execution, or runtime side effect is enabled.
