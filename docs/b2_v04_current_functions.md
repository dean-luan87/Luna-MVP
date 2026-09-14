# B2 v0.4 当前函数代码片段

## 一、_is_duplicate() 当前代码

**文件路径：** `vision_pipeline/b2/v03/b2_v03.py`

**函数位置：** 第 264-272 行

```python
def _is_duplicate(self, summary: Dict[str, Any]) -> bool:
    if not self._last_summary:
        return False

    # 主因子 + level 相同 → 认为是同一世界态
    return (
        summary["main_factor"] == self._last_summary["main_factor"]
        and summary["level"] == self._last_summary["level"]
    )
```

**当前问题：**
- 只看 `main_factor` 和 `level`，容易吞掉真实变化
- ENV 被降级后，很多真实变化会被"同一个 level"吞掉
- 缺少 `confidence` 差异判断

---

## 二、_summarize_world_change() 当前代码

**文件路径：** `vision_pipeline/b2/v03/b2_v03.py`

**函数位置：** 第 174-262 行

```python
def _summarize_world_change(
    self,
    evidences: Dict[FactorType, FactorEvidence],
    ts: float
) -> Dict[str, Any]:
    """
    B2 v0.4+
    核心原则：
    - 不描述世界
    - 只回答：是否需要 C 改变行为
    """

    # =========================
    # 1. 计算 ActionImpact（核心）
    # =========================
    impact = ActionImpact.NO_OP
    main_factor = None

    # --- 突发事件（最高优先级） ---
    if FactorType.EVENT in evidences:
        ev = evidences[FactorType.EVENT]

        # 明确阻断 / 高风险
        if ev.score >= 0.85:
            impact = ActionImpact.NEED_STOP
        elif ev.score >= 0.65:
            impact = ActionImpact.PATH_UNCERTAIN
        else:
            impact = ActionImpact.NO_OP

        main_factor = FactorType.EVENT

    # --- 路况 / 路径变化 ---
    elif FactorType.PATH in evidences:
        ev = evidences[FactorType.PATH]

        if ev.score >= 0.8:
            impact = ActionImpact.PATH_UNCERTAIN
        elif ev.score >= 0.6:
            impact = ActionImpact.NEED_SLOW_DOWN
        else:
            impact = ActionImpact.NO_OP

        main_factor = FactorType.PATH

    # --- 人流 / 车流（只影响舒适或安全时才说） ---
    elif FactorType.PEOPLE in evidences:
        ev = evidences[FactorType.PEOPLE]

        if ev.score >= 0.75:
            impact = ActionImpact.NEED_SLOW_DOWN
            main_factor = FactorType.PEOPLE
        else:
            impact = ActionImpact.NO_OP

    # --- 环境信息（ENV 永不直接触发 decision） ---
    # ENV 只能作为 evidence / background，不参与 impact 判定
    else:
        impact = ActionImpact.NO_OP

    # =========================
    # 2. ActionImpact → decision level（对外粗粒度）
    # =========================
    if impact == ActionImpact.NO_OP:
        level = "NOTICE"            # 等价于 SILENT / NO_OP
    elif impact in (
        ActionImpact.NEED_SLOW_DOWN,
        ActionImpact.PATH_UNCERTAIN,
    ):
        level = "CONDITION_CHANGE"
    else:
        # NEED_STOP / NEED_DETOUR
        level = "INTERRUPT"

    # =========================
    # 3. 汇总输出（结构化，不讲故事）
    # =========================
    scores = {k.value: v.score for k, v in evidences.items()}
    reasons = {k.value: v.reason for k, v in evidences.items()}

    return {
        "ts": ts,
        "window": [self.future_window_start, self.future_window_end],
        "level": level,                         # ← 对外 decision
        "impact": impact.name,                  # ← 内部真实语义
        "main_factor": main_factor.value if main_factor else None,
        "scores": scores,
        "reasons": reasons,
    }
```

**当前状态：**
- ✅ 已包含 ActionImpact 评估逻辑
- ✅ 已输出 `impact` 字段
- ✅ ENV 不再触发 decision

---

## 三、当前函数的问题分析

### _is_duplicate() 的问题
1. 只看 `main_factor` 和 `level`，容易吞掉真实变化
2. ENV 被降级后，很多真实变化会被"同一个 level"吞掉
3. 缺少 `confidence` 差异判断

### _summarize_world_change() 的状态
1. ✅ 已包含 ActionImpact 评估
2. ✅ 已输出 `impact` 字段
3. ⚠️ 需要验证 `impact` 字段是否正确使用

---

## 四、需要的 patch

### Patch 1: 更新注释（已完成）
- ✅ `log_utils.py:110` - 已更新
- ✅ `b2_health_logger.py:11` - 已更新

### Patch 2: 改进 _is_duplicate()（待完成）
需要添加 `confidence` 差异判断，避免吞掉真实变化。

### Patch 3: 验证 impact 字段（待验证）
确认 `impact` 字段是否正确输出和使用。

