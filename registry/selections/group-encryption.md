## Group Encryption: A decentralized ratchet tree over causal broadcast (BeeKEM) reaches the same logarithmic per-update cost as a centralized ratchet tree, without a total-order delivery service, at the price of an unproved causal-broadcast substrate and a conjectured, not proved, tension between partition recovery and forward secrecy

Continuous group key agreement (CGKA) is the protocol family that lets a set of members holding one
shared symmetric group key add members, remove members, and periodically refresh that key, so that
the key stays useless to anyone who is not a current member (forward secrecy, FS: past keys stay
secret after a later compromise) and recovers its usefulness once a compromised member takes a
further protocol step (post-compromise security, PCS). Every candidate below is a way to run CGKA;
they differ in what ordering guarantee they demand from the layer that delivers protocol messages
between members, and in what that demand costs in bandwidth and proof strength.

### Candidates

| Mechanism | Measured cost, as a function of group size n | Security assumption | Failure condition | Requires from other components | Evidence |
|---|---|---|---|---|---|
| TreeKEM / MLS ratchet tree, sequential operation | O(log n) hashes and public-key operations, sender and recipient, per Update/Add/Remove | PRG + IND-CPA public-key encryption (PKE); proof holds only against a non-adaptive adversary, one that commits to every corruption before the protocol runs | Adaptive-adversary security is only sketched; the reduction needs block-cipher keys of order n·log(n) bits to be meaningful, which the paper's own authors call "practically speaking, unrealistic" | A delivery mechanism supplying one consistent per-session total order of protocol messages to every member; an external PKI supplying initial member keys, with peer long-term-key authentication left as an unmodeled out-of-band step | BHARGAVAN-HAL-18, ALWEN-CRYPTO-20 |
| Same construction, under real concurrent proposal/commit load | Expected commit cost Ω(n·log₂(1+P/(P+C))), P proposals and C commits per round, derived over a randomized-operation model — already "over √n" at one proposal per commit, reaching an exponent of 0.99 (near-linear) at 50 proposals per commit; separately, Ω(n) worst case for any sequence of adds followed by refresh rounds among the remaining active members, proved for any CGKA construction that uses PKE only through its encrypt/decrypt interface | Same as row above, plus the black-box-PKE restriction the worst-case proof needs | The worst-case bound is proved to hold for "every currently known practical CGKA protocol, including every TreeKEM variant" that treats PKE as a sealed component | Same as row above | AUERBACH-CRYPTO-25, BIENSTOCK-TCC-22 |
| CoCoA (batched-round variant) | ⌈log n⌉+1 rounds to heal every compromised member, proved regardless of how the server breaks concurrent-update ties; cumulative per-user communication O(log²n) when the compromised set is known, O(n·log²n) total when it is not | IND-CPA encryption + UF-CMA signatures; "partially active" adversary — can leak any member's state adaptively but cannot forge protocol messages, because it never obtains signing keys through corruption | A fully active adversary (one that can forge as a corrupted member) is explicitly open, not proved; distributing n fresh signature-verification keys after any update costs Ω(n) per recipient regardless of round count, an unavoidable floor the paper itself proves | A server that computes an individualized packet per recipient, not a passive relay — cannot be swapped for a dumb broadcast channel without losing the bandwidth result; still needs synchronized rounds and one consistent batch order | ALWEN-EUROCRYPT-22 |
| MLS-Cutoff (bounded-concurrency fix to plain TreeKEM) | Expected commit/proposal size O(log n) at a constant proposal rate P; still Ω(n) once proposal rate scales with group size, "matching plain MLS" | Same as the MLS insider-security proof it follows: IND-CCA2 PKE, SEUF-CMA signatures, random-oracle-modeled hash/KDF/MAC | Falls back to the same Ω(n) worst case as plain TreeKEM once concurrency scales with group size; evaluated only under a uniform-random proposer/committer model, explicitly not a claim about real deployment traffic | Same total-order delivery server and tree-hash/parent-hash consistency checks as plain MLS — the fix changes only how proposals are absorbed into the tree | AUERBACH-CRYPTO-25 |
| ART (Asynchronous Ratchet Trees) | O(log n) exponentiations and bandwidth, sender and recipient, per Update/Add/Remove; O(n)/O(log n) setup exponentiations (sender/other) | Diffie-Hellman-based PRF-ODH hardness; Tamarin-verified secrecy of the initial group key, but only under the assumption that no member the agent believes present has been compromised — sender authentication and malicious-insider-subset security are both out of scope by design | Executability under concurrent conflicting updates is an unsolved open problem; the paper's own two mitigations (a grace window accepting stale-keyed messages, or transport-layer rejection of out-of-order updates) are informal and unproved | Reliable broadcast of updated public keys to the whole group after every update, plus one of the two informal concurrency mitigations — an ordering dependency structurally like TreeKEM's, but never formalized | COHNGORDON-CCS-18 |
| DeCAF (blockchain-total-order variant) | O(n·log(n)·log(t)) cumulative sender+recipient communication to heal t corrupted members in ⌊log t⌋+1 epochs, independent of which members are corrupted; in the decentralized instantiation, per-user download communication rises to O(n·log²n), losing CoCoA's O(log²n) recipient-bandwidth advantage entirely, by the paper's own comparison | IND-CPA secretly-key-updatable PKE (skuPKE) + random-oracle-modeled hashing; formally proved, concrete bound (O(εEnc·2(nQ²)²), t, Q)-secure | Forward secrecy requires deleting superseded keys timed to blockchain finality, and the paper gives no confirmation-depth value for when that deletion is safe on a forkable (longest-chain) blockchain; recording only a message hash on-chain to control chain cost loses the paper's own robustness properties unless data availability is separately solved, which it is not | An append-only, globally agreed-upon transcript — instantiated as a blockchain providing consensus (a strictly total order), not merely causal delivery — plus that chain's own liveness guarantee | ALWEN-SCN-24 |
| Weidner, Kleppmann, Hugenroth, Beresford DCGKA ("WKHB") | Highest measured CPU time of three systems compared, sender and recipient, at every tested group size 8 to 512, measured by an independent Java reimplementation built by the BeeKEM authors for their own benchmark; asymptotically O(n) sender / O(1) recipient for Update/Remove, O(n²+h_D) storage, where h_D is the size of WKHB's own membership history — figure independently re-derived, matching, by two further papers | Not assessable from this corpus: the original paper (Weidner, Kleppmann, Hugenroth, Beresford, CCS 2021) was not retrieved as a primary source; every figure here traces to other papers' reimplementation or re-derivation of it | No proof-strength comparison possible without the primary source | Decentralized: a reliable broadcast/gossip layer among members, no total-order delivery service, per every citing paper's characterization | YEN-EPRINT-26 (measured); ALWEN-EUROCRYPT-22, ALWEN-SCN-24 (independent derivations, secondary) |
| BeeKEM (selected) | O(log n) sender and recipient cost for Update/Remove in the no-concurrency case, measured as the lowest CPU time of three systems compared at every tested group size 8–512; under a network partition of 64 members into 4 groups of 16 with U members updating during the partition, total post-partition recovery CPU time and network traffic rise linearly with U then plateau once every member has updated at least once | Post-compromise security and forward secrecy reduced, by a proved game-hop argument, to the security of a non-interactive key exchange (NIKE) under the paper's own HKR-CKS notion plus IND-CPA symmetric encryption; strong convergence, remove-liveness, add-liveness-under-remove-wins, and no-secret-after-merge are proved properties; the tension between partition recovery (Correctness Under Concurrency) and forward secrecy is explicitly conjectured, not proved | Achieves only κ-parameterized forward secrecy: a member who has not updated recently exposes every group secret since her last update if compromised; deleting old secrets promptly to strengthen personal forward secrecy forfeits recovery of group secrets defined on a different partition branch once that partition heals; threat model is honest-but-partition-prone, not Byzantine | Authenticated causal broadcast (ACB): causally-ordered, eventually-reliable, sender-authenticated delivery, no group-wide total order; the shipped implementation builds ACB from a strictly weaker reliable broadcast protocol (RBP, e.g. a gossip network) via a hash-linked DAG plus signatures, a construction cited to prior work rather than proved in this paper; an external PKI for initial member keys; per-device persistent storage of the operation graph, since a new member's join cost is dominated by O(h_B) replay of it | YEN-EPRINT-26 |
| Fork-Resilient CGKA (FREEK / O-FREEK) | No implementation and no benchmark of either construction exists in the corpus; "practical" (FREEK) versus "only theoretical efficiency" (O-FREEK) is the authors' own characterization; O-FREEK's punctured-key size structurally scales with fork-branch depth — how long a fork persists, not group size | FREEK achieves a security predicate weaker than optimal, because an init secret and a MAC key are shared across all members rather than personalized, so exposing any one member's state helps compromise more than that member's own secrets should allow; O-FREEK achieves the paper's optimal predicate via hierarchical-identity-based (binary-tree) encryption and signatures | dMLS, Matrix's own competing fork-tolerant CGKA, is stated by this paper to reach the same any-causal-order processing property only by storing (not deleting) old secrets, "seriously weakening forward secrecy" — the one head-to-head comparison in this row shows causal-order tolerance and forward secrecy trading directly against each other unless FREEK's specific puncturing construction is used | Built on SAIK, a server-aided CGKA — still needs a delivery/mailboxing service for availability, though the paper states confidentiality and authenticity do not depend on that service behaving correctly; needs causality-respecting delivery per sender-receiver pair, weaker than a global total order but a real ordering requirement, distinct from BeeKEM's arbitrary-order requirement across the whole group | ALWEN-CRYPTO-23 |
| Sender Keys (base protocol; WhatsApp, Signal, up to 1,024 members) | O(1) ongoing bandwidth and symmetric encryptions per message (one signed, hash-chained ciphertext per sender); O(n) Add, O(n²) Remove communication complexity, derived not implemented | Proved (Theorem 1) to meet only a weak security notion | A malicious server can mount a censorship attack and add arbitrary members undetected, because control messages carry no per-message authentication of their own; two independent papers disagree on the base protocol's PCS: one finds it restores a weak PCS after an on-demand or removal-triggered update, the other, describing the base protocol with no update operation modeled, finds it exposes all future sender keys immediately on any compromise via deterministic hash-chaining | Authenticated pairwise two-party channels between every member pair, n(n−1)/2 of them, independently maintained, for key distribution; a central server providing total ordering of control messages | BALBAS-ASIACRYPT-23, BIENSTOCK-TCC-20 |
| Sender Keys+ (PCS-bearing update mechanism) | Update/PCS-refresh complexity O(n), down from a naive Signal-style O(n²), derived not implemented | Proved (Theorem 2) to meet a stronger, but still bounded, security notion | Requires total ordering of control messages specifically to avoid overlapping updates — the same delivery-order dependency the ratchet-tree family carries; even a triggered update does not restore PCS over a given pairwise channel unless that specific channel has separately "healed" through its own round-trip exchange since the exposure, which the paper states does not hold "by default" for member pairs that do not exchange private messages regularly | Same pairwise-channel and total-order requirements as the base protocol | BALBAS-ASIACRYPT-23 |
| Pairwise Double Ratchet fan-out, no shared group key (e.g. Apple iMessage, Signal multi-device) | O(n) sender exponentiations and bandwidth, O(1) recipient, on every single message sent — not only on membership-change operations, since there is no shared group key at all | Diffie-Hellman-based PRF-ODH hardness per pairwise channel, formally verified for the two-party case | Cost grows without bound in group size on every message, not merely on rarer key-update operations | n(n−1) independent pairwise channels, each individually maintained; no group-wide ordering or consensus primitive required at all, since every channel is independent | COHNGORDON-CCS-18, COHNGORDON-EUROSP-17 |

