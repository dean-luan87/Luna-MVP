## 原则

**一个 phase = 一个新的 Cursor Agent 会话。** 不要让同一个聊天无限拉长。

权威状态只落在：

- `docs/architecture/...` 阶段文档
- `docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md`
- `_eval_out/<phase>_smoke_v0/` 结构化产物
- 可选：本 phase 的 `PHASE_BRIEF.md` + `PHASE_RESULT.md`

**不依赖** Agent 左侧对话历史。

## 每个 phase 的标准流程

```text
1. 新建 Agent（Composer / Agent 模式）
2. 复制 docs/templates/PHASE_BRIEF_TEMPLATE.md → phases/<phase-id>/PHASE_BRIEF.md 并填好
3. 把 PHASE_BRIEF.md @ 进第一条消息（短 prompt，不要贴整段历史）
4. 跑 runner → verify → 更新 phase 文档 + verdict 表
5. 写 phases/<phase-id>/PHASE_RESULT.md（GO/NO-GO、checks、next phase）
6. 归档或删除本 phase 的 Cursor 聊天（可选）
```

## PHASE_BRIEF 写什么（保持一页以内）

| 区块 | 内容 |
|------|------|
| 目标 | 本 phase 只做什么 |
| 输入 | `_eval_out/...` 目录列表 + 必读的 json 文件名 |
| 输出 | capability / runner / verifier / `_eval_out/...` |
| 边界 | 禁止项（no runtime、no file read 等） |
| 验收 | verifier 阈值、final_decision 字符串、关键计数 |

## PHASE_RESULT 写什么

- `verifier` / `check_count`
- `final_decision` / `recommended_next_phase`
- 3–5 条结论（给人看）
- 指向 `_eval_out/.../summary.json` 与 `verifier_report.json`

## Cursor 左侧对话怎么「打包 / 清理」

### 在 Cursor UI 里

1. 左侧 **Chat / Agents** 列表里，对旧对话右键或悬停 → **Delete**（删 UI 条目）。
2. 本 phase 做完就 **New Agent**，不要继续在旧线程里发「继续」。
3. 需要留档：在对话里 **全选复制** 到 `phases/<phase-id>/CHAT_EXPORT.md`（可选，一般不必）。

### 技术归档（推荐）

对话原始数据在：

`~/.cursor/projects/<workspace>/agent-transcripts/<uuid>/`

打包脚本（Luna-Core 仓库内）：

```bash
cd /Users/luanlei/Desktop/Luna-Core
chmod +x scripts/archive_cursor_agent_transcripts.sh

# 保留当前会话 UUID 片段，只打包其余
KEEP_UUID=7973a276 ./scripts/archive_cursor_agent_transcripts.sh

# 确认 zip 无误后再删源目录，减轻 Cursor 索引负担
KEEP_UUID=7973a276 ./scripts/archive_cursor_agent_transcripts.sh --delete-after-zip
```

输出目录：`/Users/luanlei/Desktop/Luna-Core/_archive/cursor_agent_transcripts/`

每个会话一个 `*.zip` + `manifest.json`（含首条 user 摘要）。

### 当前工作区占用（参考）

- `Luna-Workspace-Min` agent-transcripts：约 54MB（多条超长 governance 线程）
- `Luna-Core` agent-transcripts：约 24MB

清理旧 zip 后，左侧列表仍要在 UI 里删一次，否则条目可能还在。

## 给 Cursor 的第一条消息模板

```markdown
请只根据 @phases/Phase-XXX/PHASE_BRIEF.md 执行本 phase。
不要依赖其它聊天历史。完成后更新 PHASE_RESULT.md 与 phase verdict 表。
```

## 下一 phase 示例

见 `phases/Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001/PHASE_BRIEF.md`。
