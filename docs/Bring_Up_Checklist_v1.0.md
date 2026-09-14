# Luna 系统接通清单（Bring-Up Checklist v1）

使用方式：
- 每一项只回答 DONE / NOT DONE
- 未 DONE 不允许进入后续相关项
- 所有模块最终都必须能在 Trace / DebugView 中看到痕迹

---

## A. 运行骨架与观测（System Skeleton）
- 系统主循环（tick / event-driven）已固定
- DebugView 可持续输出（jsonl）
- Trace / Decision 记录不中断
- 最小 fixtures 可运行（无真实输入也可跑）
- system_snapshot 结构已冻结（哪怕字段为空）

### A 模块 Gate（进入 B 的硬门槛）
- 系统在无任何真实输入下可连续运行 ≥30 分钟
- 每个 tick 都有 trace 记录
- system_snapshot 结构稳定、不随意改
- fixtures 可复现一次完整运行
- 现在往系统里“塞任何模块”，都只需要读/写 snapshot

---

## B. 文本生成与语音输出（Language Output）

### B1. 文本生成（NLG v0）
- 文本生成模块存在（非固定文案）
- 支持模板 + slot 填充
- 支持 3 类文本：
  - 状态反馈
  - 决策解释
  - 任务指令
- 文本生成受策略控制（不是随时说话）
- 文本生成输出进入 Trace

### B2. 语音输出（TTS）
- TTS 可播报任意文本
- 不再依赖固定文案
- 支持打断 / 排队策略之一
- 播报行为可在 Trace 中回放

---

## C. 任务引擎（Task System）
- TaskEngine v0 存在
- Task 有明确状态机（pending / active / completed / failed）
- Task 可读取 system_snapshot
- Task 状态变化进入 Trace
- Task 输出统一走文本生成 → 语音

---

## D. 指令入口（Command Input，非语音）
- Command Router 存在
- 指令不会绕过 C / BC
- 指令只产生意图，不直接执行动作
- 指令触发任务或状态切换
- 系统会语音确认指令结果

---

## E. 视觉输入总线（Vision Runtime）
- 摄像头帧流接入
- 帧时间戳稳定
- 感知健康状态写入 system_snapshot
- 感知丢失/降级可触发语音反馈
- 视觉输入不直接触发决策（必须经 snapshot）

---

## F. 即时危险（C 模块接通）
- 即时危险事实写入 system_snapshot
- 至少 2 类危险可触发：
  - 感知失败
  - 障碍过近
- C 决策只读 snapshot
- STOP / HOLD 可真实生效
- 危险决策可解释（DebugView）

---

## G. OCR（在此步才引入）
- OCR 引擎已接入
- OCR 输出结构化（text / confidence / timestamp）
- OCR 写入 system_snapshot
- OCR 不直接播报（经 Task / NLG）
- “读文字”任务可完整跑通

---

## H. 离线地图（Offline Map）
- 离线地图数据可加载
- 地图可在无网络环境使用
- 地图数据写入 system_snapshot
- 地图仅作为环境事实（不直接决策）
- 地图变化可被任务读取（如“接近路口”）

---

## I. GPS / 定位（Location）
- GPS 数据接入
- 定位状态（ok / weak / lost）写入 snapshot
- 位置变化有时间连续性
- GPS 丢失可触发语音反馈
- GPS 不直接控制行为（经 B / Task）

---

## J. 任务清单能力（逐个上线）

### J1. 红绿灯任务
- 红/绿状态写入 snapshot
- 状态变化可被任务观察
- 语音提示符合“助手口吻”

### J2. 楼层到达任务
- 楼层信息写入 snapshot
- 到达事件可被检测
- 到达后任务可完成/切换

### J3. 电梯按钮任务
- 按钮面板被识别为事实
- 目标楼层可生成指令文本
- 可确认“是否已按下”

### J4. 出入口任务
- 出入口/EXIT 信息写入 snapshot
- 可生成方向性任务
- 错误方向可纠偏

---

## K. 本地小模型（适度复杂对话）

必须在前面全部稳定后

- 本地模型接入
- 模型仅用于文案润色 / 对话
- 模型不产生执行指令
- 模型输出经过策略过滤
- 模型输出可回溯（trace）

---

## L. 语音输入（ASR，最后接）
- ASR 引擎接入
- ASR 输出只进入 Command Router
- 错识别有确认机制
- ASR 不绕过 C / BC
- ASR 可被关闭/降级

---

## M. 阶段完成判定（必须全部满足）
- 系统连续运行 ≥30 分钟
- 任一行为都可解释
- 任一任务都可回放
- fixtures 可复现至少 1 个完整流程
- 无模块“偷偷直连执行层”

---

使用建议（给你一句实话）
- 不要一次勾太多
- 每完成一个 Section（A/B/C…），就跑一次完整流程
- 不通过验收，禁止进入后续 Section
