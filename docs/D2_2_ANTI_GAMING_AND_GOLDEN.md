# D2.2 冻结文档（Anti-Gaming + Golden）

## 1. 目标

把 D 的离线进化评估从「可刷分」升级为「抗作弊的工业门禁」，防止以下四类问题：

1. **通过减少决策/减少字段暴露来逃避回归检测**（沉默作弊）
2. **在低风险帧刷 early_gain**（低风险刷分）
3. **只在简单环境通过，复杂环境崩溃**（环境错觉）
4. **Golden 数据集缺口导致评估失真**（覆盖率不足）

---

## 2. 评估输入与产物

**输入：**

- `library_store/<version>/episodes/.../records.jsonl`（OBS_V1 原样）
- `outputs/<version>/simulations/.../replay_output.jsonl`（baseline/candidate）
- `patches/*.json`（参数补丁）

**产物（写入 outputs，不写 library_store）：**

- `outputs/<version>/simulations/<bundle>/scorecard.json`
- `outputs/<version>/simulations/<bundle>/gate_result.json`
- （suite 模式）`outputs/<version>/sim_suites/<suite_id>/suite_report.json`

---

## 3. 新增指标（D2.2）

### 3.1 Coverage Gate（反作弊核心，硬门禁）

**定义（以「对齐后的帧集合」为总帧）：**

- **total_frames**：baseline 与 candidate 按 seq 对齐后的帧数（交集）
- **decision_valid_frames**：该帧存在 `decision.safety_level` 且 `decision.control_mode`
- **lookahead_valid_frames**：该帧存在 `decision.pal_lookahead_m` 且 > 0（或非 null，按现有规则固定）

**指标：**

- `decision_coverage_ratio` = decision_valid_frames / total_frames
- `lookahead_coverage_ratio` = lookahead_valid_frames / total_frames
- `decision_coverage_delta` = cand_ratio - base_ratio
- `lookahead_coverage_delta` = cand_ratio - base_ratio

**阈值（冻结）：**

- `MAX_COVERAGE_LOSS = 0.02`
- 若 `decision_coverage_delta < -0.02` → FAIL
- 若 `lookahead_coverage_delta < -0.02` → FAIL

**失败原因枚举（必须打印具体数值）：**

- `COVERAGE_FAIL_DECISION_LOSS`
- `COVERAGE_FAIL_LOOKAHEAD_LOSS`

### 3.2 Weighted Early Gain（反低风险刷分，先做指标、暂不做硬否决）

**高风险帧集合（v1 冻结）：**

- 优先：`risk_analysis.complexity_delta > 0` 的帧
- 若无法获得 complexity_delta（replay 不含 explain）→ 标记 `weighted_early_gain_unavailable=true`，该指标不计入排序/门禁

**指标：**

- `early_gain_weighted` = (base_first_guarded_in_high_risk - cand_first_guarded_in_high_risk) / max(high_risk_count, 1)
- `high_risk_count` 写入 scorecard，便于审计

**说明**：现有 `early_conservative_action_gain` 仍保留为硬规则（>=0），weighted 只是「防刷分的解释性指标」，先不上硬门禁。

---

## 4. Golden 数据集与分桶 Gate（环境错觉治理）

**Golden 存储（物理隔离，冻结）：**

- `library_store/<version>/golden/<golden_id>/records.jsonl`
- `library_store/<version>/golden/<golden_id>/meta.yaml`（或 meta.json）

**meta 必填字段：**

- `version_tag`
- `episode_id`
- `source_episode_path`（可选，但建议保留）
- `tags`（非空数组，必须在枚举里）
- `reason`（进入 golden 的理由）
- `created_at`（UTC）

**标签枚举（冻结 v1）：**

- low_light
- cross_traffic
- dynamic_object
- crowded
- reflection
- narrow_passage

**分桶 Gate 规则（冻结）：**

- 对每个 tag bucket：bucket 内**所有** episode 必须 PASS，bucket 才 PASS
- **任意** bucket FAIL → overall FAIL
- bucket 缺失：overall 可 PASS，但必须在报告里标记 `missing_buckets`（交给 C 做补采样/灰度）

---

## D2.2 Cursor 可执行任务清单（按文件/函数口径）

| Task | 内容 | 验收点 |
|------|------|--------|
| D2.2-1 | Scorer 增加 Coverage 指标（_extract_aligned_frames / _is_decision_valid / _is_lookahead_valid → scorecard["coverage"]） | baseline=candidate 时 delta=0；candidate 删 decision 时 delta<0 |
| D2.2-2 | Gate 增加 Coverage 否决，打印 COVERAGE_FAIL: Decision/Lookahead coverage delta = ... (max loss 0.020) | 作弊样例触发 FAIL 且 reason 明确 |
| D2.2-3 | Scorer 增加 Weighted Early Gain（scorecard["early"]，不进硬门禁） | complexity_delta 不可用时 unavailable=true |
| D2.2-4 | tools/promote_to_golden.py（复制 records + 生成 meta，golden_id=episode_id__ts） | tags 为空/不在枚举 → 退出非 0 |
| D2.2-5 | tools/golden_bucket_report.py（每 tag 数量 + missing_buckets） | 输出总数、每 bucket 数量、missing 列表 |
| D2.2-6 | tools/run_sim_suite.py（多 episode → suite_report.json：per-episode、per-bucket、overall、missing_buckets） | 写入 outputs/.../sim_suites/<suite_id>/suite_report.json |
| D2.2-7 | tools/test_anti_gaming_d22.py（置空 decision → Coverage FAIL；低风险 GUARDED → weighted≈0/unavailable） | 两例作弊均被检出 |

---

## 终审结论与已知语义漏洞

**Gate 顺序（价值观表达）**：Safety → **Coverage** → Stability → Efficiency → EarlyGain。沉默作弊（Coverage）优先于行为表现（Stability/Efficiency）拦截。

**Coverage 设计**：以 baseline 与 candidate 按 seq **对齐后的帧集合（交集）** 为 total_frames，逻辑闭合。

**Weighted Early Gain**：replay 不含 complexity_delta 时 `weighted_early_gain_unavailable=true`，当前为“未来接口”。suite_report 中输出 `weighted_early_gain_available_ratio`；若长期 &lt; 50% 需升级 replay 数据结构。

**Golden 分桶**：任意 bucket FAIL → overall FAIL；bucket 缺失仅标 missing_buckets。后续治理可引入 `golden_version`（Golden 变更需人工审核 + 版本化）。

**已知语义漏洞**：若 candidate 在风险帧上将 `safety_level` 降级为 SAFE（baseline 为 CAUTION），当前 Gate 会 PASS（regression 只判“更危险”）。是否算作弊取决于语义：safety_level 是“风险判断结果”还是“参数可塑的输出”。D1 启动前建议做“恶意参数空间攻击测试”（patch 强制 safety_level 全 SAFE），据此决定是否引入 D2.3。测试见 `tools/test_anti_gaming_d22.py` 中 `test_safety_level_downgrade_passes`。

---

*文档版本：D2.2 冻结*
