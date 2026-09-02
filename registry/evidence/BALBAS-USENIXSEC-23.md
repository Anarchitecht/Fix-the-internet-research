## [BALBAS-USENIXSEC-23] Cryptographic Administration for Secure Group Messaging
**Citation:** David Balbás, Daniel Collins, Serge Vaudenay. "Cryptographic Administration for Secure Group Messaging." USENIX Security Symposium, 2023.
**Retrieved:** full text via https://eprint.iacr.org/2022/1411.pdf (full version, August 7 2023)
**Source URL:** https://eprint.iacr.org/2022/1411.pdf
**Domain:** H

### What it does
The mechanism enforces group-membership control cryptographically so a subset of members, the administrators, are the only parties who can add or remove members or change the administrator set, instead of that policy being enforced only at the application level or trusted to the delivery server. It defines administrated continuous group key agreement (A-CGKA), an extension of continuous group key agreement (CGKA, the primitive underlying MLS/TreeKEM in which a group derives one shared secret that it updates as membership changes) that adds a correctness notion for group evolution and a security game in which even a fully corrupted non-administrator member cannot forge a message that adds a new user. Two constructions realize A-CGKA on top of any CGKA:

Individual Admin Signatures (IAS): every administrator holds its own signature key pair, registered with a public-key infrastructure (PKI). Every proposal or commit that changes membership must carry the issuing administrator's signature; other members verify against the PKI-registered public key before accepting the change. Administrators may hold optimal forward secrecy by using forward-secure signatures instead of static ones, at no added asymptotic cost.

Dynamic Group Signature (DGS): the administrator set runs a second, separate CGKA instance (CGKA*) among only its own members, and that instance's group secret is used to derive a single shared signing key for the current administrator set. Standard (non-admin) members receive only the resulting admin public key, not the second CGKA's traffic, so administrator turnover costs standard members nothing beyond receiving one new public key.

Both constructions were integrated as an extension to an open-source MLS implementation (adding an administrator-signature proposal type and validation step to the standard MLS commit/process pipeline) and benchmarked.

### Measured results
Benchmarked by modifying the Cisco Go implementation of MLS (github.com/cisco/go-mls) to add the IAS extension, run on a laptop with a 4-core 11th Gen Intel i5-1135G7 processor and 16 GB RAM, using Go's testing package, HPKE with DHKEM(P-256, HKDF-SHA256)/HKDF-SHA256/AES-128-GCM from Go standard libraries. Each data point is the average over 100 iterations that randomized which group members and administrators performed the operation (position in the MLS TreeKEM tree affects cost).

| Measurement | Condition | Result |
|---|---|---|
| Commit-algorithm running time overhead vs. baseline MLS | up to |G|/8 members carrying out admin updates simultaneously (admin update ⊇ standard update) | under 20% overhead |
| Proc-algorithm (commit-processing) running time | admin vs. standard updates, same scenarios as commit benchmark | very similar between admin and standard, increases linearly in number of updates |
| Commit message size, baseline MLS | \|G\|=8, t=2 update proposals | 1.49 KB |
| Commit message size, baseline MLS | \|G\|=128, t=32 update proposals | 17.11 KB |
| Commit message size, IAS-extended MLS | \|G\|=8, t=2 update proposals | 1.56 KB |
| Commit message size, IAS-extended MLS | \|G\|=128, t=32 update proposals | 17.17 KB |
| Commit message size, IAS-extended MLS with t/2 admin updates added | \|G\|=8 case (1 admin update) | 1.60 KB |
| Commit message size, IAS-extended MLS with t/2 admin updates added | \|G\|=128 case (16 admin updates) | 17.65 KB |
| Proposal size, both implementations | standard proposals | 364–366 bytes |
| Proposal size, both implementations | admin proposals | 364–368 bytes |

Two experiment axes: (1) group size |G| swept over {8, 16, 32, 64, 128} at fixed member/admin ratio |G|/|G*|=4 and t=|G*| updaters (t/2 admin-updaters); (2) fixed |G|=64, |G*|=16, number of updates t swept over {0,4,8,...,28} (t/2 admin updates). Four commit scenarios compared in each: standard commit only; standard commit with t update proposals; admin commit with t/2 admin-update proposals only; admin commit with both t update and t/2 admin-update proposals. Absolute running times for commit ranged roughly 0–35 ms and for proc roughly 0–20 ms across the full |G| sweep (read from Figures 12–13; exact per-point values are not tabulated in the text, only plotted).

Asymptotic per-operation additional cost of the two constructions over a plain CGKA (Table 1 of the paper), where t is the number of admin proposals in a commit, s is the cost of one signature or verification (O(λ) for security parameter λ), k is the cost of one signature key-pair generation (O(λ)), and C is the cost of running CGKA*:

| Construction | Message length (admins) | Message length (all members) | Time (admins) | Time (all members) |
|---|---|---|---|---|
| IAS | ts + tk | ts + tk | O(ts + k) | O(ts) |
| DGS | C + s + k | s + k | O(C + s + k) | O(s + k) |

