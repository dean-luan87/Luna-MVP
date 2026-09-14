# Qwen 外部长输入 Provider：A/B 结论与默认档位（M0）

## 结论（已采纳）

主链 **`QwenExternalLongInputModelProvider` 默认档位为 `optimized`**（代码常量 `DEFAULT_QWEN_AB_PROFILE`，未设置 `LUNA_QWEN_AB_PROFILE` 时即此档）。

**`legacy` 不作为默认**，仅保留为：A/B 对照、回归基线、故障排查时临时切换（`LUNA_QWEN_AB_PROFILE=legacy`）。

## optimized（B）具体行为

- 请求体显式 **`enable_thinking: false`**（执行链与思考链分离）
- 默认 **`max_output_tokens = 1024`**（可用 `LUNA_QWEN_MAX_OUTPUT_TOKENS` 覆盖）
- **`requests.Session` + keep-alive**（同实例多轮复用连接）

## A/B 口径（摘要）

- 脚本：`tools/ab_qwen_provider_long_input_compare.py`（子进程避免模块缓存；每组 smoke + `LUNA_BENCH_ITERS` 轮 benchmark）
- 模型：`qwen-plus`，prompt 与主链 smoke 对齐
- 指标：全样本 `avg_ms`、`p95_ms`、`json_rate`、`val_rate`、`fallback_rate`、`mixed_preserve_rate`（mixed 医院用例）

## 一轮实测结果（示例，10 轮 × 4 case）

| 档位 | avg_ms | p95_ms | json / val / fallback | mixed_preserve_rate |
|------|--------|--------|-------------------------|------------------------|
| legacy（A） | ~7162 | ~9150 | 1.0 / 1.0 / 0.0 | ~0.8 |
| optimized（B） | ~6781 | ~8371 | 1.0 / 1.0 / 0.0 | 1.0 |

## 为何采纳 B

- 结构稳定性保持满分（json / val / fallback）
- **avg 略降、p95 明显下降**（同轮次、同 Key、同网络条件下）
- **mixed 保留从约 0.8 到 1.0**：对主链「可治理、不丢 mixed」比单纯再快几百毫秒更重要

## 为何 legacy 仍保留

不作为默认，避免新同学误把 `legacy` 当主链；仅用于对照与排障复现，与早期「无 thinking 字段 / 4096 / 无 Session」行为对齐。

## 反向验证（B→A）

非采纳前置条件；可选空档补强证据强度，不改变当前默认决策。
