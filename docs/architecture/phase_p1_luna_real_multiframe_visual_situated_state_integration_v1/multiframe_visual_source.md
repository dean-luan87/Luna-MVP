# Multi-Frame Visual Source

The existing local YOLO11n Provider Runtime is reused twice:

- Provider: `provider:yolo:local:v1`
- Model: `model-asset:yolo11n:weights-v1`
- Model path: `vision/detection/yolo/yolo11n.pt`
- Frame A: `_tmp_eval_inputs/roboflow_real_exit_v1/source_image.jpg`
- Frame B: runtime-generated horizontal-flip derivative under
  `_eval_out/real_multiframe_visual_situated_state_integration_v1/`

The derived frame is a controlled transformation of a real local image. It
is not a camera frame and is not evidence of physical movement. Each YOLO
call produces its own Provider Runtime result, observation reference,
temporal reference, detection reference, bbox and frame dimensions. Historical
outputs are not used as provider results.
