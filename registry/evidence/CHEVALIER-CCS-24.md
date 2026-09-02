## [CHEVALIER-CCS-24] Quarantined-TreeKEM: a Continuous Group Key Agreement for MLS, Secure in Presence of Inactive Users
**Citation:** Céline Chevalier, Guirec Lebrun, Ange Martinelli, Abdul Rahman Taleb. "Quarantined-TreeKEM: a Continuous Group Key Agreement for MLS, Secure in Presence of Inactive Users." ACM SIGSAC Conference on Computer and Communications Security (CCS), 2024. DOI: 10.1145/3658644.3690265.
**Retrieved:** full text via https://eprint.iacr.org/2023/1903.pdf (full version; extended abstract in ACM CCS'24 proceedings)
**Source URL:** https://eprint.iacr.org/2023/1903.pdf
**Domain:** H

### What it does
Quarantined-TreeKEM (QTK) reduces the period during which an offline group member's key material stays valid and readable by an adversary, in a Messaging Layer Security (MLS)-compatible Continuous Group Key Agreement (CGKA). A CGKA is the sub-protocol of MLS that lets every member of a group derive the same shared group key across asynchronous key-update rounds. In standard TreeKEM, the CGKA the MLS RFC 9420 standardizes, forward secrecy (past messages stay unreadable after a future compromise) and post-compromise security (a compromised member's channel heals once that member updates) both require every member, including ones who have gone offline, to update the encryption key on their path in the group's binary key tree, called the Ratchet Tree. A member who stays offline (called inactive) never updates, so that member's key material stays exposed for the member's entire absence, and the MLS standard's only prescribed remedy is eviction after a timeout.

