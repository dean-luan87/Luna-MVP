# Document Surface Detector v1 — Real Runtime Integration Plan

**Phase:** `Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001`  
**Runtime:** `document_surface_detector_v1` — Luna 第一个真实轻量视觉 Runtime（本阶段仅 planning + contract）

---

## 定位

document/surface **候选发现器**，不是 OCR、layout parser、document understanding、fact source。

---

## 冻结管线

```
Attention-Gated Region
    ↓
Model Manager Capability Match
    ↓
document_surface_detector_v1
    ↓
document_surface_candidate
    ↓
overlap / occlusion candidate
    ↓
Ownership Evidence Package
    ↓
Text Owner Assignment Candidate
    ↓
Validation
```

---

## 核心问题

多张纸、菜单、票据叠放时，先发现 document surface entity，再 per-owner text assignment，**避免 OCR 平铺混读**。

---

## 下一阶段

`Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-DryRun-v1-001`
