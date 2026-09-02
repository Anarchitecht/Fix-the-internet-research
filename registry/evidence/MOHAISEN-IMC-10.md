## [MOHAISEN-IMC-10] Measuring the Mixing Time of Social Graphs
**Citation:** Abedelaziz Mohaisen, Aaram Yun, Yongdae Kim. "Measuring the Mixing Time of Social Graphs." ACM Internet Measurement Conference (IMC), 2010. Pages 383-389. DOI 10.1145/1879141.1879191.
**Retrieved:** full text via https://www.tdi.gatech.edu/pub/imc10-mohaisen.pdf (candidate URL; matched title, authors, venue in first 2000 characters)
**Source URL:** https://dl.acm.org/doi/10.1145/1879141.1879191
**Domain:** F

### What it does
Measures, rather than assumes, the mixing time of real social graphs — the length of random walk needed for the walk's position distribution to approach the graph's stationary distribution — because several Sybil-defense designs (SybilGuard, SybilLimit, SybilInfer, Whanau) rely on social graphs being "fast mixing" (mixing time polynomial in log(n) for a target closeness epsilon) as a precondition for their security proofs, and no prior paper had directly measured this property on the graphs those defenses target.

Mixing time T(epsilon) is defined as the maximum, over all starting nodes v_i, of the minimum walk length t such that the total variation distance between the walk's distribution after t steps and the graph's stationary distribution falls below epsilon. Two measurement methods are used. The first computes the Second Largest Eigenvalue Modulus (SLEM), written mu, of the graph's random-walk transition matrix; mu bounds mixing time as mu/(2(1-mu)) * log(1/(2*epsilon)) <= T(epsilon) <= (log(n) + log(1/epsilon))/(1-mu). The paper reports the lower bound from this formula because it stated more forcefully how much larger the true mixing time can be than assumed. The second method directly samples: starting from a randomly chosen node, it computes the walk's distribution after t steps for increasing t and measures the total variation distance to the stationary distribution, repeated from 1,000 randomly chosen starting nodes per graph, aggregated as percentiles (top 10%, median 20%-60%, bottom 10%) of the resulting epsilon values at each walk length t. For graphs too large to exhaustively sample (millions of nodes), representative subgraphs of 10,000, 100,000, and 1,000,000 nodes are extracted from the original graph using breadth-first search from a random starting node; the paper notes this sampling method may bias toward faster mixing, which only strengthens a finding of slower-than-expected mixing.

### Measured results

| Dataset | Nodes | Edges | SLEM (mu) | Mixing time to reach epsilon=0.1 (lower bound, SLEM method) |
|---|---|---|---|---|
| Wiki-vote | 7,066 | 100,736 | 0.899418 | (small dataset, in the 200-400 range group below) |
| Slashdot 1 | 82,168 | 582,533 | 0.987531 | (small dataset, in the 200-400 range group below) |
| Slashdot 2 | 77,360 | 546,487 | 0.987531 | (small dataset, in the 200-400 range group below) |
| Facebook | 63,392 | 816,886 | 0.998133 | (small dataset, in the 200-400 range group below) |
| Physics 1 | 4,158 | 13,428 | 0.998133 | 200-400 |
| Physics 2 | 11,204 | 117,649 | 0.998221 | 200-400 |
| Physics 3 | 8,638 | 24,827 | 0.996879 | 200-400 |
| Enron | 33,696 | 180,811 | 0.996473 | 200-400 |
| Epinion | 4,158 | 13,428 | 0.998133 | 200-400 |
| DBLP | 614,981 | 1,155,148 | 0.997494 | 100-400 |
| Facebook A | 1,000,000 | 20,353,734 | 0.982477 | 100-400 |
| Facebook B | 1,000,000 | 15,807,563 | 0.992020 | 100-400 |
| Livejournal A | 1,000,000 | 26,151,771 | 0.999387 | 1,500-2,500 |
| Livejournal B | 1,000,000 | 27,562,349 | 0.999695 | 1,500-2,500 |
| Youtube | 1,134,890 | 2,987,624 | 0.997972 | 100-400 |

The dataset-grouped mixing-time figures above are the paper's stated ranges read from Figures 1 and 2 (small-graph and large-graph lower-bound plots), quoting the paper's own text: "physics co-authorship, Enron, and Epinion... a mixing time of 200 to 400 is required to achieve epsilon=0.1"; "about 1500 to 2500 in case of Livejournal, it ranges from 100 to about 400 in case of DBLP, Youtube, and Facebook."

