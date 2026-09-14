# LUNA OCR Bridge — Shadow Serialization Go/No-Go Pack v0

## GO

- `ocr_evidence_pack_shadow.json` 生成且内层 `pack.pack_version == ocr_evidence_pack_v0`。  
- `validate_ocr_evidence_pack_v0` **通过**。  
- source ref / forwarding block 报告齐全；**无**伪造 runtime 类前缀。  
- trace/replay/audit jsonl **非空**。  
- `verify_ocr_evidence_pack_shadow_serialization_v0.py` **GO**。

## CONDITIONAL_GO

- 部分 ref 仅为 `eval:` / `shadow:`，缺真实 runtime source binding（预期）。  
- `readiness_posture` 可为 **CONDITIONAL_GO_shadow_offline_binding_only**。

## NO_GO

- 调用 OCR provider 或 MidPlatform。  
- `fact_text_layer` 被打开或 `raw_text_joined` 被当作唯一中台输入。  
- 伪造 `runtime:` 等禁用前缀。  
- 改变 OCR routing 或写世界模型 / 蜂巢 / 语音链。
