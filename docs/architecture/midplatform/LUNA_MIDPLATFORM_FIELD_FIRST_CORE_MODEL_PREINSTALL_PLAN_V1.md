# Luna Midplatform — Field-First Model Preinstall Plan v1

## Phase

`Phase-Midplatform-Field-First-Core-Model-Preinstall-Plan-and-Cache-Manifest-Prepare-v1-001`

## 核心原则

**先预装结构，不预装重量；先建缓存清单，不下载权重。**

- 先建模型房间，不直接接模型
- 禁止下载权重 / clone 大仓库 / 运行推理
- 不跳过 Model Document Capability Review
- 模型输出只能是 candidate

## 8 个模型房间

Visual Perception | OCR/Text | Audio/Speech | Spatial/SLAM/Scene Graph | ECS | Semantic/Event Graph | Field Simulation | Midplatform Reasoning

## 目录结构

`configs/models/field_first/model_rooms/` + 5 个 manifest JSON

## Adapter 占位

`capabilities/midplatform/model_adapters/field_first_adapter_*` — 禁止 import torch/cv2/paddle/transformers

## 全部 manifest 约束

`download_authorized=false` | `weights_downloaded=false` | `inference_ready=false`

## Next Phase

`Phase-Midplatform-Field-First-Core-Model-Document-Capability-Review-v1-001`
