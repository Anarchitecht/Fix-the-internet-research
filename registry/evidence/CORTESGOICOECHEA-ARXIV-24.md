## [CORTESGOICOECHEA-ARXIV-24] Scalability Limitations of Kademlia DHTs when Enabling Data Availability Sampling in Ethereum

**Citation:** Mikel Cortes-Goicoechea, Csaba Kiraly, Dmitriy Ryajov, Jose Luis Munoz-Tapia, Leonardo Bautista-Gomez. "Scalability limitations of Kademlia DHTs when enabling Data Availability Sampling in Ethereum." arXiv, 2024. DOI 10.48550/ARXIV.2402.09993.
**Retrieved:** full text via https://arxiv.org/pdf/2402.09993
**Source URL:** https://arxiv.org/pdf/2402.09993
**Domain:** A

### What it does
The paper determines whether a Kademlia distributed hash table (DHT — a data structure that maps keys to the network addresses of the nodes storing their values, using node-to-node routing) can serve as the content-location mechanism for Ethereum's proposed Data Availability Sampling (DAS — a scheme letting a node verify a large block is fully published by successfully retrieving a small random subset of its erasure-coded pieces). It builds a discrete-event DHT simulator ("py-DHT") reproducing Kademlia's routing-table structure, lookup and provide (store-announcement) operations, and configurable network-condition parameters (connection failure rates, latency ranges, and a "gamma" overhead parameter modeling the added delay a node experiences from serving many concurrent connections). It validates the simulator against a live measurement tool ("looking-up-ipfs") run against the production InterPlanetary File System (IPFS) Kademlia DHT, then uses the validated simulator to project DHT behavior at Ethereum-scale request volumes the live network was not tested at.

Ethereum's DAS proposal (DankSharding) erasure-codes each block into a 256x256 grid, extended in both directions to 512x512 samples so any half of the samples in a row or column suffice to reconstruct that row or column (and thus the whole block) via Reed-Solomon encoding. Each of the 262,144 resulting samples (512 bytes of data plus 48 bytes of a KZG polynomial-commitment proof) would be addressed and located through the DHT, keyed by a Beacon Node's identifier and the segment's position, rather than through IPFS-style provider records that first ask who holds the content and only then fetch it. A sampling node issues 80 concurrent lookups for randomly selected samples (the number the paper states as sufficient for high-probability reconstruction confidence on a 512-by-512 encoded block) and DAS verification is complete only when every one of the 80 succeeds.

### Measured results

| Operation | Condition | Result |
|---|---|---|
| Lookup hops, live IPFS network | 100 sets of 80 concurrent DHT lookups, real IPFS DHT, AWS Paris VM (4 CPU, 8 GB RAM, 50 GB SSD), 3 Oct 2023 | 99% of lookups completed in under 18 hops; a 1% tail reached up to 100 hops |
| Lookup hops, simulator | 100 sets of 200 concurrent lookups, k=20, alpha=3, beta=20, fast-failure (connection-refusal) rate 10% | 99th percentile 12-14 hops; concurrency-overhead parameter had negligible effect on hop count |
| Lookup latency by region, live IPFS | Probelab Team's regional IPFS measurements, k=20, alpha=3, beta=20 | 90th percentile latency: 700 ms (US), 700 ms (Europe), 1.7 s (South America), 1.5 s (Africa, figure as stated in the paper) |
| Lookup latency, live IPFS | 100 rounds of 80 concurrent lookups, IPFS network | 90% completed between 600 ms and 1.2 s |
| DHT provide (seeding) latency, simulator | 1,000 concurrent provide operations from a single node, network of 12,000 nodes, k=20 | Completed within 20 seconds only under low network overhead; requires higher-end hardware to sustain even that |
| DHT provide (seeding) latency, simulator | 10,000 concurrent provide operations from a single node, same network | The cumulative distribution shows the DHT reaching a throughput bottleneck (no numeric completion time given for this run) |
| DHT provide (seeding) latency, simulator, worst case | 262,144 concurrent provide operations (a full DankSharding block) from a single node, best-case simulated per-connection delay factor of 0.015 ms | 10-14 minutes to complete, roughly 50 to 70 times the 12-second Ethereum slot deadline |
| DHT provide (seeding) latency, live IPFS | 100 sets of 80 concurrent CID (content identifier) provide operations, real IPFS network, 80-second timeout per set | Only about 20% of the 100 sets completed within 70 seconds; about 67% of sets were cut off by the 80-second timeout |
| Per-node storage load under a naive seeding scheme | 262,144 block segments (512 columns x 512 rows) seeded across roughly 13,000 active Ethereum nodes (the paper's stated current network figure), k=20, alpha=3 (the paper's stated standard Kademlia parameters) | 403.29 segments per node on average, every 12 seconds |
| Provide-operation hop count | Same seeding scenario | Median 8 to 10 hops to notify the k closest nodes to a segment's key |

