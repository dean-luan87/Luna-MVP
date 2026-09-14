# LUNA — Scene Delta Individual & Hive Storage Policy v0

## Phase

- **Phase-MidPlatform-SceneDelta-001**

## Purpose（本阶段只做定义）

冻结“个体存储 vs 蜂巢群体存储”的分层策略，明确：

- Scene Delta 的压缩/增量记录用于减少重复处理与支持世界变化分析
- 但**不等于事实共享**，更不等于写入真实世界模型
- 群体聚合必须受隐私、安全、验证等级约束

## Storage levels（冻结）

```json
{
  "storage_level": "individual_local | hive_group_candidate | hive_verified_pack",
  "shareable_to_hive": false,
  "privacy_risk_level": "low | medium | high",
  "requires_anonymization": true,
  "cross_luna_validation_status": "not_uploaded | pending | multi_source_confirmed | contradicted"
}
```

## individual_local_compression（定义）

用途：

- 服务当前设备/当前用户（减少重复处理）
- 支持个人常走路径的世界变化记忆候选（仍 candidate-only）
- 可记录“位置变化频率/复查建议”等统计，但不得直接写事实

约束：

- 默认 `shareable_to_hive=false`
- 不实现任何真实上传

## hive_group_compression（定义；本阶段不实现）

用途（定义性）：

- 聚合多个 Luna 的重复观察（区域级世界变化判断）
- 支持 cross-validation（稳定/真实/过期/冲突）
- 为未来 Evidence Knowledge Pack 预留（需要严格隐私与验证 gate）

硬约束：

- 本阶段不实现上传/共享
- 默认不允许从 candidate 直接变成 verified pack
- 必须可追责（来源、匿名化、验证状态）

## 禁止项（强制）

- 禁止把压缩记录直接当世界事实写入
- 禁止未经验证就默认 shareable
- 禁止在本阶段实现任何真实上传

