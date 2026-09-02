## [TRAUTWEIN-SIGCOMM-22] Design and Evaluation of IPFS: A Storage Layer for the Decentralized Web

**Citation:** Dennis Trautwein, Aravindh Raman, Gareth Tyson, Ignacio Castro, Will Scott, Moritz Schubotz, Bela Gipp, Yiannis Psaras. "Design and Evaluation of IPFS: A Storage Layer for the Decentralized Web." ACM SIGCOMM, 2022. Pages not stated in retrieved text. DOI 10.1145/3544216.3544232.
**Retrieved:** full text via https://doi.org/10.1145/3544216.3544232
**Source URL:** https://doi.org/10.1145/3544216.3544232
**Domain:** C+J

### What it does
The InterPlanetary File System (IPFS) locates and retrieves content by its cryptographic hash rather than by its storage location, so a requester can verify what it receives without trusting who served it. IPFS builds a Content Identifier (CID) for each piece of content: a self-describing structure that states the encoding, the hash function used (default SHA2-256), and the hash digest itself. On import, content is split into chunks (default 256 kB), each chunk gets its own CID, and IPFS links the chunks into a Merkle Directed Acyclic Graph (DAG) — a tree-like hash structure that allows a node to have multiple parents, which lets identical chunks shared across files be stored once. To publish content, a node computes a provider record mapping the CID to its own PeerID (the hash of its public key) and stores that record on the k = 20 peers whose PeerIDs are numerically closest to the CID's hash under the XOR distance, using the Kademlia distributed hash table (DHT) — a peer-to-peer index that routes lookups toward the peer whose identifier is closest to the target key. Provider records expire after 24 hours by default and are republished every 12 hours so churned-out peers get replaced. To retrieve content, a requester first asks its already-connected neighbors using the Bitswap block-exchange protocol (a 1-second opportunistic timeout), and only then performs two sequential Kademlia lookups over the DHT: one to map the CID to a hosting PeerID (a "DHT walk," forwarding each request to α = 3 closest-known peers per round), and a second to map that PeerID to a network address (a Multiaddress). It then connects to that address and fetches the content over Bitswap. IPFS distinguishes DHT Server peers (publicly reachable, store and serve records) from DHT Client peers (behind NAT, only request) using AutoNAT: a new peer starts as a client, asks other peers to dial it back, and upgrades to server status once three peers succeed in connecting to it. Anyone that retrieves content can optionally begin serving it themselves by publishing their own provider record for the same CID. IPFS gateways bridge the peer-to-peer network to plain HTTP: a gateway runs a DHT Server node alongside an nginx web server with a Least-Recently-Used (LRU) cache, so a browser with no IPFS software can fetch content via a normal GET request.

### Measured results