### Selection

BeeKEM is selected: a decentralized CGKA protocol whose members exchange protocol messages over
authenticated causal broadcast (no group-wide total order) and whose key-refresh, member-add, and
member-remove operations cost O(log n) in the common, no-concurrency case, degrading gracefully
rather than catastrophically as concurrent operations increase.

Against the TreeKEM/MLS baseline and its total-order-preserving descendants (CoCoA, MLS-Cutoff):
every one of them requires a delivery mechanism that supplies one consistent order of protocol
messages to every group member in a session (ALWEN-CRYPTO-20), a requirement the same paper's own
Section 8.3 attack shows is not merely inconvenient but load-bearing — a leaked state from one
sibling under concurrent, unordered delivery recovers a group key no honest party should be able to
compute, and the authors state this generalizes to every TreeKEM variant they are aware of. That
total order is exactly the coordination point a decentralized architecture removes elsewhere;
building it back in for group encryption alone reintroduces a central or consensus-backed
dependency the rest of the system does not otherwise need. Even granting a working central server,
TreeKEM's real cost under uniformly random concurrent proposals reaches near-linear (exponent 0.99
of n) at moderate concurrency (AUERBACH-CRYPTO-25), and any construction using PKE as a sealed
component is proved to hit Ω(n) worst case regardless of concurrency, on ordinary add-then-refresh
sequences (BIENSTOCK-TCC-22) — a bound that governs TreeKEM, CoCoA, and MLS-Cutoff alike, since none
exploits PKE's internal algebraic structure to escape it. BeeKEM's measured cost, by contrast, rises
with the number of members who updated during a partition and then plateaus, rather than continuing
to grow with group size (YEN-EPRINT-26 Fig. 5) — a different, and for a partition-tolerant
architecture more favorable, degradation shape than TreeKEM's.

