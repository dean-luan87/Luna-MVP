# Luna Voice：Qwen Prompt Budget 实验附录（M3.1）

> **性质**：实验记录模板。跑批后填入数据与结论；**不**作为默认主链已上线依据。  
> **实验脚本**：`tools/benchmark_qwen_plus_prompt_budget_matrix_m3_1.py`  
> **Case 配置**：`configs/voice/qwen_prompt_budget_cases_m3_1.json`（36 条：4 budget × 3 复杂度 × 3 case）

---

## 跑批命令（示例）

```bash
cd /path/to/Luna-Core   # 或经 Workspace-Min 的 tools 符号链接等价根
source .venv-tx/bin/activate   # 按本地环境
export LUNA_EXTERNAL_LLM_PROVIDER=qwen
export DASHSCOPE_API_KEY='…'
# 可选：export LUNA_PROMPT_BUDGET_QWEN_MODEL=qwen-plus
python3 tools/benchmark_qwen_plus_prompt_budget_matrix_m3_1.py
```

校验（不调 API）：

```bash
python3 tools/benchmark_qwen_plus_prompt_budget_matrix_m3_1.py --dry-run
```

结果 JSON：`logs/benchmark_qwen_plus_prompt_budget_m3_1_<timestamp>.json`

---

## A. Prompt Budget 档位说明

| 档位 | 文件 | 内容要点 |
|------|------|----------|
| **P1 极简** | `capabilities/voice/config/prompts/prompt_budget_m3_1/voice_long_input_parse_v1_1_prompt_qwen_plus_p1_minimal.md` | 最小宪法 + 最小任务规则 + JSON 形状提醒；极限短预算 |
| **P2 标准** | `capabilities/voice/config/prompts/voice_long_input_parse_v1_1_prompt_qwen_plus.md` | **与当前生产 qwen-plus 分层提示一致**；作对照基线 |
| **P3 增强** | `…/prompt_budget_m3_1/…_p3_enhanced.md` | P2 等价主干 + mixed/unsupported/澄清/多意图附加段 |
| **P4 重载** | `…/prompt_budget_m3_1/…_p4_heavy.md` | P3 全文 + 上下文协议、长句策略、边界穷举、记忆占位说明 |

**差异小结**（填写跑批观感即可）：

- P1 ↔ P2：___  
- P2 ↔ P3：___  
- P3 ↔ P4：___  

---

## B. 矩阵结果（复杂度 × Budget）

> 从 `logs/benchmark_qwen_plus_prompt_budget_m3_1_*.json` 的 `matrix_budget_x_complexity` 与控制台矩阵摘抄。  
> **标红规则**：若相对 P2 同格出现 `json_rate` / `val_rate` 明显下滑、`fallback_rate` 明显上升、或 mixed 丢失增多，须在格内文字标注 **【劣化】**。

### B.1 按单元格（行=复杂度 C1–C3，列=P1–P4）

|  | P1 | P2 | P3 | P4 |
|--|----|----|----|-----|
| **C1** | json / val / fb / avg_ms / p95 / tokens / mixed | … | … | … |
| **C2** | … | … | … | … |
| **C3** | … | … | … | … |

**mixed 保留率**：仅在标注为 mixed 的 case 上统计；无 mixed 的格填「—」。

### B.2 按 Budget 汇总（每档 9 条）

| Budget | json | val | fallback | avg_ms | p95_ms | avg_tokens(in/out/total) | mixed保留 | multistep_flat 条数 | unsupported 误判启发 |
|--------|------|-----|----------|--------|--------|---------------------------|-----------|---------------------|-------------------------|
| P1 |  |  |  |  |  |  |  |  |  |
| P2 |  |  |  |  |  |  |  |  |  |
| P3 |  |  |  |  |  |  |  |  |  |
| P4 |  |  |  |  |  |  |  |  |  |

---

## C. 结论（须明确回答）

1. **简单档（C1）**：P1 / P2 是否足以支撑结构稳定？___  
2. **中等档（C2）**：是否必须至少 P2 / P3？___  
3. **高复杂档（C3）**：P1 / P2 是否会明显掉 mixed 或 validator？___  
4. **速度 / 稳定性最均衡的「主链档」倾向**：___（P1–P4 选一或组合策略）  
5. **是否值得做「复杂度 → prompt budget」路由？** 初步判断：___  

---

## D. 最终一句结论（三选一，仅填一条）

- [ ] **1.** 已足够支撑进入 Prompt Budget Router 设计阶段  
- [ ] **2.** 仍需补更多 case 才能决定 Prompt Budget 路由  
- [ ] **3.** 当前 Prompt Budget 差异不足以形成稳定路由依据  

**选定项编号**：___  

**证据一句**：___  

---

## 变更记录

| 日期 | 说明 |
|------|------|
| （填） | 首次跑批 JSON 路径、模型名、AB profile |
