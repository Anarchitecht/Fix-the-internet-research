# Architecture

One mechanism per component, each justified against every rejected candidate by an evidence key, then
checked against every other selection for a requirement it removes.

This document is written against `evidence.md`, which holds 407 papers read in full. A selection
whose justification cannot cite an evidence key is a guess and is labeled one at the point it is
made. No selection here carries that label; one — the capacity ordering within the transit tier —
labels half of itself a pick rather than a selection, because the overlay it recommends has no
full-text entry in this corpus.

## What the composition check found

Twenty-one requirements that one selection removes from another, against 28 component pairs checked
and clear. Ten have no published resolution and become open problems. Eight degrade a stated property
and the degradation is written down. Three await a changed selection.

**The single most connected conflict is forgery resistance.** Computational work priced per write is
selected because the corpus establishes every social-graph alternative reduces to community detection
around a trusted seed and fails where the honest population itself splits into communities. That
selection then collides with five others: the two-tier capacity structure, the local-index search
path, the message privacy ladder, relay-introduced connection establishment, and gossip-based
ranking. Each collision has the same shape — work priced per write bounds how fast an identity can
write, and bounds nothing about how many identities read, relay, rank, or occupy a position.

**Four selections independently reasoned their way out of a consensus ledger, and a fifth needs
one.** Naming rejects a mining-majority ledger, key transparency rejects on-chain root posting, group
encryption rejects a blockchain total order as stronger than the causal order it needs, and ranking
rejects consensus-favouring aggregation as the capture point the design exists to remove. Storage
payment then requires exactly such a ledger for unbiased challenge randomness and automatic
settlement, and no other selection supplies one. That four components refused the same dependency and
a fifth cannot proceed without it is architectural, not incidental.

**Illegal-content interdiction and private retrieval cannot both hold for the same fetch.** A serving
node must read the content identifier to test it against a deny list. Private information retrieval's
security property is that the serving node cannot determine which identifier was requested. No
construction in the corpus lets a server test a blinded query against a blocklist without learning
the query. The honest resolution is to disclose that interdiction does not cover a fetch made under
the private-retrieval tier.

## The selections

