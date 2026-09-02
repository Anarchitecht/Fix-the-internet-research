## [STEINER-IMC-07] A Global View of KAD

**Citation:** Moritz Steiner, Taoufik En-Najjary, Ernst W. Biersack. "A Global View of KAD." ACM Internet Measurement Conference (IMC), 2007. DOI 10.1145/1298306.1298323.
**Retrieved:** full text via https://www.moritzsteiner.de/papers/KADsteiner.pdf (candidate URL from registry; local file matches title/authors/abstract)
**Source URL:** https://www.moritzsteiner.de/papers/KADsteiner.pdf
**Domain:** A+J

### What it does
The paper measures the deployed population and churn behavior of KAD, a Kademlia-derived distributed hash table (DHT) that forms the publishing and search network inside the eDonkey2000 peer-to-peer file-sharing system. The authors build a crawler, Blizzard, that discovers KAD peers by iterative breadth-first queries starting from several hundred known contacts, logging each peer's crawl timestamp, IP address, and KAD ID (KAD's node identifier). Blizzard runs two independent instances, one at the University of Mannheim and one at Institut Eurecom, to cross-check against crawler crashes or local network loss. Two crawl types are run: a full crawl of the entire KAD identifier space, and a zone crawl restricted to one 256th of the identifier space (all IDs sharing the same 8 high-order bits), which is far cheaper and lets the authors sample at short time intervals. KAD's routing structure follows Kademlia: peers are stored in buckets ordered by XOR distance to the local node, each bucket holding up to 10 contacts, with iterative forwarding to the contact whose ID shares the longest common prefix with the destination. KAD publishes two key types on the 10 peers whose ID matches the key in the first 8 bits (the "tolerance zone"): source keys (hash of file content), republished every 5 hours, and keyword keys (hash of filename tokens), republished every 24 hours.

### Measured results

| Result | Conditions |
|---|---|
| 3 to 4.3 million distinct peers found per full crawl | Full crawl of the entire KAD ID space; peers not behind NAT/firewall (1.5-2 million) are the directly contactable subset used for the rest of the paper's statistics |
| A full crawl completes in about 8 minutes and generates about 3 GB of inbound and outbound traffic each | Single crawler machine, 100 Mbit/s bidirectional bandwidth-limited; first million peers found in ~10 s, second million in ~50 s, after which discovery rate drops sharply |
| Full crawls run 3 times/day, 2006-08-18 to 2006-08-26 and 2006-10-03 to 2006-10-12; one full crawl/day from 2007-03-20 onward | Crawl schedule used for full-crawl statistics |
| Zone crawl of 8-bit zone 0x5b run once every 5 minutes for 179 days (2006-09-23 to 2007-03-21), totaling 51,552 crawls | Basis for essentially all churn and demographic statistics in the paper |
| 12,000 to 20,000 peers observed per 8-bit zone, versus a theoretical maximum of 2^120 addresses per zone | Full crawl; near-uniform distribution across the 256 zones except outlier zones caused by modified clients reusing one KAD ID across >10,000 instances (observed in zone 0xe1) |
| Weekend peer population about 10% higher than weekday | Full crawl population over roughly two weeks, diurnal/weekly pattern |
| Europe (Spain, France, Italy, Germany) is the highest-population continent; China is the single highest-population country; under 15% of peers are in the Americas | Country distribution from Maxmind IP geolocation, full crawl and 8-bit zone crawls, corroborating each other |
| Zone crawl over 179 days: 400,278 distinct KAD IDs, 3,228,890 distinct IP addresses, peers from 168 countries and 2,384 ISPs; 174,318 KAD IDs seen for only a single session; 242,487 KAD IDs with lifetime <= 1 day | 8-bit zone 0x5b, 51,552 crawls over 179 days; more than half of Chinese-origin KAD IDs were seen for only one session |
| Peer arrival/departure counts between consecutive 5-minute crawls follow a Negative Binomial distribution with parameters r=16.81, p=0.127; arrival and departure CDFs are statistically the same | First week of the 179-day zone crawl |
| Approximately 2,000 new KAD IDs per day in the sampled zone, extrapolated to about 500,000 new KAD IDs/day and about 180 million new KAD IDs/year system-wide | Zone crawl, 8-bit zone extrapolated to the full 256-zone ID space; more than 50% of new KAD IDs originate in China, over one order of magnitude more than any other single country |
| Rate of KAD-ID change ("KAD ID aliasing") after one month: about 35% for Chinese-origin peers, about 20% for Spanish-origin peers, about 10% average across all countries | Pivot-set method: peers holding the same IP address and same KAD ID across full crawls of 2007-03-20 and 2007-03-30 (160,641 peers, the "pivot set"), tracked in daily full crawls from 2007-04-01 onward for subsequent KAD ID changes on the same IP |
| Session lengths show a long tail, with sessions as long as 78 days, and are best fit by a Weibull distribution with shape parameter k < 1 | Stated in the conclusion as a summary finding; detailed data referred to the authors' companion technical report, not presented in this paper |

