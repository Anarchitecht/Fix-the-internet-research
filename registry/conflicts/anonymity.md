# Anonymity family: conflicts and disagreements

Scope: onion-routing latency, website-fingerprinting classifier accuracy,
padding-defense bandwidth and time overhead, mix-network latency and
cover-traffic rate, private-information-retrieval throughput and query/response
sizes, private-set-intersection cost, oblivious-RAM bandwidth multipliers.
Entries read: `CAI-CCS-14`, `JUAREZ-ESORICS-16`, `GONG-USENIXSEC-20`,
`GONG-SP-22`, `HOLLAND-POPETS-22`, `SHEN-SP-24`, `WANG-USENIXSEC-14`,
`SIRINAM-CCS-18`, `HENZINGER-USENIXSEC-23`, `MENON-USENIXSEC-24`,
`MENON-SP-22`, `ZHOU-SP-24`, `MUGHEES-CCS-21`, `DAVIDSON-POPETS-23`,
`ANGEL-SP-18`, `CHOR-JACM-98`, `VANDENHOOFF-SOSP-15`, `CORRIGANGIBBS-SP-15`,
`TYAGI-SOSP-17`, `LAZAR-OSDI-18`, `LAZAR-SOSP-19`, `CHENG-ACSAC-20`,
`PIOTROWSKA-USENIXSEC-17`, `PIOTROWSKA-WPES-21`, `DOUCEUR-IPTPS-02`,
`DINGLEDINE-USENIXSEC-04`, `KOLESNIKOV-CCS-16`, `CHASE-CRYPTO-20`.

## 1. Padding-defense overhead: simulation against live Tor deployment, for the same defense

### 1.1 Tamaraw, matched-parameter same-paper comparison

`SHEN-SP-24` reports Tamaraw's bandwidth and time overhead twice, under the
same rho and L parameters, once by simulation and once by an actual
pluggable-transport (PT) deployment on the live Tor network:

- Simulation (closed-world, DF-CW-scale dataset, 95 sites): 121% bandwidth
  overhead, 43% time overhead.
- Live deployment (WFDefProxy PT framework, real Tor bridge, Tor Browser
  10.5.10, first 100 accessible sites from the February 2023 Tranco list):
  135% bandwidth overhead, 78% time overhead.

Bandwidth overhead rises 14 percentage points; time overhead rises 35
percentage points, entirely from moving the identical padding schedule off a
trace-transformation simulation and onto a real network path. `SHEN-SP-24`
states this pattern held for every defense it tested live, worst for
RegulaTor (below), and attributes the general gap to "packet dependencies
between incoming and outgoing traffic that simulation cannot represent." This
is the cleanest matched pair in the corpus for the assigned question, because
parameters and dataset are the paper's own and held fixed across both modes.

### 1.2 Tamaraw, cross-paper: simulated 196% against live-deployed 121%

`HOLLAND-POPETS-22` simulates Tamaraw (rho_out=0.04, rho_in=0.012, L=100,
750-byte packets, "Tao Wang's implementation," applied to the DF-CW dataset)
and reports 196% bandwidth overhead, 36.9% latency overhead. `GONG-SP-22`
deploys Tamaraw as a live PT on an actual Tor entry node (rho_c=14ms,
rho_s=4ms, L=100, 514-byte packets) and reports 121% data overhead, 26% time
overhead on the live Tor network. Both figures are real; this is the pair
the brief already names as calibration (196% against 121%). Two conditions
differ at once, not one: simulation against live deployment, and packet size
(750 bytes against Tor's actual 514-byte cell). `GONG-SP-22` states directly
that Tamaraw's rho parameters "had to be recalculated for this deployment
because Tor's actual cell size (514 bytes) differs from the 750-byte payload"
Tamaraw's original paper assumes, so part of the 75-percentage-point gap is a
parameter-recalibration effect, not a pure simulation-against-live effect —
the `SHEN-SP-24` pair in §1.1, which holds the padding schedule fixed, isolates
the live-deployment effect on its own.

### 1.3 RegulaTor: same-paper sim-to-real gap is small in one paper, huge in another

`HOLLAND-POPETS-22` reports RegulaTor-Heavy's own simulated overhead (DF-CW
dataset): 79.7% bandwidth, 6.6% latency. Its own real-world PT deployment
(WFPadTools/Obfsproxy bridge, one month, August 2021, Alexa Top 100, 100
samples/site): 78.2% bandwidth, 13.9% latency. Bandwidth is unchanged; latency
overhead roughly doubles.

