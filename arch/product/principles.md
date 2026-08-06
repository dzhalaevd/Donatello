# Product Principles

These principles turn our philosophy into decision-making rules. They apply to features, interfaces, Recommendations,
live communication, notifications, experiments, safety operations, and monetization.

The beliefs behind these rules are documented in [philosophy.md](./philosophy.md). Capitalized domain terms use the
definitions in [glossary.md](./glossary.md).

All principles apply to the same canonical sequence:

```text
Dating Intent and Boundaries
  -> Live Availability
  -> Recommendation
  -> Preview Interest
  -> Mutual Preview Interest
  -> Conversation Pairing
  -> Live Conversation
  -> Continue Decision
  -> Match
  -> Post-Match Communication
  -> optional Offline Meeting
```

## 1. Optimize for Meaningful Outcomes, Not Engagement

When engagement conflicts with the likelihood of an informed, voluntary, and safe outcome, choose the latter.

Views, Preview Interests, Conversation minutes, messages, Matches, and return visits are diagnostic metrics, not
evidence of User value by themselves. Informed non-continuation can be a Meaningful Outcome.

## 2. Keep Choice Small, Predictable, and Complete

Offer a small and predictable number of Recommendations in a session. A Recommendation Limit must create a clear
stopping point, not an infinite feed or automatic progression to the next Candidate.

Limits exist to test whether manageable choice reduces overload. They must not create artificial scarcity, variable
rewards, paid advantage, or anxiety about missing a Candidate. The appropriate number and period require validation.

## 3. Separate Preview Interest From Match

A positive Recommendation Decision creates Preview Interest: willingness to try a short Live Conversation, not a
Match, compatibility conclusion, or consent to later contact.

Reciprocal Preview Interest creates Mutual Preview Interest. A Match cannot exist before an eligible Live Conversation
and two independent positive Continue Decisions. The product must make each decision's meaning understandable without
requiring every internal domain state to appear as a separate User-facing step.

## 4. Explain Without False Certainty

Users should understand why a Candidate was recommended and which stated factors influenced the Recommendation.

Explanations must not expose sensitive information, turn Compatibility Assessments into judgments of personal worth,
present assumptions as facts, or promise a Conversation, Match, relationship, or Offline Meeting.

## 5. Make Live Communication Mutual and Voluntary

A Conversation Pairing may be created only after Mutual Preview Interest, compatible Live Availability, and both
Users' confirmation to enter. A User may revoke availability, decline the Pairing, leave the Live Conversation, or
change their mind at any time.

Silence, refusal, early exit, or a changed decision must never be bypassed through automation or pressure. Voice, video,
their combination, waiting behavior, and the duration threshold remain product hypotheses requiring validation.

## 6. Keep Continue Decisions Private and Independent

Reaching the minimum Live Conversation threshold only makes the Continue Decision available. It does not certify
Conversation quality and does not require either User to remain, decide positively, or explain a negative decision.

Each Continue Decision is private. A Match is created only when both Users independently choose to continue. If either
does not, communicate a neutral non-Match outcome without revealing who declined.

## 7. Design Calm, Complete Sessions

Every availability, Recommendation, pairing, and Live Conversation session needs an understandable beginning, current
state, and end.

Avoid infinite scrolling, automatic continuation to more Candidates, streaks, variable rewards, urgent countdowns,
anxiety-driven notifications, and repeated prompts designed to pull a User back into an unproductive loop.

## 8. Put Safety and Privacy in the First Release

The first end-to-end release must provide, before and during the Live Conversation and after a Match:

- an immediate way to leave or end contact;
- block and report controls;
- protection of sensitive profile, location, and contact data;
- private Preview Interest and Continue Decisions;
- no product-side recording of Live Conversations by default, plus a clear warning that external recording cannot be
  prevented;
- no public rejection, Conversation, attractiveness, or User-worth ratings;
- clear expectations about what reports trigger and what safety cannot be guaranteed.

No minimum duration, conversion goal, growth target, or technical simplification may disable or postpone these controls.

## 9. Support the Journey After a Match Without Prolonging It

A Match represents reciprocal willingness to continue after a Live Conversation. It may open minimal Post-Match
Communication and optional support for maintaining Boundaries or planning an Offline Meeting.

The product must not manufacture messages, make continued contact obligatory, or prolong communication for retention.
Either User remains free to pause, end, block, or report the connection.

## 10. Test Hypotheses With Outcome and Harm Measures

Before testing a mechanism, define the problem it is intended to affect, the expected Meaningful Outcome, guardrail
metrics, affected groups, stopping criteria, and what evidence would disconfirm the hypothesis.

An A/B test does not make a manipulative or unsafe pattern acceptable. Synchronous communication, Recommendation
Limits, threshold duration, Match timing, and Post-Match Support must remain hypotheses until evidence supports them.

## 11. Never Turn Money Into an Advantage Over People

Payment must never increase visibility in hidden rankings, buy another person's attention, reveal Preview Interest or a
Continue Decision, bypass Live Availability, or accelerate a User ahead of others in a pairing queue.

Paid features should provide clear standalone value without making the free experience less safe, less transparent, or
less capable of reaching a Meaningful Outcome.

## Decision Priority

When principles conflict, decisions should follow this order:

1. Safety and User consent.
2. User well-being.
3. Meaningful Outcomes.
4. Trust, transparency, and data control.
5. Simplicity and accessibility.
6. Product sustainability.
7. Engagement and growth.

## Product Decision Checklist

Before implementing or testing a feature, ask:

1. Which problem and Meaningful Outcome does it address, and for whom?
2. Is it clear whether the User is expressing Preview Interest or making a Continue Decision?
3. Could it increase anxiety, coercion, compulsive behavior, choice overload, or unequal waiting?
4. Can the User decline, leave, block, report, and control sensitive data at every relevant state?
5. Is it clear why the system behaves this way and what it does not know?
6. What guardrail metrics, stopping criteria, and disconfirming evidence are required?
7. Could the same outcome require less attention, less waiting, or less User data?

If these questions cannot be answered with evidence or an explicit validation plan, the feature is not ready for
implementation or experimentation.
