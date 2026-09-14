# Observation Attention Layer Governance Standard V1

**Standard ID:** `ObservationAttentionLayerGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Layer-Planning-v1-001`

## 定位

Observation Attention Layer 将 **区域分割** 升级为 **观察调度 / 注意力分配**：

```
分割区域 → 优先级排序 → 后续模型路线候选 → Detection/OCR/Depth/SLAM 任务路由
```

不是模型层、不是事实层、不是导航决策层。

## TestBoardProtectedArtifactRuleV1 追加规则（23 条）

1. Observation Attention outputs are candidates only.  
2. Observation Attention does not execute models.  
3. Observation Attention does not call Detection/OCR/SLAM/Depth directly.  
4. Observation Attention does not write facts.  
5. Observation Attention does not write semantic layer.  
6. Observation Attention does not trigger runtime.  
7. Observation Attention does not trigger navigation/action/speech.  
8. Observation Attention does not call output adapter.  
9. Observation Attention does not mutate registry.  
10. Observation Attention must preserve source envelope.  
11. Observation Attention must not overwrite model output.  
12. MobileSAM prompt labels remain candidate labels.  
13. Human corrections are priority signals, not ground truth.  
14. Follow-up routes are route candidates, not execution commands.  
15. Region priority schema is required.  
16. Follow-up model route schema is required.  
17. Task context policy is required.  
18. TestBoard record is required.  
19. Test process record is required.  
20. Test conclusion record is required.  
21. Test artifacts are protected.  
22. Test records are non-deletable.  
23. Cleanup must not delete TestBoard artifacts.
24. Single-frame MobileSAM must not output confirmed_dynamic.
25. Motion state is candidate_only, not motion ground truth.
26. Static/dynamic/scene_structure routes are candidates, not execution commands.
27. Human correction motion linkage is priority signal only.

## Schema 注册

| Schema | Path |
|--------|------|
| Attention Record | `schemas/observation_attention/observation_attention_record_schema_v1.json` |
| Region Priority | `schemas/observation_attention/region_priority_schema_v1.json` |
| Follow-up Route | `schemas/observation_attention/followup_model_route_schema_v1.json` |
| Policy | `schemas/observation_attention/observation_attention_policy_v1.json` |

## 禁止矩阵

| 操作 | 允许 |
|------|------|
| 生成 attention record | ✓ candidate |
| 调用 Detection/OCR runner | ✗ |
| 写 fact | ✗ |
| 导航指令 | ✗ |
| prompt_label → 事实类别 | ✗ |
| correction → ground truth | ✗ |
| route → 立即执行 | ✗ |

## 下游

- Detection/OCR Runner 接入优先服务 P0/P1 区域  
- UI 执行阶段：胶囊排序、右侧面板、底部摘要
