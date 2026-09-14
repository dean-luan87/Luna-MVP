# Luna Model Manager — Mixed Region Understanding Plan v1

**Phase:** `Phase-P1-Midplatform-Luna-Model-Manager-Real-OCR-Recognition-Runtime-Integration-Planning-v1-001`  
**Layer:** Text-Visual Dual Processing Layer  
**Mode:** Planning only — OCR 是 Mixed Region Understanding 的 Text Branch，不是独立 pipeline。

---

## 1. 核心问题

真实世界视觉信息不是「文字」或「图片」二选一，而是 **Mixed Visual Semantic Region**：

| 场景 | 混合内容 |
|------|----------|
| 店招 | 文字 + 人物插画 + 火锅图标 + 装饰字体 |
| 地铁导视 | 文字 + 箭头 + 线路颜色 + 站点图标 |
| 商场广告 | Logo + 艺术字 + 商品图片 + 小字说明 |

- **区域 → OCR**：丢掉图形信息
- **区域 → VLM**：容易产生幻觉

Luna 设计：

```
Region
 |
 +----------------+
 |                |
Text Branch       Visual Branch
 |                |
OCR               Image Understanding
 |                |
Text Evidence     Visual Evidence
 |
 +-------- Fusion --------+
              |
     Mixed Semantic Evidence
              |
        Validation
```

---

## 2. 架构位置

```
Text Detection
      ↓
Region Candidate
      ↓
Mixed Region Analyzer   ← 新增
      ↓
 ┌──────────────┐
 │              │
Text Path    Visual Path
 │              │
OCR          Image Feature
 │              │
 └──────Fusion─┘
      ↓
Evidence Candidate
```

OCR Recognition 是 Text Path 的一个 Runtime，不是终点。

---

## 3. 三层证据冻结

### Layer 1: Text Evidence

负责：字符、数字、符号、语言  
来源：OCR Detection + OCR Recognition

```json
{
  "type": "text_candidate",
  "text": "阿叔阿姨的店",
  "confidence": 0.82
}
```

### Layer 2: Visual Evidence

负责：形状、颜色、Logo、图标、物体、布局  
来源：Vision Model / Grounding / VLM（规划阶段 fixture）

```json
{
  "type": "visual_candidate",
  "features": ["person illustration", "food icon", "restaurant style"]
}
```

### Layer 3: Semantic Fusion

负责：多个 evidence 是否互相支持 — **不是** 文字+图片=答案

```json
{
  "type": "mixed_evidence_candidate",
  "text_support": 0.8,
  "visual_support": 0.7,
  "conflict": false,
  "next_action": "fact_admission_candidate"
}
```

---

## 4. 三个必须处理的场景

### 4.1 遮挡 / 损坏

OCR: `阿叔阿?的店`（缺字）  
Visual: 两个老人图案 + 火锅图标  
Fusion: `可能是一个餐饮店招` — **补语义，不补文字**

### 4.2 相似文字 + 图片误导

OCR: `STARBUCKS` + Visual: 绿色圆形 Logo + 咖啡杯 → 一致，可信度提高  
OCR: `STARBUCKS` + Visual: 汽车维修店 → **Conflict** → `validation_review`

### 4.3 艺术字

OCR: 可能失败（火焰形状「火锅」）  
Visual: 红色火焰图案 + 餐饮场景 + 锅具元素 → **补充 OCR 缺失，不替代 OCR**

---

## 5. Luna vs 普通 OCR

```
普通 OCR:  图片 → 文字 → 结果

Luna:      目标 → 选择区域 → 区域理解 → 拆分证据
           (Text / Visual / Spatial / Context)
           → Evidence Fusion → Validation → Decision
```

OCR 只是其中一个能力。

---

## 6. Collaboration Slots（下一阶段）

| Slot | Capability | Role |
|------|------------|------|
| slot_2a | text_recognition | Text Branch — PaddleOCR Recognition |
| slot_2b | visual_understanding | Visual Branch — Image Feature |
| slot_3 | evidence_fusion | Semantic Fusion |

---

## 7. 模块结构

```
runtime/mixed_region/
├── mixed_region_understanding_plan_v1.md
├── mixed_region_analyzer_v1.py
├── text_evidence_builder_v1.py
├── visual_evidence_builder_v1.py
├── semantic_fusion_adapter_v1.py
├── mixed_region_understanding_adapter_v1.py
└── mixed_region_understanding_policy_v1.json
```

---

## 8. 下一阶段

`Phase-P1-Midplatform-Luna-Model-Manager-Mixed-Region-Understanding-Planning-v1-001`

包含 Text Recognition Slot、Visual Understanding Slot、Evidence Fusion Slot。  
OCR Recognition 只是其中一个 Runtime。
