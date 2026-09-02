## [STUTZBACH-IMC-06] Understanding Churn in Peer-to-Peer Networks
**Citation:** Daniel Stutzbach, Reza Rejaie. "Understanding Churn in Peer-to-Peer Networks." ACM Internet Measurement Conference (IMC), 2006. DOI 10.1145/1177080.1177105.
**Retrieved:** full text via https://dl.acm.org/doi/10.1145/1177080.1177105 (matched: title, authors, and IMC'06 venue line confirmed in first 2500 characters of the file)
**Source URL:** https://dl.acm.org/doi/10.1145/1177080.1177105
**Domain:** A

### What it does
The paper measures how long peers stay connected to a peer-to-peer system (session length) and how that time is distributed, correcting for measurement errors that the paper shows earlier churn studies did not correct for. It defines two correction methods against two biases. The first bias, biased peer selection, arises when a study repeatedly probes a fixed set of peers chosen because they were previously observed, which over-samples peers that return regularly; the paper avoids it for Gnutella and Kad by crawling the entire visible population (Gnutella: full-network snapshots; Kad: every peer in a chosen DHT zone, unbiased because Kad IDs are drawn uniformly at random and are uncorrelated with session length) rather than polling a fixed peer list. The second bias, censored long sessions, arises because any measurement window of finite length τ cannot observe the true length of a session that outlasts the window; the paper's "create-based method" (taken from Saroiu et al.) restricts session-length measurement to sessions that begin in the first half of the window, so every measured session has an equal, unbiased chance of ending within the remaining τ/2, while sessions still running at the window's end are counted (their existence recorded) without their exact length being asserted.

### Measured results

| Result | Conditions |
|---|---|
| Session-length distributions fit a Weibull distribution with shape/scale parameters k=0.34, λ=21.3 (Red Hat); k=0.38, λ=42.4 (Debian); k=0.59, λ=41.9 (FlatOut) | 3 BitTorrent tracker-log datasets: Red Hat (3 months, starting Mar. 21, 2003), Debian (2 months, starting Feb. 22, 2005), FlatOut (2 months, starting Nov. 11, 2004); log-normal fit tried first but overestimated sessions over 1 day for Red Hat and Debian |
| BitTorrent session-length tail index alpha = 2.5 (Red Hat), 2.7 (Debian), 2.1 (FlatOut), all outside the 0<alpha<2 heavy-tailed range | Fit by a line to the log-log transform of the CCDF tail of each of the 3 BitTorrent datasets; the paper concludes BitTorrent session lengths are not heavy-tailed, contrary to prior reports |
| BitTorrent inter-arrival times fit a Weibull distribution with scale parameter k=0.79 (Debian), k=0.53 (Red Hat), k=0.62 (FlatOut), a better fit than exponential | Same 3 BitTorrent datasets; exponential model predicted 9% of inter-arrivals under 10 minutes vs. 33% observed in FlatOut, and predicted 0.38% over 10 hours vs. 1.5% observed |
| Splitting the Red Hat dataset into 1-hour segments, exponential and Weibull distributions each fit in >93% of segments at the p=5% Anderson-Darling test level; splitting Debian into 6-minute segments, only 28% fit exponential and 38% fit Weibull | Red Hat: a few dozen events/segment on average; Debian: a few hundred events/segment (1-hour split) then a few dozen (6-minute split); FlatOut excluded as too sparse to segment meaningfully |
| Roughly 40% (Gnutella), 55% (Kad), 60% (BitTorrent Red Hat/Debian) probability that a randomly selected active peer has been up more than 5 hours; roughly 15% for BitTorrent FlatOut | Uptime-of-coexisting-peers measurement (CCDF, Figure 6) on the 5 Gnutella, 4 Kad, and 3 BitTorrent datasets described below |
| Roughly 10-20% of Gnutella and Kad peers per snapshot, and roughly 1-3% of BitTorrent Red Hat/Debian peers, have uptime exceeding 1 day (Gnutella/Kad) or 2 weeks (BitTorrent) | Same uptime measurement as above |
| Median remaining uptime for Gnutella peers stays between 50% and 100% of elapsed uptime regardless of elapsed value; for Kad, uptime predicts remaining uptime strongly only up to about 4 hours elapsed, after which the median grows only slowly | Figure 7, computed from the 5 Gnutella and 4 Kad datasets |
| In Gnutella, about 50% of peers already up 8 hours stay up at least 8 more hours, but the bottom 20% of that population show much shorter remaining uptime, i.e. high variance around the median predictor | Figure 8, one representative trace per system (Gnutella 1, Kad 1, BitTorrent Red Hat), conditioned on already-observed uptime of 1, 2, and 8 hours |
| Consecutive session lengths of the same peer are strongly correlated in Gnutella (by IP address) and Kad (by node ID); BitTorrent shows no such correlation | Section 6.2, all 5 Gnutella, 4 Kad, and 3 BitTorrent datasets, pairing each peer's session i with session i+1 |
| Peer availability across two consecutive days is strongly correlated in Gnutella and Kad; BitTorrent shows no such correlation except that a peer up the full 24 hours on day 1 tends to stay up the full 24 hours on day 2 | Each 2-day dataset split into two 1-day windows (Gnutella, Kad); consecutive day-pairs used for the longer BitTorrent logs |
| More than half of peers in both systems studied for this metric appear only once per day; a small number appear up to 60 times per day | Figure 12, appearances-per-day distribution across the Gnutella, Kad, and BitTorrent datasets |
| 22% (Red Hat), 70% (Debian), 27% (FlatOut) of BitTorrent tracker-log sessions ended ungracefully and were excluded from session-length analysis | Measured directly from the 3 BitTorrent tracker logs |
| The Red Hat tracker log contains 5 unexplained multi-minute-to-8-hour gaps, Debian 2, FlatOut 1; shortest gap 20 minutes, longest 8 hours, all other inter-event gaps under 4 minutes | Direct inspection of the 3 BitTorrent tracker logs' event timestamps |

