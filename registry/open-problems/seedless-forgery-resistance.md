# Forgery resistance without trusted seed identities

## Verdict: open

No published mechanism admits identities into a decentralized network and bounds the count an
adversary can forge, without relying on some party or population that the protocol itself must
trust in advance. Every mechanism retrieved for this pass substitutes one anchor for another —
a seed node, a seed committee, an issuer, a hardware manufacturer, or a platform's own ground
truth — and states that substitution as an explicit assumption, not as a solved elimination of
trust.

## Two analyses established the shared failure mode; a third confirms it by an independent route

Viswanath, Post, Gummadi, and Mislove (SIGCOMM 2010) took four published social-graph Sybil
defenses — SybilGuard, SybilLimit, SybilInfer, and SumUp — and showed each reduces to the same
operation: given one trusted node, rank every other node by proximity to it, then cut the ranking
at a threshold. The four schemes' rankings agree most strongly exactly where graph conductance
(the ratio of edges leaving a node set to edges inside it) has a local minimum — the boundary of a
locally dense cluster around the trusted node. Substituting an off-the-shelf local
community-detection algorithm for any of the four schemes' own procedures produces comparable
accuracy, which is how the reduction was demonstrated. Across eight real social graphs (514 to
446,181 nodes), detection accuracy correlates with network modularity at −0.81: the more the
honest population itself splits into distinct communities, the worse every scheme performs. On the
Facebook graduate-student graph (514 nodes), an adversary who places attack edges only among the k
nodes nearest the trusted node — rather than uniformly at random — drives detection accuracy below
0.5 as k shrinks toward zero, meaning Sybil nodes rank above honest ones. The paper states as an
open question whether the assumption every scheme needs, that Sybils can form only a bounded
number of edges into the honest region, holds in any real online social network today.

Alvisi, Clement, Epasto, Lattanzi, and Panconesi (IEEE Security and Privacy 2013) reduced
universal Sybil defense to a random-walk membership test relative to one seed, then reframed the
achievable goal from classifying every node in the network to finding one seed's local, sparsely
cut community (their Problem 1), solved by a Personalized PageRank algorithm called ACL. Under an
attack pattern observed on the Renren social network — many isolated Sybil nodes, each with a few
attack edges, rather than one dense Sybil cluster — every tested scheme performs close to random
guessing on the Facebook-New Orleans graph: SybilLimit 0.45, SybilGuard 0.44, community detection
0.34, GateKeeper 0.49, ACL 0.37, where 0.5 is the random-guessing point. The paper states plainly
that community-detection-based Sybil defense is often described as solved and that this is false
in general: an adversary using only two attack edges from one honest node to two Sybil endpoints
can force the community-detection algorithm to admit an entire attacker-built Sybil chain.

Furutani, Shibahara, Akiyama, and Aida (IEEE Transactions on Information Forensics and Security
2023) reached the same conclusion by a third, independent route: they showed five propagation-based
detectors (CIA, SybilRank, SybilWalk, SybilSCAR, SybilBelief) are each one instance of graph-signal
low-pass filtering, and that every one of them collapses once community strength falls below a
theoretical detectability threshold, regardless of which filter or which graph shift matrix is
used. The mathematical form differs from the first two analyses; the conclusion — detection
accuracy is governed by how strongly the honest and Sybil regions separate into communities, and
collapses when they do not — is the same one three independent groups reached from three different
directions.

## A measurement on a 21-million-node network shows the assumption already fails at scale

Gao, Wang, Gong, Kulkarni, Thomas, and Mittal (IEEE CNS 2018, the SybilFuse paper) measured network
modularity directly on a labeled Twitter follower graph of 21,297,772 nodes and 265,025,545 edges,
with ground truth obtained by re-crawling every account through Twitter's own suspension API. The
modularity of the benign/Sybil partition is 0.0042, and rises only to 0.0046 when restricted to the
Sybil region's largest connected component — far below the 0.3 threshold the paper cites as the
point above which a partition counts as a detectable community structure at all. Under this
measured condition, every structure-only baseline the paper tests performs near-random to modest:
SybilRank reaches Area Under the Curve (AUC, the probability a randomly chosen Sybil node ranks
above a randomly chosen benign node) 0.57, Integro 0.48 to 0.54, SybilBelief 0.74, SybilSCAR 0.74.
The paper's own hybrid method, SybilFuse, reaches AUC 0.85 by adding a locally trained classifier
signal on top of structure — but that classifier is itself trained on 3,000 labeled benign and
3,000 labeled Sybil nodes drawn from Twitter's own centralized suspension decisions, a ground-truth
source the paper states its own method sits on top of, not one it replaces. A manual audit of the
100 top-ranked accounts still active after Twitter's own moderation found 82.8% of the 29 still-active
accounts show Sybil-like characteristics anyway, meaning the platform-supplied ground truth this
detector depends on is itself imperfect.

