# Shared Contracts

Provider adapters normalize data into common transport and travel contracts.

Initial contract families:

```text
TransportStop
TransportRoute
TransportLeg
TransportJourney
FareObservation
TicketRule
LiveDeparture
LiveArrival
LiveVehiclePosition
TransportDisruption
ConnectionRisk
AlternativeJourney
AccessibilityStatus
SourceEvidence
```

Every observation must include source identity, retrieval timestamp, evidence class, freshness, and confidence. Provider payloads remain adapter-internal.

Contracts must not contain plaintext secrets or private identity/document fields.
