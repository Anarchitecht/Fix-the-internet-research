## [URDANETA-CSUR-11] A Survey of DHT Security Techniques
**Citation:** Guido Urdaneta, Guillaume Pierre, Maarten van Steen. "A Survey of DHT Security Techniques." ACM Computing Surveys 43(2), 2011. DOI 10.1145/1883612.1883615.
**Retrieved:** full text via https://www.distributed-systems.net/my-data/papers/2011.acm-cs.pdf
**Source URL:** https://www.distributed-systems.net/my-data/papers/2011.acm-cs.pdf
**Domain:** A

### What it does
This paper classifies published defenses for distributed hash tables (DHTs — overlay networks in which each node holds a small routing table and a lookup for key k is routed hop by hop toward the node responsible for k) against three attack categories and states each defense's mechanism and disadvantage. It runs no experiments of its own; every quantitative figure below is a figure the survey reports from the paper it discusses, not a measurement performed by Urdaneta, Pierre, and van Steen. The three categories: the Sybil attack (one physical attacker creates many logical identities), the Eclipse attack (an attacker occupies enough of a correct node's routing-table entries to isolate that node from the honest network, also called routing-table poisoning), and routing/storage attacks (a poisoned routing table or a colluding storage-set causes a lookup to fail or return forged data).

