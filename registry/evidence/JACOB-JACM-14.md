## [JACOB-JACM-14] SKIP+: A Self-Stabilizing Skip Graph

**Citation:** Riko Jacob, Andrea W. Richa, Christian Scheideler, Stefan Schmid, Hanjo Täubig. "SKIP+: A Self-Stabilizing Skip Graph." Journal of the ACM, 2014. DOI 10.1145/2629695.
**Retrieved:** full text via https://schmiste.github.io/podc09.pdf
**Source URL:** https://schmiste.github.io/podc09.pdf
**Domain:** A

Retrieval note: the file on disk carries the header "PODC'09, August 10-12, 2009" and the title "A Distributed Polylogarithmic Time Algorithm for Self-Stabilizing Skip Graphs," which is the earlier conference version of this result by the same five authors, presenting the same SKIP+ construction, the same theorem statements (Theorem 3.17, 4.2, 4.3), and the same proofs referenced below. The registry's target record cites the 2014 Journal of the ACM version under the title "SKIP+: A Self-Stabilizing Skip Graph" (DOI 10.1145/2629695), which is stated in HSkip+ (Feldotto, Scheideler, Graffi, P2P 2014) and elsewhere to be the extended journal version of this PODC 2009 paper. Every mechanism, theorem, and proof cited below appears in the retrieved conference text; where the journal version might state a tightened bound or add material not present here, this entry records the conference-version content only and does not claim journal-version-exclusive content.

### What it does
The algorithm restores a valid peer-to-peer overlay topology (a variant of the skip graph, called SKIP+) from any starting network state that is still weakly connected (every node reachable from every other by some path, ignoring edge direction), without any external coordinator and without any node knowing the network size. A skip graph gives every node a unique identifier and a random bit string chosen at join time; a node connects at level i to the nearest node sharing the same i-bit prefix of that random string, for every i, so the graph forms nested groups whose neighbor lists shrink geometrically with level and give logarithmic-diameter routing. SKIP+ extends this definition so that whether a node's current neighbor set is correct can be checked using only information the node and its direct neighbors already hold, which the plain skip graph definition does not allow. The self-stabilizing algorithm, called ALG+, runs as a set of local rules: each node inspects its own state and its current neighbors' states every round, and a rule fires when a Boolean guard over that local state is true, either dropping an edge or asking two neighbors to connect to each other. Rule 1 promotes an edge to a neighbor whose prefix match is currently unmatched at some level to a stable edge. Rule 2 forwards a temporary edge one hop toward a node with a longer matching prefix when the current endpoint is not the correct match. Rule 3a has a node introduce two of its own stable neighbors to each other so they can each check whether the other should become their own neighbor. Repeated local application of these three rules, with no node ever learning the network size or any global topology fact, converges to a valid SKIP+ graph.

### Measured results
This is a proof-based theory paper; it reports no empirical measurement, testbed, or simulation. Every quantitative claim is an asymptotic worst-case bound proved for the synchronous message-passing model defined in section 1.2 (time proceeds in discrete rounds; every message sent in round i is delivered at the start of round i+1; a node communicates only with nodes it currently holds a link to).

| Result | Bound | Conditions |
|---|---|---|
| Full construction from an arbitrary weakly connected graph (Theorem 3.17) | O(log^2 n) rounds, with high probability | n = number of nodes; synchronous round model; starting graph only required to be weakly connected, otherwise arbitrary |
| Single node leave, starting from an already-valid SKIP+ graph (Theorem 4.2) | O(log n) rounds and O(log^4 n) total messages/edge-insertions across all affected nodes, with high probability | Same model; only the departing node's direct neighbors (bounded to O(log n) of them by Lemma 4.1) need to change their neighbor set |
| Single node join, starting from an already-valid SKIP+ graph (Theorem 4.3) | O(log n) rounds and O(log^4 n) total work, with high probability | Same model; the joining node initially knows one arbitrary existing node u and is integrated level by level |
| Node degree in a valid SKIP+ graph (Lemma 4.1) | O(log n), with high probability | Follows from the random bit string assigned to each node at join, independent of round model |

"With high probability" in this paper's usage means the stated bound holds with probability at least 1 - 1/n^c for a constant c that can be made arbitrarily large by adjusting constants in the proof (stated directly in the Lemma 4.1 proof).

