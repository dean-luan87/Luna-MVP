# Phase 3：Baseline 为什么一直赢 —— 诊断与下一步

## 结论摘要

- **Determinism 与物理机制已闭环**：Phase 2 可交付链健康；漂移根因是「输入集合不一致」已修复。
- **当前问题不是 bug，是结构性问题**：baseline 在现有排序与候选空间下就是最优；要突破需要「优化」而非「排错」。

---

## 一、从 C1 rank_report 看 baseline 为什么赢

以 `outputs/d1_runs/phase2_production_lock/20260216065530/rank_report.json` 为例。

### 1. rank_key 规则

- 先过 Stress 安全门禁，再按词典序：
  - **L1**：Stress `early_gain_weighted_mean` ↑（越大越好）
  - **L2**：Regular `guarded_ratio_delta_mean` ↓（越小越好）
  - **L3**：Regular `volatility_mean` ↓（越小越好）

### 2. 实际数据

- **Stress 通道（40 pulse episodes）**：所有 30 个 patch（baseline + conservative + 27 个 LHS 候选）的 stress 指标**完全一致**：
  - `early_gain_weighted_mean` = 2.8593
  - `volatility_mean` = 0.0355
  - `guarded_ratio_delta_mean` = 0.5568
  - `stress_high_risk_frames_count` = 1430
- **Regular 通道（12 episodes）**：只有这里出现分化：
  - baseline / conservative / 部分候选：`volatility_mean` = 0，`guarded_ratio_delta_mean` = 0 → **rank_key = (2.8593, 0, 0)**
  - 其余候选：`volatility_mean` = 0.0022～0.023 → **rank_key = (2.8593, 0, -vol)**，在 L3 上劣于 baseline

因此：**L1 上无人超过 baseline（大家 early_gain 相同），L2/L3 上 baseline 为 0/0 最优，故 baseline 冠军。**

### 3. 含义

- **不是「多目标排序压制了更好的候选」**：当前数据下没有任何候选在 stress 上比 baseline 更好。
- **是「候选空间在 stress 上没有产生差异」**：在 40-clip pulse + 当前 LHS 与权重边界下，effective patch（base + candidate）在 stress 上的表现与 baseline 完全一致；差异只体现在 regular 的 volatility。
- 因此：要判断下一步是「放宽/改选拔规则」还是「扩大候选空间」，需要先做**单指标冠军实验**。

---

## 二、建议的下一步（按顺序）

### 第一件：单指标冠军榜（仅按 early_gain 排序）

- **目的**：区分是「排序规则压制变异」还是「候选空间本身没突破 baseline」。
- **做法**：使用 `--rank-by early_gain_only`，仅按 L1 Stress early_gain 排序，不看 L2/L3；跑 n=80。
- **解读**：
  - 若 **baseline 仍排第一（或与别人并列第一）**：说明在当前候选空间下，无人能在 early_gain 上超越 baseline，问题在**搜索空间/采样**（例如需要 hyper 桶、更大 cap 或 CMA-ES）。
  - 若 **有候选在仅 early_gain 下超过 baseline**：说明是词典序的 L2/L3 把「更激进」的候选压下去了，可再考虑是否放宽或调整排序规则。

**命令示例**（单指标冠军，n=80）：

```bash
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 tools/run_d1_tournament.py \
  --dual-channel --determinism-check 1 \
  --rank-by early_gain_only \
  --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
  --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
  --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
  --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
  --regular-suite library_store/v1.1/golden_stress_v2 \
  --n-candidates 80 --seed 42 \
  --out-dir outputs/d1_runs/phase2_production_lock --mode recompute
```

### 第二件：把 hyper 桶真正放出来

- **现状**：已有 10% hyper 桶，RISK_WEIGHT_KEYS 上界 cap=1.3（约 ×1.5 default）。
- **建议**：可尝试将 hyper 上界提到 **×1.4～×1.5**（或 cap 1.4/1.5），让「越界一小步」的变异更明显；hyper 仍须过 **conservative sustain gate**，避免只放脉冲不过军检。
- **目的**：在 baseline 线性邻域外引入**结构性变异**，看是否能在 stress 上出现 early_gain 差异。

### 第三件：Phase 3 优化方向（宏观）

- 当前系统已能稳定触发 Guarded、determinism 可交付；问题从「能不能亮」变成「谁更亮」。
- 若 baseline 是手调平衡点，**纯随机 LHS 很难超越**；可考虑：
  - 用 **CMA-ES 或贝叶斯优化** 替代/补充 LHS；
  - 或对 early_gain 敏感权重做**定向搜索**（梯度方向或局部放大）。
