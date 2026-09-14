# Unified final decision

Canonical helper：`compute_unified_final_decision`。

只有以下条件同时满足才输出 `GO`：

```text
functional_checks_passed
AND contract_failures == []
AND governance_preflight == PASS
AND governance_postflight == PASS
AND cognitive_logic_result == PASS
AND operational_result == PASS
```

否则输出 `NO_GO`。Runner 的 `READY_FOR_USER_VERIFICATION` 是 artifact generation status，不得复用为 verifier final decision。
