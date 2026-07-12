# Travel Domain Composition

Travel is a Skeleton domain composition. It owns travel entities, lifecycle, policies and composition recipes. It does not own generic system capabilities.

Source architecture:

- `alanua/Skeleton#1750` — general modular architecture;
- `alanua/Skeleton#1748` — Travel domain composition;
- `alanua/Skeleton#1747` — Offer Intelligence;
- `alanua/Skeleton#1749` — fixture-only first slice.

## Travel-owned semantics

Travel owns:

- trip, itinerary, segment and trip-pack records;
- opportunity-map and weekend-radar lifecycle;
- travel-offer, transport, stay, activity and package domain records;
- travel-specific total-cost and useful-time policies;
- travel-specific scoring, explanation and false-bargain rejection;
- document-blocker and risk-projection semantics;
- review, approve, reject, defer and recheck proposals;
- booking-record semantics after explicit approval.

## Shared Skeleton capabilities

Travel consumes provider-neutral Skeleton capabilities for:

- calendars, schedules, tasks, workflows and notifications;
- acquisition, parsing, evidence, provenance and artifacts;
- geo, maps, routing and tracker reads;
- document rules and eligibility checks;
- finance, currency and generic value calculations;
- weather, events, disasters and situational intelligence;
- entity resolution, search and retrieval;
- MemoryGateway, private artifact storage and secret references;
- Runner, Loop, observability, approvals and action gates.

Travel must not create a second scheduler, parser framework, map store, task queue, memory database, audit log, secret vault or notification subsystem.

## Provider boundary

Domain code requests capabilities and does not import provider SDKs directly.

```text
Travel policy
→ shared capability contract
→ environment and policy resolution
→ provider adapter
→ external source
```

Provider-specific payloads remain behind adapters. A provider result cannot silently gain more authority during composition: an estimate remains an estimate, a parsed observation remains unverified, and an external status does not become private canon automatically.

## Side-effect classes

Travel operations are classified as:

- `READ_ONLY` — research, lookup, parsing and monitoring;
- `PROPOSAL` — shortlist, alert, recheck, itinerary or booking-order proposal;
- `APPROVED_MUTATION` — separately gated external action after explicit authorization.

The repository currently defines only read-only and proposal behavior. Booking, payment, reservation, contact, cancellation and subscription changes are outside the current authority boundary.

## Failure rules

- unknown capability, version, privacy class or authority fails closed;
- one failed adapter must not stop unrelated modules;
- missing evidence is `UNKNOWN`, never guessed;
- stale, fallback, cached, estimated and simulated states remain explicit;
- private inputs are referenced by bounded IDs and are not copied into public code or fixtures.
