## [MATURANA-TIT-22] Convertible Codes: Enabling Efficient Conversion of Coded Data in Distributed Storage

**Citation:** Francisco Maturana, K. V. Rashmi. "Convertible Codes: Efficient Conversion of Coded Data in Distributed Storage." IEEE Transactions on Information Theory, 2022. DOI 10.1109/TIT.2022.3155972.
**Retrieved:** full text (text on disk carries the earlier working title "Convertible Codes: Efficient Conversion of Coded Data in Distributed Storage"; author list, DOI, and content match the registry record)
**Source URL:** https://arxiv.org/abs/1907.13119
**Domain:** C

### What it does
Code conversion changes the redundancy parameters of data already stored under an erasure code, from an initial [n_I, k_I] code to a final [n_F, k_F] code, without decoding back to the original data and re-encoding from scratch. The paper defines the access cost of a conversion as the total count of coded blocks read or written during the conversion, and restricts its analysis to the merge regime, where multiple initial stripes (each a group of n_I coded blocks produced from k_I original data blocks) combine into fewer, larger final stripes, formally k_F = lambda * k_I for an integer lambda >= 2. A convertible code is a paired construction of the initial and final generator matrices, chosen jointly so that a conversion can compute each final stripe's parity blocks directly from a small subset of the initial stripes' existing parity blocks by linear combination, rather than by reading every data block and full-encoding again. The paper proves a lower bound on access cost achievable by any linear, maximum-distance-separable (MDS, meaning any k of the n coded blocks in a stripe suffice to reconstruct the original k data blocks) convertible code in the merge regime, then gives two explicit families of constructions (Hankel-I and Hankel-II, built from submatrices of a superregular Hankel array, a triangular array of field elements in which every submatrix is guaranteed invertible) that meet this lower bound while using a polynomial rather than exponential field size.

### Measured results
This is a theoretical paper: every reported figure is a proven bound or a worked numeric example under that bound, not an experimental measurement. No simulation, prototype, or deployment evaluation appears in the text.

| Result | Conditions |
|---|---|
| Access cost of conversion is at least r_F + lambda * min(k_I, r_F); at least r_F + lambda * k_I if r_I < r_F | Theorem 8, proven for all linear MDS (n_I, k_I; n_F, k_F = lambda * k_I) convertible codes in the merge regime; r_I = n_I - k_I and r_F = n_F - k_F are the initial and final parity-block counts |
| Worked example: naive re-encoding accesses 24 blocks per final stripe; the access-optimal convertible code accesses 12 | (n_I=14, k_I=10; n_F=24, k_F=20), lambda=2; the paper states this as a 50% reduction in access cost |
| Worked example: converting a [k_I+1, k_I] single-parity-check code by merging two initial stripes into one final [2k_I+1, 2k_I] stripe drops access cost from 2*k_I (naive re-encoding) to 2 blocks | Example 1, lambda=2, single-parity-check code (XOR-parity), n_I = k_I+1, n_F = k_F+1 |
| Hankel-I construction meets the access-optimal lower bound whenever r_F <= floor(r_I / lambda), at field size q >= max(n_I - 1, n_F - 1) | Merge regime, linear MDS convertible codes; field size matches the maximum field size already required by a plain [n_I,k_I] or [n_F,k_F] Reed-Solomon code, so the paper states no field-size penalty is incurred for this range |
| Hankel-II construction meets the access-optimal lower bound whenever r_F <= r_I - lambda + 1, at field size q >= k_I * r_I | Merge regime, linear MDS convertible codes; wider r_F coverage than Hankel-I at a larger field size |
| Worked example of Hankel-I: (n_I=9, k_I=5; n_F=12, k_F=10) built from a superregular Hankel array of size n_F - 1 = 11 | Illustrates the field size q=11 = max(n_I-1, n_F-1) with n_I-1=8, n_F-1=11 |
| Worked example of Hankel-II: (n_I=7, k_I=4; n_F=10, k_F=8) | Illustrates a case outside Hankel-I's r_F range that Hankel-II covers |

