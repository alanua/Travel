# Travel

Public-safe code, contracts, provider metadata, reusable adapters and architecture for the Travel opportunity-planning and logistics domain.

## Purpose

Travel supports worldwide opportunity discovery, rolling annual-map maintenance, weekend and day-trip radar, live shortlist comparison, multimodal route planning, full-cost evaluation, booking-ready trip packs and live journey monitoring.

Research, monitoring and shortlisting create options, not commitments. Booking, reservation, payment, contact, cancellation and subscription changes require a separately approved path and explicit authorization.

## Canonical public-safe inventory

- `MODULES.yaml` — machine-readable Travel module inventory and shared Skeleton dependencies;
- `docs/DOMAIN_COMPOSITION.md` — Travel-owned semantics and shared capability boundaries;
- `docs/OPPORTUNITY_AND_LIFECYCLE.md` — annual map, weekend radar, modes and statuses;
- `docs/ACCESS_AND_ROUTE_POLICY.md` — door-to-door access, airport, rail and surface-transport policy;
- `docs/OFFER_INTELLIGENCE.md` — offer discovery, normalization, verification and dedupe;
- `docs/TRANSPORT_AND_ADAPTERS.md` — transport gateway, reusable adapters and live monitoring;
- `docs/DATA_EVIDENCE_AND_SCORING.md` — evidence classes, warehouse, baselines, costing and scoring;
- `docs/SITUATIONAL_INTELLIGENCE.md` — bounded read-only risk and disruption sensor boundary;
- `docs/PERSONALIZATION_MONITORING_AND_OUTPUT.md` — private personalization, rechecks and outputs;
- `docs/PRIVACY_AUTHORITY_AND_SECRETS.md` — public/private/artifact/secret separation;
- `docs/ROADMAP.md` — staged implementation and dependency gates;
- `contracts/TRAVEL_CONTRACTS.md` — provider-neutral domain contract catalogue.

The baseline is tracked in `alanua/Travel#1` and derives from the public-safe Skeleton architecture in `alanua/Skeleton#1750`, `#1748`, `#1747`, `#1749`, `#1545` and `#1761`.

## Public/private boundary

This repository may contain:

- generic architecture and deterministic code;
- reusable transport, accommodation, package, climate, event, safety and price-observation adapters;
- provider-neutral contracts;
- public provider identifiers, licences, coverage notes and source-health metadata;
- synthetic fixtures and public-safe tests.

This repository must not contain:

- personal travel history, preferences, budgets, watchlists, rankings or route candidates;
- raw tracks, live/home locations or private calendars;
- passport, visa, residence, family, booking, ticket, payment or document-number data;
- private price observations or derived personal decisions;
- API keys, credentials, cookies, tokens or secret values.

Private context belongs behind Skeleton MemoryGateway. Sensitive files belong in the approved encrypted artifact store. Secrets belong in the provider-neutral Secret Store Gate and are referenced only through typed opaque references.

## Adapter strategy

Provider-specific adapters are added when a real planning or monitoring need appears, validated on bounded routes, and retained for reuse.

```text
REQUIRED_FOR_TRIP
→ SOURCE_RESEARCH
→ PROTOTYPE
→ VALIDATED_FOR_ROUTE
→ ACTIVE_FOR_TRIP
→ REUSABLE_ADAPTER
→ MAINTAINED
→ DEGRADED | RETIRED
```

Travel requests capabilities rather than concrete providers. Official APIs and official GTFS/GTFS-Realtime/SIRI/NeTEx/GBFS sources are preferred. Unsupported, stale, fallback, estimated and simulated states remain explicit.

## Current status

```text
PROJECT = ACTIVE_BOOTSTRAP
MODULE_INVENTORY = DOCUMENTED
LIVE_ADAPTERS = NOT_IMPLEMENTED
PRIVATE_RUNTIME = NOT_CONNECTED
BOOKING_AUTHORITY = NONE
```
