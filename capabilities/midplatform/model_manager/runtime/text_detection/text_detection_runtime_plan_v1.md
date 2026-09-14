# Luna Model Manager — Real Text Detection Runtime Integration Plan v1

**Phase:** `Phase-P1-Midplatform-Luna-Model-Manager-Real-Text-Detection-Runtime-Integration-Planning-v1-001`  
**Layer:** Model Manager → Runtime → Text Detection  
**Mode:** Planning only — 一次一个真实 Runtime，先 Text Detection 后 OCR。

---

## 1. 战略收敛

Luna 已验证：理解任务、选择能力、组织 Slot、追踪调用原因、治理 Evidence。

本阶段验证：

> Model Manager 能否把一个真实模型**安全地**接入 Collaboration Engine。

**不要**直接规划「三个真实模型接入」。坚持 **一次一个真实 Runtime**。

---

## 2. 为什么先 Text Detection，不是 OCR

当前 Luna 最大问题不是「读不出来」，而是 **找不到该读哪里**。

嘉会湖、店招问题本质都是 **target proposal**。

第一真实 Runtime：

```
slot_1: text_detection  →  PaddleOCR Detector  →  text_region_candidate
```

OCR、Qwen Context 延后至 Phase 2、Phase 3。

---

## 3. 候选方案

| 方案 | 评估 |
|------|------|
| **PaddleOCR Text Detection** | ✅ 推荐 — 工程成熟、scene text、输出适配 text_region_candidate |
| DBNet / CRAFT | 研究路线，可后续 |
| Grounding DINO | ⏸ 暂缓 — 开放词汇对象发现，非「哪里有文字」 |

---

## 4. 架构

```
L2 Agent Plan (identify_place)
    ↓
Collaboration Slot: slot_1 text_detection
    ↓
Model Manager Binding (paddleocr_detector_v1)
    ↓
Text Detection Runtime Adapter
    ↓
text_region_candidate
    ↓
Evidence Package → Validation
```

---

## 5. 必须守住的边界

1. **Detector 不认识任务** — 输出文字区域候选，不是「发现店招」
2. **Detector 不触发 OCR** — 由 Collaboration Engine 决定 slot_2
3. **不改变 L2 Plan** — identify_place 目标不变

---

## 6. Runtime Roadmap

| Phase | Runtime | Status |
|-------|---------|--------|
| 1 | Text Detection | **当前** |
| 2 | OCR Recognition | Deferred |
| 3 | Qwen Context | Deferred |

---

## 7. 模块结构

```
runtime/text_detection/
├── text_detection_runtime_plan_v1.md
├── text_detection_runtime_adapter_v1.py
├── text_detection_request_builder_v1.py
├── text_detection_response_parser_v1.py
├── text_detection_evidence_normalizer_v1.py
└── text_detection_runtime_policy_v1.json
```

---

## 8. 下一阶段

`Phase-P1-Midplatform-Luna-Model-Manager-Real-Text-Detection-Runtime-Integration-DryRun-v1-001`
