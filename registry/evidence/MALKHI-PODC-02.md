## [MALKHI-PODC-02] Viceroy: A Scalable and Dynamic Emulation of the Butterfly

**Citation:** Dahlia Malkhi, Moni Naor, David Ratajczak. "Viceroy: A Scalable and Dynamic Emulation of the Butterfly." ACM PODC, 2002. DOI 10.1145/571825.571857.
**Retrieved:** full text via https://www.wisdom.weizmann.ac.il/~naor/PAPERS/viceroy.pdf
**Source URL:** https://www.wisdom.weizmann.ac.il/~naor/PAPERS/viceroy.pdf
**Domain:** A

### What it does
Viceroy locates data in a distributed hash table (DHT) while every server keeps a constant number of outbound links, so a server join or departure changes a constant number of links in expectation regardless of how many servers are in the network. It achieves this by having each server emulate one node of a butterfly network — a fixed interconnection pattern in which nodes are arranged in levels and each non-leaf node at level L connects down to two nodes at level L+1 and up to one node at level L-1.

Each server picks two values at join time: an identifier drawn independently and uniformly from the real interval [0,1), fixed for the server's lifetime, and a level, a positive integer chosen by a local estimation procedure (below). Three link sets connect servers: a general ring linking each server to its ring successor and predecessor by identifier order; a level ring linking servers that share the same level; and butterfly links — each server's "left down" link goes to the first level-L+1 server clockwise from its own identifier, its "right down" link goes to the first level-L+1 server clockwise from identifier + 1/2^L, and its "up" link goes to the first level-L-1 server clockwise from its own identifier.

A server estimates the network size n locally, without any global count, by taking the reciprocal of the ring distance to its immediate successor (1/d(s, succ(s))) as an estimate n0, then draws its level uniformly from [1, floor(log n0)]. This keeps level assignment self-adjusting to local density without communicating n to any server.

Lookup for target identifier x, starting at server y, runs in three phases: follow up-links to a level-1 root server; descend butterfly links, at each level-L server moving to the right-down link if the target is at ring distance >= 1/2^L and to the left-down link otherwise, until reaching a server with no further down link or one that overshoots the target; then traverse the general ring (clockwise or counter-clockwise) to the closest server to x. An improved third phase ("hopping," Section 7) interleaves level-ring links with ring links instead of stepping server-by-server, so the worst-case path length becomes logarithmic with high probability rather than only in expectation.

A background "bucket" mechanism (sketched, not fully specified) partitions the ring into contiguous groups of Theta(log n) servers each and reassigns levels within a bucket so every level from 1 to log n has at least one and at most a constant number of representatives per bucket, which bounds the largest number of incoming links any single server can receive.

### Measured results
None. The paper is a theoretical construction with worst-case and expected-case bounds proved as theorems; it contains no implementation, simulation, or empirical measurement. Every quantitative claim below is an asymptotic bound with a proof, not a measured figure, and is reported here as a stated bound, not a measurement, per Rule 1.

Stated asymptotic properties, each proved for a Viceroy network holding n servers, under the paper's own assumptions (see Requirements below):
- Out-degree of every server: 7 total (5 used in the simple, non-hopping lookup variant) (Theorem 6.6).
- Expected in-degree: O(1); largest in-degree: O(log n) with high probability, over the randomness of identifier and level choice (Theorem 6.6).
- Lookup path length (dilation): O(log n) in the worst case, with high probability, using the improved ("hopping") third-phase routing of Section 7 (Theorem 7.3). The simple lookup variant (Section 6) achieves O(log n) dilation only in expectation, not with high probability, because the ring-traversal third phase can pass through as many as O(log^2 n) servers in the worst case.
- Load per server (fraction of all-pairs lookups passing through a given server): expected O(log n / n); maximum over all servers, O(log^2 n / n) with high probability (Theorem 6.4).
- Join or leave cost: a constant number of link changes in expectation, and O(log n) link changes with high probability, per join or leave event.
- Bucket-mechanism overhead: a server leaving causes at most O(1) other servers to change level; a bucket reshuffle (triggered once every (c-1) log n steps for a paper-unspecified constant c) touches O(log n) servers, giving amortized O(1) per join/leave.

Table 1 (reproduced from the paper, comparing dilation / congestion / linkage cost against the schemes it cites): Chord — log n / (log n)/n / log n. Tapestry — log n / (log n)/n / log n. Content Addressable Network (CAN) with d dimensions — d*n^(1/d) / d*n^(1/d-1) / d. Kleinberg-style Small Worlds — log^2 n / (log^2 n)/n / O(1). Viceroy is the paper's proposed alternative to this table, trading Small Worlds' O(1) linkage cost for O(log n) dilation and O(log n) linkage cost at constant, not logarithmic, out-degree.

