# Scenario Catalog

12 个场景均为 synthetic controlled inputs：

| ID | 行为类别 | Round 1 |
|---|---|---|
| 01 Single Clear Cue | single_path | 否 |
| 02 Unknown Exit | multi_path | 否 |
| 03 Signage and Human Flow Agree | multi_path / independent lineage | 否 |
| 04 Signage and Human Flow Conflict | conflict_preservation | 否 |
| 05 Signage Not Visible | governed_absence | 否 |
| 06 OCR Conditions Insufficient | unresolved_gap | 否 |
| 07 Multiple Unknowns | multi_path | 否 |
| 08 Deferred Branch | deferred_branch | 否 |
| 09 Rejected Branch | rejected_branch | 否 |
| 10 No Acquisition Strategy Available | governed_absence | 否 |
| 11 Irrelevant Environmental Change | stability_under_irrelevant_change | 是 |
| 12 Evidence Changes Cognitive Basis | cognitive_update | 是 |

Scenario 02/03/04/07 只提供多个显式 governed bases；不由 Sandbox 解释 signage、
human flow 或 spatial 的文本含义。Scenario 08/09 验证治理结果对 strategy formation
的局部隔离。Scenario 10 验证合法 Need/Branch 在无 basis 时保持 strategy=0。

Scenario 12 的 Round 1 仅把 synthetic coverage ref 注入现有认知链；是否收敛、
Branch 是否减少、Strategy 是否重复，均写入 trace 供人工 Cognitive Logic Review，
不由 verifier 预设。
