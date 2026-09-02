## [BONO-WEBSCI-24] An Exploration of Decentralized Moderation on Mastodon
**Citation:** Carlo Bono, Lucio La Cava, Luca Luceri, Francesco Pierri. "An Exploration of Decentralized Moderation on Mastodon." ACM Web Science Conference (WebSci), 2024. Pages 53-58. DOI 10.1145/3614419.3644016.
**Retrieved:** full text
**Source URL:** target record (registry/targets-deduped.json)
**Domain:** K

### What it does
The paper characterizes instance-level blocklisting on Mastodon: an administrator-issued action, exposed since Mastodon v4.0.0 (November 2022) through the public GET /api/v1/instance/domain_blocks endpoint, that lists which remote instances a given instance has silenced or fully banned along with a free-text motivation string. The authors crawl this endpoint daily for active instances discovered through the instances.social aggregator, over about 16,000 indexed instances, and analyze which instances get banned most, what motivations administrators state, how blocklisting activity is geographically distributed, and how similar different instances' blocklists are to each other, using Jaccard distance and agglomerative clustering plus a directed ban-graph.

### Measured results
| Metric | Value | Conditions |
|---|---|---|
| Instance discovery source and scale | instances.social aggregator, approximately 16,000 indexed instances | Static reference count of the aggregator's coverage, not the crawled sample |
| Active instances crawled | Approximately 1,000 per day | Daily crawl, July 6 to November 15, 2023 (about 4.5 months); an instance is counted only if online at crawl time and supporting Mastodon API v2 |
| Monthly active user distribution across instances | Power-law-like distribution (no fitted exponent stated) | Same crawl period, drawn from GET /api/v1/instance/activity |
| Most-banned instance | pawoo.net, described as the second-largest Mastodon instance | Cumulative ban count over the July-November 2023 observation window |
| Average in-degree in the instance-to-instance ban graph (received bans) | 3 to 4 | Directed graph G=(V,E) where V is all instances that ban or are banned, and an edge (i,j) exists if instance i lists instance j in its blocklist; computed over the full observation window |
| Ban-graph connectivity change | One connected component in July 2023; splits into at least two connected components from August 2023 onward | Same directed ban graph, tracked monthly |
| Most-banned domains by subdomain count (spam-campaign indicator) | activitypub-troll.cf ranked highest, followed by ngrok.io and masto.host (and hostdon.ne.jp) | Subdomains under the same parent domain collapsed to one count (e.g., XYZ.activitypub-troll.cf and XZY.activitypub-troll.cf both counted under activitypub-troll.cf) |
| Ban-motivation keyword analysis | Most frequent lemma in ban motivations relates to NSFW content, including a high frequency of the term "pen*s"; other frequent terms include references to a censorship-free platform, "hate," "speech," "harassment," "transphobia," "federate," and "fedi" | Lemmatized free-text motivation field from domain_blocks entries, same crawl |
| Geographic distribution of banned instances (raw count) | Highest in the United States, followed by France and Germany | Same crawl period |
| Geographic distribution of banned instances (normalized by total instances per country) | Northern Europe and Russia show the highest fraction of banned instances | Same data, normalized by per-country instance count, values reported in log10 scale |
| Pairwise blocklist similarity (Jaccard distance over sets of banned domains, agglomerative clustering) | Most instance pairs cluster near distance 1 (highly dissimilar blocklists); a smaller number of instances form tight clusters (near-identical blocklists) | Full pairwise matrix over crawled instances with domain_blocks data available |

### Parameters
- Crawl window: July 6, 2023 to November 15, 2023, daily.
- Instance discovery: instances.social aggregator, restricted to instances that are online at crawl time and support Mastodon API v2 (domain_blocks endpoint requires Mastodon v4.0.0 or later, released November 2022).
- Obfuscated-domain matching: instances that partially mask a moderated instance's domain (e.g., "m**todon.example") are de-obfuscated by matching against known domains in the dataset only when the match is unique.
- Similarity method: Jaccard distance over per-instance sets of banned domains, followed by agglomerative clustering.

