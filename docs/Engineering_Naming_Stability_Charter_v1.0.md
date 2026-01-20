# Engineering Naming Stability Charter v1.0

## 目的
防止系统进入演化期后，被规划文档 / Issue / Cursor 反向破坏稳定性。

## 适用范围（冻结对象）
本公约适用于以下模块（当前已进入演化期）：
- BC
- `output_controller/`
- `authority.py`
- `ability_matrix.py`
- `debug_view.py`
- C
- `instinct_controller/`
- Risk Center（危险感知中台）
- `risk_center/`
- `risk_layer/`
- `interfaces/bus.py`
- 调试 / 回放 / 对比工具
- `tools/debug/*`

## 命名优先级规则
当出现冲突时，按以下优先级裁决：
1. 运行中代码路径（最高优先级）
2. pytest 覆盖的 import 路径
3. CLI 工具实际调用路径
4. 文档中已有引用
5. Issue / TODO / 规划脚本（最低优先级）

结论：Issue 不得反向要求已稳定模块改名。

## 等价实现处理规则
当出现如下情况：
- 设计中叫 `envelope_bus.py`
- 实现中为 `interfaces/bus.py`
- 行为、接口、测试完全一致

唯一允许的做法：
- 保持现有文件名
- 在文件头部增加 Alignment 注释
- 在文档中维护“命名对照表”

明确禁止：
- 为对齐 Issue 批量改名
- 在无收益情况下做全仓迁移
- 让 Cursor 自动 refactor 命名

## 软别名策略（仅在必要时）
只在以下情况下使用软别名：
- 外部脚本无法修改
- 历史工具依赖旧路径

示例（允许）：
```python
# risk_center/interfaces/envelope_bus.py
from .bus import *
```

规则：
- 只 forward
- 不加逻辑
- 不新增测试依赖

## Debug / 可视化模块特殊规则
DebugView / CLI 工具命名允许“语义优先于结构”：
- `dump_bc_snapshots.py` ✅ 合理
- 不强制要求 `dump_debug_view.py`
- 工具名以“用户理解成本最低”为准

## 冻结声明
从本阶段起，任何涉及 BC / C / Risk 的命名变更，
必须以“演化收益 > 稳定性成本”为前提，否则一律拒绝。
