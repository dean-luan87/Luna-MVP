# LUNA OCR Bridge — Runtime Flag & Kill Switch Policy v0 (Phase-OCRBridge-Implementation-RFC-001)

## 建议环境变量 / 配置键（语义冻结；名称可微调须 ADR）

### 全局 kill（最高优先级）

| 变量 | 建议默认 | 含义 |
|------|----------|------|
| `LUNA_DISABLE_OCR_BRIDGE_RUNTIME_V1` | **`true`**（或等价「关闭整个 OCR Bridge runtime 行为」） | 一旦为 true：**禁止**任何 shadow 以外的副作用；建议同时短路 validate/forward 链。 |

### 分项开关（默认全部 false）

| 变量 | 建议默认 | 含义 |
|------|----------|------|
| `LUNA_ENABLE_OCR_EVIDENCE_PACK_SHADOW_V1` | **`false`** | 仅生成 **shadow** `OcrEvidencePack`（不落 MidPlatform、不写事实层）。 |
| `LUNA_ENABLE_OCR_EVIDENCE_PACK_VALIDATE_V1` | **`false`** | 对 shadow pack 跑 **validator**；依赖 shadow 或独立输入须定义清楚。 |
| `LUNA_ENABLE_OCR_EVIDENCE_PACK_FORWARD_MIDPLATFORM_V1` | **`false`**（**长期 false** 直至单独 phase 书面授权） | **真实**转发 MidPlatform；默认 **永不开**。 |
| `LUNA_ENABLE_OCR_FACT_TEXT_LAYER_CANDIDATES_V1` | **`false`** | 允许写入 **fact_text_layer_candidates** 路径；**单独开闸**。 |

---

## 强制规则

1. **Shadow pack** 可先实现，但 **默认关闭**。  
2. **Validate** 可在 shadow 之后，但 **默认关闭**。  
3. **`forward_midplatform` 必须长期默认关闭**，直至独立 **Implementation-Authorize** phase。  
4. **`fact_text_layer_candidates` 必须单独开闸**。  
5. **全局 disable 优先级最高**：`LUNA_DISABLE_OCR_BRIDGE_RUNTIME_V1=true` 时，分项全开也必须 **no-op / fail-closed**（由实现 ADR 定义短路顺序）。  
6. **任一必填 `source_ref` 缺失** → **fail-closed**（不 forward、不写事实层、记入 `missing_fields`）。  
7. **任一 distortion violation** → **fail-closed**。

---

## 与 MidPlatform hard gate 的关系

转发前须同时满足：**flags 允许** + **refs 完整** + **validator OK** + **无 governance 违规**；否则保持 **blocked**（与 `OcrEvidencePack` 内 `midplatform_contract.forwarding_mode` 语义一致）。
