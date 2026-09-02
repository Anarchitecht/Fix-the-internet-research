# Composition check: stability over time

Assigned kind: which selections require an identifier, a key, a position in a routing structure, or
a replica lifetime to remain constant, and which other selection's own stated behavior changes that
same value. Method: every file in `registry/selections/` was read in full. `registry/conflicts/composition.md`
(agent X, no retrieval) was read first; none of its eight findings concerns identifier, key, or
position stability, so none is restated here. `registry/composition/ordering.md`, `reachability.md`,
`honesty.md`, and `observability.md` were read next; two of `reachability.md`'s findings (2 and 3)
touch identity-key rotation, but from a reachability angle — which quorum can be gathered, and for
how long a session stays connected — not from the angle this pass covers, which is what happens to a
value that some other component has already bound to the pre-rotation key. Neither of those findings
is restated here.

## Classification: what each selection binds to a persistent identifier or key, and what does not

**Identifier fixed by construction, with no rotation concept — content addressing:**
- `storage-encoding.md`, `repair.md`, `content-location.md`'s stored objects, and `moderation.md`'s
  deny-list entries are all keyed by the hash of the content itself. There is nothing to rotate: a
  changed object is a new object under a new hash, and `moderation.md`'s own text states the
  consequence directly — re-encoding the same bytes under an alternate identifier evades a hash-keyed
  block on 97.4% of tested identifiers (`SOKOTO-USENIXSEC-24`). This class is not examined further
  here, since immutability is the selection's own stated property, not a value another selection
  destroys.

**Identifier stated to persist across key rotation, by an explicit chaining mechanism:**
- `identity.md` selects the W3C DID as the identifier layer specifically because a DID persists while
  the keys named inside its document change: the rejected `did:plc` baseline candidate is described
  in the same file as a chain where "each later document version is valid only if signed by the key
  authorized in the immediately preceding version" (`KLEPPMANN-CONEXT-24`). `key-transparency.md`'s
  selected Parakeet mechanism is built to watch exactly this kind of update stream and certify
  non-equivocation across it (`MALVAI-NDSS-23`). Rotation is not a stability problem for either of
  these two selections; it is the condition each is designed to operate under.

**Position or identifier derived from, and requiring the continued availability of, one specific
rotatable private key:**
- `naming.md`'s GNS zone: the DHT storage location of every record a zone publishes is "a scalar
  multiple of the zone's private key by a representation of the label, hashed to form the DHT lookup
  key" (`WACHS-CANS-14`, stated in naming.md's own "what the corpus does not settle" §4), and "each
  zone's own key, not any external party, authorizes changes to that zone's records."
- `application-data.md`'s signed append-only log: "per feed writer, one persistent signing key whose
  corresponding public key serves as the log's identifier" (`KERMARREC-DICG-20`), and the identical
  primitive is reused, by the selection's own text, "as the pointer mechanism between the other two"
  — the mutable name that resolves to a CRDT's current operation-DAG head and to the newest object in
  an evolving media collection.
- `content-location.md`'s S/Kademlia: "an identity or key-issuance mechanism elsewhere in the system
  must produce the public key each node's identifier is derived from," with the added computational
  puzzle "not a substitute for that key's own provenance."
- `capacity-ordering.md`'s HSkip+ (the recommended internal routing layer for the transit tier):
  "node identifiers, and the capacity/bandwidth value used to order them, are assumed correct and
  uncorrupted at the start of the protocol and are only compared, stored, and transmitted, never
  independently checked" (`FELDMANN-CSUR-21`).

**Authorization state whose validity is checked once, at admission, and never re-checked against the
identity layer afterward:**
- `group-encryption.md`'s BeeKEM: "BeeKEM's own Add operation performs no identity check on the added
  public key beyond what that external PKI already vouches for" (stated in the selection's own "what
  this selection requires" section).

**No stability requirement found — checked and clear:**
- `key-transparency.md`'s Parakeet witnesses observe ordinary DID-document update rounds and are
  built to certify rotation events, not to assume their absence.
