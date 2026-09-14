# AUTHORITY_RESPONSIBILITY_UNITY

`GovernanceAuthorityResponsibilityRecordV1` 显式记录 module、owner、authority、responsibility、decision/failure types 和 authority→responsibility mapping。

验证规则：

- authority 无配对 responsibility：`AUTHORITY_WITHOUT_RESPONSIBILITY`
- responsibility 无配对 authority：`RESPONSIBILITY_WITHOUT_AUTHORITY`
- authority 没有 owner：`AUTHORITY_OWNER_MISSING`
- 同一 authority 被不同 owner 声明：`AUTHORITY_COLLISION`
- responsibility owner 与 record owner 不一致：`RESPONSIBILITY_OWNER_MISMATCH`

CALL permission、trace/provenance ownership 不被视为 semantic authority。
