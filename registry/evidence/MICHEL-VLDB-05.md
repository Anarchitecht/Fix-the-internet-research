## [MICHEL-VLDB-05] KLEE: A Framework for Distributed Top-k Query Algorithms
**Citation:** Sebastian Michel, Peter Triantafillou, Gerhard Weikum. "KLEE: A Framework for Distributed Top-k Query Algorithms." VLDB, 2005. pp. 637-648.
**Retrieved:** full text via http://www.vldb.org/archives/website/2005/program/paper/thu/p637-michel.pdf
**Source URL:** http://www.vldb.org/archives/website/2005/program/paper/thu/p637-michel.pdf
**Domain:** B

### What it does
KLEE finds the k documents with the highest aggregate score across index lists (one list per query term or attribute) that are held by different peers, while keeping network bandwidth, the number of communication round trips, and each peer's local work low, at the cost of a small, quantified drop in result accuracy relative to an exact answer. It generalizes the threshold-algorithm (TA) family — algorithms that compute a top-k answer over multiple sorted lists by bounding each candidate document's possible final score between a worst-case and best-case value and stopping once no unseen document can beat the current k-th best worst-case score — from a single machine's local index lists to lists distributed one-per-peer, where every round trip to fetch data costs network latency and bandwidth rather than a local disk access.

One peer, the coordinator (the peer where the query originated), directs a set of cohort peers (the peers holding index lists for the query's terms) through up to three communication phases:

1. **Exploration.** The coordinator asks every cohort peer for its local top-k entries plus statistical metadata: a histogram over the peer's score range (equal-width cells, each carrying a document-ID count, an average score, and a Bloom filter — a compact set-membership structure that hashes each member into a bit array and may report a false positive but never a false negative — over the document IDs whose score falls in that cell). For any document whose score is missing from a peer's reported top-k, the coordinator locates which histogram cell that document falls into via the Bloom filter and substitutes the cell's average score as an estimate. This produces an estimated topKscore (the k-th highest aggregate score in the current estimate), which in turn defines each peer's candidate list: every document at that peer scoring above topKscore/m (m = number of cohort peers).
2. **Optimization** (local to the coordinator, no communication). The coordinator estimates, from the histogram statistics already collected, how much bandwidth a further filtering phase would save, and decides whether to run it.
3. **Candidate List Reduction** (optional, one round trip). Each peer builds a Candidate List Filter (CLF): a bitmap in which every document scoring above topKscore/m is hashed to a bit. The coordinator stacks the m peers' CLFs into an m-by-b Candidate List Filter Matrix (CLFM) and keeps only the documents that hashed into a column with at least R bits set (i.e., documents plausibly present in enough peers' candidate lists to matter), discarding the rest without ever transferring their (docID, score) pairs.
4. **Candidate List Retrieval.** One final round trip fetches the (docID, score) pairs for the surviving candidate documents from each cohort peer, and the coordinator computes the final approximate top-k list from them.

KLEE-3 is the three-step, two-communication-phase variant (skips step 3); KLEE-4 is the full four-step, three-communication-phase variant.

### Measured results

