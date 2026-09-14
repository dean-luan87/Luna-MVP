# D2.2 可 Patch 键空间（来自 a3/config + merge 约定）

## Patch 合并入口（当前）

- **simulation/sim_runner.py**：`patch_config = _load_json(patch_path)`，`candidate = {**baseline_config, **patch_config}`，写入 `run_meta.json["config_applied"]`。当前 **未** 传入 A3 执行（passthrough）；D0.1 接入真实重算时需从此处把 candidate 转成 A3Config。

## A3 实际读取的配置（a3/config.py + a3/engine.py）

以下键名按「扁平化」约定（patch JSON 一层 key，D0.1 可做嵌套展开或点号解析）。

### 1. 权重层（weights）— 参与 complexity 加权

| 键名 | 默认值 | 说明 |
|------|--------|------|
| risk_density | 0.30 | 风险密度权重 |
| redline_hit | 0.25 | 红线触发权重 |
| occlusion_ratio | 0.12 | 遮挡比 |
| roi_load | 0.20 | ROI 负载 |
| path_instability | 0.30 | 路径不稳定 |
| motion_instability | 0.30 | 运动不稳定 |
| branch_load | 0.20 | 分支负载 |
| speak_pressure | 0.05 | 语音压力 |
| reject_pressure | 0.03 | 拒绝压力 |

### 2. 阈值层（thresholds）— 决定 SAFE/CAUTION/DANGER 与 hold

| 键名 | 默认值 | 说明 |
|------|--------|------|
| safe_to_caution | 0.38 | ema ≥ 此值可进 CAUTION |
| caution_to_danger | 0.68 | ema ≥ 此值可进 DANGER |
| hysteresis | 0.06 | 回滞，防抖 |
| min_mode_hold_ms | 2000 | 模式最短保持时间(ms) |

### 3. 输出策略（output_policy）— lookahead / advice_scale

| 键名 | 默认值 | 说明 |
|------|--------|------|
| lookahead_safe_m | 5.0 | SAFE 时前瞻(m) |
| lookahead_caution_m | 10.0 | CAUTION 时前瞻(m) |
| lookahead_danger_m | 15.0 | DANGER 时前瞻(m) |
| lookahead_redline_boost_m | 5.0 | 红线时额外前瞻 |
| advice_scale_safe | 1.0 | SAFE 时建议尺度 |
| advice_scale_caution | 0.7 | CAUTION 时建议尺度 |
| advice_scale_danger | 0.4 | DANGER 时建议尺度 |

### 4. 平滑（smoothing）

| 键名 | 默认值 |
|------|--------|
| alpha | 0.25 |

### 5. 顶层

| 键名 | 默认值 |
|------|--------|
| enabled | False |
| roi_count_cap | 12 |
| branch_count_cap | 6 |

---

## blind_patch 极端化策略（降低风险敏感度）

- **权重**：风险相关权重压到 0 → complexity 偏低，不易进 CAUTION/DANGER。
- **阈值**：safe_to_caution / caution_to_danger 提到接近 1.0 → 几乎不离开 SAFE。
- **lookahead**：可保持或略放大，非必须。

Patch JSON 可用扁平 key（如 `weights.risk_density`）或单层嵌套（如 `{"weights": {"risk_density": 0}}`），由 D0.1 解析约定决定。当前 sim_runner 仅做 `dict merge` 并写入 run_meta，不解析嵌套。
