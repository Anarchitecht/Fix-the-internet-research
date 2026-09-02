## [HEEP-ATNAC-10] R/Kademlia: Recursive and Topology-aware Overlay Routing

**Citation:** Bernhard Heep. "R/Kademlia: Recursive and Topology-aware Overlay Routing." Australasian Telecommunication Networks and Applications Conference (ATNAC), 2010. Pages 102-107. DOI 10.1109/ATNAC.2010.5680244.
**Retrieved:** full text via https://telematics.tm.kit.edu/publications/Files/416/RKademlia_2010.pdf
**Source URL:** https://telematics.tm.kit.edu/publications/Files/416/RKademlia_2010.pdf
**Domain:** A

### What it does
R/Kademlia reduces key-based routing (KBR — the service of delivering a message to whichever overlay node is currently responsible for a given destination key) latency and network traffic below original Kademlia's, by replacing Kademlia's iterative lookup with recursive routing while keeping Kademlia's k-bucket routing-table structure and XOR distance metric unchanged.

In iterative routing (original Kademlia), the lookup initiator itself contacts a sequence of O(log N) nodes (N the network size) one round at a time, each returning closer candidates, and the initiator retains control of the whole procedure; parallel Remote Procedure Calls (RPCs, sent to several candidate nodes at once) reduce the effect of unresponsive nodes but increase bandwidth use. In recursive routing, each node on the path forwards the message directly to whichever peer in its own k-buckets is closest (by the routing metric) to the destination key, so the initiator loses control of the message after the first hop; a recursive lookup is the same mechanism but returns a list of close nodes to the initiator instead of delivering a message. Because a purely recursive lookup gives the initiator no new peer contacts (contacted nodes never respond directly to it, unlike in iterative mode), R/Kademlia adds one of two signaling modes to let the initiator (and, in one mode, every node on the path) learn about new peers anyway: Direct Mode, where every node on the routing path sends n of its own closest-to-target k-bucket entries straight back to the initiator by a separate message type (at the cost of contacting non-peers, which the paper states can create difficulties in Network Address Translation/Port Address Translation, NAT/PAT, scenarios); and Source-routing Mode, where the destination node's closest nodes are merged into the path hop-by-hop back to the initiator, so every intermediate node also learns of new peers, using only peer-to-peer connections but shifting more messages onto the return path. Hop-by-hop acknowledgments detect a failed node on the path (the timeout computed TCP-style as t_o = RTT_X + 4*sigma_RTT_X) and cause the message to be rerouted to the next-closest node rather than restarting the whole lookup.

