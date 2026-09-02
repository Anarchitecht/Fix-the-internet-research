## [PIOTROWSKA-WPES-21] Studying the Anonymity Trilemma with a Discrete-event Mix Network Simulator
**Citation:** Ania M. Piotrowska. "Studying the Anonymity Trilemma with a Discrete-event Mix Network Simulator." WPES '21 (Workshop on Privacy in the Electronic Society), co-located with ACM CCS, 2021. DOI 10.1145/3463676.3485614.
**Retrieved:** full text via https://arxiv.org/abs/2107.12172 (arXiv:2107.12172v2)
**Source URL:** https://arxiv.org/abs/2107.12172
**Domain:** G

### What it does
The simulator lets an operator compare the anonymity, latency, and bandwidth overhead that different mix-network design choices produce, without deploying each design. It is a discrete-event simulator written in Python using the Simpy process-based framework, configurable across four network topologies (cascade, multi-cascade, stratified, and peer-to-peer (P2P)), two mixing techniques (batch-and-reorder, and Poisson mixing — a variant of continuous-time mixing where each mix delays a packet by an interval drawn from an exponential distribution before forwarding it), adjustable client and mix cover-traffic generation and rate, and adjustable packet and message sizes with fragmentation. Client sending behavior is modeled as a Poisson process. The simulator computes two anonymity metrics: a Shannon-entropy metric over the probability distribution linking an outgoing packet to past incoming packets at a mix (from Serjantov and Danezis, 2002), and a sender-receiver third-party unlinkability metric from the Loopix paper, which measures the expected log-likelihood difference an adversary gains distinguishing which of two senders sent an observed packet, and extends it across multiple observation rounds using an average-case leakage estimate via the Law of Large Numbers rather than the worst-case differential-privacy composition theorem. The paper uses the simulator to reproduce and directly compare three deployed mix-network designs: Elixxir (xx network), which implements the cMix protocol using batch-and-reorder mixing over a cascade topology, with a precomputation phase that performs public-key operations before the real-time processing phase, at the cost of a precomputation time that grows linearly with anonymity-set size and must be repeated before each real-time phase; HOPR, a peer-to-peer network in which each node holds incoming packets in a single queue and forwards one packet chosen uniformly at random per step, using Sphinx packet encapsulation; and Nym, which implements the Loopix design directly, grouping mixes into a three-layer stratified topology with Poisson mixing and Sphinx packets.

### Measured results
| Result | Value | Conditions |
|---|---|---|
| Anonymity (entropy) and latency vs. user count, single-cascade Elixxir | anonymity stays low and roughly constant as users scale from 10^2 to 10^5; latency rises sharply with user count (log-scale axis, 10^1 to 10^5 seconds) | Elixxir batch size 1000 packets; simulated on AWS EC2; single cascade topology |
| Anonymity and latency vs. user count, multi-cascade Elixxir | anonymity remains constant (fixed to batch size) regardless of user count; latency lower than the single-cascade case but still the highest of the three systems compared | same Elixxir batch-and-reorder configuration, multiple parallel cascades added once existing cascades reach full capacity |
| Anonymity and latency vs. user count, HOPR (P2P) | anonymity stays very low even as users scale from 10^2 to 10^5, because traffic is spread thinly across the P2P mesh; latency scales well (bounded, roughly 0 to 10 seconds) | HOPR P2P topology, per-node processing capacity assumed 1000 packets/second, random-uniform packet selection from each node's queue |
| Anonymity and latency vs. user count, Nym (stratified) | anonymity rises with user count (up to entropy ~17.5-20 at the higher end of 10^2-10^5 users); latency stays bounded (0-10 seconds), governed by the mean of the per-hop exponential delay | Nym stratified topology, 3 layers, Poisson mixing, per-node capacity 1000 packets/second, mean per-hop delay parameter 0.1 second unless stated otherwise, each end user sends on average 1 packet/second (Poisson), all packets routed via 3 mix nodes |
| Cover traffic needed for target anonymity, HOPR | to sustain increasing anonymity as user count grows, HOPR requires cover-to-real traffic ratios up to 10:1; even at 10:1 anonymity plotted stays below the levels Nym reaches with far less cover traffic | HOPR P2P topology, ratios of 1:1, 5:1, 10:1 cover:real traffic tested against user counts 10^2 to 10^5 |
| Cover traffic needed for fixed target anonymity of entropy 10, Nym | required cover packets per user falls from a high value toward roughly 0 as user count rises from 10^2 to 10^5 | Nym stratified topology, target fixed anonymity level of 10 in entropy, cover traffic assumed generated at the mixes rather than by clients |
| Required per-hop mixing delay vs. user count, Nym | the average delay per mix node needed to sustain rising anonymity (entropy climbing to 17.5-20) falls from roughly 100 seconds toward 0.01 seconds as user count rises from 10 to 100,000 | Nym stratified topology, 3 layers, same per-node capacity and per-user sending-rate assumptions as above |

Cryptographic-processing time for onion encryption is explicitly excluded from all reported latency figures; the paper states this exclusion is because that time depends on the specific onion-encryption implementation and code optimization, not on the mixing design being compared.

