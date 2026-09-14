# LUNA OCR Bridge — Runtime Source Ref Plan v0 (Phase-OCRBridge-Implementation-RFC-001)

**规则（写死）**

1. **Runtime `source_ref` 不得使用 `eval:*` 前缀。** `eval:*` **仅允许**出现在 Design-only 示例 pack（OCRBridge-Design-001）。  
2. **Runtime ref 缺失时，`OcrEvidencePack` 不得进入 MidPlatform**（fail-closed）。  
3. **缺失字段必须写入** pack 侧 **`missing_fields`**（实现阶段字段名以 RFC 后续修订为准；语义固定）。  
4. **禁止**补造 `trace_id` / `session_id` / 任意 **source_ref**。

---

## 各 ref 真实来源（规划）

| ref | 真实来源（意图） | 备注 |
|-----|------------------|------|
| **image_frame_ref** | 统一图像帧 / 相机 buffer / 解码帧 id；须可回放或可追溯 | 不得伪造；与 perception 帧生命周期一致 |
| **crop_or_roi_ref** | OCR 输入裁剪区域；整图 OCR 须显式 **`full_frame_roi`** | 与 bbox 坐标系声明一致 |
| **ocr_provider_invocation_ref** | RapidOCR / PaddleOCR / CnOCR **单次调用记录**（含 provider 版本、参数哈希） | 与 stage2 executor 对齐 |
| **raw_candidate_ref** | raw 行/块 candidate 产物（索引或内容寻址 id） | 非 MidPlatform 主输入 |
| **layout_governance_ref** | layout / symbol / glyph governance 输出快照 id | 见 `ocr_layout_symbol_governance_v0` |
| **image_quality_gate_ref** | input quality gate 结构化输出 id | 与 blur/contrast/skew 等一致 |
| **eligibility_gate_ref** | runtime eligibility 结论（非 eval 仿真器） | 与 OCR-007 评测路径分离 |
| **reading_order_ref** | reading_order_candidates / 选定 ro id | uncertain 时禁止 global fact |
| **trace_ref** | RequestTrace / TRW **jsonl** 路径或逻辑 id | 不伪造 |
| **replay_ref** | replay **jsonl** 路径或切片 id | 不伪造 |
| **audit_ref** | hard audit / 评估审计视图键 | 与实现阶段 observability 对齐 |

---

## MidPlatform 转发前（hard gate 语义）

在 **所有必填 runtime ref 齐备** 且 **validator 通过** 且 **无 distortion violation** 且 **flag 授权** 之前，**任何** forward 必须保持 **blocked / no-op**。

### Hard gate 检查清单（实现阶段须逐项落地）

1. `LUNA_DISABLE_OCR_BRIDGE_RUNTIME_V1` 不为「关闭整个桥」的阻断态时，才允许继续评估分项开关。  
2. **`LUNA_ENABLE_OCR_EVIDENCE_PACK_FORWARD_MIDPLATFORM_V1`** 未显式授权前 **恒 false**。  
3. 顶层与条目 **runtime `source_ref`** 无 `eval:*`、无缺失、无伪造。  
4. **`missing_fields` 为空**（或实现约定下可接受的显式豁免，须 ADR）。  
5. **`midplatform_contract.forwarding_mode`** 与 hard gate 一致；**distortion** 与 **reading_order** 规则已通过 validator。  
6. **hard_audit** 全 false（含 `midplatform_invoked`、`scene_delta_invoked`、`world_context_invoked`）。

详见 `LUNA_OCR_BRIDGE_RUNTIME_FLAG_AND_KILL_SWITCH_POLICY_V0.md` 与 `LUNA_OCR_BRIDGE_SHADOW_ONLY_WIRING_STRATEGY_V0.md`。