### Stated limitations
The paper is stated as "a first exploration," acknowledging no prior work had studied Mastodon instance-level blocklisting dynamics before this study. Obfuscated blocklist entries (instances that partially mask which domain they banned) are only recoverable when the partial string uniquely matches one known domain in the dataset, so some ban targets remain unresolved. The geographic country-level counts are stated to give "only rough indications," given the large and uneven proliferation of instances across countries. The authors state as future work an investigation of the broader effects of decentralized moderation tools, specifically segregation, toxicity, and transitivity, none of which this paper measures. The paper identifies but explicitly declines to adjudicate the risk of blocklist misuse ("abuse of ban lists to harm or destabilize the Fediverse"), stating this risk is "left to the common sense" of administrators and volunteers rather than measured.

### Requirements it places on the rest of the system
The measurement method requires each instance to expose its blocklist and ban motivations through the public domain_blocks API endpoint; the authors state some instances explicitly obfuscate the domain of a moderated instance, which is a participant-controlled opt-out from full transparency that the measurement can only partially work around. The similarity and clustering analysis requires the same endpoint to be queryable across many instances simultaneously to build a directed graph over shared moderation targets; an instance that does not expose domain_blocks (pre-v4.0.0, or one that hides the endpoint) is invisible to this method both as a source and, if never named uniquely, as a target. The finding that blocklists are frequently near-identical for a subset of instances is attributed by the authors to publicly shared blocklist curation (they cite the existence of a public blocklist repository), meaning the observed clustering reflects import of a shared external list rather than independent per-administrator judgment for at least some instances; the paper does not measure what fraction of ban decisions originate this way.

### Contradicts
None found.

### References worth retrieving
- Anaobi, Raman, Castro, Zia, Ibosiola, Tyson. "Will Admins Cope? Decentralized Moderation in the Fediverse." WWW 2023. — already in this corpus (ANAOBI-WWW-23), cited directly as reference [1].
- Nicholson, Keegan, Fiesler. "Mastodon Rules: Characterizing Formal Rules on Popular Mastodon Instances." CSCW '23 Companion, 2023. — competing (measures declared instance rules rather than enforced blocklists; direct comparison point the paper itself makes, contrasting with Reddit's content moderation).
- Raman, Joglekar, De Cristofaro, Sastry, Tyson. "Challenges in the Decentralised Web: The Mastodon Case." ACM Internet Measurement Conference (IMC), 2019. — foundational (earlier large-scale Mastodon infrastructure measurement).
- Zannettou, Bradlyn, De Cristofaro, Kwak, Sirivianos, Stringini, Blackburn. "What is Gab: A Bastion of Free Speech or an Alt-Right Echo Chamber." WWW 2018 Companion. — foundational (independent characterization of gab.com, one of this paper's top-banned instances, cited directly).
- La Cava, Mandaglio, Tagarelli. "Polarization in Decentralized Online Social Networks." WebSci 2024. — foundational (same venue and year, related-work companion on DOSN structural dynamics).
- Zignani, Gaito, Rossi. "Follow the 'Mastodon': Structure and Evolution of a Decentralized Online Social Network." ICWSM 2018. — foundational (Mastodon structural measurement, cited directly).
- Zia, He, Raman, Castro, Sastry, Tyson content referenced as toxic-content-in-Pleroma study by same author group as ANAOBI-WWW-23 (referred to in text as "Zia et al. [2]"). — competing (independent Pleroma toxicity-spread measurement).

### Verbatim extracts
- "instances.social ... currently covering about 16K instances"
- "the average in-degree of Mastodon instances, i.e., the number of received bans, ranges between 3 and 4"
- "most instances yielding pairwise distances close to one ... signaling very diverse blocklists"
- "starting from August we spotted the division of the network in at least two connected components"
