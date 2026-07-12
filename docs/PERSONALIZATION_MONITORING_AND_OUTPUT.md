# Personalization, Monitoring and Output

Travel separates generic public-safe domain logic from private runtime context.

## Personalization projection

Private inputs may include:

- confirmed travel history;
- visited-place and trip-format history;
- confirmed preferences and dislikes;
- pace, duration and climate tolerance;
- transport, night-travel and transfer tolerance;
- accommodation and cleanliness requirements;
- food, architecture, design, nature and market interests;
- temporary trip-specific requests;
- leave windows, budget and document constraints.

These values remain behind MemoryGateway. Public code defines only schemas, rules and synthetic fixtures.

The system distinguishes:

```text
CONFIRMED_FACT
TEMPORARY_REQUEST
INFERENCE
UNKNOWN
```

An inference cannot silently replace a confirmed fact. Corrections and explicit feedback override prior inferences.

## Repetition policy

A visited city does not automatically mark an entire country or region as covered. Repeats may remain valuable when the season, region, route format, event, gastronomy or activity is materially different.

The private runtime supplies the visited-place canon and repetition weights. Public code contains no personal destination list.

## Monitoring policy

Active options and blocked options may be rechecked when relevant inputs change:

- prices or availability;
- schedules and capacity;
- entry, transit or document rules;
- safety, weather or disaster state;
- strikes, closures and disruptions;
- events and seasonal conditions;
- deadlines and booking conditions.

Monitoring must:

- use the shared Skeleton scheduler and Loop rather than a Travel-owned scheduler;
- preserve previous observations;
- detect material changes;
- downgrade stale or degraded options;
- suppress repeated low-value alerts;
- notify only through an approved attention policy;
- stop when the watch expires or is disabled.

## Material-change examples

```text
price crosses configured threshold
availability materially narrows
route becomes unreliable
entry rule changes
stronger verified alternative appears
document blocker clears or appears
window changes from OPEN to CLOSING
source becomes stale, fallback or simulated
```

A monitor result is a proposal, not a commitment or automatic purchase action.

## Input policy

Travel asks only for essential missing constraints. Known private facts are reused through the approved memory route rather than repeatedly requested.

Consequential assumptions are stated. Unknown facts remain unknown.

Passwords, API keys and secret values are never requested during normal operation. Secret onboarding occurs only through the approved Secret Store Gate workflow.

## Annual-map output

A map entry may include:

- best and cheapest windows;
- shoulder and avoid periods;
- duration and route format;
- route quality;
- realistic full cost;
- useful days;
- principal benefits and risks;
- document and duplication state;
- lead time, deadline and urgency;
- status, alternatives, confidence and next review;
- evidence labels and retrieval date.

## Shortlist output

A shortlist compares current verified candidates on:

- full cost and price authority;
- weather and season;
- safety and disruptions;
- authenticity and novelty policy;
- documents;
- useful time and route quality;
- stay value;
- crowd and event pressure;
- urgency and waiting cost;
- confidence and unresolved unknowns.

## Booking-ready trip pack

After explicit option selection, a trip pack may contain:

- exact dates and full route;
- segments and safe margins;
- ticket and reservation rules;
- alternatives and last safe fallback;
- day plan and map-ready stops;
- accommodation requirements;
- totals, baggage and fees;
- booking order;
- food, nature, free activities and local warnings;
- etiquette and Plan B.

The pack is an instruction and decision artifact. External purchase or contact remains separately gated.