QTK adds a quarantine mechanism run by whichever member is the current committer (the member assembling the next round's Commit message). When a committer detects a member whose key age exceeds a threshold, the committer places that member (called a ghost) into quarantine: the committer blanks the ghost's path in the Ratchet Tree, draws a fresh seed, deterministically generates a new encryption keypair for the ghost, and splits the seed with a (t, m)-threshold secret-sharing scheme (Shamir's scheme in the implementation) into m shares distributed to other group members (shareholders). The committer keeps one share itself and then deletes the ghost's secret key, seed, and its own retained shares beyond the first from its own state, so no single member (including the committer) retains the full key. Two share-distribution methods place the m shares in the tree: the default method piggybacks each share on the already-HPKE-encrypted path-secret ciphertexts the committer sends during its own path update (cheap, but the number of shares depends on tree depth and structure, and can drop as low as two in an unbalanced tree); the horizontal method encrypts each share separately to a fixed set of m recipients (used when the default method would produce too few shares, and always used in the server-aided delivery variant). When a ghost reconnects, it broadcasts a Quarantine End proposal, shareholders return their shares, and if the ghost collects at least t shares per quarantine key generation it reconstructs the seeds and decrypts all buffered messages from its absence; if it cannot, that content is permanently lost for the ghost but the ghost still rejoins the group through a regular Join. QTK supports two message-delivery models: broadcast-only (all handshake traffic, including quarantine-specific Share Distribution and Share Recovery messages, goes to every member, requiring no server capability beyond MLS's own) and server-aided (the delivery server routes quarantine-specific messages only to their intended recipients, lowering communication cost but requiring server-side routing logic beyond plain broadcast).

### Measured results

**Availability (probability a reconnecting ghost recovers all t shares), perfect Ratchet Tree, shareholder unavailability p = 1/2, threshold t = ⌈m/2⌉** (Table 1):

| Tree height h | Default: shares m | Default: failure prob. upper bound | Horizontal: shares m | Horizontal: failure prob. upper bound |
|---|---|---|---|---|
| 3 | 3 | 0.2 | 4 | 0.07 |
| 4 | 4 | 2^-7 | 4 | 2^-10 |
| 8 | 8 | 2^-31 | 8 | 2^-154 |
| 12 | 12 | 2^-127 | 16 | 2^-2,288 |
| 16 | 16 | 2^-511 | 16 | 2^-36,848 |

Groups spanning tree heights 3 to 16 (n from 2^3 to 2^16 users, the range the MLS specification targets) keep failure probability under 2^-10 with threshold t = ⌈m/2⌉, and under 2^-20 for groups above 2^8 users. Below tree height 6 (n < 2^6 users) the horizontal method gives a lower failure probability than the default method at the same target of 2^-10.

**Computational cost**, simulated with an open-source fork of an official MLS Kotlin library, on a laptop Intel Core i7-10510U CPU @ 1.80 GHz, using Shamir secret sharing, default share distribution (Table 2):

| Group size n | Shares m | Regular MLS commit | Quarantine init/update, single ghost | Quarantine init/update, extra ghost | Quarantine key reconstruction |
|---|---|---|---|---|---|
| 8 | 3 | 7 ms | 13 ms | 10 ms | 0.6 ms |
| 32 | 5 | 13 ms | 17 ms | 10 ms | 1.3 ms |
| 128 | 7 | 25 ms | 20 ms | 15 ms | 2.6 ms |
| 1,024 | 10 | 230 ms | 120 ms | 120 ms | 3.5 ms |

A single-ghost quarantine costs roughly the same as a proposal-empty MLS commit in small groups and roughly half that cost in large groups. Cost per additional concurrent ghost drops below the single-ghost cost because per-ghost computation is shared.

**Storage cost**: each shareholder of a ghost's quarantine adds 45 bytes of state (4-byte leaf index, 32-byte share, 4-byte shareholder rank, 1-byte share index, 4-byte creation epoch), plus 41 bytes per additional share from a later quarantine-key update, against an MLS leaf public state (leafNode field) of 829 bytes (classical cryptographic parameters) to 1,981 bytes (post-quantum parameters), per the Table 4 parameter set.

**Communication cost per user of one ghost's quarantine** (Table 3), computed analytically from bounds derived in the paper's Appendix D and the parameter values of Table 4 (X25519/AES-256/ECDSA classical suite; ML-KEM/Kyber post-quantum KEM with a classical ECDSA signature; daily active-user key renewal δ_upd = 1 day; quarantine key renewal δ_quar-upd = 2 days). Best/average/worst-case broadcast-only cost in kB per user, classical setting, versus an active user's own per-period update cost:

| Quarantine length | Group size | Broadcast-only best–avg–worst (kB) | Active user cost (kB) |
|---|---|---|---|
| 7·δ_upd | 8 | 1.9 – 2.5 – 4.2 | 1.9 |
| 7·δ_upd | 65,536 | 5.2 – 13.7 – 17.0 | 5.8 |
| 28·δ_upd | 8 | 4.0 – 6.2 – 12.1 | 4.0 |
| 28·δ_upd | 65,536 | 13.9 – 45.4 – 57.1 | 23.2 |

In the post-quantum setting under the same conditions, worst-case broadcast-only cost for a 28·δ_upd quarantine in a 65,536-user group reaches 547.4 kB per user, against 55.5 kB for an equivalent active user. In the server-aided delivery mode, quarantine communication cost stays close to or below the cost of an equivalent active user's regular updates across the tested group sizes (8 to 65,536) and quarantine lengths (7, 14, and 28 update periods), because only the intended recipients receive quarantine-specific messages rather than the whole group.

### Parameters
| Parameter | Value used | Range tested / notes |
|---|---|---|
| δ_upd (active-user key renewal period) | 1 day (illustrative) | Application-dependent; not derived, stated as an illustrative example |
| δ_quar-upd (quarantine key renewal period) | 2 days = 2·δ_upd | Fixed ratio used throughout |
| Quarantine length δ_quar | 7·δ_upd, 14·δ_upd, 28·δ_upd | Three values tested (short/medium/long) |
| Secret-sharing threshold t | ⌈m/2⌉ | Chosen as a stated security/availability trade-off; failure probability increases at least exponentially with t |
| Number of shares m | h = ⌈log2(n)⌉ (default distribution, perfect tree); minimum m_min = 4 | Tested for tree heights 3–16 (n = 2^3 to 2^16) |
| Shareholder unavailability probability p | 1/2 ("very conservative") | Used for Table 1 bounds |
| n_resend_max (max Share Resend proposals) | 3 | Fixed parameter trading communication cost against availability |
| Group sizes tested (communication cost) | 8, 128, 65,536 | Up to 2^16, cited as the MLS specification's target scale |
| Cryptographic sizes, classical | pk 32 B, ct+tag 48 B, sig (ECDSA) 64 B, spk 33 B, cred (X509-ECDSA) 700 B, leafNode 829 B, s 32 B, int 4 B | — |
| Cryptographic sizes, post-quantum | pk 1,184 B, ct+tag 1,104 B, sig 64 B (classical ECDSA retained), leafNode 1,981 B | KEM = Kyber/ML-KEM; signature left classical |

### Stated limitations
The paper's security analysis assumes a partially active adversary that can corrupt any member and leak all secret state except that member's private signature key, so the adversary cannot impersonate a corrupted member; this follows the same adversarial model as the MLS standard and the cited Tainted TreeKEM analysis. The authors state they leave the case of a fully active adversary — one able to impersonate a corrupted or reconnecting ghost and thereby recover that ghost's quarantine keys and its entire message history since the last key update — as a discussion item (Appendix A.1) with a proposed mitigation (multi-factor or out-of-band reauthentication) whose formal security analysis is left as an open problem for future work. The authors state they do not analyze irregular distributions of inactive users (for example, clustering by time zone), because both MLS and QTK place users in the tree by arrival order. The availability analysis (Table 1, Appendix C) explicitly excludes the horizontal share-distribution method in non-perfect trees from full treatment, stating only that it appears more resilient than the default method by the same evidence that motivated Table 1. If a ghost fails to reconstruct enough shares, forward-looking group content already exchanged during the quarantine is permanently lost to that member; the paper states this outcome as an accepted trade-off, not a solved case. Quarantine does not change the time at which the whole group reaches forward secrecy: a footnote states forward secrecy still requires every ghost either to update after reconnecting or to be evicted, so a single permanently silent inactive member still blocks group-wide forward secrecy under QTK exactly as it does under plain TreeKEM.

### Requirements it places on the rest of the system
QTK requires an underlying TreeKEM-based CGKA with a Ratchet Tree (a full binary tree with users at leaves) and a Propose & Commit round structure, and the authors state it stays compatible with the family of TreeKEM-derived CGKAs in the literature (CoCoA, DeCAF, RTreeKEM, Tainted TreeKEM). It requires an Authentication Service assumed secure enough that member corruption never leaks the corrupted member's signature key or grants a signature oracle — the paper states this is the same assumption RFC 9420 and the cited security analyses make, not one QTK adds. It requires a Delivery Service (a central, untrusted server) capable of at minimum broadcast delivery to the whole group; the higher-throughput server-aided variant additionally requires the Delivery Service to route two message types (Share Distribution Message, Share Recovery Message) to specific named recipients rather than broadcasting them, a capability the paper states is not assumed of a fully general broadcast-only delivery service such as MLS's own baseline. It requires every group member to run a (t, m)-threshold secret-sharing scheme and to retain per-ghost share state (leaf index, share value, shareholder rank, share index, creation epoch) until that ghost either reconnects or is evicted, so any storage-constrained member implementation must budget for this growing state. Each committer must track, per member, the epoch of that member's last key update (field e_pk) so a fixed inactivity threshold δ_inact can trigger quarantine, meaning the tree's public state carries per-leaf metadata beyond plain TreeKEM. Reconstructing lost history for a returning ghost requires the Delivery Service to buffer undelivered messages for at least the duration of that member's quarantine, since QTK's own recovery step explicitly requests buffered content from the Delivery Service after successful key reconstruction.

### Contradicts
None found within this corpus. QTK's specific claim — that quarantine reduces the vulnerability window of an inactive member without eliminating the need for eventual eviction or reconnection — is not commonly summarized elsewhere in a way this entry can check against another KEY in this batch.

### References worth retrieving
- Alwen, Auerbach, Cueto Noval, Klein, Pascual-Perez, Pietrzak, Walter. "CoCoA: Concurrent Continuous Group Key Agreement." EUROCRYPT 2022. — foundational (comparison baseline for post-compromise-security round count)
- Alwen, Auerbach, Cueto Noval, Klein, Pascual-Perez, Pietrzak. "DeCAF: Decentralizable CGKA with Fast Healing." SCN 2024. — competing (reduces healing rounds to ⌈log2(t)⌉+1 for t compromised of n members)
- Alwen, Coretti, Dodis, Tselekounis. "Security Analysis and Improvements for the IETF MLS Standard for Group Messaging." CRYPTO 2020 (introduces RTreeKEM). — competing (the only cited prior work improving TreeKEM's forward secrecy)
- Alwen, Hartmann, Kiltz, Mularczyk. "Server-Aided Continuous Group Key Agreement." ACM CCS 2022. — foundational (basis for QTK's server-aided delivery variant)
- Devigne, Duguey, Fouque. "MLS Group Messaging: How Zero-Knowledge Can Secure Updates." ESORICS 2021. — competing
- Hashimoto, Katsumata, Postlethwaite, Prest, Westerbaan. "A Concrete Treatment of Efficient Continuous Group Key Agreement via Multi-Recipient PKEs." ACM CCS 2021. — competing
- Barnes, Beurdouche, Robert, Millican, Omara, Cohn-Gordon. "The Messaging Layer Security (MLS) Protocol." RFC 9420, 2023. — foundational (the standard QTK extends)
- Bhargavan, Barnes, Rescorla. "TreeKEM: Asynchronous Decentralized Key Management for Large Dynamic Groups." Inria Research Report, 2018. — foundational (origin of TreeKEM)
- Cohn-Gordon, Cremers, Garratt, Millican, Milner. "On Ends-to-Ends Encryption: Asynchronous Group Messaging with Strong Security Guarantees." ACM CCS 2018. — foundational (ART, TreeKEM's architectural predecessor; already a target as COHNGORDON-CCS-18)
- Chevalier, Lebrun, Martinelli, Plût. "The Art of Bonsai: How Well-Shaped Trees Improve the Communication Cost of MLS." ePrint 2024/746. — foundational (source of the depth-balance tree-structure notion QTK's non-perfect-tree availability analysis relies on)

### Verbatim extracts
- "Inactive users ... do not update anymore their encryption keys and therefore represent a vulnerability for the entire group."
- "the confidentiality of the ghost's secret key no longer relies on the security of a single user"
- "setting the secret sharing threshold to half the number of shares ... is sufficient to yield a failure probability that remains under 2−10"
- "the computational cost of our protocol only grows logarithmically with the number of users"
- "the overhead of around 500 kB does not sound unrealistic given the important communication cost that a CGKA already has"
- "the corruption of a group member neither leaks its private signature key nor gives the adversary a signature oracle"