### Parameters
| Parameter | Value used | Range tested |
|---|---|---|
| Per-node processing capacity (HOPR, Nym) | 1000 packets/second | fixed across experiments, held equal between HOPR and Nym for comparability |
| Elixxir batch size | 1000 packets | fixed |
| Mean of per-hop exponential delay (HOPR, Nym) | 0.1 second per node | varied down to roughly 0.01 s in the Figure 5 delay-vs-anonymity experiment |
| Per-user sending rate | 1 packet/second (Poisson process) | fixed unless stated otherwise |
| Number of mix hops per path | 3 | fixed |
| Nym stratified topology layer count | 3, matching Nym's live open-source code base at time of writing | fixed |
| User count (x-axis of every figure) | -- | 10^2 to 10^5 (Figures 1-4); 10 to 10^5 (Figure 5) |
| Cover-traffic ratios tested (HOPR) | -- | real-traffic-only, 1:1, 5:1, 10:1 cover:real |
| Target fixed anonymity level for cover-traffic sizing (Nym) | entropy of 10 | fixed target |

### Stated limitations
The paper states no separate limitations or future-work section; it is a 6-page workshop paper. Within the results, it is explicit that its fairness assumptions (equal per-node processing capacity for HOPR and Nym, exclusion of cryptographic-processing latency, a single Loopix-style mean delay parameter applied to both HOPR and Nym even though HOPR's whitepaper describes an intended Chaumian design its current code base does not yet implement) are simplifications chosen to make the three systems comparable, not measurements of each system's own deployed default configuration. The paper notes explicitly that it is not yet clear which mixing technique HOPR will ultimately use, since the live HOPR code base at the time (single random-uniform-selection queue) differs from the batching design described in HOPR's own whitepaper.

### Requirements it places on the rest of the system
Reproducing the Nym-favorable results requires a stratified topology with intersecting routes across layers, so that independent paths still contribute to one shared anonymity set — a P2P topology (as in HOPR) or a cascade topology (as in Elixxir) does not produce this property in the simulator. Sustaining Nym's entropy growth with user count as cover-traffic volume falls requires that cover traffic can be generated by the mix nodes rather than solely by clients; the paper states this delegation as a property distinguishing Nym from HOPR, where end users alone carry the burden of generating cover traffic. The comparison assumes uniform, honest per-node processing capacity (1000 packets/second) across all mix nodes in a design; the simulator does not model heterogeneous or adversarially throttled node capacity. The anonymity-set intersection property Nym relies on for its entropy-vs.-user-count result requires the same Poisson-mixing, memoryless-delay mechanism the underlying Loopix paper analyzes (cited in this batch as PIOTROWSKA-USENIXSEC-17): the paper states explicitly that the exponential distribution's memoryless property is why a single mix leaks the same information under Poisson mixing regardless of whether HOPR's or Nym's mixing technique nominally differs.

### Contradicts
None found within this batch. The paper corroborates, rather than contradicts, PIOTROWSKA-USENIXSEC-17's use of Shannon entropy and the sender-receiver third-party unlinkability metric — it reuses both definitions directly from that paper, citing it as reference [44].

### References worth retrieving
- Foundational: A. Serjantov, G. Danezis, "Towards an Information Theoretic Metric for Anonymity," PET 2002 (cited as [48]; the entropy metric this paper reuses).
- Foundational: A. M. Piotrowska, J. Hayes, T. Elahi, S. Meiser, G. Danezis, "The Loopix Anonymity System," USENIX Security 2017 (cited as [44]; also PIOTROWSKA-USENIXSEC-17 in this batch — Nym's underlying design and the unlinkability metric's source).
- Competing: N. Tyagi, Y. Gilad, D. Leung, M. Zaharia, N. Zeldovich, "Stadium: A Distributed Metadata-Private Messaging System," SOSP 2017 (cited as [52]; also TYAGI-SOSP-17 in this batch).
- Competing: J. Van den Hooff, D. Lazar, M. Zaharia, N. Zeldovich, "Vuvuzela: scalable private messaging resistant to traffic analysis," SOSP 2015 (cited as [53]).
- Competing: xx network whitepaper (cited as [3]; primary source for Elixxir/cMix's own claimed design, distinct from this paper's simulated reconstruction of it).
- Competing: Robert Kiel, Sebastian Burgel, "HOPR - a Decentralized and Metadata-Private Messaging Protocol with Incentives," HOPR whitepaper, 2019 (cited as [47]; the paper notes the live HOPR implementation differs from this whitepaper's description).
- Attack/critique: A. Panchenko, L. Niessen, A. Zinnen, T. Engel, "Website fingerprinting in onion routing based anonymization networks," WPES 2011 (cited as [41]).
- Attack/critique: S. Siby, M. Juárez, C. Díaz, N. Vallina-Rodriguez, C. Troncoso, "Encrypted DNS -> Privacy? A Traffic Analysis Perspective," NDSS 2020 (cited as [49]).

### Verbatim extracts
- "Anonymity loves company, hence scalability is one of the key properties of any anonymous communication network."
- "the anonymity provided by Nym increases as the network grows"
- "P2P networks like HOPR need huge volumes of cover traffic to reach reasonable levels of anonymity"
- "in Nym this responsibility can be delegated to the mixes"
- "It is not yet clear which mixing technique HOPR peers will use"
- "we exclude from our analysis ... the time needed for the cryptographic processing of the packets"
