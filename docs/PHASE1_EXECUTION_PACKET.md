# Travel Phase 1 Execution Packet

Status: `READY_FOR_IMPLEMENTATION / PUBLIC_SAFE / NO_LIVE_PROVIDERS`

This packet defines the first deterministic implementation slice for the Travel domain. It does not authorize live acquisition, private-profile access, booking, payment, contact, cancellation, subscription changes or canon mutation.

## Goal

Create a small provider-neutral core that can represent and validate travel opportunities without network access or private data.

The slice must prove that Travel can accept several synthetic source records, normalize them into one stable domain model, preserve evidence and uncertainty, and produce a deterministic shortlist proposal without creating any external commitment.

## Exact implementation scope

The implementation slice should add only the following public-safe files:

```text
src/travel/__init__.py
src/travel/contracts.py
src/travel/normalization.py
src/travel/scoring.py
schemas/travel_opportunity.schema.json
schemas/travel_source_record.schema.json
examples/synthetic/opportunities.json
tests/test_travel_contracts.py
tests/test_travel_normalization.py
tests/test_travel_scoring.py
```

A later implementation may adjust package-layout details, but it must preserve the same bounded responsibilities and must not introduce provider clients or runtime integration.

## Domain records

### SourceRecord

A source record represents one observation from one source. It must include:

- opaque public-safe source identifier;
- source class and evidence tier;
- retrieval timestamp;
- observed price and currency when known;
- price semantics: exact, from, per-person, total, estimated or unknown;
- origin and destination references when known;
- travel window or event window;
- included and excluded components;
- freshness and confidence;
- explicit stale, fallback, simulated and unknown markers;
- public-safe provenance reference.

### TravelOpportunity

A normalized opportunity must include:

- stable deterministic opportunity id;
- opportunity type;
- origin and destination references;
- earliest and latest usable dates;
- duration bounds;
- normalized total-cost components without currency conversion side effects;
- transport, stay, package, event and route-quality summaries;
- evidence references;
- confidence and freshness;
- lifecycle status;
- assumptions and blockers;
- proposal-only decision state.

No private traveller identity, budget, home location, document status, booking reference or preference value may appear in these public records.

## Lifecycle

The first slice supports only proposal states:

```text
OBSERVED
→ NORMALIZED
→ ELIGIBLE_FOR_COMPARISON
→ SHORTLIST_PROPOSED
→ DEFERRED | EXPIRED | REJECTED
```

`SELECTED`, `BOOKING_READY`, `BOOKED`, `PAID` and similar commitment states are outside this slice.

## Normalization rules

Normalization must be deterministic and fail closed on malformed inputs.

Required behavior:

1. preserve the original source value and its semantics;
2. never convert `from` into `exact`;
3. never convert per-person into total without an explicit public synthetic party-size input;
4. never assume baggage, transfers, taxes, resort fees, reservations or local transport are included;
5. preserve unknown and missing values;
6. keep currencies unchanged in core normalization;
7. reject impossible date windows and negative amounts;
8. preserve each evidence reference instead of collapsing provenance;
9. deduplicate only when deterministic identity fields match;
10. retain conflicting observations as separate evidence entries.

## Scoring contract

The scoring module must return a decomposed proposal score, not a booking decision.

Required components:

- timing fit;
- route quality;
- evidence quality;
- freshness;
- cost completeness;
- uncertainty penalty;
- risk and blocker penalty;
- explanation tokens.

The first slice uses only explicit synthetic weights supplied by tests. It must not read user preferences or private MemoryGateway state.

## Synthetic fixtures

The fixture set must include at least:

1. exact total package price;
2. `from` price with missing baggage;
3. per-person fare requiring explicit party-size handling;
4. stale observation;
5. conflicting observations from two sources;
6. incomplete date window;
7. simulated fallback record;
8. duplicate record with identical deterministic identity;
9. same route but materially different offer;
10. malformed negative-price record that must fail.

Fixture names and content must be fictional and public-safe.

## Tests

Tests must run with network disabled and verify:

- JSON Schema Draft 2020-12 validity;
- deterministic ids across repeated runs;
- exact/from and per-person/total separation;
- preservation of source evidence and uncertainty;
- conflict retention;
- conservative deduplication;
- stale and simulated states remain visible;
- malformed dates and prices fail closed;
- scoring decomposition is stable and explained;
- no private-field vocabulary appears in public schemas or fixtures;
- no booking, payment, contact or mutation function exists in the slice.

## Forbidden actions

- no HTTP clients, browsers, scraping or live provider calls;
- no credentials, cookies, tokens or secret references;
- no private MemoryGateway reads or writes;
- no calendar, notification or monitoring activation;
- no booking, reservation, payment, contact or cancellation actions;
- no automatic currency conversion;
- no personal route candidates, budgets, preferences, documents or history;
- no provider-specific fields in the core domain model.

## Validation commands

```bash
python -m unittest discover -s tests -v
python -m compileall -q src tests
git diff --check
```

If the repository later standardizes on pytest, the same tests may be executed through pytest without changing their deterministic contract.

## Exit gate

Phase 1 is complete only when:

- every exact file is reviewed;
- all deterministic tests pass with network disabled;
- schemas and fixtures contain no private values;
- normalization preserves uncertainty and provenance;
- no side-effect or booking authority exists;
- the resulting PR is explicitly reviewed before merge.

## Next slice after completion

After Phase 1 passes, Phase 2 may implement fixture-only Offer Intelligence translators against saved public-safe inputs. Live adapters remain blocked until the transport/provider source, licence, authentication, rate-limit and failure contracts are separately reviewed.
