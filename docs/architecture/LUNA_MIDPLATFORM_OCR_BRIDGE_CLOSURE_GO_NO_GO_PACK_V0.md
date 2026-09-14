# LUNA — MidPlatform OCR Bridge Closure GO/NO-GO Pack v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-003**

## Scope

本阶段只做 OCR Raw Text → MidPlatform bridge 的回归验收与 closure 收口：

- 只读多个 Bridge-002/002-Fix `output_root`
- 生成 regression 聚合输出
- 冻结 `closed_v0` 状态（offline skeleton only）

不做：

- 不接真实 runtime/中台/下游
- 不做最终语义提炼
- 不生成/不执行导航动作
- 不真实播报
- 不写真实世界模型

## GO conditions（必须全部满足）

1. regression 工具输出完整（summary/matrix/boundary/trw/notes）
2. regression verifier 通过（A–T 全通过）
3. 多输入路径证据成立（sample_matrix / yolo_ocr_bridge_root / ocr_benchmark_root）
4. boundary 成立（semantic_summary/navigation_action 永远为 null；不触发执行/TTS/下游）
5. blocked evidence retained（`retained_evidence_ref` 不缺失）
6. closure 文档完成（closure review / status matrix / boundary register / baseline / future branches）
7. 明确 frozen closure status（`closed_v0`、offline_skeleton_only、runtime_not_allowed）

## CONDITIONAL_GO conditions（允许但必须 honest 记录）

- 某条非关键输入 root 存在非核心字段缺失，但：
  - 不影响边界（禁止项仍成立）
  - regression summary 中明确记录 `unsupported/partial` 的 honest notes
  - 形成 future parser fix 的 follow-up

## NO_GO conditions（任一出现即 NO_GO）

- 任意路径出现 `semantic_summary` 非 null
- 任意路径出现 `navigation_action` 非 null
- 任意路径触发真实 TTS（或 `real_tts_invoked=true`）
- 任意路径触发下游调用（`downstream_invocation_count>0`）
- 任意路径写入真实世界模型
- trace/replay/whitebox 缺失或为空
- blocked evidence 被删除或缺失 `retained_evidence_ref`
- 本阶段接入真实中台/runtime

