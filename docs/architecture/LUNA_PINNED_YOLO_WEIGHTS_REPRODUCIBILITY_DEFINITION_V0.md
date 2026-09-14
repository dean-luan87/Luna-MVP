# LUNA — Pinned YOLO Weights & Dependency Reproducibility Definition v0 (Phase-ModelPerception-013)

## 背景 / 问题
当前 YOLO shadow 已成为 **Option A / phone_local / offline evaluation** 的默认 perception source（Phase-ModelPerception-012）。
但模型加载仍依赖 `torch.hub` 路径与环境依赖，存在不可控漂移风险：
- 上游代码/权重变更
- hub cache 行为差异
- 依赖版本漂移（已出现过 `seaborn` 缺失案例）

本阶段目标不是增强能力，而是把“能跑”升级为“可复现”。

## 本阶段目标（只做定义）
定义 pinned YOLO weights / pinned dependencies 的工程约束，回答：
1. 权重从哪里来、如何固定版本
2. 权重 hash 如何记录与校验
3. 依赖版本如何固定与记录
4. torch.hub 是否允许继续作为默认加载路径（结论：不允许长期默认）
5. readiness check 必须检查什么
6. 如何记录 model_config_id / weights_source / dependency_status
7. 权重/依赖不匹配如何 fallback baseline/mock
8. 如何保证后续离线评测可复现

## 严格边界（必须写死）
- 不新增 runtime
- 不改 YOLO adapter
- 不重跑评测链
- 不扩 Option A
- 不进入 controlled_live_stream / full controlled trial
- 不执行导航动作、不真实播报
- pinning 策略不得绕过 disable/fallback/rollback

## 输出（本阶段需产出文档集合）
- `docs/architecture/LUNA_YOLO_WEIGHTS_AND_DEPENDENCY_MANIFEST_SCHEMA_V0.md`
- `docs/architecture/LUNA_YOLO_MODEL_LOAD_POLICY_V0.md`
- `docs/architecture/LUNA_YOLO_REPRODUCIBILITY_READINESS_CHECK_POLICY_V0.md`
- `docs/architecture/LUNA_YOLO_REPRODUCIBILITY_GO_NO_GO_PACK_V0.md`

## 停止条件
满足即停止（不要进入实现阶段）：
- manifest schema 完成
- model load policy 完成
- readiness check policy 完成
- go/no-go pack 完成
- README 索引完成

