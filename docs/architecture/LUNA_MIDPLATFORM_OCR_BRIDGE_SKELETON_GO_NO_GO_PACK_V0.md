# LUNA — MidPlatform OCR Bridge Skeleton GO/NO-GO Pack v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-002**

## GO 条件

- `tools/evaluate_midplatform_ocr_bridge_v0.py` 能在任意允许输入类型上生成完整输出文件集
- verifier 检查通过：
  - candidate_only=true
  - semantic_summary=null
  - navigation_action=null
  - allows_execute_now=false
  - real_tts_invoked=false
  - downstream_invocation_count=0
  - trace/replay/whitebox JSONL 三份非空
- 未写入真实世界模型、未接真实 MidPlatform runtime、未接推荐/任务执行

## NO-GO 条件

- 任意 candidate 输出出现：
  - semantic_summary != null
  - navigation_action != null
  - allows_execute_now != false
- trace/replay/whitebox 任意一份缺失或为空
- 未能保持 evidence 为 candidate-only 与 non-runtime 边界

