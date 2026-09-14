# LUNA — Visual Symbol Evidence GO/NO-GO Pack v0

## Phase

- **Phase-WorldModel-VisualSymbolEvidence-001**

## Scope

本阶段只验收“定义是否完整、边界是否写死、映射是否可追责”，不验收任何 runtime/模型效果。

## Phase-WorldModel-VisualSymbolEvidence-001-Fix linkage

本阶段的 verifier 定义补丁见：

- `docs/architecture/LUNA_VISUAL_SYMBOL_EVIDENCE_VERIFIER_TEST_MATRIX_V0.md`

## GO criteria（必须全部满足）

1. **VisualSymbolEvidence 定义完整**
   - 明确与普通 OCR `raw_text` 主链的区别
   - 明确允许 OCR 作为辅助但不得单独确认含义
2. **分类 schema 完整**
   - 覆盖 `signature / seal_or_stamp / stylized_logo / brand_mark / emblem / watermark / handwritten_mark / symbolic_label / certificate_mark`
3. **meaning confirmation 策略完整**
   - `unknown/suspected/confirmed/contradicted` 状态与确认方法枚举冻结
4. **forced memory 策略完整**
   - 强制记忆分级与硬约束写死（未确认不得写事实）
5. **trust & fraud risk 策略完整**
   - 高风险类别必须带 `fraud_risk_status`
   - 默认不得输出真假最终裁决
6. **WorldContextEvidence 映射完整**
   - 未确认：candidate-only/no_write + requires_revalidation
   - 已确认：低优先级候选 + requires_revalidation
7. **Non-governance boundaries 明确**
   - 不实现 runtime
   - 不接真实记忆/世界模型写入
   - 不生成导航动作
   - 不做真假最终裁决

8. **verifier matrix（001-Fix）覆盖完整**
   - 覆盖分类、确认、强制记忆、欺诈风险、OCR 辅助边界、世界证据映射
   - 明确 hard blockers
   - 明确 no runtime/no navigation/no TTS

## NO-GO conditions（任一出现即 NO_GO）

- 把未确认符号直接写入事实记忆/事实世界证据
- 用 OCR 结果强行确认签名/印章/证书含义（无确认链条）
- 直接判定真假（输出 verified/forged 的最终结论）
- 直接执行任务/导航动作/真实播报
- 缺少 `source_image_ref` / `crop_region` / `trust` / `confirmation` 的可追责记录
- 缺少 verifier matrix 或 hard blockers 未冻结（定义不完整）