### Parameters
- lambda (merge factor, k_F = lambda * k_I): integer, lambda >= 2; the paper's theory and both Hankel constructions are stated for this range.
- r_I, r_F (initial and final parity-block counts, r_I = n_I - k_I, r_F = n_F - k_F): free parameters bounding which construction (Hankel-I or Hankel-II) applies and at what field size.
- s (number of groups the r_I initial parity encoding vectors are split into, in the general Hankel-based sequence of constructions): ranges over {lambda, lambda+1, ..., r_I}; s = lambda recovers Hankel-I, s = r_I recovers Hankel-II.
- Field size q: q >= max(n_I - 1, n_F - 1) for Hankel-I; q >= k_I * r_I for Hankel-II; the paper states this as an explicit field-size-versus-r_F-coverage tradeoff, with intermediate s values interpolating between the two.

### Stated limitations
The paper restricts every proof to the merge regime, k_F = lambda * k_I with lambda an integer at least 2; it states going beyond the merge regime to general parameter regimes as its first listed direction for future work, meaning the access-cost lower bound and both Hankel constructions carry no proven guarantee outside this regime. The paper optimizes only access cost, defined as block count touched; it states that network bandwidth, disk input/output, and CPU consumption are related but separate resource costs it does not bound, and explicitly notes its access-optimal constructions reduce these other costs but are not proven optimal for them. The general high-field-size construction of Section V is stated to require a field size that grows too large for practical use, which motivates the lower-field-size Hankel constructions, but those Hankel constructions cover only the r_F ranges bounded above (not every r_F value at every field size).

### Requirements it places on the rest of the system
Both endpoints (n_I, k_I) and (n_F, k_F) must be fixed and known to the code construction in advance for the access-optimal guarantee to apply as proven; the paper's own "Handling a priori unknown parameters" discussion shows the Hankel sequence can be built to stay access-optimal across a bounded family of possible final parameters (k_F' = lambda' * k_I, n_F' = r_F' + k_F', 0 <= r_F' <= r_F, 2 <= lambda' <= lambda) chosen at construction time, so a system that wants flexibility across multiple possible future targets must enumerate that family up front rather than discover the target parameters after the fact. The conversion procedure reads specific parity blocks from the initial stripes identified by the construction and computes final parity blocks by linear combination over the finite field, so the storage system must be able to address and read individual coded blocks (not only fully-reconstructed data) and must apply linear operations over the same field the code was built over. The MDS property and the access-cost lower bound are both proven only for linear codes, so a non-linear or non-MDS encoding scheme receives no guarantee from this paper's results.

### Contradicts
None found.

### References worth retrieving
- Rashmi, Shah, Gu, Kuang, Borthakur, Ramchandran. "A solution to the network challenges of data recovery in erasure-coded distributed storage systems: A study on the Facebook warehouse cluster." USENIX HotStorage, 2013 — foundational (measured repair-bandwidth motivation for reducing conversion cost).
- Kadekodi, Rashmi, Ganger. "Cluster storage systems gotta have HeART: improving storage efficiency by exploiting disk-reliability heterogeneity." USENIX FAST, 2019 — foundational (the paper the abstract cites for the 11%-44% storage-space-reduction motivation for redundancy adaptation; that figure is attributed to this source, not measured by MATURANA-TIT-22 itself).
- Sathiamoorthy, Asteris, Papailiopoulos, Dimakis, Vadali, Chen, Borthakur. "XORing elephants: Novel erasure codes for big data." VLDB Endowment, 2013 — competing (also in this corpus as SATHIAMOORTHY-VLDB-13, a locally repairable code rather than a convertible code).
- Rashmi, Shah, Kumar. "Optimal exact-regenerating codes for distributed storage at the MSR and MBR points via a product-matrix construction." IEEE Transactions on Information Theory, 2011 — foundational (also in this corpus as RASHMI-TIT-11; the repair-bandwidth-optimal code family this paper's access-cost framework parallels).
- Tamo, Wang, Bruck. "Access versus bandwidth in codes for storage." IEEE Transactions on Information Theory, 2014 — competing (states access cost and bandwidth cost as generally distinct optimization targets, directly relevant to this paper's stated limitation that it optimizes access cost only).
- Papailiopoulos, Dimakis. "Locally Repairable Codes." — competing (also in this corpus as PAPAILIOPOULOS-TIT-14; a different mechanism for reducing the block count touched during repair).

### Verbatim extracts
"the access cost of conversion is at least rF +λ min{kI,rF}"
"the optimal access cost is (λ + 1)rF = 12, which corresponds to savings in access cost of 50%"
"the access-optimal convertible codes... also reduce the total network bandwidth, disk IO, and CPU overhead"
"an important future direction is to go beyond the merge regime considered in this paper"
