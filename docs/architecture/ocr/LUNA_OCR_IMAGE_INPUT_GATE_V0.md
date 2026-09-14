# LUNA OCR Image Input Gate v0

**Phase**: `Phase-OCR-Input-Size-Governance-001`  
**性质**: 架构规范（静态）；**不**运行 OCR、**不**接主线、**不**改 routing。

## 1. 实证依据（必须遵守）

`Phase-PaddleOCR-Failed-Sample-Isolation-001` 产物：  
路径 `_eval_out/paddleocr_failed_sample_isolation_v0`（见 `paddleocr_failed_sample_isolation_summary.json` 与 `paddleocr_failed_sample_crash_classification.json`）。

- **size_sensitive**：`labeled_007`、`labeled_019`（同图 `ocr_7.png`）在**原图/部分尺度**下可触发 **SIGSEGV**，经 **downscale（如 max side 1600/1024）** 后子进程可通过。  
- **size_sensitive + 大图 native 风险**：`labeled_010`（约 **3000×5334 / 16MP**）原图 **SIGSEGV**；部分中间尺度仍存在 **native 风险或超时**。  

**结论**：任意大图、整图未经治理即进入**实时** OCR provider 在工程上不可接受。

## 2. 核心原则

1. **所有**拟进入 OCR Provider 的图像（含评测子进程、异步任务、用户显式请求）必须先经过 **OCR ImageInputGate**。  
2. **禁止**未经验证尺寸/像素预算的整图直接进入**实时（sync / low-latency）** OCR provider。  
3. **实时路径默认 ROI-first**：优先对 ROI 或小窗口执行 OCR；全图仅作显式降级或异步路径。  
4. **full-image OCR** 仅允许：`evaluation` / `async` / `user-requested` / `low-frequency fallback`，且仍须满足像素预算与降级策略。  
5. 超限输入必须产生可审计的 **evidence**（含 transform 记录），并最终经 **OCR Bridge**；输出仍是 **OCR evidence**，不是 world fact。  
6. 治理失败（无法降采样、分块、或资源不足）**不得**导致整任务未定义崩溃；须降级、超时、并向 **OCR Orchestrator / STCM / Performance Governance** 上报。  
7. **禁止** MidPlatform / WorldModel **直写**；本闸门只描述 OCR 输入侧。

## 3. Gate 输出（逻辑模型）

- `gate_decision`: `allow_realtime_roi` | `require_downscale` | `require_tiling` | `defer_async_heavy` | `reject_unsupported`  
- `transform_chain_ref`: 指向 source chain 与坐标变换记录（见坐标重建策略文档）。  
- `stcm_hints`: 大图像默认异步、过期分块结果不可驱动动作（与 STCM 策略对齐）。

## 4. 与配置的关系

机器可读阈值见 `configs/ocr/ocr_image_input_governance_v0.example.json`。