- 这类工作属于 **Phase 3 性能边界优化**，而不是继续修 determinism 或物理机制。

---

## 三、A/B 判死结果（军工式排障）

用 `tools/diagnose_early_gain_ab.py <run_dir>` 对 run 20260216071808 执行：

- **Step 1**：stress_responsive 报告存在（baseline / d1_candidate_000 均有）。
- **Step 2**：baseline vs d1_candidate_000 同集 scorecard 的 `first_guarded` / `early_gain_weighted` / `high_risk_seq_count` **完全一致**（前 5 集均同）。
- **Step 3**：从 replay 复算 first_guarded：baseline 的 candidate_replay 与 d1_candidate_000 的 candidate_replay 在首集 **first_guarded seq 均为 3961**。

**结论：A) 真实平台期**。权重扰动（LHS）未改变「进入 Guarded 的帧」；early_gain 链路正确，但**候选空间对 early_gain 不敏感**。下一步应把搜索变量切到**时间响应**旋钮（smoothing.alpha / peak_hold / view_conf_gate），见下节。

---

## 四、Phase 3 时间响应搜索（Step A：只开 alpha）

变量选错物理层级：当前搜的是「风险幅度」，DANGER 触发是「时间响应」问题。只动**时间常数类**参数。

### 已实现（Step A 最小干预）

- **smoothing.alpha** 仅在 **stress_responsive** 下可被候选覆盖，已收窄为 **[0.55, 0.70]**（拉满有效率）；conservative/regular 不合并 alpha（`_candidate_patch_for_conservative` 剥离）。
- **candidate_generator**：非 baseline 候选默认带 `smoothing.alpha` 采样（`include_responsive_alpha=True`）；baseline 仍为空 patch。

### Step A 命令（n=40，单指标冠军）

```bash
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 tools/run_d1_tournament.py \
  --dual-channel --determinism-check 1 \
  --rank-by early_gain_only \
  --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
  --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
  --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
  --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
  --regular-suite library_store/v1.1/golden_stress_v2 \
  --n-candidates 40 --seed 42 \
  --out-dir outputs/d1_runs/phase2_production_lock --mode recompute
```

### 成功标志与扫描

- **诊断**：`python3 tools/diagnose_early_gain_ab.py <run_dir>` 看同集 baseline vs 候选 first_guarded 是否分化。
- **扫“早于 baseline”的赢家**：`python3 tools/scan_earliest_first_guarded.py <run_dir>` 从 replay 读各 patch 的「最早 first_guarded seq」，找 **first_guarded_seq < 3961**（或相对 baseline 更早）的 patch。  
  - Run 20260216073053 扫描结果：**d1_candidate_022、d1_candidate_031** 的 earliest first_guarded_seq=**1773**，baseline/多数=1774 → **已有正向梯度，Phase 3 可育种**。

### 收窄 alpha 后再跑（phase3_alpha_band，n=60）

alpha 已收窄为 [0.55, 0.70]，更多候选能点火，便于在「点火人群」里按早几帧分化。命令：

```bash
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 tools/run_d1_tournament.py \
  --dual-channel --determinism-check 1 \
  --rank-by early_gain_only \
  --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
  --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
  --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
  --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
  --regular-suite library_store/v1.1/golden_stress_v2 \
  --n-candidates 60 --seed 42 \
  --out-dir outputs/d1_runs/phase3_alpha_band --mode recompute
```

跑完后用 `scan_earliest_first_guarded.py <run_dir>` 看是否有更多 first_guarded_seq 早于 baseline 的候选。phase3_alpha_band 一轮（20260216073911）结果：55/60 点火，但 earliest 全员 1774 → **alpha 只改“能否跟上”，不改“峰值在哪一帧”**；需 Step B 改峰值记忆结构。

### Step B：峰值记忆结构（peak_hold_frames + peak_decay）

目标：让 EMA 在峰值**前 1～3 帧**被拉高，从而出现 first_guarded **早于 1774**（哪怕早 1 帧即进入梯度优化阶段）。

- **已实现**：仅在 stress_responsive 候选中增加  
  **smoothing.peak_hold_frames ∈ [3, 8]**、**smoothing.peak_decay ∈ [0.88, 0.98]**；conservative/regular 不合并这两项。
- **成功信号**：`scan_earliest_first_guarded.py <run_dir>` 输出中出现 **earliest first_guarded_seq < 1774**（至少一个候选）。

**Step B 命令（n=60，out-dir phase3_peakhold）**：

