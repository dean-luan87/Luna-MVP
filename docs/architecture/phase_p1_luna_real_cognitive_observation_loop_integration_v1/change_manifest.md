# Change Manifest

新增 evaluation-layer real cognitive observation loop：

- real OCR case definitions and source bindings；
- bounded two-cycle integration engine；
- user-terminal Runner；
- fail-closed Verifier。

共享 Runtime 只做向后兼容的 additive plumbing：透传 live loop 的 cycle/prior
candidate refs；根据真实非空 native OCR output 绑定 observation information
refs；保留旧调用者未提供新字段时的原有行为；暴露实际 A-Route proof 供上层
形成 cycle-2 prior lineage。

同时扩展既有 Plane G evaluator 对 `LIVE_RUNTIME` 的 mode-aware invocation
boundary 判断；没有新增 Plane G assertion set，也没有重写 YOLO/RapidOCR
provider behavior。

## Documentation closure

依据用户终端真实 Verifier 结果完成 closure：

- `LIVE_RUNTIME`；2 cases；56 checks；`failed_checks=[]`；
- `operational_result=PASS`；`cognitive_logic_result=PASS`；`final_decision=GO`；
- Case A 单轮 sufficient/Stop；Case B Gap-driven Re-observation、第二次真实
  Provider invocation、new RuntimeObservation/Evidence、Revision、gap reduction、
  sufficient/Stop；无 Cycle 3；
- recorded result 未使用；candidate-only；无 World Truth、Field mutation 或
  Decision/Task/Action execution；`validation_errors=[]`。

历史 `WAITING_FOR_USER_TERMINAL_VERIFICATION` 仅表示 Agent 静态实现完成时的
阶段状态，现已由真实终端验证关闭。
