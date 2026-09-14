# Minimum Sufficiency

Provider `SUCCESS` 只表示真实观察动作完成并产生合法 native output；它不表示
Goal 已满足。

实际 sufficiency 由 CState Formation 根据 `required_information_refs` 与真实
结果派生的 `available_information_refs` 计算；当 Runtime ingress 提供
Evidence-to-information support binding 时，只有 relevance 为 `RELEVANT` 的
Evidence 才能把其声明的 information refs 纳入 coverage。跨轮的既有 coverage
通过 inherited information refs 保留，不会被错误归属于新 Evidence：

- Case A：真实非空 text candidate 覆盖唯一 requirement 后为 `SUFFICIENT`；
- Case B Cycle 1：仅 station candidate 可用，platform requirement missing，
  因而为 `INSUFFICIENT`；
- Case B Cycle 2：真实 platform candidate 加入前一轮 available information 后，
  两个 requirements 都可用，形成 `SUFFICIENT`。

空结果不提供 information ref；它不会被提升为 fake Evidence，也不会被误报为
Provider unavailable。若最终仍 insufficient，Runner 保留该结果并停止在两轮
预算内，不制造成功结论。