```bash
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 tools/run_d1_tournament.py \
  --dual-channel --determinism-check 1 \
  --rank-by early_gain_only \
  --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
  --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
  --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
  --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
  --regular-suite library_store/v1.1/golden_stress_v2 \
  --n-candidates 60 --seed 42 \
  --out-dir outputs/d1_runs/phase3_peakhold --mode recompute
```

跑完后执行（将 `RUN_ID` 换成实际时间戳目录）：

```bash
python3 tools/scan_earliest_first_guarded.py outputs/d1_runs/phase3_peakhold/RUN_ID
```

若出现 **first_guarded_seq=1773**（或更小）的候选，Phase 3 即从「点火成功」进入「梯度优化／育种」阶段。

---

## 六、Phase 3 形态选择与结构确认（run 20260216074801）

### 结果：baseline 被结构性超越

- **Champion: d1_candidate_001**，early_gain_weighted_mean=**3.6131**（baseline 2.8593）。
- 60/60 通过，双 stress Gate 下稳定；early_gain 不再平台期，**peak_hold/decay 是相变旋钮**。

### 前 5 名 smoothing 结构（effective_patch.stress_responsive）

| 排名 | patch_id         | alpha   | peak_hold_frames | peak_decay | early_gain_mean |
|------|------------------|--------|------------------|------------|-----------------|
| 1    | d1_candidate_001 | 0.6133 | **3**            | **0.8894** | 3.6131          |
| 2    | d1_candidate_022 | 0.6527 | **3**            | **0.9029** | 3.6131          |
| 3    | baseline         | 0.6    | 3                | 0.92       | 2.8593          |
| 4    | d1_candidate_000 | 0.6515 | 7                | 0.8887     | 2.8593          |
| 5    | d1_candidate_002 | 0.5849 | 7                | 0.8827     | 2.8593          |

**结论（结构确认）**：

- 冠军**没有**拉长 peak_hold（均为 3，与 baseline 一致）；第 4、5 名 peak_hold=7 反而只得到 baseline 级 early_gain。
- 赢家共性：**alpha 略升（0.61～0.65）** + **peak_decay 略降（0.88～0.90，即略快衰减）**。  
→ 本轮进化主轴是 **alpha × peak_decay 的协同**，不是 peak_hold 拉长。

### 下一步：锁定进化轴 + 稳定性检查

1. **不再以 earliest 单帧为主**：评价从「谁最早触发」转为「谁在高压段内 early_gain 持续更优」。
2. **收缩到单轴、分阶段局部搜索**（exploitation）：
   - 阶段一：**peak_decay ∈ [0.88, 0.92]**，peak_hold=3，alpha=0.6；
   - 阶段二：**alpha ∈ [0.58, 0.68]**，peak_decay 固定冠军值，peak_hold=3；
   - 阶段三：视结果再微调或加 view_conf_gate。
3. **稳定性检查（必做）**：见下节「完整性 L1+L2+L3 回归验证」。

### 完整性 L1+L2+L3 回归验证（人格体检）

单指标优化易产生「极端响应型」；在继续挖 stress 深度前，必须先验证**梯度是否可持续、是否在安全边界内**。

**命令**（与 phase3_peakhold 同参数，仅去掉 `--rank-by early_gain_only`）：

```bash
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 tools/run_d1_tournament.py \
  --dual-channel --determinism-check 1 \
  --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
  --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
  --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
  --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
  --regular-suite library_store/v1.1/golden_stress_v2 \
  --n-candidates 60 --seed 42 \
  --out-dir outputs/d1_runs/phase3_full_rank \
  --mode recompute
```

**跑完后看三件事**：

1. **Champion 是否仍为 d1_candidate_001**（或同等级 alpha×decay 型）。
2. **L2/L3 是否明显恶化**：冠军的 `volatility_mean`、`guarded_ratio_delta_mean` 是否仍在可接受范围（与 baseline 量级可比）。
3. **是否有人在 regular 上异常「过度 Guarded」**（排名或报告里 regular 指标是否出现极端值）。

**三种可能结局**：

| 结局 | 含义 | 下一步 |
|------|------|--------|
| **情况 1**：冠军不变，L2/L3 正常 | alpha×decay 优化是「真实进化」，非病态 | 可进入局部精调（peak_decay / alpha 单轴） |
| **情况 2**：冠军换回 baseline | 当前优解是 stress 专用人格，不适合常态 | 引入轻微 regular 惩罚或门控，而非继续放大 stress |
| **情况 3**：新候选胜出 | 多指标排序暴露更优平衡点 | 以新冠军为锚点，再决定是否精调或加门控 |

