## [SAFARPOOR-DEHKORDI-AAMAS-25] More Efficient Sybil Detection Mechanisms Leveraging Resistance of Users to Attack Requests
**Citation:** Ali Safarpoor Dehkordi, Ahad N. Zehmakan. "More Efficient Sybil Detection Mechanisms Leveraging Resistance of Users to Attack Requests." AAMAS, 2025. DOI 10.5555/3709347.3743572.
**Retrieved:** full text via https://arxiv.org/abs/2501.16624
**Source URL:** https://arxiv.org/abs/2501.16624
**Domain:** F

### What it does
This mechanism improves an existing Sybil (fake-account) detector's accuracy by running two
graph-algorithm preprocessing steps before that detector runs, using the concept of a benign
user's resistance to an attack request — whether that user rejects a friend/connection request
from a fake account. Resistance r(v) of a user v is 0 (accepts any incoming request) or 1
(rejects). Revealing a user's resistance means testing it directly, described as sending a
friend request from a dummy Sybil account to that user and observing accept/reject.

Preprocessing step one, Maximizing Benigns (MB), selects a budget of k users whose resistance
to reveal so that revealing them provably or heuristically identifies the largest expected count
of additional users as benign. A user is newly discoverable as benign if a path exists from it to
a user already known to be benign, where every user on that path (except possibly the endpoint
itself) has been revealed to have resistance 1 (a resistant user only accepts requests from users
it already trusts, so an unbroken chain of resistant users back to a known-benign anchor rules
out a Sybil origin for that path). The paper proves this maximization problem is #P-hard to
compute exactly (via a reduction from the a-b Connectedness for Induced Subgraphs problem) and
that no polynomial-time (1-1/e)-approximation exists unless NP ⊆ DTIME(n^(O(log log n))) (via
reduction from Maximum Coverage). It gives two algorithms: a Monte Carlo Greedy algorithm that
estimates the objective by repeated random sampling (its sample count is derived from Hoeffding's
inequality to bound estimation error within ε at confidence α), and a Traversing algorithm that
greedily picks, at each step, the not-yet-revealed user with highest (resistance probability ×
count of not-yet-benign in-neighbors), updating in-neighbor counts as each reveal resolves.

Preprocessing step two, Discovering Potential Attack Edges (PAE), identifies edges likely to run
from a Sybil into the benign region. A potential attack edge is defined as an incoming edge to a
known-benign user whose resistance equals 0 (accepts requests indiscriminately), from a user
outside both the known-benign and known-Sybil sets. Because no two candidate reveals' discovered
edge-sets overlap in this formulation, selecting the k benign users with the highest expected
value of (1 − resistance-probability) × (count of qualifying in-neighbors) is provably optimal,
computed in linear time using a median-of-medians top-k selection. Downstream, the discovered
potential attack edges are used to reduce the edge weight given to them in a detection algorithm
that relies on homophily (the tendency of connected users to share a benign/Sybil label).

The paper also introduces a synthetic-dataset generation framework that overlays a Sybil region
onto a real benign social graph, offering three named attack strategies for how a Sybil "copies"
a benign subgraph and forms attack edges into it: Random (uniform request targeting), Preferential
Attachment (a modified Barabási-Albert model that also weights by a target's history of accepting
prior attack requests), and BFS (breadth-first traversal outward from each Sybil's paired benign
node, falling back to Preferential Attachment when BFS cannot reach enough targets).

### Measured results

