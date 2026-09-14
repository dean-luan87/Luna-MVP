# Preflight / Postflight

Preflight：profile、registry、applicable rule set、authority/responsibility pairs、profile-declared refs、protocol refs 和 boundary consistency 必须通过，否则 Phase engine 不应执行，状态为 `GOVERNANCE_PREFLIGHT_BLOCKED`。

Postflight：验证 candidate-only/read-only/truth/runtime/mutation/authoritative-effect flags。违反规则时返回 `GOVERNANCE_POSTFLIGHT_BLOCKED`。

本阶段 evaluation runner 只生成 controlled artifact；实际 verifier 才形成最终决策。
