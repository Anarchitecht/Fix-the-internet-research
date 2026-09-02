# Forward secrecy under long partitions in decentralized group key agreement

## Verdict: open

No published paper proves or disproves the conjecture. The paper stating it, Yen, Fábrega, Da,
Kleppmann, Mumm, Park, Zelenka, "BeeKEM: Decentralized, Secure and Efficient Group Key Agreement"
(IACR ePrint 2026/1434), calls it a conjecture in its own text and gives no proof. A companion
notebook page by the paper's first author, dated 31 July 2026 — after the mechanism was designed,
before or concurrent with the ePrint posting — states the same limitation directly: "We lack a
formal impossibility result; it seems inherent, but this is something I will be thinking about a
little more." Two other corpus results address a related but distinct question, worst-case update
communication and computation cost, and neither one's authors claim it bears on the retention
conjecture.

## The conjecture, stated precisely

BeeKEM is a decentralized continuous group key agreement (DCGKA) protocol: a group of users
derives a shared symmetric key, refreshed over time, with no central server and no requirement
that every user's device see every other user's operations in the same order. Membership changes
and key refreshes are recorded in a hash-linked operation graph each device replays locally; when
the network partitions, users on different sides can each keep issuing `Update` operations, and
when the partition heals, the two sides' operation graphs must merge.

BeeKEM defines a retention parameter κ: each user retains her κ most recent personal secrets. Two
correctness and security properties depend on κ in opposite directions:

- **Correctness Under Concurrency (CUC)**: after a partition heals, every user can recover every
  group secret produced by an `Update` on the other side, so long as she was a member on that
  side at the time. CUC holds only at κ = ∞ — retaining every past personal secret.
- **Forward secrecy (FS)**: compromising a user's current state must not expose group secrets
  from before her most recent update. Full FS requires deleting each personal secret immediately
  after it is superseded — κ = 1.

A user who deletes her old secret sk_old to gain forward secrecy, then reconnects after a
partition, cannot decrypt group secrets the other side produced from updates to sk_old — she has
destroyed the material needed to recover them. BeeKEM's own text states the mechanism explicitly:
"If Alice did an Update during the partition and deleted her old secret sk_old for the sake of FS,
she would lose her ability to 'catch up.'" The paper's precise sentence is: "We conjecture the
tradeoff between CUC and FS may be inherent in decentralized settings" — with an earlier passage
narrowing the scope further, to DCGKA schemes with sublinear update cost specifically.

The paper constructs both endpoints — BeeKEM itself (κ tunable, weakens FS to gain CUC) and a
sketched variant, BeeKEM^FS, that deletes immediately (full FS and full cross-fork security, at
the cost of losing recovery of any secret defined on a branch a user did not directly
participate in) — but states BeeKEM^FS is a sketch, not benchmarked, with "a full treatment"
deferred to future work. Constructing both extremes of a tradeoff is not a proof that no protocol
can do better than trade one against the other; it demonstrates the tradeoff is non-empty at both
ends, nothing about points in between or about whether a fundamentally different construction
could occupy neither.

## What the two adjacent corpus results actually measure, and why neither settles it

The task names two candidate results and asks whether either bears on the retention conjecture.
Both are read in full in this corpus and both answer a different question: the worst-case
communication or computation *cost* of a CGKA operation, not whether forward secrecy and
cross-branch recovery can coexist under a network partition.

**Bienstock, Dodis, Garg, Grogan, Hajiabadi, Rösler, "On the Worst-Case Inefficiency of CGKA"
(TCC 2022; corpus key BIENSTOCK-TCC-22).** This paper proves that any CGKA protocol using
public-key encryption only through its encrypt/decrypt interface — never its internal algebraic
structure — has worst-case communication Ω(n) in group size n, on a specific pattern of
operations: some users join and go passive while the remaining active users refresh keys among
themselves, a pattern forced by post-compromise security's requirement not to reuse key material
those passive users received. The proof goes through an intermediate primitive, Compact Key
Exchange, and a black-box separation adapted from Boneh, Papakonstantinou, Rackoff, Vahlis, and
Waters (FOCS 2008). The paper's own model is fully synchronous and non-concurrent — its text
states the bound "already holds for fully synchronous, non-concurrent CGKA executions" — and its
full text, checked directly, contains no mention of network partitions, forks, or branches; its
uses of "partition" refer to partitioning a set of tree nodes into paths inside the protocol's own
data structure, an unrelated sense of the word. This paper bounds how much a CGKA protocol must
communicate in the worst case; it says nothing about whether a protocol that has already paid that
cost can simultaneously keep full forward secrecy and full ability to recover secrets from an
unmerged concurrent branch.