| Measurement | Value | Conditions |
|---|---|---|
| Total DHT peers discovered | 198,964 unique PeerIDs, 1,998,825 Multiaddresses, 464,303 unique IP addresses, 152 countries | crawler run every 30 minutes from a server in Germany, over 9,500 network crawls, 2021-07-09 to 2022 (crawler tool: Nebula) |
| Peer reachability | 253,198 (54.5%) reachable at least once; 211,105 (45.5%) never reachable | same crawl dataset |
| Geographic concentration of peers | US 28.5%, China 24.2%, France 8.3%, Taiwan 7.2%, South Korea 6.7% | same crawl dataset, "Detailed Analysis" time window |
| Reliable peers (>90% uptime) | 1.4% (2,747 peers); largest single country (US) holds 0.3% of all peers | same crawl dataset |
| Never-reachable peers | ~33.1% of all discovered peers; China holds 12.5% of these | same crawl dataset |
| Multi-PeerID hosts | 92.3% of IP addresses host exactly one PeerID; top 10 IP addresses host almost 66,000 distinct PeerIDs | same crawl dataset |
| Autonomous System (AS) coverage | peers found in 2,715 unique ASes; top 10 ASes hold 64.9% of IP addresses; top 100 hold 90.6%; 2 Chinese ASes alone hold >30% | same crawl dataset, AS assignment via CAIDA AS Rank |
| Cloud-hosting share | <2.3% of IPFS nodes hosted on any of 1,525 curated cloud-provider IP ranges (Udger dataset); largest single provider (Contabo GmbH) 0.44% | same crawl dataset; compared against a stated 6% Amazon-only share for Mastodon in a separate cited study |
| Churn / session uptime | 87.6% of sessions under 8 hours; only 2.5% of sessions exceed 24 hours; median session length varies from 24.2 min (Hong Kong) to more than double that (Germany) | 467,134 session observations, first half of the "Detailed Analysis" window, long-session-correction method from three cited prior churn studies |
| Content publication latency (overall, all regions combined) | 33.8 s / 112.3 s / 138.1 s at 50th/90th/95th percentile | 6 AWS t2.small VMs, one per region (Bahrain, Sydney, Cape Town, N. California, Frankfurt, São Paulo), each running go-ipfs v0.10.0 as a DHT Server, 3,281 total publication operations across regions, each publishing a fresh 0.5 MB object |
| Per-region publication latency (50th pct) | 27.70 s (Frankfurt) to 42.32 s (São Paulo) | same 6-region AWS setup, per Table 4 |
| DHT walk share of publication delay | 87.9% of overall publication delay on average | same 6-region AWS setup |
| RPC batch duration (storing the provider record at k=20 peers) | 43.3% complete under 2 s; 53.7% exceed 5 s; 11.3% exceed 20 s | same 6-region AWS setup; spikes attributed to TCP/QUIC dial timeouts (5 s) and WebSocket handshake timeout (45 s) |
| Content retrieval latency (overall, all regions combined) | 2.90 s / 4.34 s / 4.74 s at 50th/90th/95th percentile; 100% success rate | same 6-region AWS setup, 14,564 total retrieval operations, sample size 4,324 per graph; includes a mandatory 1 s Bitswap opportunistic-discovery timeout since retrieving peers were disconnected between rounds |
| Per-region retrieval latency (50th pct) | 1.81 s (Frankfurt) to 3.75 s (Cape Town) | same 6-region AWS setup, per Table 4 |
| Single DHT walk median duration (retrieval) | 622 ms; both walks (provider then peer record) complete under 2 s for 50% of retrievals in every region | same 6-region AWS setup |
| Content fetch duration | over 99% of content-exchange operations complete under 1.26 s | same 6-region AWS setup, fixed 0.5 MB object size |
| Retrieval stretch (IPFS retrieval time ÷ estimated HTTPS retrieval time) | majority of operations at least 4x HTTPS across all regions; stretch < 2 for 80% of retrievals in Frankfurt once the 1 s Bitswap timeout is excluded | same 6-region AWS setup, stretch computed as (Discover+Dial+Negotiate+Fetch)/(Dial+Negotiate+Fetch) |
| Gateway usage | 101,000 unique users, 274,000 unique CIDs requested, 6.57 TB downloaded | one public Protocol Labs gateway (ipfs.io, US-located instance), one day of logs, January 2022, 7.1 million user requests |
| Gateway object-size distribution | 79.1% of objects >100 KB; median 664.59 KB; Pearson correlation between object size and latency = 0.13 | same gateway dataset |
| Gateway cache performance | nginx cache median latency 0 s (46.4% of traffic, 46.0% of requests); IPFS node store median latency 8 ms (38.0% of traffic, 40.2% of requests); non-cached median latency 4.04 s (15.6% of traffic, 13.8% of requests) | same gateway dataset, Table 5 |
| Gateway cache hit rate | nginx hit rate 32.3% (at 00:00) to 65.6% (at 17:30); combined with pinned local-store content, hit rate exceeds 80% | same gateway dataset, one-day period, 30-minute bins |
| Gateway referral traffic | 51.8% of traffic referred by third-party websites; 70.6% of that referred traffic from just 72 sites ranked 10k-50k on the Tranco list | same gateway dataset |
| Comparison to prior Kademlia deployments | median record-lookup completes under 1 s for half of IPFS probes, versus over a minute for the BitTorrent Mainline/Azureus Kademlia implementations, cited from two other studies | IPFS: this paper's 6-region AWS setup; BitTorrent Kademlia figures are from Wolchok & Halderman (WOOT 2010) and a second cited crawl study, attributed to excessive dead nodes and slower contemporary links, not independently re-measured here |

### Parameters
- CID chunk size: default 256 kB, used to split imported content before building the Merkle DAG.
- Hash function for CIDs: default SHA2-256, 32-byte digest.
- DHT key space: 256-bit, using SHA256 hashes of PeerIDs and CIDs (the paper states this replaces the original Kademlia 160-bit SHA1 key space, citing anticipated advances in deliberate hash collisions).
- Kademlia bucket structure: i = 256 buckets of k = 20 nodes each.
- Transport for DHT operations: TCP and QUIC, not UDP, cited as a deliberate deviation from the original Kademlia specification made "to make connection management in the implementation more straightforward."
- Provider-record replication factor: k = 20 closest peers by XOR distance, described as a practitioner-chosen compromise between replication overhead and record loss under churn, also referencing a recommendation in the original Kademlia paper.
- Provider-record republish interval: 12 hours (default).
- Provider-record expiry interval: 24 hours (default).
- DHT lookup parallelism (α): 3 peers queried per round during a DHT walk, per the original Kademlia specification.
- AutoNAT server-upgrade threshold: 3 successful inbound connection attempts from other peers.
- Address book size: up to 900 recently seen peers cached locally per node, to skip repeated peer-record lookups.
- Bitswap opportunistic-discovery timeout before falling back to the DHT: 1 second.
- Performance-benchmark object size: 0.5 MB, fixed for every publication/retrieval measurement round.
- Performance-benchmark deployment: 6 AWS t2.small virtual machines, one per region (Bahrain, Sydney, Cape Town, N. California, Frankfurt, São Paulo), each running go-ipfs v0.10.0.

