# Open problem: verifying contributed bandwidth without trusting the contributor

**Verdict: partly.** Published constructions cut the achievable self-report inflation from a
demonstrated 177x down to a proven 1.33x, and one 2024 construction measures a single link's
capacity directly, from ordinary peers, within about 10% error, without any of them trusting the
contributor. Every one of these constructions obtains that bound by spending something a fully
open, permissionless, decentralized deployment does not already have for free: a fixed
semi-trusted quorum of measurement infrastructure, a pre-existing Sybil-resistant method for
drawing a random, uncontrollable witness sample from the same population being measured, or
continuously funded dedicated measurement bandwidth separate from the network's own capacity.
None verifies one untrusted peer's bandwidth contribution from bare peer-to-peer primitives with
no privileged quorum and no Sybil-resistance assumption supplied from outside the mechanism.

## What was searched

Corpus entries opened in full: `GHOSH-HOTPETS-14` (TorPath/TorCoin), `JANSEN-HOTPETS-14` (TEARS),
`JANSEN-PAM-21` (Tor bandwidth-estimation accuracy), `JOHNSON-POPETS-17` (PeerFlow),
`TRAUDT-ICDCS-21` (FlashFlow), `SHENG-NDSS-24` (Proof of Backhaul), `KEIZER-MOBIHOC-20` (Proof of
Timely Relay for NAT-traversal relays), `LEVIN-SIGCOMM-08` (BitTorrent PropShare, local
reciprocity rather than third-party verification), `ANDERSON-CCGRID-06`, `AIYER-SOSP-05` (BAR
fault tolerance, storage-audit accountability model, checked for a bandwidth analogue and found
none). Index files searched by keyword: `bandwidth`, `proof.of.bandwidth`, `proof.of.relay`,
`proof.of.coverage`, `reciprocal`, `tit.for.tat`, `bandwidth.token`, `bandwidth.credit`,
`torflow`, `peerflow`, `eigenspeed`, `bandwidth auth`.

