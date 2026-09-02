## [YANG-IMC-11] Uncovering Social Network Sybils in the Wild
**Citation:** Zhi Yang, Christo Wilson, Xiao Wang, Tingting Gao, Ben Y. Zhao, Yafei Dai. "Uncovering Social Network Sybils in the Wild." ACM Internet Measurement Conference (IMC), 2011. DOI 10.1145/2068816.2068841.
**Retrieved:** full text via https://arxiv.org/pdf/1106.5321
**Source URL:** https://arxiv.org/pdf/1106.5321
**Domain:** F

### What it does
The paper reports a measurement of Sybil accounts on a real, deployed online social network (OSN),
Renren (120 million users at the time, the largest OSN in China), using account data the operator
supplied under a research collaboration. It builds a real-time detector from behavioral signals
observable at the OSN operator and evaluates whether the graph-topological assumption behind
published decentralized Sybil defenses (SybilGuard, SybilLimit, SybilInfer, SumUp) holds for Sybils
actually operating in the wild, rather than for Sybils synthetically injected into a real social graph.

Detector mechanism: for each account the operator computes three per-account signals directly from
friend-request logs — invitation frequency (friend requests sent per fixed time window), the
fraction of an account's outgoing friend requests that are accepted, and the fraction of its
incoming friend requests it accepts. It adds one graph signal, the clustering coefficient of an
account's first 50 friends (added in time order), computed from invitation edges alone, which
requires no waiting on recipient responses. A threshold rule — outgoing-acceptance ratio < 0.5 AND
invitation frequency < 20 per window AND clustering coefficient < 0.01 — flags an account as a
Sybil. The paper also trains a support vector machine (SVM) on the same four signals and compares
its accuracy to the threshold rule.

Topology analysis mechanism: build a graph restricted to the 667,723 detected Sybil accounts and
the edges among them ("Sybil edges"), separately from edges connecting a Sybil to a normal account
("attack edges"). Decompose the Sybil-only graph into connected components and measure, per
component, the ratio of Sybil edges to attack edges — the quantity community-detection Sybil
defenses require to exceed 1 for a community to be separable by a graph cut. Reconstruct, per
account, the chronological sequence of edge creation from timestamps to test whether Sybil-Sybil
edges are created together (deliberate) or interleaved randomly with edges to normal accounts
(accidental).

### Measured results

