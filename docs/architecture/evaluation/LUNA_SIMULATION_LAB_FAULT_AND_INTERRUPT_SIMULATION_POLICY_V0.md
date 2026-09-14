# Luna Simulation Lab — Fault & Interrupt Simulation Policy v0

**Phase**：`Phase-Luna-Simulation-Lab-001`  
**定位**：**Network/Fault** 与 **Long-run / Interrupt** 中的 **故障与中断** 子集；与 Evaluation Test Board **Level 4 / Level 5** 语义对齐。

---

## 1. 必须覆盖的故障与中断类别（设计 v0）

| 类别 | 示例 | 产物关注点 |
|------|------|------------|
| 任务中断 / user_cancel | 用户取消长 OCR | `interrupt_trace.jsonl` |
| system_timeout | 平台或 harness 超时 | cancellation / STCM trace |
| 子进程崩溃 / SIGSEGV | exit 139、kill -9 | crash report、signal、RSS |
| 网络断开 / 高延迟 / 丢包 | offline、unstable profile | audit、fallback 路径 |
| 内存不足 | OOM 或接近限制 | resource_report |
| stale result | 过期结果仍返回 | stale_result_report |
| voice notice expiry | 过期语音不播报 | voice_notice_report |
| provider fallback | 治理允许的降级 | audit，**禁止** 未经批准的默认切换 |

---

## 2. profile 映射

- **`crash_recovery`**：子进程 kill、exit 139 复现、batch recovery + resume。  
- **`network_unstable` / `offline`**：网络类故障。  
- **`stcm_deadline_stress`**：与 STCM policy 文档联动的人工延迟 / miss。

---

## 3. 禁止项

故障模拟 **不得** 作为 **绕过治理** 改默认 routing 或默认 provider 的借口；所有异常路径须 **可审计**。

**不等同真实硬件；真实硬件验证仍为后置必须环节。**