Datasets: Gnutella, 5 sets of full-network crawls, each a 48-hour period of back-to-back snapshots at roughly 7-minute intervals, collected Oct.-Dec. 2004, using the Cruiser crawler. Kad, 4 datasets, each a 48-hour crawl of one DHT zone (zone sizes given as ID-prefix masks, e.g. 0x594/10), collected Apr. 2005, using Cruiser's Kad module. BitTorrent, 3 tracker logs: Red Hat (3 months, Mar. 2003), Debian (2 months, Feb. 2005), FlatOut game demo (2 months, Nov. 2004).

### Parameters
- Measurement-window split point: session-length measurement restricted to sessions beginning in the first half of each measurement window (the create-based method), giving unbiased measurement for session lengths up to τ/2.
- Weibull shape/scale parameters fit per dataset (BitTorrent session length): Red Hat k=0.34, λ=21.3; Debian k=0.38, λ=42.4; FlatOut k=0.59, λ=41.9.
- Weibull scale parameter fit per dataset (BitTorrent inter-arrival time): Debian k=0.79; Red Hat k=0.53; FlatOut k=0.62.
- Heavy-tail index alpha fit per dataset (BitTorrent session length): Red Hat 2.5, Debian 2.7, FlatOut 2.1.
- Anderson-Darling goodness-of-fit significance level: p=5%.
- Gnutella crawl interval: approximately 7 minutes; measurement window: 48 hours (5 datasets).
- Kad measurement window: 48 hours per zone (4 zones/datasets), one zone specified as an ID prefix and mask (e.g. 0x594/10).

### Stated limitations
The paper states it cannot make unbiased measurements of any session length longer than half the measurement window (τ/2); it can only record that such a session existed and continued past the window's end, not its exact length. It states the Debian uptime distribution is skewed by a large population of long-lived seed peers operated by the Debian organization itself, so that dataset's uptime results are not treated as representative of ordinary peer behavior. It states that whether the slight downward curvature seen in the Gnutella and Kad session-length CCDFs reflects a true non-heavy-tailed distribution or is a measurement artifact from under-counting long sessions cannot be ruled out with the data collected. It states it has not addressed how peer behavior correlates with time of day, geographical location, or file preference, and leaves that to future work. It states it is still developing heuristics to distinguish a peer missed during one crawl snapshot from a peer that genuinely departed, and that this affects the precision of long-lived-peer characterization.

