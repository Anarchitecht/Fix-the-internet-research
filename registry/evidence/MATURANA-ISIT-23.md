## [MATURANA-ISIT-23] Locally Repairable Convertible Codes: Erasure Codes for Efficient Repair and Conversion
**Citation:** Francisco Maturana, K. V. Rashmi. "Locally Repairable Convertible Codes: Erasure Codes for Efficient Repair and Conversion." IEEE International Symposium on Information Theory (ISIT), 2023. pp. 2033-2038. DOI: 10.1109/ISIT54713.2023.10206604.
**Retrieved:** full text via https://doi.org/10.1109/ISIT54713.2023.10206604
**Source URL:** https://doi.org/10.1109/ISIT54713.2023.10206604
**Domain:** C

### What it does
This paper lowers the data-transfer cost of changing an erasure code's parameters (called code conversion) on data already encoded with a locally repairable code (LRC), so an operator can adjust the tradeoff between repair cost and storage overhead as failure rates, workloads, or storage budgets change over the data's lifetime, without paying the cost of reading and re-encoding everything from scratch.
An LRC divides k data symbols into m = k/r local groups of r symbols each, adds ℓ local parity symbols per group (each a function only of that group's r data symbols), and adds g global parity symbols (each a function of all k data symbols). This (r, ℓ) data locality lets a single failed data node be repaired by reading only r other nodes in its local group, instead of reading all k data nodes as a maximum-distance-separable (MDS) code such as Reed-Solomon would require.
Code conversion changes the code's parameters (k, g, r, or ℓ) on data already encoded, without decoding to the original message and re-encoding. The mechanism (called a converter) reads data from existing nodes, computes new symbols, and writes them; conversion bandwidth is the total data moved between nodes during this process. This paper's construction technique starts from a systematic Vandermonde-matrix maximum-distance-separable base code, applies a basic pyramid-code transformation (zeroing out generator-matrix entries outside each local group's row range) to obtain (r, ℓ) locality, then layers a piggybacking framework on top — encoding α parallel instances of the base code per symbol and adding extra "piggyback" functions to certain symbols so that, during conversion, the initial code's local and global parity symbols can be reused directly as inputs to the final code's parity symbols instead of requiring the underlying data symbols to be re-read. The paper gives two named conversion types under this framework, both holding r and ℓ fixed while k and g vary: global merge conversion, combining λI ≥ 2 initial codewords into one larger final codeword (kF = λI·kI); and global split conversion, dividing one initial codeword into λF ≥ 2 final codewords (kI = λF·kF). Each parity in the construction is classified as a merge parity, split parity, or unchanged parity, and constructed via one of a small set of named techniques (linear combination, piggybacking, piggybacking-plus-linear-combination, or direct pass-through) depending on its classification.

### Measured results
The paper reports read conversion bandwidth (γ̃ = γ/α, where γ is the total data read from nodes during conversion and α is the per-symbol vector length) as closed-form expressions (Theorem 2 for global merge, Theorem 3 for global split) parameterized by the initial and final code's (k, g, r, ℓ) values, not as an empirical measurement from an implementation. All reported numeric comparisons are worked examples evaluating these closed-form expressions, not simulation or deployment results — no runtime, wall-clock cost, hardware, or trial count is given anywhere in the paper.

| Conversion (initial → final parameters) | This construction's γ̃ | Default re-encode-from-scratch γ̃ | Prior maximum-distance-separable-only construction's γ̃ |
|---|---|---|---|
| Global merge: (k=6, g=1, r=3, ℓ=1) → (k=12, g=2, r=3, ℓ=1) | 7⅓ | 12 | 8 (Maturana & Rashmi, ISIT 2021) |
| Global split: (k=12, g=2, r=3, ℓ=1) → (k=6, g=1, r=3, ℓ=1) | 5 | 12 | 5⅓ (Maturana & Rashmi, 2022) |
| Global conversion: (k=40, g=2, r=10, ℓ=2) → (k=20, g=3, r=10, ℓ=2) | not given in absolute γ̃ | not given | 17.89% more bandwidth than this paper's construction (stated as a relative reduction, absolute figures not stated in the retrieved text) |

### Parameters
- (k, g, r, ℓ): the four code parameters this construction converts between — k data symbols, g global parity symbols, r data symbols per local group, ℓ local parity symbols per group. The paper's worked examples use (6,1,3,1)→(12,2,3,1), (12,2,3,1)→(6,1,3,1), and (40,2,10,2)→(20,3,10,2); no general recommended values are given, since the construction is parameter-general.
- α: per-symbol vector length (number of parallel base-code instances via the piggybacking framework), treated as a free variable in the construction, not fixed to a numeric value.
- Constraint r | k (r must divide k) is required for the construction as presented.
- d (minimum distance) is fixed at the optimal value for given (k, g, r, ℓ) via the bound d ≤ n − k + 1 − ℓ(⌈k/r⌉ − 1), from prior work (Gopalan, Huang, Simitci, Yekhanin, 2012) that this paper's constructions meet with equality.

### Stated limitations
The paper restricts its constructions to global conversions, meaning only k and g change while r and ℓ stay fixed; it does not address conversions that change r or ℓ (changing the group size or the number of local parities) — this is stated as a scope choice ("in this paper we focus on global conversions") rather than argued to be infeasible. The paper also states its read-conversion-bandwidth focus explicitly excludes access cost (the number of nodes contacted, as opposed to the volume of data moved), citing Xia et al.'s prior up/downcoding work as the access-cost-focused alternative. No formal limitations, discussion, or future-work section appears in this conference-length paper; it ends immediately after presenting Theorem 3 with no concluding discussion of open problems.

### Requirements it places on the rest of the system
- The initial and final codes must both be systematic codes with (r, ℓ) data locality and optimal minimum distance, built from the paper's Vandermonde-based pyramid-code-plus-piggybacking construction; the technique is not stated to generalize to arbitrary existing LRCs.
- A conversion changing k requires M := lcm(kI, kF) data nodes to be evenly divided among λI = M/kI initial codewords and λF = M/kF final codewords — the storage layer must be able to regroup data across this least-common-multiple boundary, not just within one codeword.
- Where the number of codewords increases during conversion, the construction requires an explicit instance-reassignment permutation step (defined via a `batch()` function and permutation πᵢ) to keep every final codeword using the identical code; without this step the paper states the system would need to track extra per-codeword metadata.
- The converter role (reading old symbols, computing, writing new symbols) is assumed to be a single logical actor with read access to all relevant initial-code nodes and write access to all final-code nodes; the paper does not model converter failure, partial conversion, or concurrent access during conversion.
- The construction assumes a sufficiently large finite field to guarantee the Vandermonde matrix's maximum-distance-separable property (via a primitive-element choice of evaluation points); no field-size bound is stated in the retrieved text.

### Contradicts
None found. No other entry in this corpus reports locally-repairable-code conversion-bandwidth figures to compare against.

### References worth retrieving
- foundational: F. Maturana, K. V. Rashmi, "Convertible codes: enabling efficient conversion of coded data in distributed storage," IEEE Transactions on Information Theory 68, 2022 — introduces the general code-conversion problem this paper extends to locally repairable codes.
- foundational: F. Maturana, K. V. Rashmi, "Bandwidth cost of code conversions in distributed storage: fundamental limits and optimal constructions," ISIT 2021 — the maximum-distance-separable-only conversion-bandwidth construction this paper's Example 1 (γ̃=8) compares against.
- foundational: F. Maturana, K. V. Rashmi, "Bandwidth cost of code conversions in the split regime," 2022 — the maximum-distance-separable-only split-conversion construction this paper's Example 2 (γ̃=5⅓) compares against.
- competing: M. Xia, M. Saxena, M. Blaum, D. Pease, "A tale of two erasure codes in HDFS," USENIX FAST 2015 — first LRC-to-LRC conversion procedure (up/downcoding), optimizing access cost rather than conversion bandwidth; the direct prior-work comparison point.
- foundational: C. Huang, M. Chen, J. Li, "Pyramid codes: flexible schemes to trade space for access efficiency in reliable data storage systems," ACM Transactions on Storage 9, 2013 — the basic pyramid-code construction this paper's base code derives from.
- foundational: P. Gopalan, C. Huang, H. Simitci, S. Yekhanin, "On the locality of codeword symbols," IEEE Transactions on Information Theory 58(11), 2012 — proves the minimum-distance bound for (r,ℓ) data locality that this paper's codes meet with equality.
- foundational: K. V. Rashmi, N. B. Shah, K. Ramchandran, "A piggybacking design framework for read-and download-efficient distributed storage codes," IEEE Transactions on Information Theory 63(9), 2017 — the piggybacking framework this paper's construction is built on.
- competing: S. Wu, Z. Shen, P. P. C. Lee, Y. Xu, "Optimal repair-scaling trade-off in locally repairable codes: analysis and evaluation," IEEE Transactions on Parallel and Distributed Systems 33, 2022 — LRC scaling in a clustered setting optimizing inter-cluster communication, a related but distinct cost model from this paper's inter-node conversion bandwidth.
- competing: Y. Hu, L. Cheng, Q. Yao, P. P. C. Lee, W. Wang, W. Chen, "Exploiting combined locality for wide-stripe erasure coding in distributed storage," USENIX FAST 2021 — clustered LRC scaling work cited alongside Wu et al. as related but addressing a different cost model.

### Verbatim extracts
- "Locally repairable codes (LRCs) reduce the repair cost at the cost of higher storage overhead."
- "our construction achieves the conversion of (k,g,r,ℓ) from (40, 2, 10, 2) to (20, 3, 10, 2) with 17.89% less conversion bandwidth"
- "The present paper is, to the best of our knowledge, the first one to focus on LRC conversion bandwidth"
- "we focus on reducing conversion bandwidth instead" [of access cost]
- "in this paper we focus on global conversions, which only change k and g"
