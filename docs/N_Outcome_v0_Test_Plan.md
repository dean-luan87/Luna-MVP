# N 层（Outcome v0）完整测试方案（冻结版）

## 一、测试目标（只回答三件事）

1. 当 ENGAGED 发生但未执行动作时，N 层是否**一定**产出 Outcome？
2. Outcome 的 type / reason 是否全部可解释（无 UNKNOWN）？
3. Outcome 是否可被稳定统计与验证（脚本可 PASS）？

**目标不是“是否经常发生”，而是“一旦发生是否正确记录”。**

---

## 二、测试前置条件（必须满足）

- 已接入：J 层（engaged_signal）、N 层（outcome）
- 已存在：`tools/verify_outcome_n_v0.py`
- Trace 格式：允许出现 `engaged_signal` 与 `outcome`（同条）
- **不允许**：修改算法、阈值、节律/仲裁逻辑

---

## 三、测试方式（唯一方式）

启用一次性 **「可控 ENGAGED × 未执行」** 测试模式：

- 主流程通过 `--force-engaged-test` 开关（仅测试用）：
  - 强制 `rhythm_state = "ENGAGED"`、`engagement.level = "L1"`
  - 强制本 tick `decision = WAIT`（不执行动作）
- 该开关不进入正式逻辑，不影响封版。

---

## 四、测试执行步骤（逐条执行）

### Step 1：运行一次测试流程

```bash
python3 run.py --video test_video_complex_6m42s.mp4 --force-engaged-test
```

- 至少运行 **30–60 秒**
- 不需要语音输入、不需要任务触发
- 期间应多次进入 ENGAGED 且 decision=WAIT，从而产生 engaged_signal + outcome

### Step 2：确认 trace 写入

确认 `logs/a3_trace.jsonl` 中至少 1 行包含：

- `"engaged_signal": { ... }`
- 同一行包含 `"outcome": { ... }`

Outcome 结构必须包含：

- `outcome_type`: 冻结枚举（ACTION / NO_ACTION）
- `reason`: 冻结枚举（ACTION_EXECUTED / BLOCKED_* / NOT_ATTEMPTED）
- `apply_now`: false

### Step 3：运行 N 层自动验收脚本

```bash
python3 tools/verify_outcome_n_v0.py logs/a3_trace.jsonl
```

---

## 五、验收判据（全部满足才算通过）

脚本输出必须满足：

- `ENGAGED ticks (rhythm=ENGAGED): >= 1`
- `Engaged_signal records (J):     >= 1`
- `Outcome records (N):           == Engaged_signal records`
- `[PASS] Outcome completeness OK`
- `[PASS] Consistency OK`
- `[PASS] No UNKNOWN outcome type or reason`
- `[PASS] apply_now all false (shadow-only)`
- **Final verdict: ✅ N layer v0 PASSED**

且：

- Outcome type / reason 仅来自冻结 enum
- apply_now 全为 false
- 不允许出现 FAIL_UNKNOWN / UNKNOWN

---

## 六、通过后的结论（可写入设计文档）

**N 层（Outcome v0）已验证：**

- 在 ENGAGED 且未执行动作时，Outcome 必然产出
- Outcome 的失败/未执行原因完全可解释
- Outcome 可被稳定统计、自动验证
- 满足 shadow-only、不干预行为的设计约束

**N 层 v0 可冻结。**

---

## 七、失败时的唯一修复方向（不扩散）

| 现象           | 只允许修复                         |
|----------------|------------------------------------|
| engaged_signal 未写 | 修 J 层触发条件                    |
| 有 J 无 N      | 修 Outcome 生成调用链              |
| reason 为 UNKNOWN | 补齐失败归因枚举                   |
| enum 漂移      | 冻结枚举定义                       |

**不允许：** 调参、改节律、改 eligibility、改 arbitration。

---

## 八、测试完成后的状态

- N 层封板
- 后续只在真实运行中观察分布
- 不再作为工程阻断点
