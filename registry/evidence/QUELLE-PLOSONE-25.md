## [QUELLE-PLOSONE-25] Bluesky: Network topology, polarization, and algorithmic curation
**Citation:** Dorian Quelle, Alexandre Bovet. "Bluesky: Network topology, polarization, and algorithmic curation." PLOS ONE, 2025. DOI 10.1371/journal.pone.0318034.
**Retrieved:** full text via https://arxiv.org/abs/2405.17571
**Source URL:** https://doi.org/10.1371/journal.pone.0318034
**Domain:** K

### What it does
The paper measures the deployed Bluesky network — a decentralized microblogging system built on the
AT Protocol — using complete user repository data pulled directly from the network rather than a
platform-supplied API export. Because Bluesky is decentralized, any party holding a user's decentralized
identifier (DID) can retrieve that user's repository: the authors first queried the centralized DID PLC
directory (a lookup service mapping each DID to the network address of that user's personal data server,
PDS) to resolve each user's PDS address, then queried that PDS directly for the user's repository
contents (posts, likes, reposts, follows, blocks, feed creations). Starting from a seed list of 5.28
million user IDs posted publicly by a Bluesky contributor in March 2024, they recursively expanded the
dataset by extracting data for every user referenced within already-downloaded data, repeating until no
new users were found, and stored the result in a relational database with one table per interaction type.

