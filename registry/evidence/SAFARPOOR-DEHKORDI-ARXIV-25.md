## [SAFARPOOR-DEHKORDI-ARXIV-25] Graph-Based Fake Account Detection: A Survey
**Citation:** Ali Safarpoor Dehkordi, Ahad N. Zehmakan. "Graph-Based Fake Account Detection: A Survey." arXiv preprint, 2025. DOI 10.48550/arXiv.2507.06541.
**Retrieved:** full text via https://arxiv.org/pdf/2507.06541
**Source URL:** https://arxiv.org/abs/2507.06541
**Domain:** F

### What it does
The paper classifies published methods for fake-account detection (FAD) in online social networks (OSNs) by the graph mechanism each method uses to separate real accounts from fake accounts. It groups methods into three families: classical graph algorithms (random walk and loopy belief propagation), traditional machine-learning methods on hand-built graph features, and graph neural network (GNN) methods, and further subdivides the GNN family by how each method handles heterophilic edges (edges joining nodes of different classes), multiple edge or node types, added content features, contrastive training, reinforcement learning, temporal dynamics, mixture-of-experts routing, federated training, and adversarial robustness.

Every method the survey covers relies on one of two structural assumptions stated formally. The homophily assumption states that real accounts predominantly connect to other real accounts while fake accounts are pushed into connecting mostly with each other, because their attempts to connect to real accounts are frequently rejected. The small-cut assumption states the number of edges directly joining the real region to the fake region (attack edges) is small relative to the two regions' internal edge counts. The survey treats these as the same underlying claim — a structural separation between real and fake regions — and states both formally as a homophily ratio, the fraction of edges connecting same-label node pairs.

The classical random-walk family (SybilGuard, SybilLimit, SybilRank, SybilInfer, SybilDefender, SybilWalk) runs traces (random walks) from known real accounts and either classifies a node by whether traces starting from it stay trapped in a small region, or ranks nodes by the frequency with which real-seeded traces land on them. The belief-propagation family (SybilBelief, SybilFrame, SybilSCAR, SybilHP) represents the graph as a Markov random field and propagates a posterior probability of being fake between neighboring nodes over multiple iterations until the probabilities stabilize.

### Measured results
This is a survey; it runs no experiments of its own. The only numeric results it states are descriptive statistics of the benchmark datasets the surveyed methods use, reproduced here as a measured property of the field's evaluation data rather than of any single detection method.

| Dataset | Nodes | Fake accounts | Real accounts | Edges | Text features |
|---|---|---|---|---|---|
| Cresci-15 | 5,301 | 3,351 | 1,950 | 7,086,134 | yes |
| TwiBot-20 | 229,580 | 6,589 | 5,237 | 33,716,171 | yes |
| TwiBot-22 | 1,000,000 | 139,943 | 860,057 | 170,185,937 | yes |
| MGTAB | 10,199 | 2,748 | 7,451 | 1,700,108 | numerical vector encoding |
| MGTAB-large | 410,199 | 2,748 | 7,451 | 97,997,710 | numerical vector encoding |

Cresci-15's human accounts were collected from volunteers who passed CAPTCHA verification plus a manually labeled political dataset; its fake accounts were obtained from three online markets. TwiBot-20's labels came from five active Twitter accounts annotating each node by consensus (at least four of five agreeing), with unresolved cases reviewed manually or discarded.

The survey cites one independent empirical finding against the homophily assumption: Yang et al.'s large-scale study of fake accounts on Renren (a Chinese OSN) found fake accounts embedded within real communities rather than isolated, meaning coordinated fake-account behavior can follow patterns not captured by structural separation between a real region and a fake region.

### Parameters
Not applicable in the sense of a single mechanism's tuned constants — the survey reports the parameter choices of surveyed methods individually (e.g., trace-length choices for SybilLimit versus SybilGuard, iteration counts for belief propagation) rather than a single set of its own. No survey-level parameter is stated.

### Stated limitations
The authors identify the following gaps as unresolved in the field, stated as future-work directions: benchmark datasets are drawn almost entirely from Twitter and expanding to other platforms with different structures is unaddressed; labels are binary (fake/real) though finer categories (spammer, robot, data collector) would better capture the diversity of fake-account behavior; heterophilic edges (edges joining accounts of different classes) cause feature mixing during message passing in graph neural networks and no principled causal method for identifying which edges are heterophilic yet exists for the fake-account detection setting specifically; few-shot and zero-shot learning, well explored for general node classification, have not been adapted to fake-account detection; cold-start nodes (newly joined accounts with few connections) remain difficult to classify with existing graph-based methods, and this maps directly onto early detection since fake accounts are typically poorly connected when created; explainability for deep-learning-based detectors is largely unaddressed, limiting deployment in settings requiring accountable decisions; and adversarial-attack research specific to fake-account detection is limited to a small number of studies, so realistic attack strategies for benchmarking detector robustness remain underdeveloped.