Mohaisen, Yun, and Kim (ACM IMC 2010) independently measured why: the fast-mixing property every
random-walk-based scheme in this family assumes — that a random walk from any node reaches the
graph's overall distribution within O(log n) steps — does not hold at the walk lengths those
schemes' own evaluations used. Real graphs need walk lengths of 100 to 2,500 steps to reach a
total-variation distance of 0.1 from the stationary distribution, one to two orders of magnitude
larger than the 10-to-15-step walks SybilGuard and SybilLimit's own published evaluations used.
Forcing a graph to mix faster by removing low-degree nodes, the trimming step those evaluations
also used, removed over 85% of the WikiTalk graph's nodes before the assumption held.

## What has been published since 2023, and what each result assumes

**Graph neural network detectors.** Heeb, Plesner, and Wattenhofer (arXiv 2024, SybilGAT) replace
the fixed propagation weights of SybilRank, SybilBelief, and SybilSCAR with a Graph Attention
Network, a graph neural network layer that learns a separate weight per neighbor rather than one
global weight per edge. On a real 269,640-node Twitter graph, the four-layer variant reaches AUC
0.8489 against SybilSCAR's 0.8022. Under a targeted attack-edge placement — the same class of
attack Viswanath et al. and Alvisi et al. showed degrades every prior scheme — performance on a
pre-trained, larger evaluation graph falls to AUC 0.6021, barely above the 0.5 random-guessing
point, and the paper's own robustness sweep shows the gap over baselines widening only because the
baselines degrade faster, not because SybilGAT stays accurate. The mechanism requires a small,
already-labeled set of honest and Sybil nodes before training or inference proceeds (5% of each
region's true size by default); SybilGAT does not determine which nodes to trust as ground truth,
it consumes a trusted label set exactly as the schemes it replaces do. The authors state that
robustness against an attack targeting the attention mechanism specifically "remains to be fully
explored."

**Resource-based admission.** Gupta, Saia, and Young's resource-burning framework (SIROCCO 2020,
surveying their own prior algorithms including ERGO) bounds the fraction of Sybil identifiers at
any time to a constant α, given that the adversary's resource-spending rate stays within a bound
relative to the rate at which honest identifiers join. This substitutes a resource-parity
assumption — the honest population's aggregate spending capacity must not be swamped by the
adversary's — for a graph-connectivity assumption; it removes the social graph, but not the
requirement that some population supply a bounded, sustained resource commitment the adversary
cannot outmatch by spending more. For the specific case that matters to a decentralized network —
extending the bound to a Distributed Hash Table under permissionless churn — the paper's own
Section 4.2 states this requires a committee, "a small identifier set with a good majority," to
issue and validate the resource-burning challenges, and states outright that decentralizing that
committee is itself unresolved (their Open Problem 3). Resource burning does not eliminate the
pre-trusted anchor for this case; it relocates the anchor from a seed node in a social graph to a
seed committee coordinating admission, and the paper states that relocation as an open problem, not
a solved one.

**Proof-of-personhood constructions.** Every reviewed or retrieved construction requires an anchor
outside the protocol.

- Borge, Kokoris-Kogias, Jovanovic, Gasser, Gailly, and Ford (IEEE EuroS&PW 2017) build
  proof-of-personhood on in-person pseudonym parties under an anytrust assumption: at least one
  organizer, and at least one of that organizer's independent servers, must be honest and
  non-colluding. The paper runs no experiment; it states that preventing one person from attending
  two simultaneous parties in different regions relies on travel-time infeasibility, not on a
  cryptographic guarantee.
- Siddarth, Ivliev, Siri, and Berman (Frontiers in Blockchain 2020) reviewed seven deployed
  proof-of-personhood systems. Four of seven anchor Sybil resistance to a social graph seeded from
  trusted starting points (BrightID) or to vouching networks with a stated minimum connection
  density (Duniter, Kleros/Proof of Humanity, Humanity DAO). The paper states there is "no
  evidence of the Web of Trust schemes' effectiveness for Sybil-resistance in the presence of
  multiple attack vectors" for any of the four. It states a reverse-Turing-test approach (Idena's
  FLIP test) stops automated bots but not "human-generated attacks, in which one individual passes
  the test multiple times and creates multiple different identities" — an unresolved gap, because
  nothing in the mechanism stops a market for completing the test on another person's behalf.
- The BrightID whitepaper (2020) anchors its own Sybil-ranking algorithm to seed groups from the
  start, and states as an open question, unresolved in the document itself, who holds the
  authority to grant seed status to the first seed group with no existing parent group.
