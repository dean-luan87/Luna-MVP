# Protocol and Information Channel Boundary v1

Information Channel Governance owns transport/channel rules such as producer,
consumer, routing, delivery, and channel-level trace requirements. Protocol
Governance owns contract identity, version, compatibility, lifecycle, and
change-control semantics.

Neither boundary owns the other. A channel can transport a valid protocol
without making the payload semantically correct or runtime-admissible.
