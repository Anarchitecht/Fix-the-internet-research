## [ZHOU-EPRINT-24] Pacmann: Efficient Private Approximate Nearest Neighbor Search
**Citation:** Mingxun Zhou, Elaine Shi, Giulia Fanti. "Pacmann: Efficient Private Approximate Nearest Neighbor Search." IACR Cryptology ePrint Archive 2024/1600, 2024.
**Retrieved:** full text via https://eprint.iacr.org/2024/1600.pdf
**Source URL:** https://eprint.iacr.org/2024/1600
**Domain:** B

### What it does
Pacmann lets a client run approximate-nearest-neighbor (ANN) search over a server-held vector database while the server learns nothing about the query vector. The client, not the server, runs the graph traversal: it holds a private-information-retrieval (PIR) hint built during a one-time preprocessing pass, and at each hop of the search it issues PIR queries to fetch only the neighbor list and vectors of the current graph vertex, computes distances locally, and picks the next vertex itself. Because the server never sees which vertex indices are fetched, it cannot infer the query's topic from access patterns.

The graph the client searches is built by the server from a customized construction, not an off-the-shelf HNSW (hierarchical navigable small world) or DiskANN graph. The construction enforces a directed, exactly-C-out-regular graph, because a non-uniform out-degree would leak information about a vertex's cluster from the number of PIR queries a hop causes. Build proceeds in three parts: for each vector, find 2C approximate neighbors with an existing ANN library, trim to C with the sparse-neighborhood-graph (SNG) heuristic (sorted by distance, discarding a candidate that lies closer to an already-kept candidate than to the vertex itself, for diversity), add edges in both directions, then re-balance in-degree by keeping each directed edge (x -> y) with probability C / InboundDegree(y) and re-filling or re-trimming each vertex's outbound edges to exactly C.