| Result | Conditions |
|---|---|
| Traversing algorithm completes in 119 milliseconds vs. 52 minutes for Monte Carlo Greedy, at budget k=30 | Facebook dataset (SNAP), Preferential Attachment attack strategy |
| Traversing and both Monte Carlo Greedy variants "significantly outperform" Random, Highest-Resistance, and Highest-Resistance-and-Degree baselines on discovered-benigns count; Traversing outperforms both Monte Carlo variants | Facebook dataset (4,039 nodes, 88,234 undirected edges, avg in/out-degree 43.69), budget k ranging 1 to unstated max, three attack strategies; qualitative claim from Figure 2, no numeric gap stated in the main text |
| Proposed PAE algorithm outperforms Random selection at discovering potential attack edges, at all tested budgets | Facebook dataset; proven optimal by construction, not merely observed |
| ~20% of the PAE algorithm's discovered potential attack edges are true attack edges (Sybil-to-benign), for various budgets; this ratio approaches that of a Full-Knowledge algorithm (which knows the true resistance values, unavailable to the proposed algorithm) as budget grows | Facebook dataset, all three attack strategies |
| Sybil-detection AUC (Area Under the Curve) after MB preprocessing (Traversing) rises for all three detectors and all three attack strategies over no preprocessing (Init): SybilSCAR 0.924→0.988 (Random), 0.876→0.954 (Preferential Attachment/BA), 0.986→0.995 (BFS); SybilWalk 0.966→0.998 (Random), 0.929→0.972 (BA), 0.985→0.996 (BFS); SybilMetric held at 1.00/1.00 (Random), 1.00/1.00 (BA), 0.97→0.99 (BFS) | Facebook dataset, known-benign training set of 80 users (2% of benigns, matched by an equal count of Sybils), Sybil fraction fixed at 10% of the network, MB+PAE preprocessing budget fixed at 1% of benigns |
| Adding PAE discovery after MB (MB+PAE) changes AUC inconsistently versus MB alone: e.g. SybilMetric under BA drops from 1.00 to 1.00 (no change), under Random unchanged at 0.988/0.998, under BA SybilSCAR drops slightly from 0.954 to 0.944, under BFS SybilMetric rises from 0.99 to 1.00 | Same setup as above; the paper states PAE-based weight reduction "enhances the AUC in some cases, but not always" |
| Sybil fraction fixed at ~10% of network size in synthetic attacks, non-resistant fraction fixed at 25% of benign users, based on external prevalence figures the paper cites (not measured in this paper) | Applies to all reported experiments; cited external figures: ~16% Sybil rate on Facebook per one study, ~10% fake-account rate on Twitter per a 2013 study, 18% immediate accept / 52% undecided after two weeks / 30% decline in a university fake-friend-request study |

### Parameters
- Budget k: varied from 1 to an unstated maximum in the MB and PAE experiments (Figures 2–3); fixed at 1% of the benign-set size for the classification-preprocessing experiments (Table 1).
- Known-benign/training-set size: 2% of the benign set, matched by an equal count of known Sybils; concretely 80 (Facebook), 200 (Pokec), 150 (LastFM), 200 (Twitter) users.
- Sybil-set size: fixed at approximately 10% of the network, a pick attributed to the cited 16% (Facebook) and 10% (Twitter) real-world Sybil-rate studies, not derived from this paper's own measurement.
- Non-resistant fraction: fixed at 25% of benign users, a pick attributed to the cited university fake-friend-request study (18% immediate accept, 52% undecided after two weeks).
- Resistance-probability generator: p_r(v) = (1 − r(v))·x³ + r(v)·(1 − x³) for x drawn uniformly on [0,1]; the paper states that for r(v)=1 this gives P(p_r(v) ≥ 0.5) = 0.79 and an average probability value of 0.75, with no derivation offered beyond restating the formula's output at that one input.
- Random-strategy multiplier c: set to 4 in all attack strategies, chosen so that the expected accepted-attack count matches the desired non-resistance ratio of 25%.
- Monte Carlo Greedy sample count R: set to ⌈k²·Δ_in²·ln(1/(1−α)) / (2ε²)⌉ via Hoeffding's inequality, for a caller-chosen error margin ε and confidence α; no specific ε/α values are stated as used in the reported experiments.
- Datasets: Facebook (4,039 nodes, 88,234 undirected edges, avg degree 43.69, source SNAP), Twitter (10,000 nodes, 350,600 directed edges, avg degree 35.06, source SNAP), LastFM (7,624 nodes, 27,806 undirected edges, avg degree 7.29, source SNAP), Pokec (10,000-node induced subgraph of benigns, 94,066 directed edges, avg degree 9.4).

### Stated limitations
The paper states its own greedy-preprocessing objective function for Maximizing Benigns is not
submodular (proved in an appendix), so the standard (1−1/e) approximation guarantee for greedy
algorithms does not apply to it, despite empirically strong performance. It states exact
computation of the Maximizing Benigns objective is #P-hard, forcing reliance on either Monte
Carlo estimation (computationally far slower, 52 minutes vs. 119 milliseconds at k=30 on
Facebook) or the heuristic Traversing algorithm, which carries no proven approximation ratio.
It states current sybil-detection methods, including its own preprocessing approach, are
"vulnerable to dataset biases, especially when preprocessing reveals new benigns and skews the
dataset," and lists developing bias-robust algorithms as future work. It states that reducing
discovered potential-attack-edge weights (rather than directly incorporating potential-attack-edge
information into the detection algorithms) produces an inconsistent AUC benefit, and identifies
direct incorporation as an open avenue rather than a solved problem. It states that finding a
Maximizing Benigns algorithm with a proven theoretical approximation guarantee (given the proven
non-submodularity) remains future work. It states its own preprocessing algorithms assume the
attacker (Sybil accounts) does not itself exhibit resistance and do not model an attacker that
selectively rejects requests to other suspected Sybils to reduce detectable homophily, though the
paper notes this is a real possibility for attackers to exploit.