| Comparison | Result | Conditions |
|---|---|---|
| KLEE-4 vs. TPUT/X-TPUT bandwidth, Overlap benchmark | factor ~2.5 to more than an order of magnitude | synthetic Overlap benchmark, Zipf theta=0.7, 5-term queries, overlap parameter Omega swept 10%-100% of score mass, filter false-positive target c=10% |
| KLEE-4 vs. TPUT/X-TPUT bandwidth, Zipf-GOV and Zipf-XGOV | factor of 2 | Zipf theta=0.7, c=10%, real query sets from GOV/XGOV with synthetic Zipf-distributed scores |
| Aggregate total bandwidth, KLEE-4 vs. both TPUT variants | factor ~8 (Overlap benchmark), factor >2 (Zipf-GOV and Zipf-XGOV) | theta=0.7, Omega=30% (Overlap); c=10% throughout; KLEE-3 better by ~2.5x (Overlap) and ~10% (Zipf-GOV/XGOV) |
| Aggregate response time, KLEE-4 (KLEE-3) vs. TPUT algorithms | better by factor >4 (>2) on Overlap; >4 (25%) on Zipf-XGOV; ~2.5 (3.5) on Zipf-GOV vs. X-TPUT (TPUT) | same benchmarks/parameters as above; DTA (Distributed TA) response times are described as very disappointing due to high random-I/O counts; KLEE-4 overall 1-2 orders of magnitude better than DTA |
| KLEE-4 bandwidth vs. X-TPUT, real-world collections | factor ~2 (GOV, >2 terms), 2-3x (XGOV), ~3x (IMDB) | GOV = 1.25M documents from a .gov web crawl (TREC-12 Web Track), 8 GB total index-list size, 50 original queries up to 5 terms; XGOV = same corpus with WordNet-expanded queries averaging 2x as many terms, up to 18; IMDB = ~375,000 movies, >1,200,000 persons, 140 MB total index-list size, text + set-valued attributes |
| KLEE-4 bandwidth vs. TPUT, real-world collections | up to 6x (GOV), more than an order of magnitude (XGOV), similar factors (IMDB) | same collections as above |
| Detailed benchmark totals (Overlap, theta=0.7, Omega=30%, c=10%, 50-query batch) | DTA: 3,182,737 bytes / 581,226 ms / recall 1.0; TPUT: 16,152,355 bytes / 1,148,847 ms / recall 1.0; X-TPUT: 8,406,897 bytes / 92,137 ms / recall 0.73, score error 0.026, rank distance 3.85; KLEE-3: 8,592,431 bytes / 92,745 ms / recall 0.70, score error 0.026, rank distance 4.14; KLEE-4: 2,845,225 bytes / 33,616 ms / recall 0.69, score error 0.027, rank distance 4.33 | single Table 1 row, same benchmark configuration; DTA and TPUT are exact (recall forced to 1, score error 0 by construction) |
| Average recall on real-world collections | KLEE-4/KLEE-3: 90%/90% (GOV), 79%/83% (XGOV); average score error ~2% (GOV) and ~5% (XGOV) of topKscore | same GOV/XGOV collections; top-20 queries (k=20) throughout all experiments |
| Bloom-filter false-positive targets used | step-1 filters: pfp < 0.004; step-3 (CLF) filters: pfp < 0.06 | fixed for all reported experiments; the paper states the larger step-3 pfp is a deliberate tradeoff against 6% extra (docID, score) pairs sent for falsely-included candidates |

Hardware/simulation setup: implementation in Java, all peer data on local disk, all processes run on a single 3 GHz Pentium machine (not a real distributed testbed); disk I/O modeled as a 9 ms seek/rotational latency plus an 8 MB/s transfer rate; network latency modeled with a 150 ms round-trip time for packets up to 1 KB and an 800 Kb/s large-transfer rate (the wide-area throughput figure the paper cites from a separate SLAC-to-Lyon measurement study), with cohort communication run in simulated parallel (longest per-phase time counted).

### Parameters
- k (top-k size): fixed at 20 for all reported experiments.
- Score-mass fraction c for histogram "high-end" cells reported in phase 1: tested at 5%, 10%, 20%; only c=10% results are reported ("for space reasons").
- Zipf skew parameter theta: 0.3, 0.7, 1.0 tested; only theta=0.7 curves are shown ("similar results occur with all other tested values").
- Overlap parameter Omega (synthetic term-correlation control): swept 10%-100% of index-list score mass, in steps of 10 percentage points.
- Number of query terms/peers m: 2 to 10 (Overlap benchmark), up to 5 (GOV), up to 18 (XGOV, WordNet-expanded), 3-5 (IMDB).
- Bloom filter false-positive rate: <0.004 for step-1 per-cell filters, <0.06 for step-3 Candidate List Filters.
- R (bit-count threshold for keeping a CLFM column): selected per-query via the technique in the paper's Section 5 ("interesting columns"); no single fixed numeric value is stated as used across all experiments.
- Histogram cell count n and structure: equal-width cells over the score range (0, 1]; exact n not stated as a numeric constant in the excerpted sections.

### Stated limitations
The evaluation runs entirely on one physical machine (a single 3 GHz Pentium) with disk and network I/O simulated from separately measured latency/throughput parameters, not on a real multi-peer network; the authors state this choice was made explicitly to avoid interference from concurrent processes and to get reproducible, comparable timings across algorithms run at different times, which also means the reported response times are model-based estimates, not wall-clock measurements from a live network. KLEE is explicitly an approximate algorithm: KLEE-3 and KLEE-4 both show recall below 1.0 and nonzero score error and rank distance in every table, in exchange for the bandwidth and time reductions; the paper frames this tradeoff as its central contribution rather than a defect, so a use case requiring exact top-k results is not what KLEE targets. The competing method in Suel et al. [Su03] is noted by the authors as unclear how to generalize beyond two peers — this is the authors characterizing a different paper's limitation, not KLEE's own, and is recorded here only as an attributed statement about that other work.

