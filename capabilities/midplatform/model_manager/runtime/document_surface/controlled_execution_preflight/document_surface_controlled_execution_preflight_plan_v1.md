# Document Surface Detector v1 — Controlled Execution Preflight Plan v1

## Phase

`Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Preflight-v1-001`

## Purpose

Preflight 只读检查：依赖、目录、registry、输出边界、trace、abort、rollback、协议合规是否就绪。不执行 detector，不读取图片内容。

## Allowed

- cv2 import 探测（禁止图像处理函数）
- 目录/registry/schema 存在性检查
- 路径封闭性检查（metadata only）

## Forbidden

- detector 执行、cv2.imread、图像处理、OCR/VLM/layout、依赖安装、runtime 激活

## Next Phase

- cv2 可用：`Controlled-Execution-DryRun-v1-001`
- cv2 不可用：`CV2-Dependency-Admission-Review-v1-001`
