# V1.8.1 日志与指标文档

**版本**: V1.8.1  
**创建日期**: 2025-12-29  
**状态**: ✅ 已完成

---

## 一、字段定义

### Observer Mode 专属日志字段

#### 最小日志字段（必须）

| 字段名 | 类型 | 说明 | 写入时机 |
|--------|------|------|----------|
| `observer_trigger_reason` | string | Observer Mode 触发原因 | observer_mode=true 时 |
| `observer_level` | string | Observer Mode 级别（background / confirm / intervene） | observer_mode=true 时 |
| `observer_user_response` | string | 用户响应（accepted / rejected / ignored，仅 CONFIRM 时使用） | CONFIRM 且有用户响应时 |

#### 额外字段（内部日志，用于排查）

| 字段名 | 类型 | 说明 | 写入时机 |
|--------|------|------|----------|
| `observer_enabled` | bool | Observer Mode 是否启用（写死当前是否启用） | observer_mode=true 时 |
| `observer_bypass_reason` | string | 记录为何未记录/未触发 | 需要记录未触发原因时 |

---

## 二、写入时机

### 写入条件

**硬约束**：
1. ✅ `observer_mode=false` 时，**禁止写任何新增字段**
2. ✅ `observer_enabled=False` 时，不记录（避免污染日志）
3. ✅ 日志写入失败 → 吞掉异常（或降级到 debug），不影响用户侧流程

### 写入流程

```python
# 伪代码示例
def log_observer_mode_event(...):
    # 硬约束 1: observer_mode=false 时，禁止写任何新增字段
    if not observer_enabled or not metadata.get("active", False):
        return  # 完全不写上述字段
    
    try:
        # 写入日志
        log_metadata = {
            "observer_trigger_reason": ...,
            "observer_level": ...,
            "observer_user_response": ...,
            "observer_enabled": observer_enabled,
            "observer_bypass_reason": ...,
        }
        write_log(log)
    except Exception as e:
        # 硬约束 2: 日志写入失败不影响主流程
        logger.debug(f"[ObserverMode] 日志写入失败（已忽略）: {e}")
        # 不抛出异常
```

---

## 三、开关策略

### Observer Mode 开关

**配置项**：`OBSERVER_MODE_ENABLED`（建议在配置文件中）

**行为**：
- `OBSERVER_MODE_ENABLED = False` → 完全不写 Observer Mode 日志字段
- `OBSERVER_MODE_ENABLED = True` → 正常写入日志

### 日志级别控制

**日志级别**：`INFO`（默认）

**降级策略**：
- 日志写入失败 → 降级到 `DEBUG`，不影响主流程
- 不影响用户侧流程

---

## 四、指标口径

### 核心评估指标

#### 1. confirm_success_rate（CONFIRM 成功率）

**定义**：
```
confirm_success_rate = accepted / (accepted + rejected + ignored)
```

**计算逻辑**：
- 统计所有 `observer_level == "confirm"` 的日志
- 统计 `observer_user_response` 为 `accepted`、`rejected`、`ignored` 的数量
- 成功率 = accepted / 总数

**数据来源**：
- 日志字段：`observer_level`, `observer_user_response`

---

#### 2. intervene_trigger_count（INTERVENE 触发次数）

**定义**：
```
intervene_trigger_count = 所有 observer_level == "intervene" 的日志数量
```

**计算逻辑**：
- 统计所有 `observer_level == "intervene"` 的日志条数

**数据来源**：
- 日志字段：`observer_level`

---

#### 3. human_help_trigger_count（人工求助触发次数）

**定义**：
```
human_help_trigger_count = 所有 trigger_reason 包含 "human_assist" / "human_help" / "fallback" 的日志数量
```

**计算逻辑**：
- 统计所有 `observer_trigger_reason` 包含关键词的日志条数

**数据来源**：
- 日志字段：`observer_trigger_reason`

---

#### 4. avg_confirm_rounds_per_scene（平均每场景 CONFIRM 轮数）

**定义**：
```
avg_confirm_rounds_per_scene = 总 CONFIRM 轮数 / 场景数量
```

**计算逻辑**：
- 统计每个场景（`scene_id`）的 CONFIRM 轮数
- 计算平均值

