# Ubiquitous Language

This document defines the canonical domain language of **Make Dating Free Again**. It contains meanings and distinctions,
not product policy or technical design. Product rules belong in [principles.md](./principles.md).

## Core Participants

**User**:
A person who uses the product to pursue a mutual connection according to their stated Dating Intent.
_Avoid_: customer, lead, traffic, dater

**Dating Profile**:
The representation of a User shown to other Users when they make a dating decision. It is distinct from the User,
account, authentication identity, and database record.
_Avoid_: card, account, profile when referring to an account

**Dating Intent**:
A User's explicitly stated goal and acceptable form of connection.
_Avoid_: conversion goal, user type, inferred intent

## Recommendation Domain

**Candidate**:
A User eligible to be considered for another User but not yet presented to them.
_Avoid_: lead, item, product, option

**Recommendation**:
A time-bounded proposal for a User to consider a specific Candidate, accompanied by an understandable reason for the
selection.
_Avoid_: impression, feed item, result, card

**Recommendation Explanation**:
A user-understandable description of the factors that caused a Candidate to be recommended.
_Avoid_: score, ranking, algorithm verdict

**Compatibility Assessment**:
A probabilistic assessment of how well two Users may satisfy each other's Dating Intents, preferences, and constraints.
_Avoid_: person quality, attractiveness score, profile value

**Recommendation Decision**:
A User's explicit response to a Recommendation: express Interest or decline it.
_Avoid_: swipe, vote, discard

**Interest**:
A positive Recommendation Decision made by one User regarding another User. It is unilateral.
_Avoid_: match, consent

**Mutual Interest**:
The state in which two Users have independently expressed Interest in each other.
_Avoid_: Match when referring only to reciprocal decisions

**Match**:
A product-enabled opportunity for two Users to communicate after Mutual Interest has been established.
_Avoid_: couple, relationship, success

## Connection Outcomes

**Conversation**:
Communication between Users after a Match through an available channel.
_Avoid_: engagement, activity

**Meaningful Conversation**:
A Conversation in which both Users obtain enough information to make an informed decision about continuing or ending
the connection.
_Avoid_: any message exchange, chat length, retention

**Offline Meeting**:
A voluntary meeting between Users outside the product, reported by the Users or measured with their consent.
_Avoid_: conversion without specifying the outcome

**Meaningful Outcome**:
An outcome the participating Users consider useful, including a Meaningful Conversation, a safe Offline Meeting, or an
informed decision not to continue.
_Avoid_: retention, time in app, message volume, engagement

## Product Quality

**Dating App Fatigue**:
Emotional or cognitive exhaustion associated with repetitive evaluation, rejection, uncertainty, excessive choice, or
compulsive dating-product usage.
_Avoid_: low engagement, churn

**Intentional Usage**:
Product usage directed toward a clear purpose, with understandable session boundaries and without automatic
continuation.
_Avoid_: activity, engagement

**Recommendation Limit**:
A clearly communicated limit on the number of Recommendations available during a defined period.
_Avoid_: paywall, energy, scarcity boost

**Post-Match Support**:
Optional assistance after a Match that helps Users begin a Meaningful Conversation or progress toward an Offline
Meeting.
_Avoid_: post-match retention, conversation autopilot

## Canonical Relationships

```text
User -> Dating Profile
User -> Dating Intent
Candidate -> Recommendation -> Recommendation Decision
positive Recommendation Decision -> Interest
reciprocal Interest -> Mutual Interest -> Match
Match -> Conversation -> Meaningful Conversation
Meaningful Conversation -> optional Offline Meeting
Conversation or Offline Meeting -> possible Meaningful Outcome
```

These states are not interchangeable. In particular, Mutual Interest is not yet a Match, a Match is not yet a
Conversation, and a Conversation is not necessarily meaningful.
