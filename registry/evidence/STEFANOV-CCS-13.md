## [STEFANOV-CCS-13] Path ORAM: An Extremely Simple Oblivious RAM Protocol
**Citation:** Emil Stefanov, Marten van Dijk, Elaine Shi, Christopher W. Fletcher, Ling Ren, Xiangyao Yu, Srinivas Devadas. "Path ORAM: An Extremely Simple Oblivious RAM Protocol." ACM CCS, 2013. DOI 10.1145/2508859.2516660.
**Retrieved:** full text via https://eprint.iacr.org/2013/280.pdf (arXiv:1202.5150 original construction, later published at CCS 2013)
**Source URL:** https://eprint.iacr.org/2013/280.pdf
**Domain:** G

### What it does
Path ORAM (Oblivious Random Access Memory) hides which data a client reads or writes from an untrusted storage server, so that the server observes only a sequence of physical storage accesses statistically indistinguishable from any other access sequence of the same length, regardless of the client's actual logical read/write pattern. The security definition it satisfies (Definition 1) requires that for any two request sequences of equal length, an outside observer cannot distinguish the resulting physical access patterns, and that the protocol returns correct data with overwhelming probability. The mechanism: server-side data is organized as a binary tree of height L, where every node is a "bucket" holding up to Z real data blocks (padded with dummy blocks to always appear full at size Z). Each data block is currently assigned, in a client-held position map, to one uniformly random leaf of the tree; the protocol's invariant is that every block resides either in some bucket along the path from that leaf to the root, or in the client's local "stash." To read or write a block, the client looks up its assigned leaf x in the position map, downloads every bucket along the path from leaf x to the root into its stash, reassigns the block to a freshly and independently chosen random leaf, updates the position map, then writes the path back to the server — greedily placing blocks from the stash (including the requested block) as deep down the path toward their newly assigned leaves as bucket capacity allows, so that stash occupancy stays low. Because the requested block is re-randomized to a new leaf on every access, repeated accesses to the same block do not produce a repeated physical access pattern. To keep the position map itself small (it grows linearly with the number of blocks N in the naive construction), the paper applies a recursion technique: the position map is itself stored as a sequence of smaller ORAMs, each holding the position map for the next level, so that only a constant amount of position-map state remains on the client after recursion.

### Measured results
| Result | Value | Conditions |
|---|---|---|
| Proved asymptotic bandwidth cost, small blocks | O(log^2 N) blocks moved per access | block size B = Omega(log N) bits, recursive Path ORAM, failure probability N^-omega(1) (negligible in N) |
| Proved asymptotic bandwidth cost, moderate blocks | O(log N) blocks moved per access | block size B = Omega(log^2 N) bits (e.g. 4 KB blocks), recursive Path ORAM using block size Theta(log N) during recursion, failure probability N^-omega(1) |
| Proved client storage | O(log N) . omega(1) blocks | recursive Path ORAM, both block-size regimes above |
| Per-access bandwidth formula (non-recursive, exact) | 2 . Z . log(N) blocks per load/store operation (read the path down, then write it back) | bucket size Z held constant, tree height L = ceil(log2 N) |
| Concrete stash-overflow failure bound (worked example, non-recursive) | for stash capacity R log N blocks, server storage 20N blocks, bandwidth 10(log N)^2 blocks/operation, over s load/store operations, failure probability at most 14 . s . log N . 0.625^-R | bucket size Z=5, tree height L=ceil(log N); choosing R = Theta(log s + log log N) . omega(1) drives failure probability to negligible |
| Empirical stash size vs. security parameter lambda (Figure 3/4) | required stash size grows linearly with lambda and is empirically independent of N (verified up to lambda=26) for Z=4 | simulated a single run of ~250 billion accesses after a 1-billion-access warm-up, worst-case round-robin access pattern {1,2,...,N,1,2,...}, measured at N=2^16, bucket size Z=4 |
| Extrapolated max stash size for larger security parameters (Table/Figure 5) | at Z=4: lambda=80 needs stash 89; lambda=128 needs stash 147; lambda=256 needs stash 303. At Z=5: lambda=80 needs 63; lambda=128 needs 105; lambda=256 needs 218. At Z=6: lambda=80 needs 53; lambda=128 needs 89; lambda=256 needs 186 | extrapolated from empirical results for lambda <= 26 (practical security parameters such as lambda=128 cannot be directly simulated, since a feasible-time observed failure would contradict the target security level); worst-case round-robin access pattern; stash size excludes the transiently fetched path |
| Average bucket load per tree level (Figure 6) | for Z in {4,5}, expected bucket load near the root is about 1 block (about 25% full for Z=4, about 20% full for Z=5); Z=3 shows a qualitatively different, worse distribution | worst-case round-robin access pattern, measured across tree levels |
| Hardware secure-processor overhead (cited from Ren et al. and Maas et al., not measured in this paper) | approximately 1.2x to 5x performance overhead on benchmarks including SPEC traces and SQLite queries | on-chip caches used, Path ORAM requests issued only on last-level cache misses |