Sybil defenses fall into six mechanism families: centralized certification (a trusted authority signs one certificate per identity), distributed registration (nodes vet each other's join requests without a central authority), physical-network-characteristic fingerprinting (network coordinates or measured latency distinguish physical hosts), social-network-based verification (SybilGuard, SybilLimit — described below), computational puzzles (a node must solve a proof-of-work puzzle to obtain or keep an identity), and game-theoretic mechanisms (an economic penalty for operating Sybil identities).

Eclipse defenses fall into two families: constrained routing tables, where the only entries a node may hold are determined by a public function of node identifiers (defeats Eclipse by construction but forecloses proximity-based neighbor selection), and defenses that keep a proximity-optimized table alongside a constrained fallback table, switching to the fallback when a routing-failure test signals that the optimized table has been poisoned.

Routing/storage defenses combine redundant storage (replication or erasure coding across multiple nodes so that no single compromised node controls a key) with redundant routing (sending a lookup along multiple paths or through multiple candidate next-hops per step, so a single malicious node on one path does not block the lookup). Replicas placed at numerically close identifiers ease consistency maintenance for mutable data; replicas spread across the identifier space are harder for a spatially concentrated attacker to capture, but the paper argues this is not a large improvement because placement functions are public and an attacker can target all relevant locations for a given key. Redundant routing takes one of three forms: wide paths (each routing hop attempts several candidate next-hops in parallel; the hop advances if any one candidate is honest), multiple disjoint paths (independent full paths from source to destination; success requires a majority of paths to be entirely honest), or multiple wide paths (successive attempts at a full wide-path route).

### Measured results
All figures below are as reported by this survey about other authors' experiments; none is this survey's own measurement. Retrieve the cited primary source before using a figure in a selection.

| Reported finding | Conditions (as stated in survey text) | Source discussed |
|---|---|---|
| 15% malicious nodes produces approximately 80% malicious entries in standard Pastry routing tables | Pastry proximity-based routing table, no defense | Condie et al. 2006, cited by Urdaneta section 4.6 |
| Probability of successful single-path routing ≈ 0.24 | f = 0.25 fraction malicious, path length 5, formula (1−f)^5 | Worked example in the survey's own text, section 4 |
| Redundant-routing false-positive probability 0.77 under a node-suppression attack vs. 0.12 without attack | Fraction of colluders f = 0.3, γ = 1.23, 256 samples for the distance test, target false-negative rate 0.001 | Castro et al. 2002, section 5.2 |
| Checked iterative routing adds 2.7 extra hops on average | Castro et al.'s simulation, exact node count and topology not given in this survey's text | Castro et al. 2002, section 5.2 |
| Probability of reaching all correct replicas ≈ (1−f)^(1+log_b N) | f = fraction malicious, b = identifier base, N = expected node count | Castro et al. 2002 formula, section 5.2 |
| SybilGuard: 99.96% of nodes have at least 10 route intersections at group size w=300 (no malicious nodes) | Kleinberg synthetic social-network model, up to 1,000,000 nodes, degree 24 | Yu et al. 2006, section 3.7 |
| SybilGuard: probability that all routes remain in the honest region stays near 100% for attack edges g ≤ 2,000, dropping to 99.8% at g = 2,500 | 1,000,000-node network, w=300 (route length parameter reported elsewhere in the text as needing to be as large as 2,000 for a million-node network) | Yu et al. 2006, section 3.7 |
| SybilLimit accepts between 10 and 20 Sybil nodes per attack edge | Synthetic Kleinberg network of 1,000,000 nodes / 10.9 million edges (w=10, r=10,000); Friendster 932,000 nodes / 7.8 million edges (w=10, r=8,000); LiveJournal 900,000 nodes / 8.7 million edges (w=10, r=12,000); DBLP 106,000 nodes / 626,000 edges (w=15, r=3,000) | Yu et al. 2008, section 3.8 |
| Myrmic: 97th/90th percentile lookup times 346 ms / 281 ms; 93% of lookups solved within 6 hops plus verification | PlanetLab testbed, 120 nodes, all correct, certificate size l=3, 500 lookups per node at 1 request per 3 seconds | Section 5.7 (referenced from surrounding text; source paper not separately keyed here) |
| Myrmic: 0.0122% of lookups fail | LAN environment, 1,000 nodes, 30% malicious, verification procedure assumed infallible | Same as above |
| KAD DHT estimated size: 1.5 million nodes (Steiner et al. 2007) vs. 4 million nodes (Crosby and Wallach 2007) | Two independent measurement studies of the same deployed network, methodology not detailed in this survey | Section 6 |

### Parameters
No parameters are this survey's own; each value above belongs to the cited primary paper and is listed under Measured results with its source.

### Stated limitations
The survey states that none of the reviewed Eclipse or Sybil defenses is evaluated against an adversary that attacks a small subset of nodes, a specific key, or specific routing-table rows, or that poisons slowly by behaving correctly most of the time — these are called more subtle attacks left unaddressed by every proposal it reviews. Singh et al. 2006 (cited within) explicitly states that defending against localized attacks, where an honest node is geographically surrounded by malicious nodes, remains an open problem. The survey states that no reviewed transactional DHT design tolerates malicious nodes. The survey states that Rodrigues and Liskov's study of erasure coding versus replication does not model mutable data or malicious nodes, so its bandwidth-parity finding may not hold once both are considered. The survey concludes that current deployed DHTs (KAD, BitTorrent, LimeWire, the Storm botnet, OpenDHT) are not designed to tolerate malicious nodes, and that Kademlia (used by all of them) remains vulnerable to Sybil and Eclipse attacks because nodes generate their own identifiers.

### Requirements it places on the rest of the system
The survey's own conclusion (section 7) states four preconditions the reviewed literature treats as jointly necessary for a secure DHT: secure assignment of node identifiers (an identifier a node cannot freely choose), a bound on the fraction of malicious nodes, malicious nodes spread across the identifier space rather than concentrated, and data replication combined with a routing mechanism that reaches a correct replica set with high probability. Centralized-certification Sybil defenses require an online or offline certification authority trusted by all participants and a certificate-revocation mechanism. Social-network Sybil defenses (SybilGuard, SybilLimit) require every participant to hold a genuine social relationship with some other participants, offline distribution of a symmetric key per social edge, and low churn in the social graph, since registry and witness tables update only on social-graph change. Computational-puzzle Sybil defenses require every honest node to continuously spend computing resources on puzzle solutions and require the puzzle difficulty to be set low enough for the least-capable honest node to keep solving puzzles while retaining spare capacity for other work; the survey cites a measurement (Anderson and Fedak 2006) that the most powerful nodes in a real peer-to-peer system have several orders of magnitude more CPU capacity than the least powerful, which bounds how high that difficulty can be set. Redundant-routing schemes based on multiple disjoint paths require paths to actually be disjoint for the stated success probability to hold; the survey states this disjointness is not guaranteed in practice. Eclipse defenses based on constrained routing tables require stable, randomly assigned node identifiers and foreclose proximity-based neighbor selection as a performance optimization.

### Contradicts
None found within this corpus. The paper is itself a secondary source over the papers it discusses (Castro et al. 2002 [CASTRO-OSDI-02 in this corpus], Yu et al., Singh et al., and others); a downstream synthesis step should prefer the primary source's own reported conditions over this survey's paraphrase where the two differ.

### References worth retrieving
- Castro, Druschel, Ganesh, Rowstron, Wallach. "Secure Routing for Structured Peer-to-Peer Overlay Networks." OSDI 2002. — foundational (already in corpus as CASTRO-OSDI-02)
- Douceur. "The Sybil Attack." IPTPS 2002. — foundational, defines the Sybil attack this entire literature responds to
- Baumgart, Mies. "S/Kademlia: A Practicable Approach Towards Secure Key-Based Routing." ICPADS 2007. — competing / already read per brief section 7
- Yu, Kaminsky, Gibbons, Flaxman. "SybilGuard." (venue not given in this excerpt) 2006. — foundational for social-graph Sybil defense
- Yu, Gibbons, Kaminsky, Xiao. "SybilLimit." 2008. — foundational, supersedes SybilGuard on the same social-graph mechanism
- Singh, Castro, Druschel, Rowstron. "Defending against Eclipse attacks on overlay networks." 2006. — competing, in-degree/out-degree control approach
- Awerbuch, Scheideler. "Towards a Scalable and Robust DHT." SPAA 2006. — competing, de Bruijn-graph-based theoretical defense
- Condie, Kacholia, Sankararaman, Hellerstein, Maniatis. "Induced Churn as Shelter from Routing Table Poisoning." NDSS 2006. — competing, augments Castro et al.'s two-table defense
- Fiat, Saia, Young. S-Chord swarm-based erasure-coded defense, 2005. — competing, theoretical
- Fiat, Saia. Butterfly-network supernode topology, 2007. — competing, theoretical
- Naor, Wieder. de Bruijn-graph-variant topology for wide-path routing, 2003. — competing, theoretical
- Hildrum, Kubiatowicz. Redundant routing-table-entry defense using network proximity, 2003. — competing
- Rodrigues, Liskov. Study comparing erasure coding and replication bandwidth under churn, 2005. — competing / attack on the assumed coding advantage
- Steiner, Natoli, Biersack. Measurement of Sybil/Eclipse attacks against deployed KAD network, 2007. — attack-or-critique, real-world measurement
- Crosby, Wallach. "An Analysis of BitTorrent's Two Kademlia-Based DHTs." Rice TR-07-04, 2007. — attack-or-critique, real-world measurement
- Holz, Steiner, Dahl, Biersack, Freiling. Measurement study of the Storm botnet's Kademlia-based command channel, 2008. — attack-or-critique, real-world measurement of a deployed adversarial DHT

### Verbatim extracts
- "having a logically central, trusted authority to issue identities is the only practical way" (Douceur's conclusion, as restated)
- "15% of malicious nodes in the overlay results in around 80% of malicious entries"
- "the probability of false positives is 0.77 under a node suppression attack, and 0.12 without"
- "adds 2.7 extra hops on average to the routes without significantly increasing"
- "between 10 and 20 accepted Sybil nodes per attack edge"
- "with a fraction with 30% of malicious nodes, only 0.0122% of the lookups failed"
- "defending against such attacks remains an open problem" (localized-attack limitation, attributed to Singh et al.)
- "we are not aware of any transactional DHT design that tolerates malicious nodes"
