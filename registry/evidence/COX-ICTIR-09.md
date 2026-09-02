## [COX-ICTIR-09] Probably Approximately Correct Search

**Citation:** Ingemar J. Cox, Ruoxun Fu, Lars Kai Hansen. "Probably Approximately Correct Search." ICTIR 2009 (LNCS 5766). Pages 2-16. DOI 10.1007/978-3-642-04417-5_2.
**Retrieved:** full text via http://www0.cs.ucl.ac.uk/staff/ingemar/Content/papers/2009/ictir09.pdf
**Source URL:** http://www0.cs.ucl.ac.uk/staff/ingemar/Content/papers/2009/ictir09.pdf
**Domain:** B

### What it does
The paper gives an analytic model for how closely a search system built from independent, non-cooperating computers can match a deterministic, fully-indexed search system, using less coordination. Each of K computers independently and uniformly samples n documents (without replacement, on that one computer) from a collection of N total documents to build its local index -- the acquisition stage. A query goes to a randomly chosen subset of k' computers, and their results merge into one result set -- the retrieval stage. Modeling document sampling as an urn-and-balls process, the paper derives the expected coverage (the fraction of the N-document collection present in the union of all K computers' samples) as a closed-form function of N, n, and K, and separately derives the expected number of documents from a deterministic top-r result list that appear in the sampled system's top-r result list, as a function of N, n, and k' (the query fan-out). The measure of retrieval quality is this expected overlap with the deterministic result list, not any ground-truth relevance judgment; the deterministic system is treated as the target the sampled system is judged against.

### Measured results
| Result | Conditions |
|---|---|
| Expected coverage approx 1 (near-total) when 300,000 machines each independently sample 0.1% of the collection | Analytic instance modeled on a claimed Google configuration: N unspecified numerically, n/N = 1/1000, K = 300,000 (1000 partitions x 300 replicas per partition, per a cited source) |
| Expected retrieval overlap P(d'_i) approx 0.63 when a query goes to k'=1000 machines, each holding 1/1000 of the collection | Same modeled Google-scale configuration; overlap defined as probability a specific document is present in the union of k' machines' samples |
| Expected overlap in the top-10 results, E(r') = 6.3 documents out of 10 | Derived from P(d'_i)=0.63, r=10, via E(r')=r*P(d'_i) |
| Distribution of exact top-10 overlap counts: P(0 matches)=0.0000452, P(6 matches)=0.245 (highest), P(10 matches)=0.0102, P(5 or more matches) over 88% | Binomial distribution with P(d'_i)=0.63, r=10 (paper's Table 1) |
| Sending the query to 2000 machines instead of 1000 raises correctness to 86%, at the cost of halving query throughput | Same modeled configuration, k' doubled from 1000 to 2000, n/N = 1/1000 held fixed |
| Peer-to-peer configuration: coverage = 0.947 | Modeled instance: K=1,000,000 machines, each with 1GB storage, indexing n=50,000 documents (20KB/document assumed), collection size N=17 billion documents |
| Peer-to-peer configuration: retrieval overlap P(d'_i) = 0.03, expected top-10 overlap E(r')=0.3 documents | Same 1,000,000-machine configuration, query sent to k'=10,000 machines |
| Reaching 63% PAC performance in the 1,000,000-machine, 17-billion-document configuration requires querying 340,000 machines, or increasing per-machine capacity to 340GB (yielding P(d'_i)=0.63 at k'=1000) | Same modeled configuration, two alternative fixes analyzed algebraically, not simulated |
| BubbleStorm's independently derived match probability formula (1 - e^(-k'g/K), g = document replication count) gives 0.03 under the same 1,000,000-machine parameters, matching this paper's PAC estimate | Cross-check against Terpstra et al.'s BubbleStorm formula, same K, k', and derived g approx 3 |
| Simulated coverage matches analytic expectation closely: Simulation 1 expectation 0.6323 vs average 0.6322 (std dev 0.0003); Simulation 2 expectation 0.8648 vs average 0.8648 (std dev 0.0004); Simulation 3 expectation 0.8347 vs average 0.8346 (std dev 0.0004) | Three simulations, 20 trials each. Sim 1: synthetic collection N=1,000,000 document IDs, n=1000, K=1000. Sim 2: same but K=2000. Sim 3: TREC45 dataset, N=556,079 documents, n and K as in Sim 1; 100 random test queries per trial, top-10 ranking compared against the full-collection deterministic result |
| Simulated query-performance (retrieval overlap) also concentrates near expectation: Simulation 1 expectation 0.6323 vs average 0.6264 (std dev 0.0135); Simulation 2 expectation 0.8648 vs average 0.8636 (std dev 0.0124); Simulation 3 expectation 0.8347 vs average 0.8377 (std dev 0.007) | Same three simulation configurations as above |

