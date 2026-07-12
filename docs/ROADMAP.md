# Travel Implementation Roadmap

This roadmap records public-safe architecture and implementation order. It does not authorize live deployment, credentials, private-data import or external mutations.

## Current status

```text
PROJECT = ACTIVE_BOOTSTRAP
MODULE_INVENTORY = DOCUMENTED
LIVE_ADAPTERS = NOT_IMPLEMENTED
PRIVATE_MEMORY_BRIDGE = EXTERNAL_DEPENDENCY
BOOKING_AUTHORITY = NONE
```

## Dependency references

- `alanua/Skeleton#1750` — general module and composition contracts;
- `alanua/Skeleton#1748` — Travel domain boundary;
- `alanua/Skeleton#1747` — Offer Intelligence architecture;
- `alanua/Skeleton#1749` — fixture-only Offer Intelligence slice;
- `alanua/Skeleton#1545` — read-only WorldMonitor sensor;
- `alanua/Skeleton#1761` — secret-store boundary;
- `alanua/Travel#1` — this repository baseline.

## Phase 0 — architecture baseline

- maintain `MODULES.yaml` as the public-safe module inventory;
- document domain/shared/adaptor boundaries;
- define lifecycle, evidence, privacy and authority rules;
- keep all provider and implementation status explicit;
- no live network or private inputs.

## Phase 1 — core contracts and synthetic fixtures

- trip, itinerary, opportunity, offer and transport domain schemas;
- provider-neutral normalized records;
- source and module descriptors;
- lifecycle and evidence enums;
- deterministic synthetic fixtures;
- privacy-leak and failure-contract tests.

## Phase 2 — Offer Intelligence fixture slice

- source registry;
- saved public-safe fixtures;
- several independent fixture translators;
- normalization, lifecycle and conservative dedupe;
- exact versus `from`, per-person versus total, and missing-value tests;
- no live acquisition or browser execution.

## Phase 3 — transport gateway pilot

- generic stop, journey, live-update, disruption and ticket-rule contracts;
- one reviewed official national-rail adapter;
- one reviewed regional or urban transport adapter;
- capability-specific health and explicit unsupported states;
- bounded route validation using synthetic or public-safe test cases;
- no personal journey monitoring yet.

## Phase 4 — reusable adapter library

For each real planning need:

1. create a transport coverage plan;
2. identify existing adapters and capability gaps;
3. review official source, licence, authentication and limits;
4. implement only the missing adapter or capability;
5. validate against bounded current evidence;
6. retain the adapter for future routes;
7. add health, degradation and schema-change handling.

The same process applies to stays, packages, events, climate, documents and destination-cost sources.

## Phase 5 — private runtime integration

After Skeleton shared capabilities are ready:

- bind private profile and constraints through MemoryGateway references;
- bind approved secret references through the Secret Store Gate;
- store raw sensitive artifacts in the encrypted artifact store;
- connect approved scheduling, Runner/Loop and notification capabilities;
- add private observation warehouse and read-back verification;
- retain strict separation between observation, proposal and canon.

## Phase 6 — live planning and monitoring

- rolling annual opportunity map;
- weekend radar;
- current shortlist comparison;
- fare, stay and package rechecks;
- trip-specific live journey monitoring;
- alternative route and last-safe-return proposals;
- meaningful-change notifications only.

## Phase 7 — booking-ready trip packs

After explicit option selection:

- exact itinerary and safe margins;
- ticket, baggage, reservation and cancellation rules;
- accommodation and local transport plan;
- booking order;
- day plan and map-ready stops;
- warnings, etiquette and Plan B;
- booking records after external actions are separately approved and confirmed.

## Quality gates

Every implementation slice must verify:

- no private data or secret leakage;
- no provider-specific fields in domain core;
- evidence, retrieval time, freshness and confidence preservation;
- explicit stale, cached, fallback, simulated and unknown states;
- bounded timeouts, response sizes, redirects and rate limits;
- deterministic tests with network disabled in CI;
- independent adapter failure isolation;
- no automatic booking, payment, contact, cancellation or canon mutation.
