# Incentives family: conflicts and disagreements

Scope: throughput gained by a strategic client, the fraction of participants
contributing nothing, bandwidth-accounting accuracy, proof-of-work and
memory-hard-function costs and the attacks on them, anonymous-token issuance
and redemption cost, and storage-payment outcomes. Entries covered: `ADAR-FM-00`,
`AIYER-SOSP-05`, `ALWEN-EUROSP-17`, `BENHAMOUDA-ASIACRYPT-23`, `BIRYUKOV-EUROSP-16`,
`BIRYUKOV-FC-15`, `BONEH-ASIACRYPT-16`, `COHEN-IPTPS-03`, `COX-SOSP-03`,
`DAVIDSON-POPETS-18`, `GHOSH-HOTPETS-14`, `GOLLE-EC-01`, `JANSEN-HOTPETS-14`,
`JANSEN-PAM-21`, `JOHNSON-POPETS-17`, `KREUTER-CRYPTO-20`, `LEVIN-SIGCOMM-08`,
`LOCHER-HOTNETS-06`, `NGAN-IPTPS-03`, `PERCIVAL-BSDCAN-09`, `PIATEK-NSDI-07`,
`REVUELTA-DLT-24`, `SIRIVIANOS-IPTPS-07`, `SILDE-FC-22`, `TAHERIBOSHROOYEH-ARXIV-22`,
`TRAUDT-ICDCS-21`, `TYAGI-EUROCRYPT-22`, `VISHNUMURTHY-P2PECON-03`. `KRISHNAN-ICIS-02`
holds no evidence — its retrieved file is a mismatch for the target citation and
carries no extracted claims, so it contributes nothing to this family.

## 1. The specific memory-hard-function attack the assignment asks about

`ALWEN-EUROSP-17` and `BIRYUKOV-EUROSP-16` reach opposite conclusions about
whether the Alwen-Blocki tradeoff attack threatens Argon2i-B at 1 GB of memory,
the same memory scale, because they apply different methods to the same attack
family.

`BIRYUKOV-EUROSP-16` (the Argon2 v1.3 specification, authored by the algorithm's
designers) evaluates the attack analytically: it takes the Alwen-Blocki attack's
own published time-area formula, `2 T^(7/4)(5+t+ln T)/8`, and substitutes
Argon2's parameters directly. The resulting time-area advantage is below 1 (no
adversary benefit) for memory up to 2^20 blocks (1 GB) and below 2 up to 2^24
blocks (16 GB), and the document concludes this attack "is not better than the
ranking attack" the designers already analyze, so it treats the memory range up
to 16 GB as safe from this attack family.

