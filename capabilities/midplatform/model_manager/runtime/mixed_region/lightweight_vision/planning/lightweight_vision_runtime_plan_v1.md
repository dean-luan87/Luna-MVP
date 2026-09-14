# Luna — Lightweight Vision Runtime Planning v1

**Phase:** `Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Lightweight-Vision-Runtime-Planning-v1-001`  
**Principle:** 真实 Runtime 为 Ownership Graph 提供候选证据，不是「一次性理解区域」。

---

## 管线

```
Attention-Gated Region
    ↓
Ownership Lightweight Vision Runtime Selection
    ↓
Document / Surface / Layout / PriceTag / Screen Candidate
    ↓
Ownership Evidence Package
    ↓
Relation Candidate
    ↓
Per-Entity Channel Activation
    ↓
Validation
```

---

## 轻量 Runtime 注册表

| Runtime | 用途 | 输出 |
|---------|------|------|
| document_surface_detector | 纸张、菜单、票据 | document_surface_candidate |
| layout_detector | 区块、表格、标题 | layout_region_candidate |
| price_tag_detector | 货架价签 | price_tag_candidate |
| screen_surface_detector | 手机/电视/自助机屏幕 | screen_surface_candidate |
| reflection_detector | 玻璃反光 | reflection_candidate |
| overlap_occlusion_detector | 重叠遮挡 | occlusion_relation_candidate |

---

## 冻结边界

- no_global_ocr
- no_full_scene_segmentation_by_default
- no_all_model_activation
- attention_gate_required
- runtime_outputs_candidate_only
- runtime_does_not_assign_fact
- runtime_does_not_override_ownership_graph
- failure_returns_runtime_error_candidate

---

## 首个真实 Runtime（执行阶段）

`document_surface_detector` — 直接服务叠放纸张 OCR 混读问题。

---

## 下一阶段

`Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001`