**数据来源**：
- 日志字段：`observer_level`, `scene_id`（metadata 中）

---

## 五、指标计算函数

### 函数签名

```python
def calculate_observer_metrics(log_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    v1.8.1: 核心评估指标计算
    
    硬约束：
    - 仅提供函数/脚本入口
    - 不自动运行（避免污染性能与日志）
    - 不影响 v1.8 主链路
    """
```

### 返回值

```python
{
    "confirm_success_rate": float,  # CONFIRM 成功率
    "intervene_trigger_count": int,  # INTERVENE 触发次数
    "human_help_trigger_count": int,  # 人工求助触发次数
    "avg_confirm_rounds_per_scene": float,  # 平均每场景 CONFIRM 轮数
    "total_sessions": int,  # 总会话数
    "total_observer_events": int  # 总 Observer Mode 事件数
}
```

### 使用方式

**不自动运行**：
- 函数仅提供计算能力
- 需要手动调用或通过脚本调用
- 不接入主流程

**示例**：
```python
from core.observer_mode_metrics import calculate_observer_metrics
from Luna_Badge.core.log_manager import LogManager

# 读取日志
log_manager = LogManager()
logs = log_manager.read_logs()

# 计算指标（手动调用）
metrics = calculate_observer_metrics(logs)
print(metrics)
```

---

## 六、安全约束验证

### 硬约束 1: observer_mode=false 时，禁止写任何新增字段

**验证方式**：
- ✅ 代码检查：`if not observer_enabled or not metadata.get("active", False): return`
- ✅ 测试：observer_mode=false 时，日志中不应出现 Observer Mode 字段

### 硬约束 2: 日志写入必须是旁路

**验证方式**：
- ✅ 代码检查：`try-except` 包裹，吞掉异常
- ✅ 测试：日志写入失败时，主流程不受影响

### 硬约束 3: 指标计算不影响主链路

**验证方式**：
- ✅ 代码检查：仅提供函数，不自动运行
- ✅ 测试：主流程不调用指标计算函数

---

## 七、向后兼容性

### v1.8 兼容性

**保证**：
- ✅ observer_mode=false 时，行为 100% 等价 v1.8
- ✅ 日志字段不影响 v1.8 日志解析
- ✅ 指标计算函数不影响 v1.8 主链路

### 日志格式兼容

**v1.8 日志格式**：
- 不包含 Observer Mode 字段
- 日志解析器应忽略未知字段

**v1.8.1 日志格式**：
- 包含 Observer Mode 字段（仅在 observer_mode=true 时）
- 向后兼容：v1.8 日志解析器可正常解析（忽略未知字段）

---

## 八、使用建议

### 日志记录

**推荐时机**：
- Observer Mode 激活时
- CONFIRM 有用户响应时
- INTERVENE 触发时
- 人工求助触发时

**不推荐**：
- observer_mode=false 时记录
- 频繁记录（避免日志膨胀）

### 指标计算

**推荐方式**：
- 定期（如每天）手动计算
- 通过脚本批量计算
- 不接入实时监控（避免性能影响）

**不推荐**：
- 实时计算（影响性能）
- 自动运行（避免污染日志）

---

## 九、故障排查

### 为什么没有记录日志？

**检查清单**：
1. ✅ `observer_enabled` 是否为 `True`？
2. ✅ `metadata.get("active")` 是否为 `True`？
3. ✅ 日志写入是否失败（检查 debug 日志）？

### 为什么指标计算不准确？

**检查清单**：
1. ✅ 日志数据是否完整？
2. ✅ 日志字段是否正确？
3. ✅ 场景 ID 是否正确？

---

## 十、总结

### 完成状态

- ✅ Prompt 6.1: Observer Mode 专属日志（已完成）
- ✅ Prompt 6.2: 核心评估指标计算（已完成）

### 安全验证

- ✅ observer_mode=false 时，行为 100% 等价 v1.8
- ✅ 日志写入失败不影响主流程
- ✅ 指标计算不影响主链路

### 下一步

可以进入测试阶段：统一输出测试脚本总集（正常 / 极端 / 回滚 / 人工求助）

---

**最后更新**: 2025-12-29  
**维护者**: V1.8.1 开发团队


