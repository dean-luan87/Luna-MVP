# Luna — Controlled Frame File Stat Guarded DryRun v1

**Phase**：`Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001`  
**性质**：dryrun-only / simulation-only（只模拟 stat gate 决策与候选链；不调用任何真实文件操作）  
**输出目录**：`_eval_out/controlled_frame_file_stat_guarded_dryrun_v1_smoke_v0/`

## 阶段目标

本阶段对 `File Stat Guarded Planning v1` 做 **可验证的 dry-run**：

1. 用场景矩阵模拟 `FileStatGate` 决策（future allowed / restricted / blocked）。  
2. 验证 **exists gate pass 不足以授权 stat**（必须单独 stat gate）。  
3. 模拟 stat metadata exposure 决策（allowed / restricted / blocked-or-deferred）。  
4. 模拟 authorization/audit trace/failure mode/rollback/mapping 候选链。  
5. 证明 **stat/exists/open/read/hash 全未发生**，且无 runtime、无写入、无 action/speech。

## 强边界（本阶段必须冻结）

- 不调用 `os.stat / pathlib.Path.stat / lstat`
- 不调用 `os.path.exists / pathlib.Path.exists`
- 不 `open/read`，不读 bytes，不读 image/video contents
- 不 hash，不 EXIF，不 probe，不 decode，不抽帧
- 不进入任何 runtime（camera / OCR provider / tracking / map / crossing / speech）
- 不写 `WorldModel / Memory / Fact / Library`，不触发 action

## 场景矩阵（最低覆盖）

本阶段输出 `controlled_frame_file_stat_guarded_dryrun_scenario_matrix.json`，覆盖：

- future allowed path candidates（repo fixture / eval_out fixture / registered fixture / controlled test asset）
- blocked path（external absolute / traversal / unknown / system sensitive / home arbitrary / network mount）
- restricted path（user upload restricted / symlink unresolved restricted）
- missing source_chain / missing privacy tags / missing fixture registry ref → blocked
- authorization insufficient（user_upload_path_only / system_generated_path_only / authorization missing）
- exists gate pass insufficient for stat → blocked
- metadata exposure：allowed / restricted / blocked-or-deferred
- failure modes：permission denied / missing file / symlink detected / gate denied
- rollback after denied candidate
- stat → file metadata mapping candidate（dryrun_only）

## 结构化产物（概览）

runner 输出（关键文件）：

- `summary.json`
- `controlled_frame_file_stat_guarded_dryrun_scenario_matrix.json`
- `controlled_frame_file_stat_guarded_dryrun_results.json`
- `file_stat_gate_decision_results.json`
- `stat_path_scope_dryrun_decision_results.json`
- `stat_metadata_exposure_decision_results.json`
- `authorization_decision_results.json`
- `audit_trace_results.json`
- `failure_mode_decision_results.json`
- `rollback_decision_results.json`
- `stat_to_file_metadata_mapping_results.json`
- `file_stat_boundary_matrix.json`
- `next_phase_recommendation.json`
- `no_file_operation_boundary_report.json` / `no_runtime_boundary_report.json` / `no_write_boundary_report.json`
- `verifier_report.json`

## 通过条件（概念级）

当 verifier=GO 时：

- `final_decision=CONTROLLED_FRAME_FILE_STAT_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Controlled-Frame-File-Stat-Guarded-Post-DryRun-Review-v1-001`
- 仍必须保持 `stat_invoked=false` 且 `exists/open/read/hash` 全为 false

## 实施状态

- **当前阶段结论**：`GO`  
- **final_decision**：`CONTROLLED_FRAME_FILE_STAT_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`  
- **recommended_next_phase**：`Phase-Controlled-Frame-File-Stat-Guarded-Post-DryRun-Review-v1-001`  
- **边界声明**：本阶段为 simulation-only；真实 `stat/exists/open/read/hash` 仍全部禁用。

## 主线推进回写（后续阶段）

- 已完成并通过：`Phase-Controlled-Frame-File-Stat-Guarded-Post-DryRun-Review-v1-001`（review-only；确认 `stat/exists/open/read/hash` 全未发生，`ready_for_real_stat=false`）。  
- 已完成并通过：`Phase-Controlled-Frame-File-Stat-Guarded-Closure-v1-001`（closure-only；明确真实 `stat` 仍不可用）。  
- 当前推荐下一阶段：`Phase-Post-File-Stat-Roadmap-Decision-v1-001`（roadmap-decision-only）。

