# Keying family: conflicts and disagreements

Scope: group key agreement cost and security properties — sender and recipient
cryptographic operation counts, message sizes, persistent storage, update cost
as a function of group size, post-compromise recovery cost, and measured
runtimes, for continuous group key agreement (CGKA) and the standards and
constructions built on it. Entries checked: `ALBRECHT-CTRSA-21`,
`ALBRECHT-SP-23`, `ALWEN-CRYPTO-20`, `ALWEN-CRYPTO-23`, `ALWEN-EUROCRYPT-22`,
`ALWEN-SCN-24`, `ALWEN-TCC-20`, `AUERBACH-CRYPTO-25`, `AZARI-ACNS-25`,
`BALBAS-ASIACRYPT-23`, `BALBAS-USENIXSEC-23`, `BARNES-RFC-23`,
`BARTUSEK-EPRINT-26`, `BEURDOUCHE-RFC-25`, `BHARGAVAN-HAL-18`,
`BIENSTOCK-TCC-20`, `BIENSTOCK-TCC-22`, `CHEVALIER-CCS-24`,
`CHOU-USENIXSEC-25`, `COHNGORDON-CCS-18`, `COHNGORDON-CSF-16`,
`COHNGORDON-EUROSP-17`, `GREENE-EPRINT-25`, `HALE-SSR-26`, `HASHIMOTO-CCS-22`,
`JAEGER-EUROCRYPT-25`, `KLEIN-SP-21`, `MANGIPUDI-EPRINT-26`, `THIEMT-CCS-25`,
`UNGER-SP-15`, `WALLEZ-SP-25`, `WALLEZ-USENIXSEC-23`, `YEN-EPRINT-26`.

## 1. Two independent benchmarks of the same post-quantum MLS combiner report
   opposite signs for whether it is faster than running post-quantum alone

`GREENE-EPRINT-25` implements the Amortized Post-Quantum (APQ) combiner for
MLS — two parallel MLS sessions, one classical and one post-quantum, with the
post-quantum session advanced only periodically — and measures it against a
post-quantum-only (PQC) MLS baseline across group sizes 2 to 100 on an AMD
FX-6300 (Windows 10). At every tested group size and every Full:Partial
amortization ratio tested (1:10, 1:50, 1:100), APQ ran faster than PQC-only:
30-50% lower CPU cycles per epoch (Table IX), and at group size 100 the
1:100 ratio ran in 226.05 s against PQC-only's 433.32 s over a 500-epoch
session.

`HALE-SSR-26` independently reimplements and benchmarks the same combiner
draft, extending `GREENE-EPRINT-25`'s implementation with a second mode and a
comparison against the X-Wing hybrid KEM, fixed at group size 2 (the paper
argues this is the amortization-adverse worst case, since MLS's tree
structure only helps at larger sizes), on an Apple M2 Max (macOS Ventura),
across three NIST security levels and ratios 1:1, 1:10, 1:50, 1:100. In every
tested combination except two (H-CA-L and H-C-X), APQ's total runtime
**exceeded** the runtime of running the post-quantum session alone — the
opposite sign from `GREENE-EPRINT-25`'s headline result. `HALE-SSR-26`
identifies the cause: Partial Commits dominate the operation count, and at
medium and high security levels the traditional (classical) ciphersuite
component `HALE-SSR-26` pairs against (P384-based, or Ed448) is itself slower
than its paired post-quantum component, so APQ's per-epoch cost skews toward
the slower of the two, not the faster.

