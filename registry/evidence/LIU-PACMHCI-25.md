## [LIU-PACMHCI-25] Understanding Decentralized Social Feed Curation on Mastodon
**Citation:** Yuhan Liu, Emmy Song, Owen Xingjian Zhang, Jewel Merriman, Lei Zhang, Andrés Monroy-Hernández. "Understanding Decentralized Social Feed Curation on Mastodon." Proceedings of the ACM on Human-Computer Interaction (CSCW), 2025. DOI 10.1145/3757688.
**Retrieved:** full text via https://arxiv.org/abs/2504.18817
**Source URL:** https://arxiv.org/abs/2504.18817
**Domain:** K

### What it does
The paper reports a two-part interview study of Mastodon users and, from the first part's findings,
builds and tests braids.social, a prototype web client that lets a user compose one unified feed from
three of Mastodon's existing API-exposed feeds by setting a priority level per source, without any
server-side or platform-supplied ranking model.

Part one: eleven participants (P1–P11) gave 60-minute interviews about their existing Mastodon feed
use — which of the platform's built-in feeds (home, local, federated) they read, how they choose a
home server, and what third-party tools they already use to filter content.

Part two: braids.social is a Flask (backend) and React (frontend) web client that authenticates to a
user's Mastodon account over OAuth 2.0 with read-only permissions, then calls three existing Mastodon
API endpoints — Home Timeline, Public (with the `local` parameter), and Trending Status — each
returning 40 posts per call. Each source is assigned a priority level (None, Low, Medium, High
Priority) by the user through a slider. The client merges the returned posts into one display list,
placing posts from a higher-priority source above posts from a lower-priority source, while posts
within a single source's fragment retain that source's original chronological order. Each displayed
post carries a badge showing which source it was drawn from — "Users you follow," "Hashtag you
follow," "Trending post," "Local post," or "Prioritized account" — assigned once, from the first
source the post was seen in, to avoid a post carrying two badges when duplicated across sources. A
separate control lets a user pin up to a small number of specific accounts, on any Mastodon instance,
to always surface regardless of follow status. Ten of the eleven part-one participants (P12–P21) then
used braids.social in a further 60-minute session, completing three assigned feed-configuration tasks
and reporting on the experience.

### Measured results
This is a qualitative interview study; it reports no throughput, latency, message-count, or
scalability figures. The only reported figures are counts of participant responses within the fixed
interview sample:

| Finding | Count | Condition |
|---|---|---|
| Preferred Mastodon's chronological (non-algorithmic) feed order | 8 of 11 part-one participants | Open-ended interview question comparing chronological and algorithmic feeds |
| Switched their home server at least once | 3 of 11 part-one participants (P2, P3, P7) | Self-reported over the course of platform use, no fixed time window given |
| Preferred third-party Mastodon clients over the official app | 7 of 11 part-one participants | Self-reported client choice |
| Set "Home feed" (Following Content) to High priority and other sources to None/Low/Medium in braids.social | 9 of 10 part-two participants (all but P18) | Free configuration during the unstructured part of the part-two session, recorded in Table 1 |
| Given the task "make one source show roughly twice as many posts as another," chose the High/Low priority-level pair | 7 of 10 part-two participants | Task 3 of the assigned configuration tasks; the remaining 3 chose High/Medium |

Table 1 in the paper lists each of the 10 part-two participants' (P12–P21) chosen priority level
(None/Low/Medium/High) for each of the four source categories (Following Content, Local Posts,
Trending Posts, Accounts) during their free-form session with braids.social; it is a record of stated
individual preferences, not an aggregate measurement with a denominator beyond n=10.

### Parameters
| Parameter | Value used | Range tested |
|---|---|---|
| Posts retrieved per API call | 40, fixed, per source per request | Not varied |
| Priority levels per source | 4 discrete levels: None, Low, Medium, High Priority | Not varied; participants report difficulty distinguishing Medium from adjacent levels |
| Feed sources merged | 3 (Following Content = Home Timeline API, Local Posts = Public API with local parameter, Trending Posts = Trending Status API) plus a separate "Prioritized accounts" pin list | Fixed set; not varied |
| Interview sample size | 11 (part one), 10 of the same 11 (part two) | Not varied; the paper states this is a limitation |
| Authentication scope | OAuth 2.0, read-only | Not varied |