`SHEN-SP-24` reproduces RegulaTor in simulation (80% bandwidth, 5% time) and
then deploys it live (WFDefProxy PT, Tor Browser 10.5.10, Tranco Feb-2023 top
100): time overhead rises to 112%, which `SHEN-SP-24` itself calls the most
severe simulation-to-real divergence of every defense it tested.

Reading the two real-world deployments against each other is a second,
cross-paper disagreement: RegulaTor's live latency overhead is 13.9%
(`HOLLAND-POPETS-22`, WFPadTools/Obfsproxy PT, Aug 2021, Alexa Top 100) against
112% (`SHEN-SP-24`, WFDefProxy PT, ~2023-24, Tranco top 100) — an eightfold
gap between two papers each claiming a real Tor-network PT deployment of the
same defense. Conditions genuinely differ (different PT framework
implementation, different site population, roughly two years apart, and no
stated confirmation that `SHEN-SP-24` reran `HOLLAND-POPETS-22`'s own
traffic-volume recalibration step for RegulaTor's R and N parameters before
deploying). Given that difference in conditions, this is not a proven
contradiction, but an eightfold gap between two live deployments of a defense
whose own bandwidth-side parameters usually transfer with much smaller error
(§1.1's Tamaraw bandwidth figure moved 14 points, not 800%) is large enough
that a difference in what was implemented, not only where it ran, is the more
likely explanation; neither paper's retrieved text lets this be resolved
further.

## 2. Same nominal parameters, different dataset: FRONT and WTF-PAD overhead

`GONG-USENIXSEC-20` and `HOLLAND-POPETS-22` both simulate FRONT at identical
parameters (N_c=N_s=1700, W_min=1s, W_max=14s) and report bandwidth overhead
33.01% (`GONG-USENIXSEC-20`, DS-19 dataset, Alexa Top 100 collected 2019) against
81.0% (`HOLLAND-POPETS-22`, DF-CW dataset, collected by Sirinam et al. in
2016) — 2.5 times higher on the older dataset. The same ratio (about 2.4
times) recurs at the second tested FRONT budget, N=2500: 48.80%
(`GONG-USENIXSEC-20`) against 119.0% (`HOLLAND-POPETS-22`). This is a
difference in what was measured, not a contradiction: FRONT's dummy-packet
budget is a fixed absolute count per page load, so the same budget is a larger
fraction of a smaller real-page trace; `HOLLAND-POPETS-22` documents elsewhere
that its own defense's overhead is sensitive to the real-traffic-volume
baseline of whichever dataset it runs against, and average page sizes on the
open web grew between the 2016 and 2019 collection dates. The same
dataset-year pattern appears, at smaller magnitude, for WTF-PAD's default
configuration: 54% (`JUAREZ-ESORICS-16`, own 2014-era dataset), 54.0%
(`HOLLAND-POPETS-22`, reproducing "authors' original code" on DF-CW),
32.71% (`GONG-USENIXSEC-20`, DS-19), 61% (`SHEN-SP-24`, its own dataset). A
synthesis citing a defense's fixed-budget overhead figure must name which
dataset and collection year it came from; the figure does not transfer across
datasets even at identical padding parameters.

## 3. PIR throughput: cross-hardware, not cross-claim

`HENZINGER-USENIXSEC-23` measures DoublePIR at 7.4 GB/s/core (AWS c5n.metal,
single-threaded). `MENON-USENIXSEC-24` reruns the same reference
implementation (commit-pinned) on an AWS r6i.16xlarge and measures 9.9-10.6
GB/s across the tested database sizes. Both papers' own text name this as a
hardware artifact rather than a disagreement about the construction:
`MENON-USENIXSEC-24`'s own entry states the two figures are "a cross-hardware
discrepancy, not a same-condition contradiction." A synthesis citing
SimplePIR/DoublePIR throughput must cite the paper and machine, not a single
number.

## 4. Does a recent PIR result change the cost of interactive private search

The brief's open-problem framing ("current single-server PIR costs seconds
per query on multi-gigabyte databases") describes the FHE-composition family
measured in this corpus: `MENON-SP-22` (Spiral) takes 24.46 seconds of server
computation for one 30 KB-record retrieval from a 7.9 GB database (2^18
records); `MUGHEES-CCS-21` (OnionPIR) takes about 400 seconds for a 30 KB
entry from a similarly sized database, and its own comparison baseline,
SealPIR, is slower still.

Three papers published in 2023-2024 supersede that figure for the specific
case of retrieving one small record by an already-known index. `HENZINGER-USENIXSEC-23`
(SimplePIR/DoublePIR) answers a query against a 1 GB database in 74-94 ms of
server time. `MENON-USENIXSEC-24` (YPIR) answers a query against a 32 GB
database in 2.64 seconds of server time without requiring the tens-of-megabyte
offline "hint" download SimplePIR/DoublePIR need before a client's first
query. `ZHOU-SP-24` (Piano) is the sharpest case: on a live wide-area link
(US west coast server, US east coast client, 60 ms round-trip time), Piano
answers one query against a 100 GB database in 73 ms total, 1.2 times a
non-private direct-download baseline on the same link, against an extrapolated
10.9 seconds for SimplePIR at the same size (the open-source SimplePIR
implementation does not run at 100 GB, so this comparison figure is Piano's
own extrapolation, stated as such in its own text, not a measured SimplePIR
run).

This changes the answer to "does single-server PIR cost seconds per query on
gigabyte-scale databases" from yes to no, for one-bit-to-one-byte records
retrieved by a client-known numeric index. It does not close the broader
"private search at interactive latency" problem the brief poses, for two
reasons stated directly in the requirements these same papers place on the
rest of the system. First, every one of these schemes — `ANGEL-SP-18`,
`DAVIDSON-POPETS-23`, `HENZINGER-USENIXSEC-23` alike — requires the client to
already hold the numeric database index it wants before the online phase
begins; `DAVIDSON-POPETS-23` states explicitly that mapping a real key (a URL
hash, a search term) to that index is a separate mechanism the client must
obtain out of band, and none of these papers builds or measures that
mechanism. Second, the sub-second figures above are demonstrated for small,
fixed-size records (one bit up to 64 bytes in `MENON-USENIXSEC-24`'s own
tables); the same corpus's large-record results (`MENON-SP-22`: 24.46 s at 30
KB/record over 7.9 GB; `MUGHEES-CCS-21`: about 400-900 s at 30-60 KB/record)
have not been re-measured under the newer hint-free constructions at
comparable record sizes. The retrieval-by-known-index cost has become
interactive; the search-by-content-or-keyword cost, which is what "private
search" means for a browsing client, is not demonstrated at that speed by any
entry in this corpus.

