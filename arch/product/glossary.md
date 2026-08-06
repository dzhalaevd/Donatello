# Ubiquitous Language

This document defines the canonical domain language of **Make Dating Free Again**. It contains meanings and
distinctions, not product policy, validation claims, or technical design. Product rules belong in
[principles.md](./principles.md), and evidence belongs in [research.md](./research.md).

## Core Participants

| Term                  | Definition                                                                                                                                                          | Avoid                                                                     |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| **User**              | A person who enters or uses the product to explore a mutual connection, including before they have stated a Dating Intent or completed participation setup.         | customer, lead, traffic, dater                                            |
| **Dating Profile**    | The representation of a User shown to another User before a Live Conversation. It is distinct from the User, account, authentication identity, and database record. | card, account, profile when referring to an account                       |
| **Dating Intent**     | A User's explicitly stated goal and acceptable form of connection.                                                                                                  | conversion goal, user type, inferred intent                               |
| **Boundaries**        | A User's explicitly stated limits on participation, disclosure, contact, and acceptable forms of connection.                                                        | inferred limits, hidden eligibility score                                 |
| **Live Availability** | A User's revocable declaration that they are currently willing and able to enter a short Live Conversation.                                                         | online status, permanent availability, consent to a specific Conversation |

## Recommendation and Preview Domain

| Term                           | Definition                                                                                                                                                                                                                              | Avoid                                               |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| **Candidate**                  | A User eligible to be considered for another User but not yet presented to them.                                                                                                                                                        | lead, item, product, option                         |
| **Recommendation**             | A time-bounded proposal for a User to consider a specific Candidate for a possible short Live Conversation, accompanied by an understandable reason for the selection.                                                                  | impression, feed item, result, card                 |
| **Recommendation Explanation** | A user-understandable description of the factors that caused a Candidate to be recommended.                                                                                                                                             | score, ranking, algorithm verdict                   |
| **Compatibility Assessment**   | A probabilistic assessment of how well two Users may satisfy each other's Dating Intents, preferences, and Boundaries.                                                                                                                  | person quality, attractiveness score, profile value |
| **Recommendation Decision**    | A User's explicit response to a Recommendation: express Preview Interest or decline it.                                                                                                                                                 | swipe, vote, Match Decision                         |
| **Preview Interest**           | A private, unilateral Recommendation Decision that a User is currently willing to try a short Live Conversation with the Candidate. It is not a Match, compatibility confirmation, consent to later contact, or irrevocable commitment. | Interest, like, Match, consent                      |
| **Mutual Preview Interest**    | The state in which two Users independently hold reciprocal Preview Interest. It indicates only mutual willingness to consider entering a short Live Conversation and does not itself open communication.                                | Mutual Interest, Match, compatibility               |

## Live Conversation Domain

| Term                           | Definition                                                                                                                                                                                                                                                  | Avoid                                                                            |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| **Conversation Pairing**       | A temporary product state connecting two Users for one initial Live Conversation after both have confirmed willingness and current availability.                                                                                                            | Match, relationship, permanent chat                                              |
| **Live Conversation**          | Synchronous voice or video communication between Users within a Conversation Pairing.                                                                                                                                                                       | text chat, Match, any message exchange                                           |
| **Eligible Live Conversation** | A Live Conversation that has reached the minimum policy threshold required to make a Continue Decision available. The term describes decision eligibility only; it does not mean the Conversation was meaningful, safe, or successful.                      | successful Conversation, quality Conversation, completed relationship assessment |
| **Continue Decision**          | A private decision made independently by each User after an Eligible Live Conversation: continue the connection or do not continue it.                                                                                                                      | Match Decision, rating, public rejection                                         |
| **Match**                      | The state created only when both Users independently make a positive Continue Decision after an Eligible Live Conversation. A Match may open Post-Match Communication but is not a relationship, compatibility verdict, or guarantee of an Offline Meeting. | Mutual Preview Interest, Conversation Pairing, couple, success                   |

## Connection Outcomes

| Term                         | Definition                                                                                                                                                                                                                                          | Avoid                                                                    |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| **Post-Match Communication** | A persistent communication channel made available after a Match so Users can continue the connection or plan an Offline Meeting.                                                                                                                    | pre-conversation chat, engagement channel, mandatory contact             |
| **Conversation**             | An umbrella term for communication between Users. Use Live Conversation or Post-Match Communication when the state of the journey matters.                                                                                                          | engagement, activity                                                     |
| **Meaningful Conversation**  | A Conversation that one or both participating Users report as providing enough information for their own informed decision about continuing or ending the connection. Duration or Continue Decision eligibility does not establish meaningfulness.  | Eligible Live Conversation, any message exchange, chat length, retention |
| **Offline Meeting**          | A voluntary meeting between Users outside the product, reported by the Users or measured with their consent.                                                                                                                                        | conversion without specifying the outcome                                |
| **Meaningful Outcome**       | An outcome the participating Users consider useful, including a Meaningful Conversation, informed non-continuation, a Match, an Offline Meeting, or another informed next step. The product must not assume that continuation is always preferable. | retention, time in app, message volume, Match count, engagement          |

## Product Quality

| Term                     | Definition                                                                                                                                                                                       | Avoid                                                                           |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| **Dating App Fatigue**   | Emotional or cognitive exhaustion associated with repetitive evaluation, rejection, uncertainty, excessive choice, or compulsive dating-product usage.                                           | low engagement, churn                                                           |
| **Intentional Usage**    | Product usage directed toward a clear purpose, with understandable session boundaries and without automatic continuation.                                                                        | activity, engagement                                                            |
| **Recommendation Limit** | A clearly communicated limit on the number of Recommendations available during a defined period.                                                                                                 | paywall, energy, scarcity boost                                                 |
| **Post-Match Support**   | Optional assistance after a Match that helps Users continue communication, maintain Boundaries, or move toward an Offline Meeting without automating consent or artificially prolonging contact. | pre-match conversation automation, post-match retention, conversation autopilot |

## Canonical Relationships

```text
User -> Dating Profile
User -> Dating Intent
User -> Live Availability

Candidate -> Recommendation
positive Recommendation Decision -> Preview Interest
reciprocal Preview Interest -> Mutual Preview Interest
Mutual Preview Interest + confirmed availability -> Conversation Pairing
Conversation Pairing -> Live Conversation
Eligible Live Conversation -> Continue Decision becomes available
reciprocal positive Continue Decision -> Match
Match -> Post-Match Communication
Match -> optional Offline Meeting

Meaningful Conversation,
informed non-continuation,
Match,
or Offline Meeting
-> possible Meaningful Outcome
```

These states are not interchangeable. In particular:

- Preview Interest and Mutual Preview Interest are not a Match;
- Conversation Pairing exists only to enable the initial Live Conversation;
- a User may revoke Live Availability, decline a Pairing, leave, block, or report at any time;
- reaching the minimum threshold makes the Continue Decision available but never requires continuation;
- a Match exists only after reciprocal positive Continue Decisions;
- Post-Match Communication begins only after a Match.
