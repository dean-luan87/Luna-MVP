# Luna File Size Governance Inventory v0

> **状态：仅梳理记录，暂不修改代码。**  
> 扫描方式：限定 `capabilities/`、`tools/`、`docs/`（排除 `_tmp_eval_out` 等），禁止全库 rglob。  
> 扫描日期：2026-06-10

## 汇总

| 类型 | above_suggest | warning | blocker_candidate |
|------|---------------|---------|-------------------|
| Python (.py) | 255 | 131 | **18** |
| Markdown (.md) | 2 | 1 | 0 |

## 优先级 A：Midplatform Task Manager Foundation Handoff 链（与 533s 超时直接相关）

| 行数 | 级别 | 文件 | 建议拆分方向 |
|------|------|------|--------------|
| 1335 | blocker | `task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_dryrun_v1.py` | constants → shared；matrix 读 index；capability 留编排 |
| 1286 | blocker | `...owner_approval_request_planning_v1.py` | OUTPUT_CANDIDATE_SPECS / matrix → 独立模块 |
| 1228 | blocker | `...owner_approval_request_dryrun_v1.py` | 同上 |
| 1216 | blocker | `...owner_approval_request_issuance_planning_v1.py` | 同上 |
| 1090 | warning | `...owner_approval_request_issuance_post_dryrun_review_v1.py` | 拆 review builders + timeout/precondition 子模块 |
| 1049 | warning | `...owner_approval_request_post_dryrun_review_v1.py` | 模板化重复逻辑 → shared post_review builder |
| 949 | warning | `...owner_approval_dryrun_v1.py` | dryrun 公共逻辑下沉 |
| 832 | warning | `task_manager_foundation_handoff_evaluation_template_lineage_v1.py` | **按 family/domain 拆文件**，保留聚合入口 |
| 802 | warning | `...owner_approval_post_dryrun_review_v1.py` | post_review shared |
| 747 | above_suggest | `verify_..._issuance_dryrun_v1.py` | 检查项分组 / shared verifier helpers |
| 627 | above_suggest | `verify_..._issuance_post_dryrun_review_v1.py` | 同上 |
| 1408 | blocker | `protocol_input_output_symmetry_registry_patch_v1.py` | registry 表拆 index + detail JSON |

路径前缀：`capabilities/midplatform/` 或 `tools/evaluation/midplatform/`。

## 优先级 B：Python blocker_candidate 全表（>1200 行，共 18 个）

| 行数 | 文件 |
|------|------|
| 5161 | `capabilities/voice/runtime/voice_final_text_dispatcher.py` |
| 1902 | `tools/real_scenario_pack.py` |
| 1738 | `tools/decision_monitor_viewer.py` |
| 1596 | `capabilities/governance/gate_taxonomy_and_requirement_framework_planning_v1.py` |
| 1462 | `capabilities/midplatform/task_manager_runtime_dryrun_v1.py` |
| 1444 | `capabilities/vision/controlled_frame_file_stat_guarded_dryrun_v1.py` |
| 1408 | `capabilities/midplatform/protocol_input_output_symmetry_registry_patch_v1.py` |
| 1404 | `capabilities/vision_runtime/yolo_candidate_adapter_v0.py` |
| 1377 | `capabilities/vision/controlled_frame_input_dryrun_v1.py` |
| 1353 | `capabilities/midplatform/basic_navigation_guidance_loop_stabilization_test_v1.py` |
| 1335 | `capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_dryrun_v1.py` |
| 1299 | `capabilities/vision/visual_ocr_map_task_feedback_dryrun_v1.py` |
| 1286 | `capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1.py` |
| 1252 | `capabilities/vision/controlled_frame_sample_dryrun_v1.py` |
| 1251 | `capabilities/midplatform/basic_navigation_loop_vision_strengthening_dryrun_v1.py` |
| 1244 | `capabilities/vision/controlled_frame_file_existence_check_guarded_dryrun_v1.py` |
| 1228 | `capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1.py` |
| 1216 | `capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1.py` |

## 优先级 C：Markdown warning / above_suggest

| 行数 | 级别 | 文件 |
|------|------|------|
| 1565 | warning | `docs/V1_8_5_WORLD_CONTEXT_MODELING.md` |
| 1045 | above_suggest | `docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PREPLAN_V1.md` |
| 968 | above_suggest | `docs/V1_8_5_CONTEXT_EVOLUTION_ENGINE.md` |

## 已符合或接近标准的示例

- 多数 `run_midplatform_*` runner：< 200 行
- `protocol_separation_rule_v1.py`：~198 行（规则定义体量合理）

## 整改原则（未来执行）

1. **先拆 shared constants / matrix / whitelist**，再瘦 capability
2. **template_lineage** 按 `GRANT_*` / `VISION_*` / `GOVERNANCE_*` family 分文件
3. **verifier** 共用 `file_size_governance_v1.build_file_size_governance_review` 与 grouped check helpers
4. **扫描** 只用 `file_size_governance_v1.scan_python_files(roots=...)`，禁止对整个 repo 无界 rglob
5. 新阶段新增 Python **目标 ≤600 行**；继承大模板时优先 composition 而非 copy-transform 整文件

## 刷新清单

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 -c "
from pathlib import Path
from capabilities.midplatform.file_size_governance_v1 import write_inventory_snapshot
write_inventory_snapshot(
  output_path=Path('_tmp_eval_out/file_size_governance_inventory_snapshot_v0.json')
)
print('ok')
"
```
