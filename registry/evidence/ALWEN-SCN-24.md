## [ALWEN-SCN-24] DeCAF: Decentralizable CGKA with Fast Healing
**Citation:** Joël Alwen, Benedikt Auerbach, Miguel Cueto Noval, Karen Klein, Guillermo Pascual-Perez, Krzysztof Pietrzak. "DeCAF: Decentralizable CGKA with Fast Healing." Security and Cryptography for Networks (SCN), 2024. DOI 10.1007/978-3-031-71073-5_14.
**Retrieved:** full text via https://eprint.iacr.org/2024/629.pdf
**Source URL:** https://eprint.iacr.org/2024/629.pdf
**Domain:** H

### What it does
DeCAF is a continuous group key agreement (CGKA) protocol: a group of users maintains a shared, continuously updated key while going online only sporadically and having their protocol messages relayed by an untrusted server or, in the decentralized setting the paper targets, posted to an append-only data structure such as a blockchain. DeCAF replaces TreeKEM's key-replacement update with a secretly key-updatable public-key encryption (skuPKE) scheme: an update samples a pair of public and secret update information that transforms an existing key pair into a new one, rather than replacing it outright, so concurrent updates to the same ratchet-tree node can both be applied instead of one being dropped. Each user holds a path from their leaf to the root of a ratchet tree; an update re-randomizes every key on that path and encrypts the new path secrets to the resolution (the set of uncompromised, non-blanked descendants) of each co-path node, exactly as in TreeKEM, but using the update rather than replace operation of skuPKE. Because both concurrent updates to a node are retained instead of one being discarded, a corrupted user heals — has all their leaked secrets replaced by fresh, unknown-to-the-adversary material — after every corrupted user has issued one update and those updates have propagated through ⌊log(t)⌋ + 1 epochs, where t is the number of currently corrupted users, independent of the group size n and independent of which users happen to update. Add and remove operations follow the mechanism already standardized in Messaging Layer Security (MLS), which the paper states eases adoption.

### Measured results
No empirical measurement; all results are asymptotic communication-complexity bounds proved formally, not benchmarked on an implementation.

| Protocol | Concurrent updates | Epochs to heal t corruptions in group of n | Cumulative sender (upload) communication | Per-user recipient (download) communication | Sender cost of one update after healing |
|---|---|---|---|---|---|
| TreeKEM I (commit-only healing) | No | n | O(n log(n)) | O(n log(n)) | O(log(n)) |
| TreeKEM II (update-proposal healing) | Yes | 2 | O(n) | O(n) | O(n) |
| Causal TreeKEM (Weidner thesis, 2019) | Yes | n | O(n log(n)) | O(n log(n)) | O(log(n)) |
| Bienstock et al. (TCC 2020) | Yes | 2 | O(n²) | O(n²) | O(log(n))* — weak post-compromise security (PCS) only; matching PCS to the others needs O(n) cost after healing |
| Weidner, Kleppmann, Hugenroth, Beresford (CCS 2021, decentralized CGKA / DCGKA) | Yes | 2 | O(n²) | O(n) | O(n) |
| CoCoA (Alwen et al., EUROCRYPT 2022), centralized-server setting | Yes | log(n) | O(n log²(n)) | O(log²(n)) | O(log(n)) |
| CoCoA, decentralized setting (no server crafting per-user messages) | Yes | log(n) | O(n log²(n)) | O(n log(n)²) — loses its recipient-communication advantage | O(log(n)) |
| DeCAF (this paper) | Yes | log(t) | O(n log(n) log(t)) | O(n log(n) log(t)) | O(log(n)) |

Conditions common to every row: n is the group size, t is the number of corrupted users out of n (unknown to the protocol, which does not know its identity is corrupted), and all users are assumed to update every epoch — an assumption the authors state is required for TreeKEM I and Causal TreeKEM to reach the stated epoch counts, and that could be reduced for TreeKEM II, Bienstock et al., and Weidner et al. by an oracle-optimal, unrealizable choice of which users update. The concrete worked example in the paper: for t = 4 corrupted users prioritized left-to-right in the tree, CoCoA needs ⌈log(n)⌉ + 1 = 4 epochs to heal and DeCAF needs ⌊log(t)⌋ + 1 = 2 epochs.

### Parameters
- t: number of corrupted users, unknown to the protocol; the healing time is stated as a function of t, not of which users are corrupted.
- k: a block-batching parameter for the blockchain instantiation — the ratchet tree is updated only every k blocks, so a message referencing a given tree version can be included in any of the next k blocks. The paper states k should not be chosen larger than necessary, because only one update per k-block epoch counts toward healing (unless a corruption occurs strictly between two updates inside the same k-block window). No numeric value for k is given or tested; it is left as an implementation choice.
- Security-proof bound: with an IND-CPA-secure skuPKE instantiation and random-oracle-modeled hash functions, DeCAF is (O(εEnc · 2(nQ²)²), t, Q)-secure in the active-security CGKA game, where εEnc is the skuPKE encryption adversary's advantage, t is adversary running time, and Q is the number of oracle queries in the security game.

