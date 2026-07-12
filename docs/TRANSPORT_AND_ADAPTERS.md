# Transport, Adapters and Journey Monitoring

Transport providers are integrated through reusable adapters. An adapter is created when a real planning or monitoring need appears, validated on bounded routes, and then retained for future journeys.

## Architecture

```text
Travel domain policy
→ Transport Gateway
→ Adapter Registry
→ provider adapter
→ official or reviewed source
```

Travel requests capabilities. Provider-specific fields do not leak into domain core.

## Adapter lifecycle

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

Validation is capability-specific. An adapter may support schedules while fares or live positions remain `UNSUPPORTED` or `UNKNOWN`.

## Transport coverage plan

Every candidate journey may produce a `TransportCoveragePlan` containing:

- countries and regions crossed;
- required national, regional, urban, coach, ferry, airline and airport providers;
- existing adapters and versions;
- missing adapters;
- minimum required capability;
- authentication and licence class;
- implementation and validation effort;
- fallback source;
- current health and data quality.

New adapters are implemented only for missing capabilities required by the route. Existing validated adapters are reused.

## Capability families

- stop and station search;
- planned departures, arrivals and journeys;
- realtime departures and arrivals;
- delay, cancellation, platform and route changes;
- disruption notices;
- fares, reservations and ticket rules;
- accessibility and station facilities;
- vehicle positions;
- booking reference links without booking authority.

## Source order

1. Official API.
2. Official GTFS, GTFS-Realtime, SIRI, NeTEx, GBFS or equivalent feed.
3. Official downloadable timetable or operator dataset.
4. Licensed aggregator.
5. Bounded official-site observation.
6. Community source as discovery evidence only.

Unofficial endpoints and site parsing are fallbacks, never presumed authority.

## Provider families

Initial reusable families include:

- German national rail and station/live-service sources;
- German regional transport unions and urban operators;
- national and regional rail in neighbouring countries;
- city transit networks;
- coach and ferry operators;
- airlines and airports;
- generic GTFS/GTFS-Realtime/SIRI/NeTEx/GBFS adapters.

Exact provider registration follows source, licence and capability review.

## Multimodal journey policy

Travel supports:

- local or regional feeder plus long-distance rail;
- long-distance rail plus local or regional continuation;
- high-speed rail out and regional return;
- regional out and high-speed return;
- rail plus coach or ferry;
- cross-border handoff at the last covered stop;
- open-jaw and different-station returns;
- night trains and intermediate overnight stays.

The planner compares one protected through ticket with split-ticket alternatives. It records whether a connection is protected, unprotected or unknown.

## Separate-ticket risk

Each segment records:

- contract or ticket group;
- fixed-train restriction;
- reservation requirement;
- minimum and chosen connection margin;
- missed-connection rights where known;
- last safe fallback;
- overnight or abandonment risk.

A cheaper split route is rejected when lost useful time, transfer risk or fallback cost removes the apparent saving.

## Live journey projection

Shared transport observations are projected into trip-specific state:

```text
planned journey
+ current delay/cancellation/platform data
+ ticket relationships
+ connection margins
→ connection risk
→ alternative journey proposal
```

Monitored signals may include:

- delay and early termination;
- cancellation;
- platform or stop change;
- missed-connection probability;
- replacement transport;
- accessibility outage;
- last safe return;
- route-wide disruption.

Monitoring is read-only and bounded to an approved journey reference. It stops after the relevant journey window.

## Normalized contracts

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

Every result carries source identity, retrieval time, freshness, evidence class, confidence and adapter version.
