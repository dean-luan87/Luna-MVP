# GO / NO-GO Pack — Hardware Profile Capability Registry v1

## GO

- profile/camera/device/sensor schema + status enum + unknown profile + adapter placeholder  
- guardedtrial_allowed_now=false（预期）  
- 无 probe/camera/fact；verifier=GO

## NO_GO

- 探测硬件、调用 camera、guardedtrial_allowed_now=true、写 hardware fact/WM/routing change