**Bartusek, Bitansky, Dodis, Garg, Wu, "Fair-Weather No More: Guaranteed Efficiency in Secure
Group Messaging" (IACR ePrint 2026/1677; corpus key BARTUSEK-EPRINT-26).** This paper builds the
first CGKA with worst-case polylogarithmic cost for every core operation, by routing the
construction through a lattice-based primitive (incremental and updatable distributed broadcast
encryption, built on the decomposed Learning With Errors assumption from Abram, Malavolta, and
Roy, CRYPTO 2025) whose internal structure the construction uses directly, non-black-box. The
paper's text states plainly that this narrows the scope of Bienstock et al.'s impossibility result
by exploiting exactly the barrier that result identifies — PKE-as-sealed-component — without
refuting the result itself. Its own text, checked directly, contains no discussion of partitions,
forks, or branches either; the string "fork" occurs only as a verb describing test-user generation
inside a security-game reduction, and "branch" only as program control flow in the construction's
pseudocode. Crucially, the paper achieves post-compromise security with every operation
polylogarithmic, but forward secrecy costs a dedicated `FSRefresh` operation the paper states is
"the only linear-time operation in our new CGKA scheme" — and the paper lists as its own open
problem: "We leave it as an open problem to achieve a truly (computation-wise!) sublinear CGKA
scheme with forward secrecy." So even outside any decentralized or partition setting, achieving
low-cost updates and full forward secrecy together, in the same construction, is unresolved by
this paper's own account.

Read together, the two results establish a communication/computation cost floor and a way past a
specific instance of it, on an axis — worst-case update cost as a function of the primitive class
used — that is orthogonal to the retention conjecture's axis: whether recovering a group secret
defined on a branch a user did not participate in is compatible with that user having deleted the
personal secret from which that group secret derives. A protocol could in principle have cheap
(polylogarithmic) updates and still face the retention conjecture's tension, or expensive (linear)
updates and still face it — cost and the CUC/FS tension are different properties of a scheme, and
neither cited paper's proof or construction touches partitions, forks, or branch merging at all.
Bartusek et al.'s own unresolved gap (sublinear-cost forward secrecy, full stop) is suggestive
that the general tension between cheap updates and full forward secrecy is not confined to the
decentralized setting, which — if anything — weakens rather than supports treating decentralization
specifically as the source of the retention conjecture's tension, but neither paper states this
inference itself; it is not drawn in either paper's text and is recorded here as reasoning from
what is measured, not as a further published claim.

## The closest related formal result, and why it falls short of a proof