### Stated limitations
The authors state the findings are limited by small sample size, and that Mastodon users are, by
their own account, "generally more concerned about algorithmic transparency, anti-corporation, and
privacy than traditional social media users," so the sample may not generalize even within Mastodon's
own user base. Recruitment ran through Google Forms and Zoom, which the authors say may have
deterred some Mastodon users from participating. The authors state findings on Mastodon feed curation
may have limited generalizability to other decentralized platforms — PeerTube, Pixelfed — whose users
form different strong-tie/weak-tie interaction patterns, and separately that Mastodon's ActivityPub
protocol differs in decentralized architecture and information flow from AT Protocol and Farcaster,
so results may not transfer to platforms built on those protocols without adaptation. Participants in
the braids.social session reported difficulty precisely interpreting what distinguishes the "Medium"
priority slider setting from "Low" or "High"; the authors state they leave to future work "the optimal
level of granularity" for the slider affordance. The authors did not test whether user attitudes
toward machine-learning-based curation would shift if applied by a non-profit, ad-free operator,
stating this as an open question.

### Requirements it places on the rest of the system
braids.social is built entirely as a client against Mastodon's existing, unmodified server-side API;
it requires no protocol change and no new server-side capability beyond what the Home Timeline,
Public, and Trending Status endpoints already expose. It requires the home server to run the Trending
Status endpoint (the paper notes this is itself a server-side re-ranking of the federated feed by
popularity and time, so braids.social's "Trending Posts" source already depends on one piece of
algorithmic ranking computed off-client). It requires OAuth 2.0 read-only account access; no write or
posting capability is used. The client performs no local storage or persistence of the merged feed
across sessions beyond what is described; each session's badge assignment and fragment ordering are
recomputed from whatever the three API calls return at request time, so the merge mechanism requires
no cross-session state and no coordination between multiple client instances of the same user.

### Contradicts
None found. No claim about message counts, scalability, or attack resistance is made or misattributed
to this paper in the reviewed corpus.

### References worth retrieving
- **Raman, Joglekar, De Cristofaro, Sastry, Tyson, "Challenges in the decentralised web: The mastodon case," IMC 2019** — competing/foundational measurement study of Mastodon's deployed network, cited [64].
- **Zhang, Zhao, Wang, Johnston, Chalhoub, Ross, Liu, Tinsman, Zhao, Van Kleek et al., "Trouble in Paradise? Understanding Mastodon Admin's Motivations, Experiences, and Challenges," PACM HCI (CSCW2) 2024** — competing qualitative study on Mastodon governance/moderation, cited [81]; overlapping authorship with ZHANG-ARXIV-25 in this corpus.
- **Anaobi, Raman, Castro, Bin Zia, Ibosiola, Tyson, "Will Admins Cope? Decentralized Moderation in the Fediverse," WWW 2023** — foundational measurement of Mastodon moderation labor, cited [2].
- **La Cava, Greco, Tagarelli, "Understanding the growth of the Fediverse through the lens of Mastodon," Applied Network Science 2021** — foundational network-growth measurement, cited [48].
- **La Cava, Greco, Tagarelli, "Information consumption and boundary spanning in Decentralized Online Social Networks: The case of Mastodon users," Online Social Networks and Media 2022** — foundational measurement of cross-instance information flow, cited [49].
- **Zignani, Gaito, Rossi, "Follow the 'mastodon': Structure and evolution of a decentralized online social network," ICWSM 2018** — foundational structural measurement, cited [83].
- **He, Gordon, Popowski, Bernstein, "Cura: Curation at Social Media Scale," PACM HCI (CSCW2) 2023** — competing curation-tool system, cited [39].
- **Feng, Koo, Tan, Bruckman, McDonald, Zhang, "Mapping the Design Space of Teachable Social Media Feed Experiences," arXiv 2024** — competing/foundational feed-curation design work, cited [29].
- **Jeong, Sheth, Tahir, Alatawi, Bernard, Liu, "Exploring platform migration patterns between twitter and mastodon," arXiv/ICWSM 2023** — foundational migration measurement, cited [43].

### Verbatim extracts
"we conducted a two-part interview study with 21 participants" (line 86).
"nine out of ten participants (except P18) put the following content...as a high priority" (line 556-557).
"seven out of ten participants set the categories to high and low priority" (line 605-606).
"Our findings indicate that while visual cues and real-time feedback improved transparency" (line 643).
"our findings are limited by the small sample size" (line 717).
"limited generalizability across other decentralized platforms with different interaction dynamics" (lines 728-729).
