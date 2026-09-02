# Forgery family: conflicts and disagreements

Scope: accepted forged identities per attack edge, detection accuracy and area
under the curve (AUC), the graph properties a defense assumes (mixing time,
modularity, attack-edge count), proof-of-personhood issuance rates, and
reputation-metric convergence. Entries covered: `ALVISI-SP-13`, `CAO-NSDI-12`,
`GAO-CNS-18`, `MOHAISEN-IMC-10`, `VISWANATH-SIGCOMM-10`, `VISWANATH-EUROSYS-12`,
`DANEZIS-NDSS-09`, `YU-SIGCOMM-06`, `YU-SP-08`, `WEI-INFOCOM-12`,
`BOSHMAF-NDSS-15`, `GONG-TIFS-14`, `HEEB-ARXIV-24`, `SUN-ASONAM-20`,
`GYONGYI-VLDB-04`, `KAMVAR-WWW-03`, `LESNIEWSKI-LAAS-NSDI-10`,
`LESNIEWSKI-LAAS-SNS-08`, `MISLOVE-NSDI-08`, `TRAN-NSDI-09`,
`WORLDCOIN-WP`, `IDENA-WP`, `SIDDARTH-FRONTIERS-20`, `FORD-EUROSPW-17`,
`CRITES-CCS-25`, `BRIGHTID-WP`.

## 1. A real 21-million-node graph destroys the fast-mixing and bounded-attack-edge
   precondition four defenses share

`CAO-NSDI-12` (SybilRank) states its own requirement directly: the non-Sybil
region of the graph must be "well-connected, non-bipartite, and fast-mixing
relative to the full graph including Sybils," and Sybils must be "limited in
the number of attack edges they can form into the non-Sybil region."
`YU-SIGCOMM-06` (SybilGuard), `YU-SP-08` (SybilLimit), and `DANEZIS-NDSS-09`
(SybilInfer) state the same fast-mixing precondition, each fixing a
random-walk length derived from an assumed mixing time of Theta(log n).

`GAO-CNS-18` measures this precondition directly on a real 21,297,772-node,
265,025,545-edge Twitter graph (from Kwak et al.'s WWW 2010 crawl, ground
truth from Twitter's own account-suspension records). The benign/Sybil
partition has modularity 0.0042 — Clauset et al.'s cited threshold for
detectable community structure is 0.3, so this graph carries no detectable
separation between the two regions by that standard. The 18,414,469 measured
attack edges are not the assumed handful: 90% of them concentrate on 3% of
benign nodes, hypothesized to be celebrity accounts that follow back
indiscriminately, and 50% of Sybil nodes connect through a single isolated
attack edge each rather than clustering. Under these measured conditions,
SybilRank (SR) reaches an AUC of 0.57 — barely above the 0.5 random baseline —
and SybilInfer's analogue in the same table (SB, SybilBelief) reaches 0.74.

`ALVISI-SP-13` reaches a convergent, independently obtained result on a
different real graph: under the "RenRen-observed attack pattern" (many
isolated Sybil nodes, each with a handful of attack edges, rather than one
well-connected Sybil cluster) measured on the Facebook-New Orleans graph, every
tested defense performs close to random — SybilLimit 0.45, SybilGuard 0.44,
Mislove's community detection 0.34, GateKeeper 0.49, ACL 0.37 (probability a
random honest node ranks above a random Sybil node; 0.5 is random). This is
the same failure mode `GAO-CNS-18` measures at far larger scale (50% of Sybils
isolated, 90% of attack edges on 3% of benign nodes) — the two results
corroborate each other rather than conflicting, because they measure the same
underlying condition (attack edges scattered across many isolated points
rather than concentrated on a sparse cut) on two different real deployments.

