# LUNA Evaluation — PaddleOCR Controlled Trial GO / NO-GO Pack v0（Phase-PaddleOCR-Controlled-Trial-001）

## GO

- **materialize_verdict**（输入 materialize summary）为 **GO**；pinned **可读**且 **pinning_complete**、**missing_ref_count**、**sha256** 满足 CacheMaterialize 约定。  
- **Constructor**：`constructor_ok=true`。  
- **OCR**（非 `--constructor-only`）：**1–3** 张图，**全部** `ok`，**`trial_verdict=GO`**。  
- **审计**：`network_request_invoked=false`，`model_cache_modified=false`，**无** routing / RapidOCR / runtime / whitebox / MidPlatform 标志为真。  
- **Verifier**：`verdict=GO`。

## CONDITIONAL_GO

- **`--constructor-only`** 且 constructor **成功**（**未**跑 Layer 2）。  
- 或 **trial_verdict=CONDITIONAL_GO**（例如部分 OCR 失败但错误报告完整 — 以 run 脚本策略为准），**无** verifier **硬 blockers**。  
- **cls** 兼容性疑点已写入 constructor / notes，但 **未**触发硬失败。

## NO_GO

- **materialize** 非 **GO** 或 pinned / sha / pinning 不满足。  
- **Constructor** 失败而 **trial** 仍宣称 **GO**（verifier 拦截）。  
- **OCR** 失败而 **trial** 仍宣称 **GO**。  
- **`network_request_invoked=true`**、**样本数 > 3**、**model_cache_modified**、**routing / RapidOCR / 主线 / MidPlatform** 任一为真。  
- **缺失**必要产物或审计 JSON。

## 与下一阶段

**GO** 仅表示 **离线受控最小 trial** 通过；**不**表示可切换默认 OCR provider 或接入主线。后续若需 **angle cls** 与 **current API** 严格对齐，应更换 **cls** 缓存并重跑 **CacheMaterialize** + **Controlled Trial**。
