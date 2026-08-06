# User Story Map

This story map translates the product hypothesis into a user-centered journey. It is a strategic planning artifact,
not an implementation backlog or a claim that the proposed behavior has been validated.

The map should be reviewed collaboratively by product, design, engineering, safety, operations, and representative
Users before a release slice becomes committed scope. Product meaning and decision rules remain owned by
[vision.md](./vision.md), [principles.md](./principles.md), and [glossary.md](./glossary.md). Evidence and its limits
are
owned by [research.md](./research.md).

[FigmaJam](https://www.figma.com/board/2icO7WBdUhP1Fci5jc7pIQ/Make-Dating-Great-Again?node-id=0-1&t=Sb6y6rmdH7E9IVFz-1)

## Context

### Segment

Adults who seek a mutual connection, are willing to state their Dating Intent and Boundaries, experience choice
overload or repeated low-quality interactions in existing dating products, and are willing to test a short synchronous
conversation before persistent communication.

The initial market, supported Dating Intents, communication modes, orientations, relationship structures, and
accessibility needs are open research decisions.

### Proto-persona

**Alex** represents an adult in the target segment, not a validated demographic persona. Alex:

- wants a connection consistent with an explicitly stated Dating Intent and Boundaries;
- is tired of evaluating many Dating Profiles and repeating unfinished text exchanges;
- wants enough context to decide whether a short live conversation is worth trying;
- needs control over visibility, availability, personal information, participation, and session length;
- wants to leave, block, or report at any time without being penalized;
- wants a Match to mean that both people chose to continue after actually speaking.

### Narrative

**Quickly learn whether a relevant person is worth continuing with through a limited choice and mutually accepted Live
Conversation, while retaining safety, privacy, and control at every step.**

### Canonical journey

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

The journey is directional, not a funnel every User must complete. A User may decline a Recommendation, withdraw Live
Availability, refuse a Pairing, leave a Live Conversation, choose not to continue, or decide not to meet. Stopping is
not automatically a Meaningful Outcome; it may become one when a participating User considers the resulting informed
non-continuation useful.

## Backbone

The horizontal axis reads left to right as Alex's journey. Seven activities are retained because each marks a required
domain transition in the product hypothesis.

| Activity                                    | User-facing steps                                                                              | Resulting state                                                 |
|---------------------------------------------|------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| 1. Establish trustworthy participation      | Enter deliberately -> create a minimum Dating Profile -> state Dating Intent and Boundaries    | User may participate but is not yet live-available              |
| 2. Declare readiness for live communication | Choose a supported mode -> declare availability now -> understand waiting and session limits   | Revocable Live Availability                                     |
| 3. Consider a limited Candidate             | Review a Recommendation -> understand available context -> express Preview Interest or decline | Preview Interest or completed Recommendation Decision           |
| 4. Establish Conversation Pairing           | Receive a ready-to-enter prompt -> reconfirm availability -> accept room entry                 | Temporary Conversation Pairing based on Mutual Preview Interest |
| 5. Have a Live Conversation                 | Enter the room -> communicate synchronously -> continue, leave, block, or report               | Live Conversation; possibly eligible for a decision             |
| 6. Make a continuation decision             | Reach decision eligibility -> decide privately -> learn the mutual outcome                     | Match or informed non-continuation                              |
| 7. Continue the connection safely           | Open minimal Post-Match Communication -> continue or plan -> pause, end, block, or report      | Ongoing connection or optional Offline Meeting                  |

## Release Slices

The vertical axis is priority. Every slice crosses the journey. **R0** is a concierge or throwaway prototype for early
validation; **R1** is the first complete, safety-capable product pilot, not a profile-only or pairing-only release.

| Activity                   | R0: Concierge/prototype validation                                           | R1: Safety-complete product pilot                                                                             | R2: Better control and learning                                      | Future: Validated extensions                                 |
|----------------------------|------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|--------------------------------------------------------------|
| Establish participation    | Minimum profile, Dating Intent, and Boundaries collected with manual support | Informed entry, minimum Dating Profile, Dating Intent, Boundaries, privacy controls                           | Profile preview, editing impact, consent history                     | Validated profile formats, localization, accessibility modes |
| Declare Live Availability  | Availability-now signal for one configured mode                              | Revocable availability now, one configured live mode, clear waiting and session end                           | Availability windows, mode preference, calm queue information        | Scheduled sessions or additional validated modes             |
| Consider a Candidate       | Manual or simple matching, minimum context, Preview Interest                 | Small predictable set, minimum context, explanation, Preview Interest or decline                              | Preference tuning, better explanations, limited reconsideration      | Validated assessment factors and bounded comparison          |
| Establish Pairing          | Manually coordinated ready-to-enter prompt and room confirmation             | Mutual Preview Interest, availability reconfirmation, room consent, expiry                                    | Pairing controls and technical-failure recovery                      | Validated rematching or scheduling behavior                  |
| Have Live Conversation     | Existing voice/video room with stated privacy limits and an immediate exit   | Product-integrated synchronous room, leave at any time, block, report, privacy protection, elapsed time       | Optional prompts, accessibility support, connection-quality controls | Mutually requested live aids and additional formats          |
| Decide whether to continue | Independently collected Continue Decisions; Match only if reciprocal         | Eligibility after configured threshold, private Continue Decisions, neutral outcome, Match only if reciprocal | Validated decision timing and private reflection                     | Alternative validated outcome paths without forced Match     |
| Continue safely            | Consensual contact exchange after Match and a minimal block/report route     | Minimal Post-Match Communication, end contact, block, report, optional meeting planning                       | Boundary and notification controls, planning support                 | Safety partnerships and consent-based outcome reflection     |

### R0 validation flow

```text
minimum Dating Profile
  -> Dating Intent and Boundaries
  -> Live Availability now
  -> manual or simple Candidate selection
  -> Preview Interest
  -> Conversation Pairing
  -> existing voice/video room
  -> early exit or minimal block/report route
  -> independent Continue Decisions
  -> Match only after reciprocal continuation
  -> consensual contact exchange
```

R0 is intended to test willingness, comprehension, live participation, and continuation decisions before building a
full platform. It does not relax informed consent, immediate exit, privacy disclosure, or a usable route to block and
report. It must not be presented as production-ready safety or moderation.

The exact live mode, duration threshold, Recommendation Limit, waiting policy, and Post-Match Communication channel are
pilot configuration decisions that require validation. R1 must select testable values without presenting them as
universal product truths.

## Activity Details and Tasks

Within each activity, tasks are ordered vertically: **R1** establishes the complete pilot, **R2** deepens the
experience,
and **Future** is conditional on evidence.

### 1. Establish trustworthy participation

**User goal:** Understand the product's purpose and create only the information needed to participate deliberately.

**Main actions:** Confirm eligibility, review expectations, create a minimum Dating Profile, state Dating Intent and
Boundaries, and choose privacy controls.

**System state:** The User and Dating Profile exist with explicit Intent and Boundaries. Live Availability is absent.

**Alternative branches:** The User stops onboarding, belongs to an unsupported pilot segment, withholds optional data,
edits a choice, pauses discovery, or deletes the profile according to policy.

**Safety mechanisms:** Data minimization, clear visibility preview, sensitive-data protection, consent, eligibility or
verification controls selected for the pilot, and access to block/report information before contact.

**R1 tasks:**

1. Confirm adult and pilot eligibility without implying that identity verification guarantees safety.
2. Explain the live-first hypothesis, what the product can do, and what it cannot guarantee.
3. Create and preview a minimum Dating Profile with no unnecessary contact or location data.
4. State a supported Dating Intent and hard Boundaries explicitly.
5. Set visibility and privacy controls before becoming discoverable.

**R2 tasks:**

1. Edit profile, Intent, and Boundaries and understand which future states change.
2. Review consent history and visibility from another User's perspective.
3. Pause discovery while preserving chosen settings and required safety access.

**Future:** Offer validated localized, accessible, or alternative profile presentations without pressuring disclosure.

### 2. Declare readiness for live communication

**User goal:** Indicate a revocable willingness to speak now without consenting to any specific Candidate.

**Main actions:** Choose a supported voice/video setting, declare Live Availability, review the expected wait and
session
boundary, and remain or leave intentionally.

**System state:** Live Availability is active for a bounded period and can be revoked. No Recommendation Decision or
Conversation Pairing exists solely because the User is available.

**Alternative branches:** The User is unavailable, revokes availability, times out, changes a supported mode, receives
no Candidate, or ends the session without penalty.

**Safety mechanisms:** Explicit availability consent, no exposure of raw presence or location, calm timeout, no urgent
countdown, and immediate exit from waiting.

**R1 tasks:**

1. Choose the pilot's supported live mode or decline to begin.
2. Declare availability now for a clearly bounded session.
3. Understand that availability is not consent to a Candidate or Conversation.
4. See a calm waiting state and the natural session endpoint.
5. Revoke availability immediately without losing safety or account access.

**R2 tasks:**

1. Set a bounded availability window and supported mode preference.
2. Receive honest queue information without false certainty or pressure.
3. Control calm reminders without streaks or urgency.

**Future:** Test scheduled availability or additional live modes only if immediate availability is inaccessible or lacks
sufficient liquidity.

### 3. Consider a limited Candidate

**User goal:** Decide whether one relevant Candidate is worth a short Live Conversation without deciding whether to
continue the connection.

**Main actions:** Review the Candidate's minimum profile context and Recommendation Explanation, then express Preview
Interest or decline.

**System state:** A time-bounded Recommendation becomes a Recommendation Decision. A positive decision creates private
Preview Interest; it does not create a Pairing, Match, or persistent channel.

**Alternative branches:** Decline, report or block the Candidate, let the Recommendation expire, revoke availability,
reach the Recommendation Limit, or receive no Candidate.

**Safety mechanisms:** Minimal disclosure, understandable explanation, no hidden worth ranking, private decisions,
pre-contact block/report, and no automatic next Candidate.

**R1 tasks:**

1. See a small, predictable number of Recommendations in the session.
2. Review only the context needed to consider a short Live Conversation.
3. Understand why the Candidate was recommended and what remains uncertain.
4. Express private Preview Interest or decline without urgency.
5. Reach a visible session end without infinite or automatic continuation.

**R2 tasks:**

1. Give structured feedback on explanation usefulness without rating the Candidate's worth.
2. Adjust explicit preferences and understand their future effect.
3. Correct an accidental decision within a fair, bounded policy.

**Future:** Test richer explanations or small bounded comparisons only if they improve calibrated decisions without
increasing overload.

### 4. Establish Conversation Pairing

**User goal:** Confirm that both Users still want and are able to enter the same short Live Conversation.

**Main actions:** Respond to a ready-to-enter prompt, reconfirm Live Availability and room readiness, then enter or
decline the temporary Pairing. Mutual Preview Interest may remain an internal state rather than a separate screen.

**System state:** Mutual Preview Interest plus confirmed availability and room consent creates a temporary Conversation
Pairing. It opens only the initial live room and expires according to policy.

**Alternative branches:** Either User changes their mind, becomes unavailable, does not join, blocks or reports, the
Pairing expires, or a technical failure prevents entry. None creates a Match.

**Safety mechanisms:** Reconfirmation before room entry, private Preview Interest, no persistent contact exchange,
Pairing expiry, block/report, and neutral outcomes that do not reveal who declined.

**R1 tasks:**

1. Understand that another User is also ready to talk without requiring a separate Mutual Preview Interest screen.
2. Reconfirm current availability and willingness to enter the room.
3. Check the configured microphone/camera mode before joining.
4. Enter or decline the Pairing without exposing a private reason.
5. Expire the Pairing safely when consent, availability, or entry is missing.

**R2 tasks:**

1. Recover from a verified technical entry failure without forced rematching.
2. Control Pairing expiry and retry behavior within a fair policy.
3. Receive clearer, non-anxious status information while the other User confirms.

**Future:** Test scheduled Pairings or alternative rematching rules only after measuring availability and no-show
patterns.

### 5. Have a Live Conversation

**User goal:** Gain enough direct context to decide whether continuing might be worthwhile, while remaining free to
leave at any moment.

**Main actions:** Enter the room, communicate synchronously, monitor session state, and continue, leave, mute, block, or
report.

**System state:** Conversation Pairing becomes a Live Conversation. When the configured minimum threshold is reached,
the Conversation becomes eligible for Continue Decisions; eligibility does not measure quality.

**Alternative branches:** Early exit, mutual end, silence, changed consent, abuse, technical failure, or threshold not
reached. These branches must not force continued participation or create a Match.

**Safety mechanisms:** Immediate leave, mute where applicable, block, report, sensitive-data protection, clear elapsed
state, no product-side recording by default, a clear warning that external recording cannot be prevented, and an
operational response path for safety reports.

**R1 tasks:**

1. Enter synchronous communication only after both Users confirm the Pairing.
2. Understand the configured format, duration policy, and privacy limitations.
3. See elapsed state without an urgent timer that pressures completion.
4. Leave, block, or report before or after the threshold without obstruction.
5. Handle early exit and technical failure with a neutral, privacy-preserving outcome.

**R2 tasks:**

1. Use optional conversation or boundary prompts without automated speech or consent.
2. Access validated translation or accessibility support.
3. Follow a fair reconnect policy for verified technical interruption.

**Future:** Add mutually requested live aids or communication formats only after safety, accessibility, and outcome
validation.

### 6. Make a continuation decision

**User goal:** Privately decide whether to continue after an eligible Live Conversation, without pressure or public
rejection.

**Main actions:** Recognize that the decision is available, choose Continue or Do not continue independently, and learn
whether the outcome is mutual.

**System state:** An Eligible Live Conversation allows Continue Decisions. Reciprocal positive decisions create a Match;
any other outcome creates informed non-continuation and no persistent channel.

**Alternative branches:** The Conversation ends before eligibility, either User chooses not to continue, a decision
expires, or decision submission fails. The timing and expiry policies remain open decisions.

**Safety mechanisms:** Private independent decisions, neutral non-Match outcome, no disclosure of who declined, no
forced positive choice, and block/report access independent of duration or outcome.

**R1 tasks:**

1. Make Continue Decision available only after the configured eligibility threshold.
2. Explain that eligibility does not mean the Conversation was meaningful or successful.
3. Let each User choose Continue or Do not continue privately and independently.
4. Create a Match only after two positive Continue Decisions.
5. Communicate non-continuation neutrally and end the temporary connection safely.

**R2 tasks:**

1. Validate whether the decision should happen in-room, immediately after, or within a short window.
2. Offer private reflection without requiring a reason or rating the other User.
3. Recover decision submission safely without leaking the other User's choice.

**Future:** Support other mutually selected next outcomes only if they preserve the meaning of Match and do not create
pressure to continue.

### 7. Continue the connection safely

**User goal:** Continue a mutually chosen connection or plan an Offline Meeting while retaining Boundaries and exit
control.

**Main actions:** Open the supported Post-Match Communication channel, continue talking or plan a meeting, and pause,
end, block, or report the connection.

**System state:** Match opens minimal persistent communication. An Offline Meeting remains optional and external to the
product unless Users consent to planning or outcome feedback.

**Alternative branches:** One User ends contact, communication becomes inactive, plans change, no meeting is desired,
or a safety concern is reported. Match does not create an obligation to respond or meet.

**Safety mechanisms:** Connection-level block/report/end controls, contact and location privacy, meeting safety
guidance,
data minimization, and explicit consent for outcome measurement.

**R1 tasks:**

1. Open one minimal Post-Match Communication channel only after Match creation.
2. Explain that Match permits contact but does not require a reply, relationship, or meeting.
3. Preserve pause, end, block, and report controls inside the Match.
4. Let Users discuss an Offline Meeting without unnecessary contact or location disclosure.
5. Collect outcome feedback only with explicit consent and clear privacy boundaries.

**R2 tasks:**

1. Add connection-level notification and availability Boundaries.
2. Offer optional planning and trusted-contact guidance where operationally appropriate.
3. Explain report status and expected safety response more clearly.

**Future:** Add validated safety partnerships, longitudinal reflection, or additional communication channels without
optimizing for prolonged contact.

## Problem-to-Product-Hypothesis Matrix

Every mechanism below is intended to test a hypothesis about a problem. None is described as a guaranteed solution.

| Problem                             | Product hypothesis                                                                                                             | Mechanism                                                                                            | Expected outcome                                                                | Guardrail                                                                                       | Validation method                                                                                   |
|-------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Choice overload                     | Smaller, bounded choice may support more deliberate decisions                                                                  | Recommendation Limit, no infinite feed, visible session end                                          | Lower perceived overload and more considered Recommendation Decisions           | Do not create artificial scarcity, paid advantage, or hidden viable choices                     | Target-segment interviews plus experiment on set size, comprehension, fatigue, and decision quality |
| Asynchronous communication friction | Coordinating availability and moving quickly to live contact may reduce waiting and unfinished text exchanges                  | Live Availability, Mutual Preview Interest, Conversation Pairing, no mandatory pre-live chat         | Shorter time from Recommendation to real interaction                            | Measure anxiety, exclusion, queue imbalance, no-shows, and safety incidents                     | Pilot cohort with time-to-conversation, pairing completion, qualitative interviews, and harm review |
| Decision fatigue                    | Fewer Candidates and two explicit decisions may reduce repetitive micro-decisions                                              | Preview Interest before conversation; Continue Decision after conversation; complete sessions        | Clearer purpose and stopping points with less reported decision burden          | No automatic continuation, urgent timer, streak, or pressure to decide positively               | Session diary, validated fatigue measures, abandonment reasons, and cross-group comparison          |
| Emotional-regulation use            | Purposeful bounded sessions without retention loops may support more Intentional Usage                                         | Explicit session goal, no endless feed, no variable rewards, successful session exit                 | Less unproductive browsing and clearer reason for use                           | Do not pathologize Users or infer motives from behavior; retain opt-out and support information | Longitudinal self-report and behavioral diagnostics interpreted without causal overclaiming         |
| Matches without meaningful progress | Reserving Match for mutual post-conversation continuation may make the state more informative                                  | Eligible Live Conversation plus reciprocal positive Continue Decisions                               | A larger share of Matches represents informed mutual willingness to continue    | Match count is not a success metric; early exit and non-continuation remain valid outcomes      | Compare downstream informed outcomes and safety guardrails with an appropriate baseline             |
| Fear and insufficient trust         | Minimum context, validated trust signals, format control, and immediate safety controls may make early live contact acceptable | Minimum Dating Profile, pilot verification choice, room reconfirmation, privacy, exit, block, report | More Users can decide safely whether to enter and remain in a Live Conversation | Never claim verification guarantees safety; minimize sensitive data; measure harms by group     | Usability and safety research, threat modeling, report audits, and segmented opt-in/exit rates      |
| Low-quality profile-only decisions  | Treating profile response as Preview Interest and deciding after live contact may improve informed choice                      | Separate Recommendation Decision from Continue Decision                                              | Users base continuation on direct interaction as well as profile context        | Do not claim duration equals quality or force Users to reach the threshold                      | Comprehension tests, post-conversation confidence, regret, and qualitative outcome interviews       |
| Ghosting after an app-defined match | Requiring synchronous contact before Match may move non-continuation earlier and reduce empty persistent channels              | No persistent channel before reciprocal post-conversation continuation                               | Fewer Matches that never contain mutual contact                                 | Do not merely relocate rejection harm; monitor early exit, pressure, and availability exclusion | Compare no-response outcomes, perceived rejection, and safety before and after the pilot model      |

## Open Decisions Requiring Validation

The following must not be fixed as universal product rules without additional evidence:

1. The user-facing and internal name for `Conversation Pairing`.
2. Voice, video, or a User-selectable combined mode.
3. The value and policy meaning of the minimum duration **N**.
4. The amount and type of Dating Profile information visible before a Live Conversation.
5. The number and period of Recommendations in a session.
6. The overall Live Conversation duration and whether a maximum exists.
7. Waiting, expiry, no-show, and queue behavior while seeking another available User.
8. The Post-Match Communication channel.
9. Repeat-pairing, rematching, and accidental-decision correction rules.
10. Report, moderation, evidence-handling, escalation, and response-time policy.
11. Whether Recommendations are generated only between simultaneously live-available Users or whether Preview Interest
    may persist across availability windows.
12. Whether Mutual Preview Interest appears as a separate User-facing state or is represented only by a ready-to-enter
    Conversation prompt.

## Success Signals and Guardrails

Candidate pilot signals include:

- Users understand Preview Interest, Conversation Pairing, eligibility, Continue Decision, and Match as distinct states;
- Users can explain why a Recommendation appeared and what remains uncertain;
- bounded sessions end without pressure to continue;
- Users reach a mutually entered Live Conversation within an acceptable wait;
- every User can leave, block, and report before, during, and after a Live Conversation;
- eligible Users make private Continue Decisions without interpreting the threshold as a quality verdict;
- Matches represent reciprocal post-conversation continuation;
- Users report informed continuation or non-continuation without unacceptable fatigue, anxiety, abuse, privacy harm,
  technical failure, or unequal access across groups.

Views, Preview Interests, Pairings, Conversation minutes, Matches, messages, time spent, and return visits may diagnose
the journey, but none is sufficient evidence of User value by itself.

## Explicit Non-goals

The map excludes:

- infinite profile browsing, streaks, variable rewards, and artificial urgency;
- calling Preview Interest, Mutual Preview Interest, or Conversation Pairing a Match;
- mandatory persistent messaging before a Live Conversation;
- hidden rankings of people or claims that Compatibility Assessments are verdicts;
- automated Preview Interest, room consent, Continue Decisions, messages, or pressure to continue;
- forcing Users to remain in a Live Conversation until the threshold;
- revealing which User declined after informed non-continuation;
- postponing exit, block, report, privacy, or sensitive-data protection beyond R1;
- payment for visibility, another person's attention, hidden decisions, or queue priority;
- guarantees of compatibility, a Match, relationship, Offline Meeting, or personal safety;
- public ratings of rejection, Conversation quality, or a User's worth.

## Alignment Changelog — 2026-08-06

### Contradictions resolved

- The former path created Match from reciprocal profile-level interest and placed Conversation afterward.
- The previous story map had already moved live contact earlier but used competing terms: `Interest`, `Qualifying
  Conversation`, and `Match Decision`.
- `Post-Match Support` previously included starting a first Meaningful Conversation, which now occurs before Match.

### Definitions changed

- `Preview Interest` and `Mutual Preview Interest` now describe willingness to try a Live Conversation.
- `Conversation Pairing` now describes the temporary, consent-confirmed connection for that Conversation.
- `Eligible Live Conversation` describes only threshold eligibility, not Conversation quality.
- `Continue Decision` is the private post-conversation decision.
- `Match` now exists only after reciprocal positive Continue Decisions.
- `Post-Match Communication` is the persistent channel available after Match.
- `Meaningful Conversation` now depends on participating User report, and a merely technical Live Conversation is not
  automatically a Meaningful Outcome.
- Continue Decision eligibility is now expressed as availability of the decision, not automatic creation of one.

### Hypotheses intentionally left open

Synchronous communication effectiveness, voice versus video, N, Recommendation Limit, pre-conversation information,
the relationship between Recommendation and Live Availability, visibility of Mutual Preview Interest, waiting design,
Match timing details, Post-Match Communication, rematching, and moderation operations remain subject to research and
pilot evidence.

### Sources of truth

- [glossary.md](./glossary.md) owns canonical terms and state distinctions.
- [vision.md](./vision.md) owns the problem, audience, product hypothesis, and intended outcome.
- [philosophy.md](./philosophy.md) owns product beliefs and value judgments.
- [principles.md](./principles.md) owns enforceable product decision rules and guardrails.
- [research.md](./research.md) owns evidence, methods, limitations, and unanswered research questions.
- This story map owns the hypothesized journey, release slices, traceability matrix, and open product decisions.