- `indexing.md`'s PAC search and `moderation.md`'s labeled-object identifiers key to content hashes
  or to a stable per-object identifier the naming component supplies, not to a labeler's or a
  querying peer's own rotatable signing key.
- `storage-encoding.md`/`repair.md`'s local-group placement (`PAPAILIOPOULOS-TIT-14`) fixes group
  *membership* against node churn, a question `repair.md` and `storage-encoding.md` already dispute
  between themselves (recorded in `repair.md`'s own text and in `composition/reachability.md` finding
  1); it does not depend on any participant's identity key remaining fixed, so it is not re-examined
  here.

## Finding 1: Identity-layer key rotation orphans every downstream value that was bound to the pre-rotation public key — three independent instances, none resolved by any entry in the corpus

**The requirement, stated once, general to all three instances.** `identity.md` selects a two-key
identity: a t-of-n threshold Schnorr (FROST) key for everyday signing, and a Pedersen-shared
SPHINCS+ key exercised only to authorize a rotation. Both keys are designed to *change*. For the
FROST key, the selection's own "what the corpus does not settle" section states that when the
device set changes, "a fresh distributed key generation round for the new device set is the implied
mechanism," and separately that "whether the selected everyday key can be refreshed against a slowly
rotating set of compromised devices, without a full re-share, is unmeasured" — meaning the only
mechanism the corpus actually establishes for a device-set change is a fresh DKG, which is not shown
anywhere in this corpus to reproduce the same public key. `key-recovery.md`'s guardian-authorized
recovery flow is explicit that it does not even try to preserve the old value: recovery "consists of
collecting t guardians' signature shares over one statement, 'the current key for this identity is
now PK′' ... The original private key is never regenerated at any point in this flow." PK′ is, by
this flow's own design, a new key with no algebraic relationship to the one it replaces.

**Instance A — `application-data.md`'s feed and mutable-pointer identifier.** A feed's identifier
*is* the persistent signing key's public key (`KERMARREC-DICG-20`), and the selection reuses this
exact primitive as the name that resolves to a CRDT's current head and to the newest object in an
evolving media collection. Every follower relationship, every reader's cached "current head" pointer,
and every other zone's or object's reference to that pointer is a reference to the pre-rotation
public key. Once identity.md's device-set DKG or key-recovery.md's guardian flow moves the
identity's operating key to a new value, nothing in `application-data.md`, `identity.md`, or
`key-recovery.md` states how a follower resolves the feed going forward, or how the CRDT head and
media-collection pointers that were published under the old log identifier get republished under the
new one. This is the single highest-consequence instance, because the selection's own text states
this one primitive is reused for three separate addressing roles at once.

**Instance B — `naming.md`'s GNS zone position.** Because GNS's DHT lookup key is a scalar multiple
of the zone's own private key, a rotated zone key does not merely invalidate a signature check — it
relocates every record the zone ever published to a different point in the DHT keyspace, one
reachable only by whoever holds the *new* key. Nothing in `naming.md`'s own text (its "what the corpus
does not settle" section lists eight open items, none of them this one) or in `identity.md` states a
republication or migration step for GNS records after an identity-layer rotation. Every other zone's
delegation into this zone — the mechanism `naming.md` calls "the exact private, per-zone delegation"
this whole component is selected for — points at the old public key and does not update itself.

**Instance C — `content-location.md`'s S/Kademlia and `capacity-ordering.md`'s HSkip+ node
identifier (lower confidence).** Both selections state that a node's identifier is derived from, and
must remain tied to, one public key the identity component supplies — S/Kademlia adds a
computational puzzle specifically to make minting a *new* identifier costly, and HSkip+'s own
security assumption is that the identifier is "assumed correct... at the start of the protocol" and
"never independently checked" again afterward. Neither selection file states explicitly whether the
"node" whose identifier this is scoped to the whole multi-device identity (identity.md's FROST group
key) or to one participating device; this ambiguity is not resolved anywhere in the corpus. Under
either reading, a node whose underlying key changes — through ordinary device-set DKG, or through the
identity's own key-recovery flow, if the two are the same key — presents a brand-new identifier to
every peer holding it in a routing table. For S/Kademlia this discards accumulated bucket position
(the property that makes long-lived nodes preferentially retained) and forces the puzzle to be
re-solved; for HSkip+ it is a direct violation of the paper's own stated precondition that the
identifier is checked once and trusted thereafter, since that check happened against a value the
node no longer holds. This instance is reported at lower confidence than A and B because the
node-versus-identity scoping question is not settled by either file's text.