跑完把 **champion_id**、冠军的 **stress_metrics** 与 **regular_metrics**（或 rank_report 前几行）贴出，即可判断属哪种情况，再决定是否进入精调或引入新门控。

### phase3_full_rank 一轮结果（run 20260216075635）

**结构（比「谁赢了」更重要）**：

- **L1**：022 = 001（stress 上同分，early_gain=3.6131，high_risk_frames=1130）。
- **L2**：都正常（guarded_ratio_delta_mean=0.0）。
- **L3**：022 的 regular volatility **明显更低**（0.0022 vs 001 的 0.0143）。
- **词典序** → 022 胜出。

这不是随机波动，而是典型的 **「同等应激能力下，稳态控制更优」** 的解。022 不是更激进，而是 **更干净**；这才是值得继续投资的方向。

**022 vs 001 的 stress_responsive smoothing**（`effective_patch.stress_responsive.json`）：

| patch_id         | alpha   | peak_hold_frames | peak_decay |
|------------------|--------|------------------|------------|
| d1_candidate_022 | 0.6527 | 3                | 0.9029     |
| d1_candidate_001 | 0.6133 | 3                | 0.8894     |

022 略高 alpha、略高 peak_decay；权重组合不同，在 regular 上 volatility 更低。

**当前真正的突破**：不是 022 赢了，而是已经看到 (1) stress 梯度存在，(2) 多指标排序开始产生真实结构分化，(3) 系统进入「平衡型人格进化阶段」。Phase 3 从验证链路转为**优化问题**，是一条不同的路。

---

### 为什么暂不精调 022：先验证地形

当前结果是 **60-candidate、固定 seed** 下的单次抽样。尚不知道 022 是否对 **seed / 候选规模 / episode 组合 / LHS 抽样分布** 敏感。在进化系统里，过早围绕一个局部峰精调，容易锁进假高地。  
精调是 **exploitation**，只有在确认「这个峰不是噪声」之后才值得做。正确顺序：**先做稳定性扩容验证，再决定是否 exploit 022**。

---

## 进化验证阶段：执行框架

目标：**让数据决定方向**。不提前猜测，不提前精调。跑完只分析一张表。

### 里程碑（已完成）

- **Phase 1**：打破 baseline 不可动
- **Phase 2**：锁 determinism
- **Phase 3**：证明结构可分化（stress 梯度存在、多指标产生真实分化）

已从「系统验证」进入**系统优化**。022 赢在「stress 不输 + regular 更稳」，是一种**鲁棒人格**；若在 seed 扩展里稳定存在，即找到**平衡型人格的收敛方向**，比单纯 early_gain 更有意义。

---

### 第一阶段：Seed 稳定性验证（核心）

**已有**：seed 42 → Champion = 022（run 20260216075635）

**接下来只做两件事**：跑 **seed 123**、**seed 777**。参数完全不动（区间、smoothing 搜索、L1+L2+L3、suite 都不改），只改 `--seed`。

**命令**（仅改 `--seed`）：

```bash
# seed 123
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 tools/run_d1_tournament.py \
  --dual-channel --determinism-check 1 \
  --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
  --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
  --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
  --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
  --regular-suite library_store/v1.1/golden_stress_v2 \
  --n-candidates 60 --seed 123 \
  --out-dir outputs/d1_runs/phase3_full_rank --mode recompute

# seed 777（同上，仅改 --seed 777）
```

**跑完后每个 run 只抽 4 个指标**（不要看一堆别的）：

1. **champion_id**
2. **champion 的 regular_volatility_mean**
3. **001 的 regular_volatility_mean**
4. **022 的 regular_volatility_mean**

核心问题只有一个：**022 的低 volatility 是结构优势，还是 seed 偶然？**

**汇总表**（三个 run 跑完后执行，将后两个路径换成 seed 123/777 实际生成的 run 目录名，贴出这一张表即可）：

```bash
python3 tools/run_d1_seed_stability_summary.py \
  outputs/d1_runs/phase3_full_rank/20260216075635 \
  outputs/d1_runs/phase3_full_rank/<timestamp_seed123> \
  outputs/d1_runs/phase3_full_rank/<timestamp_seed777> \
  --labels seed42 seed123 seed777
```

输出为：每个 run 一行，含 run、champion_id、champion_vol、vol_001、vol_022、top3；**只分析这一张表**。

---

### 三种可能结果（只看上表）