### Requirements it places on the rest of the system
- Every cohort peer must maintain, per query term or attribute it indexes, a sorted index list plus a precomputed histogram-with-Bloom-filter structure (HistogramBlooms) over that list's score distribution; the paper notes this structure can be expensive to build and recommends precomputing and storing it locally rather than building it per-query, so a system adopting KLEE needs index lists that are largely static between precomputation runs, or a maintenance mechanism to keep the histograms current, which this paper does not supply.
- The mechanism assumes monotonic, per-document aggregate scoring across peers (a document's total score is a monotone combination of its per-term scores), the same requirement underlying the wider TA/NRA family; it requires a coordinator role capable of running a TA-style bookkeeping algorithm (priority queue plus worst-/best-score bounds) and of hashing and testing Bloom filters returned by every cohort peer.
- The optional Candidate List Reduction phase requires all m cohort peers to use the same hash functions and coordinated bitmap size b for their CLFs, set by the coordinator from phase-1 statistics before phase 3 begins — the cohort peers cannot independently decide their own filter sizing.
- The approach assumes cooperative, honest cohort peers: nothing in the described mechanism checks a peer's reported histogram, top-k entries, or CLF bits against manipulation, so a system exposing this to adversarial peers needs a separate verification layer this paper does not provide.
- Result quality (recall, score error, rank distance) degrades or improves depending on query-term correlation and score-distribution skew, both measured properties of the underlying data; a system selecting KLEE needs some way to estimate or tolerate that dependency, since the paper's own results show recall dropping from 90% (GOV) to 79-83% (XGOV) purely from a change in query-term count and correlation structure.

### Contradicts
None found against other entries in this corpus.

### References worth retrieving
- **[CW04] Cao, Wang, "Efficient Top-K Query Calculation in Distributed Networks," PODC 2004** — competing: TPUT, the paper's closest prior-art baseline and the algorithm KLEE is most directly benchmarked against throughout; KLEE-4 wins by factors up to an order of magnitude against it, so TPUT's own reported numbers are the other side of that comparison.
- **[Su03] Suel et al., "ODISSEA: A Peer-to-Peer Architecture for Scalable Web Search and Information Retrieval," WebDB 2003** — competing: the first P2P-style distributed top-k approach cited, limited by the authors of this paper to two peers with no known generalization.
- **[Ba05] Balke et al., "Progressive Distributed Top-k Retrieval in Peer-to-Peer Networks," ICDE 2005** — competing: addresses P2P top-k via super-peer hypercube overlay topologies, a different architectural approach to the same problem.
- **[FLN03] Fagin, Lotem, Naor, "Optimal Aggregation Algorithms for Middleware," J. Comput. Syst. Sci. 66(4), 2003** — foundational: the original TA/NRA algorithm family KLEE generalizes to the distributed setting.
- **[TWS04] Theobald, Weikum, Schenkel, "Top-k Query Evaluation with Probabilistic Guarantees," VLDB 2004** — foundational: the probabilistic-approximation technique (quantile-based bestscore substitution) this paper's approximate top-k approach builds on.
- **[BGM02]/[MGB04] Bruno, Gravano, Marian, "Evaluating Top-k Queries over Web-Accessible Databases," ICDE 2002 / TODS 29(2), 2004** — foundational: the first distributed TA-style algorithm, predating this paper's fully distributed peer setting.
- **[Hue05] Huebsch et al., "The Architecture of PIER: An Internet-Scale Query Processor," CIDR 2005** — foundational/competing: cited as the P2P federation context motivating distributed top-k processing generally; worth checking for its own measured overlay-query costs.

### Verbatim extracts
- "KLEE makes a strong case for approximate top-k algorithms over widely distributed data sources."
- "KLEE-4 outperforms the TPUT algorithms by a factor ranging from approximately 2.5 to more than an order of magnitude."
- "KLEE-4 is better than both TPUT algorithms by a factor of about 8 in Overlap"
- "Average recall values for KLEE-4 (KLEE-3) are at 90% (90%) and 79% (83%)"
- "we opted for simulating disk IO latency and network latency"
- "it is unclear and left as an open issue how to generalize to more than two peers" [describing Suel et al., not KLEE]
