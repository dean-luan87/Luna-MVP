# D1 军工级结构图 — 可量产的性格生成工厂

**版本**：v1.0（与 D1_RISK_PHYSICS_POLICY v1.0、audit_report baseline 对齐）  
**定位**：双通道 + Stress Gate + Determinism 架构的层级与数据流说明，可直接用于技术白皮书或投资人 PPT。

---

## 一、五层架构总览

```
                    ┌─────────────────────────────────────────────────────────┐
                    │                   Evidence Layer                         │
                    │  run_manifest · personality_profile · determinism_runs   │
                    └───────────────────────────┬─────────────────────────────┘
                                                │ 仅 determinism PASS 时写入
                    ┌───────────────────────────▼─────────────────────────────┐
                    │                Determinism Layer                        │
                    │  N 次指纹一致 → PASS；任一次不一致 → 拒绝产出冠军        │
                    └───────────────────────────┬─────────────────────────────┘
                                                │ 指纹：champion_id, rank_key, summary_hash
                    ┌───────────────────────────▼─────────────────────────────┐
                    │                 Ranking Layer                           │
                    │  L1 early_gain↑ → L2 guarded_tail_ratio↓ → L3 vol↓     │
                    └───────────────────────────┬─────────────────────────────┘
                                                │ 仅 Gate PASS 的候选参与排序
                    ┌───────────────────────────▼─────────────────────────────┐
                    │                Stress Gate Layer                        │
                    │  guardian_discipline PASS · high_risk_frames_count > 0  │
                    │  （early_gain 不参与门禁）                               │
                    └───────────────────────────┬─────────────────────────────┘
                                                │ 双通道分别跑 suite
                    ┌───────────────────────────▼─────────────────────────────┐
                    │                 Physics Layer                           │
                    │  Stress: risk_scale=5  │  Regular: risk_scale=1         │
                    │  effective_patch.stress.json · effective_patch.regular  │
                    └─────────────────────────────────────────────────────────┘
```

---

## 二、各层职责与约束

### 1. Physics Layer（物理层）

| 项目 | 说明 |
|------|------|
| **输入** | base patch（stress / regular 各一份）+ candidate patch（仅 weights.* + metadata 白名单） |
| **输出** | 每候选两份 effective_patch：`effective_patch.stress.json`、`effective_patch.regular.json` |
| **约束** | risk_scale_factor 仅由 base 注入（Stress=5，Regular=1）；候选禁止含 smoothing.* / risk_scale_factor |
| **合并方式** | `_deep_merge(base, candidate)`，对 base 做 deepcopy，避免写穿 |

**要点**：双通道物理完全隔离，无交叉污染；effective_patch 为确定性合并结果，不依赖时间或环境。

---

### 2. Stress Gate Layer（安全门禁层）

| 项目 | 说明 |
|------|------|
| **输入** | 每个候选的 stress 通道 suite 结果（scorecards 聚合后的 stress_scorecard） |
| **判定** | ① guardian_discipline.status == "PASS"（exit_latency_p95 ≤ 6, hysteresis_efficiency ≥ 0.90）<br>② high_risk_frames_count > 0 |
| **输出** | PASS → 进入 Ranking；REJECTED → 淘汰，且带 reasons（可审计） |
| **原则** | Gate 与 Rank 解耦；**early_gain 不参与门禁**，仅参与排序 |

**要点**：安全不被性能绑架；任一 REJECT 均有明确 reason code。

---

### 3. Ranking Layer（排序层）

| 项目 | 说明 |
|------|------|
| **输入** | 通过 Stress Gate 的候选的 stress_scorecard + regular_scorecard |
| **排序键** | `rank_key = (early_gain_mean, -guarded_tail_ratio_mean, -volatility_mean)`，降序 |
| **稳定性** | 键为 tuple of float，无 dict/set；Python sort 稳定 |
| **输出** | 冠军 = ranked[0]；rank_key 持久化到 rank_report，供 Determinism 比对 |

**要点**：性能只在「安全过关」的候选之间比较；排序键结构固定、可复现。

---

### 4. Determinism Layer（确定性校验层）

