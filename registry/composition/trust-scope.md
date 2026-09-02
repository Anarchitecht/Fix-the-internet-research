# Composition check: trust-scope

Assigned kind: which selections require a party the architecture is supposed to eliminate — a
pre-trusted seed set, a non-colluding-server pair, an index that must ingest the whole network, or
a role reachable only at a scale a well-funded operator reaches. Method: every file in
`registry/selections/` was read in full first. Each file's own "Security assumption required" and
"What this selection requires from the rest of the system" sections were checked against BRIEF
§1's stated target — identity, indexing, and storage that no company can capture — and against
BRIEF §9.2's instruction to test whether one selection destroys a precondition another needs.
`registry/composition/honesty.md`, `ordering.md`, `observability.md`, and `reachability.md` were
read before writing below; a finding already filed by one of those four is cross-referenced, not
repeated, even where the same underlying selection also raises a trust-scope question.

## What this check found overall

Most selections in this corpus were made with this exact question already in view. Several
selection documents state directly that they rejected a stronger-measured or cheaper candidate
because it needed a company-designated or majority-controlled party, and this pass confirms those
rejections hold up against the evidence each document cites. Four points remain where the mechanism
actually selected — not a rejected alternative — requires a party of exactly the kind BRIEF §1
targets, with no distributed substitute evidenced anywhere in this corpus.

## 1. Key transparency's witness committee has no selection or rotation process resisting capture by one operator

**Requirement.** No single operator or company can capture the mechanism a client relies on to
detect a substituted or maliciously issued key (BRIEF §1).

**What removes it.** `key-transparency.md` selects Parakeet: a fixed committee of 3f+1 witnesses
signs a quorum certificate each round, and the non-equivocation guarantee holds only while at least
2f+1 of that committee is honest (`MALVAI-NDSS-23`). The selection's own text states plainly that
"the composition/governance layer of the wider architecture must supply the process that selects
and rotates this committee's membership without letting one operator control 2f+1 of it," and its
own closing section states the corpus supplies no such process: no description of a
witness-selection or witness-rotation procedure resisting capture by one operator exists anywhere
in this corpus, for Parakeet or for any of the alternatives it was measured against. Whoever
currently controls a majority of committee seats controls, without detection, the mechanism the
identity component depends on to catch a substituted key.

**Confidence.** High. Both the requirement and its absence are stated directly in
`key-transparency.md`'s own text, not inferred. `registry/composition/honesty.md` finding 5's
closing note independently checked this same gap under a different assigned kind (self-report
honesty) and set it aside specifically because "that gap is about *who selects the committee*... a
governance question distinct from a participant lying about a measurable resource" — the question
this pass is assigned to answer.

**Resolution options.**
- Change the selection: adopt a witness-rotation rule drawn from another selected component (for
  example, reputation.md's flow-based trust value, or forgery-resistance.md's per-write compute
  price, used as an admission cost for a witness seat). No entry in this corpus evaluates either
  composition, so this option is unevidenced, not merely undecided.
- Accept a degraded property, stated precisely: key-transparency's non-equivocation guarantee holds
  only conditional on trusting whichever party currently controls witness-committee membership,
  not unconditionally against any company.
- Record as open: `key-transparency.md` already states this in its own "what the corpus does not
  settle" section. This pass records it as recorded, not newly discovered.

**Recorded as:** open problem.

## 2. Moderation's label-aggregation role and ranking's feed-generator marketplace both need a party that ingests the entire network stream

**Requirement.** No party needs to hold the whole network's content to provide indexing, ranking,
or moderation coverage (BRIEF §1's indexing clause, extended to these two components by their own
stated dependence on the same underlying stream).

**What removes it.** Both selections depend on subscribing to the full signed content-and-identity
stream measured in this corpus as roughly 30 gigabytes per day per subscriber (`BALDUF-IMC-24`).
`moderation.md` states this directly: the alternative to "the measured deployment's centralized
AppView" — a service that "subscribes to all known Labelers and needs to store all labels" — is
that same per-client bandwidth figure, and states its own authors' judgment that whether an
independently operated equivalent is viable "remains to be seen." `ranking.md` selects the
identical Firehose-subscription requirement for any party that wants to operate a feed generator
serving the whole network, at the same measured cost, and separately measures that operating this
role already concentrates: the top 3 hosting platforms serve 95.8% of all generators, one platform
alone serving 85.86% (`BALDUF-IMC-24`). The same structural role — a party that ingests everything
— is required twice, at a bandwidth figure ordinary participant hardware does not sustain
continuously.