### Parameters
- N: collection size (document count) -- stated range for the Web, 17 to 65 billion pages; TREC45 used as N=556,079 in simulation 3
- K: number of computers -- swept from 1000 (Sim 1) to 2000 (Sim 2) to 300,000/1,000,000 in the two analytic worked examples
- n: documents indexed per computer -- 1000 in simulations; 5*10^4 (50,000) in the peer-to-peer analytic example, derived from an assumed 1GB per-machine capacity, 1000 terms/document, 20 bytes/posting
- k': number of computers a query is sent to (query fan-out) -- swept 1000 to 2000 in the search-engine example; 10,000 in the peer-to-peer example; the paper computes that 340,000 is required to reach 63% correctness at n=50,000, N=17 billion
- r: number of top results compared, fixed at r=10 throughout the worked examples and Table 1
- Simulation trial count: 20 trials per configuration; 100 test queries per trial

### Stated limitations
The paper states retrieval-model identity is assumed between the deterministic and non-deterministic systems, and that this assumption is not verified: "Future work is needed to determine if, and under what conditions, the statistics of the local samples will be sufficiently close to the statistics of the overall collection," because most retrieval models set parameters from collection statistics that each computer can observe only locally under this scheme. The peer-to-peer configuration's poor overlap (0.03 at k'=10,000) is attributed by the paper to insufficient per-machine storage capacity relative to collection size, not to any flaw in the random-sampling mechanism itself; the paper states that raising per-machine capacity to 340GB restores 63% correctness at the search-engine's query fan-out, but states this capacity is "unlikely" to be available on most peers. The paper states that because queries go to a randomly selected subset of machines, the same query issued twice can return different result sets, which the paper states "users may find this disconcerting," and proposes (without evaluating) hashing the query to a pseudo-random, repeatable machine subset as an unevaluated mitigation. The model assumes computer homogeneity for simplicity, though the paper states this is "not needed in practice" without demonstrating the heterogeneous case. Caching of query results is listed as unanalyzed future work.

### Requirements it places on the rest of the system
Each participating computer must be able to draw an unbiased random sample of documents from the full collection during acquisition; the paper states this capability is "difficult, but certainly possible" and does not itself provide a mechanism, only assumes one for the decentralized case (the centralized case can substitute a single centralized crawler with random, non-disjoint partitioning). The query-issuing side must be able to select a random (or query-hashed pseudo-random) subset of k' computers to query; the paper's own numbers show this fan-out must scale with N/n -- the ratio of collection size to per-machine capacity -- to hold accuracy constant, so any deployment must track that ratio to size k' correctly. The retrieval-quality metric (expected overlap with a deterministic top-r list) presupposes that a deterministic full-index baseline exists, or is at least computable in analysis, against which "approximately correct" is defined; the paper does not define correctness against ground-truth relevance independent of that deterministic baseline.

### Contradicts
None found against other entries in this batch as of this extraction.

### References worth retrieving
- Li, Loo, Hellerstein, Kaashoek, Krager (Karger), Morris. "On the feasibility of peer-to-peer web indexing and search." IPTPS 2003. -- foundational (the paper's own citation for the peer-to-peer 1-million-machine, 10,000-query-fanout parameters used in the worked example)
- Raiciu, Huici, Handley, Rosenblum. "ROAR: Increasing the flexibility and performance of distributed search." SIGCOMM 2009. -- competing
- Reynolds, Vahdat. "Efficient peer-to-peer keyword searching." Middleware 2003. -- competing
- Skobeltsyn, Luu, Zarko, Rajman, Aberer. "Web text retrieval with a p2p query-driven index." SIGIR 2007. -- competing
- Terpstra, Kangasharju, Leng, Buchmann. "BubbleStorm: resilient, probabilistic, and exhaustive peer-to-peer search." -- competing (independently derived match-probability formula that the paper cross-checks its own PAC estimate against)
- Tang, Xu, Mahalingam. "pSearch: Information retrieval in structured overlays." HotNets-I 2002. -- competing
- King, Saia. "Choosing a random peer." PODC 2004. -- foundational (random-sampling primitive this paper's model assumes)
- Barroso, Dean, Holzle. "Web search for a planet: The Google cluster architecture." IEEE Micro 23(2), 2003. -- foundational (source of the 1000-partition/300-replica Google configuration this paper's worked example uses)

### Verbatim extracts
"the performance of our PAC IR system is approximately 63% of the deterministic system"
"Users may find this disconcerting"
"it would not be necessary to for each machine to independently sample the Web"
"Future work is needed to determine if, and under what conditions"
"there is a 63% chance that it is present in a subset of 1000 randomly chosen nodes"