### Parameters
- Group size |G|: swept {8, 16, 32, 64, 128} in benchmarks.
- Administrator-set size |G*|: fixed ratio |G|/|G*| = 4 in the group-size sweep; fixed |G*| = 16 with |G| = 64 in the update-count sweep.
- Number of updating members t: swept {0, 4, 8, 12, 16, 20, 24, 28} with t/2 concurrent admin updates.
- Ciphersuite: HPKE DHKEM(P-256, HKDF-SHA256), HKDF-SHA256, AES-128-GCM.
- Benchmark repetitions: 100 iterations per data point, randomizing member/admin position in the tree.
- DGS admin-CGKA cost C: paper cites an optimistic estimate of O(log m) for m administrators (from prior CGKA constructions) but states it can be O(m) in the worst case.

### Stated limitations
The security definition does not model arbitrary message injection against robustness attacks: if non-administrators are still permitted to commit, a malicious non-admin can send a malformed commit that only some members can process, denying service (not confidentiality) to a subset of members — this can be fixed with the addition of non-interactive zero-knowledge proofs inside TreeKEM, which the paper does not implement. If only administrators are allowed to commit, the schemes are safe from this attack for non-strongly-robust TreeKEM variants such as MLS's, and standard members retain forward secrecy and post-compromise security when their update proposals are committed. The security model does not capture authentication (an incorruptible PKI is assumed throughout) and does not model randomness manipulation or parties that fail to delete state as instructed (no "no-deletion oracle"); the authors state these are left for future work. Multi-group security is not included in the proofs, though the authors state the extension is straightforward. For DGS specifically: enforcing different levels of administration is not straightforward; administrators may lack a reliable view of the current administrator set if the internal CGKA* is vulnerable to insider robustness attacks (mitigated only by deploying a heavier active-security CGKA variant, not evaluated here); and an administrator cannot immediately give up its status — it must send a removal proposal, erase its state, and wait for another administrator to commit, mirroring an existing limitation in ordinary CGKA member removal.

### Requirements it places on the rest of the system
Requires an incorruptible PKI: every party, and separately every administrator, must have a registered, authenticated public key that other parties can retrieve (getSpk/registerKeys), and both IAS and DGS assume this PKI functions correctly throughout — the paper does not model PKI corruption. Requires an underlying CGKA (e.g., MLS/TreeKEM) to already supply forward secrecy and post-compromise security for the shared group secret; A-CGKA is a layer added on top of that primitive, not a replacement for it. DGS specifically requires running a second, independent CGKA instance among only the administrator subset, so the rest of the system must support concurrent membership in two overlapping group-key-agreement sessions per user (main group and admin group) and must track two epoch/generation identifiers (gid and gid*) consistently. The MLS integration in Section 4.3 requires the delivery service to support MLS's extension mechanism (additional proposal types), and requires control-message processing order to follow MLS's existing propose-and-commit ordering.

### Contradicts
None found — no other paper in this corpus's evidence file yet reports comparable A-CGKA benchmark figures. The Tainted TreeKEM comparison (Section 6.1.2) is noted as difficult because Tainted TreeKEM is not formalized in the propose-and-commit paradigm this paper uses, so no numeric comparison is drawn, and the paper does not claim one.

### References worth retrieving
- foundational: Bhargavan, Barnes, Rescorla. "TreeKEM: Asynchronous Decentralized Key Management for Large Dynamic Groups." Inria research report, 2018.
- foundational: Barnes, Beurdouche, Robert, Millican, Omara, Cohn-Gordon. "The Messaging Layer Security (MLS) Protocol." RFC 9420, 2023.
- foundational: Alwen, Coretti, Dodis, Tselekounis. "Security analysis and improvements for the IETF MLS standard for group messaging." CRYPTO 2020.
- foundational: Alwen, Coretti, Jost, Mularczyk. "Continuous group key agreement with active security." TCC 2020.
- foundational: Klein, Pascual-Perez, Walter, et al. "Keep the dirt: Tainted TreeKEM, adaptively and actively secure continuous group key agreement." IEEE S&P 2021 (Tainted TreeKEM, discussed but not numerically compared).
- competing: Weidner, Kleppmann, Hugenroth, Beresford. Decentralised CGKA (WKHB21) — cited as reducing concurrency issues by restricting who can commit, the same motivation as this paper's administrator restriction.
- attack: Rösler, Mainka, Schwenk. "More is less: On the end-to-end security of group chats in Signal, WhatsApp, and Threema." IEEE EuroS&P 2018 (burgle-into-a-group attack this paper's model prevents).
- attack: Albrecht, Celi, Dowling, Jones. "Practically-exploitable Cryptographic Vulnerabilities in Matrix." IEEE S&P 2023 (server takeover of Matrix groups via similar control-message vulnerabilities).
- attack: Katz, Shin. "Modeling insider attacks on group key-exchange protocols." ACM CCS 2005 (insider-attack model this paper's admin restriction mitigates).
- foundational: Devigne, Duguey, Fouque. "MLS: how zero-knowledge can secure updates." ESORICS 2021 (the NIZK-in-TreeKEM fix for the robustness gap this paper leaves open).
- foundational: Bellare, Miner. "A forward-secure digital signature scheme." CRYPTO 1999 (forward-secure signature construction used for optimal-security IAS).

### Verbatim extracts
- "commit algorithm involves less than a 20% overhead when up to |G|/8 members carry out admin updates"
- "proposals used 364 to 366 bytes, and admin proposals used 364 to 368 bytes"
- "we do not model authentication (we implicitly assume an incorruptible PKI)"
- "admins cannot give up their admin status immediately"
- "confidentiality is not compromised under this family of attacks"
- "DGS introduces basically no cost for standard users"