## 5. Destroyed preconditions

### 5.1 Anytrust server sets require an identity guarantee Sybil resistance cannot supply without a central issuer

`VANDENHOOFF-SOSP-15` (Vuvuzela) requires at least one of its fixed relay-chain
servers to be honest; its own security proof is "conditioned on this
one-honest-server step existing." `CORRIGANGIBBS-SP-15` (Riposte) requires no
two of its three servers to collude, and states plainly it "provides no
mechanism to enforce or detect collusion." `TYAGI-SOSP-17` (Stadium) requires
at least one honest server per mixchain. `LAZAR-OSDI-18` (Karaoke) requires a
globally known, fixed server set with a stated honest fraction. `CHENG-ACSAC-20`
(Talek) requires an anytrust deployment, at least one of its participating
servers honest. Every one of these five metadata-private messaging systems
places its privacy guarantee on the same requirement: a small, fixed set of
servers, independently operated, of which at least one (or, for Riposte, at
least two of three) is not colluding with the rest.

`DOUCEUR-IPTPS-02` proves that this requirement cannot be met by open
enrollment. Absent a logically centralized identity-issuing authority, a
single faulty entity can present an unbounded number of distinct identities
(Lemma 2, when identities are not challenged in a synchronized round) or a
number proportional to its own resource advantage (Lemma 1). Nothing in an
open, permissionless peer population — the kind the architecture in this
brief specifies for identity, indexing, and storage — gives a selection
process reason to believe that a chosen small server set is operated by
independent parties rather than one entity running every seat, or that any two
of them are not colluding. The anytrust and non-collusion preconditions these
five systems require are exactly what an admission-free peer population
cannot supply.

