# Determinism Audit Report

**审计目标**：结构级检查，识别未来可能导致 determinism 失效的隐患。  
**范围**：D1 双通道 + Stress Gate + Determinism Enforcement 相关链路。  
**日期**：审计执行时生成。

---

## 一、最高优先级：确定性链路完整性

### 1️⃣ 候选生成是否完全受 seed 控制

**检查文件**：`simulation/d1/candidate_generator.py`

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 所有 random 来自同一 seed | **PASS** | 使用 `random.Random(seed)` 单例，未使用全局 `random`/`np.random` |
| 无 time.time() 参与 | **PASS** | 未发现时间参与采样或 ID 生成 |
| 无默认 RNG | **PASS** | `generate_candidates` 内仅 `rng = random.Random(seed)` 一处创建 RNG |
| LHS/随机扰动使用固定 seed | **PASS** | LHS 使用 `generate_lhs_patches(num_sampled, seed=seed)`；非 LHS 分支使用 `rng.randint(0, 2**31-1)` 派生子 seed，序列由同一 `rng` 决定，确定性 |
| 未在循环内重新 seed | **PASS** | 无在循环内调用 `random.seed()` / `np.random.seed()` |

**结论**：**PASS** — 候选生成完全由传入 `seed` 控制，无隐性熵源。

---

### 2️⃣ run_sim_suite / sim_runner 是否含隐性随机

**检查文件**：`tools/run_sim_suite.py`、`simulation/sim_runner.py`

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 无 shuffle() | **PASS** | 两文件中均未使用 shuffle |
| 无无序 set 迭代参与排序 | **PASS** | 未发现 set 迭代影响 episode 顺序或聚合顺序 |
| episode 顺序固定 | **PASS** | `run_sim_suite.py` 第 62、89 行：`for ep_id in sorted(os.listdir(golden_dir))`，遍历顺序固定 |
| 文件/目录遍历使用 sorted() | **PASS** | golden 下 episode 列表均通过 `sorted(os.listdir(golden_dir))` 取得 |
| sim_runner 内随机/遍历 | **PASS** | `sim_runner.py` 未使用 random/shuffle；未做目录遍历，仅按传入路径读 records |

**WARNING**：`run_sim_suite.py` 第 209 行：
- `suite_id = Path(args.patch).stem + "_" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")`
- `suite_id` 写入 `suite_report.json`，**当前指纹不依赖 suite_report 内容**（指纹来自 `rank_report.json` 的 champion 的 stress_summary/regular_summary），故不影响当前 determinism。
- **建议**：若后续任何逻辑对 `suite_report` 做整体哈希或把 `suite_id` 纳入摘要，需改为不依赖时间的 ID（例如基于 patch + episode 列表的哈希），否则会破坏 determinism。

**结论**：**PASS**（加一条 WARNING 作为未来防护）。

---

### 3️⃣ 排序稳定性（lexicographic_ranker）

**检查文件**：`simulation/d1/lexicographic_ranker.py`

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 排序使用稳定排序 | **PASS** | `ranked.sort(key=lambda x: x["_rank_key"], reverse=True)`，Python 的 sort 稳定 |
| rank_key 结构固定 | **PASS** | `rank_key` 为 `(float, float, float)` 三元组：early_gain_mean, -guarded_tail_ratio_mean, -volatility_mean |
| 不包含 dict/set | **PASS** | rank_key 仅含 float，持久化为 list，无 dict/set |
| 浮点未做不可逆格式化 | **PASS** | 直接使用 float，未先格式化为字符串再参与排序 |

**结论**：**PASS** — 排序键稳定、结构固定、无非有序容器。

---

## 二、中优先级：双通道物理一致性

### 4️⃣ stress 与 regular 是否完全隔离

**检查文件**：`tools/run_d1_tournament.py`，base patch 由 `stress_base_patch` / `regular_base_patch` 分别加载

| 检查项 | 结果 | 说明 |
|--------|------|------|
| risk_scale_factor 仅 stress=5、regular=1 | **PASS** | 由各自 base patch 文件注入（stress_channel_phys_v1.json / regular_channel_phys_v1.json），候选禁止含 risk_scale_factor |
| 无 channel 交叉污染 | **PASS** | `effective_stress = _deep_merge(stress_base_patch, candidate_patch)`，`effective_regular = _deep_merge(regular_base_patch, candidate_patch)`，两路独立 |
| effective_patch 分 channel 生成 | **PASS** | 双通道下分别写 `effective_patch.stress.json` 与 `effective_patch.regular.json`，不共用 |

**结论**：**PASS** — 双通道物理与 effective_patch 完全隔离。

---

### 5️⃣ effective_patch 是否不可变（无引用修改）

**检查文件**：`tools/run_d1_tournament.py` — `_deep_merge()`

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 合并结果为独立对象 | **PASS** | `result = dict(base)` 后对 override 键赋值，得到新顶层 dict |
| 无后续对 base 的写穿 | **PASS** | 合并后仅 `write_text(json.dumps(...))`，无对 result 的嵌套 in-place 修改 |
| 嵌套引用风险 | **WARNING** | `_deep_merge` 为浅合并；若未来对 result 的嵌套 dict 做 in-place 修改，可能影响传入的 base。当前用法仅序列化写出，无此操作。建议若扩展合并逻辑，对嵌套结构使用 copy.deepcopy 或显式深合并。 |

**结论**：**PASS**（当前用法下无引用修改；WARNING 供后续扩展参考）。

---

## 三、较低优先级：浮点与指纹一致性

### 6️⃣ 指纹生成是否统一排序

**检查文件**：`tools/run_d1_tournament.py` — `_hash_dict()`

