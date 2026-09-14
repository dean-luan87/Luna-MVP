# Document Surface Detector v1 — Real Runtime Implementation Plan v1

## Phase

`Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Planning-v1-001`

## Purpose

规划 `document_surface_detector_v1` 的第一个真实实现路径。本阶段仅做 implementation planning，不执行真实模型。

## Frozen Boundary

- `document_surface_detector_v1` 是 document/surface **候选发现器**
- 只输出 candidate evidence
- 不输出 OCR text / document fact
- 不执行 global OCR / full scene segmentation by default
- 不覆盖 Ownership Graph
- surface_candidate 必须先于 text_owner_assignment
- Attention Gate required
- runtime failure → runtime_error_candidate
- 禁止 silent fallback 到 OCR/VLM/layout/full segmentation

## Recommended First Implementation

**Option A: Classical CV Document Boundary Detector** (`option_a_classical_cv_boundary`)

- 基于边缘/轮廓/四边形/透视几何（规划描述，本阶段不引入 OpenCV 执行）
- 轻量、可控、无重量模型依赖
- 与 candidate-only 契约兼容
- 便于构建 deterministic baseline

Option B/C/D 保留为 deferred candidates。

## Pipeline (unchanged from DryRun)

```
Attention-Gated Region
    ↓
Model Manager Runtime Binding
    ↓
document_surface_detector_v1 implementation
    ↓
document_surface_candidate + relation_hint_candidate
    ↓
Ownership Evidence Package
    ↓
Text Owner Assignment Candidate
    ↓
Validation
```

## Next Phase

`Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-DryRun-v1-001`

Parallel track: `Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001`