**Resolution.** No entry in `identity.md`, `key-recovery.md`, `naming.md`, `application-data.md`,
`content-location.md`, or `capacity-ordering.md` proposes or measures a mechanism for any of these
three instances, so this is recorded as an open problem, with the same three options every conflict
in this registry is required to be offered against:

- *Change a selection.* Bind the feed identifier (Instance A) and the zone's DHT position (Instance
  B) to the identity's DID rather than to the raw signing key, and carry an explicit update chain the
  way `identity.md`'s own rejected `did:plc` baseline already does — "each later document version is
  valid only if signed by the key authorized in the immediately preceding version." This would let a
  follower or a delegating zone resolve through the chain to the current key rather than holding a
  now-orphaned public key directly. No entry in this corpus specifies or measures this construction
  for a signed log or for GNS specifically; it is a direction the corpus's own already-selected
  components suggest, not a tested design.
- *Accept a degraded property.* Keep the current bindings and accept that an identity rotation — a
  routine event, since `key-recovery.md` exists specifically because device loss is not rare — orphans
  every feed, CRDT-head pointer, media-collection pointer, and GNS zone record published before the
  rotation, unless the participant keeps the old key material available indefinitely purely to
  continue resolving old references, which defeats the point of a lost-device recovery mechanism. No
  entry in this corpus measures how often this would occur or what fraction of a participant's
  published history it would affect.
- *Record as open.* State plainly that identity-layer key rotation and every selection that binds an
  identifier or a DHT position to the raw operating key have not been checked against each other by
  any entry in this corpus, and that a builder combining them as specified today should expect data
  loss on every rotation until one of the above is resolved.

Evidence: `identity.md` (`KOMLO-SAC-20`, `KLEPPMANN-CONEXT-24`), `key-recovery.md`
(`BOLDYREVA-PKC-03`), `application-data.md` (`KERMARREC-DICG-20`), `naming.md` (`WACHS-CANS-14`),
`content-location.md` (S/Kademlia candidate row), `capacity-ordering.md` (`FELDMANN-CSUR-21`).

## Finding 2: BeeKEM checks a member's identity binding once, at Add time; key-recovery's revocation model has no way to reach a member already inside the group

**Requirement.** `group-encryption.md` selects BeeKEM, whose own text states plainly that "BeeKEM's
own Add operation performs no identity check on the added public key beyond what that external PKI
already vouches for, so any Sybil resistance, key-transparency, or key-recovery mechanism selected
for identity applies before a key reaches BeeKEM, not inside it." Once a member's public key is
inside the group's tree, the group's own security depends on that member's continued good behavior,
not on any live check against the identity layer — the selection states BeeKEM's threat model is
"honest-but-partition-prone... its proofs do not cover a Byzantine participant."

**What removes it.** `key-recovery.md`'s entire purpose is to let a participant's operating key change
after a device is lost, without any assumption that the lost device is destroyed or unreachable to an
attacker: guardians co-sign "the current key for this identity is now PK′," and the flow is designed
to work even though the old key's holder — a lost or stolen device — may still exist. Nothing in
`key-recovery.md`, `identity.md`, or `group-encryption.md` states a step where a completed identity
rotation is reported into every group a member already belongs to, or where BeeKEM re-verifies a
member's binding against the identity layer on any cadence after Add. A device that was valid at Add
time and is later lost, then superseded by `key-recovery.md`'s flow, retains its original BeeKEM leaf
secret and can continue to issue valid Update, Remove, and message-decryption operations inside every
group it was already a member of — group membership does not track identity-layer authority once
granted.

**Resolution.**

