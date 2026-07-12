# Travel Architecture

## Core flow

```text
ExternalObservation
→ NormalizedSignal
→ CorrelatedSituation
→ DomainImpact
→ CanonicalDecision
```

The public repository implements reusable code and public-safe contracts. Personal planning state, private observations, derived rankings, and decisions remain behind the Skeleton private-memory boundary.

## Main modules

```text
Opportunity Map
Weekend Radar
Transport Gateway
Provider Adapter Registry
Fare and Stay Observation
Journey Planner
Live Journey Monitor
Risk and Document Gates
Costing and Comparison
```

## Transport gateway

All provider adapters normalize their output into shared contracts instead of exposing provider-specific payloads to the planning layer.

```text
Travel Module
    ↓
Transport Gateway
    ↓
Adapter Registry
    ├── national rail
    ├── regional transport unions
    ├── urban transport
    ├── coach and ferry operators
    └── standard GTFS / GTFS-Realtime sources
```

A new adapter is created only when required by an actual route or monitoring need. After bounded validation, it becomes reusable for future journeys.

## Capability model

Each provider declares support independently for:

- stop and station search;
- scheduled journeys;
- live departures and arrivals;
- delays, cancellations, and platform changes;
- disruptions and service notices;
- fares and ticket rules;
- accessibility;
- vehicle positions;
- booking links or references.

Missing capability is reported as `UNKNOWN` or `UNSUPPORTED`; it is never inferred from another provider.

## Source priority

1. Official API.
2. Official GTFS, GTFS-Realtime, SIRI, NeTEx, GBFS, or published feed.
3. Official downloadable timetable or operator data.
4. Licensed aggregator.
5. Bounded official-site observation.
6. Community source as discovery evidence only.

## Safety boundary

Adapters are read-only by default. Booking, payment, reservation, cancellation, contact, account changes, or subscription changes require a separately approved write path and explicit user confirmation.