| 情况 | 现象 | 含义 | 下一步 |
|------|------|------|--------|
| **A** | 022 在三个 seed 里都进 Top3 | 022 不是偶然；smoothing 结构形成「低 volatility 优势」 | **进入 exploit 阶段**（局部精调） |
| **B** | 022 有时赢，有时掉出 Top3 | 022 是局部峰；搜索空间还没形成稳定吸引子 | 扩大 n，或扩大 alpha/decay 区间，或改 LHS 分布 |
| **C** | 出现新结构（如 017）：stress 同分、volatility 更低 | 峰还没被完全发现 | 不围绕 022 精调，**重塑搜索分布** |

---

### 第二阶段（只有 A 成立时才做）

若 022 稳定出现，才做**局部精调**（exploitation）：

- 固定 peak_hold=3
- alpha ∈ [0.62, 0.68]
- peak_decay ∈ [0.89, 0.91]

**现在还不是时候**，等第一阶段一张表出来再定。

---

### 执行顺序

1. 跑 seed 123  
2. 跑 seed 777  
3. 用 `tools/run_d1_seed_stability_summary.py` 把三个 run 的 **Top3 + volatility 表** 打出来，贴到文档或此处  
4. 根据上表判断 A/B/C，再决定方向  

---

### Step 2（次级，算力允许时）：episode 扩容

022 胜出核心来自 L3。若算力允许，将 regular-suite 扩到更大 episode 集，确认低 volatility 是普适现象，而非对当前 12 集的偶然适配。

---

## Phase3 收敛式采样（PHASE3_CONVERGENT_SAMPLER_v1）

Seed 稳定性验证结果为**情况 B**（022 局部峰、未形成吸引子）时，采用**重塑采样分布**：从均匀 LHS 改为以 022 类结构为中心的收敛式混合分布，目标推进到「可收敛的吸引子」。

### 判据升级：参数盆地稳定，不看 patch_id

**patch_id 是随机样本编号**，跨 seed 不重合是常态。真正需要验证的是：冠军/Top3 是否稳定落在**同一参数盆地**（alpha/decay 区间），而不是同一个 ID。

用 `tools/summarize_topk_basin.py` 做**跨 run TopK 参数盆地对齐**：

```bash
python3 tools/summarize_topk_basin.py \
  outputs/d1_runs/phase3_convergent/20260224020809 \
  outputs/d1_runs/phase3_convergent/20260224021402 \
  outputs/d1_runs/phase3_convergent/20260224021720 \
  --topk 10 --out outputs/d1_runs/phase3_convergent/basin_summary.json \
  --labels seed42 seed123 seed777
```

**判据**：若三次 run 的 Top10 落在**同一小区间**（如 alpha [0.62,0.66]、decay [0.885,0.905]）→ 形成吸引子；若区间漂移很大 → 再调 exploit_ratio/方差才有意义。不再以「patch_id 重合」判定成功。

### 目标与成功判据（升级后）

1. **参数盆地收敛**：Top10 的 alpha/decay 在三 seed 下落在相近区间（basin_summary 一眼可见）。
2. **冠军稳定性**：champion 的 regular_volatility_mean 维持低位（<0.005）。
3. **冠军来源**：若长期来自 explore → 中心点偏了；若来自 exploit 且盆地收敛 → 进入 exploit 阶段。
4. **不破坏 L1**：stress early_gain 仍有梯度可选。

### 策略：固定 peak_hold + 混合分布

- **peak_hold_frames 固定为 3**（已验证拉长不带来优势）。
- **Exploit 桶（70%）**：围绕有效区集中采样
  - alpha：均值 0.635，std 0.02，截断 [0.60, 0.68]
  - peak_decay：均值 0.895，std 0.01，截断 [0.88, 0.92]
- **Explore 桶（30%）**：稍大范围探索
  - alpha：均匀 [0.58, 0.72]
  - peak_decay：均匀 [0.87, 0.93]

### 命令（单 seed 先验证盆地）

```bash
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 tools/run_d1_tournament.py \
  --dual-channel --determinism-check 1 \
  --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
  --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
  --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
  --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
  --regular-suite library_store/v1.1/golden_stress_v2 \
  --n-candidates 80 --seed 42 \
  --out-dir outputs/d1_runs/phase3_convergent --mode recompute \
  --phase3-mode convergent \
  --converge-exploit-ratio 0.7 \
  --converge-peak-hold-fixed 3 \
  --converge-alpha-mean 0.635 --converge-alpha-std 0.02 --converge-alpha-min 0.60 --converge-alpha-max 0.68 \
  --converge-decay-mean 0.895 --converge-decay-std 0.01 --converge-decay-min 0.88 --converge-decay-max 0.92 \
  --converge-explore-alpha-min 0.58 --converge-explore-alpha-max 0.72 \
  --converge-explore-decay-min 0.87 --converge-explore-decay-max 0.93
```

