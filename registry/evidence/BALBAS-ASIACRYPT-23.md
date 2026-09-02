## [BALBAS-ASIACRYPT-23] WhatsUpp with Sender Keys? Analysis, Improvements and Security Proofs
**Citation:** David Balbás, Daniel Collins, Phillip Gajland. "WhatsUpp with Sender Keys? Analysis, Improvements and Security Proofs." ASIACRYPT 2023. DOI 10.1007/978-981-99-8733-7_10.
**Retrieved:** full text via https://eprint.iacr.org/2023/1385.pdf
**Source URL:** https://eprint.iacr.org/2023/1385.pdf
**Domain:** H

### What it does
Sender Keys distributes group messages so each sender encrypts once with a symmetric key it alone controls, instead of every pair of members running a separate ratchet. Each group member generates one symmetric chain key and one signature key pair (a sender key), and pushes that sender key to every other member over a pairwise two-party channel (in deployment, Signal's Double Ratchet). To send a group message, a member encrypts with its own current chain key, hashes the chain key forward, and signs the ciphertext with its own signature key; other members decrypt by holding a copy of that sender's chain key and verify with the sender's signature public key. The protocol is deployed in WhatsApp and Signal for groups up to 1,024 members. The paper builds the first formal security model for Sender Keys (extending an M-IND group-messaging game with cleanness predicates for challenge, injection, and concurrency) and proves the deployed protocol meets a weak security notion. It then proposes Sender Keys+, a modified protocol that changes two things: an update operation that refreshes every member's chain key in one round, and revised cleanness predicates that permit control-message injection and out-of-order challenges after a channel has healed.

The Sender Keys+ update mechanism works by having the updating member generate a fresh randomness value r and distribute (new chain key, new signature public key, r) over the two-party channels to all other members; every member then re-derives every other member's chain key by applying a keyed hash function to it with r. Because members can be out of sync (some may have sent further messages before receiving the update), each member's chain key is instead advanced by a fixed number of forward-hash steps set by a constant concurrency bound N (the paper suggests N = 100), minus the number of messages ℓ that member is known to have sent out of sync, so all members reach a common chain-key state without transmitting message contents.

### Measured results
None. This is a theoretical cryptographic paper: it presents a security model, security proofs (Theorem 1 for Sender Keys, Theorem 2 for Sender Keys+), and asymptotic communication-complexity statements. No implementation, benchmark, or empirical measurement is reported.

### Parameters
| Parameter | Value | Source |
|---|---|---|
| Deployed group size | up to 1,024 parties (WhatsApp, Signal) | stated, not measured by this paper |
| Concurrency bound N (forward-hash steps per update) | example value 100 | authors' example; stated as "cost of executing 100 hash function calls sequentially is negligible," not a measured latency figure |
| Add operation communication complexity (original Sender Keys) | O(n) for a group of n users | derived, stated in Section 1 |
| Remove operation communication complexity (original Sender Keys) | O(n²) for a group of n users | derived, stated in Section 1 |
| Update/PCS-refresh complexity, naive Signal-style mechanism | O(n²) | derived |
| Update/PCS-refresh complexity, Sender Keys+ mechanism | O(n) | derived, Section 6.2 |
| Remove complexity if the paper's separate (excluded) tweak were used | O(n²) → O(n) | derived, but this tweak is explicitly not incorporated into Sender Keys+ |

### Stated limitations
Sender Keys' control messages carry no per-message authentication of their own; the paper shows a malicious server can mount a censorship attack (make a removed member appear self-removed to others while that member believes someone else removed them) and a "burgle into the group" attack (RMS18) adding arbitrary members, because the server distributes unauthenticated control messages. Post-compromise security (PCS) is weak: a member recovers from state exposure only when another member is removed or when it triggers an on-demand update, and the naive way to extend an update to the whole group costs O(n²) communication, which is why Sender Keys+ exists. PCS is further weakened because Sender Keys relies on pairwise two-party channels for key distribution; if a two-party channel between two members has not "healed" (a paper-defined round-trip parameter, refresh∆) since a prior exposure, key material sent over it remains compromised even after a group-level update or removal. In practice not all member pairs exchange private two-party messages regularly, so those channels stay unhealed, meaning even a manually triggered group update does not necessarily heal the group. Sender Keys also provides only sub-optimal forward security for authentication: an attacker can construct a scenario (Figure 9 in the paper) where a message signed before a state exposure is still successfully injected after it, when the receiving member was offline at the time. The paper's Efficient Remove Operations extension (which would lower removal from O(n²) to O(n)) is deliberately excluded from Sender Keys+ because it does not refresh signature keys, an explicit design tradeoff the authors decline to make. Ratcheting signature keys on every send would strengthen forward security for authentication but is excluded from Sender Keys+ for its added overhead. The authors state as future work: extending the model to randomness manipulation, insider threats, and successful-injection scenarios; benchmarking both protocols (no benchmark exists in this paper); and designing a mechanism to resolve ties among concurrently sent control messages under partial ordering.

### Requirements it places on the rest of the system
Requires authenticated, secure two-party channels between every pair of group members (instantiated with the Double Ratchet in deployment) — every member must independently maintain n−1 such channels. Requires a central server (or equivalent delivery service) that provides total ordering of control messages to all parties; total ordering is not required for application messages. The Sender Keys+ update mechanism additionally requires the assumption of total ordering of control messages specifically to avoid overlapping/conflicting updates. Group membership integrity depends entirely on the server behaving honestly toward control messages, since those messages carry no independent authentication in the base protocol; a malicious server can add or reassign blame for removals undetected. PCS recovery depends on the two-party channel layer actually healing (via round-trip exchange) after any exposure — a mechanism this paper does not supply and states must happen "by default" for the PCS guarantee to hold in practice.

### Contradicts
The commonly assumed folklore that Sender Keys, once updated or after a member removal, restores post-compromise security is explicitly shown false by this paper's channel-healing analysis: PCS is not restored unless the underlying two-party channels have separately healed. No other paper in this corpus's evidence file directly measures Sender Keys, so no cross-paper numeric contradiction is recorded; None found beyond this internal folklore correction.

### References worth retrieving
- foundational: Bhargavan, Barnes, Rescorla. "TreeKEM: Asynchronous Decentralized Key Management for Large Dynamic Groups." Inria research report, 2018.
- foundational: Barnes, Beurdouche, Robert, Millican, Omara, Cohn-Gordon. "The Messaging Layer Security (MLS) Protocol." RFC 9420, IETF, 2023.
- foundational: Alwen, Coretti, Dodis, Tselekounis. "Security analysis and improvements for the IETF MLS standard for group messaging." CRYPTO 2020.
- foundational: Alwen, Coretti, Dodis, Tselekounis. "Modular design of secure group messaging protocols and the security of MLS." ACM CCS 2021.
- competing: Hashimoto, Katsumata, Postlethwaite, Prest, Westerbaan. "A concrete treatment of efficient continuous group key agreement via multi-recipient PKEs." ACM CCS 2021 (HKP+21 — O(n)-sized ciphertexts in all cases, directly compared against Sender Keys+ in Section 6.4 of this paper).
- competing: Weidner, Kleppmann, Hugenroth, Beresford. Decentralised CGKA (WKHB21) — Sender-Keys-like decentralized construction, no group-messaging capture, no message-injection security model (already in corpus context as DCGKA).
- competing: Cong, Eldefrawy, Smart, Terner. "The key lattice framework for concurrent group messaging." IACR ePrint 2022/1531 — builds group messaging from two-party channels, achieves O(n) key-update complexity.
- attack: Rösler, Mainka, Schwenk. "More is less: On the end-to-end security of group chats in Signal, WhatsApp, and Threema." IEEE EuroS&P 2018 (burgle-into-the-group attack, source of the server-injection attack this paper formalizes against).
- attack: Cremers, Hale, Kohbrok. "The complexities of healing in secure group messaging: Why cross-group effects matter." USENIX Security 2021.
- foundational: Balbás, Collins, Vaudenay. "Cryptographic Administration for Secure Group Messaging." USENIX Security 2023 (already in this corpus as BALBAS-USENIXSEC-23).
- foundational: Bienstock, Dodis, Rösler. "On the price of concurrency in group ratcheting protocols." TCC 2020 (already in this corpus as BIENSTOCK-TCC-20).

### Verbatim extracts
- "bringing down the total communication complexity from quadratic to linear in the group size."
- "adding and removing users) respectively have O(n) and O(n²) total communication complexity"
- "even after updates or removals, contradicting folklore assumptions."
- "this mechanism requires the assumption of total ordering of control messages"
- "Thus, we do not include this tweak in Sender Keys+."
- "successful adoption for groups of up to 1024 parties in WhatsApp and Signal"
