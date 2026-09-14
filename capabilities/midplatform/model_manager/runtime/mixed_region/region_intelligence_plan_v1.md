# Luna Model Manager — Region Intelligence Layer Plan v1

**Phase:** `Phase-P1-Midplatform-Luna-Model-Manager-Mixed-Region-Understanding-Planning-v1-001`  
**Layer:** Region Intelligence / Mixed Evidence Understanding  
**Mode:** Planning only — 不是 OCR Enhancement，是 Luna 区域理解的统一基础层。

---

## 1. 核心定位

一个区域不是一个任务，而是一个**信息载体**。

Luna 不应该问：「这里有没有文字？」  
而应该问：「这个区域承载了哪些信息？哪些信息通道需要被激活？」

```
Region Candidate
        ↓
Mixed Region Understanding (Region Intelligence)
        ↓
Information Channel Activation
        ↓
Evidence Fusion
        ↓
Validation
```

---

## 2. Region Understanding 四通道

```
Region Understanding
    ├── Text Channel      → OCR Recognition
    ├── Visual Channel    → Logo / Shape / Object / Style
    ├── Spatial Channel   → Position / Layout / Direction
    └── Context Channel   → Scene Relationship
```

**不要固定 OCR + VLM。** 定义 **Information Slot**，由 Model Manager 路由能力。

---

## 3. Information Slot

```json
{
  "region_id": "region_001",
  "required_information": ["text", "visual_symbol", "layout"]
}
```

Model Manager 决定：

| Slot | Capability | Provider |
|------|------------|----------|
| text | understand_region_text | PaddleOCR |
| visual_symbol | understand_region_visual | Vision Model |
| layout | understand_region_layout | Spatial Analyzer |

---

## 4. Mixed Region Analyzer 职责

**不是识别器。** 判断区域需要哪些观察方式。

店招输出：

```json
{
  "region_type_candidate": "mixed_business_sign",
  "information_slots": ["text", "visual_symbol", "style"]
}
```

地铁导视输出：

```json
{
  "information_slots": ["text", "direction_symbol", "layout_relation"]
}
```

---

## 5. Evidence Completeness

不是 probability，是**当前证据覆盖目标信息的程度**。

```
Text completeness:    70%
Visual completeness:  90%
Combined information completeness: 85%
```

≠ `confidence=85%`

---

## 6. Fusion 原则

**错误：** OCR「星巴克」+ VLM「咖啡店」→ 答案「星巴克咖啡店」

**正确：** 多通道 Evidence → Mixed Evidence Candidate → Validation

---

## 7. Capability 注册升级

```
understand_region_text
understand_region_visual
understand_region_layout
understand_region_context
```

---

## 8. 统一基础层

后续店招理解、商品理解、人物关系、环境理解、无障碍辅助的统一基础。

---

## 9. Ownership Channel（第五通道）

```
Region Discovery → Ownership Layer → per-owner OCR → Fusion
```

**Luna 不是在读文字，而是在理解「这个世界里的信息属于谁」。**

### 流程

```
Image → Object/Surface Segmentation → Ownership Analysis
     → Region Partition → OCR per Region → Fusion
```

### 核心模块

```
ownership_understanding/
    region_owner_analyzer_v1.py
    occlusion_graph_v1.py
    text_owner_assignment_v1.py
```

文字必须带 `owner_candidate`，禁止全图 OCR 平铺合并。

---

## 10. 下一阶段

`Phase-P1-Midplatform-Luna-Model-Manager-Mixed-Region-Understanding-DryRun-v1-001`