### Parameters
- Random bit string length per node: not fixed to a specific value in the text; required only to be "of sufficient length" so that no two nodes are given the same prefix beyond level H = Theta(log n), the paper's own upper bound on the number of levels that holds with high probability.
- No tunable protocol parameter (bucket size, replication factor, fan-out) appears; the algorithm has no configuration knobs distinct from the model assumptions above.

### Stated limitations
The paper's own conclusion states it as an open question whether the number of actions any single node must be prepared to take, per round, is bounded by a polylogarithmic function of n; the authors state they have not derived such a bound and identify finding one, along with the algorithmic changes it would need, as future work. The self-stabilization proof and the round model both use a purely synchronous message-passing assumption defined in section 1.2 (all messages sent in a round are delivered together at the start of the next round); the paper does not analyze or claim its bounds under an asynchronous message-delivery model. The join and leave results (Theorems 4.2, 4.3) assume the graph is already a valid SKIP+ structure before the single join or leave event; they do not bound recovery time under concurrent joins and leaves, only the combined-arbitrary-state case of Theorem 3.17, which does not distinguish concurrent operations from an adversarial starting state.

### Requirements it places on the rest of the system
Every node must have an immutable, globally unique identifier and an independently, uniformly randomly chosen bit string of sufficient length assigned at join time; the self-stabilization proof (Lemma 3.1 onward) depends on these random strings to bound node degree and convergence time, so a system that assigns non-random or attacker-chosen bit strings to nodes voids the stated bounds. The synchronous round model (section 1.2) requires that a global round boundary exists across all participating nodes, or at minimum that message delivery times are bounded such that a round-based analysis translates to bounded real time; the paper does not supply that translation itself. A node must be able to inspect the full state of its current direct neighbors on demand — the algorithm's guards are Boolean predicates over "the state of the executing node and its neighbors" — so the transport layer underneath must expose neighbor state, not just message passing. The algorithm assumes every participating node executes the stated rules honestly; no Byzantine-fault or adversarial-node model is analyzed anywhere in the text, only arbitrary (non-adversarial) initial topology.

### Contradicts
None found. This entry cannot be checked against HSkip+'s claimed improvement (O(log^2 n) messages versus this paper's O(log^4 n) rounds) because HSkip+'s own bound is a message count under asynchronous message passing, a different model from this paper's round count under synchronous message passing; the two figures measure different quantities under different models and are not a direct disagreement.

### References worth retrieving
- Aspnes, Shah, "Skip graphs," ACM Transactions on Algorithms 3(4), 2007 — foundational (the skip graph structure SKIP+ extends)
- Clouser, Nesterenko, Scheideler, "Tiara: A self-stabilizing deterministic skip list," SSS 2008 — competing (prior self-stabilizing skip list, cited as not achieving sublinear time)
- Onus, Richa, Scheideler, "Linearization: Locally self-stabilizing sorting in graphs," ALENEX 2007 — foundational (linearization technique this paper's approach builds past)
- Stoica, Morris, Karger, Kaashoek, Balakrishnan, "Chord: A scalable peer-to-peer lookup service for internet applications," MIT-LCS-TR-819, 2001 — foundational / competing (cited for its own partial degenerate-state recovery protocols)
- Maymounkov, Mazières, "Kademlia: A peer-to-peer information system based on the XOR metric," IPTPS 2002 — foundational (already in corpus)
- Harvey, Jones, Saroiu, Theimer, Wolman, "SkipNet: A scalable overlay network with practical locality properties," USITS 2003 — competing (alternative skip-structure overlay)
- Goodrich, Nelson, Sun, "The rainbow skip graph: A fault-tolerant constant-degree distributed data structure," SODA 2006 — competing (alternative fault-tolerant skip graph variant)

### Verbatim extracts
- "constructs a (variant of the) skip graph in polylogarithmic time from any initial state" (abstract)
- "individual joins and leaves are handled locally and require little work" (abstract)
- "the standard synchronous message-passing model" (section 1.2)
- "the self-stabilizing algorithm ALG+ constructs SKIP+ in O(log2n) rounds" (Theorem 3.17)
- "it takes O(logn) rounds ... and O(log4n) total work w.h.p." (Theorem 4.2)
- "we do not have a polylogarithmic bound on the enabled actions per node and round" (conclusion)
