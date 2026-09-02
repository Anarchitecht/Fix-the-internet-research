# Conflicts

Four kinds, kept apart.

The contradiction pass read the completed evidence corpus and compared every figure for each quantity
across every paper reporting it. Twelve agents each took one quantity family or the requirements
index. They examined 39 candidate disagreements.

**Exactly one is a disagreement between two papers measuring the same quantity under the same
conditions. The other 38 are not disagreements at all** — the two papers measure different
populations, different operations, or the same thing by methods whose results do not compare. Calling
those contradictions would be an error. So is citing either figure of such a pair as though it were
the quantity.

The pass also found 22 requirements that another mechanism removes, 11 figures attributed to papers
whose own text does not contain them, and 7 papers whose abstract and body disagree.

---

## The one genuine disagreement: whether a published attack on Argon2i matters at the parameters the standard recommends

**Quantity.** Practical severity of the Alwen-Blocki depth-reducing-set tradeoff attack against Argon2i-B at 1 GB of memory (whether it reduces adversary cost below the honest cost within the IRTF-recommended parameter range)

**`BIRYUKOV-EUROSP-16`** — Time-area advantage smaller than 1 (no benefit to attacker) for memory up to 2^20 (1 GB), smaller than 2 up to 16 GB; states this 'is not better than the ranking attack.' Derived analytically by applying the Alwen-Blocki 2016 paper's own published closed-form time-area formula directly to Argon2's parameters -- no simulation, no attack implementation.

**`ALWEN-EUROSP-17`** — 'At tau=6 passes over 1GB of memory the attack already reduces costs by a factor of 2' -- inside the same parameter range (1 GB, up to 16 GB, IRTF-recommended 'paranoid' pass count) that BIRYUKOV-EUROSP-16 treats as safe. Measured by simulating the attack on randomly sampled Argon2i-B DAGs (10 samples per point), adding a smaller depth-reducing-set construction and an 'XOR compression' heuristic absent from the 2016 formula, plus a bounded-parallelism analysis.

**Which figure a decentralized deployment should plan against.** ALWEN-EUROSP-17's figure: it is a demonstrated attack instantiation run directly against the IRTF's own recommended deployment parameter (1 GB, up to 6 passes), not an asymptotic bound extrapolated from a weaker, non-heuristic attack instantiation. BIRYUKOV-EUROSP-16's safety conclusion rests on that weaker instantiation and does not model the heuristics that later closed the gap; a deployment choosing parameters from the analytic bound alone would understate its real exposure.

This is the only place in 407 papers where two authors measured the same thing the same way and got
answers a designer must choose between. Everywhere else the corpus is consistent once conditions are
stated.

---

## The 38 apparent disagreements that are not

The recurring shapes, each of which a synthesis must state rather than average:

- **Different populations of the same network.** Counting nodes a curated bootstrap list serves gives
  about 6,000 for a network a routing-table crawl measures at about 223,000.
- **Simulation against live implementation.** The same padding defense measures 196% bandwidth
  overhead in simulation on a closed-world dataset and 121% via a real pluggable transport on live
  traffic.
- **A system's own measurement against a competitor's re-implementation.** One private-search system
  reports 56.9 MiB of communication over 364 million documents on a 45-machine cluster; a competitor
  reports 17.4 MB per query for the same system on a 3.2-million-passage corpus on one 6-core machine.
  Both are honest. Neither is "that system's performance."
- **Different evidentiary thresholds.** Two studies of carrier-grade address translation differ about
  sixfold because one requires a directly observed leaked internal address and the other fits a
  behavioural score to a threshold.
- **Different modelled regimes.** Two storage papers reach opposite conclusions about whether durable
  wide-area storage on unreliable participants is feasible, because one models continual membership
  turnover and the other models comparatively stable membership where loss comes from disk failure.

---

## 22 requirements that another mechanism removes

Each states the requirement, what removes it, and the resolution: change a selection, accept a stated
degradation, or record an open problem. An unresolved conflict left without one of those three is a
defect.

### 1. The querier must be able to observe lookup progress hop by hop (each hop reports the next hop back to the querier) so a non-converging, misdirected lookup can be detected.

**Required by** `SIT-IPTPS-02` · **removed by** `HEEP-ATNAC-10`

SIT-IPTPS-02 states this check is enforceable only under iterative routing and is impossible under recursive forwarding. HEEP-ATNAC-10's R/Kademlia gets its entire measured latency/bandwidth advantage over iterative Kademlia (~225 ms vs ~415 ms mean latency with PNS enabled) from switching to recursive routing, under which, in the paper's own words, 'the initiator loses control of the message after the first hop' -- exactly the control SIT-IPTPS-02's principle requires the querier to keep.

**Resolution.** Keep iterative routing and accept R/Kademlia's slower, higher-bandwidth churn behavior; adopt recursive routing and substitute CASTRO-OSDI-02's statistical routing-failure test plus redundant neighbor-set-anycast routing (>99.9% success at up to 30% malicious nodes, N=100,000) in place of Sit's per-hop check; or record the tension as an open problem, since HEEP-ATNAC-10 is a pure performance paper with no adversarial model of its own.

### 2. A churn model whose analytical/simulated conclusions hold under the actual distribution of peer session lengths in the deployed population being reasoned about.

**Required by** `RHEA-USENIXATC-04` · **removed by** `STUTZBACH-IMC-06`

