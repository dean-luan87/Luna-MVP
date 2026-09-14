# MobileSAM Candidate Output Admission Policy V1

## Principle

Candidate output **may** enter runtime admission **review** only. It must **never** enter runtime, output adapter, semantic layer, fact layer, or navigation/speech directly.

## Required for Admission Review

| Field | Required |
|-------|----------|
| Schema / contract | yes |
| Source manifest | yes |
| Phase ref | yes |
| Model asset ref | yes |
| Confidence or quality summary | yes |
| Failure mode annotation | yes |

## Prohibited

- Direct fact write  
- User-visible output without output adapter gate  
- Navigation / action / speech trigger  
- Auto-promotion to `runtime_ready`

## MobileSAM Specific

- Output type: segmentation mask (candidate)  
- Not object label / semantic category  
- Prompt labels are test descriptions only
