# LUNA Voice 白盒模式切换与展开规则 V1

## 0. 文档定位

- 规定**何时简洁、何时专业**、**点击展开看到什么**；后续任何 UI/后台须遵守，避免又一版「字段堆叠」。
- 本轮**不实现**真实前端；本文件即为交互契约。
- 关联：[双模式总图](./LUNA_VOICE_WHITEBOX_VIEW_MODES_V1.md)、[数据契约](./LUNA_VOICE_WHITEBOX_VIEW_CONTRACT_V1.md)。

## 1. 默认模式

| 场景 | 默认模式 | 说明 |
|------|----------|------|
| 打开白盒总览 / 最近请求列表 | **简洁** | 先结论与列表，不加载全链 |
| 仅提供 `request_id` 的深链入口 | **专业** | 已意图下钻，直接展示单链详情（仍可将顶部保留一行 concise 摘要） |
| 告警/严重 issue 推送链接 | **专业**（推荐） | 直接定位 issue + stages；顶部可保留 concise |
| 归档按日浏览 | **简洁**（manifest 统计） | 点某条链进专业 |

## 2. 进入专业模式的方式

- 从简洁列表 **点击单行** / 「详情」→ 加载并展示 `RequestTraceProfessionalView`（或等价 JSON）。
- 从 issue 类型聚合 **点击某一类** → 可先过滤列表（简洁），再点单条进专业。
- **不允许**在简洁列表默认展开每链的 `stages` 全量。

## 3. 简洁模式下展开行为

| 操作 | 应出现内容 |
|------|------------|
| 点击单链行 | 切换至专业模式单页；或侧栏展示专业五区块（见总图 §3.2） |
| 点击「问题类型」聚合行 | 下钻为该类型的过滤列表（仍为简洁行），不直接铺全字段 |
| 系统状态区「查看更多」 | 可展开当日 manifest 摘要（计数、Top issue）；**不**默认展开 `chain_ids` 全表 |

## 4. 默认折叠（即使在专业模式）

以下区块/字段默认**折叠**或收起到二级面板，需用户 explicit 展开：

- `stages[].key_fields` 中**体积大**的键（如完整配置快照、长 metadata）；保留阶段名与 status 始终可见。
- `notes` 数组（chain / issue）
- `raw_observation_refs` 列表（展示条数即可，全文折叠）
- `RequestTraceIssue.recommended_checkpoints` 超过 3 条时，第 4 条起折叠
- Archive `chain_ids` 全量

## 5. 必须附中文/业务说明的展示点

- 列头或卡片标题：`chain_type`、`final_execution_mode`、`status`、`primary_issue_type`、`severity`、`has_fallback`、`has_rollback`
- 专业模式阶段时间线：每个 `stage_name` 旁建议显示简短中文阶段说明（可与 pipeline 文档对齐）
- `failed_stage`：显示阶段中文别名 + 原始名括号

## 6. 主样本与分叉的视觉语义（非颜色实现）

- 文案上默认强调 **Piper 主链**；Fish、fallback、rollback 链在简洁模式用标签区分即可（具体颜色分级不在本轮）。
- 简洁模式列表若 `provider_name != piper`，应在行级标注「非主样本」或等价标签（实现期再做）。

## 7. 与数据契约的衔接

- 简洁模式导出/API 必须符合 [LUNA_VOICE_WHITEBOX_VIEW_CONTRACT_V1.md](./LUNA_VOICE_WHITEBOX_VIEW_CONTRACT_V1.md) §2。
- 专业模式必须符合同文档 §3–§4。

## 8. 验收对照

- [ ] 默认总览为简洁  
- [ ] 单链详情为专业且含五区块结构  
- [ ] 关键长字段在专业模式仍默认折叠  
- [ ] 字段展示义务与字典、契约一致  
