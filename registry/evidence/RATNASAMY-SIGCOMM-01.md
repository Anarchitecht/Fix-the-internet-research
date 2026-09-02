## [RATNASAMY-SIGCOMM-01] A Scalable Content-Addressable Network
**Citation:** Sylvia Ratnasamy, Paul Francis, Mark Handley, Richard Karp, Scott Shenker. "A Scalable Content-Addressable Network." ACM SIGCOMM, 2001. DOI 10.1145/383059.383072.
**Retrieved:** full text via https://people.eecs.berkeley.edu/~sylvia/papers/cans.pdf
**Source URL:** https://people.eecs.berkeley.edu/~sylvia/papers/cans.pdf
**Domain:** A

### What it does
A Content-Addressable Network (CAN) maps a key to a value across a distributed set of nodes so that any node can locate a value knowing only its key, without a central index. Each node owns a distinct zone of a virtual d-dimensional Cartesian coordinate space defined on a torus (the space wraps at its edges). A key is hashed by a uniform hash function onto one point in that space; the (key, value) pair is stored at the node owning the zone containing that point. Two nodes are neighbors if their zones overlap along d-1 dimensions and abut along one dimension. Routing forwards a message greedily toward the destination coordinates, at each step choosing the neighbor whose zone lies closest to the destination point (straight-line greedy forwarding). A joining node discovers a bootstrap node, is routed by that node's CAN to a random point, and splits the zone of the node currently owning that point, taking half. A departing or failed node's zone is taken over by a neighbor: on graceful departure the zone is merged with a neighbor's or handed to the neighbor with the smallest zone; on failure, neighbors independently start a takeover timer proportional to their own zone volume and the neighbor with the smallest zone volume wins by sending a TAKEOVER message, so the takeover algorithm favors the neighbor whose absorption keeps the space best balanced. A background zone-reassignment algorithm (Appendix A) later restores a one-node-per-zone assignment by locating, via local coordinate-routing-table operations equivalent to a depth-first search over an implicit binary partition tree, a pair of sibling zones that can be recombined.

### Measured results

| Result | Value | Conditions |
|---|---|---|
| Path length scaling | O(d · n^(1/d)) hops; average path length = (d/4)(n^(1/d)) for perfect partitioning | d-dimensional coordinate space, n nodes, analytical result confirmed by simulation (Figure 4) |
| Per-node neighbor state | 2d neighbors | perfectly partitioned d-dimensional space |
| Effect of dimensions on path length | path length falls from 198.0 hops (d=2 "bare-bones") to ~5.0 hops (d=10 "knobs-on-full") | n = 2^18 = 262,144 nodes, Transit-Stub topology, 100ms intra-transit / 10ms stub-transit / 1ms intra-stub link delays |
| RTT-weighted routing, per-hop latency reduction | 24%-40% lower per-hop latency than unweighted routing, depending on dimension count (Table 1: d=2, 116.8ms to 88.3ms; d=3, 116.7ms to 76.1ms; d=4, 115.8ms to 71.2ms; d=5, 115.4ms to 70.9ms) | Transit-Stub topology, 100/10/1ms link delays, average underlying IP path latency ~115ms, n ranging from 2^8 to 2^18, results averaged over test runs |
| Zone overloading (MAXPEERS), per-hop latency reduction | per-hop latency falls from 116.4ms (1 node/zone) to 92.8ms (2), 72.9ms (3), 64.4ms (4 nodes/zone) (Table 2) | system sizes ranging from 2^8 upward |
| Cumulative "knobs-on-full" vs "bare-bones" comparison at n = 2^18 (262,144) nodes | path length 198.0 to 5.0 hops; average neighbor count 4.57 to 27.1 (plus 2.95 peers, i.e. ~30 total); average IP-level latency to the retrieved replica 115.9ms to 82.4ms; CAN path latency 23,008ms to 135.29ms | bare-bones: d=2, r=1, p=0, k=1, RTT weighting off, uniform partitioning off. Knobs-on-full: d=10, r=1, p=4, k=1, RTT weighting on, uniform partitioning on, landmark ordering excluded. Same Transit-Stub topology as above (Tables 4 and 5) |
| Scaling n from 2^14 to 2^18 under "knobs-on-full" (d=10) | path length rises from 4.56 hops (2^14 nodes) to 5.0 hops (2^18 nodes), growing slower than the n^(1/10) bound predicts because added hops at growing topology edges carry lower-than-average per-hop latency | same Transit-Stub topology, edge nodes added without scaling the backbone |
| Extrapolated scaling limit | authors state that under a pessimistic assumption (latency grows as n^(1/10)), the system could grow roughly another factor of 2^10 (to close to one billion nodes) before path latency exceeds four times the underlying IP latency | extrapolation from the above measured trend, not itself measured |
| Uniform partitioning effect on zone-volume distribution | without the feature, ~40% of nodes hold zones of volume V (the per-node fair share); with the feature, ~90% of nodes hold zones of volume V, and the largest observed zone volume drops from 8V to 2V | n = 65,536 nodes, 3 dimensions, 1 reality, simulation (Figure 9) |
| Background zone-reassignment hop count | average hops to find a re-assignable sibling zone: 1.12 (d=2), 1.09 (d=3), 1.07 (d=4); maximum observed: 3 hops in all three cases | simulation, uniform-partitioning feature enabled (Table 6) |
| Multiple realities effect on path length | additional independent coordinate spaces ("realities") reduce path length; for equal per-node neighbor state, increasing dimensionality reduces path length more than increasing the number of realities | 2-dimensional space, comparison at n up to 131,072 nodes (Figures 5 and 6) |