Beyond the corpus: DBLP queries `q=proof of bandwidth` (5 hits, all already known or off-topic —
`LighTx`, a closed-access proof-of-bandwidth transaction-transfer system from NETYS 2021, and two
"Securing Proof-of-Stake Nakamoto Consensus Under Bandwidth Constraint" entries that use
"bandwidth" as a network-model parameter, not as a measured contributor claim) and `q=verifiable
bandwidth` (0 hits). Web searches run: "verifiable bandwidth accounting decentralized
peer-to-peer 2024 2025", `"proof of bandwidth" attack sybil 2024 2025 arxiv`, "DePIN bandwidth
verification survey SoK systematization 2024 2025", "Helium proof of coverage attack spoofing
measurement paper", `"Selfied" sybil defense bandwidth consumption blockchain paper`, `"Sharing Is
(S)caring" DePIN security privacy arxiv`, and `"Proof of Backhaul" attack critique follow-up
citation 2025`. These surfaced `Selfied` (Hou, Yu, Sun, Computer Networks, Nov. 2024 — in-protocol
bandwidth *consumption* as a Sybil-resistance resource for block production, a different problem
from verifying a contributor's bandwidth *supply* claim, not retrieved in full because it does not
bear on this problem), `FairRelay` (arXiv:2405.02973, 2024 — payment-channel atomicity between
content delivery and payment, which prevents a relay from being cheated of payment or a client of
content, but does not itself verify a bandwidth-capacity claim to a third party; abstract read via
WebFetch, not retrieved in full for the same reason), and a DePIN security survey ("Sharing Is
(S)caring," 18th International Conference on Network and System Security, Nov. 2024 / Springer
March 2025) whose direct PDF is captcha-gated and whose Springer and ResearchGate mirrors returned
403/redirect errors on this pass — its search-result summary describes only inherited Sybil and
consensus vulnerabilities in DePIN generally, with no bandwidth-specific mechanism named, so it is
recorded here as unretrieved rather than cited for any claim. No search surfaced a construction
published after `SHENG-NDSS-24` (NDSS 2024, the most recent directly relevant publication found)
that improves on its bound, and no search surfaced a published attack against it. EigenSpeed
(Snader and Borisov, IPTPS 2009), the peer-measurement predecessor every paper below cites and
attacks, was not independently retrieved; its measured attack figures are recorded below only as
`JOHNSON-POPETS-17`'s own re-implementation and measurement of attacks against it, not from
EigenSpeed's own text.

## The scale of the problem this corpus establishes first

Before any mitigation, `JANSEN-PAM-21` measures how bad self-report is even absent an adversary.
Tor's deployed pipeline derives a relay's advertised bandwidth from the relay's own two
self-measured numbers; an active 51-hour experiment adding a real measurement burst to 4,867
relays found total advertised network capacity rose from 360 Gbit/s to 550 Gbit/s — a 52.9%
underestimate the authors state is itself a lower bound, because their measurement machine was
capped at 1 Gbit/s and could not test every relay. The error concentrates exactly where it is most
useful to an adversary: relays in the top capacity quartile discovered a median 32.5% more
capacity than they had reported (median annual uptime 56.6%), against 0.0% for the two lowest
quartiles (median uptime 93.2%) — so a self-report pipeline is not merely noisy, it specifically
under-rewards large, low-uptime relays and over-rewards small, stable ones, and the paper states a
relay can detect when it is being measured and adjust its behavior accordingly. This is the
starting condition every construction below is measured against, not a hypothetical.

## Peer-measurement bounds a lie; it does not need a trusted authority to see the traffic, but it does need Sybil-resistance to bound the coalition

`JOHNSON-POPETS-17` (PeerFlow) replaces both self-report and a centralized probe (TorFlow) with
peer measurement: a subset of relays — the largest fraction µ=0.75 by capacity per circuit
position — each keep an application-layer byte count of every relay they directly interact with,
and Directory Authorities aggregate those peer reports rather than trusting either party's own
number. Implemented and measured against a real attack: a relay falsely reporting 125,000 KB of
bandwidth while selectively dropping non-measurement traffic raised its consensus-weight share
from 7% to 11% against TorFlow (a measured 177x bandwidth-inflation factor, Shadow simulation, 498
relays). Under PeerFlow's own peer-measurement design, the same class of attack is proven bounded
by a factor γ — a worked numerical example gives γ=4.52 — provided the adversary's voting-weight
fraction stays below a trim threshold λ=0.256. The paper is explicit about what supplies that
precondition: "even without any trusted relays" the bound requires a single adversarial coalition
to stay under λ, and states this means "some other component" — a Sybil-resistance mechanism
controlling how much aggregate weight one identity can acquire — must keep any single coalition
under that threshold for the bound to hold at all. PeerFlow supplies the bounded-inflation
mechanism; it consumes, rather than produces, Sybil-resistance. It also still requires a
functioning Directory Authority infrastructure to collect, trim (discarding the fraction λ=0.256
of most-disagreeing measurements), and noise (calibrated Laplace differential-privacy noise,
δnoise=1 MiB, εnoise=0.1) the aggregated peer reports before publishing them, because raw
peer-to-peer byte counts would otherwise leak which relay pairs exchanged how much traffic — a
side channel the mechanism must actively suppress at a stated cost, not one it can ignore. Achieving even the
bounded γ is stated by the authors to require an adversary to send traffic in only one direction
or concentrate it on a minority-weight subset of measuring relays, patterns the paper calls
"highly observable" but does not itself detect or block beyond the stated bound.

## Active load-testing narrows the bound further; the cost moves to a dedicated, funded measurement quorum

`TRAUDT-ICDCS-21` (FlashFlow) replaces both self-report and passive peer measurement with active
load-testing: a coordinated team of measurers forces a target relay to carry traffic large enough
to approach its claimed capacity, cross-checking a sampled fraction of returned cells
byte-for-byte so a relay that fabricates responses is caught with probability approaching 1 as
more responses are checked. The measured result is the strongest bound in this corpus: an
analytic inflation ceiling of 1.33x true capacity (derived from a traffic-ratio cap with
recommended parameter r=0.25), against the 177x PeerFlow demonstrated for TorFlow and PeerFlow's
own 4.52x bound for its recommended parameters — FlashFlow's own Table II states this comparison
directly. Real-Internet trials (Fremont, Santa Rosa, Washington DC, Bangalore, Amsterdam; 7 runs
per configuration over 24 hours) measured relay capacity within 11% of ground truth in 95% of
trials and within 20% in 99.8%. A Shadow simulation at 5% of Tor's scale (328 relays) found
FlashFlow cut network weight error from TorFlow's 29% to 4% and eliminated transfer timeouts
entirely at every tested load level. This bound has a real, ongoing cost: the design requires a
measurement team's aggregate bandwidth to exceed the highest capacity among target relays by a
factor f=2.84 in the deployed-scale simulation — 3 Gbit/s per team, provisioned and funded as an
ongoing operational cost separate from the bandwidth being measured — and requires the same
Directory-Authority/Bandwidth-Authority infrastructure Tor already runs, with a majority of both
sets required to be honest for the security bound to hold. The authors state their own design
explicitly shares TorFlow's Sybil weakness: a relay controlling several IP addresses on one
physical machine can be measured separately at different times and obtain a full-machine-capacity
estimate for each alias, with only an unimplemented "measure co-resident relays simultaneously and
average" proposed as a mitigation. FlashFlow also measures capacity, not delivered service — the
authors state explicitly that a relay could pass every load test while carrying little real client
traffic on non-measurement circuits, and call detecting that an unresolved future-work item shared
with TorFlow.

## The 2024 construction: peers measuring peers, with no measurer required to be individually trusted, but with the challenger sample itself needing to already be Sybil-resistant

`SHENG-NDSS-24` (Proof of Backhaul) is the most recent published construction and the only one
that verifies a link's bandwidth using a crowd of *ordinary*-bandwidth peers ("challengers")
instead of a dedicated high-bandwidth measurement server or a fixed authority set, tolerating
Byzantine (corrupted) challengers directly rather than assuming an honest quorum by
administrative fiat: proven correct for a corrupted-challenger fraction β<1/3 with no verifier
timer, and up to β<1/2 with one. Measured accuracy on a controlled testbed: under 5% error at 250
Mbps with 6 or more challengers and a 100 ms challenge; on a real deployment of roughly 25-30
active Ethereum-wallet challengers spread across the US, Europe, and Asia, backhauls of 500/700/
1000 Mbps measured with 4.2%/4.1%/9.9% average error. Two participant attacks are named and
bounded rather than merely observed: a withholding attack (a corrupted challenger under-sends)
degrades accuracy only slightly (3.6% raw error at 20% Byzantine challengers); a rushing attack (a
corrupted challenger colludes with a corrupted prover to shortcut the measured path and inflate
the result) is curtailed by a correction factor α=(n−2f)/(n−f) applied to every measurement,
which the authors state necessarily lowers the reported "guaranteed bandwidth" even when every
challenger is honest — 28% below the true value at the tested β=0.2 setting — because the
protocol cannot distinguish an honest run from a rushing attack after the fact and must discount
uniformly to stay safe. Against three prior bandwidth-estimation techniques at 500 Mbps
(pathchar, MagicTrain, speedtest), Proof of Backhaul matched speedtest's accuracy while using
roughly 73x less data (6.88 MB versus speedtest's 501 MB), and comfortably beat pathchar and
MagicTrain's accuracy despite their using still less data than either. This is the strongest
published bound on data cost, accuracy, and Byzantine tolerance simultaneously found in this
search, and it achieves all three from an untrusted, ordinary-bandwidth peer population rather
than a designated authority — but the paper itself states, unprompted, two of the preconditions
that make this possible: the verifier or challenge coordinator must be able to select "a fresh,
randomly drawn subset of challengers per measurement from a larger active pool" so a corrupted
prover cannot predict who will test it, and eliminating the rushing attack's residual bandwidth
discount entirely — rather than merely bounding it — requires an added shuffle-coordination round
(PoB-Shuffle) that the authors describe as "an active area of research" to implement efficiently
in practice, not something the base protocol delivers. The random, uncontrollable sampling of
challengers from the participant pool is exactly a Sybil-resistance precondition, supplied to the
mechanism from outside it — Proof of Backhaul answers "how do you verify one link's bandwidth once
you already have an unpredictable, bounded-Byzantine sample of the network to draw challengers
from," not "how do you obtain that sample in an open-membership network with no admission
control." The protocol's liveness (whether a challenge completes and produces a result, as
opposed to whether the result is correct) also depends on a challenge coordinator that the authors
state is not itself Byzantine-fault-tolerant, mitigated only by economic incentives and a pool of
redundant coordinators, not proven. And the measured object is a single link's instantaneous
capacity at one measurement window, not a running account of bytes a peer actually forwarded on
behalf of other peers over an accounting period — the object a reciprocal-exchange credit ledger
needs is closer to the latter than the former.

## Fully decentralized, circuit-cooperative proof exists, but its guarantee is statistical across a population, not per-relay, and it was never measured past a preliminary simulation

`GHOSH-HOTPETS-14` (TorPath/TorCoin) is the one construction in this corpus with no designated
authority at all: a circuit's own four participants (client, entry, middle, exit) jointly produce
a cryptographic proof obtainable only if all four actually forwarded traffic to each other — no
proper subset can reconstruct the shared blob alone — and Bitcoin's blockchain prevents the
resulting coin from being claimed twice. This genuinely verifies, without any single contributor's
self-report and without a bandwidth authority, that real forwarding occurred on one specific
circuit. Three limits keep it from answering this problem for an open decentralized deployment.
First, circuit assignment itself depends on a majority-honest quorum of decentralized "assignment
servers" running a verifiable shuffle — a group-trust assumption, not zero-trust, and one the
paper illustrates with "if there are 10 assignment servers, we might require at least 6" without
adopting a tested value. Second, the guarantee the mechanism gives is a population statistic, not
a per-relay one: under the paper's own stated assumption that at most half of network identities
collude, only 1/16 of assigned circuits are fully colluding and able to mint coins for zero
genuine transfer — the authors state explicitly that coin possession proves goodput on one
specific circuit at mint time, not an ongoing, per-relay measure, and that a higher colluding
fraction was not analyzed. Third, the reported packet-overhead figures (roughly 5% of Tor traffic
at a tuning parameter m≥10) come from a Python-Twisted message-passing simulation the authors
themselves describe as "preliminary," with no stated relay count, run count, or live-network
deployment — no measurement in this corpus validates these figures against a real network. The
Sybil case this problem exists to prevent — the same operator running many relay identities to
occupy more than one position on its own circuit — is explicitly out of scope: the authors state
this "should be rare" and defer building any detection mechanism to future work. Its
contemporaneous companion paper, `JANSEN-HOTPETS-14` (TEARS), states the underlying problem this
whole line of work responds to in as many words: "measuring relay bandwidth securely is an open
research problem," and supplies no bandwidth-audit mechanism of its own, requiring one as an
unspecified external component.

## The narrow case with a working check node is not collusion-free either

`KEIZER-MOBIHOC-20`'s Proof of Timely Relay, built for NAT-traversal relays rather than an
anonymity network, verifies one relay's forwarding by routing a hash-and-timestamp report through
a second, independently chosen "check" node in parallel with the data path, so the working relay's
own report is never trusted alone — settled through an Ethereum smart contract that withholds
payment from both parties until each submits a mutual trust score. This requires the client to
reach two independent relay-capable nodes simultaneously for every session, and the paper's own
security analysis addresses only a rational adversary motivated by resource gain, not one willing
to collude: it does not analyze what happens when the working relay and the check node the client
selected are the same coalition, which is exactly the case a Sybil-heavy or a colluding relay
population would try to arrange. Per-transaction settlement cost, measured on a private Ganache
chain at April-2020 Ethereum gas prices, ran roughly $0.10-$0.20 for the relay and $0.40-$0.60 for
the client per contracted relationship — a real, non-zero cost of the on-chain accountability
layer, not free verification.

## What remains unestablished

No retrieved source verifies an untrusted peer's bandwidth contribution to a third party using
only primitives available to that peer's own open-membership network — every published bound
requires, as an input rather than an output, one of: a fixed quorum assumed majority-honest by
administrative design (Directory Authorities, Bandwidth Authorities, TorPath's assignment
servers), a pre-existing Sybil-resistant method for drawing an unpredictable challenger or witness
sample from the same population being measured (Proof of Backhaul's challenger pool), or
continuously funded dedicated measurement bandwidth provisioned separately from the network's own
capacity (FlashFlow's measurer teams). Where the bound is tightest (FlashFlow's 1.33x, Proof of
Backhaul's sub-10% error) the authority or witness-sampling precondition is most explicit; where no
authority or witness precondition is required at all (TorPath), the guarantee weakens to a
population-level statistic with no field measurement past a preliminary simulation, and the
paper's own contemporaneous companion states plainly that secure bandwidth measurement was still
an open research problem. No search in this pass located a published construction after
`SHENG-NDSS-24` (2024) that removes the challenger-sampling precondition, nor a published attack
against it. Closing this gap for a fully open, permissionless deployment — one drawing its
challenger or measuring-relay population from the same unauthenticated pool of contributors it is
trying to keep honest, with no fixed authority set and no external Sybil-resistance mechanism
supplied — is not demonstrated anywhere in the retrieved literature.