### Requirements it places on the rest of the system
A component that assumes session lengths are exponentially or Poisson-distributed, to derive a churn rate or a routing-table refresh interval, is contradicted by this paper's fitted Weibull/log-normal distributions across all three systems measured; substituting the measured distribution requires re-deriving any such rate from the corresponding shape/scale parameters above rather than from a single mean. A protocol that selects "stable" peers by uptime observed so far can rely on the reported correlation between current uptime and remaining uptime only in Gnutella (strong at all uptime values) and in Kad up to about 4 hours of observed uptime; past that point in Kad, and throughout BitTorrent's non-seed sessions, uptime so far is a weak predictor and a protocol needs a different signal. A bootstrap or peer-discovery mechanism that caches long-lived peers can rely on the paper's stated 20-30% of peers having uptime exceeding one day at any snapshot moment, but only under the same peer-selection method the paper used (uniform-random selection among currently active peers, or observation-count weighting), because naive periodic sampling of a fixed peer set is shown to bias toward short-lived peers.

### Contradicts
The paper's own Section 6.1 states that Guo et al. (Internet Measurement Conference, 2005) characterized BitTorrent downtime ("sleeping time") as exponentially distributed, and states this conclusion may be an artifact of incorrectly handling long sessions rather than a true property of the distribution. The paper also states that Guo et al.'s finding of an exponential lingering-time ("seeding time") distribution is inconsistent with the curvature the paper itself observes and states the data is better modeled by a Weibull distribution. None found against any other entry in this batch.

### References worth retrieving
- Saroiu, Gummadi, Gribble, "Measuring and Analyzing the Characteristics of Napster and Gnutella Hosts," Multimedia Systems Journal 9(2), 2003 — foundational (source of the create-based method this paper extends)
- Gummadi, Dunn, Saroiu, Gribble, Levy, Zahorjan, "Measurement, Modeling, and Analysis of a Peer-to-Peer File-Sharing Workload," SOSP 2003 — competing (independent session-length measurement the paper contrasts its own median/heavy-tail findings against)
- Guo, Chen, Xiao, Tan, Ding, Zhang, "Measurements, Analysis, and Modeling of BitTorrent-like Systems," IMC 2005 — competing (the paper disputes its exponential downtime/lingering-time conclusions)
- Bhagwan, Savage, Voelker, "Understanding Availability," IPTPS 2003 — competing (studies cross-peer availability correlation, stated as complementary to this paper's single-peer-across-time correlation result)
- Rhea, Geels, Kubiatowicz, "Handling Churn in a DHT," USENIX 2004 — competing (a churn-resilience mechanism whose assumed churn model this paper's measurements can validate or contradict)
- Li, Stribling, Kaashoek, Morris, Gil, "A Performance vs. Cost Framework for Evaluating DHT Design Tradeoffs under Churn," INFOCOM 2005 — foundational (DHT churn-cost tradeoff analysis this measurement paper's distribution feeds)
- Stutzbach, Rejaie, Sen, "Characterizing Unstructured Overlay Topologies in Modern P2P File-Sharing Systems," IMC 2005 — foundational (same authors' prior topology-bias finding this paper cites for the crawl-degree correlation)
- Maymounkov, Mazières, "Kademlia: A Peer-to-Peer Information System Based on the XOR Metric," IPTPS 2002 — foundational (defines the Kad-derived DHT this paper measures)
- Liang, Kumar, Ross, "The KaZaA Overlay: A Measurement Study," Computer Networks Journal, 2005 — competing (independent P2P measurement using the closed-population probing method this paper argues is biased)

### Verbatim extracts
"reported median session lengths varies from one minute to one hour"
"we must conclude that session lengths in BitTorrent are not heavy-tailed"
"the session length distribution is neither Poisson nor Pareto"
"roughly 10%-20% of peers per snapshot in Gnutella and Kad have an uptime longer than one day"
"the uptime of Kad peers is a stronger predictor of remaining uptime up to around 4 hours"
"session lengths in BitTorrent do not exhibit a clear correlation"
"20%-30% of peers at any moment have an uptime longer than one day"
