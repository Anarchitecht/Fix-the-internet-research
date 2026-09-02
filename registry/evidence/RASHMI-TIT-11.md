## [RASHMI-TIT-11] Optimal Exact-Regenerating Codes for Distributed Storage at the MSR and MBR Points via a Product-Matrix Construction

**Citation:** K. V. Rashmi, Nihar B. Shah, P. Vijay Kumar. "Optimal Exact-Regenerating Codes for Distributed Storage at the MSR and MBR Points via a Product-Matrix Construction." IEEE Transactions on Information Theory, 2011. DOI 10.1109/TIT.2011.2159049.
**Retrieved:** full text via https://arxiv.org/abs/1005.4178 (arXiv:1005.4178v2, 20 Jan 2011)
**Source URL:** https://arxiv.org/abs/1005.4178
**Domain:** C

### What it does
A regenerating code repairs a failed storage node by downloading a fraction of the data stored at each of several helper nodes rather than the entire file, reducing the total repair-time network traffic below what full-file download requires. An [n, k, d] regenerating code stores a file across n nodes so that any k nodes reconstruct the whole file, and any d of the remaining n-1 nodes serve as helpers that each transmit beta symbols (beta <= alpha, where alpha is the number of symbols stored per node) during repair, for a total repair bandwidth of d*beta. The paper targets exact-regeneration: the replacement node's content is bit-for-bit identical to the failed node's original content, not merely equivalent for later data-reconstruction. It gives a product-matrix framework in which each stored node's content is a fixed linear function (row of an encoding matrix Psi applied to a product of two smaller matrices) of the source symbols, and proves this framework yields explicit codes meeting the cut-set bound (Theorem 1 of prior work, restated as equation 2: B <= sum over i=0..k-1 of min(alpha, (d-i)*beta)) at the Minimum Bandwidth Regenerating (MBR) point for every feasible [n, k, d], and at the Minimum Storage Regenerating (MSR) point for every [n, k, d] with d >= 2k-2. Unlike prior exact-regenerating constructions, n is a free parameter independent of d, so the number of storage nodes can be chosen and later changed without being tied to d+1.

### Measured results
This is a theory paper: every reported figure is a proven achievability or non-achievability bound, not an experimental measurement.

| Result | Conditions |
|---|---|
| Cut-set bound: B <= sum_{i=0}^{k-1} min(alpha, (d-i)*beta) | Equation (2), general [n,k,d] regenerating code, proven in prior work [4],[5] via network-coding cut-set analysis, restated here as the target this paper's constructions must meet with equality |
| MSR point parameters: alpha = B/k, beta = B/(k*(d-k+1)) | Equation (3), obtained by minimizing alpha first, then beta |
| MBR point parameters: beta = 2B/(k*(2d-k+1)), alpha = 2dB/(k*(2d-k+1)) | Equation (4), obtained by minimizing beta first, then alpha |
| Product-matrix MBR construction achieves the cut-set bound with equality (exact-regeneration) for all feasible [n, k, d] | New result of this paper; no restriction to n = d+1 |
| Product-matrix MSR construction achieves the cut-set bound with equality (exact-regeneration) for all [n, k, d >= 2k-2] | New result of this paper |
| Field size sufficient for the product-matrix MBR code: any q >= 2n | Stated as a sufficient (not claimed minimal) field size; smaller fields may work with careful choice of the encoding matrix Psi |
| Field size sufficient for the product-matrix MSR code: any q >= n^2 | Same caveat, sufficient not claimed minimal |
| Prior, non-achievability result cited: exact-regeneration at the MSR point is not achievable for any [n, k, d <= 2k-3] when beta=1 | Attributed to reference [14] (Shah, Rashmi, Kumar, Ramchandran), not proven or re-derived in this paper; cited as context bounding how far d can be lowered |
| Simpler restated prior code: exact-regeneration at the MSR point for [n=d+1, k, d >= 2k-1] (the 'MISER' code) | This paper gives a simplified product-matrix description of a code originally constructed in references [6],[7]; this is not the new d >= 2k-2 result above and remains restricted to n=d+1 |

### Parameters
- alpha (symbols stored per node): free parameter; at the MSR point, alpha = B/k (Equation 3); at the MBR point, alpha = 2dB/(k(2d-k+1)) (Equation 4).
- beta (symbols downloaded per helper node during repair, beta <= alpha): free parameter; at the MSR point, beta = B/(k(d-k+1)); at the MBR point, beta = 2B/(k(2d-k+1)).
- d (repair degree, count of helper nodes contacted, k <= d <= n-1): this paper's new MSR construction requires d >= 2k-2; the earlier restated MISER code requires d >= 2k-1 with the added restriction n = d+1; the MBR construction has no lower bound on d beyond the general k <= d <= n-1 requirement.
- n (total storage nodes): free parameter, independent of k and d, for both of this paper's new constructions (stated as the paper's principal advance over prior work, which fixed n = d+1).
- Field size q: q >= 2n suffices for the MBR construction; q >= n^2 suffices for the MSR construction; both stated as sufficient conditions that a careful choice of Psi may lower further, not as proven-minimal values.
- Encoding matrix Psi: can be chosen as a Vandermonde matrix, which the paper states makes encoding, data-reconstruction, and regeneration operations largely identical to standard Reed-Solomon code operations.
- Striping: the presented codes divide the message into stripes corresponding to beta=1 per stripe, so encoding and repair operate identically and independently per stripe.

