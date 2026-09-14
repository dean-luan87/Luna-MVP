# Owner Approval Governance Standard V1

## Required Patterns

- `owner_approval_required`  
- `owner_approval_granted_for_*_preparation`  
- `owner_approval_granted_for_*_execution_next`  
- `approval_not_execution_now`  
- `approval_not_runtime_approval`  
- `approval_not_output_adapter_approval`  
- `approval_not_semantic_approval`

## Scope Independence

Each action class requires **independent** approval scope:

| Action | Separate Approval |
|--------|-------------------|
| install | yes |
| download | yes |
| model-load | yes |
| inference | yes |
| runtime | yes |
| registry patch | yes |
| fact write | yes |

## Usage Note

Approval grants **only** the named next phase. It does not auto-expand to runtime, semantic, or broad readiness.

## Forbidden

- Implicit approval from unrelated upstream GO  
- Single approval covering install + runtime + fact write  
- Treating readiness planning as execution approval