**Confidence.** High for the requirement and its cost figure, both stated directly in the cited
entry; the claim that this concentrates in practice is a direct measurement (`BALDUF-IMC-24`), not
an inference.

**Resolution options.**
- Change the selection: neither document selects a decentralized aggregator as the default; a
  future pass could require every client to bear the full-stream cost directly rather than permit
  an aggregator role, but this is exactly the option both documents already flag as impractical for
  an ordinary participant.
- Accept a degraded property, stated precisely: full moderation-label coverage and full
  feed-generator comprehensiveness are, in practice, delivered by a small number of well-resourced
  aggregator or hosting operators, not by every peer independently. A client that wants to avoid
  depending on any one of them can still bear the full per-client stream cost itself and lose
  nothing but bandwidth, so the no-capture property is not lost outright — it is priced.
- Record as open: no entry in either selection document measures a bandwidth or storage cost for a
  non-centralizing aggregator alternative.

**Recorded as:** the second option — property degrades, and is stated precisely above, since an
uncaptured fallback path (full-stream client subscription) exists and is already named in both
source documents.

## 3. The illegal-content deny list requires one maintaining organization

**Requirement.** No company can capture the mechanism that decides which content the network
serves (BRIEF §1).

**What removes it.** `moderation.md` selects an identifier deny list for illegal content: a
maintaining organization publishes hashes of content subject to a takedown request, and each
independently operated retrieval gateway voluntarily checks incoming requests against that one
list before serving (`SOKOTO-USENIXSEC-24`). The selection's own measured evidence for this
mechanism is itself the clearest demonstration of the party it requires: enforcement measures at
roughly 100% on the maintaining organization's own gateways against roughly 18% on
CDN-operated ones, a gap that exists precisely because the mechanism's actual reach is set by which
gateways choose to trust that one organization's list, not by any property the protocol enforces.
No entry in `moderation.md`'s own corpus proposes or measures a way to distribute or cross-check
that curation authority across more than one party.

**Confidence.** High. The mechanism and its single-organization dependency are stated directly in
the selection's own candidate table and selection text, not inferred.

**Resolution options.**
- Change the selection: `moderation.md` states this is "the only mechanism this corpus evidences in
  live deployment" for illegal content, so no evidenced alternative exists to substitute without
  giving up illegal-content moderation entirely.
- Accept a degraded property, stated precisely: illegal-content moderation in this architecture
  depends on trust in whichever party or parties maintain the denylist — a distinct,
  legally-motivated exception to the identity/indexing/storage no-capture goal, not covered by it.
  `moderation.md` itself already frames the selection this way, stating the mechanism is chosen
  "not because it works, but because it is the sole candidate measured."
- Record as open: `moderation.md`'s own "what the corpus does not settle" section states directly
  that no entry evaluates whether a structurally binding, as opposed to voluntary, version of this
  mechanism is achievable at all for independently operated retrieval nodes.

**Recorded as:** the second option — the degradation is real, bounded to this one function
(illegal-content gating), and already named as a deliberate exception by the selection's own text.

## 4. Reputation's flow computation, at every measured cost figure this corpus cites, runs on a party that holds the whole linkage graph

**Requirement.** No party needs to hold the whole network's trust-linkage graph to answer one
participant's question about a stranger (BRIEF §1's indexing clause, applied to the graph a
flow-based reputation computation runs over).

