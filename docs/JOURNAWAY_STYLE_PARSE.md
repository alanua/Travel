# Journaway visual reference parse

Reference page: `https://www.journaway.com/de/angebote/2-for-1-mexiko-deal-roadtrip-65533`

This document records the reusable visual and interaction patterns derived from the public page. It does not copy Journaway source code, branding, photography, copy, icons, or booking flows.

## Page rhythm

1. Narrow promotional strip.
2. Minimal white header.
3. Large asymmetrical editorial image mosaic.
4. Deal badge, oversized title, compact fact row.
5. Horizontal trip-variant selector.
6. Editorial route introduction and experience cards.
7. Linear route with connected stops.
8. Expandable day-by-day itinerary.
9. Included stays, upgrade stays, optional activities.
10. Inclusions/exclusions and practical details.
11. Sticky price/action panel on desktop and sticky bottom action on mobile.

## Visual tokens

- dominant surfaces: white and very light neutral gray;
- text: near-black with medium neutral gray secondary copy;
- action accent: vivid cyan/blue;
- promotional accent: warm yellow;
- thin neutral borders instead of heavy shadows;
- compact radii, generally 9–18 px;
- large dense headings with tight negative tracking;
- generous vertical section spacing and minimal boxed-card chrome;
- image-first cards with bottom gradient only when text overlays photography.

## Layout rules

- maximum content width around 1200–1250 px;
- primary content column around 800–840 px;
- sticky desktop summary around 340–370 px;
- hero mosaic uses one dominant image and two secondary images;
- mobile hero becomes one wide image plus two equal thumbnails;
- date and route rows scroll horizontally on narrow screens;
- itinerary collapses to compact rows; day images may hide on small screens;
- desktop sticky panel is replaced by a bottom price/action bar on mobile.

## Component rules

- variants: bordered rectangular pills, selected with a 2 px dark border;
- facts: one horizontal row separated by thin vertical rules;
- route: connected circles and line, not an embedded map;
- stays/activities: photo, status label, title, short explanation, optional action;
- buttons: compact rectangle, cyan primary, black map action, white secondary;
- status language must remain Travel-specific: candidate/planned/in-trip, never fake booking urgency.

## Travel deviations

- display full total for two before per-person price;
- no checkout, booking, sales chat, countdown or false scarcity;
- show workdays, evidence type, last-check date, documents and risks;
- use Google Maps route actions instead of an embedded map;
- private trip data is supplied only at runtime.
