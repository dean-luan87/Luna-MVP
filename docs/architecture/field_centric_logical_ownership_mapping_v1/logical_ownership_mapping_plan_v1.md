# Logical Ownership Mapping Plan v1

## Mapping objective
建立现有模块的逻辑归属（Layer / Domain / Governance / Evaluation / Provider / Runtime），为 Wave 1 的逻辑映射决策提供可审计的输入。

## Mapping principles
- 逻辑归属不等于物理迁移：本阶段不移动文件、不修改 import、不改变运行时。
- 优先复用已验证治理与 Verifier 资产；仅在确有必要时提出 adapter/扩展。
- Provider 为数据与能力提供者，不拥有解释权。
- Evaluation 提供判据与测试，不拥有事实准入权。
- Runtime 为执行边界，不得提升 candidate 为 fact。
- 所有物理移动在后续 Wave 明确 owner approval 后才允许。

## Architecture domains
- cognition (L0-L9)
- governance (constitution, admission, runtime_boundary, evidence_chain)
- evaluation (model_test_lens, verifiers, human_correction)
- providers (vision, ocr, audio, network, external/local models)
- runtime (controlled_execution, sandbox, execution_trace)

## Cognitive layer ownership
参照 L0-L9，将现有模块映射到相应 layer（见 `cognitive_layer_module_binding_v1.json`）。

## Governance ownership
治理能力横向复用，指定治理 owning domain 与 target consumers（见 `governance_asset_reuse_decision_v1.json`）。

## Evaluation ownership
测试与 verifier 作为横向能力，归入 evaluation 域并供各层调用。

## Provider ownership
Provider 保持为独立域，提供数据/能力接口，禁止决定认知输出解释。

## Runtime ownership
Runtime 负责受控执行与审计，不拥有准入决策权或 fact 提升权。

## Compatibility strategy
- adapter-first：优先设计兼容适配器，避免大规模物理迁移。
- 对关键路径提供兼容别名与接口，列入 Wave 2 设计。

## Migration wave decision
- 本阶段选择 Wave 1：逻辑所有权映射与优先级确定（不移动文件）。
- Wave 2-5 按既定策略延后执行（参见 migration_wave_decision_v1.json）。

## Deferred work
- 兼容适配器实现（Wave 2）
- 受控目录迁移计划（Wave 3）
- 迁移 dry-run（Wave 4）
- 真正迁移与生产切换（Wave 5）

## Stop conditions
- 不进行任何物理文件移动或 import 修改。
- 不执行模型训练或 runtime 激活。
- 不删除旧目录或批量改写历史代码。


**注**：本计划仅为 Wave 1 逻辑映射产物，所有实际动作需在后续 Wave 且经 owner approval 才能进行。