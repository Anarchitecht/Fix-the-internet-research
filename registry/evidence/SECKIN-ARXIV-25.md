## [SECKIN-ARXIV-25] The Rise of Bluesky

**Citation:** Ozgur Can Seckin, Filipi Nascimento Silva, Bao Tran Truong, Sangyeon Kim, Fan Huang, Nick Liu, Alessandro Flammini, Filippo Menczer. "The Rise of Bluesky." arXiv preprint, 2025. arXiv:2504.12902.
**Retrieved:** full text via https://arxiv.org/abs/2504.12902
**Source URL:** https://arxiv.org/abs/2504.12902
**Domain:** J

Note on match: the registry record lists seven authors (Seckin, Silva, Truong, Kim, Huang, Flammini, Menczer); the retrieved arXiv v1 text lists an eighth author, Nick Liu, between Huang and Flammini. Title, remaining seven author names, venue, and institutional affiliation (Observatory on Social Media, Indiana University) all match the registry record; treated as the same paper with an updated author list.

### What it does
The paper measures how Bluesky (a microblogging platform structurally similar to Twitter/X but built with decentralized governance and user-controlled data) grew from August 2023 to February 2025, and tests whether growth driven by discrete migration events from other platforms settled into a stable, self-sustaining user base rather than the sign-up-and-abandon pattern common to new social platforms. The authors assign every account to one of four groups based on which of four public migration-triggering events preceded its signup — the February 6, 2024 switch from invitation-only to open public access; the August 30, 2024 blocking of X in Brazil; the October 16, 2024 X policy change letting blocked users still see the blocking account's posts; and the November 4, 2024 US Presidential election — plus a residual group for accounts joining outside those windows. For each group they track daily post/repost/reply/like activity, and separately reconstruct a directed follower network from observed follow actions (singleton accounts with no follower and no followee excluded) to compute, as the network grows, average out-degree, clustering coefficient (the tendency of two users sharing a mutual connection to also be connected to each other), giant-component size, and two measures of in-degree inequality: the Gini index (0 to 1, higher meaning followers are concentrated on fewer accounts) and the Kappa index (kappa = <k^2>/<k^2>, the second moment of in-degree divided by the squared mean in-degree, with values above 1 indicating hub-driven fluctuation in the distribution). Growth is analyzed along "network time," meaning quantities are plotted against the cumulative number of users at each point rather than against calendar time, to align the comparison across events that occurred at different absolute user-count scales.

### Measured results

| Quantity | Value | Conditions |
|---|---|---|
| Total accounts | 30 million | End of January 2025 |
| Users with at least one friend or follower, used for network-time panels (d-i) | 26 million | Snapshot as of 7 February 2025; the paper notes user counts can occasionally decrease due to account deletion or suspension |
| New accounts after Brazil's August 30, 2024 X ban | nearly 500,000, majority Portuguese-language | Measured shortly after the ban date |
| Daily active user share at steady state | approximately 15% of all existing accounts (implying approximately 85% inactive/lurking) | Measured after the November 4, 2024 US election event, once activity reached a steady state |
| Average per-user daily activity at steady state | stabilized above 10 actions per day | Same post-election steady-state period |
| Giant-component (largest connected component) size | approximately 70-80% of all users | Emerged before the February 2024 public-access opening and remained fairly stable in relative size through the full measurement window; exact network size at each measurement point not given in the retrieved text (stated as "not shown") |
| Clustering coefficient | orders of magnitude higher than an equivalent random network with the same node and edge count | Measured on the undirected version of the follower network, across the full growth period plotted in network time |
| Gini and Kappa index trend | both indices show strong growth during the post-election user influx | Measured on the in-degree (follower-count) distribution across network time |

The paper's figures (average out-degree, average activity per active user, active-user count, Gini index, Kappa index, clustering coefficient) are plotted continuously against network size rather than reported as discrete before/after values with stated conditions; the retrieved text gives no numeric axis values for these curves beyond the ranges visible in the figure descriptions (out-degree axis to 80, clustering-coefficient axis 0.10-0.20, Gini axis 0.65-0.90, activity-per-user axis 0-17.5), so no specific measured number from these curves is recorded here beyond the discrete figures stated above.

### Parameters
No explicit collection parameters (API used, sampling rate, crawl frequency) are stated in the retrieved text beyond a reference to code and data being available at a GitHub repository and a Zenodo record; the retrieved text does not itself describe the data-collection method (e.g., which Bluesky API or firehose feed was polled, or at what interval). The follower-network visualization in Figure 1c uses a stated 1% sample of users; all other network statistics (giant component, clustering coefficient, Gini, Kappa) are computed on the full reconstructed follower graph after excluding singleton nodes.

### Stated limitations
The retrieved text states no explicit limitations or future-work section; the Discussion section states an expectation, not a measured finding, that as Bluesky reaches mainstream adoption it will attract "bad actors and harmful content," and calls for future research on abuse and manipulation without presenting any such measurement itself. The paper does not report the actual network size (user count) at which the giant-component measurements were made, describing the connectivity analysis as "not shown" in the retrieved figure. The paper draws its four-group event attribution from account creation timing alone, which the paper does not validate against explicit self-reported migration reasons or platform-of-origin data for individual accounts.

### Requirements it places on the rest of the system
None stated as a mechanism requirement — this is a measurement study of an existing deployed system's growth and network structure, not a description of a mechanism another component could implement or depend on. Any citation of the giant-component or clustering-coefficient figures elsewhere in this corpus should be scoped to a federated/decentralized microblogging platform with open follow-graph data and a burst-driven, migration-event-triggered growth pattern, since the paper's own event-group framing is specific to Bluesky's observed 2024 migration waves.

### Contradicts
None found.

### References worth retrieving
- David Easley, Jon Kleinberg, "Network effects," in Networks, Crowds, and Markets: Reasoning about a Highly Connected World, 2010, pp. 509-542 — foundational (network-effect framing the paper's stability question rests on).
- Wei Gong, Ee-Peng Lim, Feida Zhu, "Characterizing silent users in social media communities," Proceedings of the International AAAI Conference on Web and Social Media, vol. 9, 2015, pp. 140-149 — foundational (the lurker-population comparison the paper's 85%-inactive figure is checked against).
- Alessia Antelmi, Delfina Malandrino, Vittorio Scarano, "Characterizing the behavioral evolution of twitter users and the truth behind the 90-9-1 rule," Companion Proceedings of the 2019 World Wide Web Conference, 2019, pp. 1035-1038 — foundational (the comparable lurker-ratio finding on Twitter, cited alongside the Bluesky figure).
- Lilian Weng, Filippo Menczer, Yong-Yeol Ahn, "Virality prediction and community structure in social networks," Scientific Reports 3(1), 2013 — foundational (the clustering-coefficient-and-virality mechanism the paper's clustering result is interpreted through).
- Wentao Han, Xiaowei Zhu, Ziyan Zhu, Wenguang Chen, Weimin Zheng, Jianguo Lu, "A comparative analysis on weibo and twitter," Tsinghua Science and Technology 21(1), 2016, pp. 1-16 — competing (the independent Gini/Kappa hub-concentration measurement on Weibo and Twitter the paper's own indices are compared against).

### Verbatim extracts
- "reaching 30 million accounts at the end of January 2025"
- "around 85% users are silent, also known as lurkers"
- "A giant component consisting of around 70-80% of all users emerged even before public access"
- "The clustering coefficient is orders of magnitude higher than that of an equivalent random network"
- "Both indices display a strong growth in the post-election surge"
