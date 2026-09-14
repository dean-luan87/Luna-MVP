# A3 Controlled DryRun Regression Risk Register v1

| Risk | Level | Current control | Trigger | Owner candidate | Closure |
| --- | --- | --- | --- | --- | --- |
| Fixture schema drift | medium | static validation | fixture fields change | A3 owner | open follow-up |
| Enum expansion | low | controlled enums | enum changes | A3 owner | open follow-up |
| Contract drift | medium | Contract ref check | Contract changes | governance | open follow-up |
| Case mapping drift | medium | fixed mapping | fixture ID changes | A3 owner | open follow-up |
| Runner/verifier shared assumptions | medium | file-based verifier | check changes | verification owner | open follow-up |
| Warning taxonomy drift | low | expected-code list | new warning | A3 owner | open follow-up |
| Reference inventory drift | medium | closure summary | object refs expand | A3 owner | open follow-up |
| AnalysisQuestion evolution | low | current field sufficient | new object proposal | architecture | deferred |
| A2 runtime integration | high | explicitly excluded | runtime phase | A2/A3 governance | excluded |
| Model adapter boundary | high | AST/flags and exclusion | adapter proposal | capability governance | excluded |
