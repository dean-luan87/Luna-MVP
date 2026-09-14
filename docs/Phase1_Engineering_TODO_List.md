Phase-1 工程改造 TODO 清单

目标：让现有系统“符合新宪章”，而不是重写系统

原则：
- 先 接入 Authority / SoftNorm / BC 裁决顺序
- 不碰 C 自治
- 不做演化、不做评分
- 所有改造 可回滚

---

一、全局必做（不改代码也要先做）

TODO-G-1：冻结新文档为工程基线（必须先做）

动作
- 将《BC / Authority / Soft-Norm 运行宪章》存入工程文档
- 标注为：
- ARCH_SPEC/FROZEN
- IMPLEMENTATION MUST FOLLOW

目的
- 防止 Cursor / 人继续“凭感觉写逻辑”
- 后续所有改造都能对照检查

---

二、B 模块改造 TODO（第一优先级）

目标一句话：
让 B 只负责“生成候选”，不再隐性做裁决或规则判断。

---

TODO-B-1：清点 B 当前“越权行为”（必须做）

你要检查 B 里是否存在：
- ❌ 直接判断可不可走
- ❌ 内嵌安全规则（例如硬编码避让）
- ❌ 内嵌道德判断（比如“绝对不能”）
- ❌ 根据历史结果自调行为

处理原则
- 不删逻辑
- 先 标记为 legacy_decision_path

---

TODO-B-2：统一 B 的输出接口（非常关键）

目标接口（示意）

BCandidate {
  action_id
  action_type
  geometry / path
  cost_estimate        // 代价评估（非对错）
  assumptions          // 环境假设
  confidence           // B 自信度
  explanation          // 可解释文本
}

工程要求
- B 只输出“候选”
- 不输出：
- allowed / forbidden
- 优先级裁决
- 是否合规

---

TODO-B-3：禁止 B 直接感知 Authority / Gate

硬规则
- B 不读取 AuthorityLevel
- B 不读取 Gate 状态
- B 不知道自己会不会被采纳

👉 B 必须是“盲生成器”

---

TODO-B-4：为未来演化预留字段（但不启用）

BCandidate.meta = {
  model_id,
  version,
  tags,          // 例如 experimental
}

⚠️
- 只记录
- 不参与裁决
- 不影响输出

---

三、BC 模块改造 TODO（核心工程）

这是整个改造的重心。

---

TODO-BC-1：重构 BC 入口顺序（最重要）

旧逻辑（常见问题）

B 输出 → BC 混合判断 → Gate

新逻辑（写死）

SystemSnapshot
    ↓
resolveAuthority()
    ↓
裁剪 BC 能力（Ability Mask）
    ↓
BC Arbitration
    ↓
Hard Gate

👉 Authority 一定在 BC 裁决之前

---

TODO-BC-2：实现 resolveAuthority()（纯函数）

要求
- 只读 SystemSnapshot
- 不读 B / C
- 不读历史
- 不可写状态

这是 BC 的“天花板计算器”

---

TODO-BC-3：实现 BCAbilities 裁剪器

BCAbilities = maskByAuthority(authority)

作用
- 在代码层面：
- 禁止某些分支执行
- 而不是“逻辑上不走”

这是防未来误用的关键工程点。

---

TODO-BC-4：把“塑形”从规则里拆出来

检查 BC 中是否存在：
- 长期参数调节
- 行为风格累积
- “最近常这样就继续这样”

改造为
- Shaping = 运行态调制
- 必须带 TTL
- 自动失效

---

TODO-BC-5：实现 Override 的“硬门槛”

Override 必须满足 4 个条件全部为真：
1. Authority ∈ {A3, A4}
2. 环境假设失效
3. 代价反转
4. 不触及 ABSOLUTE_FORBIDDEN

工程要求
- Override 作为显式路径
- 不能是 if/else 漏洞

---

TODO-BC-6：BCSnapshot 强制落盘（不进主链）

每次裁决必须生成：

BCSnapshot {
  authority
  bc_state
  used_candidates
  overridden_norms
  shaping_applied
  execution_result
}

用途
- 只给后台
- 不反向影响运行

---

四、Gate 模块（只校验，不改逻辑）

TODO-GATE-1：Gate 与 Authority 解耦
- Gate 不知道 Authority
- Gate 只做硬边界

避免未来出现：

“Authority 高了就放过 Gate”

---

五、系统级 TODO（为后续 C / 演化铺路）

TODO-SYS-1：SystemSnapshot 标准化

确保 Snapshot 包含：
- PerceptionState
- CalibrationState
- ControlDistortion
- HardwareState
- RiskLevel
- ContextMode

Authority 只读这里

---

TODO-SYS-2：Fail-Safe 行为统一出口
- A5 时：
- 不裁决
- 不导航
- 明确告知用户

宁可不可用，不可误导

---

六、明确“现在不做的事”（防 scope creep）

🚫 本阶段不做：
- C 模块自治
- 评分系统接入
- 演化算法
- 多模型调度
- 用户偏好学习

👉 现在的目标只有一个：
让系统“跑在正确的轨道上”。

---

七、改造顺序建议（非常实用）
1. 文档冻结（已完成）
2. B 输出接口收敛
3. BC 入口顺序改造
4. resolveAuthority + Ability Mask
5. Override / Shaping 拆分
6. Snapshot 落盘

每一步都 可单独测试、可回滚。

---

下一步你可以直接选

下一条我们可以立刻进入实操，你选一个：
1. 把 TODO-B 拆成具体代码改造点
2. 给出 BC 裁决入口的伪代码（带 Authority / Ability Mask）
3. 对照你当前工程结构，给出“文件级修改建议”

你现在这个节奏是对的：
先把 TODO 钉死，再一个一个啃。
