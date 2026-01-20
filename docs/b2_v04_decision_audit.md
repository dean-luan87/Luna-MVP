# B2 v0.4 Decision 代码位置审计报告

## 一、Decision Enum 定义位置

### 1. WorldChangeLevel 枚举定义

**文件路径：** `vision_pipeline/b2/v03/types.py`

**定义位置：** 第 10-17 行

```python
class WorldChangeLevel(Enum):
    """
    世界变化等级（B2 v0.3 的最高输出）
    """
    NONE = auto()          # 无显著变化
    LOCAL = auto()         # 局部属性变化（路面、人群）
    WORLD = auto()         # 世界性质变化（室内/室外）
    EVENT = auto()         # 突发事件（高优先级）
```

**原始语义注释：**
- `NONE`: 无显著变化
- `LOCAL`: 局部属性变化（路面、人群）
- `WORLD`: 世界性质变化（室内/室外） ← **需要废弃**
- `EVENT`: 突发事件（高优先级）

---

## 二、产出 Decision 的代码路径

### 2.1 WorldChangeAggregator.aggregate() - 基于因子的聚合判断

**文件路径：** `vision_pipeline/b2/v03/world.py`

**函数名：** `aggregate()`

**方法签名：** `def aggregate(self, factors: Dict[FactorType, FactorEvidence]) -> WorldChange:`

**Decision 产出位置：** 第 40-68 行

**Decision 枚举及语义：**

| 行号 | Decision Enum | 原始语义注释 | 触发条件 |
|------|--------------|-------------|---------|
| 42 | `WorldChangeLevel.EVENT` | 突发事件（高优先级） | `score_event >= 0.8` |
| 50 | `WorldChangeLevel.WORLD` | 世界性质变化（室内/室外） | `score_world >= 0.9` ← **需要废弃** |
| 58 | `WorldChangeLevel.LOCAL` | 局部属性变化（路面、人群） | `score_local >= 0.6` |
| 65 | `WorldChangeLevel.NONE` | 无显著变化 | 其他情况 |

**代码片段：**
```python
# 第 40-46 行
if score_event >= 0.8:
    return WorldChange(
        level=WorldChangeLevel.EVENT,  # ← INTERRUPT（字符串形式）
        confidence=min(score_event, 1.0),
        factors=reasons,
        interrupt=True
    )

# 第 48-54 行
if score_world >= 0.9:
    return WorldChange(
        level=WorldChangeLevel.WORLD,  # ← WORLD_SHIFT（字符串形式）← 需要废弃
        confidence=min(score_world, 1.0),
        factors=reasons,
        interrupt=True
    )

# 第 56-62 行
if score_local >= 0.6:
    return WorldChange(
        level=WorldChangeLevel.LOCAL,  # ← CONDITION_CHANGE（字符串形式）
        confidence=min(score_local, 1.0),
        factors=reasons,
        interrupt=False
    )
```

---

### 2.2 B2v03._summarize_world_change() - 字符串形式的 decision 映射

**文件路径：** `vision_pipeline/b2/v03/b2_v03.py`

**函数名：** `_summarize_world_change()`

**方法签名：** `def _summarize_world_change(self, evidences: Dict[FactorType, FactorEvidence], ts: float) -> Dict[str, Any]:`

**Decision 产出位置：** 第 143-181 行

**Decision 字符串及语义：**

| 行号 | Decision 字符串 | 原始语义注释 | 触发条件 |
|------|----------------|-------------|---------|
| 154 | `"INTERRUPT"` | 突发事件（高优先级） | `FactorType.EVENT in evidences` |
| 158 | `"WORLD_SHIFT"` | 世界性质变化 | `FactorType.ENV in evidences` ← **需要废弃** |
| 162 | `"CONDITION_CHANGE"` | 路况/条件变化 | `FactorType.PATH in evidences` |
| 166 | `"NOTICE"` | 通知（低优先级） | 其他情况 |

**代码片段：**
```python
# 第 143-181 行
def _summarize_world_change(
    self,
    evidences: Dict[FactorType, FactorEvidence],
    ts: float
) -> Dict[str, Any]:
    """
    把多因子 → 升维成 C 能理解的"世界变化"
    """
    
    # 优先级规则（硬规则）
    if FactorType.EVENT in evidences:
        level = "INTERRUPT"           # ← 第 154 行
        main = FactorType.EVENT
    elif FactorType.ENV in evidences:
        level = "WORLD_SHIFT"         # ← 第 158 行 ← 需要废弃
        main = FactorType.ENV
    elif FactorType.PATH in evidences:
        level = "CONDITION_CHANGE"    # ← 第 162 行
        main = FactorType.PATH
    else:
        level = "NOTICE"              # ← 第 166 行
        main = max(evidences, key=lambda k: evidences[k].score)
    
    return {
        "ts": ts,
        "window": [self.future_window_start, self.future_window_end],
        "level": level,               # ← decision 字段
        "main_factor": main.value,
        "factors": {...}
    }
```

