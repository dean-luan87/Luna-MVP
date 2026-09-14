# Governance rule model

Canonical type：`GovernanceRuleV1`。

每条规则包含：`rule_ref`、name、owner、source、version、severity、domain、适用 owners/profiles/contracts、triggers、required/forbidden invariants、authority/responsibility pair、preflight/postflight flags，以及 candidate-only/read-only 标记。

每条 rule 至少引用 Constitution、Protocol 或 Architecture canonical source；unknown source、missing owner、missing version、orphan rule 均 fail closed。

第一版 severity 只有 `BLOCKER` 与 `WARNING`。Core registry 的规则为 blocker。
