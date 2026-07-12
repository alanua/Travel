# Opportunity Map and Lifecycle

Travel maintains options rather than commitments. Research, monitoring and shortlisting may create proposals, but only explicit operator selection can move an option into planning and booking-record states.

## Operating modes

### ANNUAL_MAP

Maintains a rolling twelve-month worldwide opportunity map. It records best and cheapest windows, shoulder and avoid periods, route format, expected duration, full-cost range, useful days, lead time, deadline, risks, document state, confidence and next review.

### SHORTLIST

Performs live comparison of selected candidates. It rechecks current prices, availability, schedules, baggage, stay terms, route quality, disruptions, documents, weather and total cost.

### BOOKING

Produces a booking-ready journey only after explicit selection. It may generate booking order, exact segments, safe margins, ticket rules, stay requirements, day plan, alternatives and Plan B. It does not itself purchase, reserve, contact, cancel or pay.

## Opportunity lifecycle

```text
RESEARCHED_OPTION
→ WATCH
→ WINDOW_APPROACHING
→ ACTION_RECOMMENDED
→ STRONG_SHORTLIST
→ SHORTLISTED
→ PLANNED
→ BOOKED
→ COMPLETED
```

Exceptional states:

```text
DOCUMENT_BLOCKER
RISK_RISING
TEMPORARILY_DOWNGRADED
REJECTED
EXPIRED
```

Only approved private runtime state may use `PLANNED`, `BOOKED` or `COMPLETED`. Public fixtures use synthetic examples only.

## Radar semantics

Every opportunity window is classified as:

```text
DISTANT
APPROACHING
OPEN
CLOSING
EXPIRED
```

A radar result explains:

- why the window matters;
- what changes if the operator waits;
- what uncertainty remains;
- the minimum safe next action;
- whether the result is only research, a watch, or a proposal for action.

## Global discovery

Discovery is worldwide. Nearer destinations may receive cost and access advantages, but Europe or any named destination list must not become a hard search boundary.

Discovery may include:

- countries, regions, islands and secondary cities;
- seasonal or newly announced routes;
- fare drops and package anomalies;
- festivals, exhibitions and natural phenomena;
- rail, night-train, bus, ferry and road corridors;
- stopovers, open jaws and different-airport returns;
- wildcard options that outperform familiar candidates.

Named destinations are research signals, not commitments or exhaustive scope.

## Weekend radar

Weekend Radar is a parallel short-trip layer rather than a reduced annual-map entry.

Supported forms:

```text
DAY_TRIP
OVERNIGHT
FRI_SUN
THU_SUN
BORDER_HANDOFF
REGIONAL_FEEDER_PLUS_LONG_DISTANCE
LONG_DISTANCE_OUT_REGIONAL_BACK
REGIONAL_OUT_LONG_DISTANCE_BACK
```

It evaluates:

- door-to-door time;
- useful hours at destination;
- nights and leave days used;
- full marginal cost;
- transfer count and reliability;
- last safe return;
- separate-ticket exposure;
- whether an extra day materially improves price, route quality or destination value.

A free or already-held local ticket does not make a slow route automatically superior. Useful-time gain and connection risk are first-class decision inputs.

## Route formats

Travel supports:

- round trip;
- open jaw;
- multi-country linear route;
- rail out and fly back;
- fly out and rail back;
- different-airport return;
- rail-core journey;
- night trains;
- buses and ferries;
- road trips;
- packages.

The scorer penalizes rushed pace, excessive transfers, poor useful-time yield and false savings. It does not penalize route width by itself.