`VISWANATH-SIGCOMM-10` supplies the general form of the same finding: across 8
real datasets with modularity ranging 0.278 to 0.79, it measures a -0.81
correlation between modularity and detection accuracy (A'), and shows accuracy
falling toward and below 0.5 as an adversary targets attack edges near the
trust seed rather than placing them at random. `GAO-CNS-18`'s 0.0042-modularity
graph sits far below the low end of that measured range — an extreme point
consistent with, not contradicting, `VISWANATH-SIGCOMM-10`'s trend.

**Resolution for a design selecting one of these mechanisms:** verify the
deployment graph's modularity and attack-edge distribution before relying on
any bound conditioned on fast mixing or bounded attack edges — an open,
follow-based social graph (Twitter-shaped) measures far outside the regime
these four defenses' own evaluations tested, while a closed, invitation-gated
graph (Tuenti-shaped, `CAO-NSDI-12`'s own deployment) measures much closer to
it.

## 2. `MOHAISEN-IMC-10` measures mixing times one to two orders of magnitude
   longer than the walk lengths five defenses' own evaluations used

`YU-SIGCOMM-06`, `YU-SP-08`, `DANEZIS-NDSS-09`, `LESNIEWSKI-LAAS-NSDI-10`
(Whanau), and `LESNIEWSKI-LAAS-SNS-08` (Sybil-proof one-hop DHT) each fix a
random-walk length of 10 to 20 hops, justified by an assumed mixing time of
Theta(log n) that none of the five independently measures on a real graph.

`MOHAISEN-IMC-10` measures mixing time directly — the walk length needed to
reach total variation distance 0.1 from the graph's stationary distribution —
on DBLP, Facebook, YouTube, LiveJournal, Wiki-vote, Slashdot, Enron, and three
physics co-authorship graphs. The result: 100-400 hops for DBLP, YouTube, and
Facebook, and 1,500-2,500 hops for LiveJournal — one to two orders of
magnitude longer than the 10-15-hop walk lengths `YU-SIGCOMM-06` and
`YU-SP-08`'s own published evaluations used. `MOHAISEN-IMC-10` re-implements
SybilLimit itself and finds the walk length needed to admit nearly all honest
nodes is "larger, and the resulting variation-distance quality worse," than
SybilLimit's own published walk lengths of 10 or 15. It states `LESNIEWSKI-LAAS-NSDI-10`'s
own attempted mixing-time validation is "only circumstantial." `VISWANATH-EUROSYS-12`
cites the same finding independently when explaining why Sybil-tolerance
schemes (Ostra, SumUp, Bazaar) that Canal accelerates share this contested
premise with Sybil-detection schemes.

**Destroyed precondition, stated formally:** `YU-SIGCOMM-06`, `YU-SP-08`,
`DANEZIS-NDSS-09`, `LESNIEWSKI-LAAS-NSDI-10`, and `LESNIEWSKI-LAAS-SNS-08` each
require a random-walk length derived from the honest region's true mixing
time, assumed short (O(log n), instantiated as 10-20 hops); `MOHAISEN-IMC-10`
measures that assumption false on the real graphs these designs target,
finding required walk lengths of 100-2,500 hops. A design that adopts one of
the five mechanisms must either measure its own deployment graph's mixing
time and pay the resulting larger walk length in bandwidth and latency, or
select a mechanism (§1's `GAO-CNS-18`-style local-classifier hybrid, or the
graph-attention approach in `HEEB-ARXIV-24`, §5) that is not conditioned on
fast mixing.

## 3. `WEI-INFOCOM-12`'s own survey measures the bounded-attack-edge precondition
   false on Facebook, destroying a requirement `SUN-ASONAM-20` states directly

`SUN-ASONAM-20` (TrustGCN) states its own requirement: "the real-user subgraph
[must be] fast-mixing internally and expose a comparatively sparse or negative
cut toward the Sybil region," because TrustGCN's random walk assumes Sybils
accumulate a higher rejected-to-accepted friend-request ratio than real users.

`WEI-INFOCOM-12` (SybilDefender) surveyed 214 respondents on Amazon Mechanical
Turk rating their own Facebook friend lists as "Friend" or "Stranger," and
measures an average 19.8% of rated relations as "Stranger" — a self-reported
population of accepted but non-genuine connections. It separately cites an
independent finding (Bilge et al.) that roughly 20% of bogus friend requests
on Facebook are accepted. Both figures measure a real acceptance rate of
low-value or bogus connections far above what a bounded-attack-edge, sparse-cut
assumption tolerates; `WEI-INFOCOM-12` states this survey as evidence against
its own algorithm's core assumption, not only against TrustGCN's.

## 4. Independent re-measurement of the same mechanism, on the same operator's
   platform, 2.5 years apart: SybilRank precision on Tuenti

`CAO-NSDI-12` reports SybilRank deployed on the Tuenti social graph, snapshot
August 2011 (11,291,486 nodes): of the lowest-ranked 2,000 accounts inspected,
100% were confirmed fake; across the lowest-ranked 200,000 accounts, roughly
90% were confirmed fake, falling abruptly above that mark.

`BOSHMAF-NDSS-15` reports SybilRank's precision on the same platform, Tuenti
snapshot 6 February 2014: "SybilRank precision, [lowest-ranked 20K accounts]"
is 43%, against Íntegro's 95% on the identical interval.

Both figures describe the same mechanism (SybilRank) evaluated by different
authors on the same operator's graph, 2.5 years apart, at rank cutoffs (2,000
and 200,000 versus 20,000) that fall inside the same interval `CAO-NSDI-12`
itself reports as consistently high-precision. Neither paper's retrieved text
reconciles the gap. `CAO-NSDI-12` states its own limitation that "a fake
account that succeeds in befriending many real users accumulates trust and is
ranked as non-Sybil" — a plausible mechanism for degradation as an adversary
population adapts over 2.5 years, but this is inference, not something either
paper states about the other's figure. This is recorded as an open,
unreconciled disagreement about the same mechanism's real-world precision, not
resolved as either a genuine contradiction or a fully-explained difference in
conditions.

## 5. Íntegro's uniform-random-attack-edge assumption, and its Tuenti precision
   figure, against an independent re-measurement on a real Twitter graph

`BOSHMAF-NDSS-15` proves Íntegro's security bound (Theorem 4.1) "assumes the
real region is fast-mixing and the attacker establishes attack edges uniformly
at random," and reports 95% production precision at Tuenti (lowest-ranked
20K), victim-classifier AUC 0.70 (Facebook) to 0.76 (Tuenti), and ranking AUC
above 0.92 under simulated targeted-victim infiltration on a small
(9,204-node) Facebook-derived graph.

