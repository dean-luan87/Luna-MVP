# YOLO11n external asset provisioning and admission verification

This phase prepares the controlled path for an externally provisioned local
YOLO11n weight. It does not copy files, calculate checksums, install
dependencies, import runtime packages, load a model, or invoke a provider.

The flow is:

`external source reference → provisioning record → governed path verification → identity → checksum → dependency probe result → existing contracts → technical admission`

The only canonical target is `model-asset:yolo11n:weights-v1` at
`vision/detection/yolo/yolo11n.pt`.