| 项目 | 说明 |
|------|------|
| **触发** | `--determinism-check N`（N>1）且双通道时 |
| **行为** | 第 1 次为主流程 run_dir；第 2..N 次为 `run_dir/determinism_pass_*`，各跑一次完整 D1 |
| **指纹** | champion_id、rank_key、stress_summary_hash、regular_summary_hash（仅稳定字段，sort_keys=True） |
| **结果** | 全部一致 → PASS，允许写 personality_profile / champion_bundle；任一次不一致 → NON_DETERMINISTIC_EVOLUTION，仅写 run_manifest，拒绝产出冠军人格 |

**要点**：同一输入不得产生多种冠军；随机性完全受 seed 控制；排序稳定。

---

### 5. Evidence Layer（证据链层）

| 项目 | 说明 |
|------|------|
| **run_manifest.json** | seed, git_commit, base_patch_hash, stress_suite_hash, regular_suite_hash, timestamp；若做 determinism 则含 determinism_status、determinism_runs |
| **personality_profile.json / .md** | 冠军的 stress_channel / regular_channel 指标、guardian_discipline、suite_manifest；**仅 determinism PASS 或未开校验时写入** |
| **champion_bundle** | 冠军 patch、代表性 episode 的 scorecard / gate_result；同上，仅 PASS 时产出 |

**要点**：可追溯、可审计、可拒绝；证据链完整，无「偶然冠军」。

---

## 三、数据流简图（双通道 + Determinism）

```
  candidates (LHS + baseline/agg/cons)
           │
           ▼
  ┌────────────────────────────────────┐
  │ Physics: stress_base + candidate   │──► effective_patch.stress.json
  │         regular_base + candidate   │──► effective_patch.regular.json
  └────────────────────────────────────┘
           │
           ▼
  run_sim_suite (stress)  ──► suite_report.stress.json
  run_sim_suite (regular) ──► suite_report.regular.json
           │
           ▼
  ┌────────────────────────────────────┐
  │ Stress Gate (per candidate)       │──► REJECTED + reasons 或 PASS
  └────────────────────────────────────┘
           │ 仅 PASS
           ▼
  ┌────────────────────────────────────┐
  │ Ranking: rank_key 排序             │──► champion, rank_report.json
  └────────────────────────────────────┘
           │
           ▼
  ┌────────────────────────────────────┐
  │ Determinism: 再跑 N-1 次，比指纹   │──► PASS 或 NON_DETERMINISTIC_EVOLUTION
  └────────────────────────────────────┘
           │ 仅 PASS
           ▼
  ┌────────────────────────────────────┐
  │ Evidence: run_manifest,            │
  │           personality_profile,     │
  │           champion_bundle          │
  └────────────────────────────────────┘
```

---

## 四、与「实验级」的差异（一句话对照）

| 维度 | 实验级 | 当前 D1 军工级 |
|------|--------|----------------|
| 安全与性能 | early_gain 可能一票否决或一票通过 | Gate 与 Rank 解耦，安全门禁不含 early_gain |
| 冠军唯一性 | 同一输入可能不同 run 得到不同冠军 | N 次指纹一致才产出冠军，否则拒绝 |
| 证据 | 仅有 rank_report | run_manifest + personality_profile + determinism_runs |
| 可追溯 | 依赖人工记录 | seed / git / base_patch_hash / suite_hash 全记录 |
| 确定性 | 未显式保证 | suite_id 确定性、_deep_merge 深拷贝、指纹仅稳定字段 |

---

## 五、剪彩与冻结建议

1. **剪彩**：跑通一次  
   `--dual-channel --determinism-check 3`  
   确认 personality_profile.json 生成、run_manifest.json 含 determinism_status=PASS、三次指纹一致。

2. **冻结**：  
   - 打 git tag（如 `d1_dual_channel_v1`）  
   - `docs/D1_RISK_PHYSICS_POLICY.md` 标为 v1.0  
   - `docs/audit_report.md` 标为 baseline_audit  

当前 D1 已具备**可重复、可审计、可拒绝、可回溯、可解释**的演化内核，可作为基准的「可量产性格生成工厂」版本。

---

*本文档为 D1 双通道 + Determinism 架构的正式结构说明，与 D1_RISK_PHYSICS_POLICY、audit_report 共同构成军工级基线。*
