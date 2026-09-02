## [COX-ECIR-10] Improving Query Correctness Using Centralized Probably Approximately Correct (PAC) Search

**Citation:** Ingemar J. Cox, Jianhan Zhu, Ruoxun Fu, Lars Kai Hansen. "Improving Query Correctness Using Centralized Probably Approximately Correct (PAC) Search." ECIR 2010. DOI 10.1007/978-3-642-12275-0_25.
**Retrieved:** full text via http://www0.cs.ucl.ac.uk/staff/ingemar/Content/papers/2010/ecir2010.pdf
**Source URL:** http://www0.cs.ucl.ac.uk/staff/ingemar/Content/papers/2010/ecir2010.pdf
**Domain:** B

### What it does
The paper improves the accuracy of Probably Approximately Correct (PAC) search -- a search architecture (introduced in COX-ICTIR-09) in which each of K computers independently indexes a random sample of n documents from a collection of N, and a query is answered by consolidating results from a randomly chosen subset of k computers -- for queries that repeat. It replaces the original architecture's per-user random computer selection with one centralized coordination node that selects the k computers for a query pseudo-randomly, seeded by the query itself, so the same query always reaches the same initial computer set regardless of which user issues it. For a query seen before, the coordinator retains the subset of the previous iteration's computers that scored best (the "keep ratio," a percentage that increases with each repeat occurrence) and fills the remaining query slots with newly pseudo-random computers, so the working computer set for a frequently repeated query iteratively converges toward the computers holding the most relevant documents for it. Two scoring functions for ranking a computer's contribution are given: a simple count of that computer's documents in the top-r merged result list, and a Normalized Discounted Cumulative Gain (nDCG)-like score that weights a computer's contribution by the rank position of its documents (score s_j = sum over rank positions m=1..r of delta_m / log2(1+m), where delta_m is 1 if the document at rank m came from computer j).

### Measured results
| Result | Conditions |
|---|---|
| Baseline (iteration 1) PAC accuracy = 63%, and 88% chance of 5+ of top-10 documents matching a deterministic system | Analytic result carried over from COX-ICTIR-09, restated here: n/N=0.001, k=1000, modeled on a Google-scale K=300,000 configuration |
| With known relevant-document count and r=1000, the iterative keep-ratio algorithm closely tracks the theoretical upper bound on accuracy and reaches 99% accuracy in 15 iterations | Simulation with N=100,000, n=100 (n/N=0.001 held fixed, generalizes to larger N,n at same ratio), K=300,000, k=1000; relevant document set of size r randomly drawn from N; keep ratio starts at x=20%, incremented y=3% per iteration; 10 trials averaged |
| Accuracy degrades from the theoretical upper bound as r increases: worse tracking at r=2,000 and r=4,000 than at r=1,000, though accuracy still improves every iteration in all cases | Same simulation setup, r swept across 1,000 / 2,000 / 4,000; expected relevant documents per computer = n*r/N = 1, 2, 4 respectively |
| At r=4,000, increasing query fan-out from k=1,000 to k=2,000 raises initial (iteration-1) accuracy from 63% to 86% and makes the iterative curve track the theoretical upper bound much more closely | Same simulation, r fixed at 4,000, k compared at 1,000 vs 2,000, 10 trials each |
| TREC-8 experiment, simple-count pruning: retrieval accuracy (PAC metric / deterministic metric) rises from 67% to 81% in the first 5 iterations, reaching 88% at iteration 10 | TREC-8 dataset, approximately 500,000 documents, 50 title-only topics, K=300,000, n/N=0.001, k=1,000 queried per iteration, BM25 ranking on each computer, keep ratio x=20% initial + 3%/iteration, 10 trials of 10 iterations each, metrics MAP and Recall-1000 |
| TREC-8 experiment, nDCG-like pruning: retrieval accuracy rises from 67% to 92% in the first 5 iterations, reaching 96% at iteration 10; only 4 iterations needed to reach 90% | Same TREC-8 setup as above, scoring function replaced with the nDCG-like per-computer score |

### Parameters
- K (total computers): fixed at 300,000 across all experiments, following the Google-scale configuration cited in COX-ICTIR-09
- n/N (per-computer sample fraction): fixed at 0.001 throughout; simulation substitutes N=100,000, n=100 for computational cost while keeping the ratio fixed, and states results generalize to any N,n at that ratio
- k (computers queried per iteration): 1,000 in most experiments; also tested at 2,000 for the r=4,000 case
- r (assumed/target relevant document count): swept 1,000 / 2,000 / 4,000 in simulation; fixed at r=1,000 in the TREC-8 nDCG-based experiments
- Keep ratio: initial x=20% at iteration 1, incremented by y=3% at each subsequent iteration; stated as a heuristic choice, with a "less heuristic pruning strategy" left as future work
- Trial counts: 10 trials per simulation configuration; TREC-8 experiments run 10 trials of 10 iterations each, per query, over 50 TREC-8 title-only topics
- Retrieval model for TREC-8 experiments: BM25 (Okapi)

