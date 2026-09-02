## [COHEN-SIGCOMM-02] Replication Strategies in Unstructured Peer-to-Peer Networks

**Citation:** Edith Cohen, Scott Shenker. "Replication Strategies in Unstructured Peer-to-Peer Networks." ACM SIGCOMM, 2002. DOI 10.1145/633025.633043.
**Retrieved:** full text via https://www.csl.mtu.edu/cs6461/www/Reading/Cohen02.pdf
**Source URL:** https://www.csl.mtu.edu/cs6461/www/Reading/Cohen02.pdf
**Domain:** B

### What it does
The paper determines how many copies of each data item a peer-to-peer (P2P) network should hold, given a fixed total storage budget, to minimize the number of nodes a blind random search must probe before finding an item. It models search as random probing: a search draws nodes uniformly at random and stops when one holds a copy of the queried item, so the expected number of nodes probed for item i (the expected search size) is inversely proportional to the fraction of total system capacity allocated to item i. Node capacity per peer is fixed at rho copies; total system capacity is R = n*rho for n nodes; item i receives p_i = r_i/R of that capacity, where r_i is its copy count. The paper proves that among all allocations lying between two named baselines, "Uniform" (equal copies per item, independent of demand) and "Proportional" (copies proportional to query rate q_i), every allocation strictly between them has a strictly lower expected search size than either baseline, and both baselines produce the identical expected search size m/rho (m = number of distinct items), independent of the query distribution. It then derives the allocation that minimizes expected search size: Square-root allocation, p_i proportional to sqrt(q_i), and gives three distributed algorithms that converge to it without any node needing to know the global query-rate distribution.

### Measured results
| Result | Conditions |
|---|---|
| Gain factor of Square-root over Uniform/Proportional scales as: constant for skew w<1, logarithmic in m for w=1, polynomial in m for 1<w<2, linear in m for w>2 | Derived analytically (Table 1) for truncated Zipf-like query distributions on m items, query rate of the i-th most popular item proportional to i^-w |
| Maximum gain factor of the optimal two-item allocation over Uniform or Proportional is 2 | Analytic result for m=2 items, rho=1 |
| Square-root allocation's expected search size (ESS) is 30%-50% of Proportional's/Uniform's ESS for larger m | Two query distributions built from Boeing Web proxy logs: top-m URLs weighted by request count, and top-m hostnames weighted by number of distinct requesting users |
| Under the hostname distribution, the maximum search size required by Square-root is within a factor of 2 of the minimum possible (achieved by Uniform), while Proportional requires a substantially larger maximum search size | Boeing proxy log hostname distribution, m=1000 locatable items |
| Sibling-number-memory (SNM) distributed replication algorithm converges to Square-root allocation faster than path replication and is insensitive to delay between a search and follow-up copy creation; path replication converges more slowly and can fluctuate when queries arrive in bursts or copy-creation delay is large relative to query rate | Simulated network of 10,000 nodes, tracking the fraction of nodes holding a copy of one item over time; searches stop after finding k copies, k in {1, 5}; fixed copy lifetime; queries at fixed intervals; some runs add delay between search and follow-up copy generation (Figures 6-7, no numeric summary table given in text) |

### Parameters
- rho: per-node capacity (number of item copies/keys a node can hold); held symbolic throughout the analysis, set to 1 in the two-item numeric example (Figure 1B)
- ℓ (lower bound on p_i, from r_i >= 1): ℓ = 1/R
- u (upper bound on p_i, from r_i <= n): u = rho^-1 = n/R
- Truncated-search parameter L (maximum search size before a query is declared insoluble): failure probability bounded by 2^-C when p_i >= C/(rho*L); the paper sets C = O(log L) so failure probability is polynomially small in L
- fs (fraction of soluble queries) / (1-fs) (fraction of insoluble queries): used to weight the combined cost fs*A_q(p) + (1-fs)*L(p); swept in the hostname-distribution figure (0%, 25%, 50%, 75%, 100% soluble)
- Zipf skew parameter w: swept across w<1, w=1, 1<w<2, w=2, w>2 in the analytic gain-factor table
- Simulation: 10,000 nodes; k (copies to find before stopping search) in {1, 5}; fixed copy lifetime duration (value not stated numerically in the retrieved text); queries issued at fixed intervals

