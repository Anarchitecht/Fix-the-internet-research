## [SRIVATSA-WWW-05] TrustGuard: Countering Vulnerabilities in Reputation Management for Decentralized Overlay Networks
**Citation:** Mudhakar Srivatsa, Li Xiong, Ling Liu. "TrustGuard: Countering Vulnerabilities in Reputation Management for Decentralized Overlay Networks." WWW, 2005. DOI 10.1145/1060745.1060808.
**Retrieved:** full text via Srivatsa's PhD thesis ("Security Architecture and Protocols for Overlay Network Services," Georgia Institute of Technology, 2007), Chapter 5, which states the TrustGuard framework in expanded form with the same three guards, the same cost model, and the same simulation setup described below. The file on disk is the thesis, not the four-page WWW 2005 conference paper; no copy of the conference paper itself was located in this pass.
**Source URL:** https://www.mathcs.emory.edu/~lxiong/pubs/trustguard-www05.pdf (conference paper, not retrieved this pass); thesis text extracted from local file sources/text/SRIVATSA-WWW-05.txt
**Domain:** F

### What it does
TrustGuard raises the effort a malicious node needs to expend to hold a favorable reputation score, by adding three guards on top of an existing transaction-based reputation system (the thesis builds its guards on top of PeerTrust). The strategic oscillation guard computes a node's trust value from three weighted components instead of a plain average: current-period feedback, a running history of past reputation, and the derivative (rate of change) of recent behavior, combined as TV_n(t) = alpha * R_n(t) + beta * (history term) + gamma * (derivative term), with alpha, beta, gamma summing to 1. Weighting recent fluctuation and history penalizes a node that behaves well only long enough to build trust and then defects. The fake-transaction guard requires two nodes to exchange an unforgeable transaction proof before either can file feedback about that transaction, so a node cannot flood feedback about transactions that never happened; proof exchange uses an optimistic fair-exchange protocol with a trusted third party invoked only on dispute, so the trusted third party need not be online for every transaction. The dishonest-feedback guard assigns each incoming feedback a credibility weight before summing it into a node's reputation-based trust value R_n; the thesis defines two credibility measures, one from the rater's own trust value (TVM) and one from a personalized similarity between the evaluator and the rater computed over the set of nodes both have rated in common (PSM, personalized similarity measure).

### Measured results
All experiments in Chapter 5 run a discrete-event simulator with N = 1024 nodes, a random p percent of them designated malicious; the specific figures below name where p differs from the default.

| Result | Conditions |
|---|---|
| Cost paid by malicious nodes under adaptive vs. non-adaptive trust models is "close to zero" for the non-adaptive model across all oscillation periods and history sizes tested | N=1024, model I oscillation, varying maxH (history size) |
| Relative cost extracted by malicious nodes for history size maxH = 5, 10, 15 stands in ratio 0.63 : 1 : 3.02 | Model I, oscillation period 10 time units, alpha=0.2, beta=0.8 (maxH=5) / alpha=0.1, beta=0.9 (maxH=15), beta1=0.05, beta2=0.2 |
| Cost extracted from malicious nodes under strategic-oscillation models I, II, III, IV stands in ratio 1 : 2.28 : 2.08 : 1.36 | N=1024, oscillation period equal to maxH (worst case for the guard) |
| Fading-memories technique records a node's behavior over its last 256 (2^8) time intervals using 8 stored values | m = 8 fading-memory levels, compared against a non-fading adaptive model with maxH = 10 under 100-time-unit oscillation |
| Relative cost paid by malicious nodes falls to 0.9, 0.85, 0.78, 0.66 (from 1.0 at T_off = 0) as the trusted third party's offline duration T_off rises to 0.05, 0.1, 0.2, 0.3 of maxH | N=1024; to hold the cost drop under 10%, T_off must stay under 5% of maxH |
| Trust computation error for the naive average and TVM (trust-value-weighted) credibility measures rises roughly linearly with the fraction of malicious nodes and is stated as "extremely sensitive" to collusion even at a small malicious fraction; PSM "remains effective even with both large fraction of malicious nodes and collusion" | N=1024, malicious fraction swept 0 to 0.8, non-collusive and collusive settings compared (Figures 101, 102) |
| Transaction success rate stays close to 100% for both TVM and PSM despite their non-zero trust-computation error, because relative ranking of nodes still separates good from bad | N=1024, 20% malicious nodes, collusive and non-collusive settings (Figure 104) |
| The trusted third party used for fair exchange of transaction proofs "does not become a performance bottleneck" | Stated only for N = 1024; the thesis states scalability to larger N is unstudied |

The thesis reports these results as plotted figures (91-104) and one table (Table 18, T_off vs. cost) rather than as a single reported number set; the ratios above are the only figures stated as numbers in the prose rather than read off a plot.

