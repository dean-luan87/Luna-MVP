# Luna Simulation Lab — Resource Simulation Policy v0

**Phase**：`Phase-Luna-Simulation-Lab-001`  
**定位**：**Hardware Resource Simulation** 层：在 Mac/Docker/进程限制下 **近似** 端侧算力与内存压力；**不等同** 真实 SoC 功耗、热设计与电池曲线。

---

## 1. 可模拟维度

| 维度 | 手段示例 | 说明 |
|------|-----------|------|
| CPU 核数 | Docker `--cpus`、任务亲和、背景负载进程 | 用于弱算力延迟与 STCM timeout |
| 内存上限 | Docker `-m`、进程 ulimit（平台相关） | 触发 OOM、重 OCR 崩溃路径筛选 |
| GPU 不可用 | `gpu_available: false` + 环境变量/profile | 强制 CPU-only 路径 |
| 磁盘 IO 压力 | 同盘并发读写、throttle 工具（后续 harness） | 慢盘对缓存与 manifest 的影响 |
| 热/电量 mock | **传感器状态 mock**（见 Input policy），非物理发热 | 仅逻辑门控与 trace |

---

## 2. 与 profiles 的对应

`low_memory_2gb` / `low_memory_4gb`、`low_cpu_1core` / `low_cpu_2core`、`long_run_1h` / `long_run_4h` 等 **必须在** `resource_limits` 中 **显式数字** 化，避免「口头低资源」无法复验。

---

## 3. 观测与产物

- **人工/半自动**：Activity Monitor 查看 CPU、内存、磁盘、网络、能耗（Apple 官方文档支持该类维度）。  
- **自动**：`resource_report.json` 建议包含采样时间窗、RSS 峰值、CPU%、可选 GPU 状态；长稳与 `resource_timeseries.jsonl`（Test Board）可 **合并引用**。

---

## 4. 限制声明

跨架构 **QEMU emulation** 可用于 **兼容性**，**禁止** 将其结果直接作为 **端侧性能 SLA**；Apple Silicon 上 **优先 ARM64 Linux/macOS 客体** 做性能相关阅读。

**不等同真实硬件；真实硬件验证仍为后置必须环节。**