### Stated limitations
The analysis assumes an adaptive termination search mechanism (search stops once the query is resolved) and states that a different question -- replication without adaptive termination -- is addressed elsewhere (reference [7], Kangasharju/Ross/Turner). The distributed replication algorithms are proved to converge to Square-root allocation only under a stated deletion-process assumption: copy lifetimes are independent of the item's identity and survival probability is non-increasing with age; the paper states this assumption is violated by Least Recently Used (LRU) and Least Frequently Used (LFU) eviction, though satisfied by First In First Out (FIFO), fixed lifetime durations, and random deletion. Path replication is stated to have a convergence weakness: the number of copies created per search can overshoot or undershoot the fixed point by a large factor when queries arrive in bursts or when the delay between a search and its follow-up copy creation is large relative to the query rate, and the paper states this issue can occur even for a large number of nodes. The paper states an open issue: how the proposed distributed algorithms behave in more realistic settings than the model and simulations cover.

### Requirements it places on the rest of the system
The distributed replication algorithms require that copy deletion be independent of which item is stored and of that item's access pattern -- an eviction policy that instead prunes least-recently-used or least-frequently-used copies breaks the fixed point the algorithms converge to, because it makes deletion rate depend on query rate. Path replication and sibling-number memory both require the requesting node, after a successful search, to know which item was found, so it can create new copies of that specific item at randomly selected nodes; the number of new copies created (path replication: the search size; sibling-number memory: an estimator built from recorded sibling-copy counts and ages) is a function of the search outcome for that item. Probe memory requires every node to record, per item, the count and combined search-size total of every probe it has seen for that item within a recent time window, and requires nodes to aggregate this bookkeeping across the nodes on a search path. The two-tier optimal policy (mixing Square-root with a Uniform floor) requires designating a subset of permanent-copy nodes per item that never evict that copy except on going offline, coordinated with a maximum search size L chosen jointly with that floor.

### Contradicts
None found against other entries in this batch. The paper's own numbers push back against the common attribution of "Proportional replication is close to optimal" -- the paper states Proportional is one of the two worst points among the family of allocations it studies (Lemma 3.1, Theorem 3.1), matched only by Uniform.

### References worth retrieving
- Lv, Cao, Cohen, Li, Shenker. "Search and replication in unstructured peer-to-peer networks." ICS 2002. -- foundational (already in corpus as the companion implementation paper; this paper's [9])
- Kangasharju, Ross, Turner. "Optimal content replication in P2P communities." Manuscript, 2002. -- competing (addresses replication without adaptive termination, a variant this paper explicitly excludes)
- Ratnasamy, Francis, Handley, Karp, Shenker. "A scalable content-addressable network." SIGCOMM 2001. -- foundational (structured-overlay contrast)
- Stoica, Morris, Karger, Kaashoek, Balakrishnan. "Chord: A scalable peer-to-peer lookup service for internet applications." SIGCOMM 2001. -- foundational (structured-overlay contrast; already in corpus as STOICA-SIGCOMM-01)
- Rowstron, Druschel. "Storage management and caching in PAST, a large-scale, persistent peer-to-peer storage utility." SOSP 2001. -- competing (alternative storage-replication design)
- Zhao, Kubiatowicz, Joseph. "Tapestry: An infrastructure for fault-tolerant wide-area location and routing." UCB/CSD-01-1141, 2001. -- foundational
- Kleinrock. "Queueing Systems, Volume II: Computer Applications." Wiley-Interscience, 1976. -- foundational (source of the capacity-assignment optimization the Square-root proof reuses)
- Vaidya, Hameed. "Scheduling data broadcast in asymmetric communication environments." ACM/Baltzer Wireless Networks 5, 1999. -- foundational (source of the same optimization problem in a broadcast-scheduling context)

### Verbatim extracts
"the two replication strategies have the same expected search size A = m/rho"
"Square-root allocation, when defined, minimizes the expected search size"
"one of these algorithms, path replication, is implemented, in a somewhat different form, in the Freenet P2P system"
"Two common policies, Least Recently Used (LRU) or Least Frequently Used (LFU) are inconsistent with our assumption"
"the sibling-memory algorithm arrives more quickly to Square-root allocation and also is not sensitive to delayed creation of followup copies"
"Our analysis assumes adaptive termination mechanism, where the search is stopped once the query is resolved"