### Parameters
| Parameter | Symbol | Value used | Notes / range tested |
|---|---|---|---|
| Bucket capacity | Z | small constant; theorem proved for Z>=5; Z=4 used as the practical default | empirically tested Z in {3, 4, 5}; Z=3 gives markedly worse (larger) stash occupancy and the paper states it is unclear how likely stash overflow is at Z=3 |
| Tree height | L | ceil(log2 N) in theoretical bounds; ceil(log2 N) - 1 sufficient in the experiments | -- |
| Block size (non-recursive small-block regime) | B | Omega(log N) bits | yields O(log^2 N) bandwidth |
| Block size (moderate regime) | B | Omega(log^2 N) bits (paper's example: 4 KB blocks) | yields O(log N) bandwidth |
| Stash capacity | R | O(log N) . omega(1) blocks (asymptotic); concrete worked example uses R log N | derived to bound failure probability, not a fixed constant |
| Security parameter | lambda | tested up to 26 directly; extrapolated to 80, 128, 256 | failure probability target 2^-lambda |
| Simulated total accesses | -- | ~250 billion, after 1 billion warm-up accesses | single run, N = 2^16 |

### Stated limitations
The security proof and construction explicitly exclude the timing channel: the paper states that, like all related prior ORAM work, it does not consider information leakage through when or how frequently the client makes data requests, only which physical locations are accessed. Integrity against a malicious (as opposed to honest-but-curious/untrusted-but-passive) server is not the paper's main focus; it is addressed only as an extension in Section 6.4 using a Merkle-tree hash over each bucket, and the paper states it does not focus on integrity in its main presentation. The theoretical stash-overflow bound (Theorem/Main Theorem in Section 5) is proved only for bucket size Z>=5; the paper's own empirical results show Z=4 performing well in practice but state this is not proven, and Z=3 is empirically markedly worse with an unresolved overflow-probability trend. Practical security parameters (for example lambda=128) cannot themselves be validated by direct simulation, because observing a failure at that parameter in feasible simulation time would itself indicate insufficient security; the reported large-lambda stash sizes are extrapolations from empirically measured values only up to lambda=26.

### Requirements it places on the rest of the system
Path ORAM requires the client to hold a stash (local storage measured empirically as usually near-empty, with worst-case size growing linearly in the security parameter lambda and, per the proof, O(log N) . omega(1) asymptotically) and, in the non-recursive construction, a position map whose size grows linearly with the total number of blocks N; the recursive construction removes this linear-growth requirement by storing the position map itself as smaller ORAM instances, at the cost of additional bandwidth (an added O(log N) multiplicative factor for small blocks). It requires every access — whether a logical read or a logical write — to perform the identical download-path/re-randomize/write-back sequence, so the mechanism gives no way to serve a read at lower bandwidth cost than a write, and any layer built on top of it inherits a fixed per-access bandwidth cost regardless of whether the underlying operation needed to move the data. It requires the client to generate an independent, uniformly random leaf label on every access to that block, and requires the server-side bucket capacity Z to be fixed in advance; choosing it too small (Z=3, empirically) produces materially worse stash-overflow behavior. It assumes an honest-but-curious server model for its core privacy guarantee — the server is untrusted but not assumed to tamper with results — and treats defense against a maliciously tampering server as a separable, additional mechanism (Merkle-tree bucket hashing) layered on top rather than a property the base protocol provides. It requires the client itself (its processor, memory, and disk) to be trusted; no part of Path ORAM protects data or access patterns from an adversary that can observe the client's own internal state.

### Contradicts
None found within this batch.

### References worth retrieving
- Foundational: O. Goldreich, R. Ostrovsky, "Software protection and simulation on oblivious rams," Journal of the ACM, 1996 (cited as [14]; originates the ORAM problem).
- Foundational: E. Stefanov, E. Shi, D. Song, "Towards practical oblivious RAM," NDSS 2012 (cited as [35]; source of the security definition this paper adopts).
- Competing: E. Kushilevitz, S. Lu, R. Ostrovsky, "On the (in)security of hash-based oblivious RAM and a new balancing scheme," SODA 2012 (cited as [23]; compared directly in Table 1, O(1) client storage but O(log^2 N / log log N) bandwidth).
- Competing: C. Gentry, K. Goldman, S. Halevi, C. Jutla, M. Raykova, D. Wichs, "Optimizing ORAM and using it efficiently for secure computation," PETS 2013 (cited as [12]; compared in Table 1).
- Competing: K.-M. Chung, Z. Liu, R. Pass, concurrent binary-tree ORAM work (cited as [5]; compared directly in Table 1).
- Competing: E. Shi, T.-H. H. Chan, E. Stefanov, M. Li, "Oblivious RAM with O((log N)^3) worst-case cost," ASIACRYPT 2011 (cited as [31]; the tree-ORAM predecessor this paper improves the bandwidth exponent against).
- Foundational: M. T. Goodrich, M. Mitzenmacher, "Privacy-preserving access of outsourced data via oblivious RAM simulation," ICALP 2011 (cited as [15]).
- Applied/secure-processor: L. Ren, X. Yu, C. Fletcher, M. van Dijk, S. Devadas, "Design space exploration and optimization of path oblivious ram in secure processors," ISCA 2013 (cited as [30]; source of the 1.2x-5x hardware overhead figures cited but not measured in this paper).
- Applied/secure-processor: M. Maas, E. Love, E. Stefanov, M. Tiwari, E. Shi, K. Asanovic, J. Kubiatowicz, D. Song, "Phantom: Practical oblivious computation in a secure processor," ACM CCS 2013 (cited as [25]; FPGA hardware implementation).
- Attack/critique: M. Islam, M. Kuzu, M. Kantarcioglu, "Access pattern disclosure on searchable encryption," NDSS 2012 (cited as [22]; the 80%-query-inference motivating attack on unprotected access patterns).

### Verbatim extracts
- "no information should be leaked about: 1) which data is being accessed; 2) how old it is"
- "the stash has a worst-case size of O(logN)·ω(1) blocks with high probability"
- "the bandwidth usage is O(log(N)) blocks"
- "our ORAM constructions do not consider information leakage through the timing channel"
- "We do not focus on integrity in our main presentation"
- "it is unclear how likely the stash capacity is exceeded when Z = 3"
