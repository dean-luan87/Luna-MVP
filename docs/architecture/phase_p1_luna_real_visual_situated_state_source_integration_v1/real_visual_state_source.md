# Real Visual State Source

The selected source is the existing local YOLO11n path:

- Provider: `provider:yolo:local:v1`
- Model: `model-asset:yolo11n:weights-v1`
- Capability: `object_detection`
- Local model path: `vision/detection/yolo/yolo11n.pt`
- Local image path: `_tmp_eval_inputs/roboflow_real_exit_v1/source_image.jpg`
- Runtime owner: `RealProviderExecutionEngineV1`

The new engine calls that existing engine once and reuses the resulting native
detection, `ProviderRuntimeResultV1`, RuntimeObservation, Gateway and
downstream references for all evaluation case projections. It does not read
historical `_eval_out` output as provider data and does not call OCR.

The native `ProviderNativeDetectionRecordV1` supplies detection identity,
class, confidence, bbox, frame dimensions, frame identity and provider trace.
These fields are preserved as candidate evidence and are not promoted to
world or field truth.
