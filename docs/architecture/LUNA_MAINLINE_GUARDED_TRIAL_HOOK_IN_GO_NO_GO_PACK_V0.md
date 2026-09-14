# LUNA Guarded Trial Hook-In GO / No-Go Pack v0

**Phase**：Phase-Mainline-RuntimeReadiness-004

---

## GO（本 Phase）

满足以下全部条件：

- 三条 hook wrapper 存在，且默认 `enabled=false`、`no_op=true`。  
- global kill switch 生效（`LUNA_DISABLE_ALL_GUARDED_TRIALS` 优先级最高）。  
- invalid mode 阻断（`blocked_invalid_mode`）。  
- side effect audit 全为 false：不调 provider、不播报、不进入下游、不写世界模型。  
- trace/replay/whitebox jsonl 非空。  
- verifier 通过：`tools/verify_mainline_guarded_trial_hook_in_v0.py` 返回 `ok=true`。  
- 不改变默认 provider 策略、不改变 env 语义、不删除 legacy fallback。  

