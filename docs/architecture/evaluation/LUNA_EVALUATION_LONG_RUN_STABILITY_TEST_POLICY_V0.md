# Luna Evaluation & Test Board — Long-Run Stability Test Policy v0

**Phase**：`Phase-Luna-Evaluation-Test-Board-001`  
**Level**：6  
**定位**：**Luna 全局** 长时间运行稳定性；**非 OCR 专属**。

---

## 1. 建议时长档位

| 档位 | 时长 | 用途 |
|------|------|------|
| quick stability | 30 分钟 | 快速冒烟级长稳 |
| basic stability | 1 小时 | 合并前基线 |
| extended stability | 4 小时 | 发布候选 |
| endurance | 8 小时 | 端侧耐力 |
| soak test | 24 小时+ | 后期持续浸泡 |

模块可按 **resource_budget** 声明所支持档位；未声明则 **不得** 声称完成对应档位。

---

## 2. 必须观测的信号

- **memory growth**：堆/进程 RSS/设备可用内存趋势。  
- **error accumulation**：错误率是否单调恶化。  
- **latency drift**：P95 是否持续漂移超阈值。  
- **queue backlog**：排队深度与饥饿。  
- **cache growth**：磁盘/内存缓存是否无界增长。  
- **stale_result_ratio**：过期仍被消费的比例（与 STCM 联动）。  
- **timeout_ratio** / **recovery_count**：超时与自愈频次。

---

## 3. 产出

`long_run_summary`（可并入 `test_summary.json` 或独立）、`resource_timeseries.jsonl`、`latency_timeseries.jsonl`、`error_timeseries`（可与 metrics 合并）、`stability_report.json`。详见 Artifact Standard v0 **§2**。

---

## 4. GO 条件（摘要）

无崩溃；资源增长 **可控**（低于模块声明预算或平台硬顶）；延迟漂移 **在可接受包络内**；无 **静默** 降级为错误输出。

---

**非 OCR 专属声明**：Vision 持续流、Voice TTS 长队列、MidPlatform 任务调度均适用本策略。