`GAO-CNS-18` independently re-implements Íntegro (labeled INT) and measures it
on the real 21-million-node Twitter graph described in §1, where 90% of attack
edges concentrate on 3% of benign nodes — a heavily non-uniform distribution,
not the uniform-random placement Íntegro's proof assumes — and where 75.4% of
all benign nodes are "victims" (directly connected to a Sybil). Under these
measured conditions, INT scores 0.48 AUC, and INT-PF (a hypothetical *perfect*
victim predictor substituted for the trained classifier) scores only 0.54 —
"just slightly better than random guessing" — because, per `GAO-CNS-18`'s own
analysis, Íntegro's edge-downweighting formula suppresses trust propagation
broadly once the true victim fraction is this high, regardless of how accurate
the victim classifier is.

**Destroyed precondition:** Íntegro's proved guarantee requires attack edges
placed uniformly at random against a fast-mixing region (`BOSHMAF-NDSS-15`);
`GAO-CNS-18` measures a real graph where 90% of attack edges concentrate on 3%
of nodes, and independently measures Íntegro's own algorithm failing on that
graph. A design selecting Íntegro for an open-follow social graph should not
carry forward the 95% Tuenti precision figure without also carrying forward
the near-random AUC `GAO-CNS-18` measures under a more concentrated,
Twitter-like attack-edge distribution — the closer analogue to a permissionless,
open-follow decentralized social graph.

## 6. SybilLimit re-measured: a much sparser attack regime than its own
   evaluation, in a different metric, still degrading sharply

