# v1.8.5 Phase B 完成说明：系统稳态补丁

**状态**：✅ 已完成  
**日期**：2024-12-XX  
**版本**：v1.8.5 Phase B

---

## 一、Phase B 目标

**从"能跑"到"能长期活着"的分水岭**

让世界模型具备完整的"免疫闭环"，防止系统在真实世界长期运行中被污染、偏置、失真。

---

## 二、已完成的补丁

### 2.1 FactCandidatePool：候选过期机制（TTL）

**目标**：防止长期无人支持的候选事实永久占位，造成慢性污染。

**实现内容**：
- ✅ 扩展构造函数：增加 `candidate_ttl_s` 参数（默认 24 小时）
- ✅ 新增 `cleanup_expired()` 方法：自动清理过期候选
- ✅ 在 `fetch_promotables()` 前自动清理：即使上层忘了调 cleanup，也不会积累陈年 PROMOTABLE

**规则**（写死）：
```python
if now - last_seen_ts > candidate_ttl_s:
    status = REJECTED
    last_reason = "expired_no_recent_support"
```

**参数**：
- `candidate_ttl_s = 24 * 3600`（24 小时）

**验收标准**：
- ✅ 超过 TTL 的候选 → 状态变为 REJECTED
- ✅ 无上游调用也能自动清理
- ✅ 不影响正常 PROMOTABLE 流程

**测试**：`core/world_model/memory/test_candidate_ttl.py` ✅

---

### 2.2 LibraryRegistry：事实软回滚机制

**目标**：让已入库事实具备"自然退潮能力"，而不是永久 ACTIVE。

**实现内容**：
- ✅ 扩展构造参数：增加 `verify_ttl_fact_s`（7 天）和 `verify_ttl_rule_s`（30 天）
- ✅ 新增 `soft_rollback_stale_items()` 方法：软回滚过期条目
- ✅ 在 `update()` 末尾自动调用：防止陈年 ACTIVE

**规则**（写死）：
```python
if now - last_verified_ts > VERIFY_TTL:
    lifecycle_state = PASSIVE
    confidence *= 0.85
```

**参数**：
- `verify_ttl_fact_s = 7 * 24 * 3600`（7 天）
- `verify_ttl_rule_s = 30 * 24 * 3600`（30 天）

**验收标准**：
- ✅ 超期事实不会删除
- ✅ confidence 衰减（× 0.85）
- ✅ lifecycle 自动降为 PASSIVE
- ✅ 不需要新证据即可回滚

**测试**：`core/world_model/library/test_library_rollback.py` ✅

---

## 三、系统行为变化

### 3.1 之前（Phase A）

- ❌ 临时封路 → 永久封路
- ❌ 一次误报 → 长期偏置
- ❌ 用户恶意输入 → 慢性毒化
- ❌ 系统"越跑越偏"

### 3.2 现在（Phase B）

- ✅ 临时封路：当天有效，几天后自动退潮
- ✅ 一次误报：没有持续证据就过期
- ✅ 下雨积水：雨停后 relevance 下降，事实也会随验证 TTL 逐步退场
- ✅ 系统能自然遗忘
- ✅ 数据可追责、可回滚、可复现

---

## 四、技术细节

### 4.1 候选过期机制

**触发时机**：
- 每次调用 `fetch_promotables()` 前自动清理
- 也可手动调用 `cleanup_expired()`

**清理范围**：
- 只处理 `PENDING` 和 `PROMOTABLE` 状态的候选
- `CONSUMED` 和 `REJECTED` 不处理

**清理规则**：
- 如果 `now - last_seen_ts > candidate_ttl_s`，则标记为 `REJECTED`
- 设置 `last_reason = "expired_no_recent_support"`

### 4.2 事实软回滚机制

**触发时机**：
- 每次调用 `LibraryRegistry.update()` 末尾自动回滚
- 也可手动调用 `soft_rollback_stale_items()`

**回滚范围**：
- 只处理 `ACTIVE` 和 `PASSIVE` 状态的条目
- `DEPRECATED` 不处理

**回滚规则**：
- 根据条目类型选择 TTL（FACT/SAFETY_NOTE = 7 天，RULE = 30 天）
- 如果 `now - last_verified_ts > VERIFY_TTL`，则：
  - `lifecycle_state = PASSIVE`
  - `confidence = max(0.0, confidence * 0.85)`

---

## 五、完成后的系统能力

### 5.1 免疫闭环

**世界模型现在具备完整的"免疫闭环"**：
- ✅ 候选过期机制：防止陈年候选污染
- ✅ 事实软回滚：防止陈年事实永久霸占
- ✅ 稳定性闸门：位置不稳定时不写新信息
- ✅ 慢确认机制：事实必须经过候选池慢确认

### 5.2 可追责、可回滚、可复现

- ✅ **可追责**：所有状态变化都有 `last_reason` 记录
- ✅ **可回滚**：事实不会删除，只会降级和衰减
- ✅ **可复现**：稳定 ID、时间戳、证据链完整

---

## 六、测试验证

### 6.1 单元测试

- ✅ `test_candidate_ttl.py`：候选过期机制测试
- ✅ `test_library_rollback.py`：Library 软回滚测试

### 6.2 集成测试

- ✅ `world_model_full_demo.py`：全链路演示
- ✅ `world_model_rollback_demo.py`：退潮效果演示（新增）

---

## 七、下一步建议

### 7.1 已完成

- ✅ FactCandidatePool：候选过期机制
- ✅ LibraryRegistry：事实软回滚机制
- ✅ 单元测试
- ✅ 集成演示

### 7.2 可选增强

1. **参数调优**：根据实际运行数据调整 TTL 参数
2. **监控指标**：添加过期/回滚统计指标
3. **告警机制**：大量过期/回滚时发出告警

---

## 八、总结

**Phase B 完成意味着**：

✅ 世界模型不会"越跑越偏"  
✅ 临时事实不会永久污染  
✅ 系统能自然遗忘  
✅ 数据可追责、可回滚、可复现

**这是从"能跑"到"能长期活着"的分水岭。**

---

**文档版本**：v1.8.5 Phase B 完成版  
**最后更新**：2024-12-XX  
**状态**：✅ 已完成


