# LUNA Midplatform — YOLO Depth Controlled Real Model DryRun v1

Phase: `Phase-Midplatform-YOLO-Depth-Controlled-Real-Model-DryRun-v1-001`

Controlled offline dryrun using cached YOLO output and authorized depth adapter / mock depth with real frame alignment. Not production runtime.

Pipeline: RealFrameInput → YOLORealOutput → DepthRealOutput → MultiModelAlignment → DepthObjectFusion → FieldGeometry → FieldAssembly → EnhancedFieldSceneCandidate.
