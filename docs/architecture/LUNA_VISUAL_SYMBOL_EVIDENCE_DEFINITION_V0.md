# LUNA — Visual Symbol Evidence Definition v0

## Phase

- **Phase-WorldModel-VisualSymbolEvidence-001**

## Purpose（定义冻结；不做实现）

定义“视觉符号证据（Visual Symbol Evidence）”的合同边界，用于承接**形似文字但不应走普通 OCR 主链**的视觉信息：

- 签名、印章/红章、公章
- 字形 Logo / 品牌符号 / 徽章
- 水印、手写标记、符号化标签、认证标识（certificate / certification marks）

核心动机：

- 普通 OCR 目标：**图像里的文字 → 原文文本**
- 视觉符号证据目标：**图形/符号/风格化文字 → 身份/品牌/机构/授权/来源/可信性（需确认）**

## Non-governance boundaries（硬边界）

- 不实现 runtime（只定义合同与默认策略）
- 不接真实记忆写入
- 不接真实世界模型写入
- 不执行导航动作（`navigation_action=null`）
- 不做真实播报
- 不做真假最终裁决（不得输出 verified/forged 的最终结论）

## Positioning（在 OCR 主线之外的并行分支）

视觉符号证据应默认绕过“普通 OCR raw text 作为主判断依据”的路径，进入并行分支：

`Vision Symbol Detection` → `Symbol Candidate` → `Meaning Confirmation` → `Visual Symbol Evidence` → `WorldContextEvidence / Memory Candidate`

允许 OCR 作为辅助，但必须满足：

1. **不走普通 OCR raw text 作为主判断依据**
2. OCR 可以辅助提供 `ocr_auxiliary_text`，但 **OCR 结果不能单独确认含义**
3. 必须保留图像 crop / feature signature / source attribution（可追责）

## Definitions

### visual_symbol_candidate

未确认含义前的候选对象，只能表达“疑似符号/疑似印章/疑似 Logo”，不得当作事实写入长期记忆或高优先级世界事实。

### visual_symbol_evidence

具备可追责的图像引用、视觉签名、来源记录与确认链条的证据对象。其 `meaning_status` 可能仍为 `unknown/suspected`，但结构必须完整。

## Minimum schema（冻结最低字段）

```json
{
  "visual_symbol_evidence_id": "symbol_001",
  "symbol_type": "signature | seal_or_stamp | stylized_logo | brand_mark | emblem | watermark | handwritten_mark | symbolic_label | certificate_mark",
  "source_modalities": ["vision"],
  "source_image_ref": "...",
  "crop_region": { "x1": 0, "y1": 0, "x2": 0, "y2": 0 },

  "ocr_auxiliary_text": null,

  "symbol_visual_signature": {
    "feature_hash": "...",
    "shape_descriptor_ref": "...",
    "color_signature": "...",
    "layout_context": "unknown"
  },

  "meaning_status": "unknown | suspected | confirmed | contradicted",
  "confirmed_meaning": {
    "entity_name": null,
    "entity_type": "person | brand | institution | document_authority | unknown",
    "meaning_label": null
  },

  "confirmation": {
    "confirmation_method": "user_confirmed | multi_observation | trusted_context | manual_annotation | external_verified | none",
    "confirmed_by": null,
    "confirmed_at": null,
    "confirmation_confidence": 0.0
  },

  "memory_policy": {
    "memory_write_policy": "no_write | candidate | confirmed_memory_candidate | forced_with_user_confirmation | persistent_requires_revalidation",
    "requires_revalidation": true,
    "allowed_to_bypass_ocr": true,
    "reason": "visual_symbol_not_text"
  },

  "trust": {
    "visual_confidence": 0.0,
    "context_confidence": 0.0,
    "trust_score": 0.0,
    "fraud_risk_status": "unknown | suspected_forgery | verified"
  },

  "observed_at": { "timestamp_ms": 0, "time_source": "unknown", "date_confidence": "unknown" },
  "observed_where": { "geo_location": { "lat": null, "lng": null, "accuracy_m": null }, "place_hint": "unknown", "spatial_anchor_type": "unknown", "relative_position": { "distance_estimate_m": null, "direction_hint": null } },

  "trace_ref": "...",
  "whitebox_ref": "..."
}
```

## Governance invariants（必须保持）

- 未确认含义前，`memory_write_policy` 不得为 `forced_*` 或事实性持久写入意图
- 任何情况下不得因为 Logo/印章/签名直接生成导航动作或任务执行指令
- 所有强制记忆候选必须保留：`source_image_ref`、`crop_region`、`confirmation.confirmation_method`、`trust.trust_score`

