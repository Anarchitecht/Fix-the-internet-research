## [NEAGUE-ARXIV-25] Semantica: Decentralized Search using a LLM-Guided Semantic Tree Overlay
**Citation:** Petru Neague, Quinten Stokkink, Naman Goel, Johan Pouwelse. "Semantica: Decentralized Search using a LLM-Guided Semantic Tree Overlay." arXiv:2502.10151, 2025.
**Retrieved:** full text via https://arxiv.org/pdf/2502.10151
**Source URL:** https://arxiv.org/abs/2502.10151
**Domain:** B

### What it does
Semantica routes a search query to the peer most likely to hold a semantically matching document, without any peer holding a global index of where documents reside. It builds a semantic overlay network (a peer topology in which peers with similar content connect to each other) by embedding each peer's documents with a pre-trained large language model (LLM, a language model trained on large text corpora) and organizing peers into a prefix tree (trie) keyed on those embeddings, in place of the exact-key hashing a distributed hash table (DHT) uses.

Tree construction: peers join sequentially at a root node; a leaf node that exceeds a capacity of L = 50 users runs 2-means clustering on the member embeddings and splits into two child nodes, each peer reassigned to the child whose centroid its embedding is closest to. A peer whose distance to the two child centroids differs by less than a threshold delta is cloned into both children (soft clustering), so a peer near a cluster boundary keeps neighbors on both sides of the split. One peer per split-node acts as custodian, storing that split's centroids and the network addresses of the corresponding child nodes, chaining custodians from root to leaf so a joining peer can descend the tree without a global index.

Each peer maintains a "known-users" list (peers reachable through proximity in the same or a nearby leaf) and derives from it a "closest-users" list of its n_cu most cosine-similar peers. Peers refine this list through neighbor-expansion rounds: a peer queries a random member of its known-users list for peers closer to itself in embedding space, repeating for a fixed number of rounds or until the list stabilizes.

Query resolution (chain-hopping): a query (itself an embedding) is sent to the peer whose embedding is closest to it. If that peer lacks a matching document, it forwards the query to the known-users-list neighbor with the highest cosine similarity to the query, repeating up to a maximum hop count. The paper assumes perfect local search — a peer holding the queried document returns it with 100% reliability, and a peer lacking it reports so with 100% reliability — and states this assumption is made to keep local search out of scope, so the reported accuracy measures routing, not local retrieval.

### Measured results

| Metric | Value | Conditions |
|---|---|---|
| Closest-user recall at initialization (before any expansion round) | Semantica > 5 (absolute count out of a possible 50) vs. random-baseline ~0.4 | AOL4PS dataset filtered to 6,978 users with >=1 co-occurring document; ground truth = each user's global top-50 cosine-similarity peers over the whole dataset; delta in {0, 5e-4, 1e-3} tested |
| Closest-user recall after 10 expansion rounds | Semantica ~35 (delta=0.001) or ~30 (delta=0.0005) vs. random-baseline ~5 | same setup; random baseline = same known-users list size as the delta=0.001 configuration before expansion, but randomized membership, run through the identical expansion-round algorithm |
| Closest-user recall after 20 expansion rounds | "almost all" required users, i.e. >40 of 50, for every delta value tested | same setup |
| Clone count per user | median 1, mean 1.32, std 0.64 at delta=0.001; mean 7.45, std 8.08 at delta=0.005 | AOL4PS, full delta sweep from 0 to 5e-3 given in the paper's Table II; ~5,100 of 6,980 users have zero clones at delta=0.001 |
| Two-hop document-retrieval rate | Semantica 12.75% vs. <6% for random-query baseline and for graph-diffusion (personalized-PageRank-style) baseline at any tested teleportation/alpha value | AOL4PS, query chain-hopping vs. Giatsoglou et al.'s graph-diffusion algorithm on a Barabasi-Albert graph with matched mean degree (m=104, chosen to match Semantica's mean known-users count of ~208); delta=0.003, 10 expansion rounds for Semantica; gap between Semantica and the alternatives narrows as the query-hop/query-count budget rises toward 200-600 |
| Graph-diffusion alpha ordering | alpha=1.0 > alpha=0.9 > alpha=0.5 > alpha=0.1 in retrieval accuracy | same setup; higher alpha means less diffusion, so the paper's own result is that adding diffusion degrades retrieval accuracy relative to the plain random-graph chain-hop baseline |
| Minimum-hop-distance shift to nearest document holder | Semantica's tree shifts many documents from a distance greater than 1 to a distance of exactly 1, at the cost of shifting some documents from distance 2 to distance 3 (occasionally 4-5), and makes some documents completely unreachable (disconnected subgraphs) | comparison of a Semantica-built directed graph (delta=0.001, 10 expansion rounds) against a Barabasi-Albert random graph with matched mean degree (m=86) |
| Abstract-level headline figures | "up to ten times more semantically similar users" found; "more than two times the number of relevant documents" retrieved at same network load | These are the paper's own summary of the closest-user-recall and document-retrieval experiments above, not separate measurements |

