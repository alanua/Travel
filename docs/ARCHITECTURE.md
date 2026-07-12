# Travel Architecture

Travel is a Skeleton domain composition. The canonical public-safe module inventory is `MODULES.yaml`.

## Core flow

```text
ExternalObservation
→ NormalizedSignal
→ CorrelatedSituation
→ DomainImpact
→ Proposal
→ ExplicitDecision
```

An observation or proposal does not become private canon automatically. Private canonical state requires the approved MemoryGateway route.

## Operating modes

```text
ANNUAL_MAP  = worldwide discovery and rolling opportunity windows
SHORTLIST   = current comparison and verification of selected options
BOOKING     = booking-ready proposal after explicit selection
```

The current repository does not authorize booking, payment, reservation, contact, cancellation or subscription changes.

## Travel-owned module groups

```text
Opportunity and lifecycle
├── Trip model
├── Opportunity Map
├── Global Discovery
├── Weekend Radar
├── Shortlist
└── Review proposals

Offer and product intelligence
├── Offer Intelligence
├── Stay Intelligence
├── Package Intelligence
├── Activity Intelligence
└── Source policy

Journey and logistics
├── Itinerary semantics
├── Transport Coverage Plan
├── Adapter Demand Planner
├── Journey Policy
├── Live Journey Projection
└── Trip Pack

Decision support
├── Total Cost Policy
├── Price History Policy
├── Scoring and Explanation
├── Document Gate
├── Risk Projection
└── Booking Record semantics
```

## Shared capability composition

Travel consumes shared Skeleton modules for calendars, schedules, tasks, notifications, acquisition, parsers, evidence, artifacts, maps, routing, tracker reads, documents, eligibility, finance, currency, weather, events, situational intelligence, memory, secrets, Runner/Loop, observability and approvals.

It must not duplicate those systems inside the Travel domain.

## Transport gateway

```text
Travel policy
    ↓
Transport Gateway
    ↓
Adapter Registry
    ├── national rail
    ├── regional transport unions
    ├── urban transport
    ├── coach and ferry operators
    ├── airline and airport sources
    └── GTFS / GTFS-Realtime / SIRI / NeTEx / GBFS
```

A new adapter is created only when required by an actual route or monitoring need. After bounded validation, it becomes reusable.

## Capability model

Providers declare support independently for:

- stop and station search;
- scheduled journeys;
- live departures and arrivals;
- delay, cancellation and platform changes;
- disruptions;
- fares, reservations and ticket rules;
- accessibility and station facilities;
- vehicle positions;
- safe booking references without booking authority.

Missing capability is `UNKNOWN` or `UNSUPPORTED`; it is never inferred.

## Evidence pipeline

```text
source observation
→ provenance and freshness receipt
→ travel-specific normalization
→ verification state
→ full-cost and logistics evaluation
→ annual-map or shortlist proposal
```

Confirmed, listed, indicative, historical, model-prior, estimate and unknown values remain distinct.

## Source order

1. Official API.
2. Official GTFS, GTFS-Realtime, SIRI, NeTEx, GBFS or equivalent feed.
3. Official downloadable timetable or dataset.
4. Licensed specialist or aggregator.
5. Bounded official-site observation.
6. Community source as discovery evidence only.

## Privacy and authority

- public repository: code, contracts, provider metadata, licences, synthetic fixtures and public-safe tests;
- private MemoryGateway: personal context, history, preferences, rankings, routes and decisions;
- encrypted artifact store: scans, PDFs, tickets, confirmations and sensitive snapshots;
- Secret Store Gate: typed opaque secret references and process-time injection.

Adapters are read-only by default. Every operation declares `READ_ONLY`, `PROPOSAL` or separately gated `APPROVED_MUTATION` authority.

## Detailed specifications

- `docs/DOMAIN_COMPOSITION.md`
- `docs/OPPORTUNITY_AND_LIFECYCLE.md`
- `docs/OFFER_INTELLIGENCE.md`
- `docs/TRANSPORT_AND_ADAPTERS.md`
- `docs/DATA_EVIDENCE_AND_SCORING.md`
- `docs/SITUATIONAL_INTELLIGENCE.md`
- `docs/PRIVACY_AUTHORITY_AND_SECRETS.md`
- `contracts/TRAVEL_CONTRACTS.md`
- `docs/ROADMAP.md`
