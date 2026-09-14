# M2.1 分时段 Benchmark 附录

## 状态摘要

**M2.1：主路稳定性验证通过，备路实战验证待补。**

- M2.1 分时段 benchmark：**通过**（可正式写进结论）。
- 下一步必做：**备路注入式验证**（plus timeout / exception / `None` → 验证 turbo 接管及 json / val / fallback）。完成前主备链不算完整闭环。
- 勿再扩新变量，直至注入式验证落地。

---

## 执行范围

- **day**：25 轮 × 4 case，共 100 样本
- **night**：25 轮 × 4 case，共 100 样本
- **接入**：主备 bundle（qwen-plus 主 / qwen-turbo 备）
- **provider_ab_profile**：`optimized`

（脚本：`tools/benchmark_qwen_long_voice_primary_backup_m2.py`；一键 day+night：`tools/run_m2_primary_backup_benchmark_day_night.sh`。）

---

## 全局结果

| 指标 | day | night | 结论 |
|------|---:|---:|---|
| avg_ms | 6203.7 | 6192.6 | 同档，无明显时段差异 |
| p95_ms | 7902.1 | 7944.7 | 同档，无明显长尾恶化 |
| json_rate | 1.0 | 1.0 | 稳定 |
| val_rate | 1.0 | 1.0 | 稳定 |
| fallback_rate | 0.0 | 0.0 | 稳定 |
| mixed_preserve_rate* | 0.92 | 0.96 | 固定 mixed 基准句下稳定 |

\* 该 mixed 指标仅针对 benchmark 中固定 `mixed_hospital` 句，**不等同于**真实多场景 mixed 产品评估口径。

---

## 各 case 形态

- **最慢**：`task_two_steps`（avg ~7.7s，p95 ~8.0s）
- **`mixed_hospital`**：avg ~6.2–6.3s，p95 ~7.0–7.1s
- **较快**：`unsupported_register`、`hospital_short`（avg ~4.7–6.0s）

两时段内 case 排序与量级一致，未观察到单 case 时段性异常。

---

## 主备结论

- `backup_used_count = 0`
- `provider_switch_rate = 0`

**可确认：**

- 主路 `qwen-plus` 在 200 次固定压测下稳定
- 主备接入未引入额外失败

**不可确认：**

- `qwen-turbo` 备路已在真实链路中完成实战验证

---

## 阶段结论（三条）

1. 分时段各 25 轮 × 4 case，day/night 全局 avg、p95、json/val/fallback 同档，未观察到明显时段性抖动。
2. 全程未发生接入层主→备切换，只能说明主路在压测条件下稳定，不能据此认定 turbo 备路已实战验证。
3. benchmark 内固定 mixed 基准句表现稳定，但真实多场景 mixed 产品级评估仍需单独完成。

---

## mixed 汇报口径（最稳写法）

- **benchmark 口径**：固定 `mixed_hospital` 一条，本次 day **0.92** / night **0.96**。
- **真实场景 smoke 口径**：多关键词、多场景抽检（例如 12 case smoke 曾出现约 **40%** keyword 显式落槽率）。

汇报中**不要**笼统写「mixed 已通过」，应写：

> 固定 mixed 基准句在分时段压测下表现稳定，但真实多场景 mixed 的产品级评估仍需单独完成。

---

## 一句话收束

现在可以确认**主路稳定**；下一步只补**备路注入式验证**，不要再扩新变量。

---

## 相关文档

- **M2.2 备路注入式验证（已完成）**：`LUNA_VOICE_LONG_VOICE_M2_2_BACKUP_INJECTION_APPENDIX.md`