Dataset: AOL4PS, 187,521 websites accessed by 12,907 users over three months of 2006, 1,339,101 total queries; filtered to users with at least 30 unique documents in history, then to the 6,978 users sharing at least one document with another user; each user's documents split into a 10-document test set and a training set used to compute the user's mean document embedding via BERT (Bidirectional Encoder Representations from Transformers).

### Parameters
- Leaf capacity before split: L = 50 users.
- Soft-clustering clone threshold: delta, swept over {0, 1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 3e-3, 5e-3} for the clone-count measurement; {0, 5e-4, 1e-3} for the recall-vs-expansion-rounds measurement; delta=0.003 used for the document-retrieval experiment.
- Expansion rounds: swept from 0 to 20 for the recall experiment; 10 rounds fixed for the document-retrieval and hop-distance experiments.
- Closest-users list size n_cu: not given a fixed numeric value in the excerpted sections; the comparison graphs are built to match Semantica's own resulting mean known-users count (~208 in the retrieval experiment, giving Barabasi-Albert m=104; ~86-average-degree in the hop-distance experiment, giving Barabasi-Albert m=86).
- Maximum query hops (chain-hopping): swept from 2 to 600 queries/hops in the retrieval-accuracy comparison.
- Embedding dimensionality: 768 (BERT), held constant and not varied.
- Graph-diffusion teleportation/alpha values compared: 0.1, 0.5, 0.9, 1.0.