Sample-versus-SLEM discrepancy, measured on the 1,000,000-node Facebook A subgraph: the top-10th-percentile of 1,000 sampled random walks reaches an average variation distance of epsilon=10^-5 at walk length 100, while the SLEM-derived bound reaches only epsilon=10^-2 at the same walk length — a 3-order-of-magnitude gap between the best-case sampled behavior and the worst-case SLEM bound, on the same graph and walk length.

Node-pruning effect, measured on the DBLP graph (614,981 nodes) by iteratively removing nodes below a minimum degree threshold from 1 to 5 (producing DBLP1 through DBLP5, with DBLP5 at 145,497 nodes): at a fixed walk length of 100, the lower-bound total variation distance falls from about 0.2 to about 0.03, and the average total variation distance falls from about 0.015 to about 0.002 — i.e., pruning to under a quarter of the original node count materially speeds mixing, replicating the trimming step used in SybilGuard's and SybilLimit's own evaluations.

SybilLimit reimplementation, applied without an attacker present (since SybilLimit's guarantee is stated as a function of attack-edge count, not measurable without simulating an attack): random-walk parameter r set to r0*sqrt(m) per the birthday-paradox admission formula, m being the graph's undirected edge count; walk length t increased until nearly all honest nodes in the graph were admitted by a trusted verifier node. Result (Figure 8): admission-rate-versus-walk-length curves plotted for Physics 1, Physics 2, Physics 3, Facebook A (10,000-node sample), and Slashdot 1 (10,000-node sample); the paper's stated conclusion from this is that the walk length needed to admit nearly all honest nodes is larger, and the resulting variation-distance quality worse, than the fixed walk lengths of 10 or 15 used in SybilLimit's own published evaluation.

Prior-work critique with specific figures: SybilGuard and SybilLimit's own experiments used fixed walk lengths of 10 or 15 nodes; this paper's measurement finds walk lengths of 100-2,500 are needed across the datasets in Table 1 to reach epsilon=0.1, one to two orders of magnitude larger than the walk lengths those defenses' own evaluations used.

### Parameters
- epsilon: the target total variation distance defining mixing time T(epsilon); the paper measures at multiple epsilon but reports epsilon=0.1 as its headline comparison figure; SybilGuard/SybilLimit's theoretical framing requires epsilon=Theta(1/n).
- Walk sample count: 1,000 randomly chosen starting nodes per graph for the direct-sampling method.
- Subgraph sizes for large-graph BFS sampling: 10,000, 100,000, and 1,000,000 nodes, drawn from source graphs of 3 to 5 million nodes.
- r (SybilLimit random-walk instance count parameter): set to r0*sqrt(m), r0 computed from the birthday-paradox formula for a target intersection probability, m = undirected edge count of the graph under test.
- Node-degree pruning threshold (DBLP trimming experiment): minimum degree thresholds 1 through 5, applied iteratively, reducing DBLP from 614,981 nodes (DBLP1) to 145,497 nodes (DBLP5).

### Stated limitations
The paper states its own future work as building theoretical models that account for average-case (rather than worst-case) mixing time, and cost models relating a social graph's mixing time to its trust model, motivated by the observation that graphs requiring physical acquaintance (DBLP, physics co-authorship) mix slower than online social networks with looser trust models (Facebook, wiki-vote) whose links tolerate more Sybil identities. The authors state the average mixing time observed across sampled starting nodes is consistently better than the SLEM-derived worst-case bound, but still larger than the walk lengths (10, 15) that prior Sybil-defense evaluations used. The paper does not evaluate any Sybil defense scheme other than SybilLimit for quantitative performance impact, and its SybilLimit reimplementation is run without a simulated attacker, so it reports only admission of honest nodes, not the resulting count of admitted Sybil identities under attack.

### Requirements it places on the rest of the system
- A Sybil-defense mechanism relying on a "fast mixing" precondition for its security proof needs the deployment's actual social graph measured for mixing time before that proof's guarantees can be trusted; this paper's own results show mixing time varies by more than an order of magnitude across graph types (100-400 for DBLP/Youtube/Facebook versus 1,500-2,500 for Livejournal, at the same epsilon=0.1), so no single walk-length constant transfers across deployments.
- A mechanism that trims or prunes low-degree nodes to make its social graph mix faster (as SybilGuard and SybilLimit's own evaluations do) needs to disclose the resulting reduction in graph size as part of its security claim, since this paper measures DBLP shrinking from 614,981 to 145,497 nodes (76% of nodes removed) to obtain its mixing-time improvement.
- A design that uses SLEM as its analytic proxy for mixing time needs to compute the transition matrix's second-largest eigenvalue modulus, which the paper found computationally feasible up to graphs of about one million nodes given a sparse transition matrix; beyond that the direct-sampling method (starting-node random walks) is the fallback, and it yields a materially more optimistic (smaller) mixing-time estimate than the SLEM bound on the same graph.
- Any component setting a fixed random-walk length as a network-wide constant (as SybilGuard and SybilLimit do, using 10 or 15) needs a graph-specific justification, because this paper's measurement shows the walk length required to reach epsilon=0.1 varies by dataset from about 100 to about 2,500.

### Contradicts
Contradicts the fast-mixing assumption underlying SybilGuard (Yu, Kaminsky, Gibbons, Flaxman, SIGCOMM 2006 / IEEE/ACM ToN 2008), SybilLimit (Yu, Gibbons, Kaminsky, Xiao, IEEE S&P 2008), SybilInfer (Danezis, Mittal, NDSS 2009), and Whanau (Lesniewski-Laas, Kaashoek, USENIX NSDI 2010): those designs' published evaluations used walk lengths of 10 or 15 and this paper's direct and SLEM-based measurements find mixing times one to two orders of magnitude larger (100 to 2,500, depending on dataset) are needed to reach epsilon=0.1 on the same or comparable real-world social graphs. The paper explicitly states Whanau's own attempted mixing-time estimate is "only circumstantial" and does not establish fast mixing. None found against any other paper in the current evidence corpus.

### References worth retrieving
- Competing / independent measurement, concurrent: B. Viswanath, A. Post, K. P. Gummadi, A. Mislove, "An analysis of social network-based sybil defenses," SIGCOMM 2010 — compares SybilGuard, SybilLimit, SybilInfer, and SumUp directly and finds their behavior reduces to community detection; this paper states its own slow-mixing findings agree with that result.
- Attack / critique target: H. Yu, M. Kaminsky, P. B. Gibbons, A. Flaxman, "SybilGuard: defending against sybil attacks via social networks," SIGCOMM 2006, and IEEE/ACM Trans. Netw. 16(3), 2008 — the defense whose fixed walk-length (10) evaluation this paper's central results contradict.
- Attack / critique target: H. Yu, P. B. Gibbons, M. Kaminsky, F. Xiao, "SybilLimit: A near-optimal social network defense against sybil attacks," IEEE S&P 2008 — the defense this paper reimplements and finds needs a substantially larger walk length than the original evaluation used.
- Attack / critique target: G. Danezis, P. Mittal, "SybilInfer: Detecting sybil nodes using social networks," NDSS 2009 — a fast-mixing-property-dependent Sybil detection scheme this paper cites as relying on an unverified mixing assumption.
- Competing: C. Lesniewski-Laas, M. F. Kaashoek, "Whanau: A sybil-proof distributed hash table," USENIX NSDI 2010 — a fast-mixing-dependent Sybil-proof DHT whose own mixing-time estimate this paper calls circumstantial.
- Foundational: J. R. Douceur, "The Sybil Attack," IPTPS 2002 — origin of the Sybil-attack problem these defenses address.
- Foundational: A. Sinclair, "Improved bounds for mixing rates of Markov chains and multicommodity flow," Combinatorics, Probability & Computing, 1992 — source of the SLEM-based mixing-time bound (Theorem 2) this paper's methodology uses.
- Dataset source: A. Mislove, M. Marcon, P. K. Gummadi, P. Druschel, B. Bhattacharjee, "Measurement and analysis of online social networks," IMC 2007 — source of the Livejournal and Youtube graph datasets used in Table 1.

### Verbatim extracts
- "the mixing time of social graphs is much larger than anticipated"
- "current security systems based on fast mixing have weaker utility guarantees or have to be less efficient"
- "a mixing time of 200 to 400 is required to achieve epsilon=0.1"
- "about 1500 to 2500 in case of Livejournal, it ranges from 100 to about 400 in case of DBLP"
- "the variation distance is reduced from about 0.2 to 0.03" after successive trimming
- "the SLEM-based mixing time results in only epsilon=10^-2" versus 10^-5 for the sampled top 10%
- "their evidence is only circumstantial and it does not directly follow that these social graphs are really fast mixing"