### Seed 稳定性三连

跑 seed 42 / 123 / 777，用汇总脚本打表（跑完 seed 123、777 后，将后两个路径替换为实际 run 目录名）：

```bash
# 仅 seed42（当前已跑完）
python3 tools/run_d1_seed_stability_summary.py \
  outputs/d1_runs/phase3_convergent/20260224020809 \
  --labels seed42

# 三 run 都跑完后（将后两个路径换成 seed123、777 的实际 run 目录名）
python3 tools/run_d1_seed_stability_summary.py \
  outputs/d1_runs/phase3_convergent/20260224020809 \
  outputs/d1_runs/phase3_convergent/20260224XXXXXX \
  outputs/d1_runs/phase3_convergent/20260224YYYYYY \
  --labels seed42 seed123 seed777
```

**判定**：以**盆地稳定**为准；patch_id 重合为参考，不纠结。

### 下一轮：exploit_ratio 0.85（r085）

把 `--converge-exploit-ratio 0.7` 改为 `0.85`，`--out-dir` 改为 `phase3_convergent_r085`，其余不动：

```bash
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 tools/run_d1_tournament.py \
  --dual-channel --determinism-check 1 \
  --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
  --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
  --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
  --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
  --regular-suite library_store/v1.1/golden_stress_v2 \
  --n-candidates 80 --seed 42 \
  --out-dir outputs/d1_runs/phase3_convergent_r085 --mode recompute \
  --phase3-mode convergent \
  --converge-exploit-ratio 0.85 \
  --converge-peak-hold-fixed 3 \
  --converge-alpha-mean 0.635 --converge-alpha-std 0.02 --converge-alpha-min 0.60 --converge-alpha-max 0.68 \
  --converge-decay-mean 0.895 --converge-decay-std 0.01 --converge-decay-min 0.88 --converge-decay-max 0.92 \
  --converge-explore-alpha-min 0.58 --converge-explore-alpha-max 0.72 \
  --converge-explore-decay-min 0.87 --converge-explore-decay-max 0.93
```

seed 123、777 仅改 `--seed 123` / `--seed 777`，`--out-dir` 保持不变（每次会建新时间戳子目录）。

### 固定候选集验证（--candidates-file）

区分「采样波动」与「评估稳定性」：先跑 seed 42 生成 candidates，再跑 seed 123/777 时复用同一候选集：

```bash
# 1) seed 42 正常跑（生成 candidates）
# 2) seed 123 复用 seed42 的 candidates：
python3 tools/run_d1_tournament.py ... --seed 123 \
  --candidates-file outputs/d1_runs/phase3_convergent_r085/<seed42_run>/candidates.jsonl
```

`patch_path` 仍指向源 run 的 candidates 目录，源 run 需保留。

### 调参顺序（按优先级）

1. **仍不收敛**：exploit_ratio 0.7 → 0.85（更强收敛）；仍不行再降 0.6。
2. **再调方差**：alpha_std 0.02 → 0.015；decay_std 0.01 → 0.007。
3. **最后才扩大 explore**：explore_alpha [0.56, 0.74]，explore_decay [0.86, 0.94]。

### Convergent v2 配方（r085 后续）

**目标**：让冠军从「偶发 explore 极值」逐步转为「稳定 exploit 盆地」，盆地收窄到可控区间。  
**策略**：先移中心 → 再收方差。

#### Step 1（m66）：移 exploit 中心到赢家附近

- **改动**：alpha_mean 0.635→**0.66**，decay_mean 0.895→**0.888**；std、边界、exploit_ratio 0.85、peak_hold 3 均不变。
- **脚本**：`tools/run_d1_r085_m66_seeds.sh [42|123|777|all]`
- **out-dir**：`outputs/d1_runs/phase3_convergent_r085_m66`

**判定口径（只看三条）**：

1. **Champion bucket**：冠军是否从 explore 转为 exploit（最关键）
2. **Top10 盆地**：alpha/decay 的 std 是否下降、是否更贴近 [0.65–0.68] × [0.88–0.90]
3. **regular volatility**：冠军 vol 是否仍低（<0.01 视为健康）

若 seed42/777 仍被 explore 抢冠军，但 exploit Top10 明显上移并缩窄 → 进入 Step 2。

#### Step 2（squeeze）：收方差，逼出稳定吸引子

在 Step 1 基础上：alpha_std 0.02→**0.015**，decay_std 0.01→**0.007**。

