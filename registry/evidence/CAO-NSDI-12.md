## [CAO-NSDI-12] Aiding the Detection of Fake Accounts in Large Scale Social Online Services
**Citation:** Qiang Cao, Michael Sirivianos, Xiaowei Yang, Tiago Pregueiro. "Aiding the Detection of Fake Accounts in Large Scale Social Online Services." USENIX NSDI, 2012.
**Retrieved:** full text via https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final22.pdf
**Source URL:** https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final22.pdf
**Domain:** F

### What it does
SybilRank ranks the users of an online social network (OSN) by their likelihood of being a fake
account (Sybil), so that the operator can direct limited manual-inspection effort toward the
lowest-ranked accounts first, rather than relying only on user abuse reports.

The mechanism starts from a small set of trust seeds — accounts manually confirmed non-Sybil —
and distributes an initial amount of trust equally among them. It then runs power iteration (a
standard technique for repeatedly propagating a value across a graph by matrix multiplication) to
simulate a random walk: at each iteration, every node splits its current trust evenly among its
neighbors and sums what its neighbors send it. This is run for w = O(log n) iterations, where n
is the node count, and then stopped before the walk reaches its true stationary distribution — an
early-terminated random walk. Because Sybil accounts are assumed to connect to the honest region
through only a limited number of attack edges (edges between a Sybil and a non-Sybil user), that
narrow connection is a bottleneck: trust seeded in the non-Sybil region cannot yet spread
uniformly into the Sybil region within O(log n) steps, so non-Sybil users retain higher
degree-normalized trust (a node's trust divided by its own degree) than Sybil users at
termination. SybilRank ranks nodes by degree-normalized trust rather than raw trust, which the
paper states removes a Sybil's advantage from artificially inflating its own degree and gives
each non-Sybil node close to the same degree-normalized score, since after O(log n) power
iterations trust within the well-connected non-Sybil region approaches its own local stationary
distribution (trust proportional to degree).

Because a single well-connected OSN often contains multiple weakly-interconnected communities,
SybilRank additionally applies the Louvain community-detection method to partition the graph and
places multiple trust seeds inside each detected community (in the deployment, roughly 100 nodes
inspected total across communities in an 11-million-node graph), rather than seeding trust only
in one dominant community; this prevents communities distant from a single seed set from being
starved of trust and misclassified as Sybil. A final stage annotates ranked-list intervals with
the measured proportion of confirmed fakes within each interval (from manual sampling), letting
the operator choose where in the ranked list to spend inspection effort or how often to issue
CAPTCHAs, rather than relying on a single Sybil/non-Sybil cutoff, which the paper states no
social-graph defense can currently produce with an acceptable false-positive rate.

The paper proves (Theorem 1, full proof in a companion technical report not examined here) that
when an attacker establishes g attack edges at random into a fast-mixing (mixing time O(log n))
non-Sybil region, the total count of Sybils that rank above non-Sybil users, summed over the
whole network, is O(g log n) — a bound the paper states holds for any number of trust seeds.

### Measured results

| Result | Conditions |
|---|---|
| Deployed on the complete Tuenti social graph: 1,421,367,504 edges, 11,291,486 nodes, 11,216,357 in the giant connected component; 595 communities found via Louvain, 25 of them >100K nodes; ~100 nodes manually inspected total to pick trust seeds | Tuenti (Spain's largest OSN at the time), snapshot from August 2011 |
| Of the 2,000 lowest-ranked users manually inspected, 100% were confirmed fake | Same Tuenti deployment |
| Across the lowest 200K ranked users (sampled 100 users per 50K-user interval, up to 650K users disclosed), ~90% were confirmed fake, versus ~5% for Tuenti's existing user-abuse-report method — stated as an 18-fold efficiency increase | Same deployment; described by the authors as directly related to the precision metric from collaborative filtering |
| Fake proportion falls abruptly above the 200K mark: ~90% → ~50% → ~10% moving up the ranked list | Same deployment |
| Simulated ranking quality: at 1,500 attack edges into a 5,000-node Sybil region on the Facebook sample (regular-attack topology), a non-Sybil node still ranks above a random Sybil with 70% probability (area under the Receiver Operating Characteristic curve) | Facebook sample graph (10,000 nodes, 40,013 edges), 50 trust seeds, averaged over 100 runs |
| SybilRank outperforms SybilLimit, SybilInfer, Mislove's community detection (CD), GateKeeper, and EigenTrust on area under the ROC curve and on false positive/negative rates, across regular and scale-free attack structures on all 8 test graphs | 8 social graphs from Table 1 (sizes 7,115–18,772 nodes), Sybil region of 5,000 nodes with attack-edge count varied from a small value up to a value large enough to degrade all schemes; d=4 non-attack edges per Sybil; 20% fixed false-rate pivot for ROC comparisons; 100 runs averaged |
| EigenTrust has "at least 20% higher false positive and negative rates than SybilRank in most of the attack scenarios" | Same simulation setup |
| SybilInfer shows a steep area-under-ROC-curve drop near 500 attack edges on Facebook under the regular attack | Same simulation setup; attributed to uncertain convergence of SybilInfer's Metropolis-Hastings sampling within its O(n log n)-step termination |
| EigenTrust's normalized area under the ROC curve decreases as Sybil-internal (non-attack) edge count per Sybil rises from 4 to 40, while SybilRank's improves under the same change | Facebook graph, regular attack, 100/500/1,000 attack edges tested for each scheme |
| EigenTrust concentrates high degree-normalized trust near seeds (>9,400 of 10,000 non-Sybil nodes fall below trust value 2 at distance >2 hops); SybilRank keeps roughly uniform degree-normalized trust regardless of seed distance | Synthetic scale-free graph, regular attack with 10,000 attack edges, 5 seeds, total trust set to 2m |
| In a 5-community synthetic graph (one 2,000-node core plus four 2,000-node satellite communities linked to the core by 500 edges each, average degree 10), distributing 50 seeds across all communities (10 each) outperforms confining all 50 seeds to the core community, for SybilRank, EigenTrust, and Mislove's CD alike; SybilRank remains most accurate under both seeding strategies | Synthetic multi-community graph, attack edges varied 0–5,000 |
| Under a targeted attack (200 attack edges connected to the k non-Sybil nodes nearest a trust seed, k varied 1,000–10,000), all schemes degrade as k shrinks (attack edges concentrate nearer the seed); SybilRank degrades least but still degrades at small k | Facebook graph, 5,000-node regular-attack Sybil region |
| Hadoop/MapReduce prototype processes a 160-million-node synthetic scale-free graph in under 33 hours, with execution time increasing almost linearly with graph size across sizes from 10M to 160M nodes, using O(log n) power iterations | Amazon EC2 cluster of 11 m1.large instances (1 master, 10 slaves) |
| Mean random-walk length needed to reach a fixed total variation distance of 0.01 from the stationary distribution is much longer for confirmed Sybils than for random users in the same community (random-user walks mostly <100 steps) | 25 Louvain-detected Tuenti communities >100K nodes; 1,000 random users and 100 confirmed Sybils sampled per community |

### Parameters
- Power iterations w: set to O(log n); the paper does not report the specific integer used for the Tuenti deployment (11.2M-node graph) beyond the asymptotic form, stating only that measured Sybil random-walk lengths (Figure 11) exceeded the power-iteration count SybilRank actually used.
- Trust seeds K: 50 used in the main simulated comparisons (1 chosen from the top-10 highest-degree non-Sybil nodes, 49 random non-Sybil nodes); for schemes supporting only a single seed, 1 randomly chosen top-10-degree node is used for a fair comparison. In the Tuenti deployment, seeds are chosen per Louvain-detected community after manual verification of ~4 candidate nodes per community (25 communities >100K nodes).
- Attack-edge count g: varied per experiment; up to 1,500 (Facebook, regular attack) and up to 15,000 (synthetic scale-free graph) in the ranking-quality comparison; 10,000 in the seed-distance experiment; 0–5,000 in the multi-community experiment; 200 in the targeted-attack experiment.
- Non-attack (intra-Sybil) edges per Sybil, d: fixed at 4 in the main attack-strategy simulations; varied 4–40 in the EigenTrust-comparison experiment (Figure 7).
- Sybil region size: fixed at 5,000 nodes in all simulated attacks, described as chosen to "stress-test each scheme."
- ROC fixed false-rate pivot: 20%, used to compute the corresponding other false rate for comparison across schemes.
- Total variation distance for mixing-time measurement: 0.01, used to define the walk length compared between Sybils and random users in each Tuenti community.
- EigenTrust reset probability: 0.15, run to convergence (not early-terminated), following the cited EigenTrust paper's own setting.

### Stated limitations
The paper states SybilRank's central limitation is inherent to the open nature of OSNs: a fake
account that succeeds in befriending many real users accumulates trust and is ranked as non-Sybil,
which is why the fake proportion in the Tuenti-ranked list falls sharply above the 200K mark. It
states that no social-graph-based Sybil defense, including SybilRank, can currently produce a
binary Sybil/non-Sybil classification with an acceptable false-positive rate, so a fixed
ranked-list pivot cannot substitute for manual inspection — SybilRank instead reports the fake
proportion per ranked-list interval so an operator can allocate inspection effort. It states its
own security guarantee (Theorem 1) is derived under the assumption that attack edges are placed
uniformly at random by the Sybils, not under the more effective targeted-attack strategy of
placing attack edges close to trust seeds; the paper's own targeted-attack experiment (Section 6.5)
shows all schemes, including SybilRank, degrade as the targeting gets closer to the seed. It states
that whether real social networks' non-Sybil mixing time is truly O(log n), or has an unknown
larger constant factor, or grows faster than O(log n), is unresolved, citing two independent
measurement studies that found some social networks mix slower than expected; SybilRank's
robustness to this uncertainty is qualified, not eliminated — the paper states SybilRank does not
depend on the absolute mixing time value, only on the non-Sybil region mixing faster than the full
graph including Sybils, but concedes that using too few iterations relative to the true non-Sybil
mixing time risks starving trust to non-Sybil users poorly connected to any seed. For the Tuenti
deployment, the paper states it could not evaluate SybilRank with the same false positive/negative
and ROC metrics used in simulation, because manually labeling ground truth at Tuenti's scale was
infeasible, and states it could not disclose the exact fraction of network-wide fakes SybilRank
misses, citing confidentiality constraints. It states pre-processing (pruning extremely-high-degree
nodes' edges and deferring very recent accounts) was required before applying SybilRank to Tuenti
to control two identified sources of error — well-maintained high-degree fakes and low-connectivity
new honest accounts — meaning the deployed system is not the unmodified base algorithm.

### Requirements it places on the rest of the system
Requires the operator to hold the complete social graph as an undirected graph, and requires an
initial manually verified set of non-Sybil trust seeds (drawn per detected community, not
globally) before the mechanism can run at all. Requires the non-Sybil region of the graph to be
well-connected, non-bipartite, and fast-mixing relative to the full graph including Sybils
(mixing time strictly less than that of the full graph), which is a property of the graph
structure that must be verified for a given deployment, not assumed by construction — the paper's
own Tuenti section measures an approximation of this gap rather than asserting it. Requires Sybils
to be limited in the number of attack edges they can form into the non-Sybil region; the paper
states this assumption can fail if fake accounts can cheaply befriend large numbers of real users,
and that the mechanism's accuracy specifically degrades for accounts that do so, regardless of any
other property of the account. Requires a downstream process (human review, or an automated
challenge such as a CAPTCHA) to consume the ranked list and its per-interval fake-proportion
annotations, because SybilRank itself produces a ranking and an approximate fake-density curve,
not an admission or suspension decision. Community detection (the paper uses the Louvain method)
must be re-run to identify the graph's community structure before seed placement, adding an O(m)
preprocessing cost (m = edge count) ahead of the O(n log n) trust-propagation and ranking cost.

### Contradicts
None found among the papers in this corpus. This entry corrects a claim commonly associated with
this line of work: SybilRank's security guarantee (Theorem 1) is stated only for the case where
attack edges are placed uniformly at random; the paper's own experiments (Section 6.5) show
detection accuracy is measurably worse under a targeted-attack placement strategy, so a categorical
claim that SybilRank bounds Sybil rank under any adversarial edge-placement strategy is not
supported by this paper.

### References worth retrieving
- H. Yu, M. Kaminsky, P. B. Gibbons, A. Flaxman. "SybilGuard: Defending Against Sybil Attacks via Social Networks." SIGCOMM 2006 — foundational
- H. Yu, P. Gibbons, M. Kaminsky, F. Xiao. "SybilLimit: A Near-Optimal Social Network Defense Against Sybil Attacks." IEEE S&P 2008 — competing (directly compared, SL in Figure 6)
- G. Danezis, P. Mittal. "SybilInfer" (implied by cited [23]) — competing (directly compared, SI in Figure 6; its Metropolis-Hastings convergence uncertainty is discussed as a likely cause of its performance drop)
- N. Tran, J. Li, L. Subramanian, S. S. Chow. "Optimal Sybil-resilient Node Admission Control." INFOCOM 2011 — competing (GateKeeper, directly compared, GK in Figure 6)
- S. D. Kamvar, M. T. Schlosser, H. Garcia-Molina. "The EigenTrust Algorithm for Reputation Management in P2P Networks." WWW 2003 — competing (directly compared, ET in Figure 6, and the subject of a dedicated comparison section, §6.3)
- A. Mislove, B. Viswanath, K. P. Gummadi, P. Druschel. "You are Who You Know: Inferring User Profiles in Online Social Networks." WSDM 2010 — competing (Mislove's CD, directly compared)
- B. Viswanath, A. Post, K. P. Gummadi, A. Mislove. "An Analysis of Social Network-based Sybil Defenses." SIGCOMM 2010 — foundational (supplies the unifying trust-ranking evaluation framework this paper's comparison methodology reuses)
- Z. Gyongyi, H. Garcia-Molina, J. Pedersen. "Combating Web Spam with TrustRank." VLDB 2004 — foundational
- A. Mohaisen, A. Yun, Y. Kim. "Measuring the Mixing Time of Social Graphs." IMC 2010 — attack/critique (measurement study cited as evidence that some social networks mix slower than the O(log n) assumption)
- M. Motoyama, D. McCoy, K. Levchenko, G. Voelker, S. Savage. "Dirty Jobs: The Role of Freelance Labor in Web Service Abuse." USENIX Security 2011 — foundational (cited evidence that most fake-account connections are to other fakes, supporting the limited-attack-edge assumption)
- C. Lesniewski-Laas, M. F. Kaashoek. "Whanau: A Sybil-proof Distributed Hash Table." NSDI 2010 — competing (already in this batch, LESNIEWSKI-LAAS-NSDI-10)
- A. Mislove, A. Post, P. Druschel, K. P. Gummadi. "Ostra: Leveraging Social Networks to Thwart Unwanted Traffic." NSDI 2008 — competing (already in this batch, MISLOVE-NSDI-08)
- D. N. Tran, B. Min, J. Li, L. Subramanian. "Sybil-Resilient Online Content Rating." NSDI 2009 — competing (already in this batch's set, TRAN-NSDI-09)
- H. Yu, C. Shi, M. Kaminsky, P. B. Gibbons, F. Xiao. "DSybil: Optimal Sybil-Resistance for Recommendation Systems." IEEE S&P 2009 — competing

### Verbatim extracts
- "an early-terminated random walk... has a higher degree-normalized... landing probability to land at a non-Sybil node than a Sybil node"
- "the total number of Sybils that rank higher than non-Sybils is O(g log n)"
- "∼90% of the 200K accounts that SybilRank designated as most likely to be fake, actually warranted suspension"
- "an 18-fold increase in the efficiency"
- "SybilRank's limitation lies in the open nature of OSNs"
- "finishes in less than 33 hours" (160M-node graph)