### Stated limitations
The paper states the centralized coordination node is a single point of failure, reducing fault tolerance relative to the fully decentralized PAC architecture, though it states this is "no worse than for deterministic centralized distributed architectures" and that the node could itself be replicated. The cause of accuracy degradation as the relevant-document count r grows (2,000 and 4,000 tracking the theoretical upper bound less closely than r=1,000) is stated as "unclear" and "a topic of ongoing research"; the paper does not identify the mechanism. The iterative node-caching approach is stated to apply "only for queries that occur frequently (e.g. more than 10 times)"; for infrequent queries the paper states alternative approaches remain future work and are not addressed. Combining node caching with traditional query-result caching is stated to be "outside the scope of this paper." The Section 4.2 known-relevant-document-count algorithm is stated to be an idealized upper-bound exercise, not a deployable method, because the number of relevant documents for a real query is unknown in practice (motivating Section 4.3's BM25-ranked-top-r substitute).

### Requirements it places on the rest of the system
The scheme requires a centralized coordination node that receives every query, performs the pseudo-random seed-based computer selection, retains per-query state (the identifiers of the retained computer subset from the previous iteration, called node caching, distinct from caching retrieved documents), and forwards the query to the resulting computer set; this node must be reachable by every querying client. The pseudo-random selection function must be deterministic in the query (same query text maps to the same initial computer subset) for repeat queries to benefit from node caching. The scoring functions (simple count or nDCG-like) require the coordination node to receive each computer's full ranked result list for the query, not just a match/no-match signal, so it can compute how many top-r positions a computer's documents occupy and at what rank. The BM25-based variant (Section 4.3) requires every participating computer to run the same retrieval model (BM25) locally over its own document sample so that per-computer top-r rankings are comparable when merged.

### Contradicts
None found against other entries in this batch. The paper's own numbers show that raising query fan-out k, not only iterating, materially raises baseline accuracy (63% at k=1,000 vs 86% at k=2,000 for r=4,000) -- a factor separate from, and outside, this paper's own iterative-refinement claim.

### References worth retrieving
- Cox, Fu, Hansen. "Probably Approximately Correct Search." ICTIR 2009. -- foundational (already in this corpus as COX-ICTIR-09; this paper's own direct predecessor)
- Fagni, Perego, Silvestri, Orlando. "Boosting the performance of web search engines: Caching and prefetching query results by exploiting historical usage data." ACM TOIS 24(1), 2006. -- foundational (query-caching literature this paper distinguishes its node-caching approach from)
- Jarvelin, Kekalainen. "Cumulated gain-based evaluation of IR techniques." ACM TOIS 20(4), 2002. -- foundational (source of the nDCG metric this paper's per-computer score is built on)
- Li, Loo, Hellerstein, Kaashoek, Krager (Karger), Morris. "On the feasibility of peer-to-peer web indexing and search." IPTPS 2003. -- competing
- Raiciu, Huici, Handley, Rosenblum. "ROAR: increasing the flexibility and performance of distributed search." SIGCOMM CCR 39(4), 2009. -- competing
- Skobeltsyn, Luu, Zarko, Rajman, Aberer. "Web text retrieval with a p2p query-driven index." SIGIR 2007. -- competing
- Terpstra, Kangasharju, Leng, Buchmann. "BubbleStorm: resilient, probabilistic, and exhaustive peer-to-peer search." SIGCOMM 2007. -- competing
- Yang, Ho. "Proof: A DHT-based peer-to-peer search engine." Web Intelligence 2006. -- competing
- Yang, Dunlap, Rexroad, Cooper. "Performance of full text search in structured and unstructured peer-to-peer systems." INFOCOM 2006. -- competing
- Beitzel, Jensen, Chowdhury, Grossman, Frieder. "Hourly analysis of a very large topically categorized web query log." SIGIR 2004. -- foundational (source of the query power-law-frequency claim motivating this paper's focus on repeated queries)
- Robertson, Walker, Jones, Hancock-Beaulieu, Gatford. "Okapi at TREC-3." TREC 1994. -- foundational (BM25 retrieval model used for per-computer ranking)

### Verbatim extracts
"performance can improve from 67% to 96% in just 10 iterations"
"the initial accuracy is 86% and the search once again closely follows"
"the reason for this degradation in performance as r increases is unclear"
"this iterative approach is only applicable for queries that occur frequently"
"we are not caching queries in the traditional sense"
