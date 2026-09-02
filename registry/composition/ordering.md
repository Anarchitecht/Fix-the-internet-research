# Composition check: ordering and consistency requirements

Assigned kind: which selections require a total order on operations, which require only a causal
order, which require no order, which supply or destroy each; which selections assume exactly-once
delivery, which tolerate duplicates, and which require a stable ordering under partition. Method:
every selection file in `registry/selections/` was read in full (see the parent task's read log);
the "requires from other components" and "what this selection requires" sections were the primary
source, cross-checked against each mechanism's own candidate-table row. `registry/conflicts/composition.md`
(agent X, no retrieval) was read first and is not repeated: its finding 2 (FROST's nonce-commitment
store against a CRDT-style replica) is the closest prior finding to this kind's subject matter and
is treated below as the seed for finding 1, not re-reported.

## Classification: what each selection requires of delivery order

**Requires a total order (a single agreed sequence, produced by consensus or an equivalent quorum),
across the whole network or a designated committee:**

- `incentives.md` — the selected storage-retrievability-proof payment mechanism requires "a
  blockchain or equivalent ledger that supplies per-challenge-window randomness the prover cannot
  bias in advance" and "executes the payment transaction automatically on a valid proof"
  (`VORICK-SIA-14`). A ledger of this kind is a total-order primitive: every participant must agree
  on one sequence of challenge windows and payment events, not merely on causal relationships
  between them.
- `key-transparency.md` — the selected Parakeet mechanism organizes every key-directory update into
  sequential epochs, each closed by a quorum certificate from 2f+1 of a 3f+1 witness committee
  (`MALVAI-NDSS-23`). This is a total order, scoped to one identity provider's directory and to a
  small, purpose-built committee rather than the whole network — the selection's own text states
  this distinction explicitly against Namecoin's network-wide mining majority.

**Requires a causal order (predecessors delivered before successors), no total order:**

- `group-encryption.md` — BeeKEM requires "Authenticated Causal Broadcast (ACB): causally-ordered,
  eventually-reliable, sender-authenticated delivery, with no total order required across the
  group" (`YEN-EPRINT-26`). The selection's own comparison against TreeKEM/MLS states this is the
  reason BeeKEM is chosen: MLS "requires a delivery mechanism that supplies one consistent order of
  protocol messages to every group member," a stronger and more centralizing requirement.
- `application-data.md` — the selected hash-identified Byzantine CRDT carries its own causal order
  in its predecessor-hash DAG, so the selection states it "need not supply causal-broadcast
  ordering, since the DAG's own predecessor hashes carry causal order" (`KLEPPMANN-ARXIV-20`). The
  transport underneath needs only reliable, eventually-complete delivery, not an ordering guarantee
  of its own; the rejected plain operation-based CmRDT candidate in the same table is the one that
  needed the transport itself to supply causal-order delivery (`SHAPIRO-EATCS-11`), and it was not
  selected for exactly this reason among others.

**Requires an order, but only a per-pair or per-writer one, not network-wide:**

- `application-data.md`'s signed append-only log (feeds) requires "reliable, ordered delivery
  between two connected stores, but not causal-broadcast delivery across the whole network"
  (`KERMARREC-DICG-20`). Each log is a single-writer chain with its own internal total order (hash
  links), reconciled pairwise; no cross-log or network-wide ordering is needed because a log has no
  cross-writer conflict to resolve by construction.

**Requires no order at all:**

- `content-location.md` (S/Kademlia lookups are independent request/response exchanges),
  `storage-encoding.md` and `repair.md` (immutable, content-addressed fragments, no update
  ordering), `naming.md` (GNS's per-zone signed records, resolved by comparing signatures and
  expiry fields, explicitly built without "a synchronized ledger" — the selection rejects Namecoin,
  Handshake, and ENS specifically for needing one), `indexing.md` (point queries against a random
  peer sample), `moderation.md` (each labeler's signed label and each deny-list check are
  independent per object), `nat-traversal.md` and `transport.md` (connection establishment, not
  operation ordering), and `ranking.md`'s selected default (gossip-based collaborative filtering
  merges click-log rows in any order it receives them, and the selection rejects the
  consensus-favouring family — EigenTrust, TrustRank, PeerTube's origin-instance count — precisely
  because each "places one designated party... in a position to determine or veto the ranking every
  downstream viewer sees identically," which the selection states is "the exact capture point the
  architecture's stated goal rules out").

## Classification: exactly-once versus duplicate-tolerant

- **Tolerates duplicates and reordering by design:** `application-data.md`'s CRDTs (merge is
  idempotent, commutative, and associative — `SHAPIRO-EATCS-11`); the signed-log reconciliation
  (comparing frontier indices, so a re-sent entry is simply already known); content-addressed media
  objects (re-fetching the same hash is a no-op); `forgery-resistance.md`'s per-write proof, where
  the same write-plus-proof pair reaching many peers through ordinary replication is not a
  violation, because the proof is bound to that write's own content address, not to a
  once-only-spendable resource (`BACK-HASHCASH-02`).