Against ART, the earlier Diffie-Hellman-tree construction that produced the pairwise/Sender-Keys
comparison table cited throughout this document: ART's O(log n) cost figures match TreeKEM's, but
its concurrency handling is not formalized at all — the paper offers two informal mitigations for
concurrent conflicting updates and states a complete solution is an open research question
(COHNGORDON-CCS-18) — whereas BeeKEM proves strong convergence, remove-liveness,
add-liveness-under-remove-wins, and no-secret-after-merge as theorems, not informal mitigations
(YEN-EPRINT-26).

Against DeCAF, the closest attempt at decentralizing the same batched-round family: DeCAF replaces
a single company's server with a blockchain, but a blockchain supplies consensus — a strictly
stronger and more expensive coordination primitive than the causal broadcast BeeKEM needs — and the
DeCAF paper's own comparison shows the decentralized instantiation losing CoCoA's recipient-bandwidth
advantage entirely, rising from O(log²n) to O(n·log²n) per user (ALWEN-SCN-24). DeCAF also leaves
the confirmation depth needed for safe key deletion on a forkable chain unspecified, an unresolved
parameter BeeKEM's causal-broadcast substrate does not need, since it assumes no chain fork to wait
out.

Against Weidner et al.'s DCGKA ("WKHB"), the direct predecessor in the same decentralized,
causal-order family BeeKEM belongs to: WKHB matches BeeKEM's ordering requirement exactly, but in
the one head-to-head measurement available — BeeKEM's own authors' reimplementation of both
protocols in the same benchmark harness — WKHB has the highest measured CPU time of the three
systems compared, for both sender and recipient roles, at every tested group size from 8 to 512
(YEN-EPRINT-26 Fig. 4), consistent with its O(n) sender-side asymptotic cost against BeeKEM's
O(log n). This document cannot compare the two constructions' proof strength, because the original
WKHB paper was not retrieved as a primary source into this corpus; the comparison rests on the
measured cost gap alone, which is sufficient to reject WKHB given no evidence entry supplies an
offsetting proof property BeeKEM lacks.

