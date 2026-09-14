# Authority / Responsibility Regression v1

每个 composed case 都记录 `owner_chain` 与 `responsibility_chain`。Harness 只检查连续性，不重新授予权限。

Translation/adapter correctness 由对应 adapter 负责；Field、Current World、Brain、Task、Action、Provider、Capability、Model 等 source/semantic/execution owner 不被父 Harness 接管。

