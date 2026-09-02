# Open problem: honest capacity reporting in a capacity-ordered overlay

**Verdict: open.** No retrieved paper defends a structured overlay that places participants at a
position, or rank, determined by self-reported bandwidth against a participant that misreports to
gain that position. The published defenses closest to this problem — for Tor's bandwidth-weighted
relay-selection pipeline — bound a different quantity, a flat selection *probability* over an
unordered relay set, not a *position* in an ordered structure, and every one of them either
assumes a semi-trusted measurement quorum or a challenger sample that is itself assumed
Sybil-resistant rather than made so by the mechanism. HSkip+, the specific design this problem
names, states its bandwidth-ordering property assumes honest reporting; two independent surveys,
four years apart, find no published follow-up that revisits that assumption.

## What was searched

Corpus entries opened in full: `JOHNSON-POPETS-17` (PeerFlow), `TRAUDT-ICDCS-21` (FlashFlow),
`SHENG-NDSS-24` (Proof of Backhaul), `JANSEN-PAM-21` (Tor bandwidth-estimation accuracy),
`GHOSH-HOTPETS-14` (TorPath/TorCoin), `JANSEN-HOTPETS-14` (TEARS), `ELAHI-WPES-12` (Tor guard
rotation), `FELDMANN-CSUR-21` (self-stabilizing overlay survey, already keyed for its HSkip+
forward-citation check), `JACOB-JACM-14` (Skip+). Index files searched by keyword: `bandwidth`,
`capacity`, `misreport`, `self-report`, `overlay position`, `freerid`, `incentive`, `whitewash`,
`reciprocity`. This confirmed the corpus already holds every directly relevant Tor
bandwidth-measurement paper and the two surveys that forward-cite HSkip+.

Beyond the corpus: DBLP queries `capacity-ordered overlay bandwidth misreport` (0 hits),
`self-stabilizing skip graph bandwidth heterogeneous` (0 hits), `verifiable bandwidth claim
peer-to-peer` (0 hits), `skip graph bandwidth` (0 hits), `proof of bandwidth` (5 hits, all already
known or off-topic — a closed-access transaction-transfer system and two unrelated
proof-of-stake papers using "bandwidth" as a network-model parameter). arXiv queries
`abs:"bandwidth" AND abs:"overlay" AND abs:"misreport"` (0 hits), `abs:"self-reported bandwidth"`
(0 hits), `abs:"capacity-aware" AND abs:"peer-to-peer" AND abs:"Sybil"` (0 hits). OpenAlex and
Semantic Scholar keyword searches on "self-reported bandwidth peer-to-peer overlay attack" and
"Sybil-resistant bandwidth reporting peer-to-peer overlay" returned no on-topic result beyond what
DBLP and general web search already found. General web search for `"bandwidth-ordered" OR
"capacity-ordered" overlay peer-to-peer misreport attack defense`, `skip graph OR DHT
self-stabilizing bandwidth heterogeneous adversarial misreport 2024 2025`, and `verifiable
bandwidth claim decentralized peer-to-peer overlay position Sybil 2024 2025 2026` surfaced two
papers not previously in the corpus, both retrieved in full text and checked directly rather than
from their abstracts: `IHLE-CSUR-23` (a 2023 systematic review of peer-to-peer incentive
mechanisms, 178 primary papers) and `PATEL-ARXIV-25` (a September 2025 survey of secure
peer-to-peer networks). A third paper, `ARADHYA-ARXIV-25` (self-stabilizing graph linearization
with untrusted advice, April 2025), was retrieved in full because its title is the closest textual
match to "self-stabilizing," "linearization," and "overlay" found anywhere in this search; its
full text confirms it does not bear on this problem, recorded below. The most recent publication
found that measures a capacity-misreporting defense of any kind is `SHENG-NDSS-24` (NDSS 2024);
the most recent survey checked and found silent on this specific mechanism is `PATEL-ARXIV-25`
(September 2025).

