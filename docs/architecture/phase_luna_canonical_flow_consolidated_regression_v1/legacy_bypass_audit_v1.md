# Legacy Bypass Audit v1

本回归只登记，不修复 legacy：

| surface | classification |
|---|---|
| A Route direct model/provider routing | SAFE_COMPATIBILITY |
| Task direct capability/provider routing | SAFE_COMPATIBILITY |
| FPO Need ownership | SAFE_COMPATIBILITY |
| Gateway direct source mutation | SAFE_COMPATIBILITY |
| Loop closure inference | SAFE_COMPATIBILITY |
| Dynamic Flow semantic disposition | NOT_IN_CURRENT_FLOW |
| navigation/speech shortcuts | SAFE_COMPATIBILITY |
| attention resource policy | SAFE_COMPATIBILITY |
| B1/B2 terminology | NOT_IN_CURRENT_FLOW |

本阶段 `active_bypass_count` 目标为 0；文档中的历史 overlap 不自动成为当前 flow blocker。