Against Fork-Resilient CGKA (FREEK/O-FREEK): FREEK is architecturally still server-based, built on
SAIK, a server-aided CGKA — it relaxes what a member may do with out-of-order messages once
received, not the underlying delivery infrastructure's role, and no implementation or benchmark of
either FREEK or O-FREEK exists anywhere in the corpus, so no cost comparison against BeeKEM's
measured figures is possible (ALWEN-CRYPTO-23). Where the corpus does offer one comparable data
point — Matrix's own dMLS, which reaches similar causal-order tolerance — that construction is
stated to reach it only by weakening forward secrecy, the exact trade-off BeeKEM's κ parameter is
designed to make explicit and adjustable rather than silently accept.

Against Sender Keys and Sender Keys+: the base protocol's O(1) per-message cost is real, but it
achieves this by giving up post-compromise security almost entirely — one source finds it exposes
every future sender key immediately on any compromise via deterministic hash-chaining
(BIENSTOCK-TCC-20), a stronger negative claim than a second source's finding that a later triggered
update restores a weak form of PCS (BALBAS-ASIACRYPT-23); the two papers examine different versions
of the protocol (one with no update operation modeled, one that formalizes the update Sender Keys
does support), and BALBAS-ASIACRYPT-23's is the more applicable figure for a deployment that
performs updates, since that is the version actually shipped. Even under that more favorable
reading, restoring PCS with Sender Keys+ costs O(n) and requires total ordering of control messages
specifically to avoid overlapping updates (BALBAS-ASIACRYPT-23) — the same centralization dependency
being rejected above, arrived at from a different direction. Post-compromise security and forward
secrecy are part of this component's defining function, stated in the task that produced this
document; a candidate that gives up PCS to hold cost at O(1), or gives it back only by reimporting a
total-order server, does not meet that function.

