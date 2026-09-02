# Composition conflicts: destroyed preconditions across domains

Agent X. No retrieval performed. This file reports pairs where a candidate mechanism's stated
requirement on the rest of the system is removed by another candidate mechanism's own stated or
proved behavior. Every claim below cites the evidence-file entries it rests on by KEY. Measurement
disagreements are not this family's assignment and none are reported here.

Requirements in `registry/index-requirements.md` were grouped by kind — ordering, observability,
honesty, reachability, stability over time — and checked pairwise across domains. Two candidates
already flagged as destroying each other's preconditions in the brief (square-root replication
against blinded search and against LRU eviction; MLS's total-order requirement against a
partition-tolerant delivery layer) are not repeated here. Eight pairs survive verification against
the full evidence-file text, at varying confidence. Three (findings 2, 3, 6) rest on an explicit
statement in one paper about a property a specific other mechanism destroys. The rest trace a
stated requirement in one paper against a stated behavior in another; those are marked as derived
reasoning, not as a conflict either paper states about the other. Total ordering was checked across
every entry that names it (`BARNES-RFC-23`, `ALWEN-CRYPTO-20`, `KLEIN-SP-21`, `BIENSTOCK-TCC-20`,
`BALBAS-ASIACRYPT-23`, and the rest of the MLS/TreeKEM family); every instance restates the brief's
third seed example rather than a new pair, so none is reported again here.

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

`HEEP-ATNAC-10` (R/Kademlia) is a second, independently measured instance of the same tradeoff, not
a restatement of Rhea's: it adopts recursive routing specifically to beat iterative Kademlia on
latency and bandwidth, and its own simulation quantifies the margin — at a 10,000 s mean node
lifetime, recursive routing without topology adaptation reaches roughly 350 ms mean lookup latency
against roughly 630 ms for iterative routing with five parallel RPCs, and recursive routing combined
with proximity neighbor selection reaches roughly 225 ms, at about one-third the bandwidth of the
iterative-with-PNS configuration. Because recursion is what "the initiator loses control of the
message after the first hop" means in the paper's own description, `HEEP-ATNAC-10`'s routing mode
removes the same querier-side visibility `SIT-IPTPS-02` requires, independent of Rhea's timeout
argument — a second, structurally different reason a churn- and latency-optimized DHT ends up
recursive, and therefore un-auditable by principle 2.

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

## 6. Table-poisoning countermeasures require exactly the secrecy that verifiable-identifier defenses forbid

`SIT-IPTPS-02`'s third design principle requires that a node's identifier be derived by a function
the querier can independently check against the claimant's network address, so a claimed identifier
can be verified rather than trusted. `CASTRO-OSDI-02` builds the same property into certified nodeId
assignment — a routing-table slot filled by "a public, verifiable function" of the identifier — and
its constrained routing table's measured error rates (for example, routing-failure-test false
positives at 0.12 without an attack, rising to 0.77 under nodeId suppression, at collusion bound
c=0.3) hold only once identifiers are unforgeable and checkable in this way.

`MARCUS-EPRINT-18` measures that keeping this exact identifier-to-bucket mapping public is what
enables the table-poisoning eclipse attack it demonstrates against Ethereum's geth client: "the
mapping from a node identifier to its target routing-table bucket... is a public deterministic
function... with no secret salt," letting an attacker precompute node identities landing in a
victim's most heavily weighted buckets before the victim reboots, filling its routing table before
legitimate entries can be reinserted. The paper measures this succeeding in 34 of 51 reboots (66%)
against a 33-day-uptime victim and 44 of 50 reboots (88%) against a 1-hour-uptime victim. The paper's
own recommended fix, Countermeasure 3, is to salt the identifier-to-bucket distance function with a
per-node local secret — which removes the public verifiability `SIT-IPTPS-02` and `CASTRO-OSDI-02`
require for a third party to check a claimed identifier at all.

This is a mechanism-against-mechanism conflict, not mechanism-against-environment: the same public
mapping that lets an honest node verify a peer's claimed identifier is the mapping `MARCUS-EPRINT-18`
shows an attacker uses to precompute table-filling identities, and closing that attack means giving
up the check.

**Resolution options.** Keep the mapping public and accept the eclipse exposure `MARCUS-EPRINT-18`
measures. Salt the mapping locally per Countermeasure 3 and give up third-party verifiability of
claimed identifiers, substituting some other check — none is evidenced in this corpus as compatible
with both properties simultaneously. Record the conflict as open for whichever routing-table design
is selected.

## 7. IP-bound node identity is undermined by measured Carrier-Grade NAT address sharing

