# B2 v0.2 问题分析：每帧都输出 Advisory

**问题时间**: 2025-01-XX  
**问题现象**: 每帧都输出大量重复的 Advisory，且都是 `trigger=INIT`

---

## 一、问题现象

### 1.1 日志输出
```
[B2-v0.2][1767698880.64] DEESCALATE | trigger=INIT | confidence=0.30 | impacts=0
[B2-v0.2][1767698880.64] DEESCALATE | trigger=INIT | confidence=0.30 | impacts=0
[B2-v0.2][1767698880.65] DEESCALATE | trigger=INIT | confidence=0.30 | impacts=0
... (100+ 条重复输出)
```

### 1.2 观测数据
- **reuse 比例**: 0.0% (FutureCache 没有复用)
- **suppressed 比例**: 0.0% (AdvisoryCache 没有抑制)
- **所有 advisory**: `trigger=INIT`
- **处理时间**: 0.2 秒内处理 100 帧

---

## 二、问题根源分析

### 2.1 核心问题

**所有 advisory 都是 `trigger=INIT`**，说明：
- `_last_emit_ts` 总是 `None`（第一次运行）
- 或者每次调用 `observe()` 时，`_last_emit_ts` 都被重置

### 2.2 可能的原因

#### 原因 1: `min_interval_sec` 检查没有生效
```python
# b2_controller_v02.py:198
if self._last_emit_ts is not None and (now - self._last_emit_ts) < self.min_interval_sec:
    return None
```

**问题**: 如果 `_last_emit_ts` 是 `None`，这个检查会跳过，导致每帧都输出。

#### 原因 2: `should_suppress` 总是返回 `False`
```python
# b2_controller_v02.py:287
should_suppress, cache_age = self.advisory_cache.should_suppress(
    advisory, current_world_signature, now
)
```

**问题**: 如果 `_last_advisory` 总是 `None`，`should_suppress` 会返回 `False`，导致每帧都输出。

#### 原因 3: `_last_emit_ts` 没有正确更新
```python
# b2_controller_v02.py:315
self._last_emit_ts = now
```

**问题**: 如果 `_last_emit_ts` 在每次输出后没有正确更新，或者被重置，会导致每帧都输出。

---

## 三、代码检查

### 3.1 `observe()` 方法流程

```python
def observe(self, ...):
    # 1. 检查缓存
    if not self.cache.should_run(now):
        return self.cache.get_last_advisory()
    
    # 2. 检查最小间隔
    if self._last_emit_ts is not None and (now - self._last_emit_ts) < self.min_interval_sec:
        return None
    
    # 3. 判断触发原因
    if self._last_emit_ts is None:
        trigger = "INIT"  # ← 所有输出都是这个
    elif world_changed:
        trigger = "WORLD_CHANGE"
    elif ttl_expired:
        trigger = "TTL_EXPIRE"
    else:
        return None
    
    # 4. 生成 advisory
    advisory = ...
    
    # 5. 检查是否抑制
    should_suppress, cache_age = self.advisory_cache.should_suppress(...)
    if should_suppress:
        return None
    
    # 6. 更新状态
    self._last_emit_ts = now  # ← 应该在这里更新
    ...
```

### 3.2 问题点

1. **第 198 行**: `min_interval_sec` 检查依赖于 `_last_emit_ts`，如果它是 `None`，检查会跳过
2. **第 207 行**: 如果 `_last_emit_ts` 是 `None`，会触发 `INIT`
3. **第 287 行**: `should_suppress` 依赖于 `_last_advisory`，如果它是 `None`，会返回 `False`
4. **第 315 行**: `_last_emit_ts` 应该在这里更新，但如果 `should_suppress` 返回 `True`，会在第 295 行更新

---

## 四、修复建议

### 4.1 修复 1: 确保 `_last_emit_ts` 正确更新

**问题**: 如果 `should_suppress` 返回 `True`，`_last_emit_ts` 会在第 295 行更新，但 `advisory_cache.update()` 没有被调用。

**修复**: 在 `should_suppress` 返回 `True` 时，也要更新 `advisory_cache`：

```python
if should_suppress:
    # 更新 AdvisoryCache（即使抑制了，也要记录）
    self.advisory_cache.update(advisory, current_world_signature, now)
    # 更新内部状态
    self._last_emit_ts = now
    self._last_sig = sig
    self._last_world_signature = current_world_signature
    return None
```

### 4.2 修复 2: 确保 `min_interval_sec` 检查生效

**问题**: 如果 `_last_emit_ts` 是 `None`，`min_interval_sec` 检查会跳过。

**修复**: 在 `min_interval_sec` 检查之前，先检查 `cache.should_run()`：

```python
# 检查缓存：是否应该运行
if not self.cache.should_run(now):
    return self.cache.get_last_advisory()

# 检查最小间隔（即使 _last_emit_ts 是 None，也要检查 cache）
if self._last_emit_ts is not None and (now - self._last_emit_ts) < self.min_interval_sec:
    return None
```

### 4.3 修复 3: 确保 `should_suppress` 逻辑正确

**问题**: 如果 `_last_advisory` 总是 `None`，`should_suppress` 会返回 `False`。

**修复**: 确保 `advisory_cache.update()` 在每次输出时都被调用：

```python
# 需要输出，更新 AdvisoryCache
self.advisory_cache.update(advisory, current_world_signature, now)
```

---

## 五、验证步骤

### 5.1 修复后验证

1. **运行测试**:
   ```bash
   python3 examples/b2_v02_video_test.py test_video.mp4 > b2_log.txt 2>&1
   ```

2. **检查日志**:
   - 应该看到 `future_cache=reused`（缓存复用）
   - 应该看到 `advisory suppressed`（Advisory 抑制）
   - 不应该看到大量重复的 `trigger=INIT`

3. **使用观测工具**:
   ```bash
   python3 -m vision_pipeline.b2.b2_cache_observer b2_log.txt
   ```

4. **预期结果**:
   - reuse 比例 > 30%
   - suppressed 比例 > 50%
   - 只有第一次输出是 `trigger=INIT`，后续应该是 `TTL_EXPIRE` 或 `WORLD_CHANGE`

---

## 六、总结

### 6.1 问题根源
1. `_last_emit_ts` 可能没有正确更新
2. `min_interval_sec` 检查依赖于 `_last_emit_ts`，如果它是 `None`，检查会跳过
3. `should_suppress` 依赖于 `_last_advisory`，如果它是 `None`，会返回 `False`

### 6.2 修复方案
1. 确保 `advisory_cache.update()` 在每次输出时都被调用（包括抑制时）
2. 确保 `_last_emit_ts` 在每次输出后都正确更新
3. 确保 `min_interval_sec` 检查在 `_last_emit_ts` 是 `None` 时也能生效

### 6.3 下一步
1. 应用修复方案
2. 重新运行测试
3. 验证缓存复用和抑制效果

---

**问题状态**: 🔴 待修复  
**优先级**: 🔴 高（影响缓存逻辑的核心功能）

