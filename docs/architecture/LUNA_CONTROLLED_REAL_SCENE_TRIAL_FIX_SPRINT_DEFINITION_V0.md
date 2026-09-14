# Phase-RealSceneFix-001 — Controlled Real Scene Trial Fix Sprint Definition v0（修复冲刺定义冻结）

**阶段名**：Phase-RealSceneFix-001  
**性质**：证据链修复冲刺（不是扩场景）；目标是把 fixture-only 证据链补齐到 controlled live evidence 归档链可复现。  

---

## 0) 明确声明（硬边界，写死）

- 不扩真实场景 scope（不新增场景类型，不进入 Option B/C/D，不扩 Option A）
- 不新增真实场景 run（本阶段只补“证据落盘/归档/可复现”机制；真实 run 由后续阶段执行）
- 不进入 full controlled trial
- 不开放真实用户测试
- 不开启默认路径（no default-on）
- 不扩大真实 side effects 面（candidate-only）
- 不新增模型权限/不放权
- 不新增长尾场景

---

## 1) 唯一目标

修复 RealSceneReview-001 指出的关键缺口：当前只有 fixture evidence，缺少 controlled live input 的真实 run evidence 归档质量与可复现性。

必须补齐并冻结：
- controlled live run 的真实证据落盘链（字段+文件+路径）
- explicit entry 的真实落盘链（entry_token + mode_entry_event）
- abort/fallback/degraded 的证据链支持（至少 synthetic 覆盖）
- operator notes / risk events / archive manifest 的归档稳定性

---

## 2) 允许的真实输入范围（写死）

仅允许沿用 RealSceneTrial-001 的 Option A（人行道短距离观察）的定义边界：
- 白天、低人流、平整路段
- operator + safety observer + record owner 到位
- 显式 controlled live input entry
- candidate-only、可随时 abort、必须归档

禁止：
- 新场景/高风险路口/真实过街/夜间雨天/高密人流/长距离/单人测试/外部用户测试

---

## 3) 交付物（v0）

- `docs/architecture/LUNA_CONTROLLED_REAL_SCENE_TRIAL_FIX_SPRINT_DEFINITION_V0.md`（本文）
- `docs/architecture/LUNA_CONTROLLED_LIVE_RUN_EVIDENCE_CAPTURE_CONTRACT_V0.md`
- `docs/architecture/LUNA_REAL_SCENE_ARCHIVE_MANIFEST_SCHEMA_V0.md`
- `docs/architecture/LUNA_REAL_SCENE_OPERATOR_NOTES_AND_RISK_EVENTS_TEMPLATE_V0.md`
- `tools/validate_controlled_live_run_evidence_capture_v0.py`
- `docs/architecture/LUNA_CONTROLLED_REAL_SCENE_TRIAL_FIX_SPRINT_GO_NO_GO_PACK_V0.md`
- `docs/architecture/README.md`（索引更新）

---

## 4) 完成指标（最小）

- controlled live evidence contract 已冻结（字段+落盘文件清单+断言）
- archive manifest schema 已冻结（required_files + hashes + integrity）
- operator notes & risk events 模板已冻结（支持 none_observed）
- validation tool 覆盖 A–L 场景并可复现输出结构化 JSON
- go/no-go pack 给出是否允许回到 RealSceneReview 的结论

---

## 5) 停止条件（满足即停止）

- fix sprint definition 完成
- evidence capture contract 完成
- archive manifest schema 完成
- notes/risk templates 完成
- validation tool 完成并可复现
- go/no-go pack 完成并给出“回到 review”的结论

不得顺手做下一阶段。

