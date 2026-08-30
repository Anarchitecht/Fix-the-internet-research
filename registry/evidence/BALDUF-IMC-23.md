## [BALDUF-IMC-23] The Cloud Strikes Back: Investigating the Decentralization of IPFS
**Citation:** Leonhard Balduf, Maciej Korczyński, Onur Ascigil, Navin V. Keizer, George Pavlou, Björn Scheuermann, Michał Król. "The Cloud Strikes Back: Investigating the Decentralization of IPFS." ACM Internet Measurement Conference (IMC), 2023. DOI 10.1145/3618257.3624797.
**Retrieved:** full text via https://arxiv.org/abs/2309.16203
**Source URL:** https://arxiv.org/abs/2309.16203
**Domain:** A

### What it does
The paper measures how much of a deployed content-addressed peer-to-peer file system, IPFS (InterPlanetary File System), runs on cloud infrastructure rather than on volunteer-operated machines. It does not propose a mechanism; it instruments four channels of the running IPFS network and reports the fraction of each channel that terminates on nodes hosted by a small number of commercial cloud providers. The four channels: the Kademlia distributed hash table (DHT) topology (who is a DHT server and where they are hosted), Bitswap and DHT message traffic (who generates and receives requests), content provider records (who hosts retrievable content), and entry points (HTTP gateways, DNSLink, and Ethereum Name Service (ENS) records that map human-readable names to content identifiers).

The authors crawl the DHT by sending crafted FindNode messages that sweep the address space, enumerating every node's k-buckets (its outbound DHT connections) to reconstruct a snapshot of the DHT graph. They separately capture Bitswap request traffic through a modified Go-IPFS node with an unbounded connection count that logs all incoming local-broadcast traffic, and DHT traffic through a modified Hydra-Booster (a Protocol-Labs-operated DHT accelerator) running 20 virtual peer IDs. They classify every observed IP address as cloud-hosted or not using the Udger IP-to-provider database, and geolocate every address using the MaxMind GeoLite2 database.

### Measured results
| Metric | Figure | Conditions |
|---|---|---|
| DHT servers hosted in the cloud | 79.6% (20,300 of 25,510 average crawled nodes); non-cloud 18.6% (4,737) | Average-over-crawls, unique-nodes (A-N) counting method; 101 crawls, 2023-04-18 to 2023-05-26, twice daily |
| Same metric, alternative counting method | 39.9% cloud (34,375 addresses), 60.1% non-cloud (51,689) | Global-unique-IP (G-IP) counting method, matching the method of a prior 2022 study (Trautwein et al.); same crawl dataset |
| Top-3 cloud-provider share of DHT servers | 51.9% of nodes; single largest provider (Choopa) 29.3% (7,492 nodes) | A-N method, same crawl dataset |
| DHT peer-ID traffic centralization | Top 5% of peer IDs generate ~97% of DHT+Bitswap traffic | 290M messages total from Hydra-Booster (DHT) and Bitswap-monitor logs, August 2022–May 2023 |
| DHT IP traffic centralization | Top 5% of IPs generate ~94% of messages; cloud nodes alone generate ~85% of DHT traffic vs. ~15% for non-cloud | Same traffic logs; DHT vs. Bitswap broken out separately, Bitswap cloud share ~42% |
| Cloud share of raw IP population in traffic logs | 35% overall (lower than the 79% crawl figure because traffic logs include NAT-ed clients invisible to DHT crawls) | Same traffic logs |
| Cloud share of traffic volume by IP | ~93% overall, ~98% for download-related traffic; Amazon AWS alone 68%, AWS+Packet jointly 82% | Same traffic logs |
| Hydra-Booster (Protocol-Labs-operated) share of DHT traffic | 35% of all DHT traffic, 50% of download-specific DHT traffic, ~0% of advertisement traffic | Same traffic logs |
| Content providers by hosting class | NAT-ed 35.57%, cloud-based 45%, non-cloud (public IP) 18%, hybrid 0.58% | 5.6 million content identifiers (CIDs), provider records collected over 28 days, reachability-verified |
| Provider popularity concentration | ~1% of peers appear as providers in ~90% of provider records; of those, ~70% are cloud-based, NAT-ed peers appear in <8% | Same 5.6M-CID provider-record dataset |
| Content dependency on cloud | 95% of content has at least one cloud-based provider; for 91% of content, at least half its providers are cloud-based; 23% of content is served only by cloud-based peers; conversely 77% of content identifiers have at least one non-cloud provider | Same dataset |
| NAT-ed provider relay dependency | ~80% of NAT-ed providers use a cloud-hosted node as their circuit-relay | Same dataset |
| DNSLink gateway hosting | Only 20% of gateway IPs referenced by DNSLink records are non-cloud; 50% of gateway IPs are hosted by Cloudflare alone | One month of passive DNS data from SIE Europe, March 2023 |
| ENS-referenced content hosting | 82% of content referenced by Ethereum Name Service (ENS) records is hosted on cloud nodes; 60% of that content's providers are located in the US or Germany | 20.6k setContenthash() event-log records extracted via the Etherscan API from 16 known resolver contracts, of which 16.8k resolved to provider records and 9k to unique IPs |
| Node-removal resilience (random) | Largest connected component retains 96% of remaining nodes after removing 90% of nodes at random | One crawl snapshot, 2023-05-12, 24,414 total / 16,676 crawlable nodes treated as an undirected graph; 10 repetitions, 95% confidence interval reported |
| Node-removal resilience (targeted, highest-degree-first) | Graph fully partitions into singleton components after ~60% of nodes removed | Same snapshot and graph construction |
| Node out-degree | Bounded within a narrow band set by the Kademlia parameter k | Same crawl dataset |
| Node in-degree | 90th percentile below ~500; a small number of very-high-in-degree nodes exist, 8 of the top 10 hosted on Amazon AWS | Same crawl dataset |

