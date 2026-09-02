## [ZHANG-FC-23] Kadabra: Adapting Kademlia for the Decentralized Web

**Citation:** Yunqi Zhang, Shaileshh Bojja Venkatakrishnan. "Kadabra: Adapting Kademlia for the Decentralized Web." Financial Cryptography and Data Security, 2023. DOI 10.1007/978-3-031-47751-5_19.
**Retrieved:** full text via https://arxiv.org/pdf/2210.12858
**Source URL:** https://arxiv.org/pdf/2210.12858
**Domain:** A

### What it does
Kadabra reduces Kademlia lookup latency by choosing which peers occupy each node's routing-table k-bucket based on measured past performance rather than by prefix range and random selection alone. Kademlia (background, section 2.1) assigns every node a binary identifier and routes a lookup for a key by repeatedly forwarding to the peer, from an n-entry table of k-buckets, whose identifier shares the longest common prefix with the target key under the bitwise-XOR distance metric; the i-th k-bucket holds up to k peers sharing the node's first i-1 identifier bits while differing in the i-th bit. Kadabra treats the choice of which eligible peer occupies each k-bucket as a non-stationary multi-armed-bandit problem, solved independently per bucket (since a decomposition argument shows each query touches at most one bucket). Every b queries routed through a bucket (b=100 in the paper's experiments) close one epoch and open the next. At the end of an epoch, each peer u in the current bucket receives a score equal to the negative sum, over every query routed through u during the epoch, of the time taken to receive a response through u; a query that did not route through u contributes a fixed user-set penalty value Delta instead, so a large Delta favors frequently used peers and a small Delta favors fast peers. On a random-exploration epoch (scheduled to occur every other epoch in the implementation), the node replaces the worst-scoring peer in the bucket with a peer drawn uniformly at random from the subset of known eligible peers whose measured round-trip time exceeds a user-set security parameter rho; on a non-exploration epoch, the node keeps whichever of the current or previous bucket configuration scored higher. The rho threshold exists because sampling replacement peers uniformly from all eligible peers converges toward proximity neighbor selection (choosing only nearby peers), which lowers latency but concentrates the bucket geographically, making a Sybil attack that floods low-RTT identities near the victim cheap; restricting exploration to peers farther than rho trades some latency for resistance to that concentration.

### Measured results
All results are from a custom Python discrete-event simulator (not a live network deployment), described in section 5.1; the authors state they avoided OverSim and PeerSim because those simulators are no longer maintained.

| Setting | Comparison | Result | Conditions |
|---|---|---|---|
| Nodes in a square, uniform demand, 1st k-bucket | Kadabra vs. its own random-initial epoch-0 configuration | 15% latency reduction | 2,048 nodes placed uniformly in a 10,000x10,000 Euclidean square; per-pair latency = Euclidean distance + uniform-random(100,5000) perturbation; per-node upload latency uniform-random(100,2000); averaged over 100 epochs |
| Same setting | Kadabra vs. original (vanilla) Kademlia | more than 20% lower latency | Same setup as above |
| Nodes in a square, 10-million-query run | 90th-percentile latency, last 1000 queries vs. first 1000 queries (identical query sequence at start and end) | more than 24% reduction | Same square topology and node-latency distribution |
| Nodes in a square, demand hotspots (20% of keys receive 80% of lookups) | Kadabra vs. original Kademlia and proximity routing (PR) | more than 25% lower latency | Same square topology, hotspot keys randomly chosen |
| Nodes in a square, localized high-latency region (2000x2000 sub-region set to 5,000-time-unit node latency vs. default) | Kadabra vs. proximity neighbor selection (PNS) | more than 25% latency improvement | Same square topology; PNS is reported to severely degrade for a node located inside the high-latency region because it keeps favoring nearby (also high-latency) peers |
| Nodes in the real world, 1st k-bucket of a node in Frankfurt | Kadabra vs. original Kademlia | 50% lower latency | 2,048 nodes placed at real-world city locations from an Ethereum node tracker; inter-city latency from a global ping-measurement dataset, nearest-available-city substituted where a city is missing; per-node latency drawn from an exponential distribution with mean 1,000 ms |
| Same setting | Kadabra vs. PNS and vs. PR | 35% lower latency (against both) | Same real-world topology |
| Real-world topology, region near New York City set to double the default average node latency | Kadabra vs. PNS | more than 40% more efficient (Kadabra degrades slightly but less than PNS) | Same real-world topology and latency model |
| Real-world topology, 20% of nodes adversarial (deliberately delay queries passing through them to 3x their default node latency), adversarial nodes concentrated near one victim | Kadabra vs. PNS at the victim node | Kadabra bypasses the adversarial region; PNS incurs more than 2x Kadabra's latency | Same real-world topology, 20% of 2,048 nodes marked adversarial |
| Aggregate across all evaluated settings | Kadabra vs. best baseline (varies by setting) | 15%-50% lower lookup latency | Stated as the paper's overall headline range across the square and real-world settings above |

### Parameters
- k-bucket update interval b: 100 queries per epoch (used in experiments).
- Exploration schedule: one random exploration epoch every other epoch, replacing exactly one bucket entry per exploration epoch in the reported implementation (the paper notes the number of replaced peers can be configured higher).
- Penalty parameter Delta (assigned to a query not routed through a given peer): set to a value slightly larger than the moving average of latencies observed for lookups through the bucket (no fixed numeric value given; described as adaptively chosen).
- Security parameter rho (minimum RTT threshold for an exploration candidate): swept experimentally at values [400, 350, 300, 250, 200, 150, 100, 50, 0] across the nine k-buckets (1st through last) in the square-topology experiment; no single fixed value recommended, described as a security/latency tradeoff knob to be set by the operator.
- Network size (both topologies): 2,048 nodes.
- Query fan-out alpha (parallel lookup paths, inherited from Kademlia, for the DHT application): alpha = 3 (example value given in background); alpha = 1 used for the KBR application evaluated in this paper.
- Adversarial-node evaluation: 20% of nodes marked adversarial, delaying queries by 3x their default node latency.
- Simulation length for the tail-latency (90th-percentile) experiment: 10 million queries (1 query per round, one random source-destination pair per round).

### Stated limitations
The authors state that a thorough analysis of Kadabra's robustness against attacks beyond Sybil, eclipse, and adversarial routing is left as future work, citing a specific attack-taxonomy reference. They state that testing Kadabra's convergence and performance in a real deployed network (naming IPFS and Swarm as examples) is left as future work; every result in this paper is simulation-only. They state that obtaining a theoretical (as opposed to empirical) understanding of Kadabra's convergence behavior is left as future work. The system model explicitly does not model the time taken to download a value, only the time to upload it, reasoning that download bandwidth typically exceeds upload bandwidth (section 3, stated as a modeling choice, not a validated measurement). The paper focuses primarily on recursive routing (a query relayed hop to hop by intermediate nodes) rather than iterative routing (the initiator itself contacts each hop); iterative-routing results are stated to be deferred to an appendix.

### Requirements it places on the rest of the system
Each node must locally record, per query it routes or initiates, which peer the query passed through and how long a response took to arrive; the scoring function operates only on this locally observed per-peer latency history, so no external latency-measurement service or shared state across nodes is required, but every node must implement and continuously run this bookkeeping. The exploration mechanism requires that a node knows the round-trip time to peers in its eligible-peer list L before deciding whether to include them (section 4.3: "we assume the node also knows the RTT to each peer in the list"), so a component supplying candidate peers to a Kadabra node must also supply or make measurable an RTT value for each candidate. The security property (resistance to Sybil concentration) depends entirely on the operator-chosen rho threshold; the paper does not specify how rho should be set as a function of network conditions, so a deploying system must supply that policy itself. The scoring mechanism assumes queries continue to flow through a bucket at a roughly steady rate sufficient to accumulate b=100 samples per epoch; a bucket that is rarely used will update its configuration only rarely, and the paper does not measure or bound the latency-adaptation delay under low query volume.

### Contradicts
None found. The paper's own related-work section states that Kademlia's lookup-latency problem has been targeted by many "hand-crafted heuristics" (Kaune et al., Jimenez et al., Chen et al.) which the authors say do not adapt to network heterogeneity, an attributed comparison rather than a numeric one — no comparison figures are given for those specific systems inside this paper.

### References worth retrieving
- Maymounkov, Mazières, "Kademlia: A peer-to-peer information system based on the XOR metric," IPTPS 2002 — foundational (already in corpus)
- Baumgart, Mies, "S/Kademlia," ICPADS 2007 — foundational (already in corpus; source of the Sybil/eclipse/adversarial-routing countermeasures Kadabra's related-work section cites as the basis for today's Kademlia security practice)
- Gummadi, Gummadi, Gribble, Ratnasamy, Shenker, Stoica — cited as [23], systematic comparison of proximity routing and proximity neighbor selection across DHT protocols — competing (source of the PR and PNS baselines Kadabra measures against)
- Trautwein, Wei, Psaras, Schubotz, Castro, Gipp, Tyson, "Design and Evaluation of IPFS: A Storage Layer for the Decentralized Web" — competing / independent measurement (cited as source of the 112s 90th-percentile IPFS content-storing latency figure quoted in this paper's section 2.2; note this is a different paper by an overlapping author from TRAUTWEIN-INFOCOM-24 in this corpus and should not be conflated with it)
- Kanemitsu et al., "KadRTT" — competing (RTT-based target selection and ID arrangement for Kademlia lookup acceleration)
- Steiner et al. — competing (integrated content lookup protocol for Kad, a Kademlia-based file-sharing network)
- Zhu et al. — competing (storage algorithm for Kademlia addressing load imbalance)

### Verbatim extracts
- "Kadabra achieving between 15-50% lower lookup latencies compared to state-of-the-art baselines" (abstract)
- "a decision on a k-bucket ... is made each time after b queries are routed" (section 4.1)
- "one entry on the k-bucket is chosen randomly every other epoch" (section 4.1)
- "restrict the choice of peers that are sampled during exploration" (section 4.3, on parameter rho)
- "a thorough analysis of Kadabra's robustness against other known attacks ... is a direction for future work" (conclusion)
- "Testing Kadabra's convergence and performance in a real world network ... [is an] important direction for future work" (conclusion)
