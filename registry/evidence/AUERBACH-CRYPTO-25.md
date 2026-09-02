## [AUERBACH-CRYPTO-25] Continuous Group-Key Agreement: Concurrent Updates without Pruning
**Citation:** Benedikt Auerbach, Miguel Cueto Noval, Boran Erol, Krzysztof Pietrzak. "Continuous Group-Key Agreement: Concurrent Updates without Pruning." CRYPTO, 2025. DOI 10.1007/978-3-032-01913-4_5.
**Retrieved:** full text via https://eprint.iacr.org/2025/1035.pdf
**Source URL:** https://eprint.iacr.org/2025/1035.pdf
**Domain:** H

### What it does
The paper measures, by formal derivation over a defined random-operation model rather than by implementation, how badly TreeKEM's communication cost degrades under concurrent updates, and then gives a modified update-proposal mechanism, MLS-Cutoff, that removes that degradation for a bounded rate of concurrency. TreeKEM is the continuous group-key agreement (CGKA) construction inside the IETF's Messaging Layer Security (MLS) standard: each of N group members owns a leaf of a binary ratchet tree, each tree node holds a public/secret key pair, and a user updating their key material replaces the keys from their leaf to the root, encrypting each new secret to the public key of the sibling subtree not on their own path — costing log(N) ciphertexts when the tree is fully populated. Concurrent operation uses "propose and commit": several users each broadcast an update proposal (a fresh leaf public key only, no new group secret), and one user later commits, folding every pending proposal into a single new group state. A commit cannot deliver the new keys on a proposing user's path to that path's co-nodes without knowledge the committer lacks, so TreeKEM "blanks" (deletes the key pair of) every non-leaf node on a proposer's update path that is not also on the committer's own path; a blanked node's children absorb its in-degree, so a future commit reaching a blanked node must instead encrypt separately to each of its unblanked descendants, and this growth compounds as more blanks accumulate.

The paper's model, Experiment Exp-Prop-Com, fixes a group of size N = 2^n and, for t rounds, draws P users uniformly at random to each issue one update proposal, followed by C users drawn uniformly at random to each issue a commit (C − 1 of them committing to no proposals, when C > 1, to model proposals issued less often than every commit). The paper derives a closed-form lower bound on the expected commit size under this process (Theorem 4.2, below) and shows the blank rate at a tree node of sufficient depth converges, via the node's blank/populated state forming a Markov chain, to a stationary probability of P/(P+C).

MLS-Cutoff modifies only how proposals are applied to the tree, keeping every other MLS mechanism (authentication, tree-hash and parent-hash consistency checks) unchanged. When a user issues an update proposal, the proposal itself already re-keys the user's full path (unlike plain MLS, where a proposal carries only the new leaf key), but a receiving committer stops applying that re-keying icut steps before the root — the cutoff parameter, set to log(log(N)) — so nodes above the cutoff are never touched by ordinary proposals and stay populated unless two proposing users' paths happen to collide below the cutoff, in which case the tree is blanked from the collision point upward as in ordinary MLS.

### Measured results
No implementation and no real-world trace; every figure below is a bound proved over the paper's own randomized-operation model (Exp-Prop-Com), not a benchmark. The paper states explicitly that real-world CGKA operation-sequence data is not publicly available and that its model is a deliberate simplification chosen for tractability, not a claim of realism.