| Component | Selection |
|---|---|
| **application data** | Three mechanisms compose, one per data shape, and Operational Transformation is excluded in every topology this design permits. Editable, potentially multi-writer state (a post's text, a profile field, a folder tree) is represented as a has |
| **capacity ordering** | The selected mechanism excludes low-capacity peers from relay duty by structural role rather than by throttling their share of it: a minority of peers, selected by claimed capacity, forms a transit-carrying tier that every other peer connec |
| **content location** | S/Kademlia — Kademlia's XOR-metric routing-table structure and bucket-based state, with disjoint-path lookup and crypto-puzzle-derived node identifiers added — is selected. Against plain Kademlia: plain Kademlia has the strongest live-deplo |
| **forgery resistance** | Computational work priced per write, verified locally by every peer that relays or stores the write, with no identity system consulted at all. An entity's total achievable write rate across every identity it holds is bounded by the compute  |
| **group encryption** | BeeKEM is selected: a decentralized CGKA protocol whose members exchange protocol messages over authenticated causal broadcast (no group-wide total order) and whose key-refresh, member-add, and member-remove operations cost O(log n) in the  |
| **identity** | The identifier layer is the W3C Decentralized Identifier (DID) document (`W3C-DIDCORE-22`), which registers two purpose-separated keys rather than one. An `authentication` key is a t-of-n threshold Schnorr key produced and used with FROST ( |
| **incentives** | Two different mechanisms are selected, one per resource, because the corpus shows no single candidate covering both, and one entry in the corpus states the structural reason directly: Samsara's own authors, having built a placeholder-claim  |
| **indexing** | A client-local index of content the node has itself fetched, authored, or been shown answers a query first, at no network cost. A query the local index cannot answer is broadcast under the PAC (probably-approximately-correct) protocol to z  |
| **key recovery** | A standing (t,n) threshold BLS signing key (`BOLDYREVA-PKC-03`'s TGS construction) is distributed once, at identity-creation time, among guardians the user chooses from their own existing contacts in the same network — not a dedicated servi |
| **key transparency** | Compaction over a verifiable key directory with threshold-witness quorum-certificate signing (Parakeet, `MALVAI-NDSS-23`) is selected. Against the CONIKS-family chained-snapshot mechanisms audited by the key owner (CONIKS `MELARA-USENIXSEC- |
| **moderation** | For unwanted-but-lawful content, independently operated labeling services, each client subscribed individually, are selected over instance-level blocking and shared policy lists. For illegal content, an identifier deny list honored at retri |
| **naming** | Every human-readable label is bound to a self-certifying public key through private, per-zone delegation — GNS's mechanism [`WACHS-CANS-14`] — rather than through a synchronized naming ledger or a Domain Name System link. The raw self-certi |
| **nat traversal** | Select row B: a relay introduces two peers, each learns its own externally observed address, one peer attempts a direct dial if the other looks publicly reachable, and otherwise both peers time a simultaneous outbound connection attempt fro |
| **privacy tiers** | Three ladders, ordered by measured cost within each, one per action a person takes. **Fetch** (retrieving one object from one peer): direct connection, then a 3-hop onion circuit with no padding, then the circuit plus WTF-PAD, then the circ |
| **ranking** | Client-selected feed generators are selected as the governing pattern deciding who may compute a ranking, combined with gossip-based collaborative filtering specifically selected — not merely retained — as the mechanism computing whichever  |
| **repair** | Locally Repairable Codes, in the Azure/Xorbas construction — local-group exact reconstruction as the default repair path, with a full Reed-Solomon decode retained as the fallback when a group loses more members than its local parity covers. |
| **reputation** | The selected mechanism is the capacity-bounded, own-position network flow family: SumUp's ticket-distributed max-flow approximation (`TRAN-NSDI-09`), Bazaar's max-flow risk network (`POST-NSDI-11`), and Ostra's credit-network variant (`MISL |
| **storage encoding** | Plain Reed-Solomon (n,k) MDS erasure coding is selected as the storage-encoding mechanism, over whole-copy replication, over minimum-storage and minimum-bandwidth regenerating codes, over locally repairable codes, over convertible codes, an |
| **transport** | The selection is composed by participant class, because no single mechanism is reachable from every participant this architecture must connect. WebRTC data channels (SCTP over DTLS, negotiated by ICE with STUN and TURN fallback) carry every |

---

## Composition conflicts

### 1. A blockchain or equivalent network-wide consensus ledger supplying unbiased per-challenge-window randomness and automatic payment execution, for the storage-capacity payment mechanism.

**Required by** incentives.md (storage-retrievability-proof payment, Sia/Shacham-Waters construction) · **removed by** No selected component supplies this ledger; naming.md, key-transparency.md, group-encryption.md, and ranking.md each independently reject a blockchain/consensus dependency for their own resource, on the identical stated ground that it reintroduces a capture point or a coordination primitive stronger than the architecture otherwise needs. · **no-published-resolution-open-problem**

incentives.md's own selection text requires the ledger outright with no other component in the registry providing one; the absence is not silent but pointed, since four other selections explicitly reasoned their way out of the same dependency for their own resource (naming rejects Namecoin's mining-majority consensus; key-transparency rejects on-chain root posting and full on-chain binding; group-encryption rejects DeCAF's blockchain-total-order variant as a stronger primitive than the causal broadcast it needs; ranking rejects every consensus-favouring aggregation candidate as the exact capture point the architecture's stated goal rules out).

**Resolution.** Three options recorded in registry/composition/ordering.md: (1) change the selection to Samsara's ledger-free symmetric barter (accepting its stated degradation that it does not stop a node from discarding data it promised to store), or keep the retrievability proof as a verification signal settled through the already-selected reciprocal-exchange mechanism instead of automatic ledger payment; (2) accept a degraded property by substituting per-verifier-trusted randomness and off-protocol settlement, explicitly giving up the 'prover cannot bias the challenge' guarantee with its magnitude unmeasured; (3) record as an open problem, noting the four-component pattern as evidence the tension is architectural.

### 2. The retrieval-serving node must read the requested content identifier at the moment of serving, to test it against the illegal-content deny list, independent of any viewer's choices.

**Required by** moderation.md (identifier deny list honored at retrieval) · **removed by** privacy-tiers.md (single-server computational PIR, the default Query tier) · **no-published-resolution-open-problem**

PIR's security property is precisely that the answering peer cannot determine which index (content identifier) the client queried; privacy-tiers.md states this tier applies to retrieving an already-known object by content hash, not only to keyword search, so a server serving under this tier structurally cannot read the identifier moderation.md's deny-list check needs.

**Resolution.** No published construction in the corpus lets a server test a PIR-protected query against a blocklist without learning the query, so this is recorded as an open problem alongside registry/open-problems/illegal-content-removal.md. Operationally, the corpus supports disclosing to the user that illegal-content interdiction does not cover a fetch made under the Query privacy tier (an accepted degradation), the same pattern registry/conflicts/composition.md finding 3 already uses for a different pairing. Changing a selection instead would mean dropping single-server PIR as the default Query tier or excluding some content class from that tier, neither of which any entry in the corpus evaluates.

### 3. A capacity value used to admit peers to the transit tier and to order routing within it (HSkip+) must be verified, not merely self-declared, or a coalition can claim capacity it does not have to gain a structural relay position.

**Required by** capacity-ordering.md (two-tier structure + HSkip+ bandwidth-ordered routing) · **removed by** forgery-resistance.md (selected: computational work priced per write) · **no-published-resolution-open-problem**

forgery-resistance.md's selected mechanism prices writes only and states directly that 'no identity, key-transparency, or admission component is consulted by this mechanism at all'; joining the transit tier or being ranked within it is not a write, so nothing prices a false capacity claim. incentives.md's PropShare (the only other candidate honesty mechanism) governs bandwidth already flowing on an already-established transit-tier link, after admission — capacity-ordering.md's own text confirms this. Real-world evidence already shows the incentive runs toward misreporting: up to 30% of self-declared-low-bandwidth users hold significantly higher true bandwidth (SAROIU-MMCN-02), and a peer that honestly raises its claimed capacity sees its own load rise 303% while the same change adopted network-wide lowers it 14% (YANG-ICDE-03).

**Resolution.** capacity-ordering.md itself names the fork but does not resolve it: either make one of its own optional verification layers (PeerFlow, FlashFlow) a mandatory precondition for transit-tier admission (selection changes, with PeerFlow's ~27.7-hour measurement latency and per-authority overhead accepted), or explicitly disclose the resulting degradation to users (admission and rank can be gamed up to a verification layer's own trim threshold, e.g. PeerFlow's λ=0.256), or record it as an open problem since no entry measures real-deployment misreport rates.

### 4. PAC random-peer-sample search's accuracy proof assumes every node truthfully holds the same fixed document count (rho), uniformly at random; a high-capacity node splitting into many rho-sized virtual identities must be excluded by

**Required by** indexing.md (local-index-first + PAC network fallback) · **removed by** forgery-resistance.md (selected: computational work priced per write) · **no-published-resolution-open-problem**

Registering as an index-holding peer and answering queries against a claimed document share is not a write with a canonical target string forgery-resistance.md's mechanism binds to, so its per-write price is never consulted at admission time (same scope limit as finding 1). incentives.md prices storage payment and bandwidth between already-transacting peers, not the count of index-holding identities one entity registers. registry/conflicts/search.md section 5.3 already names this precondition and explicitly defers the question to 'whichever agent covers Sybil resistance' without answering it; no selection in this registry supplies that mechanism. The consequence is measured directly: at 10% malicious peers and z=2,000 queried nodes with no defense, RICHARDSON-SIGIR-14 measures a censorship attack moving a target's rank from 5 to 582 and a promotion attack moving an unrelated document into the top 10.

**Resolution.** Either adopt a mandatory per-identity admission cost scoped to index-registration specifically (no candidate in this corpus supplies one without a ledger, a pattern already declined elsewhere per registry/composition/ordering.md finding 2), or accept the degraded, corpus-stated bound: indexing.md's own skewness defense holds only to the lower of its own tolerance (40%) and its sampling primitive's published tolerance (Brahms, 20%), so 20% is the actual claimable bound absent a Sybil layer, or record the real adversarial fraction as unmeasured and therefore this choice as unmade.

### 5. The selected relay-assisted NAT-traversal mechanism assumes the relay enforces its own advertised duration/data limits and does not deliberately delay, correlate, or corrupt the coordination exchange.

**Required by** nat-traversal.md (relay-introduced, timing-synchronized hole punching, DCUtR/Circuit-v2) · **removed by** forgery-resistance.md (selected: computational work priced per write) / incentives.md · **no-published-resolution-open-problem**

Relaying a NAT-punch coordination exchange for another peer is a standing service, not a write with a canonical target string, so forgery-resistance.md's price is not consulted (same scope limit as findings 1-3). incentives.md prices bandwidth and storage between two already-transacting peers, not a relay forwarding a third party's setup traffic. nat-traversal.md's own text states the missing defense directly: 'an admission or Sybil-resistance layer for relay operators' is required and not supplied, and attributes part of the mechanism's own measured ~30% residual coordination-failure rate to exactly this exposure (TRAUTWEIN-ARXIV-26). The one candidate that verifies relay conduct economically (KEIZER-MOBIHOC-20, an independent second node comparing delivered hashes and timestamps) belongs to the rejected row C and itself requires 'an append-only public ledger' — the infrastructure four other selections in this registry decline to build for the same reason (registry/composition/ordering.md finding 2).

**Resolution.** Either adopt KEIZER-MOBIHOC-20's economically-verified relay design for the relay role specifically (accepting its ledger dependency and its measured ~$0.40-$0.60 client-side / ~$0.10-$0.20 relay-side per-session charge), or accept the degradation nat-traversal.md's own numbers already state — part of the measured ~30% coordination-failure rate is attributable to unverified relay conduct, so the mechanism's success rate is conditional on the currently reachable relay population's honesty, not purely a function of NAT topology — or record relay-operator misbehavior rates as unmeasured, matching nat-traversal.md's own stated gap for relay sustainability.

### 6. No single operator or company can capture the mechanism a client relies on to detect a substituted or maliciously issued key

**Required by** the architecture's stated design target (BRIEF §1: identity, indexing, and storage cannot be captured by any company) · **removed by** key-transparency.md (Parakeet witness-committee selection) · **no-published-resolution-open-problem**

The selection needs a fixed 3f+1-witness committee whose non-equivocation guarantee holds only while 2f+1 members are honest; key-transparency.md's own text states no witness-selection or rotation process resisting single-operator capture exists anywhere in the corpus, so whoever controls a majority of seats controls the mechanism undetected.

**Resolution.** Recorded as an open problem: key-transparency.md's own 'what the corpus does not settle' section states this directly, and no other selection in this corpus is evidenced as a witness-selection mechanism that could close the gap.

### 7. No party needs to hold the whole network's trust-linkage graph to answer one participant's question about a stranger

**Required by** the architecture's stated design target (BRIEF §1) · **removed by** reputation.md's selected flow-based mechanism (Bazaar/SumUp/Ostra, accelerated by Canal) · **no-published-resolution-open-problem**

The selection's own text states the computation needs a party able to compute over the full linkage graph on the assessor's behalf, or a Canal-style landmark index rebuilt continuously in the background; every measured cost figure this selection cites comes from exactly that whole-graph-holding configuration, while the one decentralized alternative it also lists (Ostra's route-discovery sketch) is validated only by a preliminary measurement, not end-to-end.

**Resolution.** Recorded as an open problem, matching reputation.md's own stated gap: no entry in this corpus measures this family's fully peer-executed, decentralized variant end-to-end.

### 8. A feed's identifier, and the mutable pointer reused for a CRDT's current head and for the newest object in an evolving media collection, must remain the same persistent signing key's public key for as long as followers and other o

**Required by** application-data.md (signed append-only log / feed / reused pointer mechanism, KERMARREC-DICG-20) · **removed by** identity.md + key-recovery.md (FROST device-set DKG on membership change; guardian-authorized non-reconstructive rotation to a new key PK′) · **no-published-resolution-open-problem**

identity.md states a device-set change implies 'a fresh distributed key generation round,' with no established technique for preserving the same public key across it; key-recovery.md's flow states explicitly 'the original private key is never regenerated at any point in this flow' — PK′ has no algebraic relation to the key it replaces, so the feed/pointer identifier changes with no stated migration step.

**Resolution.** No published resolution in the corpus. Change-a-selection direction: bind the feed identifier to the DID with an explicit update chain, the way identity.md's own rejected did:plc baseline already does ('each later document version is valid only if signed by the key authorized in the immediately preceding version') — untested for a signed log in this corpus. Degraded-property direction: every rotation orphans prior feeds/pointers unless old key material is retained indefinitely, defeating the purpose of loss recovery — magnitude unmeasured. Recorded here as an open problem since no entry proposes or measures either fix.

### 9. A GNS zone's entire published record set must remain reachable at the DHT position determined by that zone's own private key, for as long as those records and every other zone's delegation into them must resolve.

**Required by** naming.md (GNS per-zone delegation, WACHS-CANS-14) · **removed by** identity.md + key-recovery.md (device-set DKG; guardian-authorized rotation to PK′) · **no-published-resolution-open-problem**

naming.md states GNS's DHT lookup key is 'a scalar multiple of the zone's private key by a representation of the label' — an algebraic dependency, not merely a signature check — so a rotated key relocates every record to an unreachable DHT position with no republication step stated anywhere in naming.md or identity.md.

**Resolution.** No published resolution. Change-a-selection direction: indirect GNS's DHT position through the identity's DID (via an update chain analogous to did:plc) rather than deriving it directly from the raw private key — untested in this corpus. Degraded-property direction: accept that identity rotation silently orphans a zone's entire prior record set and every delegation into it, with the resulting exposure unmeasured. Recorded as an open problem, since neither naming.md's nor identity.md's own gap lists name this consequence.

### 10. A node's network identifier must remain the same, already-verified value for content-location.md's S/Kademlia (to preserve accumulated routing-table bucket position and the puzzle-derived Sybil cost) and for capacity-ordering.md's

**Required by** content-location.md (S/Kademlia) and capacity-ordering.md (HSkip+, FELDMANN-CSUR-21) · **removed by** identity.md (the public key each node's identifier is stated to derive from, subject to device-set DKG rotation) + key-recovery.md · **no-published-resolution-open-problem**

Both selections derive the node identifier from an identity-supplied public key; a rotation event (ordinary device-set change or key-recovery.md's PK′ flow) presents a new identifier to every peer holding the old one in a routing table, discarding S/Kademlia's puzzle cost and bucket longevity and directly violating HSkip+'s stated never-re-checked precondition.

**Resolution.** No published resolution; reported at lower confidence than the other two instances because neither file states whether the DHT/routing 'node identifier' is scoped to the whole multi-device identity or to one participating device — that scoping question is itself unresolved in the corpus, and the finding's severity depends on which reading applies. Recorded as an open problem pending that clarification.

### 11. An atomic hold/release protocol per interaction plus a link-level locking mechanism, so that a shared link's bounded capacity in the reputation flow-network is never reserved twice at once; the security bound (fraud strictly bound

**Required by** reputation.md (Bazaar/SumUp/Ostra + Canal, capacity-bounded network-flow family) · **removed by** application-data.md (selected hash-identified Byzantine CRDT for editable multi-writer state) · **property-degrades-and-is-stated**

The selected CRDT's own convergence theorem proves no fault-tolerant algorithm exists for an invariant that is not invariant-confluent under Byzantine faults; a non-negative/never-double-spent balance is its own cited counterexample (two concurrent debits from one account can jointly violate the invariant even though each alone would not). A reputation link balance is multi-writer mutable state with no other supplying mechanism in this registry, so by default it has nowhere to live except this CRDT, which explicitly states it cannot enforce this class of invariant without a separate bounded-adversary consensus sub-mechanism it does not supply.

**Resolution.** Three options recorded in registry/composition/ordering.md: (1) change the design so link balances are bilateral two-party signed state (payment-channel-like) rather than routed through the general multi-writer CRDT; (2) accept that Bazaar/SumUp's exactness bounds hold only between reconciliations, with an unmeasured transient over-commit possible during a partition; (3) record as an open problem alongside composition.md finding 2's open list of resource classes needing exactly-once semantics.

### 12. The flow-computing party (a central service, a route-discovery layer, or a precomputed landmark index) must observe the full trust-linkage graph — who has transacted with or vouched for whom — to compute a bounded flow value betwe

**Required by** reputation.md (capacity-bounded network-flow trust metric: SumUp, Bazaar, Ostra, accelerated by Canal) · **removed by** privacy-tiers.md (cover-traffic mix network, the default Message tier) · **property-degrades-and-is-stated**

The Message tier's proven differential-privacy bound holds against any server on a message's path, including a server occupying the flow-computing role; when two participants form a real linkage (a vouch, a transaction) through this tier, the mix network hides the who-talked-to-whom fact from any observing server by design, so the flow-computing party cannot learn the edge exists.

**Resolution.** reputation.md's own selection text already names this exact requirement as a conflict to resolve rather than an open question, but does not resolve it against a specific privacy tier; this document completes that resolution as an accepted degradation: a linkage formed through a Message-tier-protected interaction contributes nothing to either participant's flow-based reputation value, so computed reputation undercounts real linkages in proportion to Message-tier adoption. The alternative of changing a selection — forcing every linkage-forming interaction to disclose its two endpoints to the flow-computing party regardless of chosen Message tier — is not specified by any mechanism in either selection file.

### 13. Both peers exchanging bandwidth must observe how much bandwidth a specific, stable neighbor identity sent in the prior round or rounds, so each can proportionally reciprocate to that same counterparty in the following round.

**Required by** incentives.md and capacity-ordering.md (proportional-share reciprocation rule, PropShare) · **removed by** privacy-tiers.md (3-hop onion circuit, the default Fetch tier) · **property-degrades-and-is-stated**

privacy-tiers.md lists the serving peer itself among the adversaries the onion-circuit tier defeats, hiding the requester's identity from the peer serving content; under this tier a requester's directly observed counterparty is an entry relay, not the peer that actually served the object, so neither side can attribute received bandwidth to a stable, recognizable counterparty across rounds.

**Resolution.** Recorded as an accepted degradation, since it is the reading both selection files' text supports without inventing an unstated mechanism: per-neighbor bandwidth reciprocation functions only for direct connections or for Fetch-tier padding defenses that still expose a stable serving-peer identity (WTF-PAD, Tamaraw), and a transfer routed through the onion-circuit tier contributes nothing to either side's reciprocation ledger, which should be disclosed to the user as outside the incentive mechanism's coverage. Changing a selection instead — settling bandwidth for anonymized transfers through the storage component's ledger-based payment rather than peer-observed reciprocity — is not evaluated by any entry in the corpus.

### 14. The Message privacy tier's proven differential-privacy bound holds only if at least one server on a message's path is honestly performing its mixing and noise-generation duties; an open, permissionless server population needs an a

**Required by** privacy-tiers.md (Message ladder: cover-traffic mix network, Karaoke default) · **removed by** forgery-resistance.md (selected: computational work priced per write) / incentives.md (storage and bandwidth pricing between transacting peers) · **property-degrades-and-is-stated**

Acting as a mix server is a standing service role, not a write with a content address the per-write price binds to, so forgery-resistance.md's mechanism is not consulted by a peer registering for that role (same scope limit as findings 1 and 2). incentives.md prices resources exchanged between two transacting peers, not a third party's conduct while mixing traffic on behalf of others who did not individually select it. privacy-tiers.md's own text states directly: 'no enforcement mechanism exists for the one-honest-server assumption against a fully open, permissionless server population... an identity or admission component that can vet or bond a small server-role subset is required before this tier can be offered with its proven guarantee intact' — and no such component is selected anywhere in this registry.

**Resolution.** privacy-tiers.md's own text already states the accepted degradation: disclose to a person selecting the Message tier that its proven bound is conditional on trusting the currently selected server-role operators, not unconditional against a fully open population. Changing the selection would mean layering a bonding requirement onto the mix-server role specifically, using forgery-resistance.md's rejected staked-deposit candidate as the nearest analog, which reintroduces the ledger dependency registry/composition/ordering.md finding 2 already documents as declined elsewhere in this architecture.

### 15. Gossip-based collaborative filtering, selected as the mechanism computing the default feed nearly every user experiences, requires that a peer's reported click/interaction log actually reflects real interactions; a validly signed 

**Required by** ranking.md (gossip-based collaborative filtering as the default-computing mechanism) · **removed by** forgery-resistance.md (selected: computational work priced per write) · **property-degrades-and-is-stated**

Reporting an interaction into a gossip stream is not a write forgery-resistance.md's per-write price was built to bind to (same scope limit as findings 1-4), and content-signing from the identity/naming component — which ranking.md does require and which is supplied elsewhere in this architecture — proves who sent a record, not that the interaction it reports occurred. ranking.md's own text states the corpus's nearest defense (GOLD-ARXIV-23's preference for metadata matches over click-history matches) is 'stated by its authors only to blunt, not stop' fabrication. The one measured stronger defense, a Data-Shapley marginal-contribution filter (GREGORIADIS-ARXIV-25), is not committed as ranking.md's default instantiation and carries its own stated cold-start gap: a newly joined node has no local click history to value incoming data against and is exposed to unfiltered poisoning until it accumulates one.

**Resolution.** Either commit to the Shapley-filtered instantiation as the mandatory default (accepting its cold-start exposure for every newly joined node), or accept the degradation ranking.md's own numbers already state: unfiltered, ranking 'converges towards a single set of rankings that it appears unable to escape from' once adversarial peers reach 75 of 100 (GOLD-ARXIV-23); filtered, Mean Reciprocal Rank holds at or above its local-only floor of 0.38 only below a 90% poisoned-neighbor share (GREGORIADIS-ARXIV-25) — or record as open, since no entry deploys this mechanism to real users and measures whether a poisoned default would be detected and abandoned, which ranking.md's own text already flags as an unanswered question for the pairing it selects.

### 16. No party needs to ingest the whole network's content stream to provide indexing, ranking, or moderation coverage

**Required by** the architecture's stated design target (BRIEF §1) · **removed by** moderation.md's labeler-aggregation service and ranking.md's feed-generator marketplace · **property-degrades-and-is-stated**

Both selections depend on subscribing to the full signed content-and-identity stream at roughly 30 gigabytes per day per subscriber; moderation.md states the only alternative to a centralizing aggregator is that same per-client cost and calls independent viability unsettled, while ranking.md requires the identical stream for any feed-generator operator and separately measures the hosting role concentrating at 85.86% on one platform.

**Resolution.** Accept a degraded property, stated precisely: full moderation-label coverage and full feed-generator comprehensiveness are, in practice, delivered by a small number of well-resourced aggregator or hosting operators rather than by every peer independently; a client can still bear the full per-client stream cost itself to avoid depending on any one of them, so the no-capture property is priced rather than lost.

### 17. No company can capture the mechanism that decides which content the network serves

**Required by** the architecture's stated design target (BRIEF §1) · **removed by** moderation.md's illegal-content mechanism (identifier deny list) · **property-degrades-and-is-stated**

The selection requires one maintaining organization to publish the denylist that each independently operated gateway voluntarily honors; its own measured deployment shows enforcement at roughly 100% on the maintaining organization's own gateways against roughly 18% elsewhere, evidence that the mechanism's actual reach is set by trust in that one organization's list, with no corpus-evidenced way to distribute or cross-check that curation authority.

**Resolution.** Accept a degraded property, stated precisely: illegal-content moderation depends on trust in whichever party or parties maintain the denylist, a distinct, legally-motivated exception to the no-capture goal — moderation.md itself already frames the mechanism as selected 'not because it works, but because it is the sole candidate measured.'

### 18. BeeKEM's security for a given group member depends on that member's continued good behavior after Add, with no live re-check against the identity layer; key-recovery.md's revocation is meant to take away a lost device's authority 

**Required by** group-encryption.md (BeeKEM) · **removed by** key-recovery.md (non-reconstructive rotation to PK′, designed for the case where a lost device's holder may still exist and act) · **property-degrades-and-is-stated**

group-encryption.md states BeeKEM 'performs no identity check on the added public key beyond what that external PKI already vouches for' at Add time; no entry states a step that reports a completed key-recovery.md rotation into every group the member already belongs to, so a lost-then-superseded device retains its original BeeKEM leaf secret and can keep issuing valid Update/Remove/decrypt operations inside groups it already joined — key-recovery.md's revocation has no reach into a group's own membership state.

**Resolution.** Change-a-selection direction: require periodic re-verification of each member's live identity-layer binding against key-transparency.md's Parakeet log, removing members whose binding predates an unrecognized rotation — unspecified and unmeasured in this corpus. Degraded-property direction (consistent with what BeeKEM's own selection already discloses): BeeKEM's threat model is stated as 'honest-but-partition-prone... not Byzantine,' and a lost device retaining live signing power is exactly this excluded case, so the gap is a specific, previously unstated instance of an already-acknowledged limitation — group-encryption.md's own requirements section should name it. No entry measures how quickly a group notices and issues a Remove for a lost device.

### 19. LRC local-group repair needs only r=3-6 fixed, named local-group members simultaneously reachable per repair event (vs. plain Reed-Solomon's much larger k, e.g. k=29 of n=80 in Storj's deployed configuration)

**Required by** repair.md (selected mechanism: Locally Repairable Codes) · **removed by** storage-encoding.md (selected mechanism: plain Reed-Solomon) · **unclassified**

Plain Reed-Solomon parities are computed from all data fragments and cannot be narrowed to a local subgroup (HUANG-ATC-12), so LRC's local-group repair path requires an encoding structure (fixed local parity groups, PAPAILIOPOULOS-TIT-14) that storage-encoding.md's selected plain-RS encoding does not have. If storage-encoding.md's selection governs how objects are actually encoded, repair.md's selected LRC repair mechanism cannot run on any object in the system, and repair reverts to needing k (29 of 80 in the one concrete cited deployment) reachable rather than r=3-6.

**Resolution.** Property degrades and is stated: if plain-RS stands, repair's real reachability requirement is k (29 of 80), not r (3-6), and RODRIGUES-IPTPS-05's own churn-regime finding (maintenance bandwidth 'unsustainable for home users') applies to ordinary repair. The alternative is changing storage-encoding.md's selection to an LRC-point base code, which is what repair.md's own comparison argues for but storage-encoding.md rejects on a separate, unresolved precondition (98%-single-chunk-failure applicability to volunteer churn). repair.md's own text names this disagreement as unresolved; this check supplies the concrete resulting reachability number.

### 20. A k-of-n (custodians) or t-of-n (guardians) reachable quorum is needed to authorize rotating which key(s) control a person's identity

**Required by** identity.md (Pedersen-VSS custodian quorum reconstructing the SPHINCS+ capabilityInvocation root) and key-recovery.md (standing threshold-BLS guardian quorum) · **removed by** each selection implicitly displaces the other's exclusivity: key-recovery.md states a valid guardian-threshold signature should be treated as 'authoritative proof of continuity for the identity' independent of identity.md's own capabilityInvocation key, while identity.md frames its custodian quorum as the mechanism that 'authorizes replacing which devices hold shares of the authentication key' · **unclassified**

Neither document names, cites, or reconciles the other's mechanism, threshold, or member population anywhere in its text (verified directly: neither file, nor 'guardian'/'custodian' terms specific to the other, appear in either). A deployer following both as written has two unreconciled reachable-quorum authorities over the same rotation event, drawn from different populations (deliberately chosen custodians vs. ordinary social contacts), with the compound identity-security bound set by whichever quorum is easier for an adversary to gather.

**Resolution.** No published resolution; recorded as an open problem. key-recovery.md's own stated reasoning against raw-reconstruction schemes ('whoever combines t shares has the secret easily computable at that moment', SHAMIR-CACM-79) applies equally to identity.md's own custodian mechanism, so the corpus's own arguments favor retiring identity.md's Pedersen-reconstruction custodian quorum in favor of key-recovery.md's non-reconstructing guardian TGS scheme if a single mechanism must be chosen — but no entry in the corpus measures or compares the two candidate reachable populations against each other, so this is stated as a direction, not a settled answer.

### 21. The Message ladder's mix-network privacy tier requires every user, active or idle, to generate cover traffic every round — a continuous-presence duty, not a bounded count — for its proven differential-privacy anonymity bound to ho

**Required by** privacy-tiers.md (selected mechanism: cover-traffic mix network, Karaoke default) · **removed by** capacity-ordering.md's own measured churn figure for the ordinary-participant (leaf) population its selected two-tier structure creates · **unclassified**

capacity-ordering.md cites real deployed connection-lifetime data showing the leaf population (the majority of participants under its own selected structure) averages 58 minutes online per session, only 1.5x less than the more stable transit tier's 93 minutes (LOO-IPTPS-04) — a session boundary roughly every hour, not a rare edge case. privacy-tiers.md's own text states that any suspension of a client's network activity 'collapses this tier's guarantee for that user during the suspended interval,' so the corpus's own measured session length for the relevant population means the continuous-presence precondition is broken by ordinary use, not merely by an exceptional one. transport.md's QUIC connection migration, the nearest available mitigation, succeeds for only 52%/78% (IPv4/IPv6) of servers (BUCHET-CCR-25) and does not itself sustain unbroken per-round cover traffic through a background or reconnection interval regardless.

**Resolution.** Property degrades and is stated: the mix-network tier's proven bound holds only while a session is continuously active; the corpus's own measured ordinary-session length (58 minutes average) falls well short of what most real usage spanning more than an hour requires, so real-world anonymity achieved is materially weaker than the proven bound for typical use. privacy-tiers.md should state this against the concrete figure rather than only its current general 'component must contend with separately' language. The magnitude of the resulting anonymity loss (as opposed to the fact that a loss occurs) is not measured anywhere in the corpus and remains an open gap.

---

## Per-component detail

Each selection's full candidate table, its comparison against every rejected candidate, what it
requires from the rest of the system, its measured cost, its failure condition, and what the corpus
does not settle, is in `registry/selections/`. The composition check's working, by kind of
requirement, is in `registry/composition/`.
