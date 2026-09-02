## [RICHARDSON-SIGIR-14] Estimating Global Statistics for Unstructured P2P Search in the Presence of Adversarial Peers
**Citation:** Sami Richardson, Ingemar J. Cox. "Estimating Global Statistics for Unstructured P2P Search in the Presence of Adversarial Peers." SIGIR, 2014. DOI 10.1145/2600428.2609567.
**Retrieved:** full text via http://www0.cs.ucl.ac.uk/staff/ingemar/Content/papers/2014/sigir2014.pdf
**Source URL:** http://www0.cs.ucl.ac.uk/staff/ingemar/Content/papers/2014/sigir2014.pdf
**Domain:** B

### What it does
The mechanism lets a node ranking documents under BM25 or a language model with Dirichlet smoothing compute the collection-wide statistics those rankers need (document frequency, average document length) inside a Probably Approximately Correct (PAC) peer-to-peer search architecture, where each of n nodes indexes only a random subset of the document collection and a query samples z random nodes. Each queried node u, besides returning its top-k' matching documents (Ru) with per-document scoring fields, also returns a vector of local statistics derived from its own index (Gu) — for BM25 these are per-term local document-frequency counts and local average document length; for the language model, local collection-probability estimates. The querying node combines the Gu values from all z responding nodes into an estimate of the true global statistic and rescoring the returned documents with it before forming the final top-k list. Because a query already contacts z nodes to retrieve matching documents, the statistics estimate is a byproduct of the existing query traffic and adds no round trip. Because responses from a large sample of nodes are combined, the estimate can be biased by malicious responders; the paper's defense has each querying node compute a skewness statistic Kt (Groeneveld-Meeden measure) over the z returned values for each query term, and repeatedly discard the value contributing most to skew until |Kt| falls under a threshold tau, before computing the global-statistic estimate from the surviving values.

### Measured results
Simulated network: n = 10,000 nodes, document collection C from the WT10g web corpus with m = 1,692,096 documents, documents distributed uniformly at random so each node indexes rho documents. Fifty queries drawn from the TREC 2009 Million Query track, each repeated 10 times, averaged. z and rho are chosen jointly so the PAC framework's theoretical expected accuracy P(di) = 1-(1-rho/m)^z equals 0.9 (z = 1; 2000; 4000; 6000; 8000; 10000, with corresponding rho = 1,692,096; 1,946; 973; 649; 486; 389).