### Stated limitations
DeCAF's forward secrecy is stated as slightly weaker than TreeKEM's, because of a potential delay until other users receive and process a given update message — the paper does not quantify this delay. Every user must process every other user's updates (unlike CoCoA, where at most log(n) other updates matter to a given user), so DeCAF's download communication is larger than CoCoA's in the centralized-server setting; the authors state DeCAF and CoCoA are "incomparable" under a central server, with the choice depending on context, and DeCAF is preferable only once the decentralized setting is assumed. Recording every protocol message on a permissionless blockchain is stated as potentially expensive, because permissionless chains such as Bitcoin or Ethereum have slow block-arrival and confirmation times and a nontrivial per-transaction cost; the paper's proposed mitigation — posting only a hash of each block's messages on-chain and keeping the messages off-chain — is stated to lose the robustness property described below unless the data-availability problem is solved separately, which the paper does not address. Deleting outdated ratchet-tree secret keys for forward secrecy must, on a longest-chain (forkable) blockchain, wait until the relevant block is considered confirmed, or a user risks losing group access on a fork; the paper does not give a confirmation-depth value. The comparison to Causal TreeKEM notes that Causal TreeKEM's claimed post-compromise security guarantee — healing in n epochs, with corrupted users unaware of their own corruption — lacks a formal security proof in the source the authors cite (a 2019 master's thesis); DeCAF's own proof is formal.

### Requirements it places on the rest of the system
DeCAF requires an append-only, agreed-upon transcript of protocol messages available to every group member — instantiated in the paper as a blockchain, but the authors state a single central server suffices structurally, at the price of losing the properties below. The security proof requires an IND-CPA-secure skuPKE scheme (a concrete instantiation from the computational Diffie-Hellman assumption is given) and models the protocol's hash functions as random oracles. Achieving the three properties the paper attributes to the decentralized setting — resistance to server-driven splitting of the group into inconsistent views, resistance to a server censoring one party's messages indefinitely, and robustness to a single point of failure — requires that every protocol message actually be recorded on-chain rather than only hashed on-chain with the payload held off-chain; recording only a hash requires a separately solved data-availability problem that DeCAF does not supply. Preventing indefinite denial-of-service against one user's healing requires the underlying chain to guarantee liveness (a submitted transaction is included within a bounded number of blocks with high probability) and requires DeCAF's own concurrent-update support, because concurrent updates remove the incentive for other users to flood the mempool to keep one user's update out. Forward secrecy requires each user to delete superseded ratchet-tree secret keys, timed to blockchain finality: immediately on a chain with immediate finality, or only after confirmation depth on a longest-chain protocol — DeCAF does not specify what confirmation depth suffices.

### Contradicts
None found within this batch.

### References worth retrieving
- foundational: Alwen, Coretti, Jost, Mularczyk, "Continuous Group Key Agreement with Active Security," TCC 2020 (this corpus's ALWEN-TCC-20).
- foundational: Bhargavan, Barnes, Rescorla, "TreeKEM: Asynchronous Decentralized Key Management for Large Dynamic Groups," 2018.
- foundational: Barnes, Beurdouche, Robert, Millican, Omara, Cohn-Gordon, "The Messaging Layer Security (MLS) Protocol," RFC 9420, 2023.
- competing: Alwen, Auerbach, Cueto Noval, Klein, Pascual-Perez, Pietrzak, Walter, "CoCoA: Concurrent continuous group key agreement," EUROCRYPT 2022.
- competing: Weidner, Kleppmann, Hugenroth, Beresford, "Key agreement for decentralized secure group messaging with strong security guarantees," ACM CCS 2021 (defines DCGKA — the direct decentralized competitor).
- competing: Weidner, "Group Messaging for Secure Asynchronous Collaboration," Master's thesis, University of Cambridge, 2019 (Causal TreeKEM, the source of the unproven n-epoch PCS claim discussed above).
- competing: Bienstock, Dodis, Rösler, "On the price of concurrency in group ratcheting protocols," TCC 2020.
- competing: Bienstock, Dodis, Garg, Grogan, Hajiabadi, Rösler, "On the worst-case inefficiency of CGKA," TCC 2022.
- foundational: Balbás, Collins, Vaudenay, "Cryptographic administration for secure group messaging," USENIX Security 2023 (this corpus's BALBAS-USENIXSEC-23).
- foundational: Jost, Maurer, Mularczyk, "Efficient ratcheting: Almost-optimal guarantees for secure messaging," EUROCRYPT 2019 (source of the skuPKE primitive DeCAF builds on).
- competing: Cong, Eldefrawy, Smart, Terner, "The key lattice framework for concurrent group messaging," ePrint 2022/1531.
- attack/critique: Cremers, Hale, Kohbrok, "The complexities of healing in secure group messaging: Why Cross-Group effects matter," USENIX Security 2021.
- foundational: Auerbach, Cueto Noval, Pascual-Perez, Pietrzak, "On the cost of post-compromise security in concurrent continuous group-key agreement," TCC 2023.
- irrelevant: X. Coin, "Elixxir architecture brief v2.0" (cited only as a prior example of blockchain-backed messaging, not a CGKA construction).

### Verbatim extracts
- "users will heal after at most log(t) requests, with t being the number of corrupted users"
- "CoCoA requires ⌈log(n)⌉ + 1 = 4 epochs to recover, DeCAF only ⌊log(t)⌋ + 1 = 2"
- "in this setting it is outperformed by DeCAF in every aspect" (referring to the decentralized setting)
- "the number of epochs that it takes to heal depends on the number of corrupted parties, but not on relative update behaviour of users"
- "Causal TreeKEM does not consider FS and PCS is only claimed after each corrupted user issues an update"