| Result | Statement | Conditions |
|---|---|---|
| TreeKEM/MLS expected commit-cost lower bound (Theorem 4.2, informal) | E[Cost(t)] ≥ Ω(N · log₂(1 + P/(P+C))) | P proposals and C commits per round constant, t sufficiently large (paper's stated sufficient bound: t > 2N² log(N)), uniform random choice of proposing and committing users each round |
| Small-N refinement of the same bound | E[Cost(t)] ≥ log₂(N)/4 − log(N)/4 | Special case P = C = 1, stated as more informative than the general bound for small N |
| Exponent e = log₂(1 + P/(P+C)) at C = 1, varying P | e = 0.22 (P=1/5), 0.42 (P=1/2), 0.58 (P=1), 0.74 (P=2), 0.87 (P=5), 0.93 (P=10), 0.99 (P=50) | C = 1 throughout; for P < 1 the paper writes P = 1/c with C = c to keep P a rate rather than a per-round integer count |
| Consequence stated in prose | At P = C = 1 (one proposal per commit), expected commit cost is "already over √N"; at P = 50, exponent 0.99 puts cost "almost linear" in N | Same model; MLS's stated target group size is up to 50,000 members (N = 50,000), against which the paper judges neither "almost all updates sequentially" nor "commits become almost linear in N" as acceptable |
| Per-node blank probability | Stationary probability that a sufficiently deep tree node is blank converges to P/(P+C) | Derived from the node's blank/populated transitions forming a Markov chain under the same round process |
| MLS-Cutoff expected proposal/commit size (Lemma 5.2) | E[\|pmsg\|] ≤ E[\|cmsg\|] ∈ O(log(N)) | C = 1, P constant, t sufficiently large, cutoff parameter icut = log(n) = log(log(N)) for N = 2ⁿ |
| MLS-Cutoff expected ciphertext count, explicit form | E[\|CTXT\|] ≤ log(N) + (P(P−1) + 1)·log(N / log(N)) + 1 | Same conditions as Lemma 5.2, derived en route to it |

Context figures the paper cites, not measured by it: Signal caps group size at 1,000 users; MLS's design target is groups up to 50,000 users.

### Parameters
- N: group size, expressed as N = 2ⁿ throughout the analysis.
- P: number of update proposals issued per round, treated as a constant independent of N in every asymptotic result; the worked table above uses P values from 1/5 to 50.
- C: number of commit-only rounds separating proposal rounds (C = 1 means every round includes P proposals followed by one commit; C > 1 models proposals issued less often than commits).
- t: number of rounds run; results require t large enough for the round-level Markov chain to approach its stationary distribution — Theorem 4.2 states t > 2N² log(N) as a sufficient bound.
- icut: MLS-Cutoff's cutoff depth, the number of tree levels near the root left untouched by an ordinary proposal's re-keying; set to log(n) = log(log(N)) to obtain the O(log(N)) bound of Lemma 5.2 — no other value is analyzed.

### Stated limitations
The randomized-operation model is stated by the authors as a deliberate simplification, not a claim about real user behavior: real-world CGKA operation traces are stated to be unavailable, so the uniform-random proposer/committer model was chosen to make the lower-bound proof tractable and its intuition legible, not because it is thought to match deployment. Theorem 4.2's stated t > 2N² log(N) round threshold means the bound is a limiting/asymptotic statement about many rounds, not a bound on cost after any fixed number of operations. Experiment Exp-Prop-Com never removes users from the group, so it never models the blanking that removal itself introduces in either MLS or MLS-Cutoff; the paper argues informally, without proof, that MLS-Cutoff would clear such blanks faster than MLS because of its additional path re-keying on proposals, but does not extend Lemma 5.2 to cover removals. MLS-Cutoff's O(log(N)) bound holds only while P stays constant relative to N; the paper states that once concurrency becomes "massive" (proposals from a number of users linear in group size), a linear communication cost is inherent for any CGKA achieving fast post-compromise security (PCS) built from standard primitives, citing Bienstock, Dodis, Rösler (TCC 2020) — MLS-Cutoff's own worst-case complexity is stated to remain Ω(N), matching plain MLS, for this reason. The paper explicitly leaves evaluating MLS-Cutoff's performance "in more realistic models" — i.e., under non-uniform, potentially adversarial or coordinated operation sequences — as an open question for future work.

### Requirements it places on the rest of the system
The security proof for MLS-Cutoff (Theorem 5.1) is conditioned on the underlying public-key encryption scheme being IND-CCA2 secure, the signature scheme being strongly existentially unforgeable under chosen-message attack (SEUF-CMA secure), and the protocol's hash and key-derivation functions and message authentication code being modeled as random oracles / ideal primitives, matching the assumptions of the MLS insider-security proof (Alwen, Jost, Mularczyk, CRYPTO 2022) that this proof is stated to closely follow. MLS-Cutoff requires the delivery service and every group member to run the same tree-hash and parent-hash consistency checks that MLS already uses, unmodified — the paper's stated design goal is that MLS-Cutoff changes only how the ratchet tree is blanked or populated by applying proposals, leaving every other MLS mechanism for authenticity and consistency intact, so that the modification is deployable inside the existing MLS wire format. Achieving MLS-Cutoff's O(log(N)) result requires the actual deployed proposal/commit rate to stay within the constant-P regime the paper analyzes; a deployment that lets update proposals scale with group size falls back to the Ω(N) worst case shared with plain MLS, so a rate-limiting or scheduling policy elsewhere in the system determines whether MLS-Cutoff's improvement is realized.

### Contradicts
This paper's Theorem 4.2 gives quantitative content — a specific exponent table and a stated "already over √N" figure at P = C = 1 — to a qualitative claim (that concurrent update proposals degrade TreeKEM's communication complexity) that ALWEN-SCN-24 (DeCAF) and ALWEN-TCC-20 state only asymptotically as the same Θ(n)/Θ(log(n)) split TreeKEM I versus TreeKEM II already carries; no numeric disagreement was found between this entry and those two.