### Requirements it places on the rest of the system
Requires an ability to directly test a specific user's resistance to an attack request — the
paper's operational definition is sending a friend request from a dummy Sybil account and
observing whether it is accepted — which consumes a "budget" the paper treats as scarce (avoiding
"bombarding all users"); the rest of the system must supply this test channel and bound its use.
Requires a pre-existing set of known-benign and known-Sybil users to seed the graph traversal
(2% of the benign population, matched one-to-one with an equal count of known Sybils, in the
paper's own experiments); the algorithms do not initialize from zero external labels. Requires
the underlying social graph's edges (accept/reject relationships) to be observable to the
component running the preprocessing, including in-degree and neighbor-set structure, to compute
the per-node scores both algorithms use. The downstream detection algorithms (SybilSCAR,
SybilWalk, the logistic-regression classifier the paper calls SybilMetric) must expose either an
extra set of newly discovered benign labels (for the MB preprocessing output) or an edge-weighting
input (for the PAE preprocessing output) for the composition to take effect — the paper measures
benefit only through those two specific injection points.

### Contradicts
None found among the papers in this corpus. The paper's own dataset-generation critique
(Section 2) states that prior synthesized Sybil datasets (citing SybilBelief's synthesized Sybil
region and another cited framework's uniform-random-edge assumption) are less realistic than its
own resistance-based attack strategies — an attributed methodological critique of those specific
prior works, not a disagreement about a shared measured quantity.

### References worth retrieving
- Q. Cao, M. Sirivianos, X. Yang, T. Pregueiro. "Aiding the detection of fake accounts in large scale social online services." NSDI 2012 — competing (SybilRank; already in this batch, CAO-NSDI-12)
- Prior work introducing SybilWalk (cited [20]) — competing (one of the three detection algorithms this paper's preprocessing is measured against)
- Prior work introducing SybilSCAR (cited [38]) — competing (unifies random-walk and belief-propagation detection; one of the three detectors measured against)
- S. Asghari, M. Haghir Chehreghani, M. Haghir Chehreghani. "On using node indices and their correlations for fake account detection." IEEE Big Data 2022 (cited [2]) — competing (source of the logistic-regression detector this paper calls SybilMetric)
- Prior work on SybilBelief, a semi-supervised belief-propagation Sybil detector (cited [15]) — competing (cited critically for its synthesized-dataset methodology)
- G. L. Nemhauser, L. A. Wolsey, M. L. Fisher. Submodular maximization guarantee (cited [29]) — foundational (the (1−1/e) greedy guarantee this paper shows does not apply to its own objective)
- A.-L. Barabási, R. Albert. "Emergence of scaling in random networks." Science 1999 (cited [3]) — foundational (Barabási-Albert model underlying the Preferential Attachment attack strategy)
- Vishwanath. University fake-Facebook-profile friend-request study (cited [35]) — foundational (empirical source for the paper's chosen 25% non-resistance parameter)
- Y. Boshmaf et al. "Íntegro: Leveraging victim prediction for robust fake account detection in large scale OSNs." Computers & Security 2016 (cited [7]) — competing
- A. Breuer, R. Eilat, U. Weinsberg. "Friend or Faux: Graph-Based Early Detection of Fake Accounts on Social Networks." WWW 2020 (cited [8]) — competing
- A. Breuer, N. Khosravani, M. Tingley, B. Cottel. "Preemptive Detection of Fake Accounts on Social Networks via Multi-Class Preferential Attachment Classifiers." KDD 2023 (cited [9]) — competing

### Verbatim extracts
- "user resistance to attack requests (friendship requests from sybil accounts)"
- "there is no (1−1/e)-approximation polynomial time algorithm for the MB problem"
- "computing f(·) is #P-hard"
- "Traversing algorithm completes in 119 milliseconds, while the Monte Carlo Greedy algorithm takes 52 minutes"
- "around 20% of found PAEs are attack edges"
- "vulnerable to dataset biases, especially when preprocessing reveals new benigns"
