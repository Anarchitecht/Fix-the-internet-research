## [SUN-ASONAM-20] TrustGCN: Enabling Graph Convolutional Network for Robust Sybil Detection in OSNs
**Citation:** Yue Sun, Zhi Yang, Yafei Dai. "TrustGCN: Enabling Graph Convolutional Network for Robust Sybil Detection in OSNs." IEEE/ACM ASONAM, 2020. DOI 10.1109/ASONAM49781.2020.9381325.
**Retrieved:** full text via https://ieeexplore.ieee.org/document/9381325 (matched: title, authors Yue Sun/Zhi Yang/Yafei Dai, Peking University, ASONAM 2020 header confirmed in first 3000 characters of the file)
**Source URL:** https://ieeexplore.ieee.org/document/9381325
**Domain:** F

### What it does
TrustGCN detects fake accounts (Sybils) in an online social network (OSN) by combining a graph convolutional network (GCN, a neural network that classifies a node by iteratively aggregating feature vectors from its graph neighbors) with a social-graph-based trust score, so that a Sybil cannot manipulate its local neighborhood to evade the GCN classifier the way it can evade an unweighted GCN. The mechanism runs in two stages. The trust-propagation stage runs a short random walk of K iterations (the paper sets K=4) starting from a set of nodes already known to be real ("trust seeds"), computing at each iteration a landing-probability vector over all nodes, separately tracking a positive landing probability T+ and a negative landing probability T- that flips sign whenever the walk crosses a negative edge (an edge recording a rejected friend request); ending the walk early, before it converges, keeps trust concentrated in the real-user region because that region mixes fast while few edges cross into the Sybil region. The trust-guided-convolution stage multiplies the graph's signed adjacency matrix by the combined landing-probability vector T = T+ + T- to produce a weighted adjacency matrix, then runs the standard GCN's neighbor-feature-aggregation step over this weighted graph instead of the original one, so a neighbor with a low trust score contributes little to the feature vector computed for the node being classified, whether or not that neighbor was added or manipulated by the attacker in the current time step.

### Measured results
The paper reports its comparisons as line plots (Figures 7 and 9) with no accuracy, precision, recall, or F1 percentage stated as a number in the running text; only the graph and dataset construction are stated numerically.

