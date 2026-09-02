## [ALWEN-CCS-22] Server-Aided Continuous Group Key Agreement
**Citation:** Joël Alwen, Dominik Hartmann, Eike Kiltz, Marta Mularczyk. "Server-Aided Continuous Group Key Agreement." ACM SIGSAC Conference on Computer and Communications Security (CCS), 2022. Also IACR Cryptology ePrint Archive, Report 2021/1456.
**Retrieved:** full text (source URL not recorded in the registry — this key has no `targets-deduped.json` entry; the paper's own bibliography entry [8] cites its ePrint self-posting at https://eprint.iacr.org/2021/1456)
**Source URL:** https://eprint.iacr.org/2021/1456 (self-cited in the paper's own bibliography; not independently confirmed by a registry record)
**Domain:** H

### What it does
Server-Aided Continuous Group Key Agreement (saCGKA) reduces the per-client bandwidth a group-messaging
member spends processing a group membership change (an "epoch" transition — add, remove, or key update
of a member), by giving the delivery server one narrow, unprivileged computation: an Extract procedure
that turns one sender-uploaded "full packet" into a separate, smaller, personalized "sub-packet" per
receiver, so a receiver downloads only the ciphertext addressed to it rather than the whole uploaded
packet. Continuous Group Key Agreement (CGKA) is the primitive that gives every current member of a
dynamic group a shared, epoch-scoped symmetric key and lets any member propose a membership or key
change; higher-level protocols (Message Layer Security, MLS, is the deployed instance) derive per-message
encryption keys from the CGKA's epoch key. The paper defines saCGKA as a formal generalization of CGKA
in which the server's Extract step is explicit, proves a new, simplified security notion for it (security
holds no matter what the server does; correctness and availability hold only if the server runs Extract
honestly), and gives a concrete protocol, Server-Aided ITK (SAIK), built by modifying MLS's underlying
CGKA (Insider-Secure TreeKEM, ITK) in two ways: replacing ITK's per-recipient public-key encryption with
multi-message multi-recipient public-key encryption (mmPKE), a primitive whose ciphertext for many
recipients is smaller than the concatenation of independent per-recipient ciphertexts; and replacing
ITK's requirement that the sender sign the full packet with a requirement that the sender sign only a
short "confirmation tag" binding the epoch's secrets, membership, and operation history.

### Measured results
All bandwidth figures below are analytically derived from closed-form formulas over the protocol's
message structure (Fig. 5/7 in the paper), evaluated at stated bit-length parameters (Fig. 8), not
measured from a running implementation — the paper states plainly: "we estimated the bandwidth for all
protocols using the formulas ... with bit lengths indicated in Fig. 8." No implementation, wall-clock
timing, or network trial is reported for SAIK itself.

Parameters behind every figure: 256-bit security level; group element 512 bits; hash 512 bits; signature
1024 bits; header 17,784 bits (sender id, epoch id, key package, credentials — estimated from MLS);
public key (Pk) 512 bits; single-recipient ciphertext (Ctx) 1152 bits; multi-recipient ciphertext for X
recipients, mCtx(X) = 512 + X·640 bits.