`ALWEN-EUROSP-17` (Alwen and Blocki's own follow-up paper) simulates the attack
instead of bounding it analytically, running it on randomly sampled Argon2i-B
DAGs at the same 1 GB memory parameter, with the pass count (τ=6) the IRTF
proposal recommends. The simulation adds two heuristics the analytic bound does
not model: an improved depth-reducing-set construction and an "XOR compression"
technique, plus an explicit accounting for bounded attacker parallelism. Under
these heuristics the attack reduces cost by a factor of 2 against Argon2i-B at
1 GB and τ=6 — inside the parameter range `BIRYUKOV-EUROSP-16`'s analytic bound
calls safe — and the paper states more than 10 passes are needed at 1 GB for the
attack to fail.

The two papers are not measuring different quantities: both state a cost-
reduction factor for the same named attack (Alwen-Blocki) against the same
target (Argon2i-B) at the same memory parameter (1 GB). The disagreement is
genuine, and each paper's own entry in this evidence set states so directly —
`BIRYUKOV-EUROSP-16`'s Contradicts section calls out that "the two documents
disagree about the practical severity of the same underlying attack family at
the same memory scale." What differs is method: `BIRYUKOV-EUROSP-16` plugs
Argon2's parameters into the original 2016 attack's own worst-case formula and
stops there; `ALWEN-EUROSP-17` runs the attack, including heuristic
improvements to it that postdate the formula `BIRYUKOV-EUROSP-16` analyzed. The
disagreement is therefore best read as an analytic upper bound on an
unoptimized attack versus a simulated, optimized instantiation of the same
attack — the earlier bound did not, and could not, account for an improvement
published after it.

A related, narrower attack on the same algorithm corroborates that Argon2i's
own security margin against memory-reduction attacks has moved since the 1.2.1
design document: `BONEH-ASIACRYPT-16` reports a separate ("no-use gap")
precomputation attack against Argon2i v1.2.1 achieving `n/4`-space computation
with, in the authors' words, "no computational penalty," against that design
document's own claimed 7.3x penalty at the same space fraction — a contradiction
`BONEH-ASIACRYPT-16` states directly against a document that is not itself a
key in this corpus (the 1.2.1 design document, distinct from the v1.3
specification retrieved as `BIRYUKOV-EUROSP-16`). `BIRYUKOV-EUROSP-16`'s own
text confirms the same class of attack was live against 1.2.1 (a 3.5x-5x
time-area advantage it calls the "no-use gap" attack) and states the v1.3
XOR-based fix was introduced specifically to close it. This is not an
independent second disagreement between two corpus entries; it is the same
pattern — an attack outrunning an earlier version's analysis — recorded against
a document version this corpus does not hold as a separate key.

## 2. Whether BitTorrent's reciprocity rule stops a strategic client from gaining throughput

`COHEN-IPTPS-03` (BitTorrent's own design paper) and `PIATEK-NSDI-07` reach
opposite conclusions about whether tit-for-tat reciprocity alone prevents a
strategic client from outperforming a compliant one, but the disagreement is
between an unmeasured design claim and a controlled measurement, not between
two comparable figures.

`COHEN-IPTPS-03` states that tit-for-tat "tend[s] to have" properties of full
resource utilization and resistance to non-contributing peers, presented as a
consequence of a cited general economic argument rather than a measurement; its
own measured-results table contains field observations of swarm health (over
1,000 simultaneous downloaders in a large deployment, tracker overhead under
0.1% of bandwidth) and no controlled test of strategic or non-contributing
peer behavior at all.

`PIATEK-NSDI-07` measures the reciprocity rule directly against a strategic
client, BitTyrant, across 114 real-world swarms (300-800 peers each) and a
350-node PlanetLab testbed: a single strategic peer gains a median 1.72x
completion-time factor over an unmodified client (a 1 Mb/s-class client's
stated headline figure is a median 70% gain), with 25% of downloads finishing
at least twice as fast. The paper's own title and conclusion state the result
as a direct rebuttal — "incentives do not build robustness in BitTorrent" — and
its Contradicts section names `COHEN-IPTPS-03` as the claim it disputes.

`LEVIN-SIGCOMM-08` measures a third protocol variant, PropShare, designed to
close part of the gap BitTyrant exploits: a lone BitTyrant peer placed among
PropShare peers averages 109 s against an all-BitTyrant baseline of 86.9 s —
worse, not better, for the strategic peer under this different allocation
rule. This is not a third figure for the same quantity `PIATEK-NSDI-07`
reports; it measures a strategic peer against a different reciprocity rule than
plain tit-for-tat, so it does not contradict `PIATEK-NSDI-07`'s 1.72x figure,
which was measured against the reference tit-for-tat client.

`LOCHER-HOTNETS-06` (BitThief, zero upload) and `SIRIVIANOS-IPTPS-07`
(large-view free-riding) both measure a different quantity again — completion
of a download with no or reduced upload contribution, rather than a throughput
multiple for an unchoke-ranking strategy — and each paper's own entry states
explicitly that its numbers are not comparable to the other's: different
torrents, different swarm compositions, and different metrics (relative
completion-time multiples against a fixed reference client versus absolute
mean completion times swept by free-rider population share). Both
independently conclude that zero or reduced upload can match or beat a
compliant client under some conditions, which is consistent with, but not the
same measurement as, `PIATEK-NSDI-07`'s figure.

## 3. Internal inconsistency: BAR's own throughput figure

`AIYER-SOSP-05`'s abstract states its replicated-state-machine prototype
"executes 20 requests per second." Section 8, the paper's own evaluation, states
"about 15 operations a second for small groups of users." The two figures are
not reconciled anywhere in the retrieved text — the entry's measured-results
table records this explicitly. A synthesis quoting only the abstract's
headline number would overstate the measured throughput by about a third.

## 4. Destroyed precondition: persistent identity versus unlinkable tokens

`GOLLE-EC-01`'s micro-payment and point-based sharing mechanisms require agents
to hold a persistent identity across time: points and monetary balances must
carry over between sessions and attach to the correct identity retroactively,
including a deferred-credit scheme for files that start rare and later become
popular. `VISHNUMURTHY-P2PECON-03` (KARMA) requires the same precondition more
strongly — every participant holds one persistent public/private key pair
established at join time, and every balance-transfer message must be signed by
that key, since KARMA's bank-set members resolve a transaction by majority vote
over that identity's transaction history.

`DAVIDSON-POPETS-18` (Privacy Pass) is built so that a server "without either
side ever having linked this redemption to the earlier signing session that
produced it" — unlinkability is the paper's stated design goal, following from
the underlying oblivious-PRF's message-hiding property. `BENHAMOUDA-ASIACRYPT-23`
generalizes the same property: its anonymous counting tokens let an issuer
enforce a one-token-per-message limit "without the issuer or a verifier
learning which client requested which message or linking two tokens to the
same client."

A system that selects an unlinkable anonymous-token scheme as its
rate-limiting or admission layer removes the signal `GOLLE-EC-01`'s and
`VISHNUMURTHY-P2PECON-03`'s incentive mechanisms require: a verifier that
cannot link two token uses to the same client cannot accumulate a balance
against that client across time. The two token schemes register a client key
at issuance (`BENHAMOUDA-ASIACRYPT-23`'s `ClientRegister` step), but that
registration is deliberately not exposed to the verifier at redemption, which
is the property that breaks the precondition. `COX-SOSP-03` (Samsara) is the
counter-example within this same family: its entry states explicitly that its
core storage-exchange mechanism "does not require certified identity or a
public-key infrastructure," so an unlinkable-token layer does not remove
anything Samsara's punishment mechanism needs — only the balance-carrying
mechanisms in `GOLLE-EC-01` and `VISHNUMURTHY-P2PECON-03` are exposed to this
conflict.

## 5. Checked and found not to conflict: RLN proof-generation time

`TAHERIBOSHROOYEH-ARXIV-22` reports membership-proof generation of
approximately 0.5 s, measured on an iPhone 8 against a Merkle tree of depth 32
(group size 2^32), a figure the paper states it took from the RLN library
rather than re-measured itself. `REVUELTA-DLT-24` reports proof generation
between 85.7 ms (MacBook M1 Pro) and 766.8 ms (Raspberry Pi 4B), measured
directly against a Merkle tree of depth 20. The two figures are not
comparable: the tree depth differs by 12 levels (2^32 versus 2^20 members,
changing the number of Merkle-path hashes the proof covers), the hardware
differs by roughly a mobile-processor generation, and `TAHERIBOSHROOYEH-ARXIV-22`'s
number is a third-party library figure rather than an independent measurement
on stated hardware. Verification time (approximately 30 ms in
`TAHERIBOSHROOYEH-ARXIV-22` versus 2.7-18.7 ms across `REVUELTA-DLT-24`'s
hardware range) sits within the same order of magnitude once the same
tree-depth and hardware differences are accounted for. This is a difference in
experimental conditions, not a disagreement.

## Not found

No unsupported attribution was found within this family: the two places where
one entry's figure traces to another paper's construction under comparable
conditions (`TRAUDT-ICDCS-21` citing `JOHNSON-POPETS-17`'s 177x TorFlow
bandwidth-inflation figure; `TYAGI-EUROCRYPT-22` re-implementing and
re-benchmarking Pythia itself rather than citing `EVERSPAUGH-USENIXSEC-15`'s
numbers) both check out against the cited paper's own retrieved text.
