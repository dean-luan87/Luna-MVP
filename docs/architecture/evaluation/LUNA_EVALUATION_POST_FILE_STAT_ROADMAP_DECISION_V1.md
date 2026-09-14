# Luna Evaluation — Post File Stat Roadmap Decision v1

**Phase**：`Phase-Post-File-Stat-Roadmap-Decision-v1-001`  
**输出目录**：`_eval_out/post_file_stat_roadmap_decision_v1_smoke_v0/`

## 目标

验证 roadmap decision 产物结构、输入 roots 加载状态、边界冻结，以及最终 `final_decision / recommended_next_phase / selected_route` 是否匹配裁决合同。

## 运行命令（smoke）

运行 runner：

```bash
python tools/evaluation/midplatform/run_post_file_stat_roadmap_decision_v1.py
```

运行 verifier：

```bash
python tools/evaluation/midplatform/verify_post_file_stat_roadmap_decision_v1.py
```

## 通过判定

verifier 必须输出：

- `verifier=GO`
- `final_decision=POST_FILE_STAT_ROADMAP_DECISION_READY_FOR_GATE_TAXONOMY_PLANNING`
- `recommended_next_phase=Phase-Gate-Taxonomy-and-Requirement-Framework-Planning-v1-001`
- `selected_route=Gate Taxonomy / Gate Requirement Framework`