Against pure pairwise Double Ratchet fan-out: this candidate achieves real, formally verified PCS
with no group-wide ordering dependency of any kind (COHNGORDON-CCS-18, COHNGORDON-EUROSP-17), which
is the strongest partition-tolerance property in this table. Its cost, however, is O(n) sender
bandwidth and computation on every single message sent, because there is no shared group key at
all — every recipient decrypts an independently ratcheted copy. BeeKEM holds one shared symmetric
group key, so its O(log n) figures apply only to membership-change and key-refresh operations;
ordinary message encryption under that shared key is O(1) regardless of group size. Pairwise fan-out
pays its O(n) cost on every message a group ever sends, not only when membership changes — a
materially worse steady-state cost for any group that exchanges more messages than it changes
membership.

### What this selection requires from the rest of the system

- The transport/broadcast component selected elsewhere must supply Authenticated Causal Broadcast
  (ACB) to every BeeKEM group: causally-ordered, eventually-reliable, sender-authenticated delivery,
  with no total order required across the group (YEN-EPRINT-26). BeeKEM's own implementation
  achieves this by extending a strictly weaker Reliable Broadcast Protocol (RBP) — the paper's own
  example is a gossip network all group members participate in — into ACB via a hash-linked
  directed acyclic graph of operations plus digital signatures, a construction the paper cites to
  prior work (Kleppmann and Howard's Byzantine-eventual-consistency result; Kleppmann's
  CRDT-Byzantine-fault-tolerance construction) rather than proving inside this paper. Any transport
  chosen for the wider architecture must either already meet ACB, or must be extended by the same
  cited construction before BeeKEM's security proofs apply to it as stated.
- The identity component must supply a public key infrastructure (PKI), used by BeeKEM as an
  external black box, that lets a member obtain another member's initial public key before adding
  them to a group. BeeKEM's own Add operation performs no identity check on the added public key
  beyond what that external PKI already vouches for, so any Sybil resistance, key-transparency, or
  key-recovery mechanism selected for identity applies before a key reaches BeeKEM, not inside it.
- Every group member's client must persist a durable local copy of both the current tree state and
  the full operation graph, or enough of it to replay from a known-valid starting point — a new
  member's join cost is dominated by O(h_B) replay of that history (h_B being the size of the
  operation graph), and a device that discards its history cannot independently verify or merge
  concurrent branches it did not witness firsthand.
- The cryptographic primitives selected for asymmetric key exchange must supply a non-interactive
  key exchange (NIKE) meeting the paper's own HKR-CKS security notion, not merely generic NIKE
  correctness, paired with a symmetric authenticated-encryption scheme whose key space is
  compatible; the paper's own implementation and benchmark instantiate this as elliptic-curve
  Diffie-Hellman plus ChaCha20-Poly1305, fixed and not varied in the evaluation.
- A system-wide or per-deployment policy must set the retention parameter κ — how many of a
  member's past personal secrets stay retained. This value is left unset by the paper and directly
  trades cross-branch partition recovery against forward secrecy; any component reasoning about
  forward secrecy elsewhere in the architecture (a privacy tier, a data-retention policy) needs to
  know which κ is in force for the groups it covers.
- Any component that composes with BeeKEM must not assume it defends against an actively malicious
  group member forging protocol messages: BeeKEM's threat model is honest-but-partition-prone
  (crash and network-partition faults only), and its proofs do not cover a Byzantine participant.

### What it costs and where it fails

Best case (no concurrent operations): the lowest measured CPU time of three systems compared, for
both sender and recipient roles, across group sizes 8 to 512, on a 16-core AMD CPU with 128 GB RAM
simulating all users and network on one machine, 5 runs per condition, median reported
(YEN-EPRINT-26 Fig. 4, Section 6.1). Asymptotically: O(log n) sender and recipient cost for Update
and Remove; O(log n) sender cost for Add, with O(1) cost to an existing recipient and O(h_B) cost to
a newly joining member who must replay the operation history. Each Update grows the welcome message
by 2.5 kB and adds 40 microseconds to a new member's processing time, in the sequential benchmark
setting.

