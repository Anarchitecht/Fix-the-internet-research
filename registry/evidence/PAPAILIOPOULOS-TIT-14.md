## [PAPAILIOPOULOS-TIT-14] Locally Repairable Codes

**Citation:** Dimitris S. Papailiopoulos, Alexandros G. Dimakis. "Locally Repairable Codes." IEEE Transactions on Information Theory, 2014. DOI 10.1109/TIT.2014.2325570.
**Retrieved:** full text via https://arxiv.org/abs/1206.3804 (arXiv:1206.3804v2, 3 May 2014)
**Source URL:** https://arxiv.org/abs/1206.3804
**Domain:** C

### What it does
A locally repairable code (LRC) reduces the number of other stored pieces a single lost piece requires reading to reconstruct, called repair locality, as distinct from repairing through the entire code. The paper formalizes an (n, r, d, M, alpha)-LRC as an encoding of a file of M bits into n coded symbols of alpha bits each, in which every coded symbol has locality r (reconstructible by accessing and processing at most r other symbols) and minimum distance d (the whole file recoverable from any n - d + 1 of the n symbols). It proves an information-theoretic bound coupling d, r, M, and alpha that holds for every code, linear or non-linear: d <= n - ceil(M/alpha) - ceil(M/(r*alpha)) + 2. It then proves this bound is achievable, whenever r+1 divides n, using a randomized vector-linear construction built by mapping the code to a directed acyclic flow-graph and applying random linear network coding, so that a capacity-achieving multicast scheme on that graph yields a code meeting the bound. Finally the paper gives an explicit construction at the maximum-distance-separable (MDS, meaning the code reconstructs the full file from any k of n symbols) operational point d = n - k + 1: encode k source symbols into n Reed-Solomon-coded blocks arranged into n/(r+1) groups of r blocks each, then compute one extra XOR parity block per group over its r blocks, so any single lost block within a group is repaired by downloading the group's other r blocks and XORing them.

### Measured results
This is a theory paper: every reported figure is a proven bound or an algebraic consequence of the construction, not an experimental measurement. No simulation or deployment evaluation appears in the text.

| Result | Conditions |
|---|---|
| d <= n - ceil(M/alpha) - ceil(M/(r*alpha)) + 2 | Theorem 1, universal bound, holds for linear and non-linear (n, r, d, M, alpha)-LRCs of any file size M and symbol size alpha |
| d <= n - k - ceil(k/r) + 2 | Same bound (Theorem 1) specialized to the scalar-code regime alpha=1, M=k, which the paper states reduces to the bound already proven by Gopalan, Huang, Simitci, Yekhanin (reference [12]) |
| The bound of Theorem 1 is achievable at distance d = n - ceil(M/alpha) - ceil(M/(r*alpha)) + 2 over a sufficiently large finite field | Theorem 2, condition: (r+1) divides n and r <= n - d; proof by mapping to a random-linear-network-coding multicast scheme on a specific directed acyclic flow-graph |
| Explicit MDS-point construction achieves distance d = n - k + 1 (the same distance as an (n,k) MDS code) with locality r, coding rate a fraction r/(r+1) of the (n,k) MDS coding rate, storage per symbol alpha = ((r+1)/r) * (M/k) | Section 5's explicit family, condition (r+1) divides n; construction meets the optimal distance bound of Theorem 1 whenever (r+1) does not divide k |
| Sub-packetization (vector length per stored symbol) equals r, over a field of size proportional to n, so each coded symbol needs r * O(log n) bits | Same explicit construction |

### Parameters
- r (locality, the count of other symbols read to reconstruct one lost symbol): free design parameter; achievability (Theorem 2) proven only when r+1 divides n and r <= n - d.
- d (minimum distance): bounded above by Theorem 1 as a function of n, r, M, alpha; the explicit MDS-point construction fixes d = n - k + 1.
- alpha (coded-symbol size, storage per node): free parameter in Theorem 1's bound; fixed to ((r+1)/r) * (M/k) in the explicit MDS-point construction.
- n, k (code length, source-symbol count): free parameters; the explicit construction additionally requires (r+1) divides n for its stated optimality and simple XOR repair.
- Field size for the explicit construction: proportional to n (small, stated as enabling r * O(log n) bits per coded symbol), distinct from the "sufficiently large finite field" required by the general randomized construction of Theorem 2, whose required size is not given as an explicit function.