- **Requires exactly-once consumption:** `identity.md`/`key-recovery.md`'s FROST preprocessing
  nonces, already covered by `composition.md` finding 2; `forgery-resistance.md`'s spent-token
  store, which is exactly-once only per verifying peer's own local view, not network-wide — the
  selection does not claim otherwise, and no other selected component depends on a stronger
  guarantee than that. `reputation.md`'s flow-network link balances also require exactly-once
  consumption of capacity; this is not yet reported anywhere in `registry/conflicts/` and is
  developed as finding 1 below.

## Finding 1: Reputation's atomic hold/release on a shared link is a cross-replica invariant the selected mutable-state mechanism proves it cannot enforce

**Requirement.** `reputation.md` selects the capacity-bounded network-flow family (Bazaar, SumUp,
Ostra, accelerated by Canal). The selection requires "an atomic hold/release protocol at the point
of interaction: capacity along the flow path is reserved before the interaction proceeds and
resolved — released or permanently debited — once an outcome signal or a bounded timeout arrives"
(`POST-NSDI-11`, `MISLOVE-NSDI-08`, `TRAN-NSDI-09`), and states that if Canal's landmark
acceleration is used, the architecture additionally needs "a link-level locking mechanism so
concurrent path-stitching does not double-consume one link's capacity" (`VISWANATH-EUROSYS-12`).
The security bound this whole family delivers rests on an exact invariant: Ostra's credit
conservation holds "the sum of all credit balances is 0" after every operation (`MISLOVE-NSDI-08`),
and Bazaar's fraud bound is a bound on a link's cut capacity, valid only while that capacity is not
concurrently over-committed (`POST-NSDI-11`). A link balance that can be read and updated by both
of its two endpoints is exactly the "editable, potentially multi-writer state" `application-data.md`
defines as its own scope.

**What removes it.** `application-data.md` selects a hash-identified, Byzantine-tolerant
operation-based CRDT as the general mechanism for this class of state, and states the limit of that
mechanism precisely: a fault-tolerant Byzantine Eventually Consistent algorithm exists only for
operations that are invariant-confluent, and a non-negative-balance invariant is the paper's own
worked counterexample — two concurrent debits from one account can together break that invariant
even though each one alone would not (`KLEPPMANN-ARXIV-20`). The selection draws the general
conclusion itself: "any operation this design needs to enforce a cross-replica invariant outside
pure commuting/inflating updates (a global uniqueness constraint on a handle, an exactly-once
counter) needs a separate, explicitly bounded-adversary consensus sub-mechanism for that specific
operation, which this selection does not supply" (`KLEPPMANN-ARXIV-20`).

A reputation link balance is this exact class of invariant: "never go negative, never be spent
twice" is not commuting and not an inflation under the semilattice order a CRDT merge needs. If a
link's balance is stored the way the architecture stores every other piece of shared, multi-writer,
mutable state — the only mechanism this corpus's selections supply for that shape of data — then
two interactions drawing on the same link during a network partition can each locally observe
unconsumed capacity and both proceed, exceeding the link's true balance once the partition heals.
This defeats the specific property Bazaar and SumUp measure: fraud strictly bounded by cut value
(`POST-NSDI-11`), and Sybil resistance bounded to about one accepted vote per attack edge
(`TRAN-NSDI-09`) — both bounds assume the balance itself was never over-committed, which is
precisely what the atomic hold/release requirement exists to guarantee and what the selected CRDT
states it cannot supply for this kind of invariant.

