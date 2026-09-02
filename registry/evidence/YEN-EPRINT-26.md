## [YEN-EPRINT-26] BeeKEM: Decentralized, Secure and Efficient Group Key Agreement
**Citation:** Derek Yen, Andrés Fábrega, Liangrun Da, Martin Kleppmann, John Mumm, Sunoo Park, Brooklyn Zelenka. "BeeKEM: Decentralized, Secure and Efficient Group Key Agreement." IACR ePrint Archive, Report 2026/1434.
**Retrieved:** full text via https://eprint.iacr.org/2026/1434
**Source URL:** https://eprint.iacr.org/2026/1434
**Domain:** H

This paper is listed in `BRIEF.md` section 7 as already verified in a prior pass ("do not
re-retrieve, do extend"). The summary there is confirmed against the full text on disk; this entry
extends it to the full evidence schema.

### What it does
BeeKEM lets a group of users establish a shared symmetric secret for end-to-end encryption, and
keep updating that secret over time for forward secrecy and post-compromise security, without any
of the users' devices going through a central server, and without requiring the group's messages to
arrive at every device in the same order. This mechanism is called continuous group key agreement
(CGKA): a protocol family that lets a group add members, remove members, and periodically refresh
the shared key. The standardized CGKA protocol underlying Messaging Layer Security (MLS, an IETF
standard used by RCS on iOS and Android, Cisco Webex, and Wire) is TreeKEM, which achieves
logarithmic-in-group-size update cost but requires a central delivery service to impose a single,
total order on every group operation so that every member processes operations in the same
sequence. A prior decentralized CGKA (DCGKA) scheme by Weidner, Kleppmann, Hugenroth, and Beresford
removes the central-server dependency but pays for it with update cost linear in group size.
BeeKEM is the first DCGKA scheme the paper is aware of that matches TreeKEM's logarithmic update
cost in the common case (no concurrent updates), while degrading gracefully — not catastrophically
— to linear cost as the rate of concurrent updates increases, and while carrying a full security
proof.

BeeKEM represents the group's key material as a perfect binary tree, following the general
TreeKEM/MLS design: each leaf corresponds to one group member and holds that member's current
public key; each inner node holds a public key and one or more encrypted copies of the
corresponding private key, encrypted so that either child of that node can decrypt it from its own
secret key and its sibling's public key. The decryption step uses a non-interactive key exchange
(NIKE): a scheme letting two parties who each know only the other's public key compute a shared
symmetric key with no protocol messages exchanged (elliptic-curve Diffie-Hellman is the concrete
instantiation used in the paper's implementation). A member can therefore recover the group secret
at the root by walking from her own leaf to the root, deriving one shared key per level from her own
current secret key and the public key of the sibling node at that level.

Membership changes and key refreshes are recorded as an append-only hash-linked graph of operations
(an operation graph, structured as a hash-based directed acyclic graph analogous to a Git commit
history), rather than a single linear log; each user's device stores its own local copy of both the
tree and the operation graph, and applies a deterministic materialization function to compute the
current tree state from whatever subset of the operation graph it has received. Because different
devices may receive operations in different orders during a network partition, the materialization
function is designed for strong convergence — any two devices that have observed the same set of
operations compute an identical tree, regardless of the order they arrived in — together with three
further named properties: remove-liveness (a removed member is absent after any merge that includes
their removal), add-liveness-under-remove-wins (an added member is present after merge unless
concurrently removed, in which case the removal takes precedence), and no-secret-after-merge (only
an explicit Update operation, never a merge of concurrent operations by itself, establishes a new
group secret). The paper states that a reader familiar with conflict-free replicated data types
(CRDTs, a family of data structures designed so that independent replicas that have applied the same
set of updates always converge to the same state, regardless of the order those updates were
applied in) will recognize this vocabulary, and states plainly that BeeKEM itself is a CRDT.

When updates happen concurrently on different branches of a network partition, the same tree node
can end up with more than one valid version — one per branch — which the paper calls a conflict
node. Rather than requiring agreement on which version is authoritative, BeeKEM has every member who
"ought" to have access to a conflict node's secret compute their own encryption of that secret under
each of their currently known public keys, so a later member who applied a causally subsequent
update supersedes the conflict and re-establishes a single version. A subsequent Update operation
(not the passive act of merging) is what collapses a conflict back into a single defined group
secret; until an Update happens, the group secret at the root of a still-conflicted tree is treated
as undefined.

### Measured results

| Result | Conditions |
|---|---|
| Best-case (fully sequential, no concurrency) per-operation CPU time for Update, Add, and Remove, group sizes 8 to 512 members | Fig. 4: BeeKEM has the lowest measured CPU time of the three systems compared, for both the sender and the recipient roles, across the tested group-size range; the paper states these results without giving individual millisecond values in the extracted text (read from a plotted figure), only the qualitative ranking and the asymptotic classification in Table 1 |
| Asymptotic classification of sender and recipient public-key-primitive invocation counts, message size, and persistent storage, sequential execution, all three systems instrumented to count Diffie-Hellman/HPKE/signature/keypair-generation calls | Table 1: OpenMLS (TreeKEM/MLS) — Update/Remove sender O(log n), recipient O(1), message O(log n) broadcast, storage O(n); Add sender O(log n), recipient O(1), message O(log n) commit plus O(n) welcome. BeeKEM — Update/Remove sender O(log n), recipient O(1) for an existing recipient, message O(log n) broadcast, storage O(n + h_B) where h_B is the size of the operation history; Add sender O(log n), existing-recipient cost O(1), new-recipient cost O(h_B), message O(log n + h_B) including welcome history. WKHB (Weidner et al.'s DCGKA) — Update/Remove sender O(n), recipient O(1), message O(n), storage O(n^2 + h_D) where h_D is the size of WKHB's group-membership history; Add sender O(1), recipient O(1), message O(h_D) welcome history |
| OpenMLS's observed linear (not logarithmic) CPU-time growth at larger group sizes, attributed cause | The paper states this arises because OpenMLS recomputes tree and parent hashes over the whole ratchet tree on each operation, an O(n) operation, even though the core TreeKEM construction itself is O(log n); described as an implementation-specific overhead, not a property of the TreeKEM algorithm itself |
| Per-Update growth in welcome-message size and new-member processing time | Each Update grows the welcome message (the message a newly added member downloads to catch up) by 2.5 kB and increases that member's Process time by 40 microseconds, in the sequential (no-concurrency) benchmark setting |
| Network-partition recovery cost, group of n=64 members split into 4 equal partitions of 16, Update called by U group members sampled uniformly without replacement during the partition, U swept over [0, 2n] = [0, 128] | Fig. 5: total post-partition recovery CPU time and cumulative network traffic rise linearly with U, then plateau once every member has updated at least once (further updates beyond one-per-member add little further cost); the cost of the very first post-partition Update (measured separately, in both CPU time and message size) grows more slowly than the cumulative recovery cost as U increases |
| Benchmark hardware and methodology | All three systems (BeeKEM and OpenMLS in Rust, WKHB in Java) simulated on a single 16-core AMD CPU with 128 GB RAM, all users and the network between them simulated on that one machine; each experiment run 5 times, median reported; standard deviation across the 5 runs stays below 1% of the median for multi-millisecond operations, up to 16% for sub-millisecond operations (stated by the authors as negligible in absolute terms), and error bars are omitted from the figures on that basis |
| Chosen Target Gap Diffie-Hellman-style formal security bound (an analytical, not wall-clock, result) | The DCGKA security proof reduces BeeKEM's security to the security of the underlying NIKE scheme and IND-CPA security of the symmetric encryption scheme, via a game-hop argument (the paper's Theorem, not reproduced numerically here since no concrete numeric security-loss bound is stated in the extracted text beyond the reduction structure itself) |

### Parameters
| Parameter | Value used in the paper | Tested range |
|---|---|---|
| Group size n, best-case comparison (Section 6.1) | Varied | 8, 16, 32, 64, 128, 256, 512 |
| Group size n, partition-recovery experiment (Section 6.2) | 64 | Fixed at 64; not varied in this experiment |
| Number of partitions in the partition-recovery experiment | 4 equal-sized subsets of 16 members each | Fixed |
| Updating members during partition, U | Swept | 0 to 2n = 0 to 128, with resampling without replacement once all n members have updated in a round |
| Key retention parameter κ | Not fixed to one benchmarked value in the performance evaluation; defined as a tunable security/liveness tradeoff parameter (users retain their κ most recent personal secrets) | κ=1 recovers the strongest (FSU/CFS-equivalent) security notions; κ=∞ recovers full Correctness Under Concurrency (CUC); the paper states higher κ degrades forward secrecy and cross-fork security but increases the ability to recover group secrets defined on other branches after a partition heals |
| NIKE and symmetric-encryption instantiation used in the implementation and benchmarks | Elliptic-Curve Diffie-Hellman as the NIKE, ChaCha20-Poly1305 as the symmetric encryption scheme | Fixed; not varied |
| Runs per experiment | 5, median reported | Fixed |
| Benchmark machine | 16-core AMD CPU, 128 GB RAM, single machine simulating all users and network | Fixed |

### Stated limitations
BeeKEM does not achieve full forward secrecy; it achieves a parameterized, weaker form (κ-FSU and
κ-CFS) for two reasons the paper states explicitly. First, a member who has not updated in a long
time must, by the protocol's own correctness requirement, retain access to every group secret
established since her last update, so compromising that member exposes all of those secrets — a
limitation the paper states also affects centralized TreeKEM (there addressed by a definition called
Forward Secrecy with Updates, FSU) and which BeeKEM inherits, generalized to the decentralized
setting. Second, and stated as specific to the decentralized setting: a member who deletes an old
personal secret to strengthen her own forward secrecy loses the ability to decrypt group secrets
defined on a different branch of a network partition once that partition heals, so BeeKEM's ability
to recover secrets after a partition heals (Correctness Under Concurrency, CUC) is in direct tension
with deleting old secrets promptly. The paper states it "conjectures" — its own word — that this
tradeoff between CUC and forward secrecy "may be inherent in decentralized settings," and states
that its alternative construction sketch, BeeKEM^FS, resolves the tradeoff in the opposite direction
(full forward secrecy, at the cost of losing the ability to recover any group secret defined on a
branch a member did not directly participate in). BeeKEM^FS and BeeKEM^PQ (a post-quantum variant)
are both stated as sketches only: the paper writes "we defer a full treatment to future work" for
both, and neither is benchmarked in the evaluation section. The evaluation section explicitly does
not compare BeeKEM's partition-handling behavior (Section 6.2) against the other two systems,
stating MLS cannot operate under partition at all and that Weidner et al.'s DCGKA behaves largely
the same under partition as in the no-partition case, so no partition-specific number for either
comparison system is reported. The paper's security proofs assume the messaging layer supplies
authenticated causal broadcast (ACB) — a communication primitive guaranteeing causally-ordered,
reliable, and authenticated message delivery — while the paper states its actual implementation
constructs ACB from a strictly weaker primitive, a reliable broadcast protocol (RBP, such as a
gossip network), using a hash DAG and digital signatures; the gap between what the proofs assume and
what the implementation is built on is bridged by a construction the paper cites to prior work
rather than proves itself in this paper.

### Requirements it places on the rest of the system
BeeKEM requires a public key infrastructure (PKI) external to the protocol, treated as a black box,
that lets a user obtain another user's initial public key before adding them to a group; the paper
does not itself supply identity verification or key distribution. It requires a reliable broadcast
protocol (RBP) — the paper's example is a gossip network all group members participate in — as the
minimum communication substrate its implementation depends on, and requires that substrate to be
extended (via a hash DAG plus digital signatures, per the paper's citations) into an authenticated
causal broadcast (ACB) for the formal security proofs to apply as stated: causally-ordered,
eventually-reliable, sender-authenticated delivery, with no requirement of a single total order
across all group members. It requires every group member's device to keep a persistent local copy
of both the BeeKEM tree and the full operation graph (or enough of it to replay from a known-valid
starting point), since a new member's join cost is dominated by replaying the O(n)-sized operation
history, and a device that discards its operation-graph history cannot independently verify or merge
concurrent branches it did not witness firsthand. It requires an underlying non-interactive key
exchange (NIKE) scheme and a symmetric authenticated-encryption scheme whose key spaces are
compatible with each other, and the paper's security reduction depends on the specific security
notion the paper calls HKR-CKS for the NIKE, not merely generic NIKE correctness. The retention
parameter κ is a system-wide (or at minimum per-deployment) policy choice that trades cross-branch
recovery against forward secrecy; the paper does not supply a default or a derivation for what value
of κ a given deployment should use, leaving that choice to whoever deploys the system. Adding a
member requires that member's initial public key be obtainable through the external PKI at add time;
BeeKEM's Add operation itself only blanks the direct path to the new leaf and does not perform any
identity check on the added public key beyond what the PKI already vouches for.

### Contradicts
None found within this batch. `BRIEF.md` section 7's prior summary states BeeKEM "requires only
causal broadcast" as a blanket requirement; this full-text pass finds the paper distinguishes two
levels — the security proofs are stated over authenticated causal broadcast (ACB), while the actual
implementation is built over a strictly weaker reliable broadcast protocol (RBP) with ACB
constructed on top via a separate, cited mechanism. This is a refinement of the brief's summary, not
a contradiction of a measured claim: no other entry in this batch reports a number that disagrees
with a number reported here.

### References worth retrieving
- foundational: M. Weidner, M. Kleppmann, D. Hugenroth, A. Beresford. "DCGKA: Decentralized Group Key Agreement for Secure Messaging." (cited as `[34]`, "WKHB") — the O(n)-update-cost prior DCGKA scheme BeeKEM is benchmarked directly against in Fig. 4 and Table 1.
- competing: J. Alwen, M. Mularczyk, Y. Tselekounis. "Fork-Resilient Continuous Group Key Agreement." (cited as `[8]`) — the centralized-delivery-service scheme the paper states independently achieves logarithmic cost and cross-fork-attack security, but "has not been accompanied by an implementation"; this is the direct comparison point for whether BeeKEM's O(log n)/cross-fork-security combination is unique to the fully decentralized setting or achievable in general.
- foundational: J. Alwen, S. Coretti, Y. Dodis, Y. Tselekounis. (cited as `[7]`) — the source of the FSU (Forward Secrecy with Updates) definition and the UPKE-based TreeKEM-to-full-forward-secrecy fix that BeeKEM^FS is stated to be analogous to.
- foundational/formal-verification: K. Bhargavan, R. Barnes, E. Rescorla. (cited as `[13]`) — a formal (F*/DY*) treatment of the MLS membership sub-protocol; the administered-group-membership guarantee a decentralized replacement must reproduce, per this paper's own framing in its related-work discussion.
- competing: R. Barnes, B. Beurdouche, R. Robert, J. Millican et al. — the MLS/TreeKEM RFC (cited as `[10]`/`[12]`) — the centralized standard BeeKEM is positioned as a decentralized alternative to, and whose OpenMLS implementation (`[30]`) is the direct performance comparison in Section 6.
- foundational: M. Kleppmann, H. Howard. "Byzantine Eventual Consistency and the Fundamental Limits of Peer-to-Peer Databases." (cited as `[25]`) — cited alongside the hash-DAG/signature construction of ACB from RBP that the paper's implementation relies on without reproving.
- foundational: M. Kleppmann. "Making CRDTs Byzantine Fault Tolerant." (cited as `[24]`) — cited for the same ACB-from-RBP construction; directly relevant to how BeeKEM's CRDT convergence claim extends to an actively malicious (not just crash-faulty or partitioned) setting, which this BeeKEM paper's stated threat model (honest-but-partition-prone users) does not itself cover.
- attack/adjacent: M. Albrecht, J. Blasco, R. Bjerg Jensen, L. Mareková. "Mesh Messaging in Large-Scale Protests: Breaking Bridgefy." CT-RSA 2021. (cited as `[3]`) — cited for the claim that group chats of thousands of members are used in real protest contexts, the motivating deployment scenario the paper cites for why O(n) DCGKA update cost is "prohibitive."

### Verbatim extracts
"the first decentralized group key agreement protocol with logarithmic update cost in the common case"
"BeeKEM is in fact a CRDT."
"we conjecture the tradeoff between CUC and FS may be inherent in decentralized settings"
"while our proofs assume an ACB, our implementation only requires an RBP"
"We defer a full treatment to future work."
"there is no new group secret defined after the merge of concurrent operations"
