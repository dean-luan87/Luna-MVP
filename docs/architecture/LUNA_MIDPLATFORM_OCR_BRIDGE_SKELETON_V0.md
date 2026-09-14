# LUNA — MidPlatform OCR Bridge Skeleton v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-002**

## Purpose

离线 skeleton：OCR raw text evidence → MidPlatform evidence layer candidates。

只实现合同侧的：
- evidence input 组装
- delta control 占位
- visual_text_relevance_class 分类占位
- filtering/blocking 占位
- text extraction candidate / world context evidence candidate / ambient context candidate 的合同输出
- trace/replay/whitebox 可追溯占位输出

不实现任何 runtime、语义提炼、导航动作、世界模型真实写入。

## Non-governance boundary

- 不接真实 MidPlatform runtime。
- 不接 SceneTask/Fusion/Output。
- 不生成 `navigation_action`（必须为 `null`）。
- 不生成 `semantic_summary`（必须为 `null`）。
- 不执行导航动作、不真实播报、不写入真实世界模型。

## Tools（实现侧）

- `tools/evaluate_midplatform_ocr_bridge_v0.py`：生成离线输出文件集
- `tools/verify_midplatform_ocr_bridge_v0.py`：验收候选与边界约束

## Success criteria（验收必过）

- 输出文件齐全且 trace/replay/whitebox 三份 JSONL 非空
- 所有 candidate 端字段满足：
  - `candidate_only=true`
  - `semantic_summary=null`
  - `navigation_action=null`
  - `allows_execute_now=false`
- 所有 evidence 端满足：
  - 时空/信任/生命周期字段存在（以 contract 统一字段口径）
  - 短 TTL + requires_revalidation（commercial/ambient 默认）

