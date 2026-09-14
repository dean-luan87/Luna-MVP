# Implementation Boundary Plan（Architecture Only）

1. 旧模块保持 canonical；本阶段只建立映射注册表和适配边界。
2. 未来实现顺序：参数只读注册 → 函数输入/输出适配 → 受控候选评估 → Runtime 批准后的有限更新。
3. 不在本阶段修改模块代码、连接 Hive、执行参数学习或替换 State Machine。
4. 每次实际变化必须经过 Architecture Change Governance、Self Review、Constitution 和独立验证。