## The mechanism HSkip+ leaves undefended

`FELDMANN-CSUR-21`, a survey of self-stabilizing overlay designs, states HSkip+ (Feldotto,
Scheideler, Graffi, P2P 2014) "reduces the stabilization time in practice and needs less work for
single join or leave events" relative to its predecessor Skip+, and that HSkip+ orders nodes by
bandwidth rather than by an arbitrary identifier so that "routing never transits a node with less
bandwidth than min of endpoints" — a property that concentrates routing load onto high-bandwidth
nodes by construction. The survey's own bibliography and text, read in full, contain no mention of
bandwidth or capacity heterogeneity anywhere except in the title of the one reference it cites for
HSkip+ itself; no self-stabilizing overlay design published in the survey's window is presented as
revisiting HSkip+'s bandwidth-ordering property. A node that reports a higher bandwidth than it
has moves toward the position routing concentrates onto — the position from which it can observe,
delay, or drop a disproportionate share of traffic transiting the structure, and the position other
nodes stop routing around rather than through. HSkip+'s own asynchronous self-stabilization proof
assumes the reported value is simply given; it contains no check of it. `PATEL-ARXIV-25`, a
September 2025 survey of secure peer-to-peer networks covering skip graphs, skip nets, rainbow
skip graphs, skip-webs, and structured-overlay Byzantine defenses (Fireflies, GUARD, Saad and
Saia's group-based multiparty computation), was read in full for any post-2021 treatment of
capacity or bandwidth as an ordering key subject to attack; the word "capacity" appears only once,
in an unrelated definition of what peers may share, and "bandwidth" appears four times, none in
connection with overlay position. The structured-overlay defenses this survey does cover — GUARD's
cryptographic-signature isolation of misbehaving skip-graph peers, Fireflies' accusation-based
peer removal, Saad and Saia's quarantine-on-detection multiparty protocol — all defend against a
peer that drops, corrupts, or forges *messages* after occupying a position; none checks whether
the *claim that earned the position in the first place* was true. Two surveys four years apart,
one exhaustively checking the self-stabilizing-overlay literature and one exhaustively checking the
secure-peer-to-peer-networks literature, independently find nothing.

## The closest published defenses bound a different quantity under assumptions this problem cannot take for granted

The nearest published work is the Tor relay-bandwidth-measurement literature, already the subject
of this registry's companion entry on verifying contributed bandwidth
(`registry/open-problems/verifiable-bandwidth.md`, item 8 of `BRIEF.md`'s open-problem list). That
literature answers a structurally different question. Tor selects a relay for a circuit slot with
*probability* proportional to its consensus weight, drawn independently for every circuit, over a
flat set of relays with no ordering relation between them; `JOHNSON-POPETS-17` (PeerFlow) and
`TRAUDT-ICDCS-21` (FlashFlow) bound how far a lie can inflate that one number. A capacity-ordered
structured overlay in the family HSkip+ belongs to instead assigns each node a fixed *position* in
a sorted or ranked structure — the position determines who a node's neighbors are, which lookups
route through it, and, per the survey passage quoted above, that routing never transits a lower-
bandwidth node than the path's endpoints. Gaming a selection probability wins more circuits over
time, in proportion to the inflation achieved; gaming a position can win a specific, structurally
privileged place — adjacency to specific other nodes, or a hub role a skip-graph-style structure's
own routing rule guarantees will not be bypassed — for as long as the position is held, independent
of how many further lookups happen to route through it. No paper in this search measures whether
PeerFlow's peer-measurement design, FlashFlow's active load test, or `SHENG-NDSS-24`'s (Proof of
Backhaul) trustfree challenger-consensus protocol, composed with a rank-ordered structure in place
of Tor's flat weighted selection, would bound an adversary's achievable position the way each
bounds an adversary's achievable selection-probability share; none of the three was designed,
tested, or discussed by its authors as an ordering input rather than a weighting input.

Each also carries an assumption a capacity-ordered peer-to-peer overlay with no privileged
membership cannot take for granted, independent of the selection-versus-position distinction.
PeerFlow's bound (a proven inflation factor of 4.52x at its worked parameters, against a measured
177x for Tor's deployed TorFlow pipeline) requires Directory Authorities to aggregate trimmed,
noised peer measurements, and the paper states directly that even "without any trusted relays" the
bound holds only if a single adversarial coalition's weight stays under a trim threshold
λ=0.256 — a precondition the paper states some other, unsupplied Sybil-resistance mechanism must
enforce. FlashFlow's tighter bound (1.33x) requires a dedicated measurement team funded to
3 Gbit/s per team in the deployed-scale simulation, run by the same Directory/Bandwidth Authority
infrastructure, with a stated requirement that a majority of both sets be honest. Proof of Backhaul
achieves its bound (sub-10% measurement error at up to 1000 Mbps, tolerating up to a proven
corrupted-challenger fraction β<1/3 with no verifier timer) without a fixed authority set, using
instead a coordinator that draws challengers at random from a pool — but the paper states this
selection must draw "a fresh, randomly drawn subset of challengers per measurement from a larger
active pool" so a corrupted prover cannot predict who will test it, without specifying how that
pool's membership is itself kept free of the same participant's Sybil identities. Every one of the
three bounds a lie once a witness or authority population already known to be adequately honest is
available; none of the three, nor any paper citing or extending them found in this search, builds
that witness population from bare open-membership peer-to-peer admission with no external
Sybil-resistance assumption.

## Measurement without any adversary already defeats the naive assumption

`JANSEN-PAM-21` measures that Tor's deployed self-report pipeline underestimates total network
capacity by at least 52.9%, with the error concentrated on exactly the relays an adversary
mimicking to gain position would want to resemble: relays in the top capacity quartile discovered a
median 32.5% more true capacity than they had reported, against 0.0% for the bottom two quartiles.
No adversary is assumed in this measurement — the paper's active speed-test experiment ran against
ordinary, non-adversarial relays. A capacity-ordered overlay that orders participants by
self-report inherits this bias before any participant lies at all: a naturally low-uptime,
high-capacity node reports itself into a lower position than its true capacity would place it, and
the paper states directly that "a relay can detect when it is being measured" — the same detection
capability that, applied deliberately rather than incidentally, is the misreporting attack this
problem asks about. No paper retrieved in this search measures the analogous quantity — position
error, not consensus-weight error — for a rank-ordered structure.

## What remains open

Nothing published places participants in a capacity-ordered overlay position — a skip-graph rank,
a sorted-line position, or an equivalent ordering key that determines routing adjacency and hub
status — from an untrusted self-report while measuring resistance to a participant that
misreports to move up. The nearest published work bounds a related but distinct quantity (Tor's
flat selection-probability weight) under assumptions (a trusted or already-Sybil-resistant witness
population) that a capacity-ordered overlay with fully open membership does not automatically
have, and none of it has been composed with, or evaluated against, a position-determining
structure. HSkip+'s own bandwidth-ordering property is stated by its authors to assume honest
reporting; `FELDMANN-CSUR-21` (2021) and `PATEL-ARXIV-25` (2025), read in full and independently,
each find no published design that revisits that assumption. Making the position worthless to hold
falsely — the third approach this problem's statement names alongside measurement and mechanism
design — appears in this corpus only as resource-burning Sybil resistance for *identity* count
(`PATEL-ARXIV-25` §2.3: computational puzzles, proof-of-space-time, proof-of-useful-work bounding
how many identities an adversary can hold) and as `GHOSH-HOTPETS-14`'s per-circuit proof of actual
goodput transfer (TorCoin, unimplemented beyond a preliminary simulation, verified only after the
fact and per-circuit rather than as a precondition for occupying a structural position); neither
mechanism family has been applied to make a false capacity claim costly specifically at the moment
it is used to select a position in an ordered structure.
