## Phase

- **Phase ID**: `Phase-Luna-Project-Module-Inventory-and-Structure-Map-DryRun-v1-001`
- **Capability module**: `capabilities/governance/luna_project_module_inventory_and_structure_map_dryrun_v1.py`
- **Status**: dry-run-only（不做真实迁移）

## Intent

在 **Project Structure Governance Planning** 完成目标结构模型之后，本阶段把现有工程资产逐项映射到未来结构，并按 **Luna 终局 life-system 方向** 归位。

核心产出是一张完整资产归位表，每条记录至少包含：

- 当前路径 / 当前模块 / 资产类型（code / doc / phase_artifact / module）
- 当前工程域（`current_engineering_domain`）
- 未来目标模块（`future_target_module`）
- **Life-System 映射（`future_life_system_mapping`）** — 必填，防止退化为纯目录整理
- 是否客户端 / 开发者后台 / 中台器官 / 能力器官 / 认知层占位
- 是否需要版本管理
- 处置动作（keep / merge / archive / split / defer）

## Hard Boundaries

- **No file move**：不移动、不重命名、不删除任何生产文件。
- **No runtime**：不启用相机、视觉模型、OCR、跟踪、导航动作等。
- **No persistent writes**：不得写入 `WorldModel/Memory/Fact/Library`。
- 扫描仅用于 inventory（listdir 级别）；不读取用户媒体内容。

## Life-System Layers

本阶段使用的 `future_life_system_mapping` 词汇表：

- `PerceptionLayer` — 视觉 / OCR / 感知
- `InteractionLayer` — 语音 / 语言交互
- `ActionLayer` — 任务链 / 导航 / 动作
- `ContextLayer` — 地图 / 位置 / 路线上下文
- `CognitionLayer` — WorldModel / Memory / Library 占位
- `GovernanceLayer` — 宪法 / Gate / 安全治理
- `MidPlatformOrganLayer` — 中台器官系统
- `CapabilityOrganLayer` — 能力器官
- `DeveloperBackendLayer` — 白盒 / 测试 / 仿真 / 评测
- `ClientSurfaceLayer` — 客户端最小运行时表面
- `HardwareInfrastructureLayer` — 硬件 / 设备基础设施
- `LifeSystemLayer` — 情绪 / 探索 / 社会关系等终局层
- `ResilienceLayer` — 韧性 / 容错
- `UnclassifiedLegacyLayer` — 待归档 legacy

## Outputs

`_eval_out/luna_project_module_inventory_and_structure_map_dryrun_v1_smoke_v0/`：

- `module_inventory.json`
- `current_to_target_structure_map.json`
- `life_system_mapping_matrix.json`
- `developer_backend_extraction_map.json`
- `midplatform_subsystem_mapping.json`
- `future_module_placeholder_mapping.json`
- `client_boundary_mapping.json`
- `migration_risk_register.json`
- `no_file_move_boundary_report.json`

## Final Decision Contract

- **`final_decision`**: `LUNA_PROJECT_MODULE_INVENTORY_AND_STRUCTURE_MAP_DRYRUN_READY_FOR_CONSOLIDATION_PLANNING`
- **`recommended_next_phase`**: `Phase-Luna-Project-Structure-Consolidation-Planning-v1-001`

## Non-Claims

- 不声称已完成任何实际文件迁移或模块合并。
- 不声称 inventory 统计为精确资产清单（`fact_status=not_fact`）。
- 不声称任何 runtime 能力已被批准或启用。
