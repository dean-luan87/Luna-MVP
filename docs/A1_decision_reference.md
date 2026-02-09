# A1 判定函数 / 文件路径与签名（供补丁式 diff 对齐用）

## 文件路径

- **A1 判定与 engagement 等级**：`intervention/engagement_v0.py`
- **调用 A1 的入口**：`runtime/a3_logger.py` 中 `log_a3_timeseries()`

---

## 函数 / 类签名（当前仓库）

### 1. 对外入口（调用方用这个）

```python
# intervention/engagement_v0.py

def get_engagement_v0() -> EngagementV0:
    ...

class EngagementV0:
    def tick(
        self,
        *,
        now: float,           # 秒，来自 time.time()
        rhythm_state: str,    # "IDLE" | "PREPARE" | "ENGAGED"
        pal: float,
        complexity: float,
        vc: float,
        control_mode: str,   # 如 "GUARDED" | "ASSISTED"
    ) -> EngagementOutput:
        ...
```

### 2. 输出类型

```python
@dataclass
class EngagementOutput:
    level: str       # "L0" | "L1" | "L2" | "L3"
    advice_scale: float
    pal_lookahead_m: float
    speak_cooldown_s: float
```

### 3. A1 时间累计核心（内部）

```python
# intervention/engagement_v0.py

@dataclass
class A1Thresholds:
    pal_l2_threshold: float = 0.19
    complexity_threshold: float = 0.50
    vc_threshold: float = 0.60
    l2_hold_seconds: float = 3.0
    dt_min: float = 0.0
    dt_max: float = 1.5

@dataclass
class A1LevelState:
    l2_acc_seconds: float = 0.0
    last_ts: Optional[float] = None
    level: int = 0  # 0=L0, 1=L1, 2=L2

def a1_update_level_time_accum(
    st: A1LevelState,
    *,
    ts: Optional[float],
    engaged: bool,
    pal: float,
    complexity: float,
    vc: float,
    th: A1Thresholds,
) -> None:
    """每来一条样本调用一次；原地更新 st。"""
```

### 4. 调用处（a3_logger 里如何调 engagement）

```python
# runtime/a3_logger.py 内 log_a3_timeseries()

now = time.time()   # float 秒
rhythm_state = get_rhythm_v0().tick(now=now, pal=pal_diff, ...)
control_mode_str = _enum_value(mode.control_mode)  # "GUARDED" 等

eng = get_engagement_v0().tick(
    now=now,
    rhythm_state=rhythm_state,
    pal=pal_diff,
    complexity=complexity_effective,
    vc=vc,
    control_mode=control_mode_str,
)
payload["engagement"] = {
    "level": eng.level,
    "advice_scale": round(eng.advice_scale, 2),
    ...
}
```

---

## 变量名对应（你方 → 本仓库）

| 你方命名 | 本仓库 |
|----------|--------|
| `ts` | `now`（传入 `tick(now=...)`，单位秒） |
| `engaged` | `rhythm_state == "ENGAGED"` |
| `pal_value` / `pal` | `pal`（即 `pal_diff`） |
| `complexity` | `complexity`（即 `complexity_effective`） |
| `vc` | `vc`（即 `view_confidence`） |
| `L2_ENTRY_THRESHOLD` | `PAL_L2_THRESHOLD`（0.19） |
| `L2_HOLD_SECONDS` | `L2_HOLD_SECONDS`（3.0） |
| `A1LevelState.level` | 0/1/2 → 映射为 `"L0"`/`"L1"`/`"L2"`，再与 L3 规则、防抖合并得到 `EngagementOutput.level` |

---

## 小结（贴给外部做补丁时复制）

- **文件**：`intervention/engagement_v0.py`
- **入口**：`get_engagement_v0().tick(now=, rhythm_state=, pal=, complexity=, vc=, control_mode=)` → `EngagementOutput`
- **A1 核心**：`a1_update_level_time_accum(st, ts=now, engaged=True, pal=, complexity=, vc=, th=)`，内部用 `st.level` 0/1/2；`now` 来自 `time.time()`（秒）。