### Stated limitations
The overall publication and retrieval delay measurements are described by the authors as the closest achievable to a controlled experiment on the public IPFS network, but not a true controlled experiment, because peer churn, CPU load, and traffic load on the rest of the network cannot be replicated in a simulation and are outside the authors' control. The performance benchmark used only a fixed 0.5 MB object size; the authors state that content-exchange duration depends on the amount of data exchanged, so retrieval-duration figures at other object sizes are not established by this paper. The stretch metric approximates the equivalent HTTPS retrieval time by subtracting the DHT discovery step from the measured IPFS time, rather than performing an independent HTTPS measurement. Retrieval measurements were run from AWS data centers, and the authors state explicitly that last-mile performance experienced by home users will differ. The authors state they have not evaluated IPFS's resilience or its capacity to withstand information attacks such as censorship, and describe this as future work. Moderation and misuse on IPFS, including a reported instance of the Storm botnet operating over the network, had not been investigated at the time of writing; the authors state their initial monitoring found no abusive behavioral signals but call further investigation future work. The Hydra Boosters DHT-augmentation component was explicitly excluded from the study due to space constraints and what the authors describe as its limited adoption. Content-import latency (as opposed to provider-record publication latency) is stated as already covered by a separate cited paper and not reevaluated here.

### Requirements it places on the rest of the system
Content retrieval requires a functioning Kademlia DHT populated with enough long-lived DHT Server peers to answer two sequential lookups (CID-to-PeerID, then PeerID-to-Multiaddress) inside the 24-hour provider-record expiry window; if fewer than k = 20 peers close to a CID remain reachable, the provider record for that CID can be lost. Any consumer of IPFS retrieval-latency figures needs to account for the mandatory 1-second Bitswap opportunistic-discovery timeout baked into every retrieval reported here, because the authors' experimental setup guaranteed a Bitswap miss on every trial. Nodes behind NAT cannot serve content as DHT Servers under the AutoNAT scheme described, so a deployment relying on those peers for storage capacity needs a separate hole-punching mechanism (the paper notes one was under development but not yet deployed) or third-party pinning services to host content on their behalf. The self-certifying CID scheme requires every consumer to independently recompute and check the content hash against the received CID; nothing in IPFS enforces this except that a mismatch is externally detectable. Because CIDs are immutable, any system built on top that needs mutable references must add a separate mapping layer (the IPNS scheme described maps a PeerID-derived CID to a signed pointer, itself requiring key management the paper does not detail here).

### Contradicts
The comparison in Related Work states that IPFS's median record-lookup latency (under 1 second for half of probes) contrasts with prior operational-DHT measurement studies of BitTorrent's Kademlia implementation reporting latencies exceeding a minute; the authors attribute this gap to excessive dead nodes and slower links in the earlier deployments rather than to a property of Kademlia itself, and this paper's own DHT still exhibits an 87.9%-of-delay DHT walk cost during publication, so the low-latency finding applies specifically to the two-hop retrieval walk, not to the 20-way publication RPC batch. No entry in this corpus reports a disagreeing IPFS-network-scale measurement (searched: no other IPFS deployment-measurement paper is in this batch).

### References worth retrieving
- Maymounkov, Mazières, "Kademlia: A peer-to-peer information system based on the XOR metric," IPTPS 2002 — foundational (already verified in this corpus per BRIEF.md §7)
- Wolchok, Halderman, "Crawling BitTorrent DHTs for Fun and Profit," WOOT 2010 — attack/critique (measured BitTorrent's Kademlia deployment showing lookup latencies exceeding a minute, the paper's own comparison point)
- Stutzbach, Rejaie, "Improving lookup performance over a widely-deployed DHT," INFOCOM 2006 — competing (independent Kademlia performance measurement and proposed fixes, cited as showing substantially worse performance than IPFS)
- Stutzbach, Rejaie, "Understanding Churn in Peer-to-Peer Networks," IMC 2006 — foundational (source of the long-session churn-correction methodology this paper's churn analysis reuses)
- Wang, Kangasharju, "Measuring large-scale distributed systems: case of BitTorrent Mainline DHT," P2P 2013 — competing (independent operational-DHT measurement study, cited as reporting churn rates similar to this paper's findings but slower lookups)
- Raman, Joglekar, De Cristofaro, Sastry, Tyson, "Challenges in the decentralised web: The mastodon case," IMC 2019 — competing (federated, non-content-addressed decentralization architecture used as the paper's cloud-hosting-share comparison point, 6% Amazon-only for Mastodon versus <2.3% any-cloud for IPFS)
- Vorick, Champine, "Sia: Simple Decentralized Storage," Nebulous Inc. technical report, 2014 — competing (incentivized decentralized storage network cited in Related Work; already a target of this batch, VORICK-SIA-14)
- Williams, Diordiiev, Berman, Raybould, Uemlianin, "Arweave: A Protocol for Economically Sustainable Information Permanence," technical report — competing (another incentivized decentralized storage network cited alongside Filecoin and Sia)

### Verbatim extracts
- "fewer than 2.3 % of IPFS nodes run in major cloud platforms"
- "the overall IPFS content retrievals have a median stretch of 4.3"
- "This is because it is very difficult to replicate peers' behaviour"
- "we are yet to evaluate the resilience of IPFS"
- "moderation remains a challenge"
- "20 is selected based on our practical experiences"
- "IPFS does not incentivize data storage, sharing, or participation"