| Quantity | Value | Conditions |
|---|---|---|
| Graph size | about 60,000 users, 2.2 million positive edges, 0.4 million negative edges | Signed friend-request graph built from a regional Peking University (PKU) network on the Renren OSN |
| Ground-truth Sybils | 5,500 accounts | Fake accounts previously identified by Renren's own security team |
| Labeled fraction | 5% of ground-truth nodes chosen at random as training labels; the remaining 95% predicted | Same PKU dataset |
| Average rejection rate | about 0.3 for real users vs. about 0.3 stated as "high" for Sybils (the paper's own text states real users have a low rejection rate of 0.3 and Sybils a high rejection rate of 0.3, without giving the Sybil-side number distinctly; treat this figure as approximate, read from Figure 4, not as an exact reported statistic) | Same PKU dataset |
| GCN training | batch size 512, learning rate 0.01, Adam optimizer, TensorFlow implementation | Same PKU dataset |
| TrustGCN propagation depth | K = 4 random-walk iterations | Same PKU dataset, same GCN hyperparameters as the plain-GCN experiment |

Qualitative findings the paper states without an accompanying number: plain GCN accuracy "drops dramatically" under the collusion attack as the count of fake positive links among Sybils grows; GCN is "more vulnerable" to the promotion attack (Sybils sending or receiving requests to/from a small number of compromised real accounts) than to collusion or self-rejection, with accuracy dropping "significantly lower"; TrustGCN "significantly enhances resilience" to all three attacks compared to plain GCN; TrustGCN shows "slight accuracy drop" as positive collusion links increase, attributed to inactive Sybils that have not yet generated enough negative (rejected) links to be distinguished, a population the paper states TrustGCN can still recall once those accounts become active.

### Parameters
- K (random-walk / power-iteration termination step count for trust propagation): 4, stated as on the order of O(log n) steps in general, with n the node count.
- Batch size: 512.
- Learning rate: 0.01, Adam optimizer.
- Labeled-data fraction: 5% of ground-truth Sybil and real nodes.
- Attack-strategy parameters, defined but not given specific swept values in the retrieved text: alpha (fraction of Sybils participating in an attack), beta (fraction of collusion, self-rejection, or promotion links among participating Sybils, meaning differs per attack type), gamma (probability that a compromised real user accepts a promotion request).

### Stated limitations
The paper states that graph-based Sybil defenses in general (the class TrustGCN extends) cannot use node feature information for classification and are usually used to produce a ranking rather than a binary classification, because a substantial fraction of Sybils still rank low even when not separated cleanly from real accounts. The paper states TrustGCN shows a slight accuracy drop as the number of positive collusion links grows, because Sybils that have not yet launched their attack present with few negative links and get misclassified as real, and states this is mitigated only after those accounts start generating requests and TrustGCN can recall them, not before. The paper states its underlying structural assumption — that Sybils accumulate more rejected than accepted friend requests, producing a negative or sparse cut between the Sybil and non-Sybil regions of the graph — as an assumption the mechanism depends on, not a property it proves holds in every OSN.

### Requirements it places on the rest of the system
TrustGCN requires a signed graph in which edges record friend-request acceptance and rejection outcomes (or, for the unsigned-graph variant, a graph where the number of edges Sybils can forge to real users is limited); a system that only records final friendships and discards rejected-request events cannot supply this signal. It requires a pre-identified set of "trust seed" nodes already known to be real, from which the random walk starts; the mechanism gives no method for producing that seed set and depends on it being externally supplied and honest. It requires the real-user subgraph to be fast-mixing internally and to expose a comparatively sparse or negative cut toward the Sybil region, because the random walk's early termination is what keeps trust concentrated on the real side — a network where Sybils' rejection rate does not exceed real users' rejection rate breaks the mechanism's separating assumption. It requires per-node feature vectors (the paper uses activity features such as friend-request frequency, acceptance fraction, and clustering coefficient) in addition to the graph structure, since the GCN aggregation step operates on both edges and features jointly.

### Contradicts
The target registry's stated reason for retrieving this paper ("why_needed") asserts it gives "a measured accuracy comparison against SybilRank and SybilBelief on the same graph." The retrieved full text contains no such comparison: SybilBelief appears only once, as bibliography entry [10], never as an experimental baseline, and SybilRank is not mentioned anywhere in the text. The paper's only quantitative comparison is TrustGCN against plain GCN (Figure 9), read from line plots with no accuracy numbers stated in the prose. This is a mismatch between the registry's description and the paper's actual content, not a mismatch of the retrieved document's identity — the retrieved file is confirmed to be TrustGCN itself. No disagreement found against any other entry in this batch.

### References worth retrieving
- Yu, Kaminsky, Gibbons, Flaxman, "Sybilguard: Defending against sybil attacks via social networks," SIGCOMM 2006 — foundational (the random-walk social-graph defense TrustGCN's trust-propagation stage extends)
- Yu, Gibbons, Kaminsky, Xiao, "Sybillimit: A near-optimal social network defense against sybil attacks," IEEE S&P 2008 — foundational
- Cao, Sirivianos, Yang, Pregueiro, "Aiding the detection of fake accounts in large scale social online services" (SybilRank), NSDI 2012 — competing (the graph-ranking approach the registry expected as a measured baseline but that this paper's retrieved text does not compare against)
- Gong, Frank, Mittal, "Sybilbelief: A semi-supervised learning approach for structure-based sybil detection," IEEE TIFS 9(6), 2014 — competing (cited only in the bibliography, not used as a measured experimental baseline in the retrieved text)
- Danezis, Mittal, "Sybilinfer: Detecting sybil nodes using social networks," NDSS 2009 — competing
- Boshmaf, Ripeanu, Beznosov, "Integro: Leveraging victim prediction for robust fake account detection in osns," NDSS 2015 — competing (feature-based detection baseline discussed in related work)
- Xue, Yang, Yang, Wang, Chen, Dai, "Votetrust: Leveraging friend invitation graph to defend against social network sybils," INFOCOM 2013 — foundational (source of the PKU/Renren Sybil dataset used here)
- Yang, Wilson, Wang, Gao, Zhao, Dai, "Uncovering social network sybils in the wild," ACM TKDD 8(1), 2014 — foundational (source of the activity-level features TrustGCN uses)
- Dai, Li, Tian, Huang, Wang, Zhu, Song, "Adversarial attack on graph structured data," ICML 2018 — attack (gradient-based GCN adversarial-perturbation method TrustGCN's threat model is adapted from)
- Zugner, Akbarnejad, Gunnemann, "Adversarial attacks on neural networks for graph data," arXiv 2018 — attack
- Douceur, "The sybil attack," Peer-to-Peer Systems / IPTPS 2002 — foundational

### Verbatim extracts
"TrustGCN significantly outperforms GCN in the robustness"
"the number of ties that the adversary can forge between Sybils and honest nodes is restricted"
"real users have a low rate of 0.3 to be rejected by others, whereas Sybils have a high rejection rate"
"we terminate the power iterations after small number of K iterations"
"TrustGCN has slight accuracy drop with the increasing number of positive collusion links"
"graph-based defenses cannot leverage the feature information for high classification accuracy"