### Parameters
- N = 1024 nodes in every reported simulation.
- p = fraction of malicious nodes, varied per experiment (20% used for the fake-transaction and transaction-success-rate experiments; swept 0-0.8 for the dishonest-feedback robustness experiments).
- Trust value combination weights alpha (current feedback), beta (history), gamma (derivative/fluctuation), summing to 1; example settings used: alpha=0.7 for the optimistic/pessimistic summarization comparison; alpha=0.2, beta=0.8 and alpha=0.1, beta=0.9 for the two history-size experiments.
- History size maxH, tested at 5, 10, and 15 time units, and separately at 10 vs. fading-memories m=8 (encoding 256 time-unit history).
- beta1 = 0.05, beta2 = 0.2 (derivative-component sub-weights) used in the maxH experiments.
- T_off (trusted-third-party offline duration), swept as a fraction of maxH: 0, 0.05, 0.1, 0.2, 0.3.
- Four strategic-oscillation behavior models: regular-period oscillation (I), exponentially distributed interval oscillation (II), exponentially distributed random-level dwell (III), and continuous sinusoidal change (IV).

### Stated limitations
The thesis states the TrustGuard framework depends on a trusted third party for fair exchange of transaction proofs; that party is a potential performance bottleneck and single point of failure, and if compromised, an adversary could forge transactions system-wide. The stated "does not become a bottleneck" result covers only N=1024; the thesis states scalability of the trusted third party to larger systems as unstudied. The personalized similarity measure needs each pair of nodes being compared to have interacted with a large-enough common set of other nodes to compute a similarity value; the thesis states this can fail when relationships between nodes are sparse, and offers only a Birthday-paradox argument (at N=1024, two nodes each rating 32 random others share a common rated node with probability 1/2) as partial mitigation, plus a suggestion to combine PSM with TVM. The thesis states its scope is limited to strategic oscillation, fake transactions, and dishonest/collusive feedback; it explicitly excludes other adversarial behavioral strategies from analysis. The thesis states modeling and analysis of further shilling-attack types is left to future work.

### Requirements it places on the rest of the system
TrustGuard requires an underlying overlay network that is already secure against message misrouting and that ties every node identity to a single principal through digital certification or a secure join procedure; the thesis states this assumption explicitly and cites Douceur's Sybil attack result that a node able to spoof multiple identities amplifies its effective strength proportionally to how many identities it holds. TrustGuard requires that transactions produce an unforgeable, exchangeable proof object before feedback can be filed, so the object model beneath it must support generating and verifying such proofs. It requires the existence of at least one trusted third party reachable by both transacting nodes to arbitrate proof exchange on dispute; that party need not be continuously online, but its offline duration directly reduces the cost extracted from malicious nodes (measured above). It requires a place to persist per-node feedback history proportional to maxH (or its fading-memory encoding) reachable by whichever node computes another's trust value; the thesis builds this storage on PeerTrust. PSM credibility weighting requires an evaluator to be able to enumerate, for any two nodes, the set of other nodes both have transacted with and to retrieve each side's past feedback on that common set.

### Contradicts
None found within this batch. The TVM credibility measure's collusion vulnerability (trust-value-weighted feedback is "extremely sensitive to collusive attempts") is a claim about EigenTrust-style trust-transitivity credibility (Kamvar, Schlosser, Garcia-Molina, cited as [48] in the thesis), not a disagreement with any other paper in this corpus.

### References worth retrieving
- Kamvar, Schlosser, Garcia-Molina, "EigenRep: Reputation Management in P2P Networks" — competing (transitive-trust reputation with pre-trusted nodes, the thesis argues pre-trusted nodes are not always available)
- Douceur, "The Sybil Attack," IPTPS 2002 — foundational (identity-amplification bound the thesis assumes overlay security must defeat)
- Damiani, Vimercati, Paraboschi, Samarati, Violante, XRep (Gnutella reputation protocol) — competing
- Cornelli, Damiani, di Vimercati, Paraboschi, Samarati, P2PRep — competing (stated as having no detailed trust metric or evaluation)
- Yu, Singh, "A social mechanism of reputation management in electronic communities" — competing (gossip-protocol trust propagation, ad hoc rather than control-theory based)
- Yu, Singh, Sycara, "Developing trust in large-scale peer-to-peer systems" — competing
- Whitby, Josang, Indulska, "Filtering out unfair ratings" — competing (statistical filtering alternative to PSM/TVM)
- Richardson, Agarwal, Domingos, "Trust management for the Semantic Web" — foundational (path-algebra trust propagation)
- Guha, Kumar, Raghavan, Tomkins, "Propagation of trust and distrust" — foundational
- Lam, Riedl, "Shilling recommender systems for fun and profit" — attack (shilling-attack taxonomy TrustGuard is tested against for random shilling only)
- Xiong, Liu, "PeerTrust: Supporting reputation-based trust for peer-to-peer electronic communities" — foundational (storage layer TrustGuard is built on)
- Micali, "Simple and fast optimistic protocols for fair electronic exchange" — foundational (the fair-exchange protocol TrustGuard's fake-transaction guard uses)
- Dellarocas, "The digitization of word-of-mouth: Promises and challenges of online feedback mechanisms" — foundational

### Verbatim extracts
"we require TrustGuard to ensure that any node behaving well for an extended period of time attains a good reputation"
"the cost paid by malicious nodes using models I, II, III and IV are in the ratio of 1 : 2.28 : 2.08 : 1.36"
"the cost paid by malicious nodes for maxH equal to 5, 10 and 15 are in the ratio of 0.63 : 1 : 3.02"
"the PSM approach remains effective even with both large fraction of malicious nodes and collusion"
"the TTP does not become a performance bottleneck with 1024 nodes in the system"
"it might get hard to find sufficient number of raters towards a common target node"