Retrieval uses Piano, a single-server PIR scheme from the client-preprocessing PIR family: the client streams the whole encoded database once during preprocessing (linear cost, amortized across all later queries) and in exchange gets sublinear per-query computation and communication of order the square root of the database size, with client storage of the same order. The paper adds three optimizations on top of the base construction: beam search (m parallel graph paths per query instead of one, cutting the hops needed for a given recall), fast starting (sqrt(n) precomputed starting vertices the client downloads once, instead of one fixed entry point), and batched PIR (a single round issues all of one hop's neighbor-list queries together, splitting the database into B partitions and querying Q/B times per partition to keep per-query privacy). Together the paper reports a 76% reduction in computation and a near-70% reduction in end-to-end latency from these three optimizations on the ablation configuration below.

### Measured results

| Metric | Value | Conditions |
|---|---|---|
| Search-success-rate improvement over clustering baseline | 63% vs 29% (2.1x) | MS-MARCO dataset, finding the single most relevant document, Pacmann vs. Tiptoe/Wally-style clustering-based private ANN |
| Recall@10 improvement over Tiptoe | 2.5x | 100-million-vector SIFT dataset |
| Quality reached vs. non-private baseline | ~90% of NGT's recall/MRR | both SIFT and MS-MARCO, non-private baseline is NGT (Neighborhood Graph and Tree), a state-of-the-art non-private graph ANN library |
| Latency at 100M records, LAN | 1.6 s (Pacmann) vs >=4 s (Tiptoe), 60% reduction | LAN setting = 5 ms round-trip time (RTT), single 2.4 GHz Intel Xeon E5-2680 CPU, 256 GB RAM, single thread |
| Latency at 100M records, WAN | 3.1 s (Pacmann) vs >=4 s (Tiptoe), 22% reduction | WAN setting = 50 ms RTT, same hardware |
| Crossover point where Pacmann beats the linear-scan latency baseline | database >5M vectors (LAN), database >50M vectors (WAN) | SIFT dataset scaled from 2M to 100M vectors, quality held fixed at 0.90 recall@10 |
| Detailed cost breakdown, WAN setting, 90% quality target | see table below | MS-MARCO = 3.2M documents reduced to 768-dim sentence-BERT then PCA to 192-dim; SIFT = 100M 128-dim vectors; 16 threads for graph build, 1 thread otherwise |

Detailed breakdown (Table 1 of the paper, WAN setting, both at ~90% of non-private quality):

| Stage | MS-MARCO (3M) | SIFT (100M) |
|---|---|---|
| Graph build time (server, one-time) | 8.5 min | 343.5 min |
| PIR preprocessing time (per client) | 9.1 s | 271.6 s |
| PIR preprocessing communication | 2.7 GB | 59.6 GB |
| Online query latency | 1.1 s | 3.0 s |
| Online query computation time | 0.10 s | 1.48 s |
| Online query communication | 3.1 MB | 14.4 MB |
| Rounds per query | 20 | 32 |
| Per-query maintenance time | 0.19 s | 1.99 s |
| Per-query maintenance communication | 60.1 MB | 399.4 MB |
| Client storage | 0.6 GB | 2.9 GB |
| Quality achieved | 0.266 MRR@100 | 0.90 recall@10 |
| Beam width m | 3 | 4 |

Ablation on a 10-million-vector SIFT subset (WAN setting): beam search alone cuts the rounds needed for 0.90 recall@10 by 3x; adding fast-starting cuts rounds a further 20%; adding batched PIR cuts per-round computation time 4x but introduces query failures that trade off against a small increase in round count.

Alternative-PIR comparison, 10-million-vector SIFT subset: substituting SimplePIR for Piano drops preprocessing communication from about 6 GB to about 300 MB but the paper's own estimate raises online per-query latency from 1.5 s to about 90 s (measured SimplePIR throughput ~10 GB/s on the same server, 25 rounds of 96 parallel queries against a 6 GB per-partition sub-database with 16-way batching).

### Parameters
- Graph out-degree C = 32 (fixed for both datasets in the main evaluation).
- Piano PIR security parameter: 128-bit.
- Batched-PIR partition count B = 16, batch size Q = 32 queries per round.
- Beam search width m = 3 (MS-MARCO) or m = 4 (SIFT-100M), tuned per dataset to hit the 90%-of-non-private-quality target.
- Exploration rounds (max hop count H, tuned per data point to reach target recall): 20 for MS-MARCO, 32 for SIFT-100M; the paper states round count grows roughly logarithmically with database size from 2M to 100M vectors.
- Fast-start vertex count: sqrt(n) preprocessed starting vertices, sampled once and downloaded by the client.
- Network settings tested: LAN = 5 ms RTT; WAN = 50 ms RTT.
- Database sizes tested: SIFT scaled from 2 million to 100 million 128-dimensional vectors (1,000 top-10 test queries per configuration); MS-MARCO fixed at 3.2 million documents (5,000-plus test queries, reported over the first 1,000).

### Stated limitations
The scheme requires the client to download the entire indexing-graph database during preprocessing in a streaming fashion (linear communication even though later per-query cost is sublinear), so the authors state it is unsuitable for network-constrained clients. It does not support dynamic updates to the database — insertions or deletions after the preprocessing pass — which the authors describe as an open problem in the PIR literature generally, not one this paper solves. The construction assumes the database itself is public (every client may learn its contents); it provides no server-side privacy, i.e., no protection of the database contents from the client. The security proof covers only a semi-honest (honest-but-curious) server; extension to a malicious server is left as future work. Preprocessing throughput assumes a good network connection (the paper's own preprocessing-time figures assume roughly 1 Gbps).

### Requirements it places on the rest of the system
- The graph the client searches must be built server-side with a fixed, uniform out-degree C for every vertex; an ANN index with irregular vertex degree (as ordinary HNSW or DiskANN indexes have) leaks information through the PIR access pattern and cannot be substituted without first regularizing it by the paper's build procedure.
- The underlying retrieval primitive must be a client-preprocessing single-server PIR scheme (the paper uses Piano) that supports batched multi-query rounds; this requires every client to complete a linear-cost, linear-communication preprocessing pass — a full streaming download of the encoded graph — before making any query, and to refresh that preprocessing state once its stored hints are exhausted.
- The database is assumed static during the query phase; any component that mutates the vector database (adds or removes vectors) after clients have preprocessed invalidates client-held PIR hints, and the paper supplies no mechanism to reconcile that.
- The privacy guarantee holds only against a single, semi-honest server; a design that needs protection against an actively malicious server, multiple colluding servers, or protection of the database contents themselves (not just the query) cannot rely on this mechanism as specified.
- Achieving the paper's latency figures assumes a good-bandwidth client link (the paper's own numbers assume approximately 1 Gbps); a client on a constrained or metered link faces the multi-gigabyte-to-tens-of-gigabytes preprocessing download stated above.

### Contradicts
None found against other entries in this corpus. Internally, the paper corrects its own earlier draft: an initial version of its cost table reported MS-MARCO online communication as 1.5 MB/query; the corrected figure recorded in the released table is 3.1 MB/query (stated in the paper's own correction note).

### References worth retrieving
- **HDCG+23** — Henzinger, Dauterman, Corrigan-Gibbs, Zeldovich, "Private Web Search with Tiptoe," SOSP 2023 — competing: the paper's main baseline for private search quality and latency; Pacmann's own numbers are calibrated against Tiptoe's reported figures.
- **ABG+24** — Asi et al., "Scalable Private Search with Wally," arXiv 2406.06761, 2024 — competing: relaxes Tiptoe's cryptographic privacy to differential privacy using batches of anonymous queries; a direct alternative point in the privacy/efficiency tradeoff space.
- **SSLD22** — Servan-Schreiber, Langowski, Devadas, "Private Approximate Nearest Neighbor Search with Sublinear Communication" (Preco), IEEE S&P 2022 — competing: uses locality-sensitive hashing and a two-non-colluding-server assumption; a different trust-model point.
- **ZPZP24** — Zhu, Patel, Zaharia, Popa, "Compass: Encrypted Semantic Search with High Accuracy," ePrint 2024/1255 — competing: solves a related but distinct problem (client-supplied encrypted database with per-client server-side state, using HNSW plus Path ORAM) rather than a public shared database.
- **ZPSZ24** — Zhou, Park, Shi, Zheng, "Piano: Extremely Simple, Single-Server PIR with Sublinear Server Computation," IEEE S&P 2024 — foundational: the PIR primitive Pacmann builds on directly.
- **BIM00** — Beimel, Ishai, Malkin, "Reducing the Servers' Computation in Private Information Retrieval: PIR with Preprocessing," CRYPTO 2000 — foundational: proves the Omega(n) lower bound for PIR without preprocessing that motivates the whole client-preprocessing approach.
- **HHCG+22** — Henzinger, Hong, Corrigan-Gibbs, Meiklejohn, Vaikuntanathan, "One Server for the Price of Two" (SimplePIR), ePrint 2022/949 — competing: an alternative single-server PIR the paper benchmarks as a substitute for Piano, with a measured 20x preprocessing-communication reduction traded against a ~60x online-latency increase.
- **MY18** — Malkov, Yashunin, "Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs" (HNSW), TPAMI 2018 — foundational: the non-private graph-ANN family whose blueprint Pacmann's graph search follows before privacy is added.
- **JSDS+19** — Jayaram Subramanya et al., "DiskANN: Fast Accurate Billion-Point Nearest Neighbor Search on a Single Node," NeurIPS 2019 — foundational: another graph-ANN baseline; source of the "distant neighbor for diversity" edge-selection idea Pacmann's graph-build procedure cites.
- **DGM+24** — Diwan, Gou, Musco, Musco, Suel, "Navigable Graphs for High-Dimensional Nearest Neighbor Search: Constructions and Limits," arXiv 2405.18680, 2024 — foundational: theoretical navigable-graph degree/hop bound the paper's own theoretical-implications section builds on.

### Verbatim extracts
- "reaching 90% quality of a state-of-the-art non-private ANN algorithm"
- "up to 62% reduction in computation time and 22% reduction in overall latency"
- "does not naturally support dynamic updates to the database"
- "Pacmann is designed under the assumption that the database is public"
- "we do not consider server-side privacy"
- "we assume the adversary is semi-honest"
- "our scheme is more suitable for a client with a good network connection"