| Group size N | Metric | SAIK (tree-best-case) | SAIK (tree-worst-case) | ITK (best/worst) | CmPKE |
|---|---|---|---|---|---|
| 10,000 | Sender bandwidth | ~4 KB (0.52% of CmPKE) | 0.8 MB (same as CmPKE) | 4.4 KB – 1.5 MB | 783 KB |
| 10,000 | Max receiver bandwidth | ~2 KB (62% of ITK best-case) | 2 KB (~0.2% of ITK worst-case, ~126% of CmPKE) | 4.4 KB – 1.5 MB | 0.8 KB (~2.4–3.02 KB per the paper's own two figures for CmPKE) |
| 10,000 | Total bandwidth | ~30 MB (~1.3× CmPKE) | up to ~50× ITK's worst-case total | 2×–50× SAIK's total (tree-best to tree-worst) | ~25 MB |

Sender bandwidth grows as O(log N) for SAIK in the tree-best case versus O(N) for CmPKE. Total bandwidth
grows as O(N log N) for SAIK versus O(N) for CmPKE. Every "tree-best-case" figure holds only when the
group's ratchet tree carries no blanked internal nodes and no unmerged leaves (Fig. 2); every
"tree-worst-case" figure holds when every non-leaf node is blanked (Fig. 3); any real execution history
falls between these two bounds, and the paper explicitly declines to report an average over histories,
stating the probability of a given execution history "depends on user and administrator behavior,
general application policies and runtime conditions" and is out of scope.

### Parameters
- Security level: 256 bits, used to fix all group-element, hash, signature, and ciphertext sizes above.
- Tree topology state: tree-best-case (no blanks, no unmerged leaves) versus tree-worst-case (all
  non-leaf nodes blanked) — the two bounds the paper reports; no single "expected" value is derived.
- Group size N tested analytically: swept from small values up to N = 10,000 in the reported comparison
  table and up to arbitrary N in the plotted curves (Fig. 6).
- mmPKE instantiated in the comparison with a Diffie-Hellman-based construction (chosen over a slower
  but post-quantum-secure alternative from the compared paper, to keep the comparison to CmPKE fair on
  cryptographic assumption).

### Stated limitations
The paper explicitly puts "which kinds of policies governing when and which parties initiate CGKA
operations lead to more bandwidth efficient executions for realistic deployments" outside its scope,
calling it "an important topic of future research." The security proof (Section 6) assumes primitives
with perfect correctness; Section 8.2 states this can be relaxed to statistical correctness (true of
most post-quantum lattice constructions) only by adding an explicit correctness-failure game hop, which
loses an additive term in the security bound. Section 8.1 states the base SAIK construction does not
achieve a stronger security predicate (formalized in the paper's Appendix H) because of a concrete
attack: a single corrupted member who both creates a new epoch adding a joiner and later creates a
second, forged epoch admitting the same joiner can leak that joiner's decryption key and forge messages
in the first, otherwise-honest epoch; the paper gives a modified construction (a second key pair sent
encrypted under a join-only key, deleted after joining) that closes this gap. No implementation is
reported, so no wall-clock, memory, or server-load figures exist for SAIK.

### Requirements it places on the rest of the system
The delivery server must be reachable by every group member and must run a specific Extract procedure
(compute the lowest common ancestor of sender and receiver in the group's ratchet tree, or accept
sender-supplied tree indices as an alternative that shifts the computation back to the client) to
produce correctness and availability; the paper's security proof holds even if the server refuses or
corrupts this step, but functionality then breaks. The construction requires an Authenticated Key
Service (AKS) — a public-key-infrastructure component from which parties fetch newly joining members'
current public key for multi-recipient encryption and current verification key for signatures, before
that member has joined; the paper's attack in Section 8.1 depends on this pre-registration step and is
closed only by adding a second, join-specific key pair distributed through the AKS. The server needs to
track (either by parsing packet headers or by trusting client-supplied indices) the shape of the group's
ratchet tree to route sub-packets. The construction assumes an ordering discipline over epoch creation:
its baseline security notion is built on the "history graph" formalism of prior CGKA security work,
requiring group members to agree on and authenticate the semantics (not the literal packet bytes) of the
sequence of operations leading to their current epoch.

### Contradicts
None found against other corpus entries on measured facts. The paper's own comparison numbers for CmPKE
are drawn from HASHIMOTO-CCS-21 (reference [31] in this paper, cited throughout as "CmPKE"); this paper
re-instantiates HASHIMOTO-CCS-21's construction with a Diffie-Hellman-based multi-recipient encryption
scheme rather than that paper's own post-quantum instantiation, for a fair comparison on cryptographic
assumption — a difference in instantiation, not a disagreement over a measured figure.

### References worth retrieving
- **Competing** — Keitaro Hashimoto, Shuichi Katsumata, Eamonn Postlethwaite, Thomas Prest, Bas
  Westerbaan. "A Concrete Treatment of Efficient Continuous Group Key Agreement via Multi-Recipient
  PKEs." ACM CCS 2021, 1441–1462. (Already retrieved in this batch as HASHIMOTO-CCS-21; this is the
  CmPKE construction ALWEN-CCS-22 benchmarks against.)
- **Foundational** — Joël Alwen, Daniel Jost, Marta Mularczyk. "On The Insider Security of MLS."
  Cryptology ePrint Archive, Report 2020/1327. (Defines ITK, the construction SAIK modifies.)
- **Foundational** — Joël Alwen, Sandro Coretti, Yevgeniy Dodis, Yiannis Tselekounis. "Modular Design of
  Secure Group Messaging Protocols and the Security of MLS." ACM CCS 2021. Full version
  https://ia.cr/2021/1083.pdf. (History-graph security formalism this paper's notion builds on.)
- **Foundational** — Katriel Cohn-Gordon, Cas Cremers, Luke Garratt, Jon Millican, Kevin Milner. "On
  Ends-to-Ends Encryption: Asynchronous Group Messaging with Strong Security Guarantees." ACM CCS 2018,
  1802–1819. (Initiated the study of next-generation CGKA protocols for large groups.)
- **Foundational** — Alexandre Pinto, Bertram Poettering, Jacob C. N. Schuldt. "Multi-recipient
  encryption, revisited." ASIACCS 2014, 229–238. (Source of the mmPKE construction SAIK's proof reduces
  to and instantiates.)
- **Foundational** — R. Barnes, B. Beurdouche, J. Millican, E. Omara, K. Cohn-Gordon, R. Robert. "The
  Messaging Layer Security (MLS) Protocol." IETF draft. (The deployed standard SAIK targets.)

### Verbatim extracts
- "server-aided CGKA (saCGKA) which generalizes CGKA and more accurately models how most E2E protocols
  are deployed in the wild."
- "the security should hold no matter what it does" — of the untrusted server.
- "We estimated the bandwidth for all protocols using the formulas ... with bit lengths indicated in
  Fig. 8."
- "for 10K parties, CmPKE requires a client to upload 783KB of data, while ... the sender or receiver
  bandwidth of SAIK is roughly 4KB."
- "the total bandwidth is roughly 25MB for CmPKE and 30MB for SAIK."
- "It is an important topic of future research to better understand which kinds of policies ... lead to
  more bandwidth efficient executions."