**Confidence.** Derived reasoning, not a statement either paper makes about the other:
`reputation.md` does not name a storage mechanism for link-balance state, and `application-data.md`
does not name reputation as an example. The link is that no other selected component in this
registry supplies mutable, multi-writer state by any other mechanism, so a link balance has nowhere
else to live within the selections made. This is the same shape of gap `composition.md` finding 2
flagged and left open ("record which resource classes in the architecture need exactly-once
semantics as an open list, since FROST is unlikely to be the only one") — this is a second instance
of that list, not a restatement of the first.

**Resolution options.**

- Change a selection: store each link's balance as bilateral state between exactly its two
  endpoints — a two-party, jointly signed, monotonically increasing sequence, closer to a payment
  channel than to the general multi-writer CRDT — rather than routing it through the
  architecture-wide CRDT mechanism. This needs only agreement between two parties, not network-wide
  or committee-wide consensus, and neither `reputation.md` nor `application-data.md` evaluates it;
  it is a design not measured anywhere in this corpus.
- Accept a degraded property: keep the CRDT-backed link state and accept that Bazaar's and SumUp's
  measured bounds (strict cut-capacity fraud limit, ~1 accepted vote per attack edge) hold only
  between reconciliations, not continuously — a partition of unmeasured duration and unmeasured
  concurrent-replica count permits a transient over-commit of a link's capacity up to the number of
  replicas that independently observed it as unconsumed. No entry in either selection file measures
  how large this transient exposure would be for a given partition length or replica count; stating
  a number here would be a guess, not a finding.
- Record as an open problem: no entry in `reputation.md`, `application-data.md`, or elsewhere in
  this corpus evaluates a bilateral or committee-backed mechanism for exactly-once link-capacity
  consumption composed with either paper's own construction. Record it as unresolved alongside
  `composition.md` finding 2's open list of resource classes needing exactly-once semantics.

## Finding 2: Incentives' storage-payment mechanism requires a consensus ledger the rest of the selected architecture consistently declines to build

**Requirement.** `incentives.md` selects payment verified by a storage-retrievability proof (the
Sia/Shacham-Waters construction) for the storage-capacity resource. Its own "what this selection
requires" section states the dependency plainly: "a blockchain or equivalent ledger that supplies
per-challenge-window randomness the prover cannot bias in advance, and that executes the payment
transaction automatically on a valid proof while redirecting funds on a missed window — no
client-side verification action is needed" (`VORICK-SIA-14`). This is a request for a network-wide
total-order and consensus primitive: every participant must agree on the same sequence of challenge
windows and the same outcome of each one, which is what a blockchain supplies and what the
selection's own security argument for storage payment depends on (an attacker controlling half the
block-producing power can bias about half the challenges — `VORICK-SIA-14`).

**What removes it.** No other selection in this registry supplies a blockchain or an
equivalent network-wide consensus ledger, and four other components explicitly reject one for the
resource they each govern, each time citing the same underlying reason:

- `naming.md` rejects Namecoin because its consensus guarantee is conditional on holding a majority
  of a specific external resource, and an adversary "with more computational power than all other
  participants combined can construct an alternative valid timeline" (`WACHS-CANS-14`,
  characterizing `KALODNER-WEIS-15`'s measured Namecoin deployment).
- `key-transparency.md` rejects on-chain root-digest posting and full on-chain binding for the same
  reason, stating directly that a design whose goal is that identity cannot be captured by any
  company should not make key-substitution detection depend on which entity currently controls the
  largest share of one chain's block production (`KALODNER-WEIS-15`, `AMBATI-SACMAT-26`).
- `group-encryption.md` rejects DeCAF's blockchain-total-order variant because "a blockchain
  supplies consensus — a strictly stronger and more expensive coordination primitive" than the
  causal broadcast the selected mechanism needs (`ALWEN-SCN-24`).
- `ranking.md` rejects every consensus-favouring aggregation candidate (EigenTrust, TrustRank, the
  PeerTube origin-instance pattern) because each places one designated party in a position to
  determine the ranking every viewer sees identically, which the selection states is "the exact
  capture point the architecture's stated goal rules out" (`KAMVAR-WWW-03`, `GYONGYI-VLDB-04`,
  `POLINSKI-CCR-24`).

`incentives.md`'s own selection reasoning for the bandwidth resource makes the identical point from
the other direction: it rejects credit-balance mechanisms (KARMA, Dandelion) specifically because
each needs a mandatory third party in the exchange path, and it never proposes a ledger for
bandwidth at all. The storage-resource half of the same document then asks for exactly that
mandatory third party — a ledger every participant must agree on — for the other resource, with no
acknowledgment of the tension against its own reasoning two paragraphs earlier or against the four
other rejections above.

