# Luna OCR Provider Levels & Usage Policy v0

**关联**：`LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md`（含 **OCRRequest**、**OCRDispatchDecision**、**OCR Orchestrator** 与 **§22 分级响应要求**）。

**范式**：OCR 是 **由中台调度的多 provider 能力系统**，不是「接一个库就能用」的模型模块。业务侧 **不得** 按「谁识别准谁上」直连 provider；须通过 **OCRRequest → Orchestrator → OCRDispatchDecision** 准入。

## Level 0：No OCR / Cache Reuse

- **runs_model**：false。  
- **用途**：复用上一帧、历史证据、Scene Delta 缓存、环境指纹命中的 OCR 证据。  
- **原则**：无新证据需求时 **默认停留 Level 0**。  
- **响应要求（摘要）**：毫秒级；输出 **cached evidence** 或 **stale candidate**；**禁止**伪造新跑模型观测。

## Level 1：Light OCR

- **runs_model**：true。  
- **典型**：低成本本地引擎（如 **RapidOCR 可作为 Level 1 候选**）、小 ROI、横向普通文本。  
- **约束**：高帧场景须限频；与 Trigger Gate 强绑定；**禁止**复杂版面语义定案。  
- **响应要求（摘要）**：`text_items`、score、basic box；低延迟；输出仍为 **evidence**。

## Level 2：Heavy Local OCR

- **runs_model**：true。  
- **典型**：PaddleOCR 类等 **高算力、高内存** 本地实现。  
- **约束**：**异步或极低频**；**禁止**作为默认逐帧路径；仅升级路径；**禁止**阻塞导航主链路同步热路径。  
- **产品化表述**：PaddleOCR **≠** 默认 provider；**=** Level 2 重型本地候选，适合 **低频、高价值、复杂 ROI、Level 1 低置信升级、本地重型 fallback**。  
- **响应要求（摘要）**：更丰富几何（polygon）、reading_order **candidate**；可审计字段齐全。

## Level 3：Remote / VLM OCR

- **runs_model**：true（含网络或大模型推理）。  
- **典型**：云端 OCR、VLM 读图、复杂版面理解。  
- **约束**：隐私、权限、成本、超时与 **最先降级** 策略；**禁止**无授权远程；**禁止**直写事实或绕过 Bridge。  
- **响应要求（摘要）**：layout evidence、structure **candidate**、semantic **hint**；全部为 **候选/证据**，须权限与预算闸门。

## 升级与降级（摘要）

升级链：**0 → 1 → 2 → 3** 须显式理由（置信、任务价值、ROI 复杂度、隐私授权）。降级链：**3 关 → 2 限频 → 1 仅高价值 ROI → 0 缓存**。调度由 **OCR Orchestrator** 根据 **规则 + 状态 + 预算** 产出 **OCRDispatchDecision**，而非业务模块自行选型。