The paper characterizes four interaction layers, each treated as a distinct directed graph on the same
user set: Followership (persistent, edge exists until explicitly removed, does not by itself indicate
agreement), Replies (non-persistent, edge per reply within a thread), Reposts (non-persistent, equivalent
to a Twitter retweet, indicates willingness to redistribute content to one's own followers), and Likes
(non-persistent, indicates topical interest but does not itself redistribute content to followers). It
separately measures Bluesky's user-generated "custom feed" mechanism, in which any user can publish a
feed generator ranging from simple keyword/regex matching to machine-learning-based ranking, which other
users can then subscribe to or like; a feed's rank in Bluesky's own feed-discovery surface is driven by
its like count, which the paper measures as a proxy for adoption.

### Measured results

| Finding | Figure | Conditions |
|---|---|---|
| Users covered by the complete-repository dataset | 5,000,000 (from a 5.28 million-ID seed list) | Recursive repository crawl via DID PLC directory + per-user PDS queries, Feb 2023-May 2024 |
| Custom feeds created | 39,639 | Same dataset, by 18,352 distinct active users who created at least one feed |
| Users who liked at least one custom feed | 139,033 of 5,000,000 (~2.8%) | Same dataset; these users liked feeds a combined 295,902 times |
| Mean likes received per feed | 2.128 (σ=5.932, max 1,799) | Distribution over all 39,639 feeds (Table 3) |
| Mean feeds created per feed-creating user | 2.161 (σ=13.931, max 1,828) | Distribution over the 18,352 feed-creating users (Table 3) |
| Mean feeds liked per feed-liking user | 14.783 (σ=156.641, max 16,132) | Distribution over the 139,033 feed-liking users (Table 3) |
| Total interaction-table row counts | Follows 149,650,293 / Posts 206,346,303 / Likes 771,009,280 / Reposts 81,655,778 / Blocks 8,357,905 / Feeds 39,639 | Full dataset, Feb 2023-May 2024 (Table 5) |
| Unique users per interaction type | Follows 3,844,491 / Posts 2,339,109 / Likes 2,581,744 / Reposts 1,197,330 / Blocks 479,427 / Feeds 18,352 | Same dataset (Table 5) |
| Peak weekly active users per layer, pre-public-opening | Followership 700,000 / Replies+Reposts 300,000 each / Likes 600,000 | Weekly counts, peak reached September 2023 |
| Peak weekly active users per layer, after Feb 2024 public opening | Followership 2,000,000 / Replies 450,000 / Reposts 550,000 / Likes 1,300,000 | Record highs following Bluesky's February 7, 2024 open registration |
| Normalized clustering-coefficient peaks (vs. degree-matched random graph, ratio 1.0 = parity) | Followership 10 / Reposts 10 / Likes 16 / Replies 200 | Peak values reached around September 2023, all four networks exhibit "more cliquish than random" structure throughout |
| Top-10 most-shared news domains' political-bias rating | 8 of 10 rated "left-center" by Media Bias/Fact Check; the other 2 rated "center" | Domain-frequency analysis of hyperlinks shared in the full post dataset |
| Israel-Palestine-conflict post volume in labeled subset | 1.3 million posts (from n-gram query over the full post table) | Query built from mutual-information-ranked n-grams across 28 languages present in the dataset, manually reviewed |
| Stance shift on Israel-Palestine conflict, month before vs. after Oct 7, 2023 | Neutral posts 82.86% -> 37.98%; Oct 2023: pro-Israel 33.01% vs pro-Palestine 28.99%; final observed month: pro-Israel 20.74% vs pro-Palestine 39.00% | Daily post-stance classification (1,000 posts manually labeled by authors, 1,000 more labeled by Appen.com crowdworkers, used to train/validate the classifier applied to the 1.3 million-post subset) |

### Parameters
| Parameter | Value used |
|---|---|
| Seed user-ID list size | 5.28 million (posted publicly by a Bluesky contributor, March 26, 2024) |
| Final analyzed user count | 5,000,000 |
| Repository resolution path | DID -> DID PLC directory -> PDS network address -> per-user repository query |
| Crawl expansion rule | recursive: any user referenced in already-downloaded data is added and queried, repeated to fixed point |
| Observation window | February 2023 (platform launch) to May 20, 2024 |
| Stance-classification training data | 1,000 posts labeled by the authors + 1,000 labeled by Appen.com crowdworkers, drawn from the 1.3 million-post Israel-Palestine subset |
| Political-domain bias source | Media Bias/Fact Check (MBFC) ratings |
| Clustering-coefficient normalization | ratio against a configuration-model random graph with the same per-node degree sequence |

### Stated limitations
The paper carries no section titled "Limitations." In the Discussion, the authors state that only a
small minority of users have liked a feed despite the availability of almost 40,000 feeds, describing
feed-mechanism adoption as limited relative to the platform's user base. They state that Bluesky's
predominantly left-leaning political composition does not imply uniformity of opinion on every issue,
evidenced by the measured Israel-Palestine stance split, and state as an open question for future work
whether issue-specific polarization on the platform reflects healthy debate or the same affective
polarization and political sectarianism documented on Twitter and Facebook, without resolving that
question themselves. They note the Followership network shows the steepest post-opening activity
decline, which they attribute to new users following platform-suggested profiles without further
engagement, stated as an interpretation rather than a directly measured cause.

### Requirements it places on the rest of the system
The measurement method itself depends on two properties of the AT Protocol's decentralization design:
a centralized DID-to-PDS directory (DID PLC) must be queryable to resolve any user's data-hosting
location, and each user's personal data server must serve that user's repository to any requester who
holds the user's DID, with no access control gating repository reads. Both properties are what make the
"complete repository" crawl possible without the platform operator's cooperation; a design that added
per-repository read authorization would break this measurement method as constructed. The custom-feed
mechanism requires no coordination beyond each feed generator computing its own ranking (by whatever
method its creator chooses) and users individually subscribing or liking; feed adoption as measured here
is a pure demand-side signal — the paper found no server-side promotion in this dataset was analyzed as
an amplification factor, since Table 3 measures like counts directly rather than any impression
metric. The measured near-power-law degree distributions (Table 1) and above-baseline clustering
coefficients across all four interaction layers place a requirement on any component whose performance
assumes uniform user degree or Erdos-Renyi-like structure: such assumptions do not hold for Bluesky's
observed graph, at any of the four interaction-layer definitions used here.

### Contradicts
None found within this corpus.

### References worth retrieving
- **Kleppmann, Frazee, Gold, Graber, Holmgren, Ivy et al., "Bluesky and the AT Protocol: Usable Decentralized Social Media"** — foundational protocol description, cited [1]; describes the feed-generator "marketplace of algorithms" design this paper measures adoption of.
- **Failla, Rossetti, "'I'm in the Bluesky Tonight': Insights from a Year Worth of Social Data," arXiv** — competing independent measurement of the same platform, cited [6]; comparison numbers on Bluesky's network structure from a separate dataset.
- **Zignani, Gaito, Rossi, "Follow the 'mastodon': Structure and evolution of a decentralized online social network"** — competing measurement of the sibling Fediverse platform, cited [7]; already flagged from LIU-PACMHCI-25 and POLINSKI-CCR-24.
- **Aliapoulios, Bevensee, Blackburn, Bradlyn, De Cristofaro, Stringhini et al., "An early look at the Parler..."** — competing measurement of an alternative decentralized-adjacent social platform, cited [8].
- **Jeong, Jiang, Tan, Bernard, Liu, "BlueTempNet: A Temporal Multi-network Dataset of Social..."** — foundational, a competing/companion dataset paper on Bluesky, cited [28].
- **Cinelli, De Francisci Morales, Galeazzi, Quattrociocchi, Starnini, "The echo chamber effect on social media"** — foundational for the polarization-measurement methodology, cited [42].
- **Gehl, Zulli, "The digital covenant: non-centralized platform governance on the mastodon social network"** — foundational/competing governance study of the sibling Fediverse platform, cited [34].

### Verbatim extracts
"only 139 thousand out of 5 million users liked at least one feed" (line 622).
"In total, 39,639 feeds have been created by 18,352 active users" (line 436).
"the feature's overall adoption appears limited relative to Bluesky's total user base" (lines 66-67).
"the complete repositories of five million users on Bluesky" (Materials and Methods).
"All but two of the top ten most spread political domains have an associated rating of left-center" (lines 700-701).
"the normalized clustering coefficient remains above one" (line 288).
