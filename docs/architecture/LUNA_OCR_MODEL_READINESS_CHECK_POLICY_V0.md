## Phase-ModelOCR-003

OCR Model Readiness Check Policy v0

### 0. 目标

定义 readiness check 的规则、失败动作与禁止项，确保 OCR 候选资产进入后续阶段前已满足“可追踪、可校验、可回退”的最低门槛。

### 1. Readiness check 的输入/输出

- **输入**：OCR model manifest（JSON）
- **输出**：readiness report（JSON），写入 `logs/`，不进入 runtime

### 2. 必须检查项（v0）

#### 2.1 manifest 基础合法性

- 必须存在：`manifest_version/model_config_id/model_family/...`
- `provider_kind` 与 `weights_source` 必须在枚举集合内

#### 2.2 禁止项（硬边界）

manifest 必须显式满足：

- `raw_text_only=true`
- `semantic_interpretation_enabled=false`
- `allows_execute_now=false`
- `real_tts_invoked=false`

任何一项不满足 → **not_ready + hard_blocker**

#### 2.3 依赖检查（best-effort）

- 不安装依赖，只做 import/version 记录
- 对 Priority 1（PaddleOCR）建议检查：`paddleocr/paddle/cv2/numpy/PIL`
- 缺依赖 → `partial`（soft follow-up），不得伪造 ready

#### 2.4 权重检查（不下载）

- `weights_source=pinned_local`：
  - 路径必须存在
  - sha256/size 必须可验证且匹配 → 否则 hard_blocker
- `weights_source=manual_download_required`：
  - 允许缺权重，但 readiness 必须标注 `partial/not_ready` 与缺失项
- path 为目录占位时允许（manifest skeleton），但不得计算 hash

#### 2.5 system provider 初检

- `provider_kind=system_provider` 时：
  - 至少检查平台是否满足（macOS Vision → darwin）
  - 不做 bridge 实现（本阶段）

### 3. Readiness 状态与失败动作（v0）

- `ready`：满足硬边界，且 pinned_local 权重可校验，依赖可 import（或明确不需要）
- `partial`：硬边界满足，但存在缺依赖或缺权重（manual_download_required）
- `not_ready`：任何 hard blocker 触发（禁止项/枚举非法/pinned_local 缺权重或 hash mismatch/system provider 不可用）

失败动作（统一）：

- readiness report 的 `recommendation` 必须为：`do_not_enter_runtime`
- 不触发任何下游链路

