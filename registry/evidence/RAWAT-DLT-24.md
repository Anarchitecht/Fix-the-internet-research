## [RAWAT-DLT-24] Accelerating Prolly Trees: Simplified Chunking for Rapid Updates

**Citation:** Abhimanyu Rawat, Tarun Kumar Vangani, Hanno Cornelius, Vanesa Daza. "Accelerating Prolly Trees: Simplified Chunking for Rapid Updates." Distributed Ledger Technologies Workshop (DLT), CEUR-WS, 2024.
**Retrieved:** full text via https://ceur-ws.org/Vol-3791/paper8.pdf
**Source URL:** https://ceur-ws.org/Vol-3791/paper8.pdf
**Domain:** D

### What it does
Lets a distributed system store a large key-value dataset as a content-addressed, ordered tree (a prolly tree, a portmanteau of "probabilistic" and B-tree, first introduced by Noms) that supports Merkle-tree-style verification (a change to one key-value pair changes the tree's root hash) plus B-tree-style ordered range access, while restructuring only a small, bounded portion of the tree on each individual insertion, deletion, or update — instead of the cascading rechunking that the paper attributes to prior prolly-tree designs (Dolthub, Canvas/okra, IPLD).

The tree's shape is content-defined: a node at level 0 stores one key-value pair and is hashed with SHA-256 (Secure Hash Algorithm, 256-bit output); a node is promoted ("boundary node" status) to the next level up when its hash's rightmost hexadecimal digits fall below a fixed threshold. Because promotion depends only on a node's own content hash, any two participants building the same underlying key-value data independently produce the identical tree — the property that content-addressing gives for reconciliation and verification. The paper models the process as Q equally sized hash-value segments, giving each node an independent probability `P_b = 1/Q` of becoming a boundary node, and derives the expected tree height for N total nodes as `H ≈ log_Q(N)` from that probability. A "bucket" or "chunk" is the run of non-boundary nodes at one level between two consecutive boundary nodes; each boundary node stores the rolling Merkle hash of all nodes in its own chunk, so a chunk's contents can be compared or verified as a single hash without inspecting every node in it.

The paper's specific contribution is an Anchor Node placed at the rightmost end of every level, rather than at the left end as in the Canvas/okra design, and absent entirely from the Dolthub and IPLD designs per the paper's characterization of them. The Anchor Node is always treated as a boundary node by construction and functions as a running accumulator for whichever nodes at that level have been inserted most recently but have not yet triggered a boundary-node promotion elsewhere. Because new insertions land at the right edge of the structure and the Anchor Node absorbs their effect on the Merkle hash chain, a sequential insertion updates only the Anchor Nodes on the path from the insertion point up to the root, leaving every previously-formed chunk elsewhere in the tree untouched; a random (non-sequential) update instead touches only the one chunk directly containing the updated key, and its rolling hash update propagates only as far up as that chunk's own boundary node.

Update proceeds in three steps, given as explicit algorithms (Algorithm 3): `SearchPosition` descends from the root, at each internal node following the child whose key range could contain the target key, then moves left along the leaf level until it finds the target key's position; the update (insertion, deletion, or value modification) is applied at that position; `UpdateHashes` then recomputes the Merkle hash of the node's own chunk, and if that chunk's boundary node's hash itself changes, recursively finds and updates the next boundary node up, continuing until a level's hash is unaffected or the root is reached. The paper states this recomputation touches a maximum of two chunks for insertion in the common case. Deletion removes the node from every level it appeared at and updates the affected chunk's Merkle hash; the paper states deletion carries probability `1/b` (where `b` is the chunking factor, i.e. the expected chunk size implied by the threshold `Q`) that the deleted node's removal causes its chunk to merge with an adjacent chunk.

The design supports batch insertion: multiple key-value pairs inserted together are treated as a pre-formed miniature subtree grafted into the larger tree at the insertion point, between two existing boundary nodes, avoiding the restructuring that inserting the same pairs one at a time would otherwise trigger. The design also supports subtree segmentation: because tree height is deterministic given the data (per the `H ≈ log_Q(N)` model) rather than dependent on insertion history, any chunk can function as a self-contained, independently comparable subtree — the paper states this is useful for lightweight clients (it gives Internet-of-Things blockchain clients as the example) that cannot hold the full tree.

### Measured results
Benchmark hardware: a 13th Gen Intel i7-13700H (20 cores), 64 GB RAM, 1 TB M.2 SSD, Ubuntu 22.04 LTS. Compared against the publicly available benchmark codebases of Dolthub (`dolthub/dolt`) and Canvas/okra (`canvasxyz/okra`), both real-world deployed prolly-tree implementations (Canvas uses libp2p as its network layer in production). Canvas's tree-initialization figures in Table 1 (marked with an asterisk in the paper) are taken directly from Canvas's own publicly posted figures because Canvas's benchmark codebase does not itself support tree-initialization benchmarks; the Dolthub and the paper's own "Proposed" tree-creation and all insertion figures were directly executed by the authors.

Tree creation/initialization time (Table 1, milliseconds, mean of repeated runs with standard deviation given for Dolthub and Proposed; Canvas figures are single reported values from its own published data, no min/max/stddev given):

| Tree type | # Entries | Min (ms) | Max (ms) | Avg (ms) | Std Dev (ms) |
|---|---|---|---|---|---|
| Dolthub | 1,000 | 3.66 | 11.53 | 5.47 | 1.44 |
| Dolthub | 100,000 | 247.25 | 325.52 | 285.07 | 22.31 |
| Dolthub | 1,000,000 | 2,841.58 | 3,614.93 | 3,012.03 | 301.99 |
| Dolthub | 10,000,000 | 34,943.06 | 49,207.39 | 41,398.00 | 5,510.00 |
| Dolthub | 17,000,000 | 47,232.56 | 73,075.68 | 61,987.00 | 11,016.00 |
| Canvas (from Canvas's own published figures) | 65,536 | — | — | 478 | — |
| Canvas (from Canvas's own published figures) | 16,777,216 | — | — | 111,494 | — |
| Proposed | 1,000 | 1.28 | 4.39 | 2.79 | 0.70 |
| Proposed | 100,000 | 184.56 | 241.66 | 210.77 | 18.21 |
| Proposed | 1,000,000 | 1,964.63 | 2,171.78 | 2,049.41 | 67.67 |
| Proposed | 10,000,000 | 19,847.38 | 24,040.66 | 21,623.00 | 1,528.00 |
| Proposed | 17,000,000 | 30,143.14 | 38,940.05 | 34,238.00 | 2,985.00 |

The paper states the proposed implementation is around 30-45% faster than Dolthub for tree creation across these sizes, and around 3 times faster than the Canvas prolly tree (this ratio is derived from the sparse Canvas datapoints — e.g. 111,494 ms for 16,777,216 entries versus a Proposed-tree figure not measured at that exact entry count, so the "3 times" comparison spans different entry counts between the two rows and is not a same-N comparison).

Insertion time (Table 2, milliseconds; same number of unique entries inserted into a pre-existing tree already holding an equal number of entries — e.g. 1,000 new entries into a tree already holding 1,000 nodes):

| Tree type | # Insertions | Min (ms) | Max (ms) | Avg (ms) | Std Dev (ms) |
|---|---|---|---|---|---|
| Dolthub | 1,000 | 2.26 | 6.56 | 3.00 | 1.00 |
| Dolthub | 100,000 | 436.79 | 582.03 | 483.00 | 51.00 |
| Dolthub | 1,000,000 | 4,910.55 | 11,217.01 | 8,632.00 | 2,090.00 |
| Dolthub | 10,000,000 | 61,720.77 | 65,942.95 | 63,828.00 | 1,723.00 |
| Canvas | 1,000 | 8.39 | 20.97 | 12.79 | 4.52 |
| Canvas | 100,000 | 658.71 | 719.643 | 679.25 | 10.49 |
| Canvas | 1,000,000 | 11,658.26 | 13,265.09 | 12,268.73 | 552.03 |
| Canvas | 10,000,000 | 153,112.30 | 159,895.32 | 154,708.51 | 1,608.02 |
| Proposed | 1,000 | 1.95 | 4.13 | 2.00 | 1.00 |
| Proposed | 100,000 | 234.34 | 293.89 | 264.00 | 16.00 |
| Proposed | 1,000,000 | 4,178.30 | 5,130.71 | 4,661.00 | 373.00 |
| Proposed | 10,000,000 | 47,975.28 | 49,631.20 | 48,804.00 | 676.00 |

For insertion, Table 2 was generated by executing the publicly available benchmark codebase of both Dolthub and Canvas directly, unlike the asterisked Canvas creation figures in Table 1. At 10,000,000 insertions, the proposed implementation's average time (48,804 ms) is roughly 24% faster than Dolthub's (63,828 ms) and roughly 3.2 times faster than Canvas's (154,708.51 ms).

### Parameters
Hash function: SHA-256, applied to each level-0 node's key-value content and to each higher-level node's own re-hashed content. Boundary-node threshold: the promotion criterion is stated as the node's hash's rightmost hexadecimal digit(s) falling below a predefined threshold; the specific numeric threshold value used for the benchmarked implementation is not given in the paper. `Q`: the number of equally sized segments the hash-value space is divided into for the height model, related to the threshold but not given a specific numeric value in the paper. Expected height formula: `H ≈ log_Q(N)` for N total nodes. Boundary-node probability: `P_b = 1/Q`. Chunking factor `b`: referenced in the deletion-triggered chunk-merge probability `1/b` but not given a numeric value in the paper. Entry counts tested: 1,000; 100,000; 1,000,000; 10,000,000; and (for creation only) 17,000,000 for Dolthub and Proposed; Canvas creation figures are reported only at 65,536 and 16,777,216 (taken from Canvas's own published data, not independently run by these authors).

### Stated limitations
The mechanism by which two prolly trees are compared to compute their difference, and the difference-calculation methodology itself, is explicitly stated to fall outside the scope of this paper; the authors state they provide sample execution code and a brief explanation in an appendix rather than a full treatment. The paper's model for expected tree height (`H ≈ log_Q(N)`) rests on two explicitly stated assumptions — uniform distribution of the hash function's output across its range, and independent selection of each node as a boundary node — neither of which is separately verified or measured in the paper; both are standard cryptographic-hash assumptions asserted, not tested. The Canvas tree-initialization figures used for comparison in Table 1 are taken from Canvas's own previously published figures rather than independently re-executed, because the authors state Canvas's own benchmark codebase does not support tree-initialization benchmarks; those specific rows are therefore not run on the same hardware as the Dolthub and Proposed rows in that table, unlike the insertion figures in Table 2, which were executed on the stated hardware for all three implementations. The authors state future work intends a multi-threaded version of the design to reduce operation time further, implying the benchmarked implementation is single-threaded. No comparison against Merkle Search Trees (MST, Auvolat and Taïani) is run empirically in this paper; MST is discussed only in the related-work section as a structurally similar but distinct design (chunking driven by leading zero count in the hash rather than trailing-digit threshold, and MST explicitly preserves transaction order, which the paper contrasts with prolly trees' content-addressable, non-lexicographic order).

### Requirements it places on the rest of the system
Every participant reconstructing or verifying the same key-value dataset must use the identical hash function (SHA-256, as used here) and the identical boundary-node threshold/`Q` parameter, because chunk boundaries and therefore the entire tree shape are derived deterministically from node-content hashes — two participants using different thresholds produce different, non-comparable trees for the same underlying data. The mechanism assumes the hash function's output is uniformly distributed and that each node's boundary-node status is drawn independently, which is what makes the height model and chunk-size distribution hold; a hash function or dataset that violates this assumption (for example, adversarially crafted keys engineered to bias hash outputs) is not analyzed in this paper, and no defense against such an adversary is given. The transport or storage layer must be able to address and retrieve individual chunks/subtrees independently, since subtree segmentation and lightweight-client use depend on a chunk being separately fetchable and separately verifiable via its own boundary node's rolling Merkle hash, without requiring the full tree. Cross-referencing MEYER-TR-24 in this same corpus: that paper states prolly trees are explicitly not "clamping-invariant" (its term for the property that two structurally different but same-content trees produce identical results when restricted to an arbitrary subrange), because a prolly tree's chunk boundaries are set by a rolling-hash window over consecutive items and clamping an arbitrary range changes which items fall inside that window, changing the resulting boundaries; a range-based set-reconciliation protocol requiring clamping-invariance (as MEYER-TR-24 defines it) cannot be composed directly with this prolly-tree design without an additional adaptation neither paper supplies.

### Contradicts
None found against other entries in this corpus on measured figures. The paper's related-work section (§5) characterizes the Dolthub, Canvas, and IPLD prolly-tree designs as all subject to "similar complexities in tree restructuring due to random updates or insertions" and states each insertion requires certain parts of those trees to update their hashes — these are the authors' own characterizations of competing systems' designs based on reading their published descriptions, not benchmarked against this paper's own measurements of those systems' restructuring cost (the paper measures Dolthub's and Canvas's total insertion/creation time, not their restructuring scope per operation), so a reader should treat the restructuring-scope claim as an architectural comparison, not a directly measured one.

### References worth retrieving
- competing: Auvolat, Taïani. "Merkle search trees: Efficient state-based CRDTs in open networks." SRDS 2019. (Cited as [19]; the structurally closest alternative n-ary Merkle tree design, using leading-zero-count-based promotion rather than trailing-digit threshold; already flagged by MEYER-TR-24 elsewhere in this corpus and worth retrieving to check this paper's characterization of MST's order-preservation property directly.)
- foundational: Boodman. "Prolly trees: Probabilistic B-trees." Noms documentation, 2021 (cited as [9], the original prolly-tree introduction this paper's design extends).
- competing: Sehn (Dolthub). "Prolly trees" blog post, 2024, and Son (Dolthub). "How Dolt stores table data," 2020 (cited as [8] and [13]; the Dolthub prolly-tree implementation directly benchmarked against in this paper — retrieve the original design description to verify the paper's characterization that Dolthub lacks an anchor-node concept).
- competing: Gustafson (Canvas). "Merklizing the key/value store for fun and profit," 2023 (cited as [11]; the Canvas/okra prolly-tree implementation directly benchmarked against, and the source of the Table 1 Canvas creation-time figures reused rather than independently measured here).
- competing: IPLD prolly-trees specification, 2022 (cited as [12]; a third prolly-tree implementation discussed but not benchmarked in this paper).
- foundational: Merkle. "A digital signature based on a conventional encryption function." 1987 (cited as [10], the Merkle tree construction prolly trees extend).
- foundational: Bayer, McCreight. "Organization and maintenance of large ordered indices." 1970 (cited as [14], the B-tree construction prolly trees extend).
- foundational: Shapiro, Preguiça, Baquero, Zawirski. "Conflict-free replicated data types." SSS 2011 (cited as [1], the CRDT framing this paper positions prolly trees within).

### Verbatim extracts
"achieving a 30% to 50% enhancement for Dolthub and a multiple-fold increase in performance for Canvas."
"the taller tree selects an Anchor Node at the same level as the shorter tree's root."
"only the Anchor Nodes, extending all the way up to the Root Node, are affected by the Merkle hash updates."
"the mechanisms by which two Prolly trees are compared... fall beyond the scope of this paper."
"In future, we sought to develop a multi-threaded Prolly tree design."
"content-addressable order, thereby not maintaining lexicographical sequence" (contrasted against MST).