Bottleneck mechanism identified: because Kademlia's routing table keeps the most stable, longest-observed nodes (its k-buckets prefer long-lived contacts, following the original Kademlia paper), the 250-300 nodes in a seeding node's routing table are contacted first on every provide operation and become the most heavily loaded nodes in the network under a high-volume single-seeder workload; the routing table does not change fast enough during a 12-second window to redistribute this load.

### Parameters
- k (replication factor / k-bucket size): 20 (paper's stated standard Kademlia value, used throughout the experiments).
- alpha (maximum concurrent lookup connections per client): 3, matching the value the paper states IPFS uses.
- beta (number of closer peers returned per lookup response): 20.
- Fast error rate (fraction of connections refused outright): varied; 10% used in the reported hop-count simulation.
- Slow error rate (fraction of connections that time out): configurable in the simulator; no single value stated as used across all reported runs.
- Gamma (incremental per-additional-connection overhead delay): varied across simulated runs (Figures 7-10); the best-case value used for the 262,144-sample worst-case run was 0.015 ms per connection.
- Network size: 12,000 simulated nodes for the seeding experiments; approximately 13,000 stated as the live Ethereum active-node count at time of writing; under 500 nodes is stated as the network size used in a prior throughput study (Dabek et al., cited as [11]) that this paper contrasts itself against.
- Sample size: 512 bytes of data plus 48 bytes of KZG proof per DAS sample; 262,144 total samples per block (512x512 grid).
- Concurrent lookups per sampling node: 80 (DAS verification requirement) in the live-network validation runs; 200 in some simulator-only runs (Figures 5, 7).
- Hardware: simulation runs on a Ryzen 5900X CPU, 32 GB RAM, 1 TB SSD; live IPFS benchmark runs on an AWS cloud VM in Paris with 4 CPU cores, 8 GB RAM, 50 GB SSD, dated 3 October 2023.

### Stated limitations
The paper states that a single node (a block proposer or builder) seeding all 262,144 samples cannot complete within the 12-second Ethereum slot deadline under any simulated configuration it tested, because the seeding node's own routing table becomes the bottleneck. It states that alternative seeding by multiple validators, each responsible for the segments in the GossipSub topics they subscribe to, still risks correlating a node's DHT-observed activity with the topic subscriptions of the validators it hosts, compromising validator anonymity, and that this correlation risk is unresolved in the paper. It states that the internal parameters of any deployed Ethereum DAS DHT were not yet fixed at the time of writing. It states that Dabek et al.'s prior DHT-throughput work does not account for the overhead of a network the scale of Ethereum's, having tested under 500 nodes. It states, as future work, an intention to evaluate DHT viability under DAS protocol variants less constrained by the 12-second slot deadline than the one analyzed here.

### Requirements it places on the rest of the system
- Requires a fixed per-operation deadline (the paper's is the Ethereum 12-second slot time) against which any DHT-based content-location mechanism's seeding and lookup latency must be measured; a mechanism whose seeding time scales with the number of items to publish from a single node, as Kademlia's provide operation does here, cannot meet a fixed per-round deadline once item count crosses a threshold the paper places between 1,000 and 10,000 concurrent provides on a 12,000-node network.
- Requires, for the anonymity property DAS assumes (that no observer can correlate which node holds which validator's samples), that neither the DHT's node-ID-to-content mapping nor its topic-subscription pattern leak validator identity; the paper identifies this as unresolved for both single-seeder and multi-seeder GossipSub-based designs.
- Requires a routing-table refresh policy elsewhere in the system if the accelerated-routing-table alternative (crawling the whole network to skip iterative lookups) is used, because refreshing frequently enough to track churn means crawling the network more often, which the paper states is incompatible with Ethereum's preference for low connection counts to limit bandwidth use.
- Requires the erasure-coding scheme (Reed-Solomon, per the paper) to guarantee reconstruction from any half of a row's or column's extended samples; the DHT-location mechanism only has to deliver enough of those samples, not all of them, which is the precondition making sampling-based (rather than full-retrieval) verification meaningful.

### Contradicts
None found within this batch. No other paper in this batch measures the same Kademlia deployment (IPFS) under the same operation; STEINER-CCR-07 and GUMMADI-SIGCOMM-03 examine a different Kademlia deployment (KAD/eMule) and different metrics (attack cost, routing geometry) respectively, not seeding throughput.

### References worth retrieving
- Competing: F. Dabek et al., "Designing a DHT for Low Latency and High Throughput," NSDI (cited as [11]) — a prior DHT-throughput-improvement paper this paper explicitly contrasts its own larger-network results against; tested under 500 nodes.
- Foundational: P. Maymounkov, D. Mazieres, "Kademlia: A peer-to-peer information system based on the XOR metric," IPTPS 2002 (cited as [28]) — already in this corpus per BRIEF.md section 7.
- Competing: Bernhard Heep, "R/Kademlia: Recursive and topology-aware overlay routing," ATNAC 2010 (cited as [22]) — this is the HEEP-ATNAC-10 key already in this batch; the paper cites it as reducing iterative-lookup overhead relevant to the seeding bottleneck it identifies.
- Competing: Elias Rohrer, Florian Tschorsch, "Kadcast: A Structured Approach to Broadcast in Blockchain Networks," AFT 2019 (cited as [37]) — extends recursive Kademlia for efficient broadcast, cited as a candidate mitigation for the seeding-cost problem.
- Competing: Zoltan Czirkos, Gabor Hosszu, "Solution for the broadcasting in the Kademlia peer-to-peer overlay" (cited as [10]) — same broadcast-extension family as Kadcast.
- Foundational/measurement: Dennis Trautwein et al., "Design and evaluation of IPFS: a storage layer for the decentralized web," ACM SIGCOMM 2022 (cited as [44]) — the primary IPFS measurement paper this work's live-network validation builds on.
- Attack/critique-adjacent (privacy): "The IPFS DHT Reader Privacy Upgrade" (cited as [41], a design discussion of double-hashing stored records to reduce query exposure) — directly relevant to the validator-anonymity requirement stated above.
- Competing: Alfonso De la Rocha, David Dias, Yiannis Psaras, "Accelerating content routing with bitswap" (cited as [15]) — the BitSwap alternative to DHT-based content routing the paper discusses as an existing IPFS workaround.
- Competing/independent measurement: Dennis Trautwein et al., "IPFS in the Fast Lane: Accelerating Record Storage with Optimistic Provide" (cited as [45]) — a proposed fix for slow DHT provide operations, the closest published attempt at the same seeding-latency problem this paper measures.
- Foundational: Alexandros G. Dimakis et al., "Network coding for distributed storage systems," IEEE Transactions on Information Theory 56(9), 2010 (cited as [17]) — cited as showing erasure coding combined with DHTs reduces bandwidth for retrievability.
- Superseded-by/emerging-alternative: "PeerDAS proposal" (cited as [31]) and "SubnetDAS proposal" (cited as [40]) — both are stated in the paper's own conclusion as emerging designs that avoid the DHT-seeding bottleneck this paper identifies, at the stated cost of either a reduced sample count (PeerDAS) or weakened query unlinkability (SubnetDAS).

### Verbatim extracts
- "99% of lookups were done in under 18 hops, with a small tail in the last 1% that can reach the 100 hops"
- "a 99th percentile of 12 to 14 hops"
- "90% of concurrent lookups performed between 600ms and 1.2 seconds"
- "roughly 13.000 active nodes"
- "a ratio of 403.29 block segments that each node in the network would have to store"
- "performing a median of 8 to 10 hops until the closest nodes are notified"
- "the congestion in the network would make the process delayed to the 10 to 14 minutes"
- "barely 20% of the hundred sets of provides concluded within 70 seconds"
- "almost 67% of the provides sets were limited by the timeout of 80 seconds"
- "those 250 to 300 in the routing table are always contacted first"
