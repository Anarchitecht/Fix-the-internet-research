# Composition check: honesty and self-report

Assigned kind: which selections assume a participant reports something — a capacity, a storage or
content holding, a bandwidth contribution, a position in a graph, a time — truthfully, and whether
any other selected component verifies that report or prices a false one. Method: every selection
file in `registry/selections/` was read in full. Each file's own "Security assumption required" and
"What this selection requires from the rest of the system" sections were checked against
`forgery-resistance.md`'s and `incentives.md`'s selected mechanisms specifically, since those two
files are this corpus's own candidate answer to "what stops a participant from lying." Both were
read first. `registry/conflicts/composition.md` (agent X) and the sibling passes already filed in
this directory, `registry/composition/ordering.md` and `registry/composition/observability.md`,
were read before writing below; their findings are cited, not repeated.

## What forgery-resistance.md and incentives.md actually cover

`forgery-resistance.md` selects one mechanism, computational work priced per write, verified
locally by the peer that relays or stores that write. Its own text states the mechanism's scope
twice, in almost identical words: it "prices each write in a resource," and "no identity,
key-transparency, or admission component is consulted by this mechanism at all — this is the
resources-not-identity-count property itself." A claim that is not a write — a capacity figure
offered at admission, a count of items a peer says it holds, a report that a peer relayed traffic
correctly, an interaction a peer says happened — is outside what this mechanism prices, and the
document says so directly: "any per-identity quota or rate limit elsewhere in the architecture is a
separate mechanism this component neither supplies nor interferes with; the composition between the
two... is not addressed by anything in this corpus."

`incentives.md` selects two mechanisms, one per resource. For storage, a retrievability proof
(Sia/Shacham-Waters) answers "does this peer still hold the bytes" with a cryptographic challenge,
not a self-report — real coverage, in principle, of one specific self-report (storage held). For
bandwidth, PropShare answers "how much should I send this neighbor" from each peer's own direct
observation of what that neighbor already sent it — also not a self-report, since the input is
locally measured, not asserted by the other side. Neither mechanism is built to verify anything
other than the one resource it prices, and `capacity-ordering.md`'s own text states this precisely
for the bandwidth case: PropShare is "the within-tier allocation mechanism deciding how much
bandwidth flows on each already-established transit-tier link" — a rule for peers already admitted
to a role, not a check on the claim that got them admitted.

Five selections assume a self-report neither mechanism reaches. A sixth, already reported by
`registry/composition/ordering.md` finding 2, is cross-referenced rather than repeated: `incentives.md`'s
own storage-retrievability proof, the one mechanism in this corpus that does verify a self-report
(storage held) rather than merely pricing it, cannot be deployed as selected because it requires "a
blockchain or equivalent ledger" that no other selection supplies, and that three other selections
(`naming.md`, `key-transparency.md`, `forgery-resistance.md`'s own rejection of the Rate-Limiting
Nullifier candidate) explicitly decline to build for the identical reason. That finding is about
storage specifically; the five below are about capacity, content-share, service conduct, and
interaction reports, none of which `incentives.md`'s ledger-dependent proof was ever built to cover
even where a ledger existed.

## 1. Capacity-ordering's transit-tier admission runs on a self-declared bandwidth figure neither selected forgery-resistance mechanism prices

**Requirement.** `capacity-ordering.md` selects a two-tier structure — a minority of peers,
selected by claimed capacity, carry all relay traffic — with routing inside that tier ordered by
the same claimed value (HSkip+). The selection's own text states what this needs and does not have:
"A capacity value to sort or select by, at minimum a self-declared one; and — because nothing in
this selection defends that value against a false claim — either a Sybil-resistance mechanism from
the identity component keeping any single coalition's claimed aggregate capacity under whatever
coalition-weight threshold a verification layer requires..., or an explicit acceptance that
admission to the transit tier and rank within it can be gamed, recorded as an open risk rather than
assumed away." The same document cites a real population already gaming this axis: peers in a
deployed system under-report their own capacity to avoid attracting requests, with up to 30% of
self-declared-low-bandwidth users measured to hold significantly higher true bandwidth
(`SAROIU-MMCN-02`), and the selected structure's own cost model shows the incentive running the
same direction from the other side — a peer that unilaterally raises its own claimed capacity sees
its own load rise 303%, while the identical change adopted network-wide instead lowers that peer's
load 14% (`YANG-ICDE-03`).

