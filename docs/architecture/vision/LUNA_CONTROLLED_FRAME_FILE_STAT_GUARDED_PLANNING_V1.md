# Luna — Controlled Frame File Stat Guarded Planning v1

**Phase**：`Phase-Controlled-Frame-File-Stat-Guarded-Planning-v1-001`  
**性质**：planning-only（只定义未来 *guarded file stat* 的 gate / scope / privacy / audit / failure / rollback / mapping；不执行任何真实文件操作）  
**输出目录**：`_eval_out/controlled_frame_file_stat_guarded_planning_v1_smoke_v0/`

## 阶段目标

本阶段用于回答并冻结：

1. **未来是否允许 stat**：答案为“可作为 future candidate”，但 **当前仍禁止**。  
2. **stat 与 exists/open/read/hash/EXIF/video probe 的边界**：stat 独立 gate，**不得复用 exists gate 直接放行**。  
3. **stat 可能暴露的 metadata 类型与隐私风险**：通过 `FileStatMetadataExposureBoundaryPolicy` 只允许极少候选字段。  
4. **哪些 metadata 可作为候选，哪些必须禁止/延后**：分为 allowed / restricted / blocked_or_deferred 三类。  
5. **哪些路径允许作为 guarded stat 候选**：仅 fixture/registry 受控路径候选。  
6. **哪些路径必须阻断**：外部绝对路径/系统敏感路径/home 任意路径/网络挂载/未知路径/路径穿越等。  
7. **stat 是否可直接生成文件事实**：**否（candidate-only；fact_status=not_fact）**。  
8. **stat 失败或权限不足如何处理**：定义 failure mode（deny/require review/re-register/keep manifest only）。  
9. **stat 结果是否允许写 WorldModel/Memory/Fact/Library**：**否（no-write 冻结）**。  
10. **下一阶段是否进入 File Stat Guarded DryRun**：是，但 dry-run 仍必须 **simulation-only**，不得调用真实 stat。

## 强边界（本阶段必须冻结）

- 不调用 `os.stat / pathlib.Path.stat / lstat`
- 不调用 `os.path.exists / pathlib.Path.exists`
- 不 `open/read`，不读 bytes，不读 image/video contents
- 不 hash，不 EXIF，不 probe，不 decode，不抽帧
- 不进入任何 runtime（camera / OCR provider / tracking / map / crossing / speech）
- 不写 `WorldModel / Memory / Fact / Library`，不触发 action

## 本阶段新增核心对象（结构化产物）

产物均在 `_eval_out/controlled_frame_file_stat_guarded_planning_v1_smoke_v0/`：

- `controlled_frame_file_stat_guarded_planning_policy.json`
- `file_stat_gate_policy.json`
- `file_stat_metadata_exposure_boundary_policy.json`
- `allowed_stat_path_scope_policy.json`
- `blocked_stat_path_scope_policy.json`
- `file_stat_authorization_policy.json`
- `file_stat_audit_trace_policy.json`
- `file_stat_failure_mode_policy.json`
- `file_stat_rollback_policy.json`
- `file_stat_decision_candidate_schema.json`
- `stat_to_file_metadata_candidate_mapping_policy.json`
- `controlled_frame_file_stat_guarded_planning_scenario_matrix.json`（≥24 场景）
- `file_stat_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_file_operation_boundary_report.json` / `no_runtime_boundary_report.json` / `no_write_boundary_report.json`
- `verifier_report.json`

## 规划场景矩阵（最低覆盖）

本阶段输出的 scenario matrix 至少覆盖：

- **future allowed path candidates**：repo fixture / eval_out fixture / registered fixture / controlled test asset  
- **blocked path**：external absolute / traversal / unknown / system sensitive / home arbitrary / network mount  
- **restricted path**：user upload restricted / symlink unresolved restricted  
- **metadata boundary**：allowed / restricted / blocked-or-deferred  
- **failure / rollback**：permission denied / missing file / gate denied / rollback-after-denied

## 通过条件（概念级）

当 verifier=GO 时：

- `final_decision=CONTROLLED_FRAME_FILE_STAT_GUARDED_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001`
- 仍必须保持 `stat_allowed_now=false` 且 `stat_invoked=false`

## 实施状态

- **当前阶段结论**：`GO`  
- **final_decision**：`CONTROLLED_FRAME_FILE_STAT_GUARDED_PLANNING_READY_FOR_DRYRUN`  
- **推荐下一阶段**：`Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001`  
- **后续推进**：
  - `Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001` 已完成并通过（simulation-only；仍不允许真实 `stat`）。  
  - `Phase-Controlled-Frame-File-Stat-Guarded-Post-DryRun-Review-v1-001` 已完成并通过（review-only；确认 `stat/exists/open/read/hash` 全未发生）。
  - `Phase-Controlled-Frame-File-Stat-Guarded-Closure-v1-001` 已完成并通过（closure-only；正式关账，且明确真实 `stat` 仍不可用）。  
  - 当前推荐下一阶段：`Phase-Post-File-Stat-Roadmap-Decision-v1-001`（roadmap-decision-only）。