`HALE-SSR-26`'s own text states these are not a like-for-like disagreement:
the two papers vary group size, hardware, and — critically — which specific
classical ciphersuite is paired against which post-quantum ciphersuite, and
neither headline percentage can be quoted without naming that pairing and
hardware. Verdict: **different conditions, not a genuine contradiction** —
but a real one to flag, because both headline claims ("APQ is faster than
PQ-only") and ("APQ is often slower than PQ-only") are true only of their own
narrow benchmark, and a synthesis that quotes either one as "the" cost of the
APQ combiner is unsupported. A design considering this combiner needs the
per-ciphersuite-pairing, per-hardware figure for its own deployment target,
not either paper's rollup percentage.

## 2. Whether Sender Keys regains post-compromise security after an update:
   not a contradiction once each paper's modeled mechanism is separated

`BIENSTOCK-TCC-20`'s Table 1 classifies the WhatsApp/Signal Sender Keys
mechanism as providing **no PCS at all** under state exposure — "reveal of
all future sender keys as soon as a member state is exposed" — because
exposing one member's chain key deterministically reveals every future key
that member's hash-chain will produce.

`BALBAS-ASIACRYPT-23` formally proves (Theorem 1) that deployed Sender Keys
achieves a **weak but non-trivial** post-compromise-security guarantee: a
member recovers from exposure when another member is removed, or when it
triggers an on-demand update, at O(n²) communication cost for the naive
whole-group extension. `BALBAS-ASIACRYPT-23` frames this finding explicitly
as correcting "commonly assumed folklore" — but the folklore it corrects is
the opposite direction from `BIENSTOCK-TCC-20`'s classification: it is
correcting an assumption that PCS is *fully* restored after any update or
removal, by showing recovery additionally requires the underlying pairwise
Double-Ratchet channel used to distribute the new chain key to have itself
"healed" since the prior exposure — a condition the paper states often does
not hold in practice, because not every member pair exchanges private
two-party messages regularly.

`BIENSTOCK-TCC-20`'s own entry flags this pair for cross-check. Resolved
verdict: **different conditions, not a contradiction**. `BIENSTOCK-TCC-20`'s
Table 1 classifies the *base* mechanism with no update operation modeled at
all (a citation to Rösler, Mainka, and Schwenk's description of the deployed
protocol without an update path); `BALBAS-ASIACRYPT-23` formally models the
update operation Sender Keys does support and finds its PCS restoration is
itself frequently defeated by the channel-healing precondition. A design that
wants to cite "Sender Keys has PCS" needs to state which channel-healing
condition it is relying on, per `BALBAS-ASIACRYPT-23`; a design that wants to
cite "Sender Keys has no PCS" is accurate only for the no-update deployment
`BIENSTOCK-TCC-20`'s table describes.

## 3. MLS's own architecture RFC authorizes exactly the delivery condition
   that the formal TreeKEM security proof states breaks it

`ALWEN-CRYPTO-20` proves TreeKEM's non-adaptive CGKA security (Theorems 1 and
2) under a stated requirement: the delivery mechanism must deliver CGKA
protocol messages "in the same order to every member of a session" — it may
drop, delay, or reorder relative to other sessions, but within one session
every member eventually sees the same total order. The paper states this
requirement is not incidental: Section 8.3 sketches an attack in which two
sibling members of the ratchet tree each process a concurrent update from a
different party under a "fully arbitrary, unordered network," and a leaked
state from one sibling lets an adversary recover a group key the honest
protocol design did not expect that party to be able to compute. The paper
states this generalizes to every TreeKEM variant the authors are aware of at
the time, including the specific fix (Kohbrok's) used elsewhere in the same
paper.

`BEURDOUCHE-RFC-25`, the MLS architecture document, classifies a deploying
application's Delivery Service into two supported kinds using the CAP
theorem: a Strongly Consistent DS, which gives every client the same message
order, and an **Eventually Consistent DS — explicitly including "a
distributed peer-to-peer message-broadcast mechanism" as a named example —
which stays available under network partition but may deliver messages to
different clients in different orders**, with reconciliation pushed onto the
clients via a deterministic tie-breaking policy applied once multiple Commits
for the same epoch are observed.

**Requirement:** a consistent, per-session total order of delivered CGKA
messages, required by `ALWEN-CRYPTO-20`'s Theorems 1 and 2 for TreeKEM's
proof of confidentiality to apply.
**Destroyed by:** the Eventually Consistent Delivery Service architecture
`BEURDOUCHE-RFC-25` authorizes as one of MLS's two supported deployment
options. Before a group's deterministic tie-break resolves a given epoch,
different members observe different, unordered Commits for that epoch —
precisely the condition `ALWEN-CRYPTO-20`'s Section 8.3 attack exploits: two
tree-sibling members each processing a concurrent update.
**Resolution options:** (a) restrict the deployment to a Strongly Consistent
Delivery Service, giving up the partition tolerance `BEURDOUCHE-RFC-25`
otherwise permits; (b) accept the exposure window during the unreconciled
period between Commits as a stated, uncorrected gap — `BEURDOUCHE-RFC-25`
does not claim its Eventually Consistent option restores the property
`ALWEN-CRYPTO-20`'s proof depends on, and neither RFC document engages with
this specific attack; (c) select a CGKA construction whose security proof is
built for this setting from the start rather than retrofitted onto it —
`YEN-EPRINT-26` (BeeKEM) is such a construction already in this corpus,
proved directly over causally-ordered broadcast rather than a per-session
total order, at the cost of the weaker, parameterized forward-secrecy
notion recorded in finding 5 below.

## 4. TreeKEM's cost table for ART attributes an "equal sender/recipient
   cost" to group creation that ART's own table shows is asymmetric

`BHARGAVAN-HAL-18` (the original TreeKEM design paper) tabulates TreeKEM's
own operation costs against Asynchronous Ratchet Trees (ART), and states, as
a general claim about the cited ART paper, that "the paper states send and
receive costs are equal," giving a single "ART recipient cost" figure of
`2n` public-key operations for the Create (group-creation) row on the
strength of that equality claim.

`COHNGORDON-CCS-18` — the ART paper itself — states in its own Table 1 an
**asymmetric** split for the corresponding Setup operation: `O(n)`
exponentiations for the sender (the group creator) against `O(log n)` for
"other" (any later-joining member), consistent with the paper's own
mechanism description — a later member computes the tree key from its own
leaf secret and its copath, an O(log n) operation, while only the creator,
who alone must generate a fresh key pair for every other member's leaf
directly, pays the O(n) cost. `COHNGORDON-CCS-18`'s equal-cost figures
(`O(log n)` / `O(log n)`) apply only to its *Ongoing* row (Update/Add/Remove),
which is the case `BHARGAVAN-HAL-18`'s own table correctly reports as `2·log(n)`
for both parties.

For Create/Setup specifically, `BHARGAVAN-HAL-18`'s attributed figure — equal
sender and recipient cost at `2n` — is not supported by, and is contradicted
by, `COHNGORDON-CCS-18`'s own stated asymmetric bound for the same operation.
This is worth checking against the original PDFs directly before it
propagates into a synthesis table, since the two entries in this corpus
disagree on a property (equal versus asymmetric cost) of the same operation
in the same cited paper, not merely on a numeric constant.

## 5. A recent logarithmic-cost CGKA result does not refute the standing
   worst-case impossibility result — two papers confirm this from opposite
   sides, and a third (BeeKEM) must not be read as doing so either

`BIENSTOCK-TCC-22` proves that no CGKA protocol built by treating public-key
encryption as a sealed black box (using only its encrypt/decrypt interface,
never its internal algebraic structure) can guarantee below-linear-in-group-
size worst-case communication cost; the bound targets a "bad sequence" of
adds followed by rounds of state refreshes among the remaining active users,
and the paper states it holds even amortized over a whole session and even
under fully synchronous, non-concurrent execution.

`BARTUSEK-EPRINT-26` (2026) constructs the first CGKA with provably
polylogarithmic *worst-case* computation and communication cost for adds,
removes, and post-compromise recovery — a genuinely stronger result than
anything else in this family. Its own text is explicit that this does not
refute `BIENSTOCK-TCC-22`: the construction routes every operation through a
new primitive (incremental and updatable distributed broadcast encryption)
built directly from the internal structure of a lattice assumption, not
through public-key encryption used as a sealed component, which is exactly
the class of construction `BIENSTOCK-TCC-22`'s own stated limitations
identify as the one avenue left open for escaping its bound. Verdict:
**operates outside the impossibility result's stated model, does not refute
it** — both papers state this themselves, so no correction is needed to the
corpus, only a note that a synthesis citing `BARTUSEK-EPRINT-26`'s
polylogarithmic result must not describe it as overturning
`BIENSTOCK-TCC-22`, and must separately note that `BARTUSEK-EPRINT-26`'s own
forward-secrecy-refresh operation is still linear-time — the paper achieves
sublinear cost for post-compromise security only, not for forward secrecy,
and states achieving both together as an explicit open problem.

`YEN-EPRINT-26` (BeeKEM) requires the same care for a different reason.
Its headline claim — "the first decentralized group key agreement protocol
with logarithmic update cost in the common case" — is correctly qualified in
the paper's own text as a common-case (no-concurrency) result: Table 1
reports BeeKEM's O(log n) sender cost for Update/Remove under sequential
execution, and the paper's own partition-recovery experiment (Fig. 5) shows
total recovery cost rising linearly with the number of members who update
during a partition, before plateauing. This is fully consistent with, not a
counterexample to, `BIENSTOCK-TCC-22`'s worst-case bound, since BeeKEM's own
evaluation section reports exactly the degradation to linear cost under
concurrency the impossibility result predicts. The risk is citation drift:
`BRIEF.md` section 7's own prior-pass summary states BeeKEM achieves "the
first DCGKA with O(log n) update cost" without the common-case qualifier
present in the paper itself; a synthesis repeating that unqualified phrasing
would misstate what BeeKEM proves.

## 6. A formal theorem on TreeKEM's forward secrecy versus the property
   informally claimed for the protocol at the time — a defect found, then
   closed, across two formal papers in this corpus

`ALWEN-CRYPTO-20`'s own text states that its central finding "directly
contradicts an informal claim commonly made about TreeKEM/MLS at the time" —
that the draft protocol already achieved standard forward secrecy. The
paper's Theorem 1 instead proves the pre-fix draft achieves only a strictly
weaker, formally defined property the authors call "forward secrecy with
updates" (fsu): corrupting any group member other than a given update's
initiator fully reveals that update's secret unless a further, order-
dependent sequence of other members' updates has already occurred, and if
the initiator's tree-sibling never updates, that secret is never forward
secret at all. The paper's proposed fix, Modified TreeKEM (built on
updatable public-key encryption), closes this gap.

