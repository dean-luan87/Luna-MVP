# Luna — Main Project Structure Migration B0 Controlled Execution v1

## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-B0-Controlled-Execution-v1-001`
- **性质**: controlled execution（B0 首次真实小批次迁移；仅三份文档范围）
- **范围锁死**:
  - `docs/architecture/README.md`
  - `docs/architecture/evaluation/README.md`
  - `docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md`

## 输入

- `B0 Preflight Via Harness`（GO，`all_fixed_checks_pass=true`）

## 执行策略

- B0 为 **stable placement**：三份文档已在规范路径，执行 `unchanged` 确认（不强行 move/rename）
- 若未来 batch_config 指定 move/rename 且目标不存在，才执行真实 `os.rename`
- 目标已存在且会造成 overwrite → **abort**

## 禁止

- delete / overwrite / merge / copy
- 触碰 `_eval_out` / protected / HR / DnAE / capabilities / runner / verifier / configs / scripts / tests
- runtime refactor / 内容重写 / 旧 phase 删除或 deprecated

## Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_B0_CONTROLLED_EXECUTION_READY_FOR_POST_MIGRATION_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Post-Migration-Review-v1-001`
