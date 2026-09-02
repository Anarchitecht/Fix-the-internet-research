## [LESNIEWSKI-LAAS-NSDI-10] Whanau: A Sybil-proof Distributed Hash Table
**Citation:** Chris Lesniewski-Laas, M. Frans Kaashoek. "Whanau: A Sybil-proof Distributed Hash Table." USENIX NSDI, 2010.
**Retrieved:** full text via https://pdos.csail.mit.edu/papers/whanau-nsdi10.pdf
**Source URL:** https://pdos.csail.mit.edu/papers/whanau-nsdi10.pdf
**Domain:** F

### What it does
Whanau builds a one-hop distributed hash table (DHT) whose routing tables resist the Sybil
attack — an adversary creating an unlimited count of false identities to influence lookups. A
node's lookup correctness depends only on the count of social-graph edges connecting honest
users to adversary-controlled nodes ("attack edges"), not on how many false identities the
adversary creates behind those edges.

The mechanism runs in two phases. A SETUP phase runs periodically across all nodes and builds
each node's routing tables by sampling other nodes through random walks over the social graph:
each node's immediate social neighbors are the only edges it can walk, and no node holds a map
of the whole graph. Each node treats every sampled node as an equally likely candidate without
being able to tell honest samples from adversary samples, relying only on the fact that a large
fraction of samples land on honest nodes when the honest region of the graph is a fast-mixing
expander graph (a graph in which a random walk of length w = O(log n), for n honest nodes,
reaches close to the stationary distribution, so that the walk's endpoint is close to uniform
over graph edges). A LOOKUP phase then uses the constructed routing tables to find a
key-value record in O(1) messages and one network round trip, without further walks.

To counter an adversary that clusters its false identifiers immediately before a targeted key
(a clustering attack), Whanau introduces layered identifiers: honest node identifiers are placed
independently and uniformly at random within each of several layers, and a lookup tries each
layer in turn, so that a clustering attack concentrated in one layer's identifier space does not
help in the others. Each social-network edge is treated as a separate virtual node, so that
routing-table space and query load scale with a person's degree in the social graph (their count
of social connections) rather than being fixed per person — a policy choice the paper states,
not a measured property.

The instant-messaging (IM) application built on Whanau has each user publish one self-signed
(public key, IP address) tuple; a sender looks up the buddy's public key in the DHT, verifies the
returned tuple's signature, and sends to the returned address. Whanau supplies availability of
lookup (an honestly-inserted value is found), not integrity (the DHT also returns adversary-
inserted values for the same key); integrity is left to the application, which the IM example
handles by discarding records with invalid signatures.

### Measured results

| Result | Conditions |
|---|---|
| Routing table size O(√(km log(km))) entries per node for aggregate system capacity of km keys, k = keys per node, m = honest edges | Analytic result, confirmed by simulation |
| Median LOOKUP: 2 messages at g=20,000 attack edges; 20 messages at g=2,000,000 attack edges, at table size 10,000 entries/link | Flickr social graph, n=1,624,992 nodes, m=15,476,835 edges (Table 2) |
| Minimum table size for fast lookups without attack: ≈1,000 ≈ √n entries/link; under g > n, requires ≈10,000 entries/link | Flickr graph |
| Performance transition point (LOOKUP messages grow exponentially) occurs at m/10 < g < m, not at the analytically predicted g > n/10 | Measured across all four datasets: Flickr (n=1.6M), LiveJournal (n=5.2M), YouTube (n=1.1M), DBLP (n=510K) |
| Layers become important (measurably reduce messages) above g=5,000 attack edges (0.3% of n) on Flickr; for g>20,000, ≈8 layers is best | Flickr, fixed resource budget of 100,000 table entries per link, clustering-attack adversary |
| Random-walk escape probability into Sybil region: 90% Sybil at walk length 40 when g=2,000,000 (1.35 attack-links/honest user on average); 60% honest at walk length 10 under the same attack | Flickr social graph |
| Random-walk mixing: CDF of per-edge landing probability approaches the ideal uniform (1/m) distribution as walk length increases from 10 to 80 steps | Sampled 100 random starting edges per network, computed over Flickr, LiveJournal, YouTube, DBLP |
| PlanetLab: median lookup latency ≈ one network round trip within PlanetLab, rising gradually with churn; percent of queries needing retry rises under churn and resets to baseline each time SETUP re-runs | 4,000 virtual Whanau nodes on 400 PlanetLab machines, routing-table size 200 entries/social link, node failure/recovery via Poisson process averaging 2 events/second, tested at 10% and 20% of virtual nodes offline plus a no-churn control |
| Table-size scaling matches the O(√m) prediction for a one-hop DHT; at m=10,000,000 edges, most lookups succeed in 1–2 messages at ≈2,000 entries/link | Synthetic preferential-attachment networks (power-law exponent ≈2) plus the four real datasets, no adversary simulated |