This is not a live contradiction in the corpus today. `WALLEZ-SP-25`,
analyzing the actual published standard (RFC 9420) rather than the pre-2020
draft `ALWEN-CRYPTO-20` analyzed, finds the finalized standard's separation
of the initialization key from the leaf-node key — a structural change from
the draft `ALWEN-CRYPTO-20` reviewed — "yields a stronger theorem in our
case" for forward secrecy, because a new participant no longer needs to
retain the medium-term initialization key after joining. Read together, the
two formal papers in this corpus document a defect that was found in an
early MLS draft and closed by the time the standard was finalized, not a
standing disagreement about the deployed standard's guarantees. A synthesis
that cites only "MLS provides forward secrecy" (the framing both
`BARNES-RFC-23` and `BEURDOUCHE-RFC-25` use, without the fsu-versus-full-FS
distinction) is not wrong about the current standard, but should not be
extended backward to every TreeKEM-family draft or variant without checking
which specific construction is meant — `KLEIN-SP-21`'s own Table 1 records
plain TreeKEM's security-loss reduction as exponential (`Ω((nQ)^n)`, Standard
Model, selective/passive only) rather than the polynomial bound
`ALWEN-CRYPTO-20`'s fix achieves, so "TreeKEM" without a variant name is not
a well-defined claim of forward secrecy strength in this corpus.