| Result | Value | Conditions |
|---|---|---|
| Sybil accounts identified and banned by the deployed detector | 100,000 | Renren production deployment, August 2010 to February 2011 |
| Total Sybil population analyzed | 660,000 (100,000 detector-caught + 560,000 caught by Renren's prior techniques, 2008–Feb. 2011) | Same Renren dataset |
| Threshold-rule detector accuracy | True Sybil classified Sybil 98.68%, classified non-Sybil (false negative) 1.32%; true non-Sybil classified non-Sybil 99.5%, classified Sybil (false positive) 0.5% | 1000 ground-truth Sybil + 1000 ground-truth normal accounts, verified by a volunteer team examining profile data; threshold rule = outgoing-acceptance < 0.5 AND frequency < 20/window AND clustering coefficient < 0.01 |
| SVM classifier accuracy on the same signals | True Sybil classified Sybil 98.99%/1.01% false negative; true non-Sybil 99.34%/0.66% false positive | Same 2000-account ground truth set, 5-fold split (4 folds train, 1 fold test) |
| Average outgoing friend-request acceptance ratio | Normal accounts 79%; Sybil accounts 26% | Same 2000-account ground-truth set |
| Incoming friend-request acceptance | 80% of Sybils accept all incoming requests | Same ground-truth set |
| Average clustering coefficient over first 50 friends | Normal accounts 0.0386; Sybil accounts 0.0006 | Same ground-truth set |
| Fraction of ground-truth Sybils that are recorded as female | 77.3% | Same 1000-Sybil ground-truth set (overall Renren population is 46.5% female) |
| Threshold separating most Sybils by invitation frequency | >20 invitations per time window flags as Sybil; a 40-requests/hour threshold catches approximately 70% of Sybils at zero false positives | Same ground-truth set, both 400-hour and 1-hour windows |
| Sybils with at least one edge to another Sybil | 20% of the 667,723 detected Sybils | Full 660,000-account Sybil population, Renren social graph |
| Sybils with no Sybil-Sybil edge at all | more than 70% | Same population |
| Number of connected components in the Sybil-only subgraph | 7,094 | Same population |
| Component size distribution | 98% of components have fewer than 10 members | Same population |
| Largest Sybil component | 63,541 Sybil accounts, 134,941 Sybil edges, 9,848,881 attack edges, 6,497,179 distinct normal-account "audience" reached | Same population, Table 2 |
| Ratio of attack edges to Sybil edges, all five largest components | every one of the five largest components has more attack edges than Sybil edges (Table 2: ratios of approximately 73:1, 903:1, 116:1, 307:1, 361:1) | Same population |
| Position of every Sybil component on the attack-edge-vs-Sybil-edge scatter plot | all components fall above the line attack edges = Sybil edges | Same population, Figure 7 |
| Degree distribution within the largest component | 34.5% of member Sybils connect to exactly 1 other Sybil; 93.7% connect to 10 or fewer | Largest component (63,541 accounts) only |
| Fraction of Sybil accounts formally connected to other Sybils via a single large accidental component | 69% of the 30% connected minority (approximately 65,000 accounts) belong to one component | Same population |

### Parameters
Ground-truth labeled set: 1000 Sybil accounts and 1000 normal accounts, manually verified.
Cross-validation split: 5 subsamples, 4 for SVM training, 1 for test. Clustering-coefficient window:
each user's first 50 friends by time order. Threshold-detector cutoffs: outgoing-acceptance ratio
0.5, invitation frequency 20 requests per fixed time window, clustering coefficient 0.01 (these
three values are the deployed detector's chosen operating point; the paper does not report a range
swept over them, only the resulting accuracy at this operating point). Adaptive online tuning of the
deployed detector's thresholds is mentioned but its mechanism is withheld at Renren's request for
confidentiality and security.

### Stated limitations
The paper withholds the deployed detector's adaptive threshold-tuning mechanism, citing Renren's
security and confidentiality requirements, so the operational detector is not fully specified. The
analysis covers one OSN (Renren) over one measurement window (accounts banned through February
2011) and the authors do not claim the found proportions (20% Sybil-Sybil connectivity, more attack
edges than Sybil edges in every measured component) generalize numerically to other social networks,
though they state the qualitative conclusion — that community-based defenses' core assumption is
untested and appears false in this deployment — as general grounds for new detection approaches.
The four signals depend on friend-request logs an OSN operator holds internally; the paper notes
that on networks where only public follower/followee data is available (Twitter), the equivalent
detection has previously worked, but that Facebook- and Renren-style OSNs expose no equivalent
public signal, so their detector requires operator-side data access it does not describe as portable
to a peer without that access.

### Requirements it places on the rest of the system
A deployment of this detection approach needs a party that observes, for every account, its full
inbound and outbound friend-request stream with timestamps and per-request accept/reject outcomes —
data available only to the OSN operator itself in the studied deployment, not to any external
observer or peer. Community-graph Sybil defenses (SybilGuard, SybilLimit, SybilInfer, SumUp) that
this paper evaluates require, to succeed, that the ratio of Sybil-Sybil edges to Sybil-normal
(attack) edges exceed 1 within some cut of the social graph; the measured population here violates
that precondition in every one of the largest observed components, so a design relying on those
defenses for Sybil identification must not assume the precondition holds against an unconstrained
snowball-sampling attacker recruiting from the honest population, since honest recruitment strategy
alone (not deliberate Sybil-Sybil linking) is what created the small fraction of Sybil-Sybil edges
observed.

### Contradicts
The paper's own result contradicts the assumption underlying SybilGuard, SybilLimit, SybilInfer, and
SumUp — that Sybil accounts form communities where intra-Sybil edges outnumber Sybil-to-normal
edges — for the Renren deployment; the authors state this as their central finding, not as an
attributed claim to be doubted. No claim commonly attributed to this paper needs correction here.
Cross-paper: None found in this batch.

### References worth retrieving
- Douceur, "The Sybil Attack," IPTPS 2002 — foundational (defines the Sybil attack).
- Yu, Kaminsky, Gibbons, Flaxman, "SybilGuard: defending against sybil attacks via social networks," SIGCOMM 2006 — competing (one of the four community-detection defenses evaluated here).
- Yu, Gibbons, Kaminsky, Xiao, "SybilLimit: A near-optimal social network defense against sybil attacks," IEEE S&P 2008 — competing.
- Danezis, Mittal, "SybilInfer: Detecting sybil nodes using social networks," NDSS 2009 — competing.
- Tran, Min, Li, Subramanian, "Sybil-resilient online content voting," NSDI 2009 — competing (SumUp).
- Viswanath, Post, Gummadi, Mislove, "An analysis of social network-based sybil defenses," SIGCOMM 2010 — attack/critique (shows the four algorithms generalize to community detection, which this paper then tests against real data).
- Newsome, Shi, Song, Perrig, "The sybil attack in sensor networks: Analysis & defenses," IPSN 2004 — foundational (Sybil attacks outside OSNs).
- Lian, Zhang, Yang, Zhao, Dai, Li, "An empirical study of collusion behavior in the maze p2p file-sharing system," ICDCS 2007 — foundational (empirical Sybil/collusion measurement in a different deployed P2P system).
- Gao, Hu, Wilson, Li, Chen, Zhao, "Detecting and characterizing social spam campaigns," IMC 2010 — foundational (companion large-scale OSN abuse measurement, same research group).
- Grier, Thomas, Paxson, Zhang, "@spam: the underground on 140 characters or less," CCS 2010 — competing (independent large-scale OSN spam measurement, Twitter).
- Stringhini, Kruegel, Vigna, "Detecting spammers on social networks," ACSAC 2010 — competing.
- Webb, Caverlee, Pu, "Social honeypots: Making friends with a spammer near you," CEAS 2008 — competing (honeypot-based detection, contrasted directly against this paper's findings on incoming-request acceptance).

### Verbatim extracts
"Sybil accounts in Renren do not form tight-knit communities: >70% of Sybils do not have any social edges."
"only 20% of Sybils are friends with one or more other Sybils."
"All components are above the 45° line, meaning that they have more attack edges than Sybil edges."
"a threshold of 40 requests/hour can identify ≈70% of Sybils with no false positives."
"34.5% of Sybils only connect to 1 other Sybil, and 93.7% connect to ≤10."
