【执行指令】登记 unified env / min wiring baseline 窗口 V1

## 目标

把当前已确认结构正确、可直接分析的窗口文件登记为 unified env / min wiring 实验线的 **baseline 窗口**，用于后续回归与对照；同时明确它 **不是“新的真实窗口”**，不得用于证明跨窗口稳定性。

## 一、已确认的 baseline 文件

- **baseline window JSONL**: `/Users/luanlei/Desktop/Luna-Workspace-Min/analyze_unified_env_shadow_out/windows/window_round01_baseline.jsonl`

## 1.1 占位/对照窗口（显式禁止当作新窗口）

- **placeholder window JSONL**: `/Users/luanlei/Desktop/Luna-Workspace-Min/analyze_unified_env_shadow_out/windows/window_round02_placeholder_NOT_REAL.jsonl`

说明（必须遵守）：

- 该文件由已有样本复制/对照而来，仅用于 **analyzer 回归 / 工具链验证 / 对照**。
- **不得**将其视为“新的真实窗口”，**不得**用于任何“跨窗口稳定性”结论。

## 二、输入契约（该文件满足）

该 baseline 文件为 **JSONL**（一行一个 JSON 对象），并满足以下最低输入契约：

- **每行含 `id`**
- **每行含 `event_timestamp`**
- **每行含 `metadata`**
- **`metadata` 中含以下关键对象**（至少满足“存在其一 + unified”）：
  - `sidewalk_env_summary_v1` 或 `retail_env_summary_v1`
  - `unified_env_summary_shadow_v1`
  - `unified_env_fill_shadow_v1`（最小接线实验的 fill 观测）

## 三、用途（baseline 的定位）

该 baseline 用于以下回归与对照场景：

- **unified env shadow analyzer 回归**
- **unified env min wiring analyzer 回归**
- **family guardrail 修前/修后对比**
- **fill shadow 行为基线验证**

## 四、限制（必须显式写清）

该 baseline 文件有以下硬性限制：

- **不是新的真实窗口**
- **不能用于证明跨窗口稳定性**
- **不能替代后续主工程重新导出的真实窗口 JSONL**

## 五、后续使用规则（强制）

后续若修改以下任一项：

- `unified_env_summary_v1`
- `unified_env_shadow_v1`
- `unified_env_fill_shadow_v1`
- 对应 analyzer（含统计口径、样本选择、blocked reason 计数口径等）

则必须至少用本 baseline 文件 **回归一次**，并保留最新的分析产物（JSON/MD）作为对照证据。

## 六、不要做的事

- 不改代码
- 不改 analyzer
- 不把 baseline 文件复制改名伪装成新窗口
- 不把它写成“第二/第三窗口”

## 一句话收束

先把 `window_round01_baseline.jsonl` 正式登记为 baseline 窗口文件，后续统一用于回归；新的真实窗口仍需从主工程重新导出。

