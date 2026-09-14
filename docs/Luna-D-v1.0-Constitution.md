# Luna-D v1.0 冻结架构文档

**（离线参数进化系统 · Industrial Mode）**

> 本文档为 D 模块宪法。D 以后所有实现均不得越界。任何突破必须升级版本号。

---

## 一、D 的定位

D **不是**决策引擎。  
D **不是**实时模块。  
D **不参与** runtime。

D **是**：

一个**离线的、确定性的、受 C 监管的**参数进化实验系统。

---

## 二、完整闭环结构

```
出问题
  → C 分析（Explain）
  → D 生成候选参数
  → D 离线回放验证
  → D 评分
  → C 灰度验证
  → 发布
  → 奖励回写经验账本
  → 进入下一轮
```

这是一个**自动驾驶式影子模式闭环**。

---

## 三、模块结构（冻结版）

### D0 — SimRunner（离线执行器）

**作用：**

- 加载 Episode
- 应用 param_patch
- 重跑 Arbiter
- 输出 replay_bundle

**约束：**

- 禁止使用真实 `CLOCK.now()`
- 禁止读取 runtime 内部状态
- 必须 **deterministic**
- 不允许写入 library_store（只写 outputs）

**输入：**

- episode_id
- param_patch.json

**输出：**

- replay_output.jsonl
- explain_output.jsonl

---

### D1 — Candidate Generator（候选生成器）

**作用：**

- 基于 Explain + Experience Ledger 生成 param_patch

**原则：**

- 不直接修改参数
- 只生成候选
- 支持全量参数空间
- 必须可复现（seed）

**输入：**

- explain_summary
- experience.jsonl
- baseline_config

**输出：**

- param_patch.json

---

### D2 — Scorer（评分裁判）

**作用：**

- 对 baseline 与 candidate 做对比
- 输出 Scorecard

**核心指标：**

1. **Safety Regression Rate**（硬门禁）
2. Volatility Index
3. Explain Completeness
4. Delta Stability
5. Consistency Rate

**冻结规则：**

- **如果 regression_count > 0 → 直接 FAIL**

---

### D3 — Gate Policy（发布门禁）

C 调用。

**规则：**

1. regression == 0
2. explain_completeness ≥ baseline
3. volatility 不超过阈值

- **通过** → 进入灰度  
- **不通过** → 写入经验账本

---

### D4 — Experience Ledger（经验账本）

**路径：**

```
library_store/v1.1/learning/experience.jsonl
```

**每条记录结构：**

```json
{
  "patch_id",
  "params",
  "regression_count",
  "volatility_index",
  "explain_score",
  "rollout_result",
  "reward",
  "created_at"
}
```

只追加，不覆盖。

---

## 四、奖惩机制（冻结）

奖励不基于「主观感觉」，只基于**客观指标**。

**定义 reward：**

| 条件 | reward |
|------|--------|
| regression == 0 | +2.0 |
| explain_score 提升 | +1.0 |
| regression > 0 | -3.0 |
| volatility 超阈 | -1.0 |

奖励写入 Experience Ledger。

**D1 在生成候选时：**

- 提升高 reward 参数组合概率
- 降低负 reward 参数组合概率
- 连续 3 次 regression 的 patch 进入 **blacklist**

---

## 五、C 与 D 的关系（最终裁定）

- **C 是监管者。**
- **D 是实验者。**

D 可以高频生成候选。  
C 决定是否灰度。  
发布成功后，**C 必须回写 reward**。

这就是认可的「**自动驾驶模式**」。

---

## 六、稳定优先级

优先级排序：

1. **Safety Regression**
2. **Determinism**
3. **Explain 完整度**
4. **参数收益**

**任何时候都不能为收益牺牲安全。**

---

## 七、当前阶段边界

**现在只进入：**

- **Phase 3.3-D0**

**只做：**

- SimRunner
- Comparator
- Scorecard 基础版

**暂时不做：**

- 全自动 Candidate Generator
- 自动灰度
- 强化学习

---

## 八、D0 的工程目标（第一阶段）

**最小目标：**

给定一个 **episode** + 一个 **param_patch**

**输出：**

- baseline_score.json
- candidate_score.json
- scorecard.json

**并打印：**

```
REGRESSION: 0
VOLATILITY: 0.23
COMPLETENESS_DELTA: +0.04
GATE: PASS
```

---

## 九、为什么现在开始 D0 是安全的？

因为：

- Explain 已结构化
- Episode 已资产化
- Determinism 已锁死
- Provider 已隔离

**地基已经够硬。**

---

## 十、冻结声明

**Luna-D v1.0 冻结：**

- 不碰 runtime
- 不读外部感知
- 不写 library_store
- 不做在线学习
- 不绕过 C

**任何突破必须升级版本号。**

---

*文档版本：Luna-D v1.0 · 冻结*