### Stated limitations
The new MSR construction is proven only for d >= 2k-2; the paper does not claim or prove achievability for 2k-3 >= d >= k under exact-regeneration with finite beta, and cites a separate non-achievability proof (reference [14]) that the cut-set bound cannot be met at d <= 2k-3 with beta=1. The paper's own stated field-size requirements (q >= 2n for MBR, q >= n^2 for MSR) are sufficient conditions, not proven lower bounds; the paper states smaller fields "may often" work with a cleverly chosen Psi but does not characterize when. The simplified restatement of the prior [n=d+1, k, d>=2k-1] MISER code remains confined to n=d+1, a restriction this paper's own new constructions remove only for the MBR point (all d) and MSR point (d>=2k-2), not for that restated variant.

### Requirements it places on the rest of the system
Repair and reconstruction both require linear operations over a fixed finite field Fq of the stated minimum size (2n for MBR, n^2 for MSR); a system layer that cannot perform field arithmetic at that size, or that needs to change n after code deployment beyond what the fixed field size supports, falls outside the construction as given. A failed node's repair connects to exactly d helper nodes chosen from the remaining n-1 nodes and downloads beta symbols from each; the guarantee of exact-regeneration (bit-for-bit identical content) requires all d helpers to be simultaneously reachable and to supply their beta symbols each, so a repair that can reach fewer than d live helpers at once receives no guarantee from this construction. The encoding matrix Psi must satisfy specific structural conditions (given above the paper's Theorem 2 and Theorem 4, for MBR and MSR respectively) for the exact-regeneration property to hold; an arbitrary or adversarially chosen Psi is not guaranteed to work, so code setup requires verifying or constructing Psi (for example as a Vandermonde matrix) according to those conditions.

### Contradicts
None found.

### References worth retrieving
- Dimakis, Godfrey, Wu, Wainwright, Ramchandran. "Network Coding for Distributed Storage Systems." IEEE Transactions on Information Theory, vol. 56, no. 9, 2010 — foundational (introduces regenerating codes and proves the cut-set bound, equation 2, that this paper's constructions meet with equality).
- Shah, Rashmi, Kumar, Ramchandran. "Explicit Codes Minimizing Repair Bandwidth for Distributed Storage." IEEE Information Theory Workshop, 2010 — foundational (the MISER code this paper gives a simplified product-matrix description of, in Appendix A, for [n=d+1, k, d>=2k-1]).
- Suh, Ramchandran. "Exact-Repair MDS Codes for Distributed Storage Using Interference Alignment." IEEE ISIT, 2010 — foundational (extends the MISER code to repair non-systematic/parity node failures exactly; also reused by this paper's simplified restatement).
- Shah, Rashmi, Kumar, Ramchandran. "Interference Alignment in Regenerating Codes for Distributed Storage: Necessity and Code Constructions." IEEE Transactions on Information Theory (submitted, arXiv:1005.1634) — attack/critique (proves the non-achievability of exact-regeneration at the MSR point for d <= 2k-3 with beta=1, the boundary this paper's own construction stops short of).
- Cullina, Dimakis, Ho. "Searching for Minimum Storage Regenerating Codes." Allerton, 2009 — foundational (computer-search identification of exact-regenerating MSR codes at specific small parameters, prior to this paper's general construction).
- Wu, Dimakis, Ramchandran. "Deterministic Regenerating codes for Distributed Storage." Allerton, 2007 — foundational (early explicit, non-exact regenerating code construction cited as prior work establishing achievability of the storage-repair-bandwidth tradeoff under functional regeneration).
- Papailiopoulos, Dimakis. "Locally Repairable Codes." — competing (also in this corpus as PAPAILIOPOULOS-TIT-14; trades a different repair-cost metric, locality, against the repair-bandwidth metric this paper optimizes).

### Verbatim extracts
"these are the first explicit constructions of exact-regenerating codes that allow n to take any value"
"the MSR point can be achieved for all parameters satisfying d≥ 2k− 2"
"any field of size 2n or higher suffices" (MBR); "any field of size n2 or higher suffices" (MSR)
"the MSR point is not achievable for any [n, k, d≤ 2k− 3] with β = 1"
