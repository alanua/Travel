# Contributing

Travel welcomes focused changes to public-safe contracts, adapters, deterministic planning logic, documentation, schemas, synthetic fixtures, and tests.

## Public-safe contributions

Use synthetic or clearly public data only. Do not include personal itineraries, private budgets, real booking references, private calendars, credentials, cookies, tokens, identity documents, or live/home locations.

## Provider adapters

Prefer official APIs and official transport feeds when available. Make freshness, fallback, estimated, unsupported, and simulated states explicit. A provider adapter must not silently gain booking, payment, contact, cancellation, or subscription authority.

## Pull requests

Keep scope narrow, document provider/data assumptions, add deterministic tests, and state whether a change affects research, monitoring, route composition, or an external action boundary. Avoid unrelated trip-page design and provider changes in the same PR.

## Skeleton boundary

Skeleton provides shared control, approval, private-memory/secret routing, and audited execution. Travel owns travel-domain semantics. Do not duplicate private authority or secret-store behavior inside the public Travel repository.

## License status

No open-source license has been selected for this repository yet. Do not add or change a repository license without an explicit maintainer decision.
