# D1 双通道物理政策（宪法）

本文档冻结 D1 双通道（Stress / Regular）的物理常数与排名规则，作为「战争演习 + 日常体验」育种系统的宪法。

---

## 一、为什么要双通道

| 通道 | 作用 | 比喻 |
|------|------|------|
| **Stress** | 保命门禁：在高压物理下是否仍过关、是否有 early_gain | 战争演习 |
| **Regular** | 体验排序：在日常物理下是否不过度保守、不抖 | 日常驾驶 |

先过生死门（Stress Gate），再比驾驶体验（Regular 指标）。不通过 Stress 的候选直接 L0 淘汰，不参与 L1/L2/L3 排序。

---

## 二、两通道物理常数

| 项目 | Stress Channel | Regular Channel |
|------|----------------|-----------------|
| **risk_scale_factor** | **5.0** | **1.0** |
| smoothing.* | 与 stress_v2_phys_v1 一致（peak_hold_frames=3, peak_decay=0.92, alpha_high=0.45, alpha_switch_at=0.85） | 同左 |

- 物理常数通过 **base physics patch** 注入，候选 patch **不允许**包含 `smoothing.*` 或 `risk_scale_factor`（Presence-Only Contract）。
- 候选仅搜索 **weights.*** 与 metadata 白名单；物理由 base patch 提供，不作为搜索维度。

---

## 三、排名规则（词典序）

| 层级 | 内容 | 说明 |
|------|------|------|
| **L0** | Stress 安全门禁 | 若 stress 下 high_risk_frames_count == 0 或 guardian_discipline FAIL，判为 FAIL，淘汰 |
| **L1** | Stress 指标 | stress.early_gain_mean 越大越好 |
| **L2** | Regular 指标 | regular.guarded_ratio_delta_mean 越小越好 |
| **L3** | Regular 指标 | regular.volatility_mean 越小越好 |

- **high_risk** 与 **early_gain** 必须基于 replay 中的 `risk_used_for_decision` 与 `threshold_safe_to_caution`，不得用固定 0.38 或 complexity_delta 推导。
- 任何统计不得读取原始 risk_raw 或 records 内部字段；只基于 replay 行为字段（control_mode / decision / risk_used_for_decision / high_risk / threshold_*）。
- guardian_discipline 仅作为 Stress Gate 的硬门槛（Pass/Fail），不进入加权项，避免 Goodhart。

---

## 四、Fail 的硬门槛

- **L0 淘汰**：PATCH_SCHEMA_VIOLATION（候选含 smoothing.* 或 risk_scale_factor）、missing_suite_report、Stress Gate 未过（overall_fail 或 high_risk_frames_count == 0 或 guardian 未过）。
- 通过 L0 的候选按 L1 → L2 → L3 词典序排序，冠军为排序后首位。

---

## 五、与单通道的关系

- 不传 `--dual-channel` 时，行为与原有单通道一致（单 suite、单 base_patch）。
- 双通道为显式开启（`--dual-channel`），两通道可暂时共用同一 golden suite，后续再拆 stress_bucket / regular_bucket。

---

## 六、Determinism Doctrine（确定性教条）

同一批 patch、同一份 suite、同一个 seed，连续跑 N 次，冠军必须**位级一致**，否则本轮进化无效。

1. **同一输入不得产生多种冠军**  
   校验项：`champion_patch_id`、`rank_key`（字典序排序键）、`stress_summary` 哈希、`regular_summary` 哈希。任一项不同即判为 `NON_DETERMINISTIC_EVOLUTION`。

2. **随机性必须完全受 seed 控制**  
   所有随机采样（候选生成、suite 内若有）必须使用传入 seed，不得有未固定熵源。

3. **排序必须稳定**  
   不可依赖 dict 遍历顺序；比较与序列化使用 `sort_keys=True` 或显式有序结构。

4. **若出现漂移，本轮进化作废**  
   不产出 personality_profile、不写 champion_bundle；仅写入 `run_manifest.json` 标记 `determinism_status: NON_DETERMINISTIC_EVOLUTION` 及各次 run 指纹，便于审计。

**启用方式**：`--determinism-check 3`（默认 1 即不校验）。仅双通道时生效。

---

## 七、验收命令（可复制）

**1）双通道冒烟**
```bash
python3 tools/run_d1_tournament.py \
  --dual-channel \
  --golden-suite library_store/v1.1/golden_stress_v2 \
  --n-candidates 5 --seed 42 \
  --out-dir outputs/d1_runs/dev_dual_smoke \
  --mode recompute
```
预期：rank_report.md 分 Stress Channel / Regular Channel 两块；Stress 下 high_risk_frames > 0；排名表有 L2/L3 差异（如 volatility_mean）。

**1b）双通道 + 确定性校验（军工级）**
```bash
python3 tools/run_d1_tournament.py \
  --dual-channel --determinism-check 3 \
  --golden-suite library_store/v1.1/golden_stress_v2 \
  --n-candidates 5 --seed 42 \
  --out-dir outputs/d1_runs/dev_dual_det \
  --mode recompute
```
预期：连续 3 次冠军指纹一致则产出 personality_profile 与 champion_bundle；任一次不一致则 `NON_DETERMINISTIC_EVOLUTION`，仅写 run_manifest。

**2）Schema 违规淘汰**  
构造含 `smoothing.peak_hold_frames` 的候选 patch，运行 tournament，预期 L0 淘汰且原因含 `PATCH_SCHEMA_VIOLATION`。

**3）单通道回归**  
不带 `--dual-channel` 的旧命令行为与改造前一致（单 suite、单 base_patch、原 rank_report 格式）。
```bash
python3 tools/run_d1_tournament.py \
  --golden-suite library_store/v1.1/golden_stress_v2 \
  --n-candidates 5 --seed 42 --out-dir outputs/d1_runs/dev_smoke --mode recompute --base-patch patches/physics/stress_v2_phys_v1.json
```

---

---

## 八、变更记录

### v1.1（Phase 2 连续高压产线）

- **Guarded 触发依赖动态响应**：默认 alpha=0.25 在「单帧脉冲」型高压下 EMA 追不上，导致 DANGER 永远差一口气；**alpha=0.6 在现有脉冲素材上可触发 DANGER/Guarded**（phase2_alpha06_probe 验证：early_gain_mean=2.73，GUARDED 帧 29650，first_guarded_candidate 非 None）。
- **结论**：Phase 2 进入**连续高压素材生产线**；不再以 scale/候选数为杠杆，而以「双 stress 物理档位 + 连续高压素材 + 压力密度熔断」为制度。
- **制度落地**：
  - Stress 物理两档：`stress_channel_phys_v1_conservative.json`（alpha=0.25，稳健）、`stress_channel_phys_v1_responsive.json`（alpha=0.6，能放电）；Gate 可配置为须同时通过两套（`--stress-base-patch-responsive`）。
  - PowerClips 主产线默认 `--min-consecutive-over 0.6:30`；pulse 与 sustain 两套素材分离（early_gain 用 pulse，exit/discipline 用 sustain）。
  - 压力密度红线熔断：`eligible_early_gain_frames_total == 0` 或 `GUARDED_frames_total == 0` 时本次进化无效，不产出冠军。

---

*文档版本：v1.1。物理常数以 patches/physics/stress_channel_phys_v1.json、stress_channel_phys_v1_conservative.json、stress_channel_phys_v1_responsive.json、regular_channel_phys_v1.json 为准。*