**What removes it.** `forgery-resistance.md`'s selected mechanism prices writes; joining the transit
tier or being ranked within it is neither a write nor consumed by anything that mechanism checks, by
its own stated scope quoted above. `incentives.md`'s PropShare governs bandwidth already flowing on
an already-established transit-tier link, after admission, as `capacity-ordering.md` states in its
own words. Four verification layers exist in `capacity-ordering.md`'s own candidate table
(PeerFlow, FlashFlow, Proof of Backhaul, TorCoin) that could feed a truer capacity number into the
selected structure, and the document explicitly declines to select any of them as mandatory,
listing each only as an optional addition with its own further cost (a Directory-Authority-class
quorum for PeerFlow and FlashFlow, a coordinator able to draw a Sybil-free challenger subset for
Proof of Backhaul, an already-functioning assignment-server quorum for TorCoin).

**Confidence.** High. `capacity-ordering.md` states the gap in its own words; this finding adds
that the two mechanisms this corpus selects specifically to answer "what stops a lie" (
`forgery-resistance.md`, `incentives.md`) do not, on inspection of their own stated scope, reach
this particular lie.

**Resolution options.**
- Change the selection: adopt one of `capacity-ordering.md`'s own optional verification layers as a
  mandatory precondition for transit-tier admission, accepting whichever added infrastructure it
  needs (PeerFlow's aggregation quorum, at 119.6 bytes/second per-authority overhead and a median
  27.7-hour measurement latency; FlashFlow's ~2.84x standing measurer-bandwidth allowance) rather
  than leaving it optional.
- Accept a degraded property, stated precisely: transit-tier admission and routing rank are gamed by
  any coalition able to claim capacity it does not have, up to the point a verification layer's
  trim threshold would otherwise catch it (PeerFlow's own bound holds only below coalition weight
  λ=0.256); state this to the user as a property of the selected architecture rather than leaving it
  implicit.
- Record as open: no entry in this corpus measures what fraction of a real deployment's transit-tier
  population would misreport capacity absent a verification layer, so a designer cannot currently
  choose between the two options above on measured grounds.

## 2. PAC search's per-node document-share assumption has no selected Sybil defense, and the consequence is measured directly

**Requirement.** `indexing.md` selects local-index-first search with a probably-approximately-correct
random-peer-sample fallback (PAC). The mechanism's accuracy proof assumes "every node holding the
same fixed document count rho, uniformly at random," and the selection's own requirements section
states what this needs: "A Sybil-resistance or admission mechanism capping how many rho-sized
virtual nodes one physical high-capacity participant can register, because RICHARDSON-SIGIR-14's
accuracy analysis assumes uniform per-node document share and states virtual-node splitting 'must
be defended against as a Sybil attack using a mechanism outside the scope of this paper.'" This is
not a hypothetical exposure: at z=2,000 queried nodes and 10% malicious peers, with no defense
active, `RICHARDSON-SIGIR-14` measures a censorship attack moving a target document's rank from 5 to
582, and a promotion attack moving an unrelated document from rank 20,778 into the top 10.

`registry/conflicts/search.md` (agent X) already names this precondition and states directly that
"whether a selected Sybil-resistance mechanism supplies that defense is a question for whichever
agent covers Sybil resistance" — flagged, not resolved. This finding resolves it: no selection in
this registry supplies one.

**What removes it.** `forgery-resistance.md`'s selection prices writes. Registering as an
index-holding peer and answering queries against a claimed document share is not a write in that
mechanism's own sense — nothing is published, no per-write target string exists to bind a proof to
— so the mechanism's per-write compute cost is not consulted at admission time, by the same scope
statement quoted in the section above. `incentives.md` prices storage payment and bandwidth
exchange between two already-identified, already-transacting peers; it does not price or verify how
many index-holding identities one physical entity registers.

**Confidence.** High for the absence of a covering selection; the accuracy consequence is a direct
citation to a controlled experiment (`RICHARDSON-SIGIR-14`), not an inference.

**Resolution options.**
- Change the selection: adopt a mandatory per-identity admission cost for index-holding registration
  specifically. No candidate in this corpus supplies one without either a ledger (the pattern
  `registry/composition/ordering.md` finding 2 already documents as architecture-wide and declined
  elsewhere) or a resource-price mechanism scoped to registration rather than to writes, which
  `forgery-resistance.md` does not evaluate.
- Accept a degraded property, bounded by the corpus's own numbers: `indexing.md`'s selection already
  states the skewness-based ranking defense (`RICHARDSON-SIGIR-14`) holds to about 40% malicious
  peers, but rests on a random-sampling primitive (Brahms) whose own published tolerance is only
  20% — so the lower of the two, 20%, is the bound this architecture can actually claim absent a
  Sybil-resistance layer for index registration, and the ranking-manipulation consequence above
  applies below that bound.
- Record as open: `indexing.md`'s own "what the corpus does not settle" already states no entry
  quantifies the real adversarial fraction any deployment would face; that number is a precondition
  for choosing between the first two options, not merely a nicety.

## 3. The Message tier's one-honest-server requirement has no selected admission or bonding mechanism for the server role

**Requirement.** `privacy-tiers.md` selects a cover-traffic mix network under a proven
differential-privacy bound (Karaoke as the default instantiation) for the Message ladder. The
proven bound holds "provided at least one server on the message's path is honest and actually
performs its assigned mixing and noise-generation duties" (`VANDENHOOFF-SOSP-15`). The selection's
own requirements section states plainly what is missing: "No enforcement mechanism exists for the
one-honest-server assumption against a fully open, permissionless server population: a single
faulty entity can present an unbounded number of distinct identities absent a synchronized,
challenged admission process (`DOUCEUR-IPTPS-02`, Lemma 1/2)... An identity or admission component
that can vet or bond a small server-role subset is required before this tier can be offered with
its proven guarantee intact; absent that, the tier's stated adversary-defeated claim... should be
disclosed to the user as conditional on trusting the specific server operators selected, not
unconditional."

**What removes it.** The same scope limit applies a third time: acting as a mix server is a
standing service role, not a write, so `forgery-resistance.md`'s per-write price is not consulted
by a peer registering for that role. `incentives.md` prices storage and bandwidth exchanged between
two transacting peers, not a third party's conduct while relaying or mixing on behalf of two others
who never chose it individually. No Sybil-resistance or bonding mechanism for a server-role subset
is selected anywhere in this registry.

**Confidence.** High; the requirement and its own absence are both stated directly in
`privacy-tiers.md`'s text, not inferred.

**Resolution options.**
- Change the selection: layer a bonding or staked-admission requirement onto the mix-server role
  specifically, distinct from the message-content path itself, so a server cannot enter that role
  for free. No candidate in this corpus is evaluated in this specific role; `forgery-resistance.md`'s
  own rejected staked-deposit candidate (Rate-Limiting Nullifier) is the nearest analog and carries
  the same ledger dependency `registry/composition/ordering.md` finding 2 already documents as
  declined elsewhere in this architecture.
- Accept the degraded property `privacy-tiers.md` itself already names: state to a person selecting
  the Message tier that its proven bound is conditional on the honesty of whichever operators
  currently hold the server-role subset they are routed through, not unconditional against a fully
  open population — the resolution `privacy-tiers.md`'s own text already proposes.
- Record as open: no entry in this corpus measures what a bonding mechanism for this specific role
  would cost or how it would compose with the ledger-avoidance pattern above.

## 4. The selected NAT-traversal relay is assumed not to tamper, correlate, or exceed its advertised limits, with no admission layer for the relay role

**Requirement.** `nat-traversal.md` selects relay-introduced, timing-synchronized hole punching with
the relay retained as a fallback path (the DCUtR/Circuit-v2 pattern). Its own requirements section
states two participant-honesty assumptions the mechanism needs and does not itself enforce: "The
relay is assumed to enforce whatever duration/data limit it advertises rather than relaying
unboundedly — the specification's default is no limit unless the operator configures one... The
relay is assumed not to deliberately delay or corrupt the coordination exchange, since the timing
synchronization degrades under path asymmetry that a congested or adversarial relay can induce, and
TRAUTWEIN-ARXIV-26's residual ≈30% failure rate is partly attributed to exactly this." The same
section states the missing defense by naming what would have to supply it: "An admission or
Sybil-resistance layer for relay operators, since an unauthenticated relay population is exactly
the address-and-timing-correlation exposure TRAUTWEIN-ARXIV-26 and VYZOVITIS-SPECS-23 both state as
a property of this mechanism, not a flaw to be fixed within it."

**What removes it.** Relaying a NAT-punch coordination exchange for another peer is a standing
service, not a write with a canonical target string a per-write proof could bind to, so
`forgery-resistance.md`'s selected mechanism does not price it, by the same scope statement cited in
findings 1 through 3. `incentives.md` prices bandwidth and storage exchanged between two
already-transacting peers; a relay forwarding a third party's coordination packets during setup is
neither. The one candidate in `nat-traversal.md`'s own table that verifies relay conduct
economically — an independent second node comparing delivered hashes and timestamps
(`KEIZER-MOBIHOC-20`) — belongs to row C (relay-only, mandatory), which the selection rejects for an
unrelated reason (an 89% throughput reduction under a bandwidth-constrained relay path,
`DUARTE-ABAKOS-20`), and it requires "an append-only public ledger" — the same infrastructure
`registry/composition/ordering.md` finding 2 documents as declined by four other selections in this
registry for the identical reason.

**Confidence.** High; both the assumption and its absence of coverage are `nat-traversal.md`'s own
stated text, and the measured residual failure rate is directly cited to the mechanism's own primary
source.

**Resolution options.**
- Change the selection: adopt `KEIZER-MOBIHOC-20`'s economically-verified relay design (row C) for
  the relay role specifically, accepting its ledger dependency and its measured per-session charge
  (≈$0.40-$0.60 client-side, ≈$0.10-$0.20 relay-side at the paper's tested Ethereum gas prices) and
  reconciling it against the same ledger-avoidance pattern the other four selections in this
  registry follow.
- Accept a degraded property, bounded by the corpus's own number: `nat-traversal.md`'s selection
  already attributes part of its measured ≈30% residual coordination-failure rate to exactly this
  unverified-relay-conduct exposure; state that the mechanism's coordination success rate is
  conditional on trusting the currently reachable relay population, not purely a function of NAT
  topology.
- Record as open: no entry in this corpus measures relay-operator misbehavior rates for the
  unpaid, volunteer-run Circuit-v2 model this selection depends on — `nat-traversal.md`'s own "what
  the corpus does not settle" already states this for sustainability; the same absence applies to
  misbehavior.

## 5. Ranking's gossip-computed default trusts a self-reported interaction log; the one measured defense is optional and has a stated cold-start gap

**Requirement.** `ranking.md` selects gossip-based collaborative filtering, specifically, as the
mechanism computing the feed a client sees by default (client-selected feed generators remain the
governing pattern for who may compute a ranking at all, but the selection states the default itself
is what nearly every person actually experiences, citing that only 2.8% of 5,000,000 measured users
ever chose an alternative, `QUELLE-PLOSONE-25`). Every instance of this mechanism in the corpus runs
on a click log or interaction history one peer reports to its gossip neighbors and that neighbor
incorporates into its own ranking model, with no cryptographic check that a reported interaction
actually happened. The selection's own requirements section states this directly: "Content-signing
or provenance from the identity/naming component, since GOLD-ARXIV-23's own defense against
fabricated evidence — preferring metadata matches over click-history matches — is stated by its
authors only to blunt, not stop, an attack manufacturing spurious click-log entries." Content-signing
proves who sent a record, not that the interaction it reports occurred — a peer's own genuine key can
sign a fabricated click.

**What removes it.** `forgery-resistance.md`'s per-write price does not reach this either: reporting
"I clicked this" into a gossip stream is not a write with a content address of its own the mechanism
was built to price, and the selection's own text (quoted at the top of this document) states composing
a per-write price with any other quota is unaddressed by this corpus. `incentives.md` prices storage
and bandwidth, not the truth of an interaction claim. One candidate in `ranking.md`'s own table
narrows the exposure — a Data-Shapley marginal-contribution filter (`GREGORIADIS-ARXIV-25`) holding
Mean Reciprocal Rank flat against up to 50% poisoned peer data — but the selection does not commit to
this specific instantiation as the default, and the filter's own stated precondition is a gap of its
own: "every participating node must already hold a minimum local click history (3 clicklogs in the
tested configuration) before it can value incoming peer data at all... a newly joined node has no
such history and is exposed to unfiltered poisoning until it accumulates one, a cold-start gap this
candidate does not itself close."

**Confidence.** High for the absence of a covering mechanism; the degradation figures are directly
measured in the cited papers, not inferred.

**Resolution options.**
- Change the selection: commit to the Data-Shapley-filtered instantiation (`GREGORIADIS-ARXIV-25`) as
  the mandatory default rather than an optional variant, accepting its cold-start exposure for
  every newly joined node until that node accumulates the minimum local history the filter needs.
- Accept the degradation `ranking.md`'s own text already states in numbers: without the filter,
  ranking quality "converges towards a single set of rankings that it appears unable to escape from"
  once adversarial peers reach 75 of 100 in the tested configuration (`GOLD-ARXIV-23`); with the
  filter, Mean Reciprocal Rank stays at or above its local-only floor (0.38) only below a 90%
  poisoned-neighbor share (`GREGORIADIS-ARXIV-25`) — state one of these two bounds as the
  architecture's actual guarantee, rather than leaving the mechanism's default instantiation
  unspecified.
- Record as open: no entry in this corpus deploys gossip-based ranking to real, identifiable users
  and measures whether a poisoned default would be detected and abandoned the way `QUELLE-PLOSONE-25`
  measures for a company-operated default; `ranking.md`'s own text already states this is a guess if
  claimed either way.

## The pattern across findings 1, 3, and 4

Three separate domains — capacity-ordering's transit tier, the Message privacy tier's mix-server
role, and NAT-traversal's relay role — each select a mechanism that assigns a standing service role
to a self-selected participant, each state directly that the role carries an honesty assumption
neither `forgery-resistance.md` nor `incentives.md` reaches, and each name the same class of missing
component (an admission or Sybil-resistance layer scoped to the role, not to a write or a
transaction) without any selection in this registry supplying it. This is not three unrelated gaps;
it is one gap — this corpus's selected forgery-resistance mechanism prices content published, not a
role assumed — recurring at every point in the architecture where a participant volunteers to act on
behalf of others rather than to publish something of their own.

## Checked and found to compose without conflict

- `incentives.md`'s PropShare (bandwidth): the input is each peer's own direct observation of bytes
  already received from a neighbor, not a claim the neighbor asserts, so there is no unverified
  self-report on this specific axis — the mechanism does not need `forgery-resistance.md` to cover
  it. (`registry/composition/observability.md` finding 3 covers a different problem on the same
  mechanism: a Fetch-tier onion circuit hiding which peer served the content, breaking observation
  itself, not the honesty of what is observed.)
- `transport.md`'s WebRTC/ICE candidate-address exchange: STUN Binding responses are unauthenticated
  by protocol design, but the selection states its own defense directly — "a reported candidate
  address must be corroborated by an actual successful connectivity check, not trusted outright" —
  so the mechanism does not rely on the unverified claim by itself; a false address simply fails the
  connectivity check.
- `reputation.md`'s flow-based trust computation: an edge represents "linkages that cost something
  real to form," so self-rating through controlled identities is bounded by cut capacity rather than
  by a claim being verified after the fact (`TRAN-NSDI-09`, `LEVIN-USS-98`); this is a different
  design from an unverified self-report, and the selection's own comparison against EigenTrust and
  TrustRank states this distinction directly. (Whether a Message-tier privacy mechanism can hide a
  linkage from the party computing the flow is a separate, already-reported issue —
  `registry/composition/observability.md` finding 2.)
- `storage-encoding.md`'s and `repair.md`'s per-fragment content check: a substituted fragment is
  caught by a content hash bound to the object's own naming layer, satisfied by `application-data.md`'s
  content-addressed object selection — this composes correctly for fragment *correctness*.
  Fragment *possession over time* is the separate, already-reported gap
  (`registry/composition/ordering.md` finding 2): the one mechanism this corpus selects to verify
  possession (a retrievability proof) needs a ledger nothing else supplies.
- `content-location.md`'s S/Kademlia node-identifier puzzle: bounds the cost of minting a fresh node
  identity for the routing-table role specifically, using its own selected mechanism (a computational
  puzzle at join time), not by relying on `forgery-resistance.md`; the two are independent, both
  selected, and neither depends on the other, so this composes without conflict on the honesty axis.

## What this pass did not settle

No entry in this corpus states what fraction of a real deployment's population would exploit any of
the five uncovered self-reports above if left as specified; each finding's own selection file
already records this absence, and the resolution options above list the number that would be needed
to choose between them. Whether the pattern found in findings 1, 3, and 4 (a service role with no
selected admission cost) also applies to key-transparency's witness committee — `key-transparency.md`
states directly that "no description in this corpus of a witness-selection or witness-rotation
process that itself resists capture by a single operator" exists — was checked and left unreported
here as a sixth instance, because that gap is about *who selects the committee*, a governance
question `key-transparency.md`'s own text frames as distinct from a participant lying about a
measurable resource, and reporting it under this kind would stretch "honesty" past what the assigned
category asks for.
