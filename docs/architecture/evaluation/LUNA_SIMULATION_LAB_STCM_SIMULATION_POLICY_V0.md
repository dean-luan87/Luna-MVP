# Luna Simulation Lab — STCM Simulation Policy v0

**Phase**：`Phase-Luna-Simulation-Lab-001`  
**定位**：**STCM Time-Space Simulation**：在 Lab 中 **可重复** 地施加 deadline、过期、语音与空间锚相关应力；**不** 实装 MidPlatform runtime。

---

## 1. 必须支持的模拟场景（与 STCM 合同一致）

| 场景 | 说明 |
|------|------|
| model deadline miss | 模型未在 ModelCallDeadline 内完成 |
| stale result discard | 过期结果 **不得** 驱动用户行动 |
| spatial anchor drift | 锚点变化导致旧结果失效 |
| voice notice requested | 请求语音通知 |
| expired voice notice dropped | 过期通知 **不得** 播报 |
| fallback decision | 治理允许的换模/异步路径 |

---

## 2. 关键输出

**STCM 事件 trace** 是 Simulation Lab 在跨模态应力下的 **关键输出**：须写入 `stcm_event_trace.jsonl` 或与 Test Board **§4 STCM 产物** 建立 **字段级别名映射**（在 `simulation_summary.json` 声明）。

---

## 3. 与 Test Board Level 8 的关系

Level 8 定义 **测什么**；本 policy 定义 **如何在 Lab 中构造** 可观测输入与延迟，使 Level 8 用例 **可复现**。

---

## 4. 限制声明

Lab 内 **人工延迟** 可验证 **逻辑与 trace**；**不** 等价于真实网络抖动或端侧调度延迟的统计分布 **认证**。

**不等同真实硬件；真实硬件验证仍为后置必须环节。**