Under partition: a group of 64 members split into 4 equal partitions of 16, with U members drawn
without replacement issuing an Update during the partition, U swept from 0 to 128 — total
post-partition recovery CPU time and cumulative network traffic rise linearly with U, then plateau
once every member has updated at least once; the cost of the very first post-partition Update grows
more slowly than the cumulative recovery cost as U increases (YEN-EPRINT-26 Fig. 5).

Where it fails: forward secrecy is only κ-parameterized, not full. A member who has not updated
recently must, by the protocol's own correctness requirement, retain access to every group secret
established since her last update — compromising that member exposes all of them, a limitation
BeeKEM inherits from centralized TreeKEM's own Forward-Secrecy-with-Updates weakness
(ALWEN-CRYPTO-20). Specific to the decentralized setting: a member who deletes an old personal
secret promptly, to strengthen her own forward secrecy, loses the ability to decrypt group secrets
defined on a different partition branch once that partition heals, so recovering secrets after a
partition heals is in direct tension with deleting old secrets promptly. The paper's own word is
that this tradeoff "may be inherent in decentralized settings" — a conjecture, not a proof.
Separately, the paper's security theorem is stated over ACB, while the shipped implementation only
guarantees the weaker RBP, with the RBP-to-ACB upgrade cited to other authors' work rather than
proved in this paper — a gap between what is proved and what is deployed that no entry in this
corpus closes.

### What the corpus does not settle

- No wall-clock or millisecond figures for BeeKEM's best-case comparison are extractable from the
  paper's text; YEN-EPRINT-26 records only the qualitative ranking (lowest of three) and the
  Big-O classification read from Fig. 4, a plotted figure, not a table of numeric values. A reader
  who needs concrete latency numbers has to consult the figure directly.
- No default or derived value for the retention parameter κ exists anywhere in the corpus.
  Deployers choose it themselves, trading cross-branch partition recovery against forward secrecy,
  with no measurement of that trade-off's effect at any specific κ.
- No proof of BeeKEM's security against an actively malicious (Byzantine) group member exists in
  this corpus. The construction needed to reach that setting — extending ACB to tolerate forged
  messages, not merely crash faults — is cited to other authors' work, not proved inside the BeeKEM
  paper itself.
- Whether Bienstock, Dodis, Garg, Grogan, Hajiabadi, and Rösler's Ω(n) worst-case black-box-PKE
  impossibility result (BIENSTOCK-TCC-22) applies to BeeKEM's NIKE-tree construction is not checked
  by any entry in this corpus. A 2026 construction that does state its relationship to that same
  impossibility result explicitly (Bartusek, Bitansky, Dodis, Garg, Wu, achieving worst-case
  polylogarithmic CGKA cost) states plainly that it "does not claim to remove" the impossibility
  result, and instead avoids its scope by using the internal structure of a lattice-based encryption
  scheme rather than treating public-key encryption as a sealed component (BARTUSEK-EPRINT-26) — the
  recent logarithmic-cost result operates outside the impossibility result's model rather than
  refuting it. BeeKEM's own NIKE-based construction plausibly escapes the same bound by the same
  general mechanism — direct use of Diffie-Hellman algebraic structure rather than opaque PKE
  encrypt/decrypt calls — but this is a reasoned inference from the structural similarity between
  BeeKEM's and BARTUSEK-EPRINT-26's escape routes, not a claim any entry in this corpus states or
  checks directly.
- No proof-strength comparison between BeeKEM and its direct predecessor, Weidner et al.'s DCGKA,
  is possible from this corpus, because the original DCGKA paper (Weidner, Kleppmann, Hugenroth,
  Beresford, CCS 2021) was never retrieved as a primary source. Every cost figure attributed to it
  here comes from other papers' reimplementation or asymptotic re-derivation.
- The largest group size measured for BeeKEM in this corpus is 512 members, and the largest
  partition experiment used 4 partitions of 16 members each. Whether the observed plateau in
  partition-recovery cost (rather than continued growth) holds at larger group sizes or higher
  partition counts is unmeasured by any entry in this corpus.
- What group size the wider client application actually needs to support in practice is not a
  number any entry in this corpus measures. BeeKEM's own motivating scenario, cited from a study of
  mesh-messaging tools used in large-scale protests, argues that groups of "thousands of members"
  make WKHB's O(n) update cost prohibitive (Albrecht, Blasco, Bjerg Jensen, Mareková, cited within
  YEN-EPRINT-26's bibliography), but this corpus contains no independent measurement of what group
  sizes the specific client being designed here will actually need to support.