- Crites, Kiayias, Kohlweiss, and Sarencheh (ACM CCS 2025, SyRA) remove the requirement that an
  issuer retain a per-user record after issuing a credential, using a distributed verifiable random
  function so the issued key is a deterministic function of the identity string and never needs to
  be looked up again. The construction still requires an external personhood-verification input —
  a signed government certificate, a biometric reading, or an OAuth token, none of which the paper
  builds — and requires a threshold t of n issuers to act honestly (t = n/2 in the paper's own
  evaluated configurations, measured at 0.0651 to 72.6 seconds of issuance time across six
  committee sizes from 10 to 300 issuers on one MacBook Pro). The paper states explicitly that
  privacy and Sybil resistance both fail once fewer than t issuers are honest, and does not
  evaluate the personhood-check step itself.
- Ľaš, Homoliak, and Mariani (IACR ePrint 2026/1723, De-SyRIS) combine facial-biometric matching
  inside a Trusted Execution Environment (TEE, a hardware-isolated processor region meant to keep
  code and data confidential from the machine's own operating system) with zero-knowledge
  social-graph path proofs, to avoid publishing the graph itself. The paper's own discussion states
  TEE security "remains an open question" in decentralized settings and cites a 2025 hardware
  attack (Seto et al., ACM CCS 2025) that discontinued a comparable TEE-based identity project. The
  paper labels its biometric-embedding database "a centralized but encrypted repository." Its own
  100-entity simulation states that the Holme-Kim graph model needs 8% to 30% of entities holding
  externally supplied reputation, depending on trust-distribution mode, before the protocol's
  intrinsic reputation mechanism can bootstrap at all — the system cannot start from zero
  externally supplied trust. The paper states outright, as an unresolved weakness rather than a
  theoretical one, that a coalition using real, highly reputable identities as gateways can
  legitimize a large Sybil cluster, with no defense against it inside the current design.
- Vozda et al. (IACR ePrint 2026/1725, Proof-of-Uniqueness) compose an issuer-signed verifiable
  credential with a threshold verifiable oblivious pseudorandom function evaluated by n nodes with
  reconstruction threshold t, so that no single node holds the deduplication key. The paper's own
  stated assumptions are that fewer than t OPRF (Oblivious Pseudorandom Function) nodes collude and
  that canonical issuance is honest; it states directly that privacy fails against "an issuer that
  actively probes its own identifiers," and that person-level deduplication holds only under the
  assumption of honest canonical issuance by that same issuer. The construction distributes trust
  across a committee; it does not remove the requirement that an issuer and a threshold of that
  committee be trustworthy.

**A structurally identical pattern outside social graphs and biometrics.** Shi and Joo (arXiv,
October 2025) built TraceRank, a reputation-ranking algorithm for a payment-gated service
marketplace, where each payment functions as an endorsement and reputation propagates along
payment flows weighted by transaction value and time. The paper states plainly that TraceRank
"seeds addresses with precomputed reputation metrics" before propagation begins, and states
TraceRank "is agnostic to seed provenance" — the seed-selection problem is left to whatever
upstream source supplies it (trading history, a social-graph platform, labeled organizations, or
an external attestation registry), not solved by the mechanism itself. Substituting a payment
graph for a social graph reproduces the identical structure Viswanath et al. and Alvisi et al.
analyzed: a ranking computed relative to a pre-supplied trusted set, with the trust-origination
problem left outside the paper.

## The pattern across every mechanism family

Six different substrates were checked against the same question — what must already be trusted
before the mechanism runs — and every one names something.

| Mechanism family | What replaces the social-graph seed | Paper's own statement of the residual trust requirement |
|---|---|---|
| Classical social-graph ranking (SybilRank, SybilLimit, ACL) | A trusted seed node or seed set | Ranking is seed-relative; accuracy depends on the seed's placement and the honest region's community structure |
| Graph neural network detection (SybilGAT) | A labeled training set of honest and Sybil nodes | 5% of each region must already be correctly labeled before training or inference runs |
| Resource burning (DefID/ERGO family) | A resource-parity bound on the adversary, and for decentralized deployment, a coordinating committee | Decentralizing that committee is stated as an open problem, not solved |
| Pseudonym parties | At least one honest, non-colluding organizer and server | The anytrust assumption is a stated precondition the protocol does not itself enforce |
| Web-of-trust proof of personhood | A seed group or a minimum-density vouching network | No reviewed system is stated to have proven effectiveness against multiple attack vectors |
| Threshold-issuer cryptographic constructions (SyRA, Proof-of-Uniqueness) | A threshold of honest issuers or committee members, plus an external personhood check | Both privacy and Sybil resistance are stated to fail once the honest threshold is not met |
| Payment-graph reputation (TraceRank) | Seed reputation scores from an external source | The paper states it is agnostic to where those scores come from |

## Where the state of the art stops

The best published result for the specific claim — bound the count of forged identities an
adversary can register, without any party the protocol itself must trust in advance — is that no
such result exists. The strongest results move the bound within one substrate (SybilFuse's local
classifier lifts AUC from 0.57–0.74 to 0.85 on the 21-million-node graph; SybilGAT lifts AUC by up
to five points over SybilSCAR on the 269,640-node Twitter graph) while keeping the same
pre-trusted-anchor requirement every earlier scheme in that substrate needed. The threshold-issuer
constructions (SyRA, Proof-of-Uniqueness) are a genuine advance on a narrower, different claim:
they let issuers stop retaining state after issuance, closing a specific storage and
correlation risk, while both papers state directly that the underlying trust requirement — a
threshold of honest issuers, plus an external personhood check neither paper builds — is
unchanged. Resource burning is a genuine advance on a different axis still: it removes the social
graph entirely, at the cost of a resource-parity assumption on the adversary and, for a
decentralized deployment, an unresolved committee-decentralization problem the paper's own authors
list as open.

## Assumption doing the work

Every mechanism in this pass supplies its stated guarantee only because some population or party
is already assumed honest before the protocol runs: a seed node's placement, a labeled training
set, a resource-spending population the adversary cannot outmatch, an anytrust organizer, a
vouching network's density, a threshold of issuers, or an externally supplied reputation score. A
decentralized deployment, by definition, has no operator positioned to guarantee any of these in
advance — no party is in a position to hand-pick a seed node, manually label a training set, or
convene an issuer committee and vouch for its honesty. Every mechanism surveyed here answers a
different question than the one this architecture needs answered: not "how do we bound forgery
given a trusted anchor" but "how do we bound forgery with no trusted anchor to give." The former is
solved, repeatedly, in different ways. The latter has no published answer.

## What was searched

Corpus: `registry/index-measurements.md` and `registry/index-requirements.md` were read in full and
grepped for `sybil`, `forgery`, `seed`, `community detection`, `social graph`, `proof of
personhood`, `admission`, `graph neural`, `GNN`, and the individual scheme names (SybilGuard,
SybilLimit, SybilRank, SybilInfer, Whanau, Bazaar, Canal). Every matching evidence file was opened
in full: `ALVISI-SP-13`, `VISWANATH-SIGCOMM-10`, `MOHAISEN-IMC-10`, `GAO-CNS-18`, `FURUTANI-TIFS-23`,
`HEEB-ARXIV-24`, `CRITES-CCS-25`, `LAS-EPRINT-26`, `FORD-EUROSPW-17`, `SIDDARTH-FRONTIERS-20`,
`BRIGHTID-WP`, `CAO-NSDI-12`, `GUPTA-SIROCCO-20`, `SAFARPOOR-DEHKORDI-ARXIV-25`, and
`SAFARPOOR-DEHKORDI-AAMAS-25`.

Beyond the corpus: DBLP's publication-search API for `sybil detection without seed` and `sybil
resistance trusted seed` returned zero hits. Web searches covered `sybil defense without
pre-trusted seed set 2025`, `proof of personhood survey 2025 systematization of knowledge`,
`Worldcoin World ID sybil resistance attack analysis 2024 2025`, `Bankrupting Sybil churn
resource-based admission`, `graph neural network sybil detection without labeled seeds
unsupervised 2024 2025`, `arxiv 2025 2026 sybil resistance decentralized identity no trusted issuer
seedless`, and `sybil resistance decentralized 2026 no pre-trusted seed set survey`. Two candidates
that looked like they might solve the problem — `Proof-of-Uniqueness: Sybil-Resistant
Privacy-Preserving Decentralized Identity through Threshold-OPRF and zk-SNARK Registry` (IACR
ePrint 2026/1725, Vozda et al.) and `Sybil-Resistant Service Discovery for Agent Economies` (Shi
and Joo, arXiv 2510.27554, October 2025) — were retrieved in full text with
`tools/fetch-paper.py` (47,139 and 10,737 characters respectively) rather than judged from their
abstracts; both state the residual trust requirement directly in their own text, quoted above. The
most recent directly relevant full-text retrieval is Ľaš, Homoliak, and Mariani's De-SyRIS, IACR
ePrint 2026/1723. A third 2026 candidate, `Human Challenge Oracle: Designing AI-Resistant,
Identity-Bound, Time-Limited Tasks for Sybil-Resistant Consensus` (arXiv 2601.03923), was found but
only its abstract was reachable in this pass; it addresses a different problem (rate-limiting how
many identities one already-admitted party can sustain over time) rather than bounding forgery at
admission, and is recorded here as unretrieved — no measurement from it is used above.