`YU-SP-08` (SybilLimit's own paper) measures roughly 10 accepted Sybils per
attack edge on Friendster, LiveJournal, and a synthetic Kleinberg graph (up to
~20 on DBLP), holding across attack-edge counts from a few thousand up to
15,000-100,000 depending on graph size.

`WEI-INFOCOM-12` independently re-implements SybilLimit (parameters taken from
SybilLimit's own paper: w=20, r=10,000) and measures it on Facebook
(3,097,165 nodes) at a much sparser g=1,000 attack edges, reporting false
negative rates of 61.3% (10 sybils/attack edge, but see below) rising to
85.3% at the hardest tested point (1 sybil/attack edge, ER Sybil-region
model). The two papers report different metrics (accepted Sybils per attack
edge versus false-negative rate) on different graphs at different attack-edge
counts, so this is not a same-quantity numeric conflict; it is flagged because
`WEI-INFOCOM-12`'s own text already calls this "exactly the kind of
re-measurement disagreement this corpus is built to preserve," and because the
direction of the gap is consistent with §2's finding that SybilLimit's
published walk-length choice understates real mixing time.

## 7. SybilSCAR AUC on two samples drawn from the same underlying Twitter crawl

`GAO-CNS-18` measures SybilSCAR (SS) at AUC 0.74 on the full 21,297,772-node
Twitter graph built from Kwak et al.'s WWW 2010 crawl, with ground truth from
Twitter's own suspension records.

`HEEB-ARXIV-24` measures SybilSCAR at AUC 0.8022 on a 269,640-node subgraph
processed from the same underlying Kwak et al. 2010 crawl (via Lu et al.
2023's processing pipeline). Neither entry's retrieved text specifies how Lu
et al.'s ground-truth labels were derived or how the 269,640-node sample was
selected from the full crawl, so the gap cannot be attributed with confidence
to sample size, sampling method, or label methodology — it is recorded as an
unreconciled difference in conditions rather than a same-quantity conflict,
because the two papers measure different derived samples of the same base
crawl, not the same graph.

## 8. No cross-paper conflict found for proof-of-personhood issuance rates or
   reputation-metric convergence

The brief's family description calls out proof-of-personhood issuance rates
and reputation-metric convergence as figure types to check. `WORLDCOIN-WP`
reports false-match-rate figures (design target 1e-12, pre-launch test
2.25e-14, stated real-world operation ~1e-12) that are exclusively
self-reported by the issuing organization, with no independent measurement
anywhere else in this corpus to compare against — its own entry already flags
this as unverifiable, not merely unverified. `IDENA-WP`'s validation-session
cadence and `SIDDARTH-FRONTIERS-20`'s 2020 snapshot of per-project user counts
(Idena 4,012; Duniter 2,801; BrightID 556; Equality Protocol 529; Humanity DAO
peak 640) are likewise self-reported adoption figures from a single source
each, not measurements any second paper in this corpus repeats or disputes.
`KAMVAR-WWW-03` (EigenTrust) reports convergence in "fewer than 10 iterations"
on a 1,000-peer simulated network; no other entry in this corpus re-measures
EigenTrust's convergence rate. This is an honest empty result for these two
sub-topics specifically — the absence of a second measurement is itself the
finding, not evidence the figures are correct.

One structural point is worth recording, not as a contradiction but as
context for a synthesis: `CAO-NSDI-12` states directly why SybilRank
terminates its power iteration *before* convergence (a deliberate departure
from EigenTrust's design, which iterates *to* convergence) — full convergence
would let trust diffuse across the very attack edges the early termination is
built to bottleneck. `KAMVAR-WWW-03`'s reported 10-iteration convergence and
`CAO-NSDI-12`'s O(log n)-iteration early termination are not measuring the
same thing and do not conflict; they are two different design decisions about
whether reaching convergence is desirable at all under this family's stated
attacker model.

## 9. Unsupported attribution: "GroupSybilRank" attributed to BrightID

`SIDDARTH-FRONTIERS-20` states that BrightID "runs GroupSybilRank — a
modification of the SybilRank algorithm — to score participants by graph
affinity to seeds." `BRIGHTID-WP`'s own retrieved whitepaper text never uses
the term "GroupSybilRank" anywhere; it states only that "BrightID solves the
unique identity problem through the creation and analysis of a social graph"
and that its research was "partly based on" SybilRank, without naming or
describing a distinct algorithm under that name. The figure this term
implies — a specific, named modification of SybilRank — travels with
`SIDDARTH-FRONTIERS-20`'s authority but is not supported by BrightID's own
primary text as retrieved for this corpus. This does not mean BrightID's
actual deployed code lacks such a routine (the whitepaper is not the codebase),
only that the retrieved primary source for this corpus does not contain the
term or a description matching it, so a synthesis should not cite `BRIGHTID-WP`
as the source of "GroupSybilRank."

## 10. Internal inconsistencies

**`WORLDCOIN-WP`.** The whitepaper's own privacy claim states "no biometric
data ever leave the user's device." The same document's own itemized
description of the Personal Custody Package — generated on the Orb (the
enrollment hardware) and sent to the user's phone — states it "currently
contains: iris and face embeddings, raw iris and face images, and the AMPC
fragments," each individually encrypted. The raw iris and face images are
formed and transported off the enrollment device as an encrypted package; the
document's "nothing leaves the device" framing and its own itemized package
contents are in tension, resolved only by reading "device" narrowly as
excluding the Orb once the package reaches the user's phone — a reading the
quoted sentence does not itself state.

**`LESNIEWSKI-LAAS-NSDI-10`** (Whanau). The paper's own analytical result
predicts the performance-transition point — where LOOKUP message count begins
growing exponentially with attack-edge count g — occurs at g > n/10 (n = honest
node count). The paper's own measurement across all four real datasets it
tests (Flickr, LiveJournal, YouTube, DBLP) instead finds this transition
occurs at m/10 < g < m (m = honest edge count), a substantially lower
attack-edge threshold than the analytical prediction promised. The paper
states this divergence as a measured fact (§7, table entry "Performance
transition point... occurs at m/10 < g < m... not at the analytically
predicted g > n/10") without reconciling it against its own Theorem-derived
bound elsewhere in the same paper.

## Notes on scope

Domain F (`ALVISI-SP-13` through `ZIEGLER-ISF-05` in the measurement index)
holds the bulk of this family's evidence; domain E supplied the
proof-of-personhood entries checked in §8. Entries read in full for this
report: `ALVISI-SP-13`, `CAO-NSDI-12`, `GAO-CNS-18`, `MOHAISEN-IMC-10`,
`VISWANATH-SIGCOMM-10`, `VISWANATH-EUROSYS-12`, `DANEZIS-NDSS-09`,
`YU-SIGCOMM-06`, `YU-SP-08`, `WEI-INFOCOM-12`, `BOSHMAF-NDSS-15`,
`GONG-TIFS-14`, `HEEB-ARXIV-24`, `SUN-ASONAM-20`, `GYONGYI-VLDB-04`,
`KAMVAR-WWW-03`, `LESNIEWSKI-LAAS-NSDI-10`, `LESNIEWSKI-LAAS-SNS-08`,
`MISLOVE-NSDI-08`, `TRAN-NSDI-09`, `WORLDCOIN-WP`, `IDENA-WP`,
`SIDDARTH-FRONTIERS-20`, `FORD-EUROSPW-17`, `CRITES-CCS-25`, `BRIGHTID-WP`.
Not read in full (index descriptions checked, no measurement-family figure
found in the index summary that pointed toward a new conflict beyond what the
above entries already establish): `DOUCEUR-IPTPS-02`, `FRIEDMAN-JEMS-01`,
`GUPTA-SIROCCO-20`, `HOFFMAN-CSUR-09`, `ISMAIL-BLED-02`, `LEVIEN-USS-98`,
`NASRULIN-BRAINS-22`, `POST-NSDI-11`, `SAFARPOOR-DEHKORDI-AAMAS-25`,
`SAFARPOOR-DEHKORDI-ARXIV-25`, `SRIVATSA-WWW-05`, `WANG-INFOCOM-17` (this key
is itself a registry mismatch — the file on disk is a later journal extension
of the cited INFOCOM 2017 paper, and its own evidence entry declines to record
figures under this key for exactly that reason), `ZIEGLER-ISF-05`,
`ADLER-ARXIV-24`, `IDE-ARXIV-25`, `CAMENISCH-TRUST-16`. A pass with more
budget should open the reputation-family entries in this list
(`SRIVATSA-WWW-05` TrustGuard, `ISMAIL-BLED-02` Beta Reputation,
`NASRULIN-BRAINS-22` MeritRank, `POST-NSDI-11` Bazaar) specifically for
reputation-metric convergence figures, since §8 above found none.
