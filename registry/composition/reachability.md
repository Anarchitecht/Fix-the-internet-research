# Composition check: reachability requirements

Assigned kind: which selections require a set of participants to be simultaneously reachable, for
what count and what duration, and whether the transport, mobile-participation, and churn figures
the corpus measures supply that. Method: every file in `registry/selections/` was read in full.
`registry/conflicts/composition.md` (agent X, no retrieval) was read first; its findings 4, 7, and 8
already cover reachability-shaped conflicts (RLN freshness against ordinary churn, IP-bound identity
against measured Carrier-Grade NAT sharing, and regenerating-code repair's simultaneous-connection
requirement against measured NAT-traversal success rates) and are not repeated here.
`registry/conflicts/storage.md` was also read; its own "Not found" section considered and rejected a
different pairing (`DIMAKIS-TIT-10`'s OMMDS against `RHEA-USENIXATC-04`'s churn-handling result), not
the one reported as finding 1 below.

## Classification: reachability requirements stated by each selection, as a count and a duration

**Fixed small group, must include specific named members, at repair time:**
- `repair.md` — Locally Repairable Codes: the other members of the fragment's local group, r=3 of 4
  (Azure (6,2,2)) up to r=6 of 7 (production (12,2,2)), reachable whenever that group loses a
  member (`HUANG-ATC-12`, `SATHIAMOORTHY-VLDB-13`). Duration: one repair operation, but repair
  operations recur at the churn rate itself, since departure is what triggers them.

**Threshold out of a larger set, any k will do, at read or repair time:**
- `storage-encoding.md` — plain Reed-Solomon: k of n fragment-holders, unspecified k/n in general but
  k=29 of n=80 in Storj's deployed configuration (`LI-IWQOS-23-STORJ`, cited in `repair.md`'s own
  candidate table). Duration: every read and every repair, for the life of the object.
- `content-location.md` — S/Kademlia: d≥2 (recommended 4-8) disjoint next-hop paths per lookup.
  Duration: one lookup.

**Fixed small group, specific named members, at a rare rotation or recovery event:**
- `identity.md` — k of n custodians (a set distinct from the participant's own devices, chosen at
  enrollment) reachable to reconstruct and immediately re-split the Pedersen-shared SPHINCS+ root
  seed (`PEDERSEN-CRYPTO-91`). Duration: one deliberate root-rotation event.
