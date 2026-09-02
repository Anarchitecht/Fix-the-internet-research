## [HE-IMC-23] Flocking to Mastodon: Tracking the Great Twitter Migration

**Citation:** Haris Bin Zia, Jiahui He, Aravindh Raman, Ignacio Castro, Nishanth Sastry, Gareth Tyson. "Flocking to Mastodon: Tracking the Great Twitter Migration." ACM Internet Measurement Conference (IMC), 2023. DOI 10.1145/3618257.3624819.
**Retrieved:** full text via https://arxiv.org/abs/2302.14294
**Source URL:** https://doi.org/10.1145/3618257.3624819
**Domain:** K

### What it does
The paper measures what happened when a large user cohort moved, over a few weeks, from Twitter to Mastodon, a federated microblogging platform where any operator can run an independent server (an instance) and instances interconnect by subscribing to each other's posts through the ActivityPub protocol. A user account belongs to one home instance; a home instance's own users see three feeds — a home timeline of accounts they follow, a local timeline of every post from other accounts on the same instance, and a federated timeline of every remote post any user on that instance has caused the instance to retrieve by following a remote account. Following a remote-instance account requires no separate registration: the follower's own instance performs the cross-instance subscription on the user's behalf. The authors built a Twitter-to-Mastodon account mapping by first compiling a list of 15,886 known Mastodon instances from instances.social, then collecting every tweet linking to one of those instances or containing migration-related keywords and hashtags (2,090,940 tweets from 1,024,577 users, October 26 to November 21, 2022), then searching each poster's bio, tweet text, and profile metadata for a Mastodon handle, accepting a match from tweet text only when the Twitter and Mastodon usernames were identical. This identified 136,009 Twitter users who created accounts across 2,879 Mastodon instances. The authors then crawled each mapped user's full timeline on both platforms (Twitter Search API, Mastodon's Account Statuses endpoint) and, for a 10% subsample selected to be representative of the followee-count distribution, each user's followee list on both platforms (Twitter Follows API, Mastodon's Account Following endpoint), and scored every collected post for toxicity using Google Jigsaw's Perspective API TOXICITY attribute (threshold 0.5) and for cross-platform content overlap using cosine similarity of Sentence-BERT embeddings (similarity greater than 0.7 counted as "similar").

### Measured results
All figures below are drawn from the 136,009-user, 2,879-instance mapped dataset, tweets and statuses collected October 1-November 30, 2022, unless a narrower condition is stated.

| Metric | Value | Condition |
|---|---|---|
| Mastodon accounts created before Musk's acquisition, among mapped accounts | 21% | full 136,009-user set |
| Users whose Mastodon username matches their Twitter username | 72% | full set |
| Mapped users holding legacy Twitter verified status | 4% | full set |
| Share of users on the top 25% of instances by user count | 96% | full set, 2,879 instances |
| Users who deleted their Twitter account entirely (interpreted from the Conclusion) | 2.26% | full set, of those whose Twitter timeline was attempted to be crawled |
| Statuses posted (single-user instance users vs. bigger-instance users) | +121.14% (single-user instance users post more) | users with 30-day-old accounts, joined after acquisition, covering 50.59% of migrated users |
| Followers, followees (single-user instance users vs. bigger-instance users) | +64.88% followers, +99.04% followees | same subset as above |
| Instances that are single-user | 13.16% of all 2,879 instances | full instance set |
| Median Twitter followers / followees of migrated users | 744 / 787 | full set |
| Median Mastodon followers / followees of migrated users | 38 / 48 | full set (median account age at measurement: 35 days, vs. 11.5 years on Twitter) |
| Mastodon users with zero followers / zero followees | 6.01% / 3.6% | full set |
| Twitter users with zero followers / zero followees | 0.11% / 0.35% | full set |
| Users whose migrated Mastodon follower count exceeds their Twitter follower count | 1.65%, by a median of 33 more followers | full set |
| Twitter followees (per user, on average) who also migrated to Mastodon | 5.99% | 10% followee subsample, 13,068 users, 11,453,484 followee edges |
| Migrated users whose Twitter followees never migrated | 3.94% | same subsample |
| Followees who migrated before the user did (average per user) | 45.76% | same subsample |
| Followees who join the user's exact same instance (average per user) | 14.72% | same subsample |
| Of users whose followees share their instance, the fraction on mastodon.social | 30.68% | same subsample |
| Users who switched their Mastodon instance after account creation | 4.09% of the full mapped set | full set |
| Instance switches occurring after the Twitter acquisition | 97.22% | of the 4.09% who switched |
| Followees (per switching user, average) who joined the user's second instance | 46.98%, vs. 11.4% who joined the first instance | switching-user subsample |
| Followees who joined the second instance before the user did | 77.42% | switching-user subsample |
| Mastodon statuses per user that are byte-identical to a Twitter post | 1.53% average | full set with crawled timelines |
| Mastodon statuses per user that are semantically similar (cosine similarity greater than 0.7) to a Twitter post | 16.57% average | same |
| Users posting entirely non-overlapping content across platforms | 84.45% | same |
| Cross-posting tool users (Mastodon-Twitter Crossposter or Moa Bridge, at least once) | 5.73% of migrated users | full set; the two tools' tweet volume rose 1128.95% and 1732.26% respectively after the acquisition |
| Toxic tweets on Twitter (Perspective TOXICITY greater than 0.5) | 5.49% of tweets, 4.02% average per user | migrated users' Twitter timelines |
| Toxic statuses on Mastodon | 2.80% of statuses, 2.07% average per user | migrated users' Mastodon timelines |
| Users posting at least one toxic item on both platforms | 14.26% | full set with both timelines crawled |
| Twitter timelines successfully crawled | 94.88% of the 136,009 users (0.08% suspended, 2.26% deleted/deactivated, 2.78% protected) | timeline crawl step |
| Mastodon timelines successfully crawled | 79.22% (9.20% had zero statuses, 11.58% instance unreachable at crawl time) | timeline crawl step |

Total volume crawled: 16,163,600 tweets and 5,746,052 Mastodon statuses.

### Parameters
Instance directory source: instances.social, 15,886 unique instances at the time of collection. Tweet collection window: October 26-November 21, 2022, via Twitter's full-archive Search API, matched against a fixed keyword/hashtag list ('mastodon', 'bye bye twitter', 'good bye twitter', #Mastodon, #MastodonMigration, #ByeByeTwitter, #GoodByeTwitter, #TwitterMigration, #MastodonSocial, #RIPTwitter) or a link to one of the 15,886 instances. Timeline crawl window: October 1-November 30, 2022. Followee subsample size: 10% of the 136,009 mapped users, drawn to include 5% from above and 5% from below the median followee count (Twitter API rate limits made a full crawl infeasible). Toxicity threshold: Perspective API TOXICITY score greater than 0.5, cited as the most common threshold choice in prior work, with 0.8 noted as an alternative used elsewhere. Content-similarity threshold: Sentence-BERT cosine similarity greater than 0.7 to count a Mastodon status as "similar" to a tweet. Handle-matching rule: a username found in free tweet text is accepted as a cross-platform match only when it is character-identical between the Twitter and Mastodon accounts; a username found in structured profile metadata (bio, pinned tweet, URLs) is accepted without that identity requirement.

### Stated limitations
The authors state their 136,009-user mapped cohort is a lower bound: Mastodon's own operator reported over 1 million new registrations in the same window, "significantly more" than the mapping method identified, because the method depends on a user voluntarily posting a discoverable link or matching username on Twitter. The paper states it cannot confirm that registrations observed through Mastodon's Weekly Activity Endpoint came directly from Twitter, only that the timing makes this likely. The authors state that the disproportionate account ages between platforms (median 11.5 years on Twitter vs. 35 days on Mastodon at measurement time) make the two platforms' social-network sizes "not directly comparable," so the follower/followee gap partly reflects account age rather than platform structure alone. The followee-influence analysis (RQ2) covers only a 10% subsample due to Twitter API rate limits, not the full mapped cohort. The paper states its toxicity comparison should not be read as evidence Mastodon needs less moderation: unlike Twitter, which the authors state has "its own moderation team," Mastodon's instances rely on volunteer administrators, so the 14.26% of users posting toxic content on both platforms is stated as a moderation burden specifically for that volunteer model. The authors state the future direction of retention (whether migrated users keep their Mastodon accounts or return to Twitter) is unresolved by this study and left as future work.

### Requirements it places on the rest of the system
A follow relationship in this federation design requires the follower's home instance to perform and maintain a subscription to the followed account's home instance on the user's behalf; this is what makes the federated timeline exist as the union of all posts any local user's following relationships have pulled in, and a client or protocol design that skips per-instance subscription bookkeeping cannot reproduce a federated timeline. Instance choice functions as an availability dependency for both the follower and the followed: the paper's crawl documents 11.58% of mapped users' Mastodon timelines unreachable specifically because those users' home instances were down at crawl time, meaning a user's post history and reachability are only as available as the single instance operator hosting them, unlike Twitter's centrally operated storage. Handle-based discovery of a real-world identity requires the identity string to be reused deliberately by the account holder across platforms, since the paper's own mapping accuracy depended on exact username matches; a design that wants to link identities across independent federated deployments needs either a convention like this or a separate cross-platform identity assertion mechanism, because ActivityPub itself supplies no such linkage. Any moderation architecture layered onto a federated design of this shape must be evaluated per-instance rather than network-wide, since toxicity and its handling are stated to depend on each instance's own (often single, volunteer) administrator, not on any platform-wide policy actor.

### Contradicts
None found within this corpus. The paper states its own instance-concentration finding (96% of users on the top 25% of instances) is consistent with the earlier Raman et al. IMC 2019 Mastodon study cited in its bibliography, and explicitly frames its smaller-instances-more-active finding as a paradox alongside, not a contradiction of, that concentration result.

### References worth retrieving
- Raman, Joglekar, De Cristofaro, Sastry, Tyson, "Challenges in the Decentralised Web: The Mastodon Case," ACM IMC 2019 — foundational (the prior large-scale Mastodon centralization measurement this paper builds on and compares against directly)
- Anaobi, Raman, Castro, Bin Zia, Ibosiola, Tyson, "Will Admins Cope? Decentralized Moderation in the Fediverse," ACM Web Conference 2023 — competing/related (measures the volunteer-moderation burden this paper's toxicity section raises but does not itself analyze)
- Bin Zia, Raman, Castro, Hassan Anaobi, De Cristofaro, Sastry, Tyson, "Toxicity in the Decentralized Web and the Potential for Model Sharing," Proc. ACM Measurement and Analysis of Computing Systems 6(2), 2022 — foundational (prior toxicity measurement on the decentralized web by an overlapping author set, proposing a model-sharing moderation mechanism)
- Hassan, Raman, Castro, Bin Zia, De Cristofaro, Sastry, Tyson, "Exploring Content Moderation in the Decentralised Web: The Pleroma Case," ACM CoNEXT 2021 — foundational (moderation-architecture case study on a related federated platform)
- Fiesler, Dym, "Moving Across Lands: Online Platform Migration in Fandom Communities," Proc. ACM Human-Computer Interaction 4(CSCW1), 2020 — competing (prior platform-migration measurement methodology, different platform)
- Otala, Kurtic, Grasso, Liu, Matthews, Madraki, "Political Polarization and Platform Migration: A Study of Parler and Twitter Usage," Web Conference 2021 Companion — competing (prior Twitter-to-alternative-platform migration measurement)
- Paul, Famulari, Strufe, "A Survey on Decentralized Online Social Networks," Computer Networks 75, 2014 — foundational (survey covering the earlier P2P social-network generation, Safebook/PeerSoN/LotusNet/LifeSocial.KOM, that this paper cites as predecessors to Mastodon)

### Verbatim extracts
"the top 25% most populous instances contain 96% of the users"
"users of single-user instances post 121% more statuses than users on bigger instances"
"only 1.53% of a user's Mastodon posts are identical to their Twitter posts"
"significantly more than our methodology identifies"
"the size of an instance has a limited impact on the size of a user's social network"
"14.26% of migrated users post at least one toxic post on both the platforms"
"volunteer administrators are responsible for content moderation"