### Parameters
- Walk length w: fixed at 10 in the clustering-attack experiments (Section 9.2); the paper states w = O(log n) is required for fast mixing and that larger w costs more bandwidth and raises the chance a walk returns a Sybil node.
- Table size (entries per social-network edge): varied from 100 to 1,000,000 in experiments; minimum viable is ≈√m.
- Number of layers: varied from 1 to 10; optimal layer count rises with table-size budget and with attacker strength, determined empirically per network (Figures 10–11), no single fixed recommendation given.
- Retry limit: 120 messages, above which a lookup is counted as failed in the heat-map experiments (Figure 9 caption).
- Amplification: running 3·log2(n) independent protocol instances in parallel is stated to reduce lookup failure probability below 1/n³, given a base (g, ε, 1/2)-Sybil-proof instance.

### Stated limitations
The implementation is not aware of network locality (does not place routing-table entries by
network proximity). Routing tables require periodic full rebuilds (re-running SETUP) to react to
churn in the social graph and in the set of stored keys; the paper describes a bandwidth/latency
tradeoff for how often to rebuild but states this as future work, not solved. The protocol as
described handles 1 ≲ k ≲ m keys per node well; outside that range (k > m or k < 1) the paper
states specific modifications are required and analyzes them without simulating them. Integrity
of returned values is explicitly out of scope; an adversary can insert or overwrite key-value
pairs for the same key and Whanau will return them alongside honest values. The paper states
Whanau can be broken by social engineering attacks that persuade honest users to link to
Sybil identities, despite being provably Sybil-proof under its graph model. The PlanetLab
experiment's scale (4,000 virtual nodes) is stated by the authors as too small to test asymptotic
scaling behavior; it demonstrates functioning under churn only.

### Requirements it places on the rest of the system
Requires a pre-existing social graph of honest, mostly-symmetric trust edges in which the honest
region has no sparse cut internally and forms a fast-mixing expander graph; the paper's own
measurement of this property (Figure 6) is a prerequisite check that must be re-run on any graph
this is deployed against. Requires each node to know order-of-magnitude estimates of m (honest
edge count), w (mixing time), and k (keys per node) to size tables and walk lengths; does not
require nodes to know g (attack-edge count) or ε (fraction of loser nodes). Requires a mechanism
elsewhere in the system to supply per-record integrity (such as a signature scheme), because
Whanau's LOOKUP returns adversary-inserted records for a queried key without filtering them.
Requires periodic re-execution of the cooperative SETUP phase across the network to track churn;
this is a synchronized, network-wide operation, not an incremental per-node update.

### Contradicts
None found among the papers in this corpus.

### References worth retrieving
- SybilGuard / SybilLimit — Yu, Kaminsky, Gibbons, Flaxman, and Yu et al. follow-up (as cited: refs [27], [26]) — foundational (fast-mixing-graph random-walk Sybil defense that Whanau builds on)
- G. Danezis, C. Lesniewski-Laas, M. F. Kaashoek, R. Anderson. "Sybil-Resistant DHT Routing." ESORICS 2005 — foundational (the bootstrap-graph correctness criterion Whanau's authors state was left as an open problem)
- G. Danezis, P. Mittal. "SybilInfer: Detecting Sybil Nodes Using Social Networks." NDSS 2009 — competing (Bayesian inference over random walks for Sybil detection)
- I. Gupta, K. Birman, P. Linga, A. Demers, R. van Renesse. "Kelips: Building an Efficient and Stable P2P DHT through Increased Memory and Background Overhead." IPTPS 2003 — competing (the insecure one-hop DHT Whanau compares its non-adversarial scaling against)
- H. Rowaihy, W. Enck, P. McDaniel, T. La Porta. "Limiting Sybil Attacks in Structured P2P Networks." INFOCOM 2007 — competing
- A. Singh, T.-W. Ngan, P. Druschel, D. Wallach. "Eclipse Attacks on Overlay Networks: Threats and Defenses." INFOCOM 2006 — attack
- B. N. Levine, C. Shields, N. B. Margolin. "A Survey of Solutions to the Sybil Attack." UMass Amherst TR, 2006 — foundational (survey)
- A. Mislove, M. Marcon, P. Gummadi, P. Druschel, B. Bhattacharjee. "Measurement and Analysis of Online Social Networks." IMC 2007 — foundational (source of the social-graph datasets used in evaluation)
- C. Lesniewski-Laas, M. F. Kaashoek. "Whanaungatanga: Sybil-Proof Routing with Social Networks." MIT CSAIL TR-2009-045 — superseded-by (this NSDI paper is the published version of this technical report)

### Verbatim extracts
- "an adversary must convince a large fraction of the honest users to make a social connection with the adversary's Sybils"
- "Whānau provides availability, but not integrity"
- "the number of Sybils in the social network does not affect the protocol's performance, but links between honest users and Sybils do"
- "Whānau can be broken by social engineering attacks"
- "for a table size of 5,000 on the Flickr graph, most lookups will succeed within 1 or 2 messages"