### References worth retrieving
- foundational: Bhargavan, Barnes, Rescorla, "TreeKEM: Asynchronous Decentralized Key Management for Large Dynamic Groups," 2018.
- foundational: Alwen, Jost, Mularczyk, "On the insider security of MLS," CRYPTO 2022 (source of the insider-security notion and safety predicate MLS-Cutoff's Theorem 5.1 proves against, and of the proof technique the authors state they closely follow).
- foundational: Barnes, Beurdouche, Robert, Millican, Omara, Cohn-Gordon, "The Messaging Layer Security (MLS) Protocol," RFC 9420, 2023.
- competing: Alwen, Auerbach, Cueto Noval, Klein, Pascual-Perez, Pietrzak, Walter, "CoCoA: Concurrent continuous group key agreement," EUROCRYPT 2022 (the paper states CoCoA achieves logarithmic complexity in this setting by re-keying updaters' full paths, but at the cost of slower post-compromise security and no insider security).
- competing: Weidner, Kleppmann, Hugenroth, Beresford, "Key agreement for decentralized secure group messaging with strong security guarantees," ACM CCS 2021.
- competing: this corpus's ALWEN-SCN-24 (DeCAF, listed in the bibliography as AACN+24), directly comparable on concurrent-update communication complexity.
- foundational: Bienstock, Dodis, Rösler, "On the price of concurrency in group ratcheting protocols," TCC 2020 (source of the Ω(N) inherent-linearity result for CGKA achieving fast PCS from standard primitives, cited to justify MLS-Cutoff's own worst-case bound).
- foundational: Bienstock, Dodis, Garg, Grogan, Hajiabadi, Rösler, "On the worst-case inefficiency of CGKA," TCC 2022.
- foundational: Auerbach, Cueto Noval, Pascual-Perez, Pietrzak, "On the cost of post-compromise security in concurrent continuous group-key agreement," TCC 2023.
- attack/critique: Cremers, Günsay, Wesselkamp, Zhao, "ETK: External-operations TreeKEM and the security of MLS in RFC 9420," ePrint 2025/229.
- competing: Balbás, Collins, Gajland, "WhatsUpp with sender keys? Analysis, improvements and security proofs," ASIACRYPT 2023 (this corpus's BALBAS-ASIACRYPT-23).
- foundational: Balbás, Collins, Vaudenay, "Cryptographic administration for secure group messaging," USENIX Security 2023 (this corpus's BALBAS-USENIXSEC-23).
- competing: Cong, Eldefrawy, Smart, Terner, "The key lattice framework for concurrent group messaging," ACNS 2024.

### Verbatim extracts
- "even if there's just one update proposal for every commit the expected cost is already over √N"
- "provably achieves an update cost of Θ(log(N)) assuming the proposers and committers are chosen at random"
- "a linear communication complexity is... inherent for this type of 'massive' concurrency"
- "MLS aims to support groups containing up to N = 50000 members"
- "Signal limits the group size to 1000 users"