Resolution is not settled by the evidence: either these systems' server roles
are staffed by an admission-controlled, identity-vetted process (a departure
from full permissionlessness for this one privacy tier, to be stated as such
rather than left implicit), or the corpus's non-collusion assumption is
recorded as an open problem for a fully open peer population, or a different
privacy mechanism not requiring a curated server set is selected for that
tier.

### 5.2 Cover-traffic-efficient anonymity requires a stratified topology a flat peer mesh does not provide

`PIOTROWSKA-USENIXSEC-17` (Loopix) and its reproduction in `PIOTROWSKA-WPES-21`
state that Loopix/Nym's anonymity growth with user count depends on a
three-layer stratified topology, in which independent routes through
different mixes still intersect into one shared anonymity set.
`PIOTROWSKA-WPES-21` states this requirement directly: reproducing the
Nym-favorable result "requires a stratified topology with intersecting routes
across layers... a P2P topology (as in HOPR)... does not produce this
property in the simulator."

The same paper measures what a flat peer-to-peer mix mesh costs instead, using
HOPR as the P2P case, under the same simulator, same per-node processing
capacity (1000 packets/second), and the same per-hop delay model as the
stratified case, so this is a matched, not merely reported, comparison: HOPR's
anonymity (entropy) stays low and nearly flat as users scale from 10^2 to
10^5, and reaching a higher anonymity level requires cover-to-real traffic
ratios up to 10:1 — at which point HOPR's anonymity still stays below what
Nym's stratified design reaches at much lower cover-traffic cost. A flat,
undifferentiated peer mesh — the topology a fully decentralized design
without a layered or role-differentiated relay structure would produce —
destroys the path-intersection property Loopix/Nym's cover-traffic economics
depend on.

This connects to §5.1: a stratified topology is itself a form of role
differentiation among peers (layer membership, or provider status in Loopix),
which raises the same question of who is trusted to hold which role and
whether that assignment survives an open, permissionless join process.
Neither paper in this corpus measures a mix design that reaches Loopix/Nym's
anonymity-per-cover-traffic-byte cost in a flat P2P topology; this is recorded
as an open problem, not resolved by any entry read for this family.

## 6. Not found: unsupported attributions and internal inconsistencies

No entry in this family attributes a figure to another corpus paper that the
cited paper's own retrieved text fails to support. The one borderline case is
a corpus bookkeeping error, not a paper-to-paper attribution: the registry's
own retrieval-justification metadata for `WANG-USENIXSEC-14` labels it "the
Walkie-Talkie paper"; `WANG-USENIXSEC-14`'s own retrieved text states this is
wrong (it is Wang, Cai, Nithyanand, Johnson, Goldberg, USENIX Security 2014,
the k-NN-attack and provable-supersequence-defense paper), and
`SIRINAM-CCS-18`'s own bibliography confirms Walkie-Talkie is a distinct 2017
paper by Wang and Goldberg. Both entries already self-correct this in their
own text; no synthesis claim in this corpus was traced back to the mislabeled
source, so this is a registry-metadata fix, not a finding against a paper.

No entry in this family shows its own abstract and its own conclusion or body
stating opposite claims about the same mechanism. The closest candidate,
`SHEN-SP-24`'s simulation-against-live-deployment gap (§1.1, §1.3), is not an
abstract/conclusion inconsistency: the paper states both figures as measured
under different execution modes and draws the same conclusion from both
(real-world overhead exceeds simulated overhead for every defense tested), so
this is a documented external-validity limitation, not an internal
contradiction.
