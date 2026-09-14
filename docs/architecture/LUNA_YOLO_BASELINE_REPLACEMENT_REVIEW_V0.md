# LUNA — YOLO Shadow Baseline Replacement Review v0 (Phase-ModelPerception-011)

## 结论（本阶段）
- **review_recommendation**: **GO**
- **baseline_replacement_scope**: **offline_evaluation_only**
- **allow_yolo_as_default_offline_perception_source**: **true**
- **allow_runtime_replacement**: **false**
- **allow_controlled_live_stream**: **false**
- **allow_full_controlled_trial**: **false**
- **allow_close_pending_real_sidewalk_run**: **false**

## 复审范围与输入（只限离线）
覆盖证据阶段：**Phase-ModelPerception-005 ~ 010**。

关键输入根（最新一套 YOLO chain）：
- perception replacement: `logs/yolo_perception_replacement_eval_option_a_phone_local_001_20260427_1558/`
- scene_task bridge: `logs/yolo_scene_task_bridge_eval_option_a_phone_local_001_20260427_1558/`
- fusion bridge: `logs/yolo_fusion_bridge_eval_option_a_phone_local_001_20260427_1558/`
- output bridge: `logs/yolo_output_bridge_eval_option_a_phone_local_001_20260427_1558/`
- e2e offline eval: `logs/yolo_e2e_offline_eval_option_a_phone_local_001_20260427_1559/`

## 必答问题（逐条回答）
1. **YOLO shadow 是否比 baseline/mock 提供真实 detection 增量？**  
   是。005 对比中 `yolo_invoked_count=3`、`detection_count_total=39`，且给出 per-sample 计数与类别分布。
2. **是否能稳定生成 Perception-001 五类 signal？**  
   是。006 `signal_schema_valid_rate=1.0`（5/5 signals 全样本存在）。
3. **不支持的 OCR/dynamic/depth/collision 是否诚实 not_available？**  
   是。006 honesty rates 均为 1.0（OCR/dynamic=not_available；depth_unavailable=true；collision_risk_not_confirmed=true）。
4. **是否完整通过 SceneTask/Fusion/Output 离线桥接？**  
   是。007/008/009 各自生成率与 schema_valid_rate 均为 1.0。
5. **E2E offline 是否保持 candidate-only？**  
   是。010 `allows_execute_now_false_all_stages_rate=1.0` 且 `candidate_only_integrity_rate=1.0`。
6. **是否保持 no-real-TTS？**  
   是。009/010 `real_tts_invoked_false_rate=1.0`。
7. **是否保持 safety leakage=0？**  
   是。005–010 所有阶段 leakage counters 维持 0；009/010 `forbidden_output_semantic_count_total=0`。
8. **是否保持 evidence boundary？**  
   是。010 evidence boundary rates 全为 1.0。
9. **是否允许后续离线评测默认使用 YOLO shadow perception？**  
   **允许**，但仅限 offline evaluation（见 scope policy）。
10. **是否允许进入真实 runtime？**  
   **不允许**。
11. **是否允许进入 controlled_live_stream？**  
   **不允许**。
12. **是否允许关闭 pending_real_sidewalk_run？**  
   **不允许**。并且 010 已验证 `pending_real_sidewalk_run_true_rate=1.0`。

## 关键治理点（本阶段必须强调）
- “baseline replacement”仅指 **离线评测默认源替换**，不授予任何 runtime 权限。
- 010 过程中曾出现真实边界缺口：`pending_real_sidewalk_run` 字段未在 006 产物中传递，导致 010 初跑 NO_GO。现已在 006 工具中补齐并增加硬断言，属于必要修复而非文档修饰。

## Soft follow-ups（不阻断本阶段 GO）
- torch.hub reproducibility 风险仍存在（后续需 pinned weights/deps）。
- SceneContext gates 尚未 fully runtime enforce（当前仍以标记/保守处理为主）。
- fusion/output policy 仍为最小规则 v0（仅做候选链路机制闭合，不评价效果）。

