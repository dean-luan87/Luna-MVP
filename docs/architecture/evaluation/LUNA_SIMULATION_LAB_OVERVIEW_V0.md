# Luna Simulation Lab — Overview v0

**Phase**：`Phase-Luna-Simulation-Lab-001`  
**名称**：Mac-based Soft/Hardware Simulation Environment v0  
**定位**：在 **Mac** 上搭建 **Luna 软硬件模拟环境（Simulation Lab）**，为 **Luna Evaluation & Test Board** 提供 **标准化、可复现的模拟运行环境**。**非** 完整硬件仿真；**不等同** 真实端侧芯片、摄像头物理视角、热设计、电池曲线与传感器噪声的认证结论。

**硬边界（本 phase）**：仅 **模拟环境架构、profile 契约、配置示例、文档与静态 verifier**。**不**运行 OCR / 视觉 / 语音模型；**不**接 runtime；**不**改 OCR routing；**不**替换 RapidOCR；**不**进入 MidPlatform 实装。具体 **Dockerfile / compose / 执行 harness** 可在后续 phase 增补（本仓库 verifier 不因缺脚本而 NO_GO，见 GO/NO-GO pack）。

---

## 1. 与 Evaluation Test Board 的关系（必须）

| 层级 | 职责 |
|------|------|
| **Evaluation Test Board** | 定义 **测什么**：Level 0–9、准入、产物、闸门。 |
| **Simulation Lab** | 定义 **在哪种模拟环境下测**：profile、资源、网络、输入、故障注入、STCM 应力。 |

**Test Board 决定「测什么」；Simulation Lab 决定「在哪种模拟环境下测」。** 二者组合才构成可治理的工程试验闭环。

---

## 2. Simulation Lab 子域（逻辑树）

在 Test Board 之下，本 v0 将 Lab 划分为：

1. **Software Environment Simulation** — Python/依赖矩阵、provider 版本、config profile、CPU-only 等。  
2. **Hardware Resource Simulation** — CPU/内存/GPU 不可用、磁盘 IO 压力、热/电量 mock。  
3. **Sensor/Input Simulation** — 图像序列、视频、ROI、OCR manifest、音频、ASR mock、GPS/map/visual anchor、传感器状态。  
4. **Network/Fault Simulation** — 离线、高延迟、丢包、超时、子进程 kill、exit code 模拟、stale result。  
5. **Long-run / Interrupt Simulation** — 与 Test Board Level 5/6 对齐的 cancel、timeout、pause/resume、crash/restart、长稳 loop。  
6. **Provider Runtime Simulation** — 在 **治理规则不变** 前提下，对 provider 选择与降级路径做 **环境侧** 约束（不改默认 routing 策略本身）。  
7. **STCM Time-Space Simulation** — deadline miss、stale discard、voice expiry、anchor drift、fallback 等 **可观测** 场景。

---

## 3. Mac 上可用基础能力（工程事实，非性能承诺）

- **Docker / venv / conda**：可复现依赖与 ** cgroup 类资源限制**（视平台而定）。  
- **Apple Virtualization.framework / UTM / 商业 VM**：可做多 **系统隔离**；Apple Silicon 上 **ARM64 客体** 通常优于跨架构 **emulation**（后者 **不宜** 作为性能判据）。  
- **观测**：Activity Monitor、`psutil`、`vm_stat`、Instruments 等用于 **半自动/自动** 资源采样（与 profile 的 `resource_report` 对齐）。

---

## 4. 必须解决的工程问题（摘要）

1. 多系统依赖下 Luna **能否启动与复现**。  
2. 不同 CPU/内存预算下 **是否崩溃**、是否触发 **声明内** 的降级。  
3. 低资源下 **自动降级** 是否符合治理与审计。  
4. OCR/Vision/Voice **provider 选择** 是否在 **模拟约束** 下仍符合治理。  
5. STCM 对 timeout / stale / voice notice 的 **可审计** 行为。  
6. 中断、恢复、长稳在 **模拟故障** 下是否稳定。  
7. **真实硬件到货前**，完成大量 **工程筛选**（**后置** 真机认证仍必须，见下节）。

---

## 5. 真实硬件验证（后置必须环节）

**Mac Simulation Lab 是工程筛选与回归环境，不是真实硬件认证环境。** 任何 **release / shadow / 端侧认证** 仍须 **真实硬件试验场** 结论；本 Lab 的 GO **不** 覆盖该环节。

---

## 6. 与 PaddleOCR exit 139 等问题

PaddleOCR labeled set **SIGSEGV / exit 139** 类问题，应在 **`crash_recovery`**、**`low_memory_*`**、**`ocr_heavy_provider_stress`** 等 profile 下 **记录** `batch_size`、RSS、`exit_code`、`signal`、crash sample，并与 **Test Board Level 4** 产物对齐；本 phase **仅** 定义 profile 与产物字段，不执行推理。

---

**schema**：`configs/evaluation/simulation/luna_simulation_lab_profiles_v0.example.json`  
**verifier**：`tools/evaluation/verify_luna_simulation_lab_v0.py`

**下一 phase（P0）**：`Phase-Luna-Simulation-Lab-Minimal-Harness-001` — 仅 `developer_full` + `crash_recovery` 可复现 harness；见 `LUNA_SIMULATION_LAB_MINIMAL_HARNESS_V0.md`。