RHEA-USENIXATC-04's Bamboo-vs-FreePastry-vs-Chord churn-handling results, reactive/periodic-recovery comparison, and timeout-calculation comparison are all produced under a Poisson (memoryless, exponential) node-death model, which the paper's own limitations section calls a simplification of real churn. STUTZBACH-IMC-06 measures real session lengths across 5 Gnutella, 4 Kad, and 3 BitTorrent datasets and finds they fit Weibull distributions with shape parameters below 1, not exponential; its own text states directly that 'a component that assumes session lengths are exponentially or Poisson-distributed ... is contradicted by this paper's fitted Weibull/log-normal distributions,' and names RHEA-USENIXATC-04 by title in its bibliography as a paper whose assumed churn model its measurements can validate or contradict.

**Resolution.** Re-run RHEA-USENIXATC-04's churn experiments under a measured Weibull churn distribution, as HEEP-ATNAC-10 already does (adopting Stutzbach's own k=0.5 Weibull model) for its own recursive-routing comparison; or treat RHEA-USENIXATC-04's specific churn-rate thresholds as qualitative rather than quantitatively transferable; or flag the gap as an open problem for any design selecting Bamboo-style reactive recovery.

### 3. Square-root replication (and its rank-aware extension) requires the node that receives a search result to learn which specific item was found -- and, for the rank-aware policy, at what rank -- so it can create new copies

**Required by** `COHEN-SIGCOMM-02 (extended by RICHARDSON-ECIR-13 to also require rank position)` · **removed by** `ZHOU-EPRINT-24`

Pacmann's private-information-retrieval-based approximate-nearest-neighbor search is built so the server 'cannot infer the query's topic from access patterns' -- the node playing the forwarder/storage role never learns which item a query touched, by design, regardless of what the client later does with the result. A node built to this specification cannot supply the identity-of-found-item signal square-root replication needs.

**Resolution.** Restrict search-driven replication to search mechanisms that do not hide result identity from the forwarding node, and offer PIR-protected search only for content that is replicated by some other trigger (e.g., publisher-driven or popularity-estimated-out-of-band replication, not search feedback); or accept that PIR-protected search and search-driven square-root replication cannot compose for the same content class and select one property per content type; or record as an open problem, since ZHOU-EPRINT-24 supplies no reconciliation -- it does not implement replication at all.

### 4. DistributedANN's near-data node-scoring service requires the operator to control code placement on every storage host, so scoring computation can be co-located with the storage host under one trust domain.

**Required by** `ADAMS-ARXIV-25` · **removed by** `DANEZIS-WALRUS-25`

ADAMS-ARXIV-25 states directly that 'a system without control over storage-host code placement (as in an untrusted peer storage layer) could not deploy the near-data scoring service as described,' and its threat model assumes a single trusted operator with no defense against a corrupted storage host. DANEZIS-WALRUS-25's Walrus storage design tolerates up to n/3 Byzantine (malicious) storage nodes by construction, meaning no single operator is assumed to control what code those nodes run.

**Resolution.** Select a vector-search mechanism compatible with an untrusted storage layer (none evaluated in this corpus family) instead of DistributedANN's near-data scoring; or run DistributedANN's scoring service only on a trusted-operator subset of storage nodes, which narrows decentralization for that subset and needs its own justification; or record as an open problem for vector/approximate-nearest-neighbor search specifically, distinct from the general PIR-vs-replication conflict above.

### 5. At least one of a small, fixed set of relay/mix servers must be honest and independently operated (Vuvuzela: 'at least one honest server' for the whole chain; Riposte: no two of three servers collude; Stadium: at least o

**Required by** `VANDENHOOFF-SOSP-15` · **removed by** `DOUCEUR-IPTPS-02`

DOUCEUR-IPTPS-02 proves (Lemma 2) that absent a logically centralized identity-issuing authority, a single faulty entity can present an unbounded number of distinct identities when identities are not challenged in a synchronized round, and (Lemma 1) a number proportional to its own resource advantage otherwise. An open, permissionless peer population — the kind this brief's architecture specifies for identity, indexing, and storage — gives no selection process a way to confirm that a small chosen server set is operated by genuinely independent parties, or that any two of them are not colluding. VANDENHOOFF-SOSP-15 states its own security proof is conditioned on this one-honest-server assumption existing and supplies no mechanism to enforce it; CORRIGANGIBBS-SP-15 states its scheme 'provides no mechanism to enforce or detect collusion' among its own three servers; the same requirement recurs, unmet, in TYAGI-SOSP-17, LAZAR-OSDI-18, and CHENG-ACSAC-20.

**Resolution.** Staff the server roles through an admission-controlled, identity-vetted process for this one privacy tier (a stated departure from full permissionlessness, not left implicit); or record the anytrust/non-collusion assumption as an open problem for a fully open peer population and offer the tier only where a curated operator set already exists; or select a different privacy mechanism for that tier that does not require a small non-colluding server set.

### 6. Loopix/Nym's cover-traffic-efficient anonymity growth with user count requires a stratified (layered) topology in which independent routes through different mixes intersect into one shared anonymity set

**Required by** `PIOTROWSKA-USENIXSEC-17` · **removed by** `PIOTROWSKA-WPES-21`

