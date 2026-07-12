# Travel Offer Intelligence

Travel Offer Intelligence discovers, parses, normalizes, verifies, deduplicates, scores and monitors travel offers that generic search cannot reliably structure.

Primary source architecture:

- `alanua/Skeleton#1747` — complete Offer Intelligence design;
- `alanua/Skeleton#1749` — bounded contracts and fixture-adapter slice.

## Pipeline

```text
travel offer sources
→ source-specific acquisition adapter
→ structured extraction
→ normalized travel-offer record
→ source-level dedupe and cross-source clustering
→ freshness and lifecycle checks
→ direct merchant verification where permitted
→ full-cost and logistics evaluation
→ annual-map or shortlist proposal
→ operator review
```

Offers remain options. The module must not book, reserve, contact, pay, submit passenger data or mutate planned/booked state automatically.

## Source classes

- deal publisher;
- retail travel brand;
- tour operator;
- OTA or metasearch;
- travel agency or quote source;
- direct airline, rail, ferry, hotel or package merchant;
- lawful newsletter or email intake;
- manual URL import.

The record separates discovery source, storefront or agency, booking provider and legal organizer.

## Access lanes

```text
OFFICIAL_FEED
OFFICIAL_API
STATIC_HTML
STRUCTURED_DATA_JSON_LD
DYNAMIC_BROWSER
NEWSLETTER_EMAIL
MANUAL_URL_IMPORT
BLOCKED_UNSUPPORTED
```

Rules:

- prefer feeds and official APIs;
- use static HTML or structured data before a browser;
- use isolated browser acquisition only when public content genuinely requires rendering;
- never bypass CAPTCHA, authentication, paywalls, robots restrictions, rate limits or technical access controls;
- never imitate a logged-in user without a separately approved private credential route;
- mark unsupported sources explicitly and retain a permitted fallback.

## Required normalized semantics

A travel-offer record distinguishes:

- article, bookable offer and agency quote;
- flight, package, stay, tour, cruise, rail and mixed offer;
- exact price and `from` price;
- per-person, per-night and total price basis;
- headline price and verified realistic total;
- exact dates and flexible windows;
- included and excluded baggage, meals, transfers, room, rental car and fees;
- cancellation, deposit and payment timing;
- source evidence, merchant evidence and verification timestamp;
- parser version and content hash;
- `UNVERIFIED`, `LISTED`, `LIVE_CONFIRMED`, `STALE`, `EXPIRED` and `REJECTED` states.

Unknown values remain unknown.

## Deduplication

The same underlying offer may appear repeatedly or across several publishers. Deduplication must:

- detect source duplicates by item ID, canonical URL and content hash;
- cluster cross-source variants conservatively by route, dates, duration, merchant and price band;
- keep all source evidence;
- preserve materially different baggage, stay, board, fee or cancellation variants;
- never erase history only because a current page disappeared.

## Verification

Deal publishers are discovery sources, not final price authorities. Before a result can become `LIVE_CONFIRMED` or support `ACTION_RECOMMENDED`, verification must recheck the direct operator or merchant path where permitted.

Verification records:

- exact dates and current availability;
- price basis and currency;
- realistic total for the configured party;
- baggage, origin access, transfers, taxes and mandatory extras;
- accommodation and board conditions;
- timestamp, evidence and confidence;
- material changes from the discovered listing.

The verifier must never submit booking, passenger, payment or contact forms.

## Adapter health

Every source adapter declares access lane, licence, rate policy, listing/detail support, live-verification support, browser need, credential class, parser version and health.

Health states:

```text
HEALTHY
DEGRADED
BLOCKED
SCHEMA_CHANGED
DISABLED
```

A layout or schema break must fail explicitly. Silent empty output is not success.

## Safe first slice

The first implementation slice is public-safe and replayable:

- shared schemas and models;
- source registry;
- static saved fixtures;
- fixture translators for a small number of sources;
- normalizer, lifecycle and dedupe;
- golden tests;
- no live network, browser, email, scheduler, credentials or private profile.
