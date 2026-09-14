# Luna — Region Intelligence Ownership Real Runtime Integration Plan v1

**Phase:** `Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Real-Runtime-Integration-Planning-v1-001`  
**Layer:** Region Intelligence → Ownership Runtime  
**Mode:** Planning only — deterministic + lightweight vision fixture，规划真实接入点。

---

## 1. 核心判断

Attention-Gated RI DryRun 已验证：**Attention 是感知资源控制系统**。

Ownership Real Runtime 不再面对整张世界，而是面对 **Attention Gate 筛选后的高价值区域**。

---

## 2. 管线

```
Attention-Gated Region
        ↓
Entity / Surface Discovery      (slot_ownership_discovery)
        ↓
Ownership Candidate
        ↓
Occlusion Relation              (slot_occlusion_reasoning)
        ↓
Text Owner Assignment           (slot_text_owner_assignment)
        ↓
Per-Entity Channel Activation
        ↓
Evidence Package
        ↓
Validation
```

---

## 3. 本阶段验证重点

1. Ownership 只处理 Attention Gate **allowed** 区域
2. 先识别信息载体，再做 OCR / Visual / Spatial
3. 文字必须绑定 `owner_candidate`，禁止孤立文本列表
4. 遮挡进入 Occlusion Graph — 被遮挡 ≠ 不存在
5. Runtime 不得静默 fallback 到全图 OCR / 全模型扫描

---

## 4. Runtime Slots（第一批）

| Slot | 职责 |
|------|------|
| `slot_ownership_discovery` | Entity / Surface Discovery |
| `slot_occlusion_reasoning` | Occlusion Graph |
| `slot_text_owner_assignment` | Text → Owner binding |

---

## 5. 输出结构

```json
{
  "entity_candidates": [{
    "entity_id": "paper_A",
    "entity_type_candidate": "document",
    "attention_gate": "allowed",
    "ownership_candidate": { "owner_type": "document_surface" }
  }],
  "relation_candidates": [{
    "entity_a": "paper_A", "entity_b": "paper_B", "relation_type": "occludes"
  }],
  "text_owner_assignments": [{
    "text_region_id": "text_001",
    "owner_entity_id": "paper_A",
    "assignment_confidence": 0.86,
    "candidate_only": true,
    "not_fact": true
  }]
}
```

---

## 6. 下一阶段

`Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Real-Runtime-Integration-DryRun-v1-001`
