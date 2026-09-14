# Model Provisioning, Registration, and Lifecycle v1

Conceptual provisioning path:

`external asset discovered → provisioning candidate → governance review →
registration → integrity registration → declared asset available`

Provisioning is metadata/change governance, not a downloader. Registration,
metadata update, declared checksum, version replacement, source provenance,
and mapping update belong to Model Governance. Lifecycle may conceptually be
candidate → registered → available-declared → deprecated → superseded/retired.

Observed runtime health remains a separate domain. No automatic upgrade or
hot-swap is introduced.
