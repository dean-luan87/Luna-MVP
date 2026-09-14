# 长短语音「时长 × 复杂度」Case 矩阵 M3

**机器真值**：`configs/voice/voice_long_voice_length_complexity_cases_m3.json`（25 条）。本文档为可读索引；修改 case 请改 JSON 后同步检查本表。

## 维度说明

| 时长档 | 标签 | 说明 |
|--------|------|------|
| L1 | 0–5s | 极短文本近似 |
| L2 | 5–10s | 短句 |
| L3 | 10–20s | 中句 |
| L4 | 20–40s | 长段 |
| L5 | 40–90s | 长段+口头冗余 |

| 复杂度 | 说明 |
|--------|------|
| C1 | 单意图单任务 |
| C2 | 单任务 + 背景说明 |
| C3 | mixed（任务 + 非任务信息） |
| C4 | 多意图 / 多步骤 |
| C5 | unsupported / clarification 风险高 |

## 矩阵清单（25 条）

| ID | 时长 | 复杂度 | 摘要 |
|----|------|--------|------|
| L1_C1 | L1 | C1 | 导航回家 |
| L1_C2 | L1 | C2 | 加班累了，导航回家 |
| L1_C3 | L1 | C3 | 头疼，去医院（mixed keyword：头疼） |
| L1_C4 | L1 | C4 | 先去医院再回家 |
| L1_C5 | L1 | C5 | 自动过户车牌 |
| L2_C1 | L2 | C1 | 便利店买水 |
| L2_C2 | L2 | C2 | 迟到，导航地库 |
| L2_C3 | L2 | C3 | 焦虑+书店（keyword：焦虑） |
| L2_C4 | L2 | C4 | 加油→超市→回家 |
| L2_C5 | L2 | C5 | 自动挂号插队 |
| L3_C1 | L3 | C1 | 三里屯导航+晕车限制 |
| L3_C2 | L3 | C2 | 文具店+顺路 |
| L3_C3 | L3 | C3 | 胃病+三甲消化科（keyword：反酸/胃） |
| L3_C4 | L3 | C4 | 法院→公司→接孩子 |
| L3_C5 | L3 | C5 | 远程门禁+拆快递 |
| L4_C1 | L4 | C1 | 机场T3+拥堵策略 |
| L4_C2 | L4 | C2 | 望京健身房+牛奶 |
| L4_C3 | L4 | C3 | 睡眠/低落+国贸客户（keyword：睡眠/低落） |
| L4_C4 | L4 | C4 | 税务→公章→吃饭→银行→办公室 |
| L4_C5 | L4 | C5 | 12123全自动代办 |
| L5_C1 | L5 | C1 | 西二旗→新中关+冗长铺垫 |
| L5_C2 | L5 | C2 | 老人头晕+加油+回家 |
| L5_C3 | L5 | C3 | 失眠压力+金融街客户（keyword：失眠/压力） |
| L5_C4 | L5 | C4 | A-F 多点动线+勿压扁 |
| L5_C5 | L5 | C5 | 全自动车机+邮件+智能家居 |

## Benchmark

```bash
cd /path/to/Luna-Core
export LUNA_EXTERNAL_LLM_PROVIDER=qwen
export DASHSCOPE_API_KEY='...'
python3 tools/benchmark_long_voice_length_complexity_matrix_m3.py
```

**注意**：本矩阵为 **qwen-plus / qwen-turbo 单模型各跑全量**，**不使用**主备 bundle。

## 相关文档

- 结果附录（运行后填写）：`LUNA_VOICE_LONG_VOICE_LENGTH_COMPLEXITY_BENCHMARK_APPENDIX_M3.md`
- Pre-Filter 设计：`LUNA_VOICE_PREFILTER_LAYER_MIN_DESIGN_M3.md`