R/Kademlia adds two topology-adaptation mechanisms, both defined originally by Castro et al. and applied here to Kademlia's structure: Proximity Neighbor Selection (PNS), which fills each k-bucket slot with whichever of the candidate nodes is physically closest (lowest network latency) rather than using Kademlia's original least-recently-used (LRU) eviction, requiring every newly met candidate node to be latency-probed before being admitted; and Proximity Routing (PR), which at each routing hop picks the next node by a combined metric d_KadPR(X,Y) = d_prox(X,Y) + d_prefix(X,Y), trading progress in identifier space against physical proximity, applicable only to recursive routing because it is a per-hop local decision. PR requires no advance probing beyond what is already needed to fill k-buckets (an unprobed candidate's proximity is set to 0.99 by default, or estimated via a network coordinate system), while PNS requires probing every newly met node for availability before insertion, which the paper states makes network-coordinate estimation unsuitable for PNS specifically.

### Measured results
All results are from OverSim-framework discrete-event simulation, not a live deployment.

| Comparison | Conditions | Result |
|---|---|---|
| Routing-latency/bandwidth trade-off, all parameter combinations | 5,000 simulated nodes, node lifetime mean 10,000 s (Weibull, shape k=0.5), k-bucket size 8, active probing enabled | R/Kademlia's convex hull dominates (best latency for given bandwidth, or vice versa) both plain Kademlia (exhaustive-iterative) and the "simple" iterative mode (which terminates on first responsible-node contact); original exhaustive-iterative Kademlia performs worst due to its non-terminating exhaustive lookup |
| RPC routing latency by churn scenario, active probing on | Node lifetime mean swept 1,000-30,000 s, 5,000 nodes, direct signaling mode, comparison includes 5 parallel RPCs for iterative modes | R/Kademlia without topology adaptation: ~350 ms; simple iterative (5 parallel RPCs): ~630 ms; original exhaustive-iterative Kademlia (not plotted numerically as a curve): 2-5 s depending on churn rate; iterative with PNS: ~415 ms; R/Kademlia with PNS: ~225 ms; combining PNS and PR gave no further latency reduction over PNS alone |
| Bandwidth consumption per node, active probing on | Same sweep as above | R/Kademlia without topology adaptation and R/Kademlia with PR: ~140 bytes/s; simple iterative and iterative-with-PNS modes: ~300 and ~1,250 bytes/s respectively; PNS (in either routing mode) uses about 4 times the bandwidth of the corresponding non-PNS variant |
| Signaling-mode comparison (Direct vs. Source-routing), low/moderate churn | Node lifetime mean >= 10,000 s | Direct Mode gives lower traffic per node than Source-routing Mode |
| Signaling-mode comparison, high churn | Node lifetime mean = 1,000 s | Combination of PNS with Source-routing Mode gives the best routing latency, because more nodes are met and probed under source routing, keeping k-buckets filled with recently verified, physically close nodes |
| Active-probing-disabled scenarios | Same lifetime sweep, active probing off (larger effective stabilization interval t_s) | Recursive routing achieves better latency only in low/moderate churn; iterative combined with PNS becomes faster in high-churn scenarios, at very high bandwidth consumption |
| Recursive vs. iterative crossover point (from prior work by Wu, Tian, Ng, cited as [3], reanalyzed here with the KAD lifetime model) | Weibull session-time model (shape k=0.5, lambda=5,000, from Stutzbach/Rejaie and Steiner/En-Najjary/Biersack's KAD churn measurements) | Recursive routing with hop-by-hop acknowledgments achieves lower routing latency than iterative routing with 5 parallel RPCs for stabilization intervals t_s up to approximately 2,500 s |

### Parameters
- k-bucket size (k): 8, fixed across all reported experiments.
- Node count: 5,000 simulated nodes (OverSim).
- Churn model: Weibull-distributed session time, shape parameter k=0.5, mean lifetime swept from 1,000 to 30,000 s; the paper's default matching value (mean 10,000 s) is stated as resembling measured KAD churn from two cited prior studies (Stutzbach and Rejaie, IMC 2006; Steiner, En-Najjary, Biersack, IEEE/ACM Trans. Networking 2009).
- t_b (bucket-refresh / maintenance interval for unused buckets): 1,000 s.
- Probe application traffic: 100-byte probe RPC messages sent from each node to random alive nodeIDs, normally distributed interval mean 60 s.
- Failed-routing latency penalty: counted as 10 s.
- Underlay network model: OverSim's "Simple Underlay," latencies from network coordinates based on Skitter Internet measurements.
- Simulation runs: 20 repetitions per protocol/parameter combination, each 1,800 s after a 1,800 s network build-up/transition phase; 95% confidence intervals computed (stated as usually too small to be visible in the plots).
- Iterative-mode parallelism levels tested: 1, 3, and 5 parallel RPCs.
- Signaling mode default for all reported non-signaling-comparison results: Direct Mode.

### Stated limitations
The paper states its evaluation of NAT/PAT (Network Address Translation/Port Address Translation) compatibility is left to future work, despite listing NAT/PAT avoidance as a design goal; Direct Mode is stated to risk connection problems in NAT/PAT scenarios because the initiator and path nodes exchange messages without being established peers. Source-routing Mode is stated to risk message loss when a node on the return path fails during high churn, since the return path is not covered by the same hop-by-hop acknowledgment mechanism used on the forward path. The paper defers a simulative comparison against other recursive KBR protocols, specifically Bamboo, to future work, reporting only that unpublished first results favor R/Kademlia's latency/bandwidth trade-off in low-churn scenarios. It states an intention to apply two additional topology-adaptation mechanisms from the author's other work (coordinate-based routing, dCBR) to R/Kademlia in future work. The paper explicitly excludes Topology-based NodeId Assignment (TbNA) from consideration, citing that it produces a non-uniform nodeId distribution.

### Requirements it places on the rest of the system
- Requires hop-by-hop hop failure detection (the TCP-style RTT-based timeout) to be computable at every node on the routing path, which requires each node to keep round-trip-time mean and variance estimates for its k-bucket peers.
- Requires, for PNS, that every newly met candidate node be latency-probed before insertion into a k-bucket; a network coordinate system cannot substitute for this because it states coordinate systems cannot estimate node availability, which PNS also requires before admission.
- Requires, for Direct Mode, that nodes accept and process signaling messages from non-peer originators (nodes they have no established relationship with), which the paper flags as the source of its stated NAT/PAT risk.
- Requires all nodes along a routing path to run R/Kademlia (not plain Kademlia) for its signaling modes to function; the paper states R/Kademlia can run in a mixed mode alongside the original protocol, but the recursive signaling modes require universal support among path nodes.
- Requires an accurate churn model (session-time distribution) to be supplied for tuning t_b and t_s; the paper's own headline results are specific to the Weibull(k=0.5, mean 10,000 s) model taken from measured public KAD networks and do not by themselves establish behavior under a different churn distribution.

### Contradicts
None found. This entry is itself a comparison point BRIEF.md section 8 (open problem list item on iterative-versus-recursive routing) calls for; it does not contradict any already-verified entry, and no other paper in this batch measures R/Kademlia.

### References worth retrieving
- Foundational: P. Maymounkov, D. Mazieres, "Kademlia: A Peer-to-Peer Information System Based on the XOR Metric," IPTPS 2002 — already verified per BRIEF.md section 7.
- Foundational: A. Rowstron, P. Druschel, "Pastry: Scalable, Decentralized Object Location, and Routing for Large-Scale Peer-to-Peer Systems," Middleware 2001 — the k-bucket organizational analog R/Kademlia's routing table is compared to.
- Foundational: M. Castro, P. Druschel, Y. C. Hu, A. Rowstron, "Exploiting network proximity in distributed hash tables," FuDiCo 2002 — origin of the Proximity Routing / Proximity Neighbor Selection / Topology-based NodeId Assignment taxonomy this paper adopts.
- Competing: D. Wu, Y. Tian, K.-W. Ng, "Analytical Study on Improving DHT Lookup Performance under Churn," P2P 2006 — the source of the recursive-vs-iterative crossover analysis (Fig. 1/Fig. 2 data) this paper reuses and re-derives with the KAD churn model.
- Competing: S. Rhea, D. Geels, T. Roscoe, J. Kubiatowicz, "Handling Churn in a DHT" (Bamboo), USENIX ATEC 2004 — Bamboo is the other recursive-routing KBR protocol this paper states it plans to compare against in future work.
- Competing: J. Li, J. Stribling, R. Morris, M. F. Kaashoek, "Bandwidth-efficient management of DHT routing tables," NSDI 2005.
- Competing: S. Kaune, T. Lauinger, A. Kovacevic, K. Pussep, "Embracing the Peer Next Door: Proximity in Kademlia," P2P 2008 — applies PNS-style topology adaptation to plain iterative Kademlia; the paper this work's PNS-in-recursive-vs-iterative comparison responds to.
- Foundational (measurement): D. Stutzbach, R. Rejaie, "Understanding Churn in Peer-to-Peer Networks," IMC 2006.
- Foundational (measurement): M. Steiner, T. En-Najjary, E. W. Biersack, "Long Term Study of Peer Behavior in the KAD DHT," IEEE/ACM Transactions on Networking 17(6), 2009 — source of the KAD churn model (Weibull k=0.5) used for this paper's default simulation parameters; note this is by the same first two authors as STEINER-CCR-07 and a companion measurement paper already in this batch/corpus.
- Methodology tool: J. Li, J. Stribling, R. Morris, M. F. Kaashoek, T. M. Gil, "A performance vs. cost framework for evaluating DHT design tradeoffs under churn," INFOCOM 2005 — the PVC framework used to produce this paper's convex-hull plots.
- Simulation infrastructure: I. Baumgart, B. Heep, S. Krause, "OverSim: A flexible overlay network simulation framework," GI 2007 — the simulator this paper's results were produced in.

### Verbatim extracts
- "R/Kademlia shows the best trade-off between routing latencies and bandwidth consumption"
- "R/Kademlia without topology adaption is faster (≈350 ms) than the simple iterative variant (≈630 ms)"
- "Activated PNS leads to an immense decrease of routing latencies... especially with R/Kademlia (≈225 ms)"
- "R/Kademlia without topology adaptation and R/Kademlia with PR activated come with a significant lower bandwidth consumption (≈140 Bytes/s)"
- "The amount of network traffic needed by PNS is about 4 times as much"
- "recursive routing with activated hop-by-hop acknowledgements is superior... up to a stabilization interval of ts≈2,500s"
- "network coordinate systems are here inappropriate, as these systems cannot be used for estimating availability"