**原始语义注释：** "把多因子 → 升维成 C 能理解的'世界变化'"

---

## 三、Decision 被使用或判断的地方

### 3.1 B2v03._log_decision() - 记录决策日志

**文件路径：** `vision_pipeline/b2/v03/b2_v03.py`

**函数名：** `_log_decision()`

**方法签名：** `def _log_decision(self, summary: Dict[str, Any], evidences: Dict[FactorType, FactorEvidence]):`

**Decision 使用位置：** 第 213-270 行

**Decision 判断/使用：**
- 第 219 行：`decision_type = summary['level']` - 从 summary 中提取 decision
- 第 243-253 行：调用 `self.logger.decision()` 记录日志
- 第 253-270 行：构建健康事件记录

**代码片段：**
```python
# 第 213-270 行
def _log_decision(
    self,
    summary: Dict[str, Any],
    evidences: Dict[FactorType, FactorEvidence]
):
    """记录 DECISION 日志：关键输出（最重要）"""
    decision_type = summary['level']  # ← 第 219 行：提取 decision
    
    # ... 省略中间代码 ...
    
    # 调用日志记录器
    self.logger.decision(
        ts=summary['ts'],
        decision_type=decision_type,  # ← 使用 decision
        main_factor=summary['main_factor'],
        confidence=max_score,
        reason=reason
    )
    
    # 记录健康事件
    health_event = B2HealthEvent(
        ts=summary['ts'],
        decision=summary['level'],     # ← 使用 decision
        ...
    )
```

**原始语义注释：** "记录 DECISION 日志：关键输出（最重要）"

---

### 3.2 B2v03.tick() - 判断是否记录 EVAL HOLD

**文件路径：** `vision_pipeline/b2/v03/b2_v03.py`

**函数名：** `tick()`

**Decision 使用位置：** 第 90 行

**Decision 判断：**
- 第 90 行：`if evidences and summary.get("level") == "NOTICE":` - 判断是否为 NOTICE

**代码片段：**
```python
# 第 90-96 行
# 4.5. 如果因子存在但未升级，记录 EVAL HOLD
if evidences and summary.get("level") == "NOTICE":  # ← 判断 decision
    scores = {k.value: v.score for k, v in evidences.items()}
    self.logger.eval_hold(
        frame_ts,
        scores,
        reason="below threshold"
    )
```

---

### 3.3 B2v03._is_duplicate() - 基于 decision 的去重判断

**文件路径：** `vision_pipeline/b2/v03/b2_v03.py`

**函数名：** `_is_duplicate()`

**方法签名：** `def _is_duplicate(self, summary: Dict[str, Any]) -> bool:`

**Decision 使用位置：** 第 183-191 行

**Decision 判断：**
- 第 190 行：`summary["level"] == self._last_summary["level"]` - 基于 decision 去重

**代码片段：**
```python
# 第 183-191 行
def _is_duplicate(self, summary: Dict[str, Any]) -> bool:
    if not self._last_summary:
        return False
    
    # 主因子 + level 相同 → 认为是同一世界态
    return (
        summary["main_factor"] == self._last_summary["main_factor"]
        and summary["level"] == self._last_summary["level"]  # ← 使用 decision 去重
    )
```

**原始语义注释：** "主因子 + level 相同 → 认为是同一世界态"

---

### 3.4 B2HealthLogger - 健康事件数据结构

**文件路径：** `vision_pipeline/b2/v03/b2_health_logger.py`

**函数名/类名：** `B2HealthEvent` (dataclass)

**Decision 使用位置：** 第 11 行

**Decision 定义：**
```python
@dataclass
class B2HealthEvent:
    ts: float
    decision: str              # WORLD_SHIFT / CONDITION_CHANGE / INTERRUPT / NOTICE  ← 第 11 行
    scores: Dict[str, float]
    reasons: Dict[str, str]
    confidence: float
    main_factor: str
```

**原始语义注释：** `WORLD_SHIFT / CONDITION_CHANGE / INTERRUPT / NOTICE`

---

### 3.5 B2Logger.decision() - 日志记录接口

**文件路径：** `vision_pipeline/b2/v03/log_utils.py`

**函数名：** `decision()`

**方法签名：** `def decision(self, ts: float, decision_type: str, main_factor: str, confidence: float, reason: str):`

**Decision 使用位置：** 第 99-118 行

**Decision 参数：**
- 第 102 行：`decision_type: str` - decision 类型参数
- 第 110 行：注释说明 `WORLD_SHIFT / CONDITION_CHANGE / INTERRUPT / NOTICE`
- 第 115 行：`self._log(LogLevel.DECISION, ts, decision_type)` - 记录 decision