### Parameters
- Server identifier: drawn uniformly and independently from the continuous interval [0,1); in practice, a fixed number of random bits sufficient to make identifier collisions implausible (exact bit count not stated as a number, left to implementation).
- Level: integer in [1, floor(log n0)], n0 the server's local size estimate; redrawn only when floor(log n0) changes, per a footnote optimization, not on every join/leave elsewhere in the network.
- Bucket size: Theta(log n) servers; a bucket merges with a neighbor when its size drops below log n and splits when its size exceeds c*log n, for an unspecified constant c bounding the diversity property (at most c servers per level per bucket).
- Out-degree: fixed at 7 (2 down, 1 up, 2 ring — general successor/predecessor, 2 level-ring — next/prev on level); only 5 of the 7 links are used by the simple (non-hopping) lookup.

### Stated limitations
The paper explicitly excludes concurrent joins and leaves and server failures from its model: it assumes multiple join and leave operations do not overlap and that servers never fail, and refers the reader to a separate paper (Lynch, Malkhi, Ratajczak, IPTPS 2002) for concurrency and failure handling. It does not address load hotspots — repeatedly requested identifiers overloading the servers along the corresponding lookup paths — though it states in a footnote that standard replica-placement mechanisms could be adapted to the DHT framework without demonstrating this. It assumes joins and leaves are independent of server identifiers, so the active server set stays randomly distributed on the ring; a correlated join/leave pattern is outside the analysis. It does not specify how a client or a joining server obtains the address of any already-active server (bootstrap discovery is out of scope). The bucket mechanism that bounds maximum in-degree is only sketched, not fully specified or analyzed to the same rigor as the base construction, by the authors' own statement.

### Requirements it places on the rest of the system
- Requires that any server able to compute another server's identifier can open a connection to it; the paper treats connection establishment as a primitive and does not specify addressing, transport, or NAT traversal.
- Requires non-overlapping join/leave events (a serialization or locking discipline elsewhere in the system) for the join/leave algorithms and their O(1)-expected-link-change bound to apply as proved; concurrent joins/leaves are explicitly out of scope and left to a different mechanism.
- Requires a failure-free server population for the bounds as proved; crash tolerance is not part of this construction.
- Requires the level-selection procedure's local density estimate (1/d(s, succ(s))) to be accurate, which in turn requires identifiers to remain uniformly distributed on the ring — violated if join/leave is correlated with identifier choice (e.g., an adversary choosing identifiers to cluster in one region).
- Requires a separate bootstrap mechanism to supply a joining server or client with the address of one already-active server.
- Requires a separate mechanism (unspecified) to handle hotspots if uneven query popularity across identifiers is expected, since the load bound (Theorem 6.4) is an average over a uniform query distribution.

### Contradicts
None found. No other paper in this corpus's current batch measures Viceroy independently.

### References worth retrieving
- Foundational: I. Stoica, R. Morris, D. Karger, M. F. Kaashoek, H. Balakrishnan, "Chord: A scalable peer-to-peer lookup service for Internet applications," SIGCOMM 2001 — the O(log n)-degree comparison point in Table 1.
- Foundational: B. Y. Zhao, J. D. Kubiatowicz, A. D. Joseph, "Tapestry: An infrastructure for fault-tolerant wide-area location and routing," UC Berkeley TR UCB/CSD-01-1141, 2001.
- Competing: S. Ratnasamy, P. Francis, M. Handley, R. Karp, S. Shenker, "A scalable content-addressable network," SIGCOMM 2001 — the constant-degree CAN alternative directly compared in Table 1.
- Competing: C. Plaxton, R. Rajaram, A. Richa, "Accessing nearby copies of replicated objects in a distributed environment," SPAA 1997 — the randomized-hypercube routing scheme Tapestry is built on, compared in the related-work section.
- Foundational: J. Kleinberg, "The small world phenomenon: An algorithmic perspective," STOC 2000 (also Nature 406, 2000) — the Small Worlds row of Table 1.
- Foundational: N. Lynch, D. Malkhi, D. Ratajczak, "Atomic Data Access in Distributed Hash Tables," IPTPS 2002 — cited by the authors as the paper handling concurrency and failures that this paper's model excludes.
- Foundational: G. Pandurangan, P. Raghavan, E. Upfal, "Building low-diameter p2p networks," FOCS 2001.
- Foundational: W. Pugh, "Skip Lists: A probabilistic alternative to balanced trees," Communications of the ACM 33(6), 1990.

### Verbatim extracts
- "the addition or removal of a node to the network requires no global coordination, only a constant number of linkage changes in expectation"
- "the out-degree of each node is 7 (only 5 of which are used in the simple version)"
- "for any server the expected load is O((log n)/n) and w.h.p. the maximum load on all servers is O((log2 n)/n)"
- "the (worst-case) dilation of the network is O(log n) w.h.p."
- "we assume that multiple join and leave operations do not overlap, and servers never fail"
- "This paper does not address the issue of hotspots"