| 检查项 | 结果 | 说明 |
|--------|------|------|
| json.dumps(…, sort_keys=True) | **PASS** | `s = json.dumps(d, sort_keys=True, ensure_ascii=False)` |
| 浮点未隐式转字符串再参与 | **PASS** | 直接对 dict 序列化，无先 format 再进哈希 |

**结论**：**PASS** — 指纹生成稳定、键序固定。

---

### 7️⃣ summary_hash 计算字段是否固定（无时间戳/路径/文件名）

**检查文件**：`tools/run_d1_tournament.py` — `get_fingerprint_from_run()` 内 stress_summary / regular_summary

| 检查项 | 结果 | 说明 |
|--------|------|------|
| stress_summary 字段 | **PASS** | 仅：guardian_discipline, high_risk_frames_count, early_gain_mean, exit_latency_p95, hysteresis_efficiency；无时间戳、路径、文件名 |
| regular_summary 字段 | **PASS** | 仅：guarded_tail_ratio_mean, guarded_tail_ratio, volatility_mean；同上 |
| guardian_discipline 内容 | **PASS** | 来自 scorecard 的审计摘要（数值与 status），无路径/时间戳 |

**结论**：**PASS** — 参与哈希的 summary 仅含稳定指标，无环境相关字段。

---

## 四、输出层完整性

### 8️⃣ personality_profile 是否只在 determinism 通过后生成

**检查文件**：`tools/run_d1_tournament.py` 主流程

| 检查项 | 结果 | 说明 |
|--------|------|------|
| NON_DETERMINISTIC_EVOLUTION 时是否写 personality_profile | **PASS** | `if det_result["status"] != "PASS": write_failure_manifest(...); return 1`，此后不会执行到 `write_personality_profile` |
| 失败时是否只写 run_manifest | **PASS** | 失败分支仅调用 `write_failure_manifest`，其内容包含 determinism_status 与 determinism_runs，等价于“只写 run_manifest”的证据链 |

**结论**：**PASS** — personality_profile 仅在 determinism 通过（或未开 determinism 校验）时写入。

---

### 9️⃣ run_manifest 是否记录完整可回溯信息

**检查文件**：`tools/run_d1_tournament.py` — `write_run_manifest()`、`write_failure_manifest()`

| 检查项 | 结果 | 说明 |
|--------|------|------|
| seed | **PASS** | 必参，写入 manifest |
| git_commit | **PASS** | 子进程读取 HEAD，写入 |
| base_patch_hash | **PASS** | 写入 |
| stress_suite_hash / regular_suite_hash | **PASS** | 以 episode_ids 的 SHA256 摘要写入 |
| determinism_runs（含 champion_id, rank_key, *summary_hash） | **PASS** | 当 `det_result` 存在时写入 determinism_status 与 determinism_runs |
| timestamp_utc / timestamp | **PASS** | 成功与失败路径均有时间戳 |

**结论**：**PASS** — run_manifest 满足可回溯所需的 seed、git、base_patch、suite_hash、determinism 与时间信息。

---

## 五、附加检查（ranker / suite 报告顺序）

| 检查项 | 结果 | 说明 |
|--------|------|------|
| ranker aggregate_suite 的 episode 顺序 | **PASS** | `simulation/d1/ranker.py` 第 62 行：`for eid in sorted(paths.keys())`，聚合顺序固定 |
| rank_candidates_dual_channel 的 candidate 顺序 | **PASS** | 由调用方传入的 `candidate_results` 顺序决定；主流程从 `candidates.jsonl` 顺序读取，LHS 与固定组顺序由 seed 决定，一致 |
| _discover_candidate_results 目录遍历 | **PASS** | `for sub in sorted(run_dir.iterdir())`，发现 candidate 时使用 sorted |

---

## 六、汇总

| 类别 | 结果 | 条数 |
|------|------|------|
| **PASS** | 通过 | 9 项全部通过 |
| **WARNING** | 建议加固 | 2（suite_id 含时间戳；_deep_merge 为浅合并） |
| **FAIL** | 未通过 | 0 |

---

## 七、结论与建议

- **当前结论**：在“指纹仅依赖 rank_report 的 champion stress/regular summary、且不哈希 suite_report”的前提下，**确定性链路、双通道隔离、指纹与输出层**均满足军工级验收要求，**无 FAIL 项**。
- **建议**：
  1. **suite_id**：若未来将 suite_report 或 suite_id 纳入任何哈希/摘要，改为基于 patch + episode 列表的确定性 ID，避免使用 `datetime.now()`。
  2. **_deep_merge**：若后续对 effective_patch 做嵌套 in-place 修改，改为深拷贝或显式深合并，避免写穿到 base_patch。
  3. 在 CI 或发布前跑一次 `--dual-channel --determinism-check 3`，用实际多轮结果验证无随机性泄漏与顺序敏感性。

---

## 八、Post-Audit 收口加固（已落实）

| WARNING | 加固方式 | 状态 |
|---------|----------|------|
| suite_id 使用 datetime | `run_sim_suite.py`：suite_id 改为基于 episode 列表的确定性哈希 `f"{patch_stem}_{suite_hash[:12]}"`，移除对 `datetime.now()` 的依赖 | ✅ 已落实 |
| _deep_merge 浅合并 | `run_d1_tournament.py`：`_deep_merge` 使用 `copy.deepcopy(base)` 再合并 override，避免嵌套修改写穿 base | ✅ 已落实 |

**报告版本**：baseline_audit（与 d1_dual_channel_v1 冻结对齐）

---

*本报告为静态结构审计，不替代多轮 determinism 实测。*
