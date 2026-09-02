## [CHYSTIAKOV-ARXIV-25] Cartesian Merkle Tree

**Citation:** Artem Chystiakov, Oleh Komendant, Kyrylo Riabov. "Cartesian Merkle Tree." arXiv preprint, 2025. arXiv:2504.10944.
**Retrieved:** full text via https://arxiv.org/pdf/2504.10944
**Source URL:** https://arxiv.org/abs/2504.10944
**Domain:** D

### What it does
A Cartesian Merkle Tree (CMT) authenticates set membership and non-membership with a Merkle root while keeping the tree structure independent of insertion order. It achieves this by combining three properties in one node set: a binary search tree ordered on key `k`, a min-heap ordered on a priority `p`, and a Merkle hash `mh` at every node (not only at leaves). The priority of an element is computed deterministically from its key by a hash-derived function `p = PH(e)`, rather than chosen at random as in a classical Cartesian tree (treap). Because priority is a deterministic function of the key, the same key set always produces the same tree shape regardless of insertion order, so the structure is history-independent. Each node's Merkle hash is `mh = H(entry || leftChildMH || rightChildMH)`, with the two child hashes sorted in ascending order before hashing and a missing child treated as hash 0. Insertion places a new node by the binary-search-tree rule on `k` and then rotates it upward while its priority exceeds its parent's, restoring the heap property (mirroring standard treap insertion) and recomputing Merkle hashes along the rotation path. Removal marks the target node's priority as negative infinity and rotates it downward until it is a leaf, then detaches it, recomputing hashes along the path. An inclusion proof carries a `prefix` (the key and sibling Merkle hash of each ancestor up to the root) and a `suffix` (the target node's two child hashes); a verifier reconstructs the accumulator hash bottom-up and compares it to the known root. A non-membership proof instead returns the key of the node whose position would immediately have held the absent key, plus that node's own inclusion path, and the verifier confirms the returned node is genuinely present and that the search rules place the absent key nowhere else.

### Measured results
Benchmarks measure Ethereum Virtual Machine (EVM) gas cost of the Solidity reference implementation's Insert and Remove functions, compared against a Solidity Sparse Merkle Tree (SMT) implementation with its `value` field removed so both structures occupy the same number of storage slots per node. Trees were populated with 100, 1,000, 5,000, and 10,000 randomly ordered elements, using two hash functions, Keccak256 and Poseidon.

| Operation | Hash | Elements | Min Gas | Avg Gas | Max Gas |
|---|---|---|---|---|---|
| Insert (CMT) | Keccak256 | 100 | 97,593 | 187,682 | 301,113 |
| Insert (CMT) | Keccak256 | 10,000 | 97,593 | 303,871 | 552,723 |
| Insert (CMT) | Poseidon | 100 | 148,017 | 599,943 | 1,246,860 |
| Insert (CMT) | Poseidon | 10,000 | 148,017 | 1,140,019 | 2,773,845 |
| Insert (SMT) | Keccak256 | 100 | 102,125 | 248,063 | 667,958 |
| Insert (SMT) | Keccak256 | 10,000 | 102,125 | 339,509 | 877,732 |
| Insert (SMT) | Poseidon | 100 | 136,354 | 471,704 | 903,027 |
| Insert (SMT) | Poseidon | 10,000 | 136,366 | 765,205 | 2,155,222 |
| Remove (CMT) | Keccak256 | 100 | 41,917 | 129,109 | 259,680 |
| Remove (CMT) | Keccak256 | 10,000 | 41,917 | 244,545 | 522,075 |
| Remove (CMT) | Poseidon | 100 | 92,329 | 430,727 | 1,071,617 |
| Remove (CMT) | Poseidon | 10,000 | 92,341 | 982,465 | 2,437,679 |
| Remove (SMT) | Keccak256 | 100 | 35,029 | 131,847 | 224,916 |
| Remove (SMT) | Keccak256 | 10,000 | 35,029 | 237,191 | 374,284 |
| Remove (SMT) | Poseidon | 100 | 35,029 | 284,457 | 466,242 |
| Remove (SMT) | Poseidon | 10,000 | 35,029 | 590,051 | 864,656 |

At 10,000 elements, average Insert gas for CMT with Keccak256 (303,871) is lower than SMT with Keccak256 (339,509) at the same size; average Remove gas for CMT with Keccak256 (244,545) is higher than SMT with Keccak256 (237,191). The paper states operation time complexity is O(log n) for insert, update, and removal, and states the trade-off against SMT as a Merkle proof size "at worst two times larger than SMTs" — this ratio is stated, not shown as a measured table entry in the retrieved text.

### Parameters
- Hash function `H` for Merkle hashing and priority derivation `PH`: instantiated in benchmarks as Keccak256 or Poseidon; the paper states `PH` "can be any deterministic algorithm."
- Dataset sizes tested: 100, 1,000, 5,000, 10,000 elements, chosen "to show how data size impacts performance."
- Storage layout: SMT comparison implementation had its `value` field removed so CMT and SMT nodes occupy the same number of storage slots, to keep the gas comparison fair.

### Stated limitations
The paper states a related structure, the Sparse Merkle Tree, cannot exceed a tree depth of 97 because of EVM stack limitations, and states its collision-free element count is bounded near 2^50 (about 1.12x10^15) by the birthday-problem argument. This bound is stated for SMT in the background section, not asserted as a CMT limitation in the retrieved text — no equivalent explicit bound is stated for CMT's own maximum size in this text. The Incremental Merkle Tree family (background comparison, not CMT itself) is stated to require an off-chain service to reconstruct the tree for proof generation and cannot be used independently on-chain.

### Requirements it places on the rest of the system
A verifier must know the current Merkle root and trust the deterministic priority function `PH` used to build the tree; if a party inserting elements could choose `PH` outputs adversarially, the history-independence property (same key set implies same tree shape regardless of insertion order) would not hold, since the whole point of deriving `p` from `k` deterministically is to remove insertion-order and priority-choice freedom. Proof verification (Algorithm 5) requires the verifier to walk a `prefix` list of ancestor keys and sibling hashes and a `suffix` pair of the target's own child hashes, recomputing hashes bottom-up with the two-child ordering rule (children sorted ascending before hashing) — any implementation must reproduce that exact ordering and concatenation or verification fails. Non-membership proofs require the verifier to independently check that the returned "nonExistenceKey" node's position under the binary-search-tree and min-heap ordering rules is consistent with the claimed absence, not merely that some hash matches.

### Contradicts
None found.

### References worth retrieving
- iden3, "Sparse Merkle Tree" (technical documentation, 2024) — foundational, the structure CMT is directly compared against in the benchmarks.
- DL Solarity, "Cartesian Merkle Tree Solidity Implementation" (GitHub, 2025) — foundational, the reference implementation the benchmarks were run against.
- DL Solarity, "Sparse Merkle Tree Solidity Implementation" (GitHub, 2025) — competing, the comparison implementation used in the gas benchmarks.
- DL Solarity, "Cartesian Merkle Tree Circom Circuit" (GitHub, 2025) — foundational, the zero-knowledge-proof-compatible circuit implementation.

### Verbatim extracts
- "supports insertions, updates, and removals of elements in O(log n) time, requires n space"
- "the only trade-off being a Merkle proof size at worst two times larger than SMTs"
- "if p is deterministically derived from k, then the same key will always produce the same point"
- "reaching depths of 97 or more is currently infeasible due to limitations within the EVM stack"
