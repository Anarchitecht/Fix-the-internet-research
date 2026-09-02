# Sync family: conflicts and disagreements

Scope: set reconciliation in all its families (characteristic-polynomial, Invertible
Bloom Lookup Table (IBLT) and rateless variants, range-based set reconciliation),
CRDTs (Conflict-free Replicated Data Types), Byzantine-tolerant replication,
Merkle-structured indexes, feed generation, ranking, moderation, and peer-assisted
video offload. Entries opened: `MINSKY-TIT-03`, `EPPSTEIN-SIGCOMM-11`,
`GOODRICH-ALLERTON-11`, `YANG-SIGCOMM-24`, `KENIAGIN-SIGMETRICS-25`,
`AMPARORE-ARXIV-26`, `GOMES-ARXIV-25`, `HARISH-NETWORKING-26`,
`NEGENTROPY-NIP77-23`, `WILLOW-SPEC-23`, `MEYER-TR-24`, `ALMEIDA-CSUR-25`,
`SHAPIRO-EATCS-11`, `SHAPIRO-SSS-11`, `ATTIYA-PODC-16`, `BURCKHARDT-POPL-14`,
`ELLIS-SIGMOD-89`, `SUN-CSCW-98`, `KLEPPMANN-AFP-18`, `KLEPPMANN-ONWARD-19`,
`KLEPPMANN-PAPOC-19`, `KLEPPMANN-PAPOC-22`, `KLEPPMANN-TPDS-17`,
`KLEPPMANN-TPDS-22`, `KLEPPMANN-ARXIV-20`, `AUVOLAT-SRDS-19`, `RAWAT-DLT-24`,
`CHYSTIAKOV-ARXIV-25`, `AIYER-SOSP-05`, `GOLD-ARXIV-23`, `WANG-ARXIV-26`,
`QUELLE-PLOSONE-25`, `LIU-PACMHCI-25`, `HEGEDUS-ECMLPKDD-19`,
`KLEPPMANN-CONEXT-24`, `AGARWAL-ICWSM-24`, `ANAOBI-WWW-23`,
`ARREGUI-GARCIA-ARXIV-26`, `BONO-ICWSM-26`, `BONO-WEBSCI-24`, `ZIA-ARXIV-25`,
`ZUO-ICWSM-24`, `ZHANG-ARXIV-25`, `ZHANG-PACMHCI-24`, `DOAN-NETWORKING-20`,
`KARAMSHUK-INFOCOM-15`, `POLINSKI-CCR-24`, `TANG-ARXIV-22`, `HEI-TMM-07`,
`ZHANG-INFOCOM-05`, `CASTRO-SOSP-03`, `CHU-JSAC-02`, `RAMAN-IMC-19`,
`HE-IMC-23`, `BALDUF-IMC-24`, `WEI-PACMNET-25`.

No cross-paper numeric measurement disagreement — two independently measured,
comparably conditioned figures for the same quantity that disagree — turned up
inside this family. The Mastodon/Fediverse moderation and peer-assisted-video
entries in domain K each state their own scope carefully (crawl date, platform,
metric) against related papers and none reports a figure another entry
contradicts under matching conditions; the entries covering Nostr availability
against Mastodon availability (`WEI-PACMNET-25`, `RAMAN-IMC-19`) are already
recorded in `registry/conflicts/centralization.md` and are not repeated here.
What this family does hold is a set of destroyed preconditions, several
unsupported attributions, and three internal abstract/body inconsistencies, all
below.

---

## 1. Range-based set reconciliation requires a property prolly trees do not have

