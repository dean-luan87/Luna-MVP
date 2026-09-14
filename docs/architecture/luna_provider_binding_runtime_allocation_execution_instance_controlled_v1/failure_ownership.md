# Failure ownership

需求/准备输入不完整归 requester/preparation owner；Provider 不可用或 eligibility
拒绝归 Provider Governance；Grant denied/expired/revoked/stale 归 Permission /
Admission Manager；资源不可满足归 Resource Governance；allocation failure 归
Runtime Executor/resource boundary；execution identity creation failure 归 Runtime
Executor；未来 session failure 归 Provider Runtime；Gateway rejection 归 Gateway；
evidence insufficiency 归 FPO。任何 owner 不能以 `UPSTREAM_INVALID` 洗掉自己 authority
范围内的失败。
