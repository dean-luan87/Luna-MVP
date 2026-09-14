# MobileSAM Output Adapter Exclusion Policy V1

## Status

`output_adapter_ready` = **false** (not granted by this planning phase)

## Requirements Before Output Adapter

- Separate request + owner approval  
- Candidate → output mapping contract  
- Human-readable result contract  
- User-visible output policy review  
- Error mode policy  
- Speech gate if speech channel involved  

## Prohibited

- `output_adapter_must_not_read_candidate_without_admission`  
- Reading trial candidate mask as final user output  
- Auto-mapping segmentation to navigation hints