- **脚本**：`tools/run_d1_r085_squeezed_seeds.sh [42|123|777|all]`
- **out-dir**：`outputs/d1_runs/phase3_convergent_r085_m66_squeezed`

**成功标准**：

- 三 seed Top10 basin std 明显下降（alpha std < 0.02，decay std < 0.008）
- 冠军更多来自 exploit
- 排名结构更稳定（同盆地内比 L3 volatility）

#### Step 3（可选）：explore 制度化巡航

explore 收窄到赢家带：explore-alpha [0.68, 0.72]，explore-decay [0.865, 0.885]。建议在 Step 2 稳定 exploit 盆地后再做。

#### 最短执行路径

1. 先跑 Step1（m66）三 seed，n=80
2. 产出：seed stability 表（champion/vol/eg/top3）+ basin 对齐（Top10 alpha/decay 区间与 std、bucket 占比）
3. 若仍是 explore 冠军：立刻跑 Step2（squeeze）三 seed
4. Step2 若 exploit 冠军占多数且 basin 收窄 → 进入 exploit 微调阶段；否则考虑 Step3 的 explore 收窄巡航

---

### Phase3 Step3 GradualShift（5-seed 可验收方案）

**目标**：把 exploit 分布从「0.66/0.89 盆地」向「0.70/0.87 赢家带」渐进迁移，验证其能否成为稳定吸引子。  
**原则**：不一刀切；保留 20% explore 逃生通道；用 5 seeds 做稳定性判定；用 A/B/C 直接落下一步。

#### Step3-GradualShift 参数块

- **exploit_ratio** = 0.80
- **exploit**：alpha_mean 0.685, alpha_std 0.015；decay_mean 0.878, decay_std 0.007；peak_hold=3；bounds [0.64,0.72]×[0.86,0.90]
- **explore**：alpha [0.68, 0.72]，decay [0.865, 0.885]，peak_hold=3

#### 运行

```bash
./tools/run_d1_step3_gradualshift_seeds.sh all
```

Seeds：42, 123, 777, 888, 2024；n=80；out-dir：`outputs/d1_runs/phase3_step3_gradualshift`。

#### 汇总与验收

跑完后用 stability summary（含 bucket、top10、exploit_win_rate）：

```bash
python3 tools/run_d1_seed_stability_summary.py \
  outputs/d1_runs/phase3_step3_gradualshift/<run1> \
  outputs/d1_runs/phase3_step3_gradualshift/<run2> \
  ... \
  --labels seed42 seed123 seed777 seed888 seed2024 --topk 10
```

#### A/B/C 验收判据（写死下一步）

| 判定 | 条件 | 下一步 |
|------|------|--------|
| **A：迁移成功** | exploit 夺冠 ≥3/5 且 champion_eg≥4.1617 的 run ≥2/5 且 champion_vol p95<0.01 | Step4：alpha_mean→0.695, decay_mean→0.874, exploit_ratio→0.85，再跑 5 seeds |
| **B：部分成功** | top10 alpha_mean>0.69（盆地确实上移）但 exploit 冠军<3/5 | exploit_ratio 0.80→0.85，保持 explore 15%，再跑 5 seeds |
| **C：失败/回滚** | champion_vol 出现 >0.02 或 top10 alpha_mean≤0.68 或冠军结构完全散 | 回滚到 r085/m66 安全配置，开启第三轴（view_conf_gate/threshold）再谈 |

#### 交付物（每次 5-seed 结束）

1. 5-seed 汇总表（stability summary 输出）
2. top10 盆地统计（alpha/decay mean/std、bucket 占比）
3. 本轮判定 A/B/C + 下一步动作（写死）

---

### Phase3 Step5：交付冻结 vs 抬天花板

Step4 已将吸引子坐实（盆地 0.696/0.869、exploit 43/50、L1=4.1617、vol=0）。不再做泛优化，进入工程化：**Step5-A 冻结交付** 或 **Step5-B 抬天花板**。

#### Step5-A：交付冻结版（Production Candidate）

**目的**：将 Step4 配方固化为可交付人格，能复现、可上线灰度。

**原则**：冠军指标一致，而非冠军 ID 一致。不同 seed 抽样不同，只要 L1=4.1617、Vol=0、Fuse 正常，即视为工业级稳定。

**冻结参数**（`configs/personality/PHASE3_PRODUCTION_RECIPE_v1.json`，DO NOT TUNE WITHOUT VERSION BUMP）：

