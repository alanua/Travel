# Access, Airport and Surface-Transport Policy

Travel evaluates every journey door to door rather than comparing headline transport prices in isolation.

## Door-to-door scope

A route includes:

- origin departure and final return;
- local or regional access to the main station, airport, coach terminal or ferry port;
- waiting and check-in time;
- long-distance segments;
- transfers and safe margins;
- destination access;
- required overnight stays caused by early departure or late arrival;
- missed-connection and fallback exposure.

## Airport policy

A configured primary airport is the default, not an absolute restriction. Alternative airports are considered only when the complete result is materially better.

Comparison includes:

- transport price for the configured party;
- origin access and destination access;
- baggage and reservation charges;
- hotel, parking or positioning costs;
- useful-time gain or loss;
- separate-ticket and missed-connection risk;
- reliability and route quality.

A cheaper fare is rejected when access, baggage, hotel, time or risk removes the saving.

## Surface transport

Travel compares:

- regional and long-distance rail;
- high-speed rail;
- night trains;
- coaches;
- ferries;
- split tickets and through tickets;
- passes and reservations;
- mixed-mode outbound and return journeys.

For every rail or surface option, it verifies where possible:

- timetable and current service state;
- reservation requirement;
- ticket validity and train binding;
- connection protection;
- strikes, closures and replacement transport;
- baggage rules;
- last safe fallback.

## Local-pass and long-distance cooperation

A local or regional pass may act as:

- origin feeder;
- border feeder;
- destination local transport;
- outbound or return segment of an asymmetric journey.

The planner may combine it with a separately purchased high-speed, long-distance, coach, ferry or foreign ticket. Every such combination records the contract boundary and whether a missed connection is protected.

## Useful-time policy

Route quality includes:

- useful hours at the destination;
- useful days;
- number and complexity of transfers;
- overnight travel benefit or fatigue;
- arrival and departure timing;
- recovery margin before the next fixed obligation.

A free slow journey may be inferior to a low-cost long-distance ticket when the latter materially improves useful time and reliability.

## Route ranking

Candidate route variants are compared on:

```text
full_cost
useful_time
transfer_count
connection_protection
reliability
fallback_quality
baggage_and_reservation_rules
comfort_friction
schedule_fit
```

The selected route is the lowest realistic total that does not impose unacceptable inconvenience, rushed pace or risk.