Synthesized datasets used to evaluate many methods do not fully capture the complexity of real-world fake-account behavior, per the survey's own statement in the datasets section, though they permit controlled, repeatable experiments that real data cannot.

### Requirements it places on the rest of the system
Any detection method the survey covers requires that the deployer already possess a social graph with edges between accounts (following, friending, or message relationships) — none of the surveyed graph-based methods can classify an isolated account with no observed edges. Random-walk and belief-propagation methods additionally require a seed set of accounts already labeled real (and, for some variants such as SybilBelief and SybilWalk, also a seed set already labeled fake) from which traces or propagated beliefs originate; the survey does not describe a graph-based method in this family that operates with zero labeled seeds. Methods relying on the homophily or small-cut assumption require that the deployment's actual attack pattern keeps attack edges (edges directly joining fake accounts to real accounts) a small fraction of total edges; the Yang et al. Renren finding cited by the survey establishes that this requirement is not guaranteed to hold and its failure degrades detection built on that assumption.

### Contradicts
None found within this corpus. The survey itself records that the homophily assumption, on which the majority of methods it covers depend, is contradicted by field data from at least one deployed platform (Renren, per Yang et al., cited as reference [30] in the source bibliography).

### References worth retrieving
- foundational: H. Yu, M. Kaminsky, P. B. Gibbons, A. Flaxman, "SybilGuard: Defending Against Sybil Attacks via Social Networks" [ref 46 in source]
- foundational: L. Page, S. Brin, R. Motwani, T. Winograd, "The PageRank Citation Ranking: Bringing Order to the Web" [ref 48]
- competing: H. Yu, P. B. Gibbons, M. Kaminsky, F. Xiao, "SybilLimit: A Near-Optimal Social Network Defense against Sybil Attacks" [ref 50] — already in this corpus as YU-SP-08
- competing: Q. Cao, M. Sirivianos, X. Yang, T. Pregueiro, "Aiding the Detection of Fake Accounts in Large Scale Social Networks" (SybilRank) [ref 49]
- competing: G. Danezis, P. Mittal, "SybilInfer: Detecting Sybil Nodes Using Social Networks" [ref 51]
- competing: W. Wei, F. Xu, C. C. Tan, Q. Li, "SybilDefender: Defend against Sybil Attacks in Large Social Networks" [ref 52]
- competing: J. Jia, B. Wang, N. Z. Gong, "Random Walk Based Fake Account Detection in Online Social Networks" (SybilWalk) [ref 44]
- competing: N. Z. Gong, M. Frank, P. Mittal, "SybilBelief: A Semi-Supervised Learning Approach for Structure-Based Sybil Detection" [ref 45]
- competing: B. Wang, L. Zhang, N. Z. Gong, "SybilSCAR: Sybil Detection in Online Social Networks via Local Rule Based Propagation" [ref 12]
- competing: Y. Boshmaf, D. Logothetis, G. Siganos, J. Lería, J. Lorenzo, M. Ripeanu, K. Beznosov, "Íntegro: Leveraging Victim Prediction for Robust Fake Account Detection in OSNs" [ref 19] — already in this corpus as BOSHMAF-NDSS-15
- foundational: L. Alvisi, A. Clement, A. Epasto, S. Lattanzi, A. Panconesi, "SoK: The Evolution of Sybil Defense via Social Networks" [ref 53]
- attack: L. Wang, X. Qiao, Y. Xie, W. Nie, Y. Zhang, A. Liu, "My Brother Helps Me: Node Injection Based Adversarial Attack" [ref 16]
- attack: Z. Yang, C. Wilson, X. Wang, T. Gao, B. Y. Zhao, Y. Dai, "Uncovering Social Network Sybils in the Wild" [ref 30]

### Verbatim extracts
"a structural separation exists between real and fake accounts" — statement of the homophily/small-cut assumption's common form.
"fake accounts are often embedded within real communities rather than isolated" — the Renren counter-finding attributed to Yang et al.
"Although these two methods were originally designed for P2P networks and were not directly applicable to OSNs" — on SybilGuard and SybilLimit's original domain.
"our understanding of adequate adversarial attacks remains limited, and further research is needed" — stated limitation on adversarial-attack research for fake-account detection.
