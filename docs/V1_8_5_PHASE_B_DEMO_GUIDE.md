# v1.8.5 Phase B Demo 指南（工程可验收）

**状态**：✅ 交付级  
**日期**：2024-12-XX  
**版本**：v1.8.5 Phase B

---

## 一、B 阶段到底解决了什么问题（先给结论）

**Phase B 解决的是一句话的问题**：

**世界模型在没有新证据、甚至存在错误输入时，能不能"慢慢变干净"。**

### 具体落地为三件事：

1. **候选事实不会无限期堆积**（Candidate TTL）
2. **已入库事实不会永久生效**（Library Soft Rollback）
3. **所有退化都有明确原因、可追责、可复现**

**这是防污染体系的核心一环，比"多识别几个物体"重要得多。**

---

## 二、Demo 设计目标

### 🎯 Demo 要证明 4 件事

1. **候选事实**：
   - 有支持 → 成长
   - 没支持 → 自动过期

2. **已入库事实**：
   - 一段时间没人验证 → 自动降级

3. **系统不会"突然清空"**
   - 事实不会删除，只会降级和衰减

4. **系统不会"越积越脏"**
   - 过期候选和事实会自动退潮

---

## 三、Demo 场景说明

### 🧪 场景 1：候选事实自然过期

**场景**："这条路被封了"

**输入序列**：
- T0：视觉 or 系统检测 → 写入 FactCandidate（support=1）
- T0+1h：无新支持
- T0+25h：触发 cleanup

**期望结果**：
```
FactCandidate.status = REJECTED
last_reason = "expired_no_recent_support"
```

**👉 没人再提、没人再看到，就当没发生过**

---

### 🧪 场景 2：候选事实成功晋级

**场景**："这里经常积水"

**输入序列**：
- Day 1：视觉 → support +1
- Day 2：视觉 → support +1
- Day 3：再次发生

**期望结果**：
```
FactCandidate.status = PROMOTABLE
→ LibraryRegistry.consume()
→ KnowledgeItem.lifecycle = PASSIVE
```

**👉 慢确认，谨慎入库**

---

### 🧪 场景 3：已入库事实自然退潮（重点）

**场景**："这条路施工，不能走"

**输入序列**：
- 入库后 7 天内：无人再验证
- 执行 soft_rollback

**期望结果**：
```
lifecycle_state: ACTIVE → PASSIVE
confidence: 0.72 → 0.61
```

**👉 不是删，是"冷却"**

---

## 四、Demo 代码

**文件**：`examples/world_model_phase_b_demo.py`

**运行方式**：
```bash
python examples/world_model_phase_b_demo.py
```

**关键特性**：
- 使用短 TTL（5 秒）用于演示
- 完整展示三个场景
- 自动验证验收点

---

## 五、运行后你应该看到什么

### 日志关键点

```
候选创建: candidate_xxx
过期候选数: 1
可晋级候选: 1
被回滚知识条目: 1
```

### 数据库变化（人工可查）

- `fact_candidates.status`：PENDING → REJECTED（场景1）
- `fact_candidates.status`：PENDING → PROMOTABLE（场景2）
- `knowledge_items.lifecycle_state`：ACTIVE → PASSIVE（场景3）
- `knowledge_items.confidence`：0.72 → 0.61（场景3）

---

## 六、B 阶段完成声明（工程口径）

### Phase B = 系统稳态完成

**系统现在具备**：
- ✅ 自动遗忘能力
- ✅ 事实生命周期管理
- ✅ 防慢性污染
- ✅ 可回滚、可解释

### 明确还没做的（正确的留白）

- ❌ 复杂语言理解（留给二期）
- ❌ 用户主观表述解析（接口已预留）
- ❌ 地图/GPS 强融合（Phase C）

---

## 七、验收标准

### 7.1 场景 1 验收

- ✅ 候选创建后，超过 TTL 自动标记为 REJECTED
- ✅ `last_reason = "expired_no_recent_support"`
- ✅ 不影响其他候选的正常流程

### 7.2 场景 2 验收

- ✅ 满足条件的候选自动升级为 PROMOTABLE
- ✅ LibraryRegistry 成功消费候选
- ✅ 新入库条目默认为 PASSIVE（保守）

### 7.3 场景 3 验收

- ✅ 超过 TTL 的事实自动降级为 PASSIVE
- ✅ 置信度衰减（× 0.85）
- ✅ 事实不会删除，只会降级和衰减

---

## 八、技术细节

### 8.1 候选过期机制

**触发时机**：
- 每次调用 `fetch_promotables()` 前自动清理
- 也可手动调用 `cleanup_expired()`

**清理规则**：
- 只处理 `PENDING` 和 `PROMOTABLE` 状态的候选
- 如果 `now - last_seen_ts > candidate_ttl_s`，则标记为 `REJECTED`

**参数**：
- `candidate_ttl_s = 24 * 3600`（24 小时，生产环境）
- `candidate_ttl_s = 5.0`（5 秒，演示用）

### 8.2 事实软回滚机制

**触发时机**：
- 每次调用 `LibraryRegistry.update()` 末尾自动回滚
- 也可手动调用 `soft_rollback_stale_items()`

**回滚规则**：
- 只处理 `ACTIVE` 和 `PASSIVE` 状态的条目
- 根据条目类型选择 TTL（FACT/SAFETY_NOTE = 7 天，RULE = 30 天）
- 如果 `now - last_verified_ts > VERIFY_TTL`，则：
  - `lifecycle_state = PASSIVE`
  - `confidence = max(0.0, confidence * 0.85)`

**参数**：
- `verify_ttl_fact_s = 7 * 24 * 3600`（7 天，生产环境）
- `verify_ttl_fact_s = 5.0`（5 秒，演示用）

---

## 九、总结

**Phase B 完成意味着**：

✅ 世界模型不会"越跑越偏"  
✅ 临时事实不会永久污染  
✅ 系统能自然遗忘  
✅ 数据可追责、可回滚、可复现

**这是从"能跑"到"能长期活着"的分水岭。**

---

**文档版本**：v1.8.5 Phase B Demo 指南  
**最后更新**：2024-12-XX  
**状态**：✅ 交付级