### Parameters
- Dimensionality d of the coordinate space: bare-bones d=2, knobs-on-full d=10; per-node neighbor state grows as O(d), path length falls as O(d n^(1/d)).
- Number of realities (independent coordinate spaces) r: bare-bones r=1; each reality adds an independent neighbor set and replicates the full (key,value) store, improving availability but adding O(r) per-node state.
- MAXPEERS (peer nodes sharing one zone) p: bare-bones p=0, knobs-on-full p=4; the paper states this value would typically be low, 3 or 4.
- Number of hash functions k (points per reality at which a (key,value) pair is stored): bare-bones and knobs-on-full both use k=1; the paper separately evaluates k=3 and k=5 (Figure 7), each multiplying query traffic and store size by k.
- RTT-weighted routing metric: on/off switch; forwards to the neighbor maximizing the ratio of coordinate-space progress to measured round-trip time.
- Uniform-partitioning feature: on/off switch; a joining node's host node splits whichever of its own zone or its neighbors' zones has the largest volume, rather than always splitting its own.
- Landmark ordering (topologically-sensitive construction): evaluated separately with 4 landmarks at least 5 hops apart; excluded from the knobs-on-full comparison and described by the authors as work in progress not otherwise used in the paper.

### Stated limitations
Designing a CAN resistant to denial-of-service attacks is called an open problem by the authors: a malicious node can act as a malicious client, server, or router, unlike on the Web. Extending CAN to handle mutable content and building keyword search on top of CAN indexing are listed as future work. The immediate-takeover algorithm loses the (key,value) pairs held by a failed node until other holders refresh that state. Under simultaneous failure of multiple adjacent nodes, a node may detect failure while fewer than half of the failed node's neighbors remain reachable; taking over in that case can leave CAN state inconsistent, so the node first performs an expanding-ring search before triggering takeover. The topologically-sensitive construction (landmark ordering) unevenly populates the coordinate space, raising load on nodes in bins corresponding to common landmark orderings. Large-scale experiments (hundreds of thousands of nodes) were judged too difficult to run physically, so all reported scaling results come from simulation, not a deployed system.

### Requirements it places on the rest of the system
Requires a uniform hash function mapping keys to points in the d-dimensional coordinate space, available to every node. Requires a bootstrap mechanism supplying a new node with the IP address of at least one existing CAN node (the paper assumes, as in prior work, an associated DNS mechanism for this). Requires nodes to send periodic soft-state update messages to their immediate neighbors carrying their own zone coordinates and neighbor list; the prolonged absence of updates is the sole failure-detection signal, so the mechanism assumes the update interval is short relative to the node-departure and node-failure rate the deployment expects. RTT-weighted routing requires each node to measure round-trip time to its neighbors, which requires periodic bidirectional probing. Landmark-based topological construction requires a well-known, globally reachable set of landmark machines that every joining node can probe. Replication across multiple realities or multiple hash functions requires the application to accept a k-fold or r-fold increase in per-node storage and, for parallel queries, in query traffic.

### Contradicts
None found.

### References worth retrieving
- Plaxton, Rajaraman, Richa, "Accessing nearby copies of replicated objects in a distributed environment," ACM SPAA 1997 — foundational (basis for the OceanStore/Tapestry O(log n)-hop, O(log n)-state routing family the paper compares CAN against).
- Karp, Kung, "Greedy Perimeter Stateless Routing," ACM MOBICOM 2000 — foundational (geographic routing precedent for CAN's coordinate-space greedy forwarding).
- Kubiatowicz, Bindel, Chen, Czerwinski, Eaton, Geels, Gummadi, Rhea, Weatherspoon, Weimer, Wells, Zhao, "OceanStore: An Architecture for Global-scale Persistent Storage," ASPLOS 2000 — competing (uses the Plaxton algorithm as its data-location scheme; the paper directly contrasts CAN's O(dn^(1/d)) routing and O(d) state against Plaxton's O(log n) routing and O(log n) state).
- Clarke, Sandberg, Wiley, Hong, "Freenet: A Distributed Anonymous Information Storage and Retrieval System," ICSI Workshop on Design Issues in Anonymity and Unobservability, 2000 — competing (contrasted as a system where content may not be found even with every node behaving correctly, unlike CAN's guaranteed "home" location).
- Waldman, Rubin, Cranor, "Publius: A Robust, Tamper-evident, Censorship-resistant, Web Publishing System," 9th USENIX Security Symposium, 2000 — competing (assumes a static system-wide server list; the paper proposes CAN's self-organization as a complementary extension).
- Stoica, Morris, Karger, Kaashoek, Balakrishnan, "Chord: A scalable content-addressable network," ACM SIGCOMM 2001 — competing (contemporaneous ring-geometry DHT).

### Verbatim extracts
- "we can route with a latency that is well within a factor of two of the underlying network latency" (n = 262,144 nodes, knobs-on-full).
- "designing a secure CAN that is resistant to denial of service attacks" is called "a particularly hard problem."
- "a malicious node can act, not only as a malicious client, but also as a malicious server or router."
- "landmark ordering is work in progress which we do not discuss further (nor make use of) in this paper."
