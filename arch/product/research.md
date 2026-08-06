# Product Research Rationale

This document records empirical findings relevant to the problem described in [vision.md](./vision.md). It contains
sources, methods, results, and interpretation limits; it does not define product strategy or decision rules.

Product decisions derived from this evidence belong in [principles.md](./principles.md).

## Summary of Findings

- One US market survey suggests that self-reported exhaustion is widespread, but it cannot measure clinical burnout or
  support generalization to all dating-app users.
- Three sequential-choice studies found that profile acceptance became less likely as participants progressed through
  the available options. The samples and scenarios were narrow, and the results do not identify an optimal product
  limit.
- A separate online experiment found that more profiles increased perceived choice overload and reduced the share of
  accepted profiles. It did not measure long-term well-being or real dating outcomes.
- In a cross-sectional Tinder study, problematic use was most strongly associated with coping, mood enhancement, and
  social connection motives, as well as contact intensity. The causal direction of these relationships is unknown.
- None of the current studies establishes that a particular product design will improve real-world outcomes in Make
  Dating Free Again.

## Evidence-Supported Problem Signals

The sources provide grounds for treating the following as product problems worth investigating, with the stated
limitations:

- **Choice overload:** Higher profile volume increased perceived overload in one controlled online experiment, and
  acceptance declined across sequential choices in three studies. These results do not define an optimal limit.
- **Fatigue from repeated decisions:** Self-reported exhaustion and sequential-choice effects are consistent with this
  concern, but the studies do not isolate every source of fatigue or establish long-term causality.
- **Low-quality or unfinished interactions:** A market survey included inability to find a good connection and
  repetitive conversations among reported reasons for exhaustion. It does not establish prevalence across markets or
  prove that asynchronous communication causes those experiences.
- **Coping, mood enhancement, and social connection motives:** These motives were associated with problematic Tinder
  use in cross-sectional data. Direction of causality is unknown.
- **Interaction volume without demonstrated meaningful outcomes:** Match and contact counts appear in the source set,
  but the studies do not show that more Matches cause better outcomes. The claimed gap between Match volume and
  Meaningful Outcomes remains incompletely measured.

Here and in the source summaries, lowercase terms such as “match” or “acceptance” retain the original study's meaning;
they must not be interpreted as the canonical product state **Match** defined in [glossary.md](./glossary.md).

## Product Hypotheses, Not Findings

The current product model tests whether:

- a small, predictable Recommendation set and complete sessions reduce perceived overload and decision fatigue;
- explicit Live Availability and Conversation Pairing shorten the path from Preview Interest to real interaction;
- a short synchronous Live Conversation provides enough context for a more informed Continue Decision than profile
  evaluation alone;
- creating a Match only after reciprocal positive Continue Decisions reduces persistent connections that never become
  meaningful;
- immediate exit, block, report, privacy, and trust mechanisms make early live contact acceptable and safer;
- removing endless feeds, streaks, variable rewards, and automatic continuation supports Intentional Usage.

None of these effects is established by the studies below. Voice versus video, the minimum duration, Recommendation
Limit, waiting design, and Post-Match Communication channel are open decisions rather than validated requirements.

## 1. Self-Reported Dating-App Exhaustion

### Source