PIOTROWSKA-WPES-21 states directly that reproducing the Nym-favorable anonymity result 'requires a stratified topology with intersecting routes across layers... a P2P topology (as in HOPR)... does not produce this property in the simulator,' and then measures the P2P case under the same simulator, same per-node processing capacity, and same per-hop delay model as the stratified case: HOPR's anonymity (entropy) stays low and nearly flat as users scale from 10^2 to 10^5, and reaching a higher level requires cover-to-real traffic ratios up to 10:1, at which point it still stays below what the stratified design reaches with far less cover traffic. A flat, undifferentiated peer mesh — the topology a fully decentralized relay layer without role differentiation produces — removes the path-intersection property the stratified design's cover-traffic economics depend on.

**Resolution.** Adopt a stratified/cascade topology for this tier, accepting that layer or provider roles are a form of peer-role differentiation (which reopens the same Sybil/curation question as the anytrust finding above); or accept the measured cover-traffic cost of a flat P2P mesh (up to 10:1, and even then below Nym's anonymity level) and state it as the tier's quantified price; or record as an open problem, since no entry in this corpus measures a mix design reaching Loopix/Nym-class anonymity-per-cover-traffic-byte in a genuinely flat P2P topology.

### 7. The non-Sybil region must be well-connected, non-bipartite, and fast-mixing relative to the full graph, with Sybils limited in the attack edges they can form into it.

**Required by** `CAO-NSDI-12` · **removed by** `GAO-CNS-18`

GAO-CNS-18 measures a real 21,297,772-node, 265,025,545-edge Twitter graph with benign/Sybil-partition modularity of 0.0042 (Clauset et al.'s cited threshold for detectable community structure is 0.3), 18,414,469 attack edges of which 90% concentrate on 3% of benign nodes, and 50% of Sybils isolated rather than clustered. Under these measured conditions SybilRank (SR) reaches only 0.57 AUC, barely above the 0.5 random baseline.

**Resolution.** Restrict SybilRank to sub-graphs first shown to be low-modularity and fast-mixing (as CAO-NSDI-12's own Louvain-seeded Tuenti deployment did), accept near-random ranking on open-follow graphs shaped like Twitter, or select a mechanism not conditioned on this precondition (e.g. the local-classifier hybrid GAO-CNS-18 itself proposes, SybilFuse).

### 8. Random-walk length must be set from the honest region's true mixing time, assumed short (O(log n)) and instantiated as 10-20 hops.

**Required by** `YU-SIGCOMM-06, YU-SP-08, DANEZIS-NDSS-09, LESNIEWSKI-LAAS-NSDI-10, LESNIEWSKI-LAAS-SNS-08` · **removed by** `MOHAISEN-IMC-10`

MOHAISEN-IMC-10 directly measures mixing time (walk length to reach total variation distance 0.1) on real social graphs and finds 100-400 hops needed for DBLP/YouTube/Facebook and 1,500-2,500 for LiveJournal -- one to two orders of magnitude longer than the 10-15-hop lengths those five papers' own evaluations used. Re-implementing SybilLimit itself, it finds the walk length needed to admit nearly all honest nodes is 'larger, and the resulting variation-distance quality worse,' than SybilLimit's published lengths, and states Whanau's own mixing-time validation is 'only circumstantial.'

**Resolution.** Measure the deployment graph's actual mixing time before fixing a walk length and pay the resulting bandwidth/latency cost (two orders of magnitude longer), or select a mechanism not conditioned on fast mixing (e.g. HEEB-ARXIV-24's graph-attention approach, which explicitly claims no fast-mixing or bounded-attack-edge requirement).

### 9. Sybils must accumulate a higher rejected-to-accepted friend-request ratio than real users, exposing a sparse or negative cut toward the Sybil region, with attack edges bounded.

**Required by** `SUN-ASONAM-20` · **removed by** `WEI-INFOCOM-12`

WEI-INFOCOM-12's own 214-respondent Mechanical Turk survey of self-rated Facebook friend lists measures an average 19.8% of relations rated 'Stranger,' and cites an independent finding (Bilge et al.) that roughly 20% of bogus friend requests on Facebook are accepted -- both measuring a real acceptance rate of low-value or bogus connections far above what a bounded-attack-edge, sparse-cut assumption tolerates.

**Resolution.** Add an explicit relationship-rating or interaction-derived edge filter before the graph reaches TrustGCN (as WEI-INFOCOM-12 itself proposes but does not enforce), accept the resulting reduced graph density, or select a mechanism that does not depend on Sybils showing a distinguishable rejection signature.

### 10. Integro's proved security bound (Theorem 4.1) requires attack edges placed uniformly at random against a fast-mixing real region.

**Required by** `BOSHMAF-NDSS-15` · **removed by** `GAO-CNS-18`

GAO-CNS-18 measures a real Twitter graph in which 90% of the 18,414,469 attack edges concentrate on just 3% of benign nodes -- a heavily non-uniform distribution -- and independently re-implements Integro (INT) on that graph, measuring AUC 0.48, with the perfect-victim-predictor variant (INT-PF) at only 0.54, because Integro's edge-downweighting formula suppresses propagation broadly once the true victim fraction (measured at 75.4% of benign nodes) is this high, regardless of classifier accuracy.

**Resolution.** Restrict Integro to deployments where attack-edge placement can be shown close to uniform random (Tuenti-shaped, invitation-gated graphs), add a defense against concentrated celebrity-node targeting, or accept that Integro's 95% Tuenti precision figure does not transfer to an open-follow graph.

### 11. A social-graph Sybil defense's accuracy depends on the honest periphery not itself being densely clustered and separated from the graph core by a small cut (fast-mixing / sparse-cut assumption).

**Required by** `YU-SIGCOMM-06, YU-SP-08, DANEZIS-NDSS-09, WEI-INFOCOM-12, CAO-NSDI-12` · **removed by** `VISWANATH-SIGCOMM-10`

VISWANATH-SIGCOMM-10 measures a -0.81 correlation between social-graph modularity and detection accuracy (A') across 8 real datasets (modularity 0.278 to 0.79), and separately shows accuracy falling below 0.5 (Sybils ranking above honest nodes) on a real Facebook graph once an adversary targets attack edges near the trust seed rather than placing them randomly -- holding for all four schemes tested (SybilGuard, SybilLimit, SybilInfer, SumUp) and for community detection substituted for each.

**Resolution.** Measure the deployment graph's modularity and its exposure to seed-targeted attacks before choosing a fast-mixing-dependent defense, restrict the defense to sub-communities already shown low-modularity, or select a defense not dependent on global fast-mixing/low-modularity structure.

### 12. TreeKEM's formal non-adaptive CGKA security proof (Theorems 1 and 2) requires the delivery mechanism to deliver CGKA protocol messages in the same order to every member within one session -- a consistent per-session tota

**Required by** `ALWEN-CRYPTO-20` · **removed by** `BEURDOUCHE-RFC-25`

BEURDOUCHE-RFC-25, MLS's own architecture RFC, explicitly authorizes an Eventually Consistent Delivery Service -- naming a distributed peer-to-peer message-broadcast mechanism directly -- as one of MLS's two supported deployment architectures, under which different clients may observe multiple concurrent Commits for the same epoch in different orders before a client-side deterministic tie-break reconciles them. ALWEN-CRYPTO-20's own Section 8.3 attack sketch shows that exactly this condition (two tree-sibling members processing concurrent updates under an unordered network) lets a leaked state from one sibling recover a group key the honest protocol did not expect that party to compute, breaking even the paper's weakest (passive) security guarantee for every TreeKEM variant the authors are aware of.

**Resolution.** (a) Restrict the deployment to BEURDOUCHE-RFC-25's Strongly Consistent Delivery Service option, giving up the partition tolerance the Eventually Consistent option otherwise offers. (b) Accept the exposure window during the unreconciled period between concurrent Commits as a stated, uncorrected security gap -- neither RFC engages with ALWEN-CRYPTO-20's specific attack. (c) Select a CGKA construction whose security proof targets this setting directly rather than retrofitting a total-order-based proof onto a partition-tolerant delivery layer, e.g. YEN-EPRINT-26 (BeeKEM), proved over causally-ordered broadcast, at the cost of BeeKEM's own weaker, parameterized forward-secrecy notion (kappa-FSU/kappa-CFS) rather than the property ALWEN-CRYPTO-20 targets.

### 13. A QUIC-based hole-punch restoration mechanism that skips re-punching after an address change needs both peers' QUIC stacks to support and permit connection migration -- to offer a spare Connection ID and answer a PATH_CH

**Required by** `LIANG-ARXIV-24` · **removed by** `BUCHET-CCR-25`

BUCHET-CCR-25's May 2024 Internet-wide scan of the real, deployed QUIC-speaking population measures migration succeeding for only 52% of IPv4 and 78% of IPv6 targets that already completed a handshake with SNI supplied, and for only 7.7%/1.2% of handshake-succeeding targets without SNI; 94% of the successful IPv6 targets belong to one hosting organization, and Cloudflare and Google are stated not to support migration at all -- so most real QUIC endpoints do not supply the precondition LIANG-ARXIV-24's restoration path depends on

**Resolution.** Treat migration-based restoration as an opportunistic shortcut behind a full re-punch fallback rather than the primary path, and probe per-peer migration support at connection time (as BUCHET-CCR-25's own scanner does) instead of assuming it; or accept and document the reduced applicability as an open limitation

### 14. ICE requires every agent to keep its keepalive interval Tr at or above a mandatory floor of 15 seconds ("MUST NOT" go lower), while separately requiring periodic keepalives to hold the underlying NAT/firewall UDP mapping

**Required by** `KERANEN-RFC-18` · **removed by** `RICHTER-IMC-16`

RICHTER-IMC-16 measures real Carrier-Grade NAT UDP mapping timeouts as short as 10 seconds (range 10-200s), below ICE's own mandatory 15-second floor -- an ICE agent following the specification's floor exactly cannot refresh a mapping that expires at 10 seconds, so the mapping and the punched session close before the next permitted keepalive is due. HALKES-NETWORKING-11's own field-measured recommendation of 55 seconds, drawn from a home-router/P2P-client population rather than carrier-operated CGN, fails against the same 10-second minimum for the same reason

**Resolution.** Measure the actual mapping timeout per path, the way RICHTER-IMC-16's own TTL-driven probing technique does, rather than trusting a fixed floor; or keepalive at whatever interval the deployment's worst-case Carrier-Grade NAT population requires, accepting the added background traffic ICE's floor was chosen to bound against; or document that ICE-compliant implementations are known to lose sessions behind the shortest-timeout CGNs

### 15. Range-based set reconciliation (RBSR) requires the backing search tree to be clamping-invariant: restricting two structurally different but same-content trees to an arbitrary sub-range must produce the identical result, 

**Required by** `MEYER-TR-24` · **removed by** `RAWAT-DLT-24`

MEYER-TR-24 proves treaps clamping-invariant and states plainly 'Prolly-trees are not clamping-invariant,' because a prolly tree's chunk boundaries are set by a rolling hash over a window of consecutive items, and clamping to an arbitrary sub-range changes which items fall in that window. RAWAT-DLT-24 builds and benchmarks exactly such a prolly tree and its own Requirements section already states a range-based reconciliation protocol requiring clamping-invariance 'cannot be composed directly with this prolly-tree design without an additional adaptation neither paper supplies.' RAWAT-DLT-24 also states computing a difference between two prolly trees is explicitly out of scope for the paper.

**Resolution.** Select a proven clamping-invariant structure (a treap, per MEYER-TR-24's proof) wherever RBSR-style arbitrary-range reconciliation is needed; or restrict prolly trees to whole-chunk Merkle comparison (root/boundary-hash equality, what Dolthub and Canvas already do) rather than arbitrary-range queries; or record the missing prolly-tree/RBSR adapter as an open problem, since neither retrieved paper supplies one.

### 16. AIYER-SOSP-05's Byzantine-Altruistic-Rational Tolerant (BART) incentive-compatibility guarantee for rational nodes requires a trusted admission authority to issue each participant exactly one cryptographic public-key ide

**Required by** `AIYER-SOSP-05` · **removed by** `KLEPPMANN-ARXIV-20`

KLEPPMANN-ARXIV-20's Byzantine Eventual Consistency (BEC) is built explicitly to stay 'immune to Sybil attacks... without proof-of-work or centrally controlled peer admission,' tolerating an unbounded fraction of Byzantine replicas. Choosing BEC's open, permissionless admission for a replication layer removes the authority-issued, one-per-participant identity that AIYER-SOSP-05's Proof-of-Misbehavior accountability mechanism and incentive-compatibility proof depend on, so BART-style sanctions against self-interested (rational) nodes cannot be layered onto a BEC-admitted, permissionless replica set without reintroducing the trusted admission authority BEC exists to avoid.

**Resolution.** Select BEC for a fully open peer-to-peer identity layer and accept its narrower guarantee (only I-confluent transactions and invariants are protected, no general rational-node incentive compatibility); select BART-style accountability only where a closed or permissioned deployment already exists (e.g. a federation of storage providers) and accept that the open-admission design target is not met there; or record layering incentive-compatible sanctions onto a permissionless BEC network as an open problem, since neither paper supplies that combination.

### 17. The querier must observe each hop's identifier and confirm identifier-distance to the target strictly decreases at every step (iterative routing), so a malicious intermediary that fails to make forward progress can be de

**Required by** `SIT-IPTPS-02` · **removed by** `RHEA-USENIXATC-04`

Rhea et al.'s TCP-style per-neighbor timeout estimation, the technique giving Bamboo its best measured latency under churn, requires recursive routing (a node communicates almost exclusively with its own logarithmic set of direct neighbors and keeps a response-time history for each). Sit and Morris state their lookup-progress check is impossible once a node forwards a query onward itself without reporting back to the querier -- their example is CAN's RTT-optimized recursive forwarding, but the incompatibility is with recursive forwarding generally. A single DHT choice of routing mode cannot supply both papers' preconditions.

**Resolution.** Keep iterative routing and accept Vivaldi-derived timeout estimates, whose accuracy diverges from TCP-style estimation at higher churn per Rhea et al.'s own results; or keep recursive routing and substitute a different lookup-integrity defense such as S/Kademlia's disjoint-path lookup (not dependent on iterative observability, per BRIEF.md's verified seeds); or record the tension as an open problem for the specific DHT selected.

### 18. FROST's commitment-server location must serve each participant's preprocessed nonce commitment correctly and exactly once -- never handing an already-consumed commitment to a second signature aggregator.

**Required by** `KOMLO-SAC-20` · **removed by** `SHAPIRO-EATCS-11`

Derived reasoning, not a claim either paper makes about the other. Shapiro et al.'s CvRDT convergence proof (also SHAPIRO-SSS-11) requires only that every update eventually reach every replica, tolerating loss, reordering, and duplication; it supplies no consume-once or linearizable-read primitive. If an architecture backs FROST's commitment store with this kind of eventually-consistent, partition-tolerant replica -- a natural choice elsewhere in a decentralized design for its availability under partition -- two isolated replicas during a network partition can each still regard the same nonce-commitment pair as unconsumed and hand it to a different aggregator, which is exactly the 'unused values' guarantee FROST's own text states the commitment server must provide.

**Resolution.** Back FROST's commitment store with a linearizable store (a single elected leader, or a consensus-backed key-value store) rather than the CRDT-style replica used elsewhere, accepting reduced partition tolerance for that one component; or restrict signing operations to periods when the commitment store's replicas are known to be mutually connected, accepting a liveness cost during partitions; or enumerate which resources in the architecture need exactly-once semantics as an explicit open list.

### 19. No observer, including the message's eventual recipients, should be able to determine which peer originated a given message (Loopix's sender-anonymity guarantee).

**Required by** `PIOTROWSKA-USENIXSEC-17` · **removed by** `GOLD-ARXIV-23`

G-Rank's clicklog gossip row carries the querying peer's node ID as application data the ranking algorithm itself consumes; the paper states peer discovery 'is not supplied by any separate mechanism' beyond reading that ID out of a received row. Loopix hides network-level message origin from an on-path or mix-node observer but, by its own stated design (attaching a sender address to a payload is left unbuilt, deferred to the application), cannot strip identity the application writes into the message body. Routing G-Rank's gossip over a Loopix-style privacy tier removes none of the sender-identifying information G-Rank depends on, because that information was never a transport-layer property.

**Resolution.** Exclude G-Rank's clicklog traffic from the privacy tier's guarantee and disclose this to the user; or redesign the clicklog schema to reference a rotating, session-scoped handle instead of a stable node ID, untested in the corpus and requiring enough persistent linkability across rotations for G-Rank's similarity clustering to still function; or select a different ranking mechanism under the privacy tier and reserve G-Rank for the non-private tier.

### 20. Every routing peer must keep its local identity-commitment-tree root synchronized with the on-chain registration/removal stream; proving membership against a stale root exposes that peer's own leaf index and compromises 

**Required by** `TAHERIBOSHROOYEH-ARXIV-22` · **removed by** `RHEA-USENIXATC-04`

Moderate confidence: rests on typical churn rates rather than a specific mechanism's design choice. Rhea et al. build their own churn experiments around median session times from 1.4 minutes to 3 hours and cite five independent prior deployed-network studies (their Table 1) giving median session lengths from about one hour down to about one minute. A peer reconnecting after an absence on this ordinary timescale is in the state Taheri-Boshrooyeh et al. state compromises anonymity -- catching up on a tree it fell behind on -- and neither that paper nor any other entry in this corpus supplies a formula relating the tolerated epoch-gap parameter Thr to a measured churn distribution.

**Resolution.** Require a peer to complete tree resynchronization, and hold outgoing messages, before publishing after reconnecting, accepting a liveness cost; or widen Thr to tolerate more drift, accepting the paper's own stated cost of a longer stale-epoch replay window; or record the missing churn-to-Thr relationship as an open problem.

### 21. A single-server PIR deployment's offline hint (SimplePIR/DoublePIR) or preprocessed structure (YPIR) must be refreshed whenever the underlying database changes enough to invalidate it; neither construction analyzes or bo

**Required by** `HENZINGER-USENIXSEC-23` · **removed by** `KLEPPMANN-CONEXT-24`

Kleppmann et al. describe the AT Protocol/Bluesky architecture as built around a continuous, unbounded-rate write stream by construction: 'A Relay requires every PDS to serve a WebSocket stream of signed repository updates,' and an App View's only input is that stream. A private-search or content-location tier over this kind of index, built on single-server PIR, must search exactly the class of continuously-updating database Henzinger et al. state they do not analyze and Menon et al. (MENON-USENIXSEC-24, YPIR) state forces a choice between serving stale precomputation or falling back to unamortized per-query computation once the database changes faster than preprocessing completes.

**Resolution.** Restrict the PIR-backed privacy tier to a periodically-snapshotted view of the index and state the snapshot interval to the user as the tier's freshness cost, rather than searching the live stream continuously; or scope the private-search tier to a slower-moving content subset and serve the live firehose only through the non-private tier; or record the missing preprocessing-cost-versus-write-rate measurement as an open problem, since it decides whether a single-server-PIR privacy tier over a live social index is feasible at all.

### 22. A compliant peer's exposure to any other single peer's optimistic-unchoke slot -- BitTorrent's deliberately unconditional bootstrap grant of upload bandwidth to a peer with nothing yet to reciprocate -- stays small, beca

**Required by** `COHEN-IPTPS-03` · **removed by** `LOCHER-HOTNETS-06`

LOCHER-HOTNETS-06 (BitThief) raises simultaneous connections from the reference default of 80 to 500 and re-announces to the tracker far more often, using the identical open tracker mechanism COHEN-IPTPS-03 relies on for random peer selection, and measures that 'opening more connections increases download speed linearly' with zero upload -- because download rate now comes predominantly from the unconditional optimistic-unchoke and seeder round-robin paths rather than from reciprocation. SIRIVIANOS-IPTPS-07 (the Large View Exploit) independently confirms the same mechanism: it states its exploit 'requires only the standard tracker announce protocol and the standard practice... of accepting and merging additional peer lists from other peers,' and measures its free-riding client reaching an average view of approximately 250 peers (five times the ~50-peer standard) and completing faster than a compliant client in 12 of 15 tested public swarms.

**Resolution.** A designer can have the tracker rate-limit or cap peer-list size and connection count per requester, trading away part of the claimed churn-robustness benefit of an unconstrained random graph; or accept that the choking algorithm's incentive property does not hold against a strategic client and add a mechanism that meters or prices the bootstrap slot itself, as LOCHER-HOTNETS-06 recommends and as PIATEK-NSDI-07 and LEVIN-SIGCOMM-08 independently confirm is needed by both stating they contradict the 'TFT alone makes BitTorrent robust' reading of COHEN-IPTPS-03.

---

## 11 figures attributed to papers that do not contain them

Each was found by holding both full texts at once. A figure in this class travels onward carrying the
citing paper's authority, which is why it matters more than an ordinary error.

### 1. `DANEZIS-WALRUS-25` cites `VORICK-SIA-14`

**The claim.** Table 1 attributes a 3x storage overhead figure to Sia, grouped under "classic erasure-coded systems (Storj, Sia)" at twelve-nines durability.

**What the cited paper's own text says.** Sia's own paper states no overhead ratio at all; it leaves erasure-code redundancy "as a design choice for the client," and its only numeric example (m=10 of n=100, a 10x expansion) is explicitly flagged by its own authors as "only illustrative" and "an extreme example," not a specification.

### 2. `LI-EPRINT-25` cites `KROL-EUROSP-24`

**The claim.** DISC-NG contains no comparison to dedicated single-service overlays and no security analysis.

**What the cited paper's own text says.** DISC-NG's own text reports eclipse-rate measurements against DHT, DHTTicket, and DISCv5 baselines at 20%/33.33%/50% Sybil fractions (DHT reaching up to 59.7%, DISC-NG staying under ~0.5%), tests robustness under non-uniform Sybil placement (DHT/DHTTicket reach 100% eclipse, DISC-NG reaches 0%), and states two liveness theorems under an explicit partial-synchrony threat model. Only the 'no comparison to a dedicated single-service overlay' half of the claim is supported; 'no security analysis' is not.

### 3. `SIDDARTH-FRONTIERS-20` cites `BRIGHTID-WP`

**The claim.** BrightID 'runs GroupSybilRank -- a modification of the SybilRank algorithm -- to score participants by graph affinity to seeds.'

**What the cited paper's own text says.** BrightID's own whitepaper never uses the term 'GroupSybilRank' anywhere in its retrieved text; it states only that its research was 'partly based on' SybilRank, without naming or describing a distinct algorithm under that name.

### 4. `BHARGAVAN-HAL-18` cites `COHNGORDON-CCS-18`

**The claim.** For the group-creation (Create) operation, ART's sender and recipient costs are equal, both requiring 2n public-key operations -- i.e. a joining/receiving member pays the same linear-in-group-size cost as the group's creator.

**What the cited paper's own text says.** COHNGORDON-CCS-18's own Table 1 states an asymmetric split for the corresponding Setup operation: O(n) exponentiations for the sender (the group creator) against O(log n) for any other/later-joining member -- consistent with the paper's own mechanism description, where a later member computes the tree key from its own leaf secret and copath in O(log n), while only the creator pays O(n) to generate every other member's leaf key pair directly. The equal-cost claim (O(log n)/O(log n)) applies in COHNGORDON-CCS-18's own table only to its Ongoing row (Update/Add/Remove), which BHARGAVAN-HAL-18 correctly reports separately as 2*log(n) for both parties.

### 5. `DICURSI-BIGDATA-24` cites `RAMAN-IMC-19`

**The claim.** "5% of instances hold 90% of users and 94% of toots (posts)" and "outages in 10 instances could remove 60% of global toot volume," both attributed to RAMAN-IMC-19 in DICURSI-BIGDATA-24's related-work summary.

**What the cited paper's own text says.** RAMAN-IMC-19's own retrieved measured-results contain no figure matching "5% of instances / 90% of users / 94% of toots" in any form. Its actual reported concentration figures are shaped differently: top-3-AS hosting share 62% of users; content-generation concentration (78% of instances produce under 10% of their own timeline content); and a simulated top-10-instance removal with no replication making 62.69% of toots unavailable (close to but not identical to the cited '60% from outages,' and describing simulated permanent removal from a graph model, not an outage). DICURSI-BIGDATA-24's own entry already flags both figures as unverified and recommends checking RAMAN-IMC-19 directly before use, but the 5%/90%/94% figure specifically is not present in RAMAN-IMC-19's retrieved text as held in this evidence file.

### 6. `KLEPPMANN-PAPOC-22` cites `AUVOLAT-SRDS-19`

**The claim.** Characterizes AUVOLAT-SRDS-19's Merkle Search Trees as the state-based CRDT counterpart to its own construction, 'tolerating any number of Byzantine nodes.'

**What the cited paper's own text says.** AUVOLAT-SRDS-19's retrieved text contains no discussion anywhere of Byzantine faults, malicious nodes, or adversarial input. Its own evaluation states explicitly 'No node joins, leaves, or crashes occurred in any reported simulation,' and its correctness argument rests only on a collision-resistant hash function and a benign gossip model -- no Byzantine-tolerance claim or proof appears in the paper.

### 7. `MEYER-TR-24` cites `AUVOLAT-SRDS-19`

**The claim.** States Auvolat and Taïani's Merkle Search Tree 'can be driven to O(n) degeneration by a malicious data source producing a set that collapses the tree to a single large array.'

**What the cited paper's own text says.** AUVOLAT-SRDS-19's retrieved text never analyzes malicious or adversarial data sources; it states expected tree depth log_B(n) with the probability of exceeding depth+c falling exponentially in c, as a probabilistic guarantee under benign random input, with no adversarial-input case considered. MEYER-TR-24's own entry flags this as unverified against the primary source; the corpus now holds that source, and it supports neither this degeneration claim nor KLEPPMANN-PAPOC-22's opposite Byzantine-tolerance claim about the same mechanism.

### 8. `targets-deduped.json (project retrieval-target registry, not a corpus paper)` cites `KLEPPMANN-TPDS-17`

**The claim.** The registry's stated reason for retrieving this paper says it 'states the paper's own memory and message-size measurements against Operational Transformation and other CRDTs.'

**What the cited paper's own text says.** KLEPPMANN-TPDS-17 (A Conflict-Free Replicated JSON Datatype / Automerge) is a formal-semantics paper with no implementation and no benchmark; its own conclusion explicitly defers performance measurement to follow-on work. This mismatch is already caught in the evidence entry's own Contradicts section: a synthesis citing this paper for Automerge's measured memory or message-size cost has no support in the retrieved text.

### 9. `GOLLE-EC-01` cites `ADAR-FM-00`

**The claim.** 'a recent study of the Gnutella network found that more than 70% of its users contribute nothing to the system,' cited to Adar and Huberman alone

**What the cited paper's own text says.** ADAR-FM-00's own measured figure is 'almost 70%' (66% of 33,335 peers, rising to ~69% once NAT-blocked transactions are counted) -- framed by the source itself as approaching but not reaching 70%, never exceeding it.

### 10. `VISHNUMURTHY-P2PECON-03` cites `SAROIU-MMCN-02`

**The claim.** '20 to 40% of Napster and almost 70% of Gnutella peers share little or no files,' cited jointly to Saroiu-Gummadi-Gribble and to Adar and Huberman for both figures together

**What the cited paper's own text says.** SAROIU-MMCN-02's own retrieved measured result states '25% of the Gnutella clients do not share any files' -- based on a live Gnutella crawl using the pong-message file-count field -- less than half the 'almost 70%' figure attributed to it jointly with Adar and Huberman, whose own paper (ADAR-FM-00) is the actual source of that number.

### 11. `DICURSI-BIGDATA-24` cites `RAMAN-IMC-19`

**The claim.** 5% of instances hold 90% of users and 94% of toots; outages in 10 instances could remove 60% of global toot volume

**What the cited paper's own text says.** RAMAN-IMC-19's own retrieved measured-results contain no '5% of instances / 90% users / 94% toots' figure in any form. Its actual reported concentration figures are shaped differently: top-3-AS hosting-provider share of users (62%), content-generation share (78% of instances produce under 10% of their own timeline content), and a simulated node-removal figure (removing the top 10 instances by toot count, no replication, makes 62.69% of toots unavailable -- close to but not identical to the cited '60% from outages of 10 instances', and describing a different event, simulated permanent removal from a graph model rather than an observed outage). DICURSI-BIGDATA-24's own entry already flags both figures as unverified pending a direct check against RAMAN-IMC-19's full text.

---

## 7 papers whose abstract and body disagree

A synthesis citing only the abstract would misstate each of these.

### 1. `DANEZIS-WALRUS-25`

- **Abstract:** Table 1 (the paper's headline comparison table) states "classic erasure-coded systems (Storj, Sia)" carry a 3x storage overhead at twelve-nines durability, and this 3x figure is what the paper's abstract-level claim of Walrus's 4.5x overhead is compared against.
- **Body:** The paper's own related-work section separately states, for the same system, "This approach results in a 2.75× replication factor," citing Storj's actual deployed 29-of-80 Reed-Solomon configuration from a different, newer (2026) Storj document. The paper does not reconcile the 3x Table 1 figure against its own 2.75x related-work figure. A third figure appears in Storj's own retrieved paper (WILKINSON-STORJ-18), whose stated "typical scenario" deployment example is a 20-of-40 Reed-Solomon setup, a 2x expansion factor -- lower than either of DANEZIS-WALRUS-25's two figures and unreconciled with both.

### 2. `ZHOU-EPRINT-24`

- **Abstract:** The evidence entry's verbatim-extract section quotes the paper directly: 'up to 62% reduction in computation time and 22% reduction in overall latency' from the paper's three combined search optimizations (beam search, fast starting, batched PIR).
- **Body:** The same entry's own descriptive 'What it does' section states the same three optimizations together give 'a 76% reduction in computation and a near-70% reduction in end-to-end latency' -- a different pair of figures for what the entry presents as the same combined result.

### 3. `WORLDCOIN-WP`

- **Abstract:** "no biometric data ever leave the user's device" (the paper's own stated privacy claim).
- **Body:** The Personal Custody Package -- generated on the Orb and sent to the user's phone -- "currently contains: iris and face embeddings, raw iris and face images, and the AMPC fragments," each individually encrypted; the raw biometric images are formed and transported off the enrollment device as an encrypted package.

### 4. `LESNIEWSKI-LAAS-NSDI-10`

- **Abstract:** The paper's own analytical result predicts the performance-transition point (LOOKUP messages beginning to grow exponentially with attack-edge count g) occurs at g > n/10, where n is the honest node count.
- **Body:** The paper's own measurement across all four real datasets tested (Flickr, LiveJournal, YouTube, DBLP) finds this transition instead occurs at m/10 < g < m, where m is the honest edge count -- a substantially lower attack-edge threshold than the analytical prediction, stated in the paper's own results table without being reconciled against the theorem elsewhere in the same paper.

### 5. `MEYER-TR-24`

- **Abstract:** Its non-homomorphic RBSR technique 'effectively render[s] merkle-search-tree reconciliation obsolete.'
- **Body:** The conclusion states 'neither option is strictly superior to the other,' because the homomorphic-hash-based RBSR variant retains an advantage (immunity to the malicious-data-source degeneration this paper attributes to non-homomorphic trees) that this paper's own construction does not have.

### 6. `AIYER-SOSP-05`

- **Abstract:** The replicated-state-machine prototype 'executes 20 requests per second.'
- **Body:** Section 8 states the measured throughput as 'about 15 operations a second for small groups of users,' with no stated change in configuration, hardware, or group size separating the two figures anywhere in the retrieved text.

### 7. `ELLIS-SIGMOD-89`

- **Abstract:** The algorithm's 'overall structure is independent of the semantic information.'
- **Body:** The algorithm's central mechanism, the transformation matrix T, is described as a set of hand-written functions, one per operator pair, each embedding operation-specific semantics (e.g. incrementing or decrementing a text position); only the surrounding control structure (request queue, state-vector comparison, log scan) is semantics-independent, not the transformation step the mechanism's correctness depends on.

---

## Per-family detail

The full working for each quantity family is in `registry/conflicts/`, one file per family, every
claim cited by evidence key.
