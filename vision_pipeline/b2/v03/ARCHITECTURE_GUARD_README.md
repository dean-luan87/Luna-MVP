# B2 / C 架构守卫系统 v0.4.1

## 📋 概述

本目录包含两套"可执行级"的架构守卫规则：

1. **Cursor Architecture Guard** - 代码审查时阻止违规
2. **DCS 硬判定项** - 运行时审判历史 trace

---

## 🎯 设计目标

**最终一句话结论：**

> 这两套东西一旦落地：
> - Cursor 负责"防走样"
> - DCS 负责"事后审判"
> - B 永远不可能再偷偷进化成"拍板者"

---

## 📁 文件说明

### 1. Cursor Architecture Guard

**文件：** `cursor_arch_guard_B2C_FROZEN_V041.md`

**用途：**
- 作为 Cursor 的系统级 Prompt / Review Guard
- 每次修改 B / C 相关代码时自动审查
- 不满足即判定为架构违规

**使用方式：**
1. 在 Cursor 中设置 Architecture Guard / Code Review Prompt
2. 将此文件内容添加到 Cursor 的系统 Prompt
3. 每次代码修改时自动审查

**核心规则：**
- RULE-B1: B 只能做条件风险预警，禁止确定性判断
- RULE-B2: 风险核验权只能在 C，B 不得替代
- RULE-B3: B 只允许在"无需靠近即可确认的人身安全风险"时直接干预
- RULE-T1: B / C 只能使用系统当前时间
- RULE-S1: 空间单位统一为"米"，遵循 3m 边界
- RULE-F1/F2: B / C 是不同频系统，不要求同步
- RULE-C1: 允许 C 过度保守，禁止提前引入学习
- RULE-M1/M2: B 的世界模型是渐进式，C 的确认结果必须回流

---

### 2. DCS 硬判定项

**文件：**
- `dcs_hard_rules_v041.py` - Python 实现
- `dcs_hard_rules_v041.md` - 规则说明文档

**用途：**
- 系统运行后审判
- 回放历史 trace
- 给工程"自省"，不是给用户看

**判定级别：**

#### 🟥 RED（硬违规，必须修）
- DCS-R1: B 输出确认性风险结论
- DCS-R2: B 替代 C 完成风险核验
- DCS-R3: B 在视角不稳定 Gate fail 时仍输出判断
- DCS-R4: B 在 ≤3m 或室内主导决策
- DCS-R5: 使用非系统当前时间进行判断

#### 🟨 YELLOW（风险设计，需关注）
- DCS-Y1: B 过于频繁唤醒但未产生有效预警
- DCS-Y2: B 输出长期只读但世界记忆未更新
- DCS-Y3: C 长期过度保守导致体验下降

#### 🟩 GREEN（设计正确）
- DCS-G1: B 只输出条件式风险
- DCS-G2: C 完成靠近核验并回写记忆
- DCS-G3: 熟悉场景下 B 自动降权
- DCS-G4: 时间 / 距离标尺始终一致

**使用方式：**
```python
from vision_pipeline.b2.v03.dcs_hard_rules_v041 import DCSHardRules

# 检查单个 trace
results = DCSHardRules.check_all(trace)

print(f"分数: {results['score']}/100")
print(f"RED 违规: {len(results['red'])}")
print(f"YELLOW 风险: {len(results['yellow'])}")
print(f"GREEN 通过: {len(results['green'])}")
```

---

## 🔧 集成指南

### 在 Cursor 中集成 Architecture Guard

1. **打开 Cursor 设置**
   - 进入 Settings → Architecture Guard
   - 或 Settings → Code Review Prompt

2. **添加规则**
   - 复制 `cursor_arch_guard_B2C_FROZEN_V041.md` 的全部内容
   - 粘贴到 Cursor 的 Architecture Guard 配置中

3. **测试**
   - 尝试修改 B / C 相关代码
   - 验证 Cursor 是否自动审查并阻止违规

### 在 CI/CD 中集成 DCS 检查

1. **创建检查脚本**
   ```python
   # scripts/check_dcs.py
   import json
   import sys
   from vision_pipeline.b2.v03.dcs_hard_rules_v041 import DCSHardRules
   
   trace_file = sys.argv[1]
   with open(trace_file, "r") as f:
       traces = [json.loads(line) for line in f]
   
   all_results = [DCSHardRules.check_all(t) for t in traces]
   
   # 统计
   total_red = sum(len(r["red"]) for r in all_results)
   avg_score = sum(r["score"] for r in all_results) / len(all_results)
   
   if total_red > 0 or avg_score < 85:
       print(f"❌ DCS 检查失败: RED 违规 {total_red} 个, 平均分数 {avg_score:.1f}")
       sys.exit(1)
   else:
       print(f"✅ DCS 检查通过: 平均分数 {avg_score:.1f}")
   ```

2. **添加到 CI 流程**
   ```yaml
   # .github/workflows/dcs_check.yml
   - name: DCS Check
     run: |
       python scripts/check_dcs.py traces/b2_runtime_trace_v04.jsonl
   ```

---

## 📊 检查清单

### 代码修改前检查

- [ ] 已阅读 `cursor_arch_guard_B2C_FROZEN_V041.md`
- [ ] 确认修改不违反任何 RULE-B* / RULE-T* / RULE-S* 等规则
- [ ] 确认所有输出包含 `advisory_only: true`
- [ ] 确认只使用 `system_ts`，无其他时间字段
- [ ] 确认遵循 3m 边界规则

### 代码修改后检查

- [ ] 运行 DCS 检查：`python -m vision_pipeline.b2.v03.dcs_hard_rules_v041`
- [ ] 确认无 RED 违规
- [ ] 确认 DCS 分数 ≥ 85

---

## 🎯 下一步

根据你的选择，可以：

1. **👉 把 DCS 接入 Web 仪表盘（红黄绿）**
   - 创建可视化界面
   - 实时显示 DCS 分数和违规项

2. **👉 用 DCS 回审 v0.1–v0.3 的代码 / trace**
   - 使用 DCS 规则分析历史版本
   - 形成进化证据链

3. **👉 冻结 v0.4.1，正式进入 v0.5**
   - 确认 v0.4.1 完全合规
   - 开始 v0.5 开发

---

**版本：** v0.4.1（冻结版）  
**最后更新：** 2025-01-12  
**状态：** ✅ 已就绪，可直接使用