### Stated limitations
The paper assumes perfect local search (100% true-positive and true-negative retrieval on a peer's own document set) and states this is a deliberate scope exclusion, not a claim that local search is solved. It assumes users have document overlap (co-occurrence) with at least one other user and validates this only on the AOL4PS dataset; it does not test datasets without such overlap. At delta = 0 (no cloning), the authors report expansion rounds do not improve recall, because same-leaf peers then share identical neighbor lists and querying them returns redundant information — cloning is required for expansion rounds to work at all in this design. The tree provides no re-balancing mechanism for peer departures; the authors state that without one, sustained churn could leave leaf nodes badly depopulated and degrade the tree toward its worst-case O(N) height (versus average-case O(log N)), negating the claimed complexity advantage — and state this re-balancing is out of scope for the paper. Custodian departure makes that custodian's centroid data unavailable, with no backup-custodian election implemented (described as a potential extension, not built). The experiments do not rank retrieved results; the authors state ranking could be done locally by the querying peer via cosine similarity but did not implement or measure it. At high hop/query budgets (up to 200-600), the tree-structured graph's advantage over a random comparison graph narrows and the authors state the random graph eventually overtakes it, because some documents become entirely unreachable in the tree-derived graph due to disconnected subgraphs.

### Requirements it places on the rest of the system
- Every peer must be able to compute or obtain an embedding for its own documents (locally via an LLM, or via an external embedding service) and for each incoming query, in a shared embedding space, before this mechanism can route anything.
- The mechanism assumes perfect local search at each peer: the rest of the system must supply an exact-match or near-exact local retrieval routine over each peer's own stored documents, since Semantica's measured accuracy is routing accuracy layered on top of an assumed-perfect local answer.
- The overlay depends on out-of-band bootstrap discovery of at least one root peer (via a bootstrap server, a public DHT, or a known reference address); this mechanism does not itself solve peer discovery for a cold-started network.
- The custodian scheme requires each split-node's centroid and address data to be held reliably by a designated peer with no replication built in; any component relying on this tree for routing must tolerate lookups failing for a period after a custodian departs, or must supply its own custodian-replication mechanism, since none is built here.
- The mechanism requires peer document sets to overlap; a corpus of purely disjoint per-peer documents (no shared interest signal) does not fit the design's stated operating assumption and was not evaluated.
- Recall performance depends on soft-clustering (a nonzero delta) being enabled together with expansion rounds; a deployment that disables cloning to save the modest per-user duplication cost also disables the mechanism by which expansion rounds improve recall.

### Contradicts
None found against other entries in this corpus. Note for synthesis: the paper's own graph-diffusion comparison (Giatsoglou et al., personalized-PageRank-style diffusion) shows diffusion degrading retrieval accuracy relative to a no-diffusion baseline at every tested alpha, which is presented as confirming, not contradicting, the diffusion paper's own reported alpha ordering.

### References worth retrieving
- **Crespo & Garcia-Molina, "Semantic Overlay Networks for P2P Systems," AP2PC 2004** — foundational: the original semantic-overlay-network concept this paper extends with LLM embeddings in place of an unspecified similarity function.
- **Giatsoglou, Krasanakis, Papadopoulos, Kompatsiaris, "A Graph Diffusion Scheme for Decentralized Content Search Based on Personalized PageRank," ICDCSW 2022** — competing: the query-mechanism baseline directly benchmarked against Semantica's chain-hopping, with disagreeing conclusions about the value of diffusion.
- **Tang, Xu, Dwarkadas, "Peer-to-Peer Information Retrieval Using Self-Organizing Semantic Overlay Networks," SIGCOMM 2003** — foundational/competing: an earlier self-organizing semantic overlay cited as already showing "low latency and high accuracy... comparable to centralized approaches," a claim worth checking directly since Semantica's motivation rests partly on it.
- **Tay et al., "Transformer Memory as a Differentiable Search Index" (DSI), NeurIPS 2022** — foundational: the trie-based "Semantically Structured Identifiers" approach this paper's tree design is explicitly modeled after.
- **Neague, Gregoriadis, Pouwelse, "De-DSI: Decentralised Differentiable Search Index," 2024** — foundational (same author group): a prior decentralization step over DSI that this paper states still requires periodic online learning to update its index, a limitation this paper claims to remove.
- **Li, Loo, Hellerstein, Kaashoek, Karger, Morris, "On the Feasibility of Peer-to-Peer Web Indexing and Search," IPTPS 2003** — this is the "standing bound" paper named in BRIEF.md section 8, item 1; the brief already flags it as needing a check for whether anything has overturned its ~6 MB/query bound at web scale — worth cross-referencing against Semantica's per-query communication figures.
- **Maymounkov & Mazieres, "Kademlia," IPTPS 2002** — foundational: the DHT baseline this paper contrasts its trie-based approach against for exact- versus semantic-key routing (already in corpus per BRIEF.md section 7).
- **Stoica et al., "Chord," SIGCOMM 2001 / TON 2003** — foundational: cited as the other classical DHT baseline for exact-key routing.

### Verbatim extracts
- "Semantica finds up to ten times more semantically similar users than current state-of-the-art approaches."
- "Semantica can retrieve more than two times the number of relevant documents given the same network load."
- "we assume that users have perfect search on their own device"
- "Currently, no mechanism was chosen to re-balance the tree if too many users have dropped out."
- "in our experiments, we do not rank the search results"
- "Including any diffusion in the system degrades the retrieval accuracy."
- "some sub-graphs are unconnected to the rest of the network"
