# Threat model

## Assets

- private trip context and location history;
- booking/ticket/payment and identity data;
- provider credentials and sessions;
- route, fare, availability, schedule, climate, event, and disruption evidence;
- explicit operator authority for commitments;
- public/private publication boundary.

## Trust boundaries and threats

### Public source vs private planning context

Public code and fixtures must not become a side channel for personal preferences, budgets, candidate rankings, bookings, tracks, calendars, or identity documents. Private context remains behind Skeleton's private memory/artifact boundaries.

### Provider and web-source injection

External pages, feeds, reviews, and imported text are untrusted data. Instructions found in source content cannot authorize tools, reveal secrets, override route policy, or change booking authority.

### Stale or conflicting evidence

Travel facts such as fares, availability, schedules, entry rules, disruptions, and opening times change. Outputs should preserve source time/freshness and must not present stale or estimated evidence as confirmed current state.

### Booking and payment escalation

A shortlist or booking-ready trip pack is not permission to reserve or pay. Mutations require a separately registered operation and explicit approval. Fallback providers must not inherit stronger authority than the requested capability.

### Redirect and deep-link abuse

External URLs may redirect to malicious or misleading destinations. Adapters and UI surfaces should validate schemes/hosts where practical and avoid turning arbitrary imported URLs into trusted actions.

### Secret leakage

API keys, cookies, tokens, payment credentials, booking references, and private decryption material must stay outside source, fixtures, public CI logs, and AI prompts.

### False-positive success

HTTP success, a rendered itinerary, or a provider response is not proof that a booking, reservation, transport connection, or private publication is valid. Verification must match the action actually taken.

## Fail-closed policy

When evidence freshness, identity, price, availability, authority, or private/public classification is ambiguous, Travel should keep the item as unverified/review-needed instead of silently escalating it to confirmed or actionable.
