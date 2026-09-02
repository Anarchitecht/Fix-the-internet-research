## [BARNES-RFC-23] The Messaging Layer Security (MLS) Protocol

**Citation:** Richard Barnes, Benjamin Beurdouche, Raphael Robert, Jon Millican, Emad Omara, Katriel Cohn-Gordon. "The Messaging Layer Security (MLS) Protocol." IETF RFC 9420, 2023. DOI 10.17487/RFC9420.
**Retrieved:** full text via https://www.rfc-editor.org/rfc/rfc9420.html
**Source URL:** https://www.rfc-editor.org/rfc/rfc9420.html
**Domain:** H

### What it does
MLS establishes a shared symmetric group key for two to thousands of clients, with forward secrecy (a past key stays secret after a later compromise) and post-compromise security (PCS, a future key stays secret after a past compromise heals), at a per-change cost that grows with the logarithm of group size rather than linearly or quadratically.

The mechanism is a ratchet tree: a perfect binary tree (a complete balanced binary tree where every leaf sits at the same depth) with one leaf per group member. Each tree node holds a Hybrid Public Key Encryption (HPKE) keypair. The private key of any node is known only to members at leaf nodes descended from it — the tree invariant. To change the group's shared secret while excluding one member, a client encrypts fresh entropy once per node on that member's path to the root (the direct path), producing log(N) ciphertexts instead of N-1 pairwise ciphertexts, where N is group size.

State evolves as a linear sequence of epochs. In each epoch a set of authenticated members shares one epoch secret, from which further keys derive. A member proposes changes (add, remove, update) in a Proposal message; a Commit message applies a set of proposals and starts the next epoch, redistributing a fresh epoch secret over the updated tree so only current members can compute it; a Welcome message equips a newly added member with the state needed to join at that epoch. Two supporting roles sit outside the cryptographic core: an Authentication Service (AS) that lets members verify each other's credentials, and a Delivery Service (DS) that routes messages between participants. The protocol assumes the AS is trusted and treats the DS as largely untrusted — MLS is designed to keep group data confidential and correct even if the DS is compromised, and expects only reliable message delivery from it.

### Measured results
None. RFC 9420 is a protocol specification, not an experimental paper; it states asymptotic costs (see Parameters) but reports no measured latency, bandwidth, node counts, or throughput from any implementation or deployment.

### Parameters
| Parameter | Value / bound | Conditions |
|---|---|---|
| Cost of a group-key change excluding one member, sender-key baseline (pairwise) | O(N) computation and communication | N = group size; used to distribute a fresh sender key to each member individually |
| Cost of achieving PCS with plain shared sender keys | O(N²) key-update messages | to give every member post-compromise security via sender keys, without a tree |
| Cost of a group-key change via the ratchet tree (MLS) | O(log N) HPKE encryptions | perfect binary tree of depth d = log2(N), one ciphertext per node on the excluded member's direct path |
| Tree shape | perfect binary tree, 2^d leaves at uniform depth d, 2^(d+1) − 1 total nodes | fixed structural requirement, not a tuned parameter |

### Stated limitations
The document states its own security analysis is high-level and that a complete analysis is out of scope, deferring to citations in the companion architecture document (BEURDOUCHE-RFC-25). It states MLS provides no confidentiality protection for some messages and fields (Section 16.4), naming group metadata as an exposed category. It states an attacker able to observe messages in transit can learn group state, including potentially group membership, and can mount denial-of-service or selective-message-removal attacks against the group; it recommends carrying MLS messages over TLS or QUIC to mitigate this, placing that mitigation outside the protocol itself. It states the protocol places no requirement on how an implementation represents the ratchet tree internally, so a security or performance property of one representation cannot be assumed of another.

### Requirements it places on the rest of the system
The Delivery Service must deliver a Commit and its accompanying Welcome message in a way that lets every recipient compute the same next epoch state; the specification does not itself provide agreement on which Commit is canonical when two members generate Commits concurrently from the same epoch. The document requires (MUST) that applications establish some way to resolve conflicting Commit messages for the same epoch, either by preventing the conflict from occurring or by a rule that selects one Commit as canonical among several sent in that epoch; it requires this resolution to minimize how long forked or stale group states are retained in memory, and to delete them promptly once no longer needed for forward secrecy. It requires that generating a Commit not modify the sender's own state before acceptance is known, and that a Welcome message not be delivered to a new joiner until its corresponding Commit is known to have been accepted. The protocol assumes an Authentication Service that group members trust to validate credentials; a compromised or misbehaving AS is treated as a distinct, separately analyzed failure mode from DS compromise. The tree invariant (a node's private key known only to leaves in its subtree) must be preserved by every path update, or the confidentiality argument for excluding a removed member fails.

### Contradicts
None found. This entry documents no measured claim, so it neither confirms nor conflicts with another corpus entry's measurements. It is the total-order-imposing baseline that BIENSTOCK-TCC-20, BIENSTOCK-TCC-22, and BARTUSEK-EPRINT-26 reason about, and that BeeKEM (already in corpus) states it removes.

### References worth retrieving
- Cohn-Gordon, Cremers, Garratt, Millican, Milner, "On Ends-to-Ends Encryption: Asynchronous Group Messaging with Strong Security Guarantees" (ART), DOI 10.1145/3243734.3243747 — foundational (the asynchronous ratcheting tree construction MLS's ratchet tree is based on)
- Cohn-Gordon, Cremers, Dowling, Garratt, Stebila, "A Formal Security Analysis of the Signal Messaging Protocol," EuroS&P 2017 — foundational (Double Ratchet analysis, the two-party baseline MLS generalizes)
- Beurdouche, Rescorla, Omara, Inguva, Duric, "The Messaging Layer Security (MLS) Architecture" (MLS-ARCH) — foundational (companion document; already a corpus target as BEURDOUCHE-RFC-25)
- Melara, Blankstein, Bonneau, Felten, Freedman, "CONIKS: Bringing Key Transparency to End Users," USENIX Security 2015 — foundational (key transparency referenced for AS credential handling)
- Bellare, Ng, Tackmann, "Nonces Are Noticed: AEAD Revisited," CRYPTO 2019 — foundational (the AEAD security definitions MLS's sender-data encryption scheme cites)

### Verbatim extracts
- "MLS assumes a trusted AS but a largely untrusted DS."
- "Applications MUST have an established way to resolve conflicting Commit messages for the same epoch."
- "requiring a number of key update messages that scales as the square of the group size"
- "costs that scale as the log of the group size"
- "A group has a single linear sequence of epochs."
- "in size ranging from two to thousands"