### Parameters
KAD bucket size: 10 contacts. Tolerance zone for key publication: 8 bits (10 peers per key). Source-key republish interval: 5 hours. Keyword-key republish interval: 24 hours. Zone-crawl granularity: 8-bit zone (1/256th of the ID space). Zone-crawl sampling interval: every 5 minutes. Crawler bandwidth: 100 Mbit/s bidirectional (a measurement-infrastructure parameter, not a KAD protocol parameter). Pivot-set qualification window: same IP address and same KAD ID held across a 10-day interval (2007-03-20 to 2007-03-30).

### Stated limitations
The paper states that KAD ID aliasing (peers changing their KAD ID, sometimes every session) makes it impossible to characterize true end-user lifetime from crawl data alone; the measured peer lifetime is only a lower bound on end-user lifetime. The authors state they have no explanation for why end-users change their KAD ID, and state this as an open problem, with a suspicion (explicitly unconfirmed) that Chinese clients run a modified implementation that assigns a new KAD ID per session. The paper reports finding modified KAD clients that reuse a single KAD ID across more than 10,000 simultaneous instances in some zones, which the authors state functions as free-riding because publishing and forwarding load meant for one peer is spread across all instances sharing that ID; they note that if the number of such modified clients grew large enough, the peers sharing an ID would be unable to see or download from one another, degrading application performance for those peers specifically. Detailed per-peer session-length and connected-time-per-day results are stated to exist but were not presented in this paper for space reasons, and the authors refer the reader to a separate technical report (Steiner, En-Najjary, Biersack, "Analyzing Peer Behavior in KAD," Institut Eurecom TR, 2007) for that data.

### Requirements it places on the rest of the system
A crawler-based measurement of a deployed Kademlia-family DHT requires the crawler to hold several hundred initial contacts to bootstrap discovery. Any protocol or client claiming persistent per-peer identity across sessions must be checked against measured behavior rather than assumed, because this paper finds that assumption false for a substantial and geographically concentrated minority of the deployed population (up to 35% KAD-ID churn per month in one country). A system that infers peer lifetime, availability, or reputation from a node identifier must account for identifier churn independent of peer departure, or it will conflate identifier turnover with population turnover. A system relying on tolerance-zone or bucket-based key replication (10 peers per key here) must also handle the same key-holder set being partly composed of NAT/firewalled peers that publish and search but do not store or forward for others, which this paper measures as roughly 50-60% of the observed population (1.5-2 million of 3-4.3 million).

### Contradicts
This paper contradicts the assumption, stated by the authors to be present in all prior KAD publications, that KAD IDs are persistent across sessions; the measured KAD-ID aliasing rate (up to 35%/month for Chinese peers) directly disproves that assumption for the deployed system. No other entry in this batch measures KAD or contradicts this paper's figures. None found among W1-5.

### References worth retrieving
- Maymounkov, Mazières, "Kademlia: A Peer-to-peer Information System Based on the XOR Metric," IPTPS 2002 — foundational (already in corpus per BRIEF.md).
- Stoica, Morris, Karger, Kaashoek, Balakrishnan, "Chord: A Scalable Peer-to-peer Lookup Service for Internet Applications," SIGCOMM 2001 — foundational/competing structured overlay.
- Ratnasamy, Handley, Karp, Shenker, "A Scalable Content-Addressable Network," SIGCOMM 2001 — competing structured overlay.
- Rowstron, Druschel, "Pastry: Scalable, Distributed Object Location and Routing for Large-scale Peer-to-peer Systems," Middleware 2001 — competing structured overlay.
- Stutzbach, Rejaie, "Improving Lookup Performance over a Widely-Deployed DHT," INFOCOM 2006 — competing/related independent measurement of a deployed DHT (describes KAD implementation details cited by this paper).
- Stutzbach, Rejaie, "Understanding Churn in Peer-to-Peer Networks," IMC 2006 — foundational churn-measurement methodology.
- Bhagwan, Savage, Voelker, "Understanding Availability," IPTPS 2003 — foundational availability-measurement methodology.
- Naoumov, Ross, "Exploiting P2P Systems for DDoS Attacks," International Workshop on Peer-to-Peer Information Management, 2006 — attack paper, relevant to KAD/Kademlia-family exposure.
- Kutzner, Fuhrmann, "Measuring Large Overlay Networks — the Overnet Example," KiVS 2005 — competing/prior independent measurement of a Kademlia-derived deployed network (Overnet, KAD's predecessor network).
- Steiner, En-Najjary, Biersack, "Analyzing Peer Behavior in KAD," Institut Eurecom Technical Report, 2007 — same-authors expanded companion report, holds detailed session-length data omitted from this paper.
- Steiner, Biersack, En-Najjary, "Actively Monitoring Peers in KAD," IPTPS 2007 — same-authors follow-up, foundational to later KAD security work.

### Verbatim extracts
- "we observed that this is not the case: There is a large number of peers... that change their kad ID"
- "Each bucket can contain up to ten contacts, in order to cope with peer churn"
- "keys are not published just on a single peer... but on 10 different peers"
- "source keys every 5 hours and, keyword keys every 24 hours"
- "Such a full crawl of kad takes about 8 minutes"
- "we found between 3 and 4.3 million different peers"
- "51,552 crawls were executed" [zone crawl, 179 days]
- "rate of change among the Chinese peers is highest with about 35%"
- "It remains an open problem to explain why kad IDs are non-persistent"