Alwen, Mularczyk, Tselekounis, "Fork-Resilient Continuous Group Key Agreement" (CRYPTO 2023;
corpus key ALWEN-CRYPTO-23) is the paper BeeKEM's own text cites as the prior work that "develop[s]
a scheme with security against this type of attack, which they call a cross-fork attack, albeit in
a different (centralized) setting from DCGKA." Fork-Resilient CGKA (FR-CGKA) targets exactly the
scenario the retention conjecture describes: a group whose members' views of the operation history
diverge, then must reconcile. Its formal model represents each client's local state as a set of
markers ("pebbles") on a history graph — a move pebble (can this client still act on this epoch),
a visited pebble (has a transition out of this epoch already been irreversibly processed, which
forward secrecy requires), and a key pebble (does the client still hold this epoch's key). Its
strongest construction, O-FREEK, achieves what the paper calls the optimal security predicate:
every epoch is secure "unless keeping it secure would be logically inconsistent with protocol
correctness" — meaning an epoch on a fork branch the client has not yet committed to abandoning
cannot be forward-secure, by the paper's own definition of what correctness requires, and only
becomes forward-secure once the client's visited pebble marks that branch as no longer
recoverable. This is a formal statement, in a different but closely related model, of the same
shape as BeeKEM's conjecture: forward secrecy for a given epoch and the ability to still recover
that epoch's key on an unresolved alternate branch are mutually exclusive by construction, not
merely in the two protocols this paper happens to have built.

This falls short of settling BeeKEM's conjecture for two reasons the corpus's own reading of the
paper states. First, FR-CGKA's "optimal predicate" is a property proved of the specific formal
framework the paper builds (pebbled history graphs over a server-relayed, causally-ordered
delivery channel) and of the specific constructions (FREEK and O-FREEK) proved to realize it — not
an unconditional impossibility theorem separate from any construction, of the kind Bienstock et
al. (TCC 2022) prove for worst-case cost. The paper does not claim, and this evidence entry finds
no claim, that every conceivable DCGKA construction, including ones outside the pebbled-history-
graph formalism, must exhibit the same tension. Second, FR-CGKA's delivery model requires only
causality-respecting delivery per sender-receiver pair through a server or mailboxing service that
need not behave correctly — close to, but not identical to, BeeKEM's fully peer-to-peer gossip
setting with no server role of any kind. Whether the pebbling framework's optimality result
transfers unchanged to BeeKEM's precise setting is not established in either paper.

## What would settle it

A proof would need to state a formal model general enough to range over every DCGKA construction —
not one specific protocol family — capturing partition and branch-merge as the model's own
primitive operations, and show that no construction in that model can simultaneously achieve (a)
recovery of every group secret produced on a branch a user was a member of, after that branch
merges back, and (b) forward secrecy for that user's state at every point before her most recent
update, including during the partition. Fork-Resilient CGKA's pebbling formalism and optimal-
predicate proof are the nearest published template for such an argument; extending it to a model
without any server role and checking whether its impossibility component (the "logically
inconsistent with protocol correctness" clause) is a property of the pebbling framework's own
definitions or a property of the underlying problem itself would be the direct next step. No
published paper retrieved for this pass performs that extension.

## What was searched

Corpus: read BeeKEM's evidence entry (YEN-EPRINT-26) and its full cached text
(`sources/text/YEN-EPRINT-26.txt`) directly for the conjecture's exact wording and surrounding
argument; read the two named corpus papers in full (BIENSTOCK-TCC-22, BARTUSEK-EPRINT-26) and
grepped their cached full text for "fork", "partition", and "branch" to check for any partition-
setting discussion the evidence-file summary might have missed; read every other H-domain
(group messaging) evidence entry bearing on forward secrecy, fork resolution, or decentralized
delivery, including ALWEN-CRYPTO-23 (Fork-Resilient CGKA), ALWEN-EUROCRYPT-22 (CoCoA),
ALWEN-SCN-24 (DeCAF), AUERBACH-CRYPTO-25, CHEVALIER-CCS-24 (Quarantined-TreeKEM), BIENSTOCK-TCC-20,
and MANGIPUDI-EPRINT-26 (Auditable CGKA); grepped `index-measurements.md` and
`index-requirements.md` for "retention," "partition," "conjecture," and "cross-fork."

Beyond the corpus: web search for `"BeeKEM" cross-fork forward secrecy decentralized group key
agreement`; `decentralized continuous group key agreement forward secrecy partition tolerance
impossibility 2026`; `"key retention" OR "retention parameter" forward secrecy fork DCGKA
impossibility proof`; `survey OR "SoK" decentralized secure group messaging continuous group key
agreement 2025 2026`; and a DBLP-directed search for citations of the Fork-Resilient CGKA paper.
Retrieved and read the Ink & Switch Keyhive project notebook page "06 · E2EE in the Local-First
Setting" (inkandswitch.com/keyhive/notebook/06/, authored by Derek Yen, BeeKEM's first author,
dated 31 July 2026), which states the same open status directly, in the author's own words, outside
the ePrint text itself. No 2023-or-later survey or Systematization of Knowledge specific to
decentralized CGKA or DCGKA was found; the most recent related work located is BeeKEM itself
(ePrint 2026/1434) and Bartusek et al. (ePrint 2026/1677), both from the weeks immediately
preceding this search.