- `key-recovery.md` — t of n guardians (drawn from the participant's own existing network contacts)
  reachable and willing to compute a threshold-BLS signature share (`BOLDYREVA-PKC-03`). Duration:
  the recovery window following device loss — unscheduled, and by construction coincides with the
  participant's own worst-connectivity moment.
- `identity.md` (separately) — t of n of the participant's own devices reachable for ordinary FROST
  signing (`KOMLO-SAC-20`). Duration: every signing operation.

**Committee quorum, reachable continuously, every round of ongoing operation:**
- `key-transparency.md` — Parakeet: 2f+1 of a 3f+1 witness committee reachable and actively
  verifying every epoch, not merely at setup (`MALVAI-NDSS-23`). Duration: continuous, for the life
  of the identity directory.

**Continuous presence, not a count but a duty, for as long as any peer might reach a participant:**
- `privacy-tiers.md` — the Message ladder's mix-network tier: "every user, active or idle, must
  generate cover traffic every round," a requirement the selection's own text ties to continuous
  network presence, not a threshold count (`VANDENHOOFF-SOSP-15`, `PIOTROWSKA-USENIXSEC-17`).

**No simultaneous-reachability requirement (checked and clear):**
- `group-encryption.md` — BeeKEM is built for exactly the opposite property: partition-tolerant
  operation with no group-wide reachability precondition, healing once each member eventually
  reconnects and issues one update (`YEN-EPRINT-26`).
- `naming.md` — GNS resolution needs the current holder of each zone's own record reachable through
  the DHT, sequentially, not a simultaneous set.
- `nat-traversal.md` — row B's relay-plus-punch pattern needs only the two communicating peers and
  one relay, and degrades to a durable relayed session rather than failing outright on a punch
  miss (`TRAUTWEIN-ARXIV-26`).

## Finding 1: `repair.md`'s selected repair mechanism needs a structural feature `storage-encoding.md`'s selected encoding does not have, so its whole reachability advantage does not apply

`repair.md` selects Locally Repairable Codes (LRC) as the default repair path specifically because
LRC needs only its local group's r members (3 to 6, depending on parameters) simultaneously
reachable to repair one lost fragment, against plain Reed-Solomon's much larger k. The selection's
own arithmetic states the reason this matters for reachability: "at the Gnutella-trace availability
`BLAKE-HOTOS-03` measures (a≈0.38), a 5-member local group (Xorbas's r=5) has roughly two orders of
magnitude higher probability of being fully reachable at once than a k=10 reconstruction set."

`storage-encoding.md` selects plain Reed-Solomon as the base encoding for the same architecture,
after directly comparing LRC and rejecting it — not because LRC is unavailable, but on a separate,
already-flagged uncertainty (whether volunteer churn produces LRC's needed "over 98% single-chunk
failure" pattern). What `storage-encoding.md`'s rejection removes, as a structural fact both
documents' own cited evidence states, is the local-parity-group structure LRC's repair path is built
on: `HUANG-ATC-12` states plainly that plain Reed-Solomon parities "are each computed from all data
fragments and cannot narrow the read to a subgroup." LRC's r-member local-group repair is not an
optional optimization layered on top of any Reed-Solomon code; it requires the object to have been
encoded with local parity groups in the first place (`PAPAILIOPOULOS-TIT-14`; `repair.md`'s own
table: "Fixed, system-known local-group membership, with blocks placed and addressed by group").
Data encoded under `storage-encoding.md`'s selected plain-RS scheme carries no such grouping.

Consequence: if `storage-encoding.md`'s selection governs how objects are actually encoded, then
`repair.md`'s selected repair mechanism cannot run as specified, on any object in this architecture,
regardless of how favorable the local churn conditions are. Repair reverts to plain reconstruction,
needing k holders reachable — k=29 of n=80 in the one concrete deployed configuration either
document cites (`LI-IWQOS-23-STORJ`), not repair.md's own r=3-6 — and `storage-encoding.md`'s own
text states what that costs under the churn regime it identifies as applicable: `RODRIGUES-IPTPS-05`'s
Overnet-trace result, that the resulting maintenance bandwidth even after coding "is stated by the
authors themselves as unsustainable for home users." `repair.md`'s selection section names this
tension explicitly ("This selection disagrees with the storage-encoding component's own selection
of plain Reed-Solomon... Resolving the disagreement... is a composition-check question, not one
either component analysis can close alone") but does not state the concrete reachability number
(k=29, not r=3-6) that results if `storage-encoding.md`'s selection stands. This composition check
supplies that number.

**Resolution.** Property-degrades-and-is-stated: if `storage-encoding.md`'s plain-RS selection is
kept, `repair.md`'s selected LRC repair path is not available as written, and the actual reachability
requirement for repair is `storage-encoding.md`'s own k (29 of 80 in the one measured deployment),
not the r=3-6 figure `repair.md`'s selection section argues for. The alternative — changing
`storage-encoding.md`'s selection to an LRC-point base encoding so `repair.md`'s own selection
becomes realizable — is the option `repair.md`'s comparison argues for, but `storage-encoding.md`
rejects it on a separate, unresolved precondition (the 98%-single-chunk-failure assumption's
applicability to volunteer churn), so this composition check does not adjudicate which selection
should change; it states that one of the two must, since as written they do not compose.

Evidence: `HUANG-ATC-12`, `SATHIAMOORTHY-VLDB-13`, `PAPAILIOPOULOS-TIT-14`, `LI-IWQOS-23-STORJ`,
`BLAKE-HOTOS-03`, `RODRIGUES-IPTPS-05`.

## Finding 2: `identity.md` and `key-recovery.md` each select a separate reachable-quorum authority over the same rotation event, and neither document names the other

`identity.md` selects a Pedersen-verifiable-secret-sharing custodian quorum (k of n custodians,
chosen at enrollment, distinct from the participant's own devices) as the mechanism that
reconstructs the identity's SPHINCS+ root seed to authorize a rotation. The selection states this
key "authorizes replacing which devices hold shares of the authentication key" — its own text
frames this as the identity's rotation authority.

`key-recovery.md` independently selects a standing threshold-BLS (TGS) guardian quorum (t of n
guardians, drawn from the participant's own existing network contacts, not the same population
`identity.md` names) to co-sign a "the current key for this identity is now PK′" statement.
`key-recovery.md`'s own text states what the rest of the system should do with that signature: "The
key-transparency component accepts a valid t-of-n guardian-threshold signature over a 'rotate to
PK′' statement as authoritative proof of continuity for the identity" — proof of continuity for the
identity in general, not proof that `identity.md`'s own capabilityInvocation key participated at
all.

Each document treats its own reachable quorum as the answer to identity-key rotation; neither
mentions the other's mechanism, its threshold, or its member population anywhere in its text
(checked directly: neither file's name, nor "guardian," nor "custodian," appears in the other). Two
consequences follow specifically for reachability. First, a deployer has two different, unreconciled
answers to "which k-or-t simultaneously-reachable people authorize a rotation of this identity,"
drawn from two different populations (custodians deliberately chosen for the role, versus ordinary
social contacts) with no stated precedence between them. Second, if both are honored as each
document's own text implies, the identity's effective rotation-security is bounded by whichever
quorum an adversary finds easier to gather, not by the harder of the two — a compound consequence
neither document's own "what the corpus does not settle" section names, because each was written as
if it were the sole mechanism.

**Resolution.** No published resolution; recorded as an open problem. `key-recovery.md`'s own stated
reasoning against raw-reconstruction schemes — "whoever combines t shares has the secret 'easily
computable' at that moment" (`SHAMIR-CACM-79`) — applies with equal force to `identity.md`'s own
custodian mechanism, which is exactly this pattern, so the corpus's own arguments point toward
retiring `identity.md`'s Pedersen-reconstruction custodian quorum in favor of `key-recovery.md`'s
non-reconstructing guardian TGS scheme if a single rotation-authority mechanism must be chosen. But
no entry in the corpus measures or compares the two candidate reachable populations (custodians
versus ordinary contacts) against each other for actual availability, so this composition check
states the direction the corpus's own reasoning favors without treating it as settled.

Evidence: `identity.md` (`PEDERSEN-CRYPTO-91`, `HULSING-CCS-19`), `key-recovery.md`
(`BOLDYREVA-PKC-03`, `SHAMIR-CACM-79`).

## Finding 3: The mix-network privacy tier's continuous-presence requirement is broken by the corpus's own measured ordinary-participant session length

`privacy-tiers.md` selects a cover-traffic mix network (Karaoke as the default instantiation) for
the Message ladder, and states the precondition its proven differential-privacy bound depends on
directly: "every user, active or idle, must generate cover traffic every round" (`VANDENHOOFF-SOSP-15`).
The same selection's own text already anticipates a gap here in general terms — "any component that
suspends a client's network activity to save power or bandwidth... collapses this tier's guarantee
for that user during the suspended interval" — without citing a figure for how often, or for how
long, an ordinary participant's connection is actually suspended.

`capacity-ordering.md` supplies that figure, for the population most relevant here: ordinary,
non-relay participants, which is what `capacity-ordering.md`'s own selected two-tier structure calls
the leaf population — the majority of any deployment under that selection, since the transit tier is
by design a capacity-selected minority. Its own live-deployment citation states real measured
connection lifetimes of 93 minutes average for the more stable transit tier against 58 minutes
average for the leaf population, "a 1.5x difference, not an order of magnitude" (`LOO-IPTPS-04`).

Consequence: the corpus's own measured figure for the population the mix-network tier would actually
be used by shows a session boundary roughly every hour, not as a rare edge case but as the typical
case. `privacy-tiers.md`'s own stated failure condition — that a suspended interval "collapses this
tier's guarantee for that user during the suspended interval" — therefore applies to ordinary use
of the tier for any session longer than about an hour, which is the median case in the corpus's own
comparable measured population, not an exception. `transport.md`'s own QUIC-migration figures do not
close this gap: connection migration, the one measured mechanism in the corpus for surviving an
address or session change without a fresh handshake, succeeds for only 52% of IPv4 and 78% of IPv6
QUIC servers that had already completed a handshake (`BUCHET-CCR-25`, cited in `transport.md`), and
in any case a migrated QUIC connection is not the same event as sustaining unbroken per-round cover
traffic through an app-background or reconnection interval.

**Resolution.** Property-degrades-and-is-stated: the mix-network tier's proven bound holds only
while a client's session is continuously active; the corpus's own measured session-length figure for
the ordinary-participant population (58 minutes average, `LOO-IPTPS-04`) means that bound is not
achieved for any real usage pattern spanning much more than an hour, which is a materially weaker
real-world guarantee than the proven one, and `privacy-tiers.md` should state this against a
concrete figure rather than only the general "component must contend with separately" language it
currently carries. No entry in the corpus measures actual anonymity achieved by a live mix-network
deployment against a churn population resembling this one, so the magnitude of the resulting
anonymity loss — as opposed to the fact that a loss occurs — remains an open measurement gap.

Evidence: `privacy-tiers.md` (`VANDENHOOFF-SOSP-15`, `PIOTROWSKA-USENIXSEC-17`), `capacity-ordering.md`
(`LOO-IPTPS-04`), `transport.md` (`BUCHET-CCR-25`).

## Checked and found no conflict

`group-encryption.md`'s BeeKEM selection was checked against every transport and churn figure in the
corpus and carries no simultaneous-reachability precondition to conflict with; it is designed
against exactly the opposite assumption, and its own measured partition-recovery cost (`YEN-EPRINT-26`
Fig. 5) rises and plateaus with the count of members who eventually return, never requiring them
back at once.

`content-location.md`'s S/Kademlia disjoint-path requirement (d≥2, recommended 4-8) was checked
against `nat-traversal.md`'s selected relay-fallback mechanism: because a relayed connection succeeds
for any two online peers regardless of NAT type, and `nat-traversal.md`'s own selection keeps the
relay as a durable fallback rather than a failure, S/Kademlia's per-lookup path count is not
undermined by the corpus's measured NAT-traversal success rates the way finding 8 in
`registry/conflicts/composition.md` already shows for the regenerating-code repair candidate
`repair.md` itself rejects.

`key-recovery.md`'s guardian threshold-BLS signing was checked against the corpus's transport
selections for a simultaneity requirement and found to need none beyond eventual reachability within
the recovery window: `BOLDYREVA-PKC-03` states signing "does not require interaction," so guardians
publish shares independently rather than needing to be online at the same moment as each other.
(Whether guardians are reachable at all within any bounded window is a separate, already-self-flagged
gap in `key-recovery.md`'s own "what the corpus does not settle," not a destroyed precondition from
another selection, and is not re-reported here.)

## Not pursued

A possible pairing between `key-transparency.md`'s witness-committee reachability requirement (2f+1
of 3f+1, every round, continuously) and `capacity-ordering.md`'s measured transit-tier churn (93
minutes average connection lifetime, `LOO-IPTPS-04`) was considered and dropped: no entry in either
selection states that the witness committee is drawn from, hosted by, or in any way sourced from
`capacity-ordering.md`'s transit tier. Making that connection would require guessing an
architectural link neither document states, which this pass does not do.