[Forbes Health Survey: 78% Of All Users Report Dating App Burnout](https://www.forbes.com/health/dating/dating-app-fatigue/),
a survey commissioned by Forbes Health and conducted by OnePoll. Data was collected from March 27 to April 1, 2024, and
the article was published in 2025.

### Design

An online survey of 1,000 US adults who had used a dating app during the previous year. Forbes reports a margin of error
of ±3.1 percentage points at a 95% confidence level, but does not publish the questionnaire, sampling and weighting
method, response rate, or demographic subgroup sizes.

This is an editorial and commercial market survey, not a peer-reviewed scientific study.

### Findings

- 78% of respondents said they sometimes, often, or always felt emotionally, mentally, or physically exhausted by
  dating apps.
- The same response was reported by 80% of millennials, 79% of Gen Z respondents, 80% of women, and 74% of men.
- Reported reasons included an inability to find a good connection at 40%, disappointment in people at 35%, feeling
  rejected at 27%, repetitive conversations at 24%, swiping at 22%, and time spent on apps at 21%.

### Interpretation Limits

Combining “sometimes,” “often,” and “always” does not constitute a measure of clinical burnout. Self-report data does
not establish that the app caused the exhaustion. The result describes a specific US sample and should not be presented
as a universal prevalence estimate.

## 2. Sequential Choice and the Rejection Mindset

### Source

Tila M. Pronk and Jaap J. A. Denissen,
[A Rejection Mind-Set: Choice Overload in Online Dating](https://doi.org/10.1177/1948550619866189),
*Social Psychological and Personality Science*, 2020.

### Design

The authors conducted three studies of swipe-like sequential choice:

- 315 single, heterosexual participants aged 18–30 evaluated 45 or 90 hypothetical profiles;
- 158 single, heterosexual participants aged 18–29 evaluated 40–45 real participants with the possibility of a mutual
  match;
- 305 single, heterosexual participants aged 18–30 evaluated 50 hypothetical profiles and reported satisfaction with
  the images and perceived dating success.

### Findings

Across the three studies, the probability of accepting a profile fell by approximately 27% on average from the first to
the last option. In the study with real participants, acceptance probability fell by approximately 29%; match
probability declined significantly only for women. In the third study, declining acceptance among women was associated
with lower satisfaction with the images and lower perceived success.

### Interpretation Limits

The studies included young, single, heterosexual participants, and two of the three used hypothetical profiles. The
observed behavioral breakpoints differed between studies, so the evidence does not define a universal profile limit.
Exposure sequence was also closely related to the accumulated number of rejections, and the authors note that future
experiments need to separate these factors.

The study did not test exposure to hundreds or thousands of profiles per day and does not demonstrate a general decline
in match probability across all groups.

## 3. Profile Volume and Decision Mode

### Source

Marina F. Thomas, Alice Binder, and Jörg Matthes,
[Decision-Making on Dating Apps: Is Swiping More Less and Swiping Right Wrong?](https://doi.org/10.1080/15213269.2025.2555430),
*Media Psychology*, 2025. The authors published the experiment's [data and materials](https://osf.io/jxbz9/).

### Design

A 3×3 online experiment: participants viewed 11, 31, or 91 profiles and were assigned to one of three decision modes—a
control condition, a fast and intuitive locomotion mode, or a critical assessment mode focused on making a defensible
choice. The sample included 401 University of Vienna students with a mean age of 22.1; 85% were women, 46.4% were in a
relationship, and 54.1% had never used a dating app. Decisions were made in a mock interface and did not lead to real
contact.

### Findings

More profiles increased perceived choice overload and reduced the share of accepted profiles. Profile volume did not
affect state self-esteem, perceived mate value, or fear of being single.

The fast, intuitive mode was associated with small reductions in state self-esteem and perceived mate value compared
with the assessment and control modes. Perceived overload also emerged earlier in this mode.

### Interpretation Limits

The sample was young, predominantly female, and composed of students. More than half of the participants had no
dating-app experience, and nearly half were in a relationship. The experiment measured short-term responses to an artificial
scenario without real consequences. It measured choice overload, not long-term fatigue or burnout.

## 4. Predictors of Problematic Tinder Use

### Source

Gonçalo Vera Cruz et al.,
[Online dating: predictors of problematic Tinder use](https://doi.org/10.1186/s40359-024-01566-3),
*BMC Psychology*, 2024.

### Design

A secondary analysis of cross-sectional self-report data from 1,387 English-speaking Tinder users aged 18–74.
Participants were recruited through social media, forums, and websites; their country of residence was not recorded.
The authors examined 29 potential predictors using correlations, analysis of variance, and a Random Forest model.

### Findings

The mean problematic-use score was 1.91 out of 5, indicating a generally low level in the sample. The model's most
important predictors were:

- using Tinder to cope with psychological difficulties;
- number of online contacts;
- using Tinder to reduce boredom and increase positive emotions;
- number of offline contacts;
- social connection motive;
- number of matches.

Loneliness and depressed mood appeared among the predictors but were not leading ones. The model explained 58% of the
variance in the test data.

### Interpretation Limits

The sample was non-random and may not represent all Tinder users or users of other services. The cross-sectional design
cannot establish causal direction: coping motives may contribute to problematic use, problematic use may aggravate
difficulties, or both may share another cause.

The study does not show that most people use Tinder instead of seeking relationships, that the app causes depression, or
that it necessarily aggravates loneliness. Problematic Tinder use is not a standalone DSM-5 diagnosis.

## What Is Not Established

The current evidence base does not establish that:

- dating apps generally and intentionally cause addiction;
- a particular daily recommendation limit is optimal;
- limiting profiles alone reduces clinical burnout;
- transparent recommendation explanations necessarily improve trust;
- synchronous communication is more effective than asynchronous messaging;
- video is more effective, safer, or more comfortable than voice;
- a particular number of minutes is sufficient for an informed Continue Decision;
- reaching the eligibility threshold means a Live Conversation was meaningful or successful;
- Users will want to enter a Live Conversation before persistent messaging;
- creating a Match after a Live Conversation improves the likelihood of an Offline Meeting;
- synchronous communication reduces ghosting;
- more app-defined matches produce more meaningful meetings;
- the observed effects are consistent across ages, countries, genders, orientations, and dating intentions;
- app use causes loneliness or depressed mood.

These claims may be framed as research questions, but not as findings from the studies listed above.

## Research Questions and Evidence Gaps

The current source set does not provide direct evidence needed to answer:

1. Are target Users willing to enter synchronous communication before persistent messaging?
2. What Dating Profile information and trust signals are necessary before a Live Conversation?
3. Is voice, video, or a User choice between them more comfortable and accessible?
4. How does early live contact affect anxiety, harassment risk, privacy, and perceived safety?
5. What minimum duration, if any, is acceptable before the Continue Decision becomes available?
6. What happens when a User leaves before that threshold, and how should the other User experience the outcome?
7. Does synchronous communication reduce ghosting or merely move rejection earlier?
8. Is simultaneous Live Availability sufficient across groups and times to produce acceptable waiting?
9. How do barriers, waiting times, safety outcomes, and benefits differ across User groups?
10. Which verification, profile, consent, moderation, and safety mechanisms are needed before a Conversation Pairing?
11. How does the target audience define overload, a good Recommendation, and a Meaningful Outcome?
12. What Recommendation Limit is appropriate for the target audience without creating artificial scarcity?
13. Does deliberate profile consideration improve real dating outcomes?
14. How do Recommendation Explanations affect comprehension, trust, and confidence calibration?
15. Does Post-Match Support improve informed continuation or safe Offline Meetings?
16. Which operational policy, response time, and evidence handling are required for reports and moderation?
17. Must Recommendations connect only simultaneously live-available Users, or can Preview Interest persist across
    availability windows without weakening the synchronous-first hypothesis?

Internal surveys should be added to this review only with their questionnaire, sample description, collection dates,
and limitations. Undocumented anonymous surveys cannot serve as reproducible evidence.
