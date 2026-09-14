# LUNA — WorldContextEvidence Source Reference Chain Policy v0

## Phase

- **Phase-WorldModel-ContextEvidence-003**

## Purpose

统一 `WorldContextEvidenceCandidate` 的引用策略，解决：

1) `source_evidence_refs` 到底放什么  
2) 审计/回放需要的“完整上游链”如何表达  

并强制“缺失不得伪造”。

## Definitions

### `source_evidence_refs`

- **只放直接引用（direct refs）**
- 例如：
  - MidPlatform：`ocr_evidence_001`
  - SceneDelta：`scene_delta_decision_xxx`

### `source_reference_chain`

完整引用链（用于 replay/audit/trust），示例：

```json
[
  {"level":"world_context_candidate","ref_id":"world_ctx_0001","ref_type":"WorldContextEvidenceCandidate"},
  {"level":"scene_delta","ref_id":"scene_delta_decision_...","ref_type":"SceneDeltaDecision"},
  {"level":"scene_delta_anchor","ref_id":"sta_...","ref_type":"SpatiotemporalDeltaAnchor"},
  {"level":"midplatform_evidence","ref_id":"ocr_evidence_001","ref_type":"MidPlatformOCREvidenceInput"},
  {"level":"ocr","ref_id":"txt_001","ref_type":"OCRRawTextCandidate"}
]
```

## Integrity & missing

### `source_ref_integrity_status`

- `complete`: direct refs 存在且 missing 为空
- `partial`: direct refs 存在，但链上有缺失（`missing_source_refs` 非空）
- `broken`: direct refs 缺失（本阶段视为 hard blocker）

### `missing_source_refs`

当缺失上游层级时必须显式记录：

```json
{"level":"ocr","expected_ref_type":"OCRRawTextCandidate"}
```

禁止：

- 缺失时伪造 ref_id
- 仅凭推断填充不存在的 YOLO/GPS ref

