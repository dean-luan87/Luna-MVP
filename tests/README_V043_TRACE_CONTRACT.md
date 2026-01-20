# B2 v0.4.3 Trace Contract Test

## 用途

验证 v0.4.3 的"可视 / 可追溯 / 不越权"合同：

- ✅ 验证每帧必有 trace
- ✅ Gate / NO_OP / READ_ONLY 行为是否符合冻结规则
- ✅ 防止未来回退成"只看结果、不看过程"

## 使用方式

### 1️⃣ 先跑一次 B2（任意方式），生成 trace

```bash
python3 tests/test_b2_v041_gate_behavior_standalone.py
```

### 2️⃣ 再跑 trace 合同验收

```bash
python3 tests/test_b2_v043_trace_contract.py \
  --trace traces/b2_trace_v043.jsonl \
  --fps 30
```

## CI 规则

- ❌ 有 ERROR → exit 2（直接拦）
- ⚠️ 只有 WARNING → exit 1（黄）
- ✅ 全部通过 → exit 0

## 检查项

### 🔒 强制锁死的工程事实

1. **每帧都有 trace**（否则文件为空直接 ❌）
2. **Gate=SUSPENDED / READ_ONLY 不得写回**
3. **NO_OP 不得发声 / 不得写 timeline**
4. **B 永远 advisory_only**
5. **禁止确认性风险语义**

### 具体检查

- ✅ 必需字段存在（schema_version, time, runtime, gate, factors, impact, to_c, writeback, dcs）
- ✅ 时间语义（t_video_s, t_str, frame_id）
- ✅ Gate 规则（SUSPENDED/READ_ONLY 不得写回）
- ✅ Impact 规则（NO_OP 不得发送消息/写 timeline）
- ✅ 一致性检查（禁止确认性风险语义）

## 它在"工程层面"做了什么

这份脚本 = 自动化审判官

任何人、任何未来 patch，只要破坏这些原则：
- 本地红
- CI 红
- 无法合并

---

**版本：** v0.4.3  
**状态：** ✅ 已完成  
**最后更新：** 2025-01-12
