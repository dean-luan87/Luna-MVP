# LUNA Mainline Guarded Trial Hook Observability Test Matrix v0

**Phase**：Phase-Mainline-RuntimeReadiness-005  
**验证入口**：`tools/verify_mainline_guarded_trial_hook_observability_v0.py`

---

## 1. 自动化检查（A–U 摘要）

| ID | 检查项 |
|----|--------|
| A | Hook root 可读（含 `mainline_guarded_trial_hook_results.json`） |
| B | Hook results 成功加载 |
| C | RequestTrace stages 已生成（≥3 条） |
| D–F | YOLO / OCR / Qwen Voice stage 均存在 |
| G | `stage_name` / `stage_namespace` 正确 |
| H–J | observability matrix、side-effect audit export、query table 存在且非空列表 |
| K–S | `enabled=false`、`no_op=true`、hard_audit 全不变量 |
| T | trace / replay / whitebox jsonl 非空 |
| U | `summary.input_hook_results_sha256` 与 hook root 文件 SHA256 一致（输入未被改写） |

---

## 2. 手工 / 文档层验收

- Phase-004 hook root 与 Phase-005 output_root 成对归档。  
- `evaluation_notes.md` 记录路径与阶段常量。  
- 下一阶段若实现 CLI query，仍以本阶段 **query_table schema** 为基准。
