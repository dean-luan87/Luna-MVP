# Verification Contract

用户终端 Verifier 已对两个 Case 完成真实检查，结果为：

`all_checks_passed=true`、`check_count=56`、`failed_checks=[]`、
`operational_result=PASS`、`cognitive_logic_result=PASS`、`final_decision=GO`。

检查内容包括：

1. `LIVE_RUNTIME`、real execution attempted/verified、provider/model invoked；
2. request/result/runtime observation/Gateway/Evidence identity 与 lineage；
3. provider success 与 cognitive sufficiency 分离；
4. Case A 一轮 `SUFFICIENT` + Stop、无 Gap/Re-observation；
5. Case B 第一轮具体 platform Gap，Gap→Re-observation trace，第二轮新真实
   invocation/new evidence/revision，`INSUFFICIENT → SUFFICIENT` + Stop；
6. cycle count 分别为 1 和 2，无 Cycle 3 或 post-sufficiency observation；
7. Candidate-only、no Truth/Fact/mutation/downstream execution；
8. Plane G assertions 完整且 compliant；
9. `validation_errors == []`。

历史边界：Runner/Verifier 尚未执行时的文档状态曾是
`WAITING_FOR_USER_TERMINAL_VERIFICATION`；本文件当前记录的是用户终端真实
验证后的 closure，不改变任何 Verifier assertion。