## 7. A related but distinct property gap: message-level unforgeability
   findings should not be read onto CGKA's forward-secrecy/PCS guarantees

`JAEGER-EUROCRYPT-25` finds that MLS's chat-encryption layer (the step that
turns the CGKA-derived group key into per-message confidentiality and
sender authenticity, distinct from CGKA itself) achieves only a weakened
in-group-unforgeability notion, and reports a practically exploitable
insider replay/reordering attack within one MLS epoch. The paper states
explicitly that a prior formal security analysis of MLS (Alwen, Coretti,
Dodis, Tselekounis, CCS 2021 — not independently held as its own entry in
this corpus, cited here only as `JAEGER-EUROCRYPT-25` describes it) did not,
and by the paper's own argument could not have, identified this attack,
because that analysis's definitions require the attacker to stay passive
after any compromise until the next key update rather than modeling an
actively malicious group member. This is a distinct property from the
forward-secrecy/PCS findings above — chat-encryption unforgeability, not
key-agreement secrecy — and should not be conflated with them in a
synthesis; a design that cites `ALWEN-CRYPTO-20` or `WALLEZ-SP-25` for MLS's
key-agreement guarantees still needs `JAEGER-EUROCRYPT-25`'s finding for the
message-authenticity layer, since the two papers prove different things
about different sub-protocols of the same standard.

## Checked and found no conflict

`BARNES-RFC-23` and `BEURDOUCHE-RFC-25` (the two MLS RFCs) report no
measured figures and do not disagree with each other or with
`BHARGAVAN-HAL-18`'s O(log n) asymptotic costs. `MANGIPUDI-EPRINT-26`'s
auditable-CGKA overhead figures and `CHEVALIER-CCS-24`'s quarantine-overhead
figures measure two different additions to MLS (audit escrow versus inactive-
member key recovery) at different operating points and are not comparable
quantities. `UNGER-SP-15`'s property ratings predate MLS/TreeKEM entirely and
make no claim about it. No internal abstract-versus-conclusion disagreement
was found in any single domain-H entry checked for this family.