| Condition | Result |
|---|---|
| BM25, global statistics from full collection, any z (n=10,000, WT10g) | average accuracy about 0.9 for all tested z |
| BM25, document-frequency term estimated from querying node's own index only | accuracy drop up to nearly 35% as z rises to 10,000 |
| BM25, average-document-length term estimated from querying node's own index only | accuracy drop up to about 10% |
| Language model, collection-probability term from querying node's own index only | accuracy drop up to about 20% |
| BM25 with the global-statistics estimation technique (statistics pooled from z=10,000 nodes' Gu, k'=rho=389 or k'=10) | accuracy close to the 0.9 theoretical value at all tested z |
| Language model with the technique, k'=rho | accuracy close to 0.9 theoretical value |
| Language model with the technique, k'=10, z up to 10,000 | accuracy drops to about 0.8, about 10% below theoretical |
| BM25 with technique, z=10,000, rho=389, k'=10 | about 95% of the 50 test queries reach accuracy >= 0.7, versus 15% when using only the querying node's local index |
| Language model with technique, same setting | about 65% of queries reach accuracy >= 0.7 (versus about 90% with full-collection statistics, 60% with local-only); over 95% of queries reach accuracy >= 0.3 (versus under 80% local-only) |
| No adversary, PAC baseline vulnerability to a censorship attack (excludes target document, correct global statistics available at each node) | z=1,000 nodes queried, f=0.3% malicious nodes gives 0.95 probability at least one malicious node is sampled, hence up to 95% of queries manipulable at the query-routing level even before the global-statistics extension is added |
| Censorship attack via corrupted global statistics, no defense (query T='small dog', target D2, z=2,000, rho=1,946 nodes each) | target document rank moves 5 -> 9 -> 582 -> 2166 as malicious-node fraction f rises 0% -> 10% -> 20% -> 30%; at f=20% the document falls out of a top-10 list |
| Same attack, PAC baseline where only document exclusion (no statistics corruption) is available and correct global statistics are known at every node | at f=20%, retrieval probability of D2 is still 84% (from the closed-form P'(di) = 1-(1-rho/m)^(z(1-f))) |
| Promotion attack via corrupted global statistics, no defense (same query/target D1, z=2,000, rho=1,946) | target rank moves 20,778 -> 84 -> 11 -> 9 as f rises 0% -> 10% -> 20% -> 30%; under 30% malicious nodes suffices to bring it into a top-10 |
| Promotion attack, exclusion-only baseline with correct global statistics at each node | over 95% of nodes must be malicious to bring the same document into a top-10 |
| Disruption attack via corrupted global statistics, no defense (z=2,000, rho=1,946, 50 TREC queries, k=k'=10) | average accuracy falls from a theoretical baseline of about 0.9 to about 0.6 at only 10% malicious nodes, a nearly 35% relative fall |
| Same attack setting, with the skewness defense active (threshold tau = +/-0.1) | attacks have very little effect while the malicious-node fraction f < 40%; the defense breaks down as f approaches 50% because malicious and non-malicious responses become statistically indistinguishable |
| Baseline requirement for random node sampling (cited from Bortnikov et al., not this paper's own measurement) | Brahms, a gossip-based secure peer-sampling service, is stated to withstand up to 20% malicious nodes before sampling bias becomes significant; the authors state this — not their own skewness defense — is what actually bounds the tolerable adversarial fraction in a deployed system |

### Parameters
- n (nodes in simulated network): 10,000, fixed across all experiments.
- m (documents in collection): 1,692,096 (WT10g corpus), fixed.
- z (nodes queried per search): varied over {1, 2000, 4000, 6000, 8000, 10000}; also fixed at 2,000 for the adversarial-attack simulations.
- rho (documents indexed per node): paired with each z to hold theoretical accuracy at 0.9; values {1,692,096; 1,946; 973; 649; 486; 389}; fixed at 1,946 for most attack simulations.
- k' (documents returned per queried node): tested at k'=rho (return everything indexed) and k'=10.
- k (final result-list length considered): 10 in most experiments; attack-manipulation figures (Fig. 4/5) use no top-k restriction so the full range of achievable rank is visible.
- BM25 free parameters: k1 = 2.0, b = 0.75 (paper states these are typical published choices, not tuned by this paper).
- Language-model smoothing parameter: mu = AVGDL (average document length).
- Skewness defense threshold: tau = +/-0.1, used in the reported defense simulations; no other tau value is reported as tested.
- Malicious-node fraction f: varied continuously from 0 to 1 in the theoretical curves (Figures 3, 6-8) and at discrete points {0, 10%, 20%, 30%} in the worked rank examples (Figures 4-5).
- Query set: 50 queries from the TREC 2009 Million Query track, each repeated 10 times and averaged.

### Stated limitations
The authors state the analysis assumes a peer's local collection is a uniform random sample of the global collection, and state that future work is needed for non-uniform sampling, such as sampling weighted by document popularity, suggesting hash sketches (cited to Bender et al.) as a possible basis. The paper assumes malicious nodes cannot forge a document's content well enough to score highly under an honest ranker, attributing that assumption to a requirement that documents be signed by a trusted third party — a requirement this paper does not itself supply or evaluate. The skewness defense is stated to depend on the underlying node-sampling mechanism (Brahms) tolerating enough malicious nodes that its own sampling bias stays below significance (20% for Brahms); if node sampling is more compromised than the statistics-estimation defense can tolerate (40%), sampling failure — not statistics forgery — becomes the binding constraint. The defense is stated to fail as the malicious fraction approaches roughly 50%, because at that point the skewness measure cannot statistically distinguish malicious from honest values.

### Requirements it places on the rest of the system
Requires a secure, gossip-based random peer-sampling layer to select the z queried nodes per query and to bound the fraction of malicious nodes actually reachable by a query, because the entire accuracy analysis is conditioned on the assumption that node selection is unbiased; the paper cites Brahms as the concrete example and states Brahms's own 20% malicious-tolerance bound, not the statistics defense's 40% bound, is what would set the deployed tolerance. Requires each node's local document set to be a uniformly random subset of the global collection, drawn independently of document popularity or any other selection criterion, because the coverage argument (expected number of distinct documents sampled equals P(di)*m) depends on that uniformity; a popularity-weighted or otherwise correlated sampling process is stated as unanalyzed. Requires a mechanism external to this paper — content signing by a trusted third party is the one named — to prevent a malicious node from returning a forged document body that scores well under the honest ranking function; without it, the attacks analyzed here (which corrupt only summary/statistics fields) would need to be extended to cover forged document content. Requires every node to index the same fixed number of documents, rho, so that no node has disproportionate influence on global-statistics estimation; the paper notes a higher-capacity node can be split into multiple rho-capacity virtual nodes, which then must be defended against as a Sybil attack using a mechanism outside the scope of this paper.

### Contradicts
None found within this corpus at time of writing. The paper's own baseline results contradict any assumption that PAC-style unstructured search is inherently resistant to a small adversarial minority once collection-wide statistics are attached to the query protocol: the paper explicitly shows the technique moves the tolerable-adversary threshold for effective manipulation from roughly 70% malicious nodes (exclusion-only censorship, correct global statistics known everywhere) down to under 20% (same attack, statistics estimated from the query, no defense).

### References worth retrieving
- Foundational: H. Asthana, R. Fu, I. J. Cox, "On the feasibility of unstructured peer-to-peer information retrieval," Advances in Information Retrieval Theory, Springer, 2011 — the PAC P2P web-search feasibility paper this work builds on.
- Foundational: I. J. Cox, R. Fu, L. K. Hansen, "Probably approximately correct search," Advances in Information Retrieval Theory, Springer, 2009 — defines the PAC framework and its accuracy formula this paper extends.
- Competing: F. M. Cuenca-Acuna, C. Peery, R. P. Martin, T. D. Nguyen, "PlanetP: Using gossiping to build content addressable peer-to-peer information sharing communities," HPDC 2003 — compact per-node index summaries and TF-IPF as an alternative to estimating document frequency directly.
- Competing: J. Lu, J. Callan, "Federated search of text-based digital libraries in hierarchical peer-to-peer networks," ECIR 2005 — hierarchical hub/leaf alternative that maintains exact global statistics at hub nodes.
- Competing: H. Chen, J. Yan, H. Jin, Y. Liu, L. M. Ni, "TSS: Efficient term set search in large peer-to-peer textual collections," IEEE Transactions on Computers 59(7), 2010 — hybrid structured/unstructured design gathering global statistics via a gossip protocol.
- Competing: H. F. Witschel, "Global term weights in distributed environments," Information Processing & Management 44(3), 2008 — random-sampling estimation of global statistics combined with a local reference corpus; the closest prior technique to this paper's own.
- Foundational (peer sampling security): E. Bortnikov, M. Gurevich, I. Keidar, G. Kliot, A. Shraer, "Brahms: Byzantine resilient random membership sampling," Computer Networks 53(13), 2009 — the secure peer-sampling service this paper's threat model depends on and whose 20% malicious-tolerance bound the authors state is the actual system-wide constraint.
- Attack/foundational: J. Douceur, "The Sybil attack," IPTPS/Peer-to-peer Systems, 2002 — cited as the attack model for virtual-node capacity splitting.
- Competing (bias-reduction technique): M. Bender, S. Michel, P. Triantafillou, G. Weikum, "Global document frequency estimation in peer-to-peer web search," 9th Int. Workshop on the Web and Databases, 2006 — hash-sketch document-frequency estimation addressing collection-overlap bias, not adversarial bias; suggested by the authors as a possible basis for handling non-uniform sampling.
- Foundational (dataset): P. Bailey, N. Craswell, D. Hawking, "Engineering a multi-purpose test collection for web retrieval experiments," Information Processing & Management 39(6), 2003 — defines the WT10g corpus used in the simulations.

### Verbatim extracts
- "an adversary controlling fewer than 10% of peers can censor or increase the rank of documents, or disrupt overall search results"
- "global statistics estimation is viable even when up to 40% of peers are adversarial"
- "it would be Brahms that imposes the limit on the maximum number of malicious nodes tolerated"
- "Our work assumed that a peer's local collection consists of a uniform random sample"
- "we assume that malicious nodes cannot construct and return corrupt documents that will score highly"
