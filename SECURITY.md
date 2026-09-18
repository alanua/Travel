# Security Policy

Travel coordinates public travel data, private planning context, external providers, and potentially high-impact booking actions. The public repository therefore keeps research and deterministic planning separate from authority to reserve, pay, contact, cancel, or expose private itinerary data.

## Reporting

Do not publish credentials, booking references, personal documents, private itineraries, live/home locations, payment data, cookies, access tokens, or a working exploit in a public issue. Prefer GitHub private vulnerability reporting when available; otherwise request a private contact channel through the maintainer profile.

## High-sensitivity areas

- booking/payment/contact/cancellation authority;
- provider credential or session leakage;
- private itinerary, location, family, passport/residence, ticket, or calendar data;
- prompt/source injection from provider pages or imported content;
- malicious redirects, deep links, or unsafe external actions;
- stale availability, fares, schedules, entry rules, or disruption data presented as current;
- unsafe automation that turns research into a commitment;
- publication of private trip artifacts or decryption material.

## Authority boundary

Research, monitoring, comparison, and shortlist generation create options only. A booking or other external mutation requires a separately approved path with explicit operator authorization. Public CI must never exercise live booking or paid-provider actions.

## Private data

Personal preferences, budgets, trip history, private candidate rankings, raw tracks, live locations, bookings, tickets, calendars, identity documents, and private price observations do not belong in this repository.
