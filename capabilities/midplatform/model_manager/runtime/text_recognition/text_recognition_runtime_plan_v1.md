# Luna Model Manager — Real OCR Recognition Runtime Integration Plan v1

**Phase:** `Phase-P1-Midplatform-Luna-Model-Manager-Real-OCR-Recognition-Runtime-Integration-Planning-v1-001`  
**Layer:** Model Manager → Mixed Region Understanding → Text Branch (OCR)  
**Mode:** Planning only — OCR 是 `text_region_candidate` 的 Text Branch 解释器，非独立 pipeline。

---

## 1. 战略定位

真实世界是 **Mixed Visual Semantic Region**，不是「文字」或「图片」二选一。

OCR Recognition 解决 Text Branch：**这个区域里可能是什么字符？**  
Visual Branch 补充图形语义。Semantic Fusion 判断证据是否互相支持。

```
Region Candidate
      ↓
Mixed Region Analyzer
      ↓
 ┌──────────────┐
 │              │
Text Path    Visual Path
(OCR)        (Image Feature)
 │              │
 └──────Fusion─┘
      ↓
Mixed Semantic Evidence → Validation
```

**不是：** 图片 → OCR → 答案  
**不是：** 区域 → VLM → 幻觉答案

---

## 2. 三层证据

| Layer | 职责 | 输出 |
|-------|------|------|
| 1 Text Evidence | 字符/数字/符号 | `text_candidate` |
| 2 Visual Evidence | 形状/颜色/Logo/图标 | `visual_candidate` |
| 3 Semantic Fusion | 证据互相支持 | `mixed_evidence_candidate` |

OCR 只负责 Layer 1，不是终点。

---

## 3. OCR Recognition 职责冻结

### 可以输出

```json
{
  "type": "text_candidate",
  "text": "嘉会湖",
  "confidence": 0.87,
  "source_region_id": "region_001"
}
```

### 禁止输出

- `location` / `current_station` 等空间事实
- 用 VLM 补全遮挡缺字（Visual 补语义，不补文字）

---

## 4. 必须守住的边界

1. **必须有 text_region 支撑** — 无 region → `unsupported_ocr_claim`
2. **低置信度不自动 Qwen 补全** — → `request_more_evidence` 或 Visual 补充
3. **Text/Visual 冲突** → `validation_review`，不直接确认
4. **Runtime 故障** → L2 replan，禁止静默切 Qwen

---

## 5. 模块结构

```
runtime/text_recognition/     ← OCR Text Branch
runtime/mixed_region/         ← Dual Processing + Fusion（核心设计）
```

---

## 6. 下一阶段

`Phase-P1-Midplatform-Luna-Model-Manager-Mixed-Region-Understanding-Planning-v1-001`

包含 Text Recognition Slot、Visual Understanding Slot、Evidence Fusion Slot。