### Stated limitations
Achievability of the Theorem 1 bound is proven only when r+1 divides n; the paper states this does not rule out the bound being tight under more general assumptions but leaves that case as an open question. The paper cites Gopalan et al. (reference [12]) showing that, for linear codes with information-symbol locality, it is impossible to construct optimal linear LRCs with all-symbol locality when r divides k and 2 < d < r+3, a parameter regime this paper's own achievability result does not cover. The explicit MDS-point construction pays a coding-rate cost: its rate is a fixed fraction r/(r+1) of an (n,k) MDS code's rate at the same distance, a loss the paper attributes to the extra XOR parity block each repair group requires; the paper notes this loss becomes small only when r grows as a sub-linear function of k (for example log k or square root of k).

### Requirements it places on the rest of the system
The explicit MDS-point construction requires n to be arranged into groups of exactly r+1 blocks (r Reed-Solomon-coded blocks plus one XOR parity block per group), so a storage layer must place and address blocks by group membership for the stated single-block XOR repair procedure to apply; repairing a lost block requires simultaneously reading the r other still-live blocks of the same group, so any r-1 of them being unavailable at once blocks that repair path (the paper does not analyze repair under partial group unavailability). The Theorem 1 bound and Theorem 2 achievability proof assume a repair of one symbol accesses exactly the locality-r group associated with that symbol, fixed at code construction time; the mechanism gives no support for reconstructing from an arbitrary subset of surviving symbols outside a symbol's own repair group faster than full-code decoding. The randomized general construction (Theorem 2) requires operating over a field large enough for random linear network coding to succeed with high probability, a size the paper states as "sufficiently large" without giving the concrete field-size requirement as a closed-form parameter.

### Contradicts
None found.

### References worth retrieving
- Gopalan, Huang, Simitci, Yekhanin. "On the locality of codeword symbols." IEEE Transactions on Information Theory, 2011 — foundational (proves the scalar-code special case of this paper's distance bound and the structure theorems this paper's Remark 3 and limitation discussion build on).
- Sathiamoorthy, Asteris, Papailiopoulos, Dimakis, Vadali, Chen, Borthakur. "XORing elephants: Novel erasure codes for big data." VLDB Endowment, 2013 — competing (also in this corpus as SATHIAMOORTHY-VLDB-13; a deployed LRC system by an overlapping author set).
- Rashmi, Shah, Kumar. "Optimal exact-regenerating codes for distributed storage at the MSR and MBR points via a product-matrix construction." IEEE Transactions on Information Theory, 2011 — competing (also in this corpus as RASHMI-TIT-11; optimizes repair bandwidth rather than locality, the alternative repair-cost metric this paper contrasts against).
- Dimakis, Godfrey, Wu, Wainwright, Ramchandran. "Network coding for distributed storage systems." IEEE Transactions on Information Theory, 2010 — foundational (introduces the repair-bandwidth metric and the random-linear-network-coding technique this paper's achievability proof reuses).
- Rashmi, Shah, Gu, Kuang, Borthakur, Ramchandran. "A solution to the network challenges of data recovery in erasure-coded distributed storage systems: A study on the facebook warehouse cluster." USENIX HotStorage, 2013 — foundational (source of the 8%-of-storage / 20%-of-repair-traffic Facebook Hadoop cluster figure this paper's introduction cites as motivation).
- Huang, Chen, Li. "Pyramid codes: Flexible schemes to trade space for access efficiency in reliable data storage systems." NCA 2007 — foundational (an earlier locality-trading code construction this paper's introduction cites as prior small-locality work).
- Cadambe, Huang, Jafar, Li. "Optimal repair of MDS codes in distributed storage via subspace interference alignment." arXiv:1106.1250, 2011 — competing (a repair-bandwidth-optimal MDS repair scheme, alternative approach to the same repair-cost problem).
- Tamo, Papailiopoulos, Dimakis. "Optimal locally repairable codes and connections to matroid theory." arXiv:1301.7693, 2013 — superseded-by (by the same author group, a later treatment of optimal LRC constructions).

### Verbatim extracts
"a coded symbol Yi... has locality r, if it can be reconstructed by accessing ri other symbols"
"an (n, r, d, M, α)-LRC has distance d that is bounded as d ≤ n − ⌈M/α⌉ − ⌈M/(rα)⌉ + 2"
"the rate of our codes will be 1/r... less than that of an (n, k)-MDS code"
"it is impossible to construct optimal and linear LRCs... when 2 < d < r + 3 and r|k"
