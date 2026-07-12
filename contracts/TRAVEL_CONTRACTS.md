# Travel Contract Catalogue

The Travel domain uses provider-neutral records. Provider payloads remain adapter-internal.

## Trip and opportunity

```text
TripReference
TravellerReference
TravelConstraintReference
OpportunityWindow
TravelOption
TravelStatusTransition
ShortlistEntry
ReviewProposal
TripPackManifest
BookingRecordReference
```

## Itinerary and logistics

```text
Itinerary
ItineraryVariant
TravelSegment
ConnectionMargin
TicketRelationship
RouteQuality
UsefulTimeSummary
FallbackPlan
TransportCoveragePlan
AdapterRequirement
```

## Transport

```text
TransportStop
TransportRoute
TransportLeg
TransportJourney
FareObservation
TicketRule
ReservationRule
LiveDeparture
LiveArrival
LiveVehiclePosition
TransportDisruption
ConnectionRisk
AlternativeJourney
AccessibilityStatus
```

## Offer Intelligence

```text
TravelOfferRecord
TravelOfferSource
TravelMerchant
TravelOrganizer
OfferVariant
OfferVerification
OfferCluster
SourceHealth
ParserFailure
```

## Stay, package and activity

```text
StayObservation
RoomCondition
StayPriceBreakdown
CancellationCondition
PaymentTiming
PackageObservation
PackageInclusion
PackageOrganizerCondition
ActivityObservation
OpeningCondition
EventWindow
```

## Cost, evidence and scoring

```text
MoneyAmount
CostComponent
FullTripCost
UsefulDayCost
EvidenceReference
FreshnessState
ConfidenceState
PriceEvidenceClass
TravelScoreComponent
TravelScoreExplanation
PriceBaseline
PriceAnomaly
```

## Documents and risk

```text
DocumentRequirementReference
TransitRequirementReference
CarrierAcceptanceReference
ReentryRequirementReference
DocumentGateResult
SituationalSignalReference
TravelRiskProjection
TravelImpactState
```

## Required metadata

Every observed or derived object contains, where applicable:

```text
source_id
source_reference
retrieved_at
observed_at
valid_for
freshness_state
evidence_class
confidence
adapter_id
adapter_version
input_hash
result_hash
```

## Authority metadata

Every operation and result declares:

```text
side_effect_class = READ_ONLY | PROPOSAL | APPROVED_MUTATION
authority = NONE | OPERATOR_REQUIRED | REGISTERED_POLICY
privacy_class = PUBLIC_SAFE | PRIVATE_CONTEXT | PRIVATE_ARTIFACT | SECRET_REFERENCE
```

Current repository contracts do not authorize `APPROVED_MUTATION` implementations.

## Failure contract

Failures are typed and explicit:

```text
SOURCE_UNAVAILABLE
AUTH_REQUIRED
RATE_LIMITED
SCHEMA_CHANGED
STALE_ONLY
SIMULATED_ONLY
UNSUPPORTED_CAPABILITY
INVALID_INPUT
PRIVACY_DENIED
AUTHORITY_DENIED
EVIDENCE_INSUFFICIENT
DOCUMENT_BLOCKED
NO_SAFE_CONNECTION
```

Missing or unsupported values remain unknown and are not inferred.
