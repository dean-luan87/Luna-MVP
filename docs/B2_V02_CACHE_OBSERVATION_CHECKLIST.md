# B2 v0.2 缓存逻辑观测清单

**目标一句话**：验证 B2 是否真的"少想了、想对了、想在该想的时候"。

---

## 一、WorldSignature 层（世界是否稳定）

### ① WorldSignature 变化频率（核心）

**观察项**：
- WorldSignature 总数
- WorldSignature 变化次数
- 平均每个 Signature 持续时间

**期望**：
- 在长直路 / 室内 / 重复路段：Signature 持续 ≥ 10–20 秒
- 场景切换（进出地铁 / 红绿灯 / 室内外）：Signature 明确变化（而不是抖动）

**异常信号**：
- Signature 每 1–2 秒就变 → hash 过敏
- Signature 长时间不变但场景明显变 → 粒度过粗

**Cursor 要看日志关键词**：
```
[B2] world_signature=xxxx
```

---

## 二、Future Cache 层（是否真的在"复用未来"）

### ② FutureCache 命中率（最重要指标之一）

**观察项**：
- `future_cache_reused` 次数
- `future_cache_recompute` 次数
- `reuse / total` 比例

**期望**：
- 宽松市内 / 重复路段：reuse ≥ 60%
- 复杂场景：reuse 下降，但仍存在（≥ 30%）

**异常信号**：
- reuse ≈ 0 → 缓存逻辑没生效
- reuse ≈ 100% → 可能"看不见变化"

**日志**：
```
[B2] future_cache=reused age=Xs
[B2] future_cache=expired recompute
```

### ③ FutureCache TTL 实际寿命

**观察项**：
- 每次 reused 时的 age
- 是否频繁刚 < TTL 就失效

**期望**：
- age 分布在 2s ~ TTL（8s）之间
- 不应大量集中在 0.1–0.5s

**异常**：
- age 永远很小 → signature 抖动
- age 永远接近 TTL → TTL 可能偏长（后续优化点）

---

## 三、Advisory Cache 层（是否"克制地说话"）

### ④ Advisory 输出总次数

**观察项**：
- B2 advisory 总数
- 与 v0.1 / v0.0 对比

**期望**：
- v0.2 < v0.1
- 在 6–7 分钟视频中：20–40 次 属于健康区间

### ⑤ Advisory 抑制次数（关键）

**观察项**：
- `advisory suppressed` 次数
- `suppressed / total` 比例

**期望**：
- ≥ 30%
- 重复路段、长直路明显抑制

**日志**：
```
[B2] advisory suppressed (same as last, age=Xs)
```

**异常**：
- suppressed = 0 → advisory TTL 或 signature 没起作用
- suppressed ≫ emitted → advisory 粒度可能过粗

---

## 四、时间结构层（B2 的"节奏感"）

### ⑥ B2 输出间隔分布

**观察项**：
- min / avg / max advisory interval

**期望**：
- avg ≥ 8s
- min ≥ 1.5s
- max 可 > 15s（稳定场景）

这是 B2 区别于 C 的关键证据。

---

## 五、跨模块安全性（底线）

### ⑦ C 是否被影响（必须确认）

**观察项**：
- C 的决策间隔是否仍是 ~2s
- C 的 decision 数是否变化
- C 是否出现新状态切换 / protection

**期望**：
- 完全不变
- B2 = 旁路系统

---

## 六、综合判断标准（最终结论）

当 Cursor 看完上面数据，要给出结论式回答：

1. **B2 是否明显减少了"未来推演次数"？**
2. **在重复路段是否表现出"记忆感"？**
3. **在场景变化时是否能果断重算？**
4. **是否完全没有干扰 C？**

只要这四条是 **YES**，这套 B2 v0.2 缓存逻辑就已经是工程级成功。

---

## 使用方法

### 方法 1：使用观测工具（推荐）

```bash
# 运行 B2 v0.2，将日志输出到文件
python your_pipeline.py > b2_log.txt 2>&1

# 使用观测工具分析
python -m vision_pipeline.b2.b2_cache_observer b2_log.txt
```

### 方法 2：手动观察日志

直接观察日志输出，查找以下关键词：
- `[B2] world_signature=`
- `[B2] future_cache=reused`
- `[B2] future_cache=expired`
- `[B2] advisory suppressed`

---

## 下一步（提前规划）

等观测数据出来后，可以进入三条分支之一：
- **B2 v0.3**：Signature 粒度调优
- **FutureSimulator 内部**：真正"变聪明"
- **定义 B2 → C**：信息价值等级

现在这一步是打地基。