**Confidence.** High for the fact that no supplying component exists in this registry's selections;
derived, not a citation-backed claim by any single paper, for the observation that this is an
architecture-wide pattern rather than an isolated omission — the pattern is drawn from reading four
independent selection documents together, each written by a different pass of this project.

**Resolution options.**

- Change a selection: adopt Samsara's symmetric barter mechanism for storage (`COX-SOSP-03`),
  already in `incentives.md`'s own candidate table, which needs no ledger and no currency —
  accepting the concrete degradation `incentives.md` itself already states for it, that it "does
  not stop a node that promises to store data and then immediately discards it," because it
  certifies a claim's existence, not the original object's continued retrievability. Or keep the
  storage-retrievability proof as a verification signal only, and settle the resulting credit
  through the reciprocal-exchange mechanism already selected for bandwidth (`COHEN-IPTPS-03`,
  `LEVIN-SIGCOMM-08`) rather than an automatic ledger-triggered currency payment — giving up the
  "automatic, no-client-action" payment release `VORICK-SIA-14` describes.
- Accept a degraded property: keep the storage-retrievability-proof mechanism, but replace the
  ledger-supplied unbiased randomness with a source each verifier trusts individually (for example,
  a verifiable random function keyed by the challenger) and settle payment off-protocol rather than
  automatically. State explicitly that this gives up the "prover cannot bias the challenge in
  advance" property, and that no entry in this corpus measures what bias becomes possible once the
  ledger-backed randomness source is removed.
- Record as an open problem: no entry in this corpus evaluates the Sia/Shacham-Waters payment
  construction operating without a blockchain-class ledger in a partition-tolerant architecture with
  no other consensus component. Record this as unresolved, and record the four-component pattern
  above as evidence the tension is architectural, not an isolated choice in one component.

## What was checked and found to compose without conflict

- `application-data.md`'s pairwise reconciliation requirements (head-hash sets for the CRDT,
  frontier indices for feeds) need only reliable, ordered delivery between two already-connected
  peers, which every candidate in `transport.md` supplies as a stream-level guarantee (QUIC, TCP,
  and WebRTC's SCTP data channels are all reliable and ordered per connection); no cross-component
  gap was found here.
- `group-encryption.md`'s BeeKEM builds its own Authenticated Causal Broadcast from a hash-linked
  DAG plus signatures over a weaker reliable-broadcast substrate, citing the identical construction
  family `application-data.md` selects for editable multi-writer state
  (`KLEPPMANN-ARXIV-20`/`KLEPPMANN-PAPOC-22`, cited by `YEN-EPRINT-26` as BeeKEM's own source for
  this step). The two selections are independently built on the same causal-broadcast-over-signed-DAG
  primitive rather than on two different, potentially incompatible ones; no conflict was found, and
  this is worth recording as a positive composition rather than only an absence of one.
- `privacy-tiers.md`'s mix-network Message tier introduces per-message random delay and does not
  promise in-order delivery between successive messages. This composes without conflict with both
  `application-data.md`'s CRDTs (already tolerant of arbitrary delivery order by construction) and
  with `group-encryption.md`'s BeeKEM (whose ACB layer is built to buffer and reorder on top of an
  unordered reliable-broadcast substrate, not to require an already-ordered one); no entry in either
  selection states in-order network delivery as a precondition, so the mix tier's reordering removes
  nothing either mechanism needs.
- `ranking.md`'s gossip-based default and `naming.md`'s GNS delegation graph were checked against
  every other selection's stated ordering requirements; neither is depended on by anything that
  needs a stronger delivery guarantee than either supplies, since both are consumed only by
  components (indexing, the client itself) that already tolerate best-effort, unordered delivery.

## Notes on scope

Two ordering-shaped items surfaced during this pass but are not reported as findings here because
they are not composition conflicts between two selections. `repair.md`'s own text already flags an
unresolved disagreement with `storage-encoding.md` over churn assumptions (not an ordering
question). `capacity-ordering.md`'s HSkip+ recommendation already flags, in its own text, a tension
between its self-stabilization proof's static-membership assumption and a churn-tolerance claim it
cannot verify from any full-text entry in this corpus — this is an internal consistency question
about one candidate's own evidence, not a conflict between two selected components' ordering
requirements, so it is left to whichever pass covers within-document evidence gaps.
