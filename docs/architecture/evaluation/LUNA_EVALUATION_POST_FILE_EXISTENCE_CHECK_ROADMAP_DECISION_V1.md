# Luna Evaluation — Post File Existence Check Roadmap Decision v1

**Phase**：`Phase-Post-File-Existence-Check-Roadmap-Decision-v1-001`  
**输出目录**：`_eval_out/post_file_existence_check_roadmap_decision_v1_smoke_v0/`

## 目标

验证 roadmap decision 产物结构、输入 roots 加载状态、边界冻结，以及最终 `final_decision / recommended_next_phase` 是否匹配裁决合同。

## 运行命令（smoke）

运行 runner：

```bash
python tools/evaluation/midplatform/run_post_file_existence_check_roadmap_decision_v1.py
```

运行 verifier：

```bash
python tools/evaluation/midplatform/verify_post_file_existence_check_roadmap_decision_v1.py
```

## 通过判定

verifier 必须输出：

- `verifier=GO`
- `final_decision=POST_FILE_EXISTENCE_CHECK_ROADMAP_DECISION_READY_FOR_FILE_STAT_GUARDED_PLANNING`
- `recommended_next_phase=Phase-Controlled-Frame-File-Stat-Guarded-Planning-v1-001`

