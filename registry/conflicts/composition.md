# Composition conflicts: destroyed preconditions across domains

Agent X. No retrieval performed. This file reports pairs where a candidate mechanism's stated
requirement on the rest of the system is removed by another candidate mechanism's own stated or
proved behavior. Every claim below cites the evidence-file entries it rests on by KEY. Measurement
disagreements are not this family's assignment and none are reported here.

Requirements in `registry/index-requirements.md` were grouped by kind — ordering, observability,
honesty, reachability, stability over time — and checked pairwise across domains. Two candidates
already flagged as destroying each other's preconditions in the brief (square-root replication
against blinded search and against LRU eviction; MLS's total-order requirement against a
partition-tolerant delivery layer) are not repeated here. Five new pairs survive verification
against the full evidence-file text, at varying confidence. Two rest on an explicit statement in
one paper about a property a specific other mechanism destroys. Three rest on tracing a stated
requirement in one paper against a stated behavior in another; those are marked as derived
reasoning, not as a conflict either paper states about the other.

## 1. Observable lookup progress and per-neighbor timeout estimation require opposite routing modes

`SIT-IPTPS-02` derives a DHT security principle: the node issuing a lookup must observe each hop's
identifier and confirm the identifier-distance to the target strictly decreases at every step. The
paper states this check "is impossible" once a node forwards a query onward itself, deciding the
next hop without reporting back to the querier — the paper's example is CAN's round-trip-time
(RTT)-optimized recursive forwarding. The requirement holds only under iterative routing: each hop
replies to the original querier, who then contacts the next hop directly.

`RHEA-USENIXATC-04` builds Bamboo's churn-handling result on the opposite routing mode. Its
TCP-style per-neighbor timeout estimation — computing a lookup timeout from the exponentially
weighted mean and variance of round-trip time to each neighbor, the technique that gives Bamboo its
best measured latency under churn — depends on a node "communicating almost exclusively with its
own logarithmic-size set of direct overlay neighbors," which the paper states requires recursive
routing. An iterative-routing DHT cannot supply this: the querier itself would need timeout
estimates to nodes across the whole network, not just its own neighbors, and Rhea's own comparison
shows the fallback for that case, Vivaldi virtual-coordinate estimation, tracks TCP-style accuracy
only down to moderate churn before diverging.

A single DHT selected for both a security property (verifiable lookup progress against a malicious
intermediary) and a churn-handling property (accurate per-hop timeout estimation) cannot satisfy
both papers' preconditions with one routing mode. Recursive routing, needed for Rhea's timeout
technique, is exactly the mode Sit and Morris name as defeating their principle 2 check.