**代码片段：**
```python
# 第 99-118 行
def decision(
    self,
    ts: float,
    decision_type: str,        # ← 第 102 行：decision 参数
    main_factor: str,
    confidence: float,
    reason: str
):
    """
    DECISION 日志：关键输出（最重要）
    :param ts: 时间戳
    :param decision_type: WORLD_SHIFT / CONDITION_CHANGE / INTERRUPT / NOTICE  ← 第 110 行
    ...
    """
    self._log(LogLevel.DECISION, ts, decision_type)  # ← 第 115 行：使用 decision
    self._log(LogLevel.DECISION, ts, f"└─ main: {main_factor}", indent=1)
    self._log(LogLevel.DECISION, ts, f"└─ confidence: {confidence:.2f}", indent=1)
    self._log(LogLevel.DECISION, ts, f"└─ reason: {reason}", indent=1)
```

**原始语义注释：** `WORLD_SHIFT / CONDITION_CHANGE / INTERRUPT / NOTICE`

---

### 3.6 TimelineWriter.write() - Timeline 记录示例

**文件路径：** `vision_pipeline/b2/v03/timeline_writer.py`

**函数名：** `write()`

**Decision 使用位置：** 第 31 行（示例注释）

**Decision 示例：**
```python
# 第 18-39 行
def write(self, record: Dict[str, Any]) -> None:
    """
    record 必须是「结构化事实」，不是日志文本
    
    推荐字段（v0.3）：
    {
        ...
        "event_type": "DECISION",
        "decision": "WORLD_SHIFT",  # ← 第 31 行：示例 decision
        "main_factor": "env",
        ...
    }
    """
```

**原始语义注释：** 示例注释，显示 `WORLD_SHIFT` 作为 timeline 记录的 decision 字段

---

### 3.7 Narrative.build_narrative() - 叙述生成中使用 decision

**文件路径：** `vision_pipeline/b2/v03/narrative.py`

**函数名：** `build_narrative()`

**Decision 使用位置：** 第 50 行

**Decision 判断：**
```python
# 第 50 行附近
decision = evidence_pack.get("decision", "UNKNOWN")  # ← 提取 decision
```

---

### 3.8 ReviewSessionBuilder.build_session() - Review 报告中使用 decision

**文件路径：** `vision_pipeline/b2/v03/review_session_builder.py`

**函数名：** `build_session()`

**Decision 使用位置：** 第 30 行

**Decision 判断：**
```python
# 第 30 行附近
decision = c.get("decision", "")  # ← 从 case 中提取 decision
```

---

### 3.9 AlignValidator.find_match() - 对齐验证中使用 decision

**文件路径：** `vision_pipeline/b2/v03/align_validator.py`

**函数名：** `find_match()`

**Decision 使用位置：** 第 20 行

**Decision 判断：**
```python
# 第 20 行附近
if expected and e.get("decision") not in expected:  # ← 验证 decision 是否匹配
```

---

### 3.10 AlignReport.write_markdown_report() - 报告生成中使用 decision

**文件路径：** `vision_pipeline/b2/v03/align_report.py`

**函数名：** `write_markdown_report()`

**Decision 使用位置：** 第 58, 67 行

**Decision 使用：**
- 第 58 行：表格标题 `| Decision |`
- 第 67 行：`r.get('decision','')` - 从结果中提取 decision

---

## 四、总结

### Decision Enum 定义汇总

| Enum | 定义位置 | 原始语义 | DTL 映射状态 |
|------|---------|---------|-------------|
| `WorldChangeLevel.NONE` | `types.py:14` | 无显著变化 | ✅ 保留（映射到 `NO_OP`） |
| `WorldChangeLevel.LOCAL` | `types.py:15` | 局部属性变化（路面、人群） | ⚠️ 需要条件映射 |
| `WorldChangeLevel.WORLD` | `types.py:16` | 世界性质变化（室内/室外） | ❌ 需要废弃 |
| `WorldChangeLevel.EVENT` | `types.py:17` | 突发事件（高优先级） | ⚠️ 需要条件映射 |

### Decision 字符串汇总

| 字符串 | 产出位置 | 原始语义 | DTL 映射状态 |
|--------|---------|---------|-------------|
| `"INTERRUPT"` | `b2_v03.py:154` | 突发事件（高优先级） | ⚠️ 需要条件映射 |
| `"WORLD_SHIFT"` | `b2_v03.py:158` | 世界性质变化 | ❌ 需要废弃 |
| `"CONDITION_CHANGE"` | `b2_v03.py:162` | 路况/条件变化 | ⚠️ 需要条件映射 |
| `"NOTICE"` | `b2_v03.py:166` | 通知（低优先级） | ⚠️ 需要条件映射或废弃 |

### 需要重构的核心文件

1. **`vision_pipeline/b2/v03/world.py`** - `WorldChangeAggregator.aggregate()` - 产出 `WorldChangeLevel.WORLD`（需废弃）
2. **`vision_pipeline/b2/v03/b2_v03.py`** - `_summarize_world_change()` - 产出 `"WORLD_SHIFT"`（需废弃）
3. **`vision_pipeline/b2/v03/types.py`** - `WorldChangeLevel` 枚举定义（`WORLD` 需标记为废弃）

---

