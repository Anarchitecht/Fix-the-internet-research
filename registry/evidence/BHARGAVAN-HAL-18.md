## [BHARGAVAN-HAL-18] TreeKEM: Asynchronous Decentralized Key Management for Large Dynamic Groups

**Citation:** Karthikeyan Bhargavan, Richard Barnes, Eric Rescorla. "TreeKEM: Asynchronous Decentralized Key Management for Large Dynamic Groups — A protocol proposal for Messaging Layer Security (MLS)." Inria HAL technical report hal-02425247, May 2018.
**Retrieved:** full text via https://hal.inria.fr/hal-02425247/file/treekem+%281%29.pdf
**Source URL:** https://inria.hal.science/hal-02425247
**Domain:** H

### What it does
TreeKEM lets a set of devices establish and continuously update one shared group key without any device needing another to be online (asynchronous), and without a trusted central authority computing the key on their behalf (decentralized), at a communication and computation cost that grows with the logarithm of group size rather than linearly.

The mechanism organizes the members of a group of size n as the leaves of a binary tree of height log(n). Each internal node of the tree corresponds to a subgroup consisting of the leaves beneath it, and holds a public/private keypair known only to devices in that subgroup; a device that is a leaf therefore holds keys for up to log(n) ancestor subgroups, up to and including the whole-group key at the root. A device's copath for a given group is the set of sibling nodes along the path from its leaf to the root — the minimum set of subgroup keys it must be given to reconstruct every key on its own path. To update the group key, add a member, remove a member, or rotate its own key, a device (the sender) generates a fresh secret for each node on its path to the root and encrypts each fresh secret once per node using the public keys of the subgroups on its copath, so a recipient anywhere in the tree needs only decrypt the single ciphertext addressed to it and then compute log(n) hash-based key derivations up its own path to arrive at the new root key.

TreeKEM handles concurrent operations — two devices independently modifying the tree without coordination — by defining merge rules: any node receiving two concurrent updates for its own position picks a consistent secret and public key using an ordering rule (for example, preferring the update from a right subtree over one from a left subtree), so the resulting state converges without requiring the sender and every recipient to agree in advance on a total order. Sequential operations get immediate consistency; concurrent operations get eventual consistency, meaning a tree node touched by two unordered operations is temporarily "un-merged" until a later, non-concurrent operation from one of its children resolves it.

### Measured results
None in the empirical sense — the paper reports no benchmark, deployment, or wall-clock measurement. Its "Measured results" are the derived operation-complexity counts in the table below, each an asymptotic or exact symbolic cost as a function of group size n, not a measured runtime.

| Operation | Sender cost (hashes, public-key ops) | Recipient cost (hashes, public-key ops) | ART recipient cost (public-key ops) |
|---|---|---|---|
| Create | n hashes, 2n public-key ops | log(n) hashes, 1 public-key op | 2n |
| Update | log(n) hashes, 2·log(n) public-key ops | log(n) hashes, 1 public-key op | 2·log(n) |
| Add | log(n) hashes, 2·log(n) public-key ops | log(n) hashes, 1 public-key op | 2·log(n) |
| Remove | log(n) hashes, 2·log(n) public-key ops | log(n) hashes, 1 public-key op | 2·log(n) |

Conditions: n is group size; ART is the Asynchronous Ratchet Trees construction (Cohn-Gordon, Cremers, Garratt, Millican, Milner, ePrint 2017/666), for which the paper states send and receive costs are equal, so its recipient-side column is the only ART figure the paper gives directly. The naive non-tree multi-KEM (key encapsulation applied to a group of public keys) baseline, given for comparison, costs O(n) storage, computation, and bandwidth at the sender and O(1) at the recipient for every one of create, add, update, and remove.

### Parameters
| Parameter | Value | Conditions |
|---|---|---|
| Per-device storage for one group of size n it belongs to | O(log(n)) | equal to the number of copath keys needed |
| Per-device storage across m groups of size n each | O(m·log(n)) | stated as the aggregate cost of joining multiple groups |
| Message size sent by an updater | 2·log(n) | log(n) encryptions, each carrying up to log(n) keys, described in the paper's step-by-step derivation |
| Tree shape | binary tree, height log(n), group members at leaves | fixed structural requirement of the construction |