- *Change a selection.* Require every group member to periodically re-present a current, live
  identity-layer binding (checked against `key-transparency.md`'s Parakeet update log) and remove any
  member whose bound key predates a rotation event the group has not separately re-admitted. No entry
  in this corpus specifies or measures such a periodic-reverification step for BeeKEM.
- *Accept a degraded property, as the corpus already partly states.* BeeKEM's own selection already
  states its threat model excludes an actively malicious participant; a lost device that continues to
  act as a group member after the identity layer has moved past it is exactly this excluded case, so
  the degradation is consistent with a limitation the selection already discloses in general terms.
  The specific consequence — that `key-recovery.md`'s revocation has no effect inside a group a lost
  device was already a member of — is not stated by either file, and should be added to
  `group-encryption.md`'s own "what this selection requires from the rest of the system," which
  currently states BeeKEM assumes external identity checks apply "before a key reaches BeeKEM" with
  no corresponding statement about what happens after.
- *Record as open.* No entry in this corpus measures how long a group typically takes to notice and
  issue a Remove for a member whose device was lost, or whether the group's own human members are
  expected to learn of a `key-recovery.md` rotation through some channel neither file specifies.

Evidence: `group-encryption.md` (`YEN-EPRINT-26`), `key-recovery.md` (`BOLDYREVA-PKC-03`).

## Checked and found no conflict

- **Content-addressed immutability against in-place revision.** Every selection in this corpus that
  needs to revise a value over time — `naming.md`'s GNS records, `key-transparency.md`'s directory,
  reputation state — is built on a signed, mutable pointer or a signed directory entry, never on
  overwriting a content-addressed object in place; `application-data.md`'s own selection resolves this
  boundary internally by choosing a different one of its three mechanisms per data shape (a CRDT for
  editable state, a signed log for anything append-only, content addressing only for what is
  genuinely never edited after publication). No selection in this registry asks a content-addressed
  object to be revised at its own hash.
- **`storage-encoding.md`/`repair.md`'s local-group membership stability.** Fixed against node
  identity-key rotation specifically: group membership in the Locally Repairable Code construction is
  a placement decision over currently-reachable holders, keyed by which physical node holds a
  fragment, not by any participant's signing key. The unresolved disagreement between `repair.md` and
  `storage-encoding.md` over whether that membership survives volunteer-scale *churn* is a different
  question, already recorded in `composition/reachability.md` finding 1, and is not restated here.
- **`key-transparency.md`'s Parakeet against identity rotation.** Checked directly: the mechanism's
  entire function is to certify a stream of DID-document updates, which is exactly what a key
  rotation produces; rotation is the input the selection is built to consume, not a precondition it
  assumes absent.
- **`reputation.md`'s linkage-graph edges against identity rotation.** Considered and not reported as
  a finding: `reputation.md` does not state whether an edge is keyed to a participant's persistent DID
  or to the specific signing key active when the edge was formed, and neither `identity.md` nor
  `key-recovery.md` states which components consume the DID versus the raw key. Reporting a conflict
  here would require guessing an unstated binding, which this pass does not do; it is recorded as a
  genuinely open question rather than a finding.

## What this pass did not settle

Whether `content-location.md`'s and `capacity-ordering.md`'s "node identifier" (Finding 1, Instance C)
is scoped to `identity.md`'s whole multi-device identity or to one participating device is not stated
by any entry in this corpus, and the severity of that instance depends entirely on which reading is
correct. No entry in this corpus measures how often an ordinary participant's device set changes,
which would bound how often Finding 1's orphaning event actually occurs; `key-recovery.md`'s own
"what the corpus does not settle" already names this same absence for its own purposes ("no entry
anywhere in this corpus measures real guardian availability or response time... how many of a
person's chosen contacts remain reachable"), and it applies with equal force here. No entry in this
corpus specifies whether `reputation.md`'s linkage graph, `moderation.md`'s labeler accounts, or
`ranking.md`'s per-author history key to a DID or to a raw signing key, so whether those components
carry the same Finding-1 exposure is unresolved rather than cleared.