`CASTRO-OSDI-02`'s certified-nodeId mechanism binds a nodeId to a specific IP address specifically
to stop certificate-swapping among colluding attacker-controlled nodes, and requires "a
certificate-revocation or reissuance path for any node whose IP address changes." `ROWSTRON-MIDDLEWARE-01`
(Pastry) states the same convention as one option — a nodeId "typically computed as the SHA-1 hash of
the node's IP address" — which the paper's routing-table-population and hop-count bounds depend on
being close to uniformly distributed. Both treat one externally visible IP address as identifying one
node.

`LIVADARIU-INFOCOM-18` measures that this one-address-one-node relationship does not hold across a
substantial and growing part of the deployed Internet. Carrier-Grade NAT (CGN), which an internet
service provider uses to share one public IPv4 address across many customers, was inferred at 4,191
of 17,400 measured "Transit/Access" autonomous systems (23.9%) and 154,098 of the measured /24 blocks
(3.64%) between July 2014 and September 2016, at a commonly reported configuration of about 100 users
sharing one external address. The paper states its own conclusion directly: "a design that assumes
one externally visible IP address corresponds to one participant, for the purposes of rate limiting,
Sybil resistance, or peer-uniqueness assumptions, cannot assume a fixed compression ratio." The paper
additionally measures "arbitrary address pooling" — one internal address mapped to more than one
external address inside a five-minute window — in 42% of that month's inferred CGN blocks, which
breaks the second half of `CASTRO-OSDI-02`'s assumption: a node's externally visible address can
change inside the certificate's revocation-detection window without the node itself changing, and
stay fixed while the population of physical nodes behind it does not.

**Resolution options.** Bind node identity to a public key rather than an IP address —
`ROWSTRON-MIDDLEWARE-01` states this as an available alternative in the same sentence as the IP-hash
convention, though `CASTRO-OSDI-02`'s specific certificate-revocation trigger was built around IP
change and would need restating around key compromise instead. Accept a degraded Sybil-resistance
bound for the fraction of the population behind CGN, sized against `LIVADARIU-INFOCOM-18`'s measured
prevalence. Record the conflict as open for a design that must support both IP-based identity and a
CGN-heavy client population.

## 8. Regenerating-code repair's simultaneous multi-peer reachability is reduced by measured NAT-traversal limits

`DIMAKIS-TIT-10`'s regenerating-code repair mechanism requires a newcomer node to connect
simultaneously to k (the Regenerating Code construction) or n−1 (the Optimally Maintained MDS
construction) other fragment-holding nodes and receive coded data from each in the same repair
operation; the paper states this "requires those holders to be locatable and reachable at repair
time," a requirement it does not itself supply, assuming an underlying storage substrate provides
node discovery and connectivity. The paper's own measured bandwidth savings (for example, a newcomer
downloading 0.16M bytes against a full-file 1.0M at k=7) are conditioned on that simultaneous
connectivity succeeding.

`HALKES-NETWORKING-11` measures that simultaneous direct connectivity to an arbitrary peer is far
from guaranteed. Only 21% of peers are directly connectable without any NAT-traversal mechanism
(Trial 1, 646 classified peers); UDP hole punching through a rendezvous peer raises the reachable
population, but even between peer types the paper classifies as eligible for it, connection success
is measured at 85% per attempt for the most favorable pairing and at approximately 41% for
first-attempt success for the pairing the paper calls the largest obstacle to connectability. Both
figures are pairwise attempt rates, not the joint probability of k or n−1 simultaneous successes
`DIMAKIS-TIT-10`'s repair operation requires; treating per-pair attempts as independent, the joint
probability of assembling all k connections in one repair operation falls off geometrically as k
grows, and `DIMAKIS-TIT-10`'s own evaluated configurations use k values of 7 and 14.

This is a different failure axis from the `DIMAKIS-TIT-10`/`BHAGWAN-NSDI-04` pairing already
considered and dropped below: `BHAGWAN-NSDI-04`-style availability asks whether a node is up at a
given time, and `DIMAKIS-TIT-10`'s own evaluation already shows its construction tolerant of low
availability traces. `HALKES-NETWORKING-11` measures a structurally different problem — whether two
simultaneously-up peers can open a direct connection to each other at all — which availability traces
do not capture and `DIMAKIS-TIT-10` does not evaluate against.

**Resolution options.** Oversample helper candidates beyond k so that partial connection failure
still leaves enough live sources, sized against `HALKES-NETWORKING-11`'s measured per-pair success
rates. Restrict regenerating-code repair to node subpopulations `HALKES-NETWORKING-11` classifies as
directly connectable or successfully traversable. Record the conflict as open, since neither paper in
this corpus supplies a joint success measurement for k-way simultaneous connection.

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
Whether two simultaneously-up peers can open a direct connection to each other at all is a separate
question availability traces do not answer; that pairing, against `HALKES-NETWORKING-11`'s measured
NAT-traversal success rates, is reported above as finding 8.