**Resolution options.** Keep iterative routing and accept Vivaldi-derived timeouts, whose own
measured divergence from TCP-style accuracy grows at higher churn (`RHEA-USENIXATC-04`). Keep
recursive routing and Rhea's better-measured timeout accuracy, and substitute a different defense
for lookup-progress verification — disjoint-path lookup of the kind S/Kademlia supplies (Baumgart
and Mies, ICPADS 2007, per `BRIEF.md` section 7's verified seeds; not itself a registry KEY), which
does not depend on iterative observability. Record the tension as unresolved for the specific DHT
selected, if neither substitution is acceptable.

## 2. FROST's exactly-once nonce commitment cannot be safely stored on a CRDT-style replica

`KOMLO-SAC-20` requires a "commitment server" location where each participant publishes single-use
nonce-commitment pairs before signing. The paper states this location "must be trusted to serve
correct, unused values" — every commitment consumed by an aggregator must never be handed to a
second aggregator, because FROST's entire non-robustness design assumes preprocessing produces a
disjoint pool of once-only values, and the paper's own defense against the Drijvers et al.
ROS-style forgery rests on binding each signature to one message and one signing set drawn from
that pool.

`SHAPIRO-EATCS-11` (and its companion `SHAPIRO-SSS-11`) proves state-based CRDT (CvRDT) convergence
under a communication model that tolerates message loss, reordering, and duplication, requiring
only that every update eventually reach every replica. The proof supplies no consume-once or
linearizable-read primitive: two replicas that have not yet exchanged a given update both hold, and
both may act on, the same locally visible state. Neither Shapiro et al. paper claims to solve
exactly-once consumption; the omission is a scope statement in the papers themselves, not an
attack they describe.

The composition problem does not appear in either paper; it appears only when an architecture backs
FROST's commitment store with an eventually-consistent, partition-tolerant replicated store of the
kind Shapiro et al. describe, chosen elsewhere in the same design for its availability under
partition. Under a network partition, two isolated replicas of that store can each still regard the
same nonce-commitment pair as unconsumed and hand it to a different signature aggregator. FROST's
own text emphasizes that the commitment server must serve "unused values" precisely because reusing
a nonce across two signing sessions is the class of failure Schnorr-family threshold signatures are
known to be unable to tolerate — the paper's forgery defense addresses a different, adversarial
version of session reuse, not two honest aggregators drawing from diverged replicas. This step is
derived reasoning about what happens when the two mechanisms are composed, not a claim either paper
makes about the other.

**Resolution options.** Back FROST's commitment store with a linearizable store — a single elected
leader, or a consensus-backed key-value store — accepting reduced partition tolerance for that one
component, rather than the CRDT-style replica used elsewhere. Restrict FROST signing operations to
periods when the commitment store's replicas are known to be mutually connected, accepting a
liveness cost during partitions instead. Record which resource classes in the architecture need
exactly-once semantics as an open list, since FROST is unlikely to be the only one.

## 3. G-Rank writes the sender's identity into the payload a mix network is built to hide

`PIOTROWSKA-USENIXSEC-17` (Loopix) provides "bidirectional sender and receiver anonymity" against a
global passive adversary: intermediate mix nodes "learn only routing metadata," and the paper lists
attaching a sender address to a message payload as a feature it has deliberately left unbuilt,
leaving that decision to whatever application runs on top.

`GOLD-ARXIV-23` (G-Rank) is such an application. Its gossip message, the clicklog row, carries "the
querying peer's node ID" as data the ranking algorithm itself consumes: the receiving peer's
similarity computation (kappa_t, kappa_m, kappa_u) needs a stable per-peer identifier to accumulate
evidence across queries, and the paper states peer discovery "is not supplied by any separate
mechanism" — a peer learns of another peer's existence only by reading that node ID out of a
received clicklog row.

Loopix hides the network-level origin of a message from an observer on the path or at a mix node.
It does not, and by its own stated design cannot, strip identifying content the application itself
writes into the payload. Routing G-Rank's clicklog gossip over a Loopix-style privacy tier removes
none of the sender-identifying information G-Rank depends on, because that information was never a
transport-layer property to begin with — the receiving peer still reads the true node ID from the
message body, and gossips it onward to every peer it later shares that clicklog row with. Selecting
G-Rank as the ranking mechanism destroys the anonymity property the privacy tier exists to supply,
for every message G-Rank generates, regardless of which transport carries it.

**Resolution options.** Exclude G-Rank's clicklog traffic from the privacy tier's guarantee
explicitly, so a user choosing the strong-privacy tier is told ranking traffic is not covered.
Redesign the clicklog schema to reference a rotating, session-scoped handle instead of a stable node
ID — untested in the corpus, since G-Rank's own similarity score accumulates evidence per peer over
time and a rotating handle would need enough persistent linkability across rotations for clustering
to still function, a property `GOLD-ARXIV-23` does not evaluate. Select a different ranking
mechanism for use under the privacy tier and reserve G-Rank for the non-private tier.

## 4. RLN's freshness requirement and ordinary peer churn (moderate confidence)

`TAHERIBOSHROOYEH-ARXIV-22` (Waku-RLN-Relay) states that every routing peer must keep its local
identity-commitment-tree root synchronized with the registration and removal events a smart
contract emits, and states explicitly that "a peer that falls behind risks proving membership
against a stale root," which the paper says "can expose that peer's leaf index and compromise its
own anonymity." Falling behind is not a rare failure mode in the paper's own model: it is what
happens to any peer that reconnects after being offline longer than the tree has advanced.

`RHEA-USENIXATC-04` builds its own churn experiments around median session times from 1.4 minutes
to 3 hours, and separately cites five independent prior deployed-network measurements (Table 1)
giving median session lengths from about one hour down to about one minute across different P2P
populations. Ordinary participation in a peer-to-peer network of the kind this corpus repeatedly
measures involves frequent reconnection after absences on exactly this timescale.

A peer rejoining after a normal, measured-length absence is in precisely the state
`TAHERIBOSHROOYEH-ARXIV-22` states compromises anonymity: catching up on a tree it fell behind on.
The paper's own Thr parameter (maximum tolerated epoch gap) trades this off explicitly, but the
paper supplies no formula relating Thr to a measured churn distribution, and no other entry in this
corpus supplies one either. This finding rests on typical churn rates rather than on a specific
mechanism whose design choice removes RLN's freshness precondition, so it is reported at lower
confidence than findings 1 through 3.

**Resolution options.** Require a peer to complete tree resynchronization, and hold outgoing
messages, before publishing anything after a reconnection — a stated liveness cost during resync.
Widen Thr to tolerate more drift, accepting the paper's own stated cost of a longer replay window
for stale epochs. Record the missing churn-to-Thr relationship as an open problem, since neither
`TAHERIBOSHROOYEH-ARXIV-22` nor any measurement entry in this corpus quantifies it.

## 5. Single-server PIR's slowly-changing-database assumption and a continuous-update social protocol

`HENZINGER-USENIXSEC-23` (SimplePIR/DoublePIR) requires every client to hold an offline-computed
hint before its first query and states plainly that the paper "does not analyze hint refresh cost
under a continuously updating database." `MENON-USENIXSEC-24` (YPIR) removes the hint-download step
but still requires server-side preprocessing against the current database state before serving
queries, and states that "a database that changes faster than this preprocessing can complete"
forces the server to serve stale precomputation or fall back to unamortized per-query computation.
Both papers leave the cost of a fast-changing, continuously-written database unmeasured.

`KLEPPMANN-CONEXT-24` (Bluesky and the AT Protocol) describes an architecture built around exactly
that kind of database: "A Relay requires every PDS to serve a WebSocket stream of signed repository
updates," and an App View's only input is that continuous stream — the design is a live, unbounded
write-rate index by construction, not an edge case a slower deployment could avoid.

If a private-search or content-location privacy tier over this kind of social index is built on
single-server PIR, the index it must search is exactly the class of database whose preprocessing
cost neither PIR paper analyzes. Serving queries the way `HENZINGER-USENIXSEC-23` and
`MENON-USENIXSEC-24` specify means choosing between answering against a stale snapshot — a
correctness cost with no measured bound in this corpus — or re-running preprocessing at a rate this
corpus records no benchmark for.

**Resolution options.** Restrict the PIR-backed privacy tier to a periodically-snapshotted view of
the index, state the snapshot interval to the user as the tier's freshness cost, and update the
snapshot on that schedule rather than continuously. Scope the private-search tier to a slower-moving
subset of content and serve the live firehose only through the non-private tier. Record the missing
preprocessing-cost-versus-write-rate measurement as an open problem, since it decides whether a
single-server-PIR privacy tier over a live social index is feasible at all.

## Findings not pursued

A candidate pairing between community-detection Sybil defenses requiring one operator to hold the
complete social graph (`CAO-NSDI-12`, `BOSHMAF-NDSS-15`) and a privacy-preserving, hidden-follow-graph
design was considered and dropped: no entry in this corpus describes a concrete mechanism for
hiding a decentralized system's follow graph from every single party, so the pairing had no second
side to cite. A candidate pairing between SplitStream's peak per-node forwarding load
(`CASTRO-SOSP-03`, measured up to 2,971 in one configuration) and the browser's 500-connection cap
(`CHROMIUM-BLINK-SRC`) was considered and dropped: SplitStream's own text defines that figure as
messages received during forest construction, not simultaneous steady-state connections, and the
paper's steady-state per-node forwarding-capacity configurations stay in the tens, well under the
cap. A candidate pairing between regenerating-code repair's need for simultaneous connections to k
or n-1 fragment-holders (`DIMAKIS-TIT-10`) and measured host availability (`BHAGWAN-NSDI-04`) was
considered and dropped: `DIMAKIS-TIT-10` evaluates its own construction against availability traces
down to a mean availability of 0.38 and reports the construction still outperforms its comparison
baseline in every trace but one, where it is "very slightly worse" — the paper's own results do not
support the claim that measured availability breaks its simultaneous-connection requirement.