**What removes it.** `reputation.md` selects a capacity-bounded network-flow computation (Bazaar,
SumUp, Ostra, accelerated by Canal). Its own text states what running that computation requires:
"either a party able to compute over the full linkage graph on the assessor's behalf (Bazaar's
design), a decentralized route-discovery layer (Ostra's own Bloom-filter-plus-landmark sketch), or
a Canal-style precomputed landmark index rebuilt continuously in the background — some component
must expose enough of the graph for a flow or approximate-flow computation to run"
(`POST-NSDI-11`, `MISLOVE-NSDI-08`, `VISWANATH-EUROSYS-12`). Every cost figure this selection cites
as evidence for its own viability — Bazaar's 8,874,521-item eBay-scale evaluation, Canal's
785x-2,329x speedup over exact max-flow — comes from that first configuration, a single machine
holding the whole graph, or from Canal's own single-machine, centrally computed landmark-index
background process. The one alternative that avoids this, Ostra's decentralized route-discovery
sketch, is validated in the cited paper only by a preliminary Bloom-filter-size measurement, not an
end-to-end deployment; `reputation.md`'s own text states directly that "no entry measures this
family's fully peer-executed, decentralized variant end-to-end."

**Confidence.** High. The requirement for a whole-graph-holding party is stated in the selection's
own words; the absence of a measured decentralized alternative is stated in the selection's own
"what the corpus does not settle" section, not inferred by this pass.

**Resolution options.**
- Change the selection: adopt Ostra's decentralized route-discovery sketch as the default instead
  of Bazaar or Canal. No entry in this corpus measures its cost or accuracy end-to-end, so this
  substitution trades an evidenced trust-scope violation for an unevidenced mechanism.
- Accept a degraded property, stated precisely: the reputation component's measured cost and
  accuracy figures hold only for a deployment in which some party — an operator, or a background
  process one operator runs — materializes the whole trust-linkage graph, contrary to the
  no-capture goal for that graph specifically.
- Record as open: no entry in this corpus measures a fully decentralized instantiation of this
  family at any cost or accuracy figure.

**Recorded as:** open problem, matching `reputation.md`'s own stated gap.

## Checked and found to comply with the architecture's own no-capture goal

- `identity.md` — rejects custodial key holding (the one production deployment measured,
  `did:plc`, "ended up with signing keys held custodially by the PDS operator," `KLEPPMANN-CONEXT-24`)
  in favor of a threshold key split across the identity holder's own devices; no company party is
  consulted for day-to-day signing.
- `naming.md` — rejects Namecoin's and Handshake's mining-majority trust and ENS's and `did:web`'s
  registrar/DNS/CA trust (`KALODNER-WEIS-15`, `HANDSHAKE-WP-18`, `XIA-IMC-22`, `BALDUF-IMC-24`), in
  favor of per-zone delegation with no registrar or naming-authority role at all.
- `content-location.md` — rejects Pastry's and Tapestry's certificate-authority-based secure
  variants specifically because a CA "reintroduces exactly the single-point-of-trust the rest of
  this architecture is designed to avoid," selecting a computational-puzzle identifier cost
  instead (`CASTRO-OSDI-02`, `ZHAO-JSAC-04`).
- `key-recovery.md` — selects guardians the user chooses from their own existing contacts over
  dedicated server operators (Pythia, PPSS) specifically to avoid a company-designated trust point,
  stating this choice is "made specifically to satisfy this architecture's stated requirement that
  no company be able to capture the network."
- `forgery-resistance.md` — rejects staked-deposit admission's dependency on "a globally ordered,
  smart-contract-capable ledger" (`TAHERIBOSHROOYEH-ARXIV-22`) in favor of per-write compute
  pricing that consults no identity, admission, or ledger party at all.
- `privacy-tiers.md` (Query ladder) — rejects multi-server private-information-retrieval as the
  default specifically because it "requires the client to address two independently operated,
  non-colluding database copies — a trust decision the client must make in advance and cannot
  verify cryptographically" (`CHOR-JACM-98`), selecting single-server computational PIR instead.
- `group-encryption.md` — rejects DeCAF's blockchain-consensus requirement, since "a blockchain
  supplies consensus — a strictly stronger and more expensive coordination primitive" than the
  causal broadcast the selected mechanism needs (`ALWEN-SCN-24`).

## The pattern across findings 1 through 4

Every rejection listed just above was made by explicitly weighing a trust-scope cost against a
measured or proven benefit and choosing against the party. Findings 1 through 4 are not cases where
that weighing was skipped; they are cases where every candidate this corpus measured for the
function in question — a witness quorum for key transparency, a full-stream aggregator for
moderation and ranking, a maintaining organization for illegal-content gating, a whole-graph holder
for reputation flow — carries the same party, so no rejection was available without abandoning the
function itself. Findings 2 and 3 both trace to the same underlying deployment
(`BALDUF-IMC-24`, `KLEPPMANN-CONEXT-24`'s AT Protocol measurement), which is this corpus's only
source of a live, network-wide, moderation-and-ranking-capable deployment; the trust-scope
questions this pass raises about that deployment's own aggregator and labeler roles are not
resolved by any independently measured alternative deployment anywhere in the corpus.

## What this pass did not settle

No entry in this corpus measures whether a decentralized substitute for any of the four parties
above — a rotated witness committee, a federated label/ranking aggregator, a multi-curator
denylist, or a peer-executed reputation-flow computation — reaches the cost or accuracy figures
this corpus cites for the centralized version. Each of the four selection documents already states
this gap in its own words; this pass adds only that the gap is the same kind of gap in each case,
and states that kind explicitly as a party the architecture's own design target singles out.
Whether any two of the four parties could be answered by one shared mechanism (for instance, a
single admission-and-rotation primitive serving both key-transparency's witness seats and
reputation's graph-holding role) is not evaluated by any entry in this corpus and is not evaluated
here.
