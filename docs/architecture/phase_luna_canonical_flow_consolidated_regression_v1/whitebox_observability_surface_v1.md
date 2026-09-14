# White-box Observability Surface v1

每个 composed transition 暴露：`attempt_id`、`transition_id`、`trace_id`、parent refs、Concern、owner/responsibility chain、transition classes、input/output refs 与 versions、constraint/evidence/provenance/invalidation refs、failure/next target，以及 candidate/runtime/source-mutation flags。

这些是后续 White-box contract 的数据要求，不是 UI，也不引入新的 observability owner。

