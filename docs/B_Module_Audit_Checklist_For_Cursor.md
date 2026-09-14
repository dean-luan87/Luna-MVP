B 模块改造 · 排查要求清单（给 Cursor 用）

目标：
找出 B 模块中所有“越权 / 混杂 / 不纯”的逻辑点
而不是立即修改。

---

一、排查总原则（先给 Cursor）

你可以先对 Cursor 说一句总指令：

“请在 B 模块中查找所有涉及：
决策、合规判断、过滤、优先级裁决、安全判断、历史反馈影响输出的逻辑。
不要修改代码，只列出位置和行为描述。”

---

二、第一类：候选“被提前否决”的逻辑（最重要）

Cursor 搜索目标

让 Cursor 重点找 所有直接 return / skip / continue / drop 的地方，尤其是带条件的。

关键词 / 模式
- return null
- return []
- continue
- break
- skip
- filter(
- if (...) return
- if (...) continue

判断标准（让 Cursor标注）
凡是满足以下任一条件的，都标记为问题点：
- 判断条件涉及：
- blocked
- illegal
- unsafe
- not_allowed
- forbidden
- 判断发生在：
- 候选生成过程中
- 而不是在 Gate / BC 中

👉 这些点 = B 在提前做裁决

---

三、第二类：硬编码“绝对规则 / 道德判断”

Cursor 搜索目标

找出所有 “永远不 / 必须不 / 禁止” 语义的逻辑。

关键词 / 语义
- never
- must_not
- forbid
- ban
- illegal
- violation
- policy
- rule
- ethic
- moral

重点关注
- 与场景强绑定的规则，例如：
- 草地 / 逆行 / 施工区 / 禁区
- 不依赖当前环境变化的判断

👉 这些都应当 从 B 中移出或降级为“假设”

---

四、第三类：B 读取了“它不该知道的状态”

Cursor 搜索目标

找出 B 是否 读取或依赖以下信息：

不允许出现的依赖
- Authority / 权限 / 等级
- Gate / Safety / Boundary
- SystemState / FailSafe / Degraded
- Calibration / Confidence / Health

关键词
- authority
- gate
- safety
- boundary
- health
- fail
- degraded
- mode

👉 只要 B 读取了这些，就是架构违规点

---

五、第四类：B 被“历史结果”污染的地方

Cursor 搜索目标

找出任何 B 根据过去结果调整当前输出 的逻辑。

关键词 / 模式
- last_result
- previous
- history
- feedback
- retry
- penalty
- reward
- score

特别注意
- “上次失败就不用这个方案”
- “成功率低就减少生成概率”

👉 这些应标记为 未来演化系统候选，不允许现在生效

---

六、第五类：B 在做“隐式优先级排序”

Cursor 搜索目标

找出 B 是否在输出阶段：
- 对候选排序
- 打最终优先级
- 只输出 Top-N（基于判断）

关键词
- sort
- rank
- priority
- best
- top
- select_best

判断标准
- 如果排序依据包含：
- 安全
- 合规
- 规则
- 是否可执行

👉 这是 BC 的职责，不是 B 的

---

七、第六类：B 的输出结构是否“夹带私货”

Cursor 搜索目标

检查 B 的输出对象 / DTO / struct：

不应该存在的字段
- is_valid
- is_safe
- allowed
- approved
- rejected_reason

应标注
- 字段名
- 被谁读取
- 是否影响下游逻辑

---

八、Cursor 输出格式要求（非常重要）

你要让 Cursor 统一按这个格式输出结果，否则后面很难用。

[ISSUE-ID]
- 文件路径：
- 行号范围：
- 问题类型：（提前裁决 / 规则硬编码 / 越权读取 / 历史污染 / 隐式排序 / 输出污染）
- 当前行为描述：
- 可能违反的架构原则：

👉 不要让 Cursor 给“修改建议”
我们下一步会自己做架构级处理。

---

九、这一轮排查完成后的状态

当 Cursor 把这轮结果给你后，你会得到：
- 一份 B 模块的“问题分布图”
- 明确知道：
- 哪些逻辑要删
- 哪些要降级
- 哪些要冻结
- 哪些是未来演化入口

这一步完成后，我们再进入真正的 B 改造动作，而且会非常快。

---

下一步（你做完这一步再回来）

等你拿到 Cursor 的排查结果后，我们下一步将只做一件事：

**把这些问题点，逐类转化为：
- 删除
- 降级为 assumption
- 移交给 BC
- 冻结为 future_evolution**

你不用急着想“怎么改”，
先把地雷标出来，这是工业级改造的第一步。
