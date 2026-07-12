# Data, Evidence, Warehouse and Scoring

Travel decisions must preserve the distinction between observed facts, cached listings, estimates, historical patterns and model priors.

## Evidence classes

```text
CONFIRMED_LIVE_PRICE
CURRENT_LISTED_PRICE
INDICATIVE_PRICE
HISTORICAL_PATTERN
MODEL_PRIOR
ESTIMATE
UNKNOWN
```

Every observation records retrieval time, source, conditions, freshness, confidence and whether the value is cached, stale, fallback, simulated or estimated.

No advertisement, cached card, stale result, simulated response or model prior may be presented as a confirmed current price.

## Source registry

Each public source descriptor records:

- provider and source identity;
- coverage and supported objects;
- official or third-party status;
- licence and access conditions;
- authentication class;
- refresh and freshness expectations;
- rate limits;
- data quality and source tier;
- stale, fallback and simulation behavior;
- validation date and known failures;
- safe use and `DO_NOT_USE` conditions.

Source tiers:

```text
A = official or primary authoritative source
B = reliable specialist or licensed provider
C = aggregator or discovery platform
D = crowdsourced or OSINT lead
E = demo, synthetic or simulation
```

D and E evidence cannot independently produce an action recommendation.

## Private Travel Price Warehouse

The public repository may define schemas and algorithms. Actual personal observations remain private.

Private warehouse object families may include:

- fares and availability;
- stays and final accommodation totals;
- packages and organizer terms;
- ground transport;
- car rental;
- activities and events;
- destination-cost observations;
- complete trip totals.

Each observation is timestamped and immutable. Corrections create new observations rather than silently rewriting history.

## Baselines and anomaly detection

Travel-specific analysis may use:

- 30-day, 90-day and 365-day baselines;
- robust median and median absolute deviation;
- percentiles;
- route-to-airport, route-to-city and route-to-region fallbacks;
- season and lead-time segmentation;
- demand, event and holiday context;
- current-source health and sample size.

A model prior is never reported as observed route history. Insufficient history remains `UNKNOWN` or uses an explicitly labeled fallback.

## Full-cost policy

Full realistic cost may include:

- origin and return access;
- long-distance transport;
- baggage and reservations;
- transfers and local transport;
- stays, taxes and mandatory fees;
- car, road, parking, toll and fuel costs;
- meals where relevant;
- visas, transit permissions and insurance;
- realistic compulsory extras;
- contingency caused by split-ticket or missed-connection risk.

Outputs include total, per-person total, cost per trip day and cost per useful day.

A headline bargain is rejected when additions materially remove the value.

## Scoring and explanation

The scorer returns decomposed components rather than one unexplained number. Components may include:

- full-cost value;
- price anomaly;
- season and weather fit;
- route quality and useful-time yield;
- stay value;
- safety and disruption exposure;
- document simplicity or blocker;
- crowd and event pressure;
- novelty or repetition policy supplied by private configuration;
- urgency and waiting cost;
- source confidence.

Private preferences, home base, party composition, leave windows, document state and personal weights are runtime inputs behind MemoryGateway. They are absent from public fixtures.

## Decision safeguards

- a document blocker caps or blocks action status;
- an official do-not-travel condition blocks recommendation;
- an unverified price cannot become a confirmed hot deal;
- simulated data is ignored for operational decisions;
- stale or degraded sources lower confidence;
- route risk, useful time and total cost can override a low headline price;
- final recommendation includes reasons, uncertainty and next review.