- **exploit**：alpha_mean 0.696, alpha_std 0.013；decay_mean 0.869, decay_std 0.004；peak_hold=3；bounds [0.65,0.73]×[0.86,0.88]
- **explore**：alpha [0.69, 0.72]，decay [0.865, 0.885]，peak_hold=3
- **exploit_ratio** = 0.85

**验收跑**：determinism-check **3**，3-seed（42/123/777）

```bash
./tools/run_d1_step5_freeze_seeds.sh all
```

**工业级验收（每 seed 4 项）**：

1. champion_eg ≥ 4.1617
2. champion_vol < 0.005
3. high_risk_frames_total > 0（无熔断）
4. guarded_frames_total > 0（无熔断）

汇总脚本：

```bash
python3 tools/run_d1_freeze_verify.py outputs/d1_runs/phase3_step5_freeze/<run1> <run2> <run3> --labels seed42 seed123 seed777
```

**冻结通过标准**：3/3 seeds 四项全过，且 Top10 alpha_mean ∈ [0.69, 0.70]。

---

#### Step5-B：抬天花板（二选一）

**路线 B1：Regular episode 扩容**

- 将 regular-suite 从 12 集扩到 30–50 集
- 新建 `library_store/v1.2/golden_regular_v3_50eps`
- 不改分布，只换 `--regular-suite`，再跑 5-seed

**路线 B2：第三轴 view_conf_gate**

- 在 stress_responsive 增加 `view_conf_gain`（默认 1.0）
- 修改 `a3/engine.py`：`raw_effective = raw * (0.5 + 0.5 * clamp01(view_conf * view_conf_gain))`
- exploit：view_conf_gain ~ N(1.20, 0.08)，clamp [1.0, 1.4]
- explore：view_conf_gain ∈ [1.25, 1.4]

---

#### 监控脚本（上线必备）

`tools/run_d1_nightly_regression.py`：最小可行 nightly 回归

- 输出：exploit_win_rate、champion_eg、champion_vol、top10 alpha_mean、guarded_ratio_delta
- RED：champion_eg < 4.0 或 champion_vol > 0.02
- YELLOW：exploit_win_rate < 0.5

---

### phase3_convergent 首轮盆地对齐结果（r=0.7）

三 run（20260224020809 / 20260224021402 / 20260224021720）Top10 合并统计：

- **alpha**：min=0.61 max=0.72 mean=0.646 std=0.029
- **decay**：min=0.87 max=0.91 mean=0.892 std=0.009
- **bucket**：exploit 20，explore 10

盆地已落在 alpha [0.61,0.72]、decay [0.87,0.91]；exploit 占比 2/3。下一轮 r085 看区间是否进一步收窄、冠军是否更多来自 exploit。

### 产物与回滚

- 每个 run 写 `sampling_plan.json`（参数范围、actual_stats、bucket 计数），便于复盘。
- 不传 `--phase3-mode` 时保持原 LHS 行为。
- patch metadata 写 `sampler=phase3_convergent_v1`、`bucket=exploit|explore`，可审计冠军来源。

---

复现前 5 名 smoothing 的命令（换 run_dir 即可）：

```bash
python3 -c "
import json
from pathlib import Path
run_dir = Path('outputs/d1_runs/phase3_peakhold/20260216074801')
d = json.load(open(run_dir / 'rank_report.json'))
for r in (d.get('ranked') or [])[:5]:
    pid = r.get('patch_id', '')
    eg = (r.get('stress_metrics') or {}).get('early_gain_weighted_mean')
    eff_path = run_dir / pid / 'effective_patch.stress_responsive.json'
    smooth = {k: v for k, v in json.load(open(eff_path)).items() if k.startswith('smoothing.')} if eff_path.is_file() else {}
    print(pid, smooth, 'early_gain=', eg)
"
```

---

## 五、关键结论（一句话）

- **Phase 2**：电源和军检电压已修好；可交付 determinism 链闭环。
- **当前**：问题不是物理、不是 determinism，也不是指标链路偷懒；是 **A) 真实平台期**：权重扰动对「何时进入 Guarded」不敏感。
- **Phase 3 现状**：已从「baseline 不可撼动」进入**结构分化阶段**（stress 梯度存在、多指标排序产生真实分化、平衡型人格进化）。022 代表「同等应激下稳态更干净」的解。
- **下一步（执行顺序）**：**先做 seed 扩展稳定性测试**（seed 42/123/777，不改区间与排序），汇总 Top 3 与 L3 volatility；确认 022 或同类结构稳定存在后，再决定是否精调 022、扩大 alpha/decay 搜索、或引入 view_conf_gate。暂不直接精调，避免锁进假高地。