### Stated limitations
The paper states its threat model assumes each device's long-term authentication keys are unaffected by compromise, handled by an unspecified out-of-band mechanism, and explicitly calls this "an undesirable gap in our model" pending evolution of MLS's authentication mechanisms. It states that concurrent-operation guarantees are strictly weaker than sequential ones: two devices removed one after another are fully deauthorized even if both had been compromised, but the same two devices removed concurrently leave a compromising adversary with temporary access to the full group key until a later update propagates. It states that preventing double-join — a device that adds or removes another device thereby gaining implicit control over that device's tree path without being a member of the corresponding subgroups — is solved for user-initiated add/remove and for group-initiated remove (using an algebraic key-combination technique under Diffie-Hellman-based encryption), but that preventing double-join efficiently for group-initiated add "remains an open problem," with the only known fix (encrypting to every key held by a subgroup) adding a significant number of extra encryptions. It states the zero-knowledge consistency-proof mechanism for making group operations independently verifiable was still being worked out in detail at time of writing, offered only as an informal sketch.

### Requirements it places on the rest of the system
The construction requires that when a new device joins a group, some existing member deliver it the current group-messaging key derived from hashing the prior group key with the new root key, because a new device cannot derive this by itself from the tree alone. It requires, for concurrent-operation handling, a merge policy that orders operation types relative to each other — the paper's own example policy runs a series of updates, then removes, then a single add, per time slot — and states this policy must be established in the protocol, not left implicit, because not every pair of concurrent operations produces a sane merged state (its worked examples include two adds landing at the same tree location, and a remove-then-update race that leaks the fresh key to the removed device if ordered the wrong way). It requires, if immediate consistency for concurrent operations is wanted rather than eventual consistency, a delivery service willing to hold a stronger trust role: either serializing all operations into one total order, or acting as an "encrypting serializer" that re-encrypts ciphertexts built against a stale key under the newer key so only a device knowing both old and new secrets can decrypt — and the paper states this second mechanism, if the delivery service colludes with a compromised device, lets that pair delay a removal or update and weaken post-compromise security. It requires an authentication mechanism external to the group-key protocol itself to bind long-term identity keys to devices, since the paper's own model assumes this is supplied out of band.

### Contradicts
None found against another corpus entry's measurement. This is the original, pre-standardization proposal that RFC 9420 (BARNES-RFC-23) formalized as MLS's ratchet tree; BARNES-RFC-23 states costs "as the log of the group size" consistent with this paper's O(log(n)) derivation, and does not report a different asymptotic bound. BEURDOUCHE-RFC-25 cites this exact document (HAL ID hal-02425247, 2018) in its own bibliography, confirming the identification.

### References worth retrieving
- Cohn-Gordon, Cremers, Garratt, Millican, Milner, "On Ends-to-Ends Encryption: Asynchronous Group Messaging with Strong Security Guarantees," ePrint 2017/666 — foundational (the Asynchronous Ratchet Trees construction TreeKEM is compared against operation-by-operation in Table 1)
- Phan, Pointcheval, Strefler, "Decentralized Dynamic Broadcast Encryption," ePrint 2011/463 — foundational (one of the four constructions TreeKEM states it borrows ideas from)
- Abdalla, Chevalier, Manulis, Pointcheval, "Flexible Group Key Exchange with On-Demand Computation of Subgroup Keys," AfricaCrypt 2010 — foundational (the Group Key Exchange line TreeKEM borrows from)
- Smart, "Efficient Key Encapsulation to Multiple Parties," 2005 — foundational (the multi-KEM construction TreeKEM's naive linear-cost baseline and terminology derive from)
- Barnes, Millican, Omara, Cohn-Gordon, Robert, "The Messaging Layer Security Protocol," IETF Internet-Draft, February 2018 — foundational (the draft MLS protocol TreeKEM was proposed for; superseded by BARNES-RFC-23)
- Omara, Beurdouche, Rescorla, Inguva, Kwon, Duric, "Messaging Layer Security Architecture," IETF Internet-Draft, February 2018 — foundational (the draft architecture; superseded by BEURDOUCHE-RFC-25)

### Verbatim extracts
- "using O(log(n)) storage, bandwidth, and complexity, both at the sender and the receiver"
- "this protocol requires O(n) storage, bandwidth, and computation"
- "TreeKEM provides immediate consistency for sequential operations and eventual consistency for concurrent operations"
- "preventing double-join efficiently in group-initiated add remains an open problem"
- "For large groups with thousands of members, linear growth does not scale."
- "an adversary who has compromised both devices still has temporary access to the full group key"