### Parameters
- Kademlia bucket size k = 20 (used both for the closest-peers lookup and as the number of resolvers contacted during Provide()).
- DHT connection manager target: 600–900 open connections per node (a configurable, version-dependent default the paper notes "were changed between IPFS releases").
- Content retrieval terminates a DHT-based provider search after 20 providers are found or all resolvers are exhausted.
- Crawl cadence: at least twice per day over 101 total crawls; average crawl duration 5.0 minutes; connection timeout 3 minutes (the paper states the choice trades shorter duration for snapshot accuracy against longer timeout for completeness, citing prior crawler-accuracy literature).
- Hydra-Booster instrumentation: 20 virtual peer IDs co-located on one virtual machine.
- Content-identifier (CID) sampling: from raw Bitswap traces, CIDs are deduplicated and a fixed 200,000 sampled per day for the "daily sampled Bitswap CIDs" dataset.
- Provider-record collection window: 28 days, 5.6 million CIDs.

### Stated limitations
The authors state that Bitswap-broadcast-based content discovery reaches only one hop, so their undirected-graph resilience analysis (which treats all observed edges, including Bitswap, as bidirectional communication channels) does not guarantee that content stays equally available even when the graph stays connected; they state a more nuanced analysis of content availability under partition is "left for future work." They state they cannot confirm whether Hydra-Booster's proactive-cache-fill behavior (which generates outbound lookups for every uncached requested CID) was exploited as an intentional denial-of-service vector during the measurement period, only that the behavior creates that exposure. They state their crawl only captures DHT servers, which are nodes with a public IP, so NAT-ed DHT clients are invisible to the topology and cloud-share figures derived from crawling, and must be estimated separately from Bitswap/DHT traffic logs (which is why the crawl-based cloud share, 79.6%, differs from the traffic-log-based cloud share, 35%). They state that the crawl cannot directly observe incoming connections (in-degree), only infer it from presence in other peers' published buckets, which undercounts true in-degree. For the ethics statement, they state they do not attempt to map collected IP addresses back to personal identities and do not perform content lookups on collected CIDs.

### Requirements it places on the rest of the system
This is a measurement paper and defines no mechanism for another system component to depend on. Its results constrain claims a synthesis can make about deployed content-addressed storage: any claim that a Kademlia-DHT-based content-location layer is decentralized in practice must state which channel (topology, traffic volume, content-provider population, or entry points) the claim covers, because the four channels disagree by 15 to 60 percentage points in cloud share depending on which is measured and which counting methodology is used. A synthesis proposing to rely on DHT crawls alone to estimate real participant diversity must account for the paper's finding that counting methodology (unique-IP-across-crawls vs. average-unique-nodes-per-crawl) changes the measured cloud share by a factor of two (39.9% vs. 79.6%), because short-lived, IP-rotating non-cloud nodes are overcounted by the unique-IP method.

### Contradicts
No claim commonly attributed to this paper was found to be unsupported by its text.
Disagrees with WEI-NSDI-24 (Trautwein et al./Wei et al., the same lab's earlier and later IPFS measurement work) on cloud-node share of DHT participants: this paper's 79.6% (its own counting method) versus the 2022 study's under-3% and the same alternative-methodology re-derivation giving 39.9%. The paper attributes the entire disagreement to counting methodology and crawl frequency, not to a change in the network between measurement windows — see WEI-NSDI-24 entry for whether that paper's numbers corroborate or diverge further.

### References worth retrieving
- Trautwein, Raman, Tyson, Castro, Scott, Schubotz, Gipp, Psaras, "Design and evaluation of IPFS: a storage layer for the decentralized web," ACM SIGCOMM 2022 — competing/prior measurement, source of the disputed <3% cloud-node figure this paper re-derives and disputes.
- Henningsen, Florian, Rust, Scheuermann, IPFS DHT crawler and analysis (2019 dataset), cited as [31],[32] — foundational, source of the crawler used in this paper and of the earlier (lower) resilience-to-removal figures this paper improves on.
- Gervais, Karame, Capkun, Capkun, 2014 — cited as [29], attack/critique, address-set-recovery style analysis (see also BIP37 privacy work already in corpus).
- Xia, Wang, Yu, Liu, Luo, Xu, Tyson, "Challenges in decentralized name management: the case of ENS," ACM IMC 2022 — foundational, methodology this paper's ENS dataset extraction follows.
- Albert, Jeong, Barabási, "Error and attack tolerance of complex networks," Nature 2000 — foundational, scale-free-network resilience theory this paper's random/targeted removal analysis is framed against.
- Balduf, Henningsen, Florian, Rust, Scheuermann (cited as [5]) — foundational/self-citation, prior work on Bitswap-broadcast privacy from the same author group.

### Verbatim extracts
- "almost 80% of the IPFS DHT servers are hosted in the cloud with the top 3 cloud providers hosting 51.9% of the servers"
- "5% of the most active peerIDs are responsible for almost 97% of the traffic"
- "34375 (39.9%) addresses on cloud providers, and 51689 (60.1%) non-cloud addresses"
- "The largest component spans 96% of remaining nodes even after randomly removing 90% of nodes"
- "the network ends up completely partitioned into components of size 1 after ≈ 60% of nodes were removed"
- "Around 1% of the peers appear as one of the providers in approximately 90% of the records"