`MEYER-TR-24` proves that range-based set reconciliation (RBSR) — the
technique `NEGENTROPY-NIP77-23` (Nostr's NIP-77) and `WILLOW-SPEC-23` deploy,
and `AMPARORE-ARXIV-26` optimizes the storage layer for — needs the backing
search tree to be "clamping-invariant": restricting two structurally different
but same-content trees to an arbitrary sub-range must yield the identical
result, or two peers computing a fingerprint over the same range from
different tree histories get different fingerprints for identical data and
either fail to detect a real match or falsely accept a mismatch. `MEYER-TR-24`
proves treaps have this property and states plainly, "Prolly-trees are not
clamping-invariant," because a prolly tree's chunk boundaries are set by a
rolling hash over a window of consecutive items, and clamping to a sub-range
changes which items fall inside that window, changing the boundaries the
comparison depends on.

`RAWAT-DLT-24` builds and benchmarks a prolly tree (content-defined chunking
by a hash-of-node-content threshold, in the tradition of Dolthub and
Canvas/okra) for exactly the kind of large key-value dataset RBSR targets, and
its own Requirements section already names the collision: "a range-based
set-reconciliation protocol requiring clamping-invariance... cannot be
composed directly with this prolly-tree design without an additional
adaptation neither paper supplies." `RAWAT-DLT-24` itself states computing a
difference between two prolly trees is out of scope for the paper ("the
mechanisms by which two Prolly trees are compared... fall beyond the scope of
this paper"), so nothing in this corpus supplies the missing adaptation.

Resolution options a synthesis has: select a proven clamping-invariant
structure (a treap, per `MEYER-TR-24`'s proof) wherever RBSR-style range
reconciliation over arbitrary sub-ranges is required; or restrict prolly trees
to whole-chunk Merkle comparison (root-hash and boundary-hash equality, the
comparison Dolthub and Canvas already perform) rather than arbitrary-range
queries; or record the missing prolly-tree/RBSR adapter as an open problem,
since neither retrieved paper supplies one.

## 2. BAR incentive-compatible Byzantine tolerance requires exactly the admission control an open-membership design removes

`AIYER-SOSP-05`'s Byzantine-Altruistic-Rational Tolerant (BART) construction
secures rational (self-interested but non-malicious) nodes through
accountability: a Proof of Misbehavior is only checkable because "a trusted
admission authority must exist to issue each participant exactly one
cryptographic public-key identity." The paper states this requirement is
"reasonable only for its target closed-membership communities" (co-workers, a
dormitory's students, a nonprofit's PC recipients) and "not for an
open-membership network," and its Byzantine-fault bound is capped at
(n-2)/3 of all nodes.

`KLEPPMANN-ARXIV-20`'s Byzantine Eventual Consistency (BEC) is built for the
opposite case: it tolerates an unbounded fraction of Byzantine replicas
specifically so a database can stay "immune to Sybil attacks... without
proof-of-work or centrally controlled peer admission." An architecture that
picks BEC's causal-broadcast-over-signed-DAG mechanism for open,
permissionless replica admission has, by that choice, removed the
authority-issued, one-per-participant identity `AIYER-SOSP-05`'s
incentive-compatibility proof depends on — so BART-style accountability and
sanctions cannot be layered onto a BEC-admitted, permissionless replica set
without reintroducing the trusted admission authority BEC was built to avoid.

Resolution options: select BEC (and accept BEC's narrower guarantee — only
I-confluent transactions and invariants, not general rational-node incentive
compatibility) for a fully open peer-to-peer identity layer; select BART-style
accountability only where a closed or permissioned deployment already exists
(a federation of storage providers, say) and admit that the open-network
design target is not met there; or record layering incentive-compatible
sanctions onto a permissionless BEC network as an open problem, since neither
paper supplies that combination.

## 3. Two papers make opposite Byzantine-robustness claims about the same Merkle Search Tree, and neither claim traces to the tree's own paper

`AUVOLAT-SRDS-19` (Merkle Search Trees, MST) contains no discussion anywhere
in its retrieved text of Byzantine faults, malicious nodes, or adversarial
input; its own evaluation states explicitly, "No node joins, leaves, or
crashes occurred in any reported simulation," and its correctness argument
rests only on a collision-resistant hash function and a benign gossip model.

`KLEPPMANN-PAPOC-22` (Making CRDTs Byzantine Fault Tolerant) characterizes
`AUVOLAT-SRDS-19` in its own reference list as the "state-based CRDT
counterpart tolerating any number of Byzantine nodes" to its own operation-based
construction. `AUVOLAT-SRDS-19`'s retrieved text supports no such claim —
see above.

`MEYER-TR-24` characterizes the same paper in the opposite direction: it
states Auvolat and Taïani's Merkle Search Tree "can be driven to O(n)
degeneration by a malicious data source producing a set that collapses the
tree to a single large array," and flags its own uncertainty about this
("This corpus does not yet hold Auvolat and Taïani (SRDS 2019) to verify that
characterization independently"). The corpus now holds it, and `AUVOLAT-SRDS-19`'s
text supports neither `KLEPPMANN-PAPOC-22`'s Byzantine-tolerance claim nor
`MEYER-TR-24`'s degeneration claim; it is silent on adversarial behavior in
both directions.

Both citing claims are unsupported attributions against the same cited paper,
and they are not obviously reconcilable as one being about safety and the
other about performance: `KLEPPMANN-PAPOC-22`'s claim is unconditional
("tolerating any number of Byzantine nodes"), and `MEYER-TR-24`'s claim is
about a specific performance collapse an adversary can trigger, not merely a
safety violation — two different properties, but `AUVOLAT-SRDS-19` proves
neither. A synthesis citing `AUVOLAT-SRDS-19` for either robustness claim needs
its own analysis or a different source; the paper does not settle it.

## 4. The corpus's own retrieval-target justification attributes a measurement to a paper that does not contain one

`registry/targets-deduped.json`'s stated reason for retrieving `KLEPPMANN-TPDS-17`
(A Conflict-Free Replicated JSON Datatype, the Automerge paper) reads: "States
the paper's own memory and message-size measurements against Operational
Transformation and other CRDTs." `KLEPPMANN-TPDS-17`'s own retrieved text
contains no such measurements — it is a formal-semantics paper with no
implementation or evaluation, and its own conclusion defers performance
measurement to follow-on work. This is caught in the evidence entry's own
Contradicts section, and it is exactly the failure `BRIEF.md` section 2.1
exists to prevent: a synthesis citing `KLEPPMANN-TPDS-17` for Automerge's
memory or message-size cost has no support in the retrieved text and needs a
different, later source.

## 5. Three internal abstract/body inconsistencies

`MEYER-TR-24`'s abstract states its non-homomorphic RBSR technique
"effectively render[s] merkle-search-tree reconciliation obsolete." Its own
conclusion states "neither option is strictly superior to the other," because
the homomorphic-hash-based RBSR variant this paper replaces retains an
advantage the paper's own non-homomorphic construction does not have:
immunity to the malicious-data-source degeneration described in finding 3
above. A synthesis citing only the abstract would carry forward an
unqualified obsolescence claim the paper's own conclusion withdraws.

`AIYER-SOSP-05`'s abstract states its replicated-state-machine prototype
"executes 20 requests per second." Section 8 states the measured figure as
"about 15 operations a second for small groups of users." The two figures are
not reconciled anywhere in the retrieved text — no stated change in
configuration, hardware, or group size separates them. A synthesis reporting
BAR-tolerant replication throughput from this paper's abstract alone would
carry forward a number the paper's own evaluation section does not confirm.

`ELLIS-SIGMOD-89`'s abstract states the algorithm's "overall structure is
independent of the semantic information." The algorithm's central mechanism,
the transformation matrix T, is described in the same paper as a set of
hand-written functions, one per operator pair, each embedding
operation-specific semantics (incrementing or decrementing a text position,
for example) — only the surrounding control structure (request queue,
state-vector comparison, log scan) is semantics-independent, not the
transformation step the algorithm's correctness actually depends on. A reader
citing the abstract for a semantics-independent transformation mechanism would
misstate what the paper's own description of dOPT requires.

---

## Restated results to not double-count

Two pairs in this family report the same underlying result twice, which a
synthesis must count once, not twice, when weighing evidence:

- `SHAPIRO-EATCS-11` and `SHAPIRO-SSS-11` are, by the two entries' own
  statements, the same two convergence conditions (state-based/CvRDT:
  monotonic semilattice with least-upper-bound merge; operation-based/CmRDT:
  commuting concurrent operations under causal delivery) published twice by
  the same four authors in the same year — the EATCS bulletin version adds a
  garbage-collection treatment and longer examples, the SSS conference version
  adds the Strong Eventual Consistency definition, the CAP-theorem argument,
  and the state/operation emulation theorems, but neither adds a second,
  independent proof of the shared convergence conditions.
- `KLEPPMANN-AFP-18` (OpSets) and `KLEPPMANN-PAPOC-19` share the same
  underlying interleaving-anomaly analysis — which sequence-CRDT algorithms
  garble concurrent same-position insertions and which do not — by the same
  authors; `KLEPPMANN-AFP-18`'s own entry states the two "should be read
  together, not treated as independent confirmations." `KLEPPMANN-PAPOC-19`
  adds one result `KLEPPMANN-AFP-18` does not contain: the lesser RGA
  anomaly and its conjectured (unproven) fix.

Separately, the Rateless IBLT communication-overhead figure of 1.35x to 1.72x
the symmetric-difference size, converging to 1.35x as the difference grows,
is `YANG-SIGCOMM-24`'s own measured result. `KENIAGIN-SIGMETRICS-25` cites it
as a comparison baseline without independently re-deriving it, and
`GOMES-ARXIV-25` uses the same 1.35 figure as an input constant (C_elem) for
its own stopping-rule design, also without independent re-derivation. Three
entries in this corpus therefore carry this number, but it is one measurement,
made once, by one paper (`YANG-SIGCOMM-24`) — cross-checked directly against
that paper's own text for this report, and confirmed to match
(`YANG-SIGCOMM-24`'s own table states "1.35x-1.72x average, converging to
1.35x when d reaches the low hundreds," the identical figure `KENIAGIN-SIGMETRICS-25`
and `GOMES-ARXIV-25` both carry forward).

---

## A pre-verified citation with no evidence-file entry behind it

`BRIEF.md` section 7 records "Range-based set reconciliation (Meyer, IEEE
SRDS 2023, arXiv 2212.13567) — rounds bounded by `2 + 2⌈log_b(n_min)⌉ −
⌊log_b(t)⌋`" as already verified. Five entries in this family —
`AMPARORE-ARXIV-26`, `KENIAGIN-SIGMETRICS-25`, `MEYER-TR-24`,
`NEGENTROPY-NIP77-23`, and `WILLOW-SPEC-23` — each cite this same Meyer SRDS
2023 paper as "already in this corpus" or "already known to this corpus per
BRIEF.md's already-verified section." No file matching this paper exists
under any key in `registry/evidence/`, no such key appears in
`registry/index-measurements.md` or `registry/index-requirements.md`, and
`retrieval-log.md` records no retrieval attempt for it — only for its
follow-on paper, `MEYER-TR-24`. The round-count formula and every other claim
attributed to this paper therefore has no full-text entry a reader can check
against `BRIEF.md`'s own section 9.4 honesty rule ("Any claim not backed by a
full-text entry is marked unverified inline"). A synthesis citing the round-count
bound, or citing this paper as a foundational source for RBSR generally, is
citing a claim with no retrievable evidence-file entry behind it in this
corpus and should mark it unverified or retrieve the paper before relying on
it.
