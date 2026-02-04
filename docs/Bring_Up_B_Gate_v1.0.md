✅ B 部分验收 Checklist / Gate（Language Output）

Gate 规则：
任何一项 NOT DONE → B 阶段未完成 → 不允许进入后续模块

---

B-F｜功能正确性（Functional）
- 系统中 不存在任何直接写死字符串播报
- 所有语音输出 100% 经过 Text Generator
- Text Generator 可独立调用（无 OCR / 无任务 / 无危险也能生成文本）
- 不同事件类型命中不同模板（状态 / 解释 / 指令）
- 模板 slot 可变，不是固定句式
- 模板缺失时有 fallback 文本

---

B-A｜架构约束（Architecture）
- 系统中 只有一个语音输出入口
- 无模块绕过 Text Generator 直接调用 TTS
- Text Generator 不直接调用执行层
- TTS Executor 不参与模板选择或决策
- 文本生成策略（什么时候说）与模板内容解耦

---

B-S｜稳定性（Stability）
- 启用 B 后系统可连续运行 ≥30 分钟
- 无语音死循环（重复说同一句）
- 无语音阻塞主循环（TTS 不拖慢 tick）
- 多次触发播报时行为可预测（排队或打断）
- 高优先级播报可覆盖低优先级播报（规则级即可）

---

B-T｜可审计性（Trace / Debug）
- 每一次播报在 Trace 中都有记录
- Trace 中至少包含：
  - 文本内容
  - 文本类型（状态 / 解释 / 指令）
  - 触发来源（事件 / 任务 / 决策）
  - 时间戳
- 可从 Trace 回放系统“说过的话”
- Trace 中 不出现 BC / C 内部决策结构

---

B-U｜用户感知（User Reality Check）
- 文案听感 不像传统地图导航腔
- 至少 5 条播报听起来像“助手在说话”
- 关键状态变化 ≤1 秒内有语音反馈
- 用户只听语音即可判断：
  - 系统在做什么
  - 为什么这么做
  - 是否处于安全状态

---

❌ 禁止项（命中即 Fail）
- ❌ 任意硬编码播报字符串
- ❌ 播报不写入 Trace
- ❌ 语音模块影响主循环节奏
- ❌ 文本生成绕过策略层
- ❌ 播报内容与系统状态明显不一致

---

🛑 B 阶段 Gate 判定
- B-F 全部 DONE
- B-A 全部 DONE
- B-S 全部 DONE
- B-T 全部 DONE
- B-U 全部 DONE
- 未命中任何禁止项

➡ 全部勾选后：B = DONE，允许进入 C / Task / OCR

---

建议用法（工程实践）
- 把本 Checklist 作为 Cursor Milestone Gate
- 每次修改 B 相关代码，必须重新跑一遍 Gate
- Gate 不通过，禁止合并后续模块
