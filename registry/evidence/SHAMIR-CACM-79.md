## [SHAMIR-CACM-79] How to Share a Secret
**Citation:** Adi Shamir. "How to Share a Secret." Communications of the ACM, 22(11), 1979. Pages 612-613. DOI 10.1145/359168.359176.
**Retrieved:** full text via https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf
**Source URL:** https://doi.org/10.1145/359168.359176
**Domain:** E

### What it does
A (k, n) threshold scheme splits one secret value D into n separate pieces so that any k of those pieces reconstruct D exactly, while any k-1 or fewer pieces leave D completely undetermined: every possible value of D remains equally likely given only k-1 pieces, an information-theoretic (not computational) guarantee. The construction uses polynomial interpolation over a finite field. The holder of D picks a random polynomial q(x) of degree k-1 whose constant term a0 equals D, with the remaining k-1 coefficients drawn uniformly at random from the integers modulo a prime p larger than both D and n. Piece i is the value q(i) for i = 1 to n, computed modulo p. Because k points uniquely determine a degree-(k-1) polynomial, any k of the (i, q(i)) pairs let a reconstructor recover q(x) by interpolation and evaluate q(0) = D; the paper cites known O(n log^2 n) algorithms for this evaluation and interpolation step, while noting the straightforward quadratic-time algorithm is fast enough for practical key management. Given only k-1 pairs, the paper's proof shows every candidate value D' in [0, p) is consistent with exactly one degree-(k-1) polynomial passing through those k-1 points and having constant term D', so all p candidates are equally probable and no information about D leaks. Pieces can be added or removed later without altering the other pieces (as long as k is unchanged), by evaluating the same q(x) at new indices, and periodically re-drawing a fresh polynomial with the same constant term rotates all pieces while leaving D unchanged, so that stale, previously exposed pieces cannot later be combined with newly exposed ones (they belong to different polynomials).

### Measured results
This is a cryptographic construction paper with a correctness and security proof, not an empirical measurement study; the one numeric example given is the illustrative combinatorial baseline the scheme replaces, not a result of an experiment.
| Figure | Context |
|---|---|
| The classical multi-lock solution to a (6,11) "eleven scientists" access-control problem (a cabinet openable only when 6 of 11 scientists are present) requires 462 locks and 252 keys per scientist | Stated as the exact minimal solution to the toy combinatorial problem the paper generalizes; used to argue that mechanical-lock solutions become exponentially impractical as the scientist count grows, motivating the algebraic scheme that follows |
| A 16-bit modulus suffices for schemes with up to 64,000 pieces (Di values) | Stated as following from the requirement that the field modulus p exceed n, since a 16-bit modulus supports fields up to 65,536 elements minus reserved headroom; given as a practical sizing guideline, not a benchmark run |

### Parameters
- Threshold k and total pieces n: chosen by the scheme designer; the paper gives no universal recommended values, describing k and n as tunable to trade the size of an authorizing majority against the size of a blocking minority.
- Field size: a prime p strictly greater than both the secret value D and the piece count n, so that n+1 distinct nonzero field elements exist to serve as indices 1 through n plus the reconstruction point 0.
- Robust key-management instance: the paper gives n = 2k-1 as the specific choice that lets the scheme tolerate the loss of up to floor(n/2) = k-1 pieces (recoverable) while also tolerating exposure of up to ceil(n/2) = k-1 of the surviving pieces (still secret) — a worked example, not a universally recommended setting.
- Recommended field width for large-scale use: a 16-bit modulus, stated as sufficient for schemes with up to 64,000 pieces; for a longer secret D, the paper recommends splitting D into shorter blocks handled separately rather than performing multi-precision modular arithmetic on the whole value at once.

### Stated limitations
The paper states the field modulus cannot be made arbitrarily small: the smallest usable value of p is n+1, because at least n+1 distinct field elements are needed to serve as the evaluation points. It states the scheme depends on the coefficients of q(x) (other than the constant term) being drawn from a uniform distribution over the field; the security proof is conditioned on that uniform choice. The paper notes a different, less efficient threshold construction was developed independently by G. R. Blakley in the same year, without stating a quantitative comparison between the two.

### Requirements it places on the rest of the system
Any system using this scheme needs a source of uniformly random field elements to generate the k-1 non-constant coefficients of q(x); the secrecy proof holds only under that uniformity assumption, so a biased or predictable coefficient generator narrows the equally-likely candidate set the proof relies on. Reconstruction requires each of the k combined pieces to carry its identifying index i alongside the value q(i), because interpolation needs the (index, value) pairs, not the bare values. A scheme wanting to rotate pieces periodically (to invalidate previously exposed pieces) needs a mechanism, external to this paper, for all n current piece holders to receive a freshly evaluated piece from a new q(x) with the same constant term, and for old pieces to be treated as no longer valid; the paper describes the technique but not a re-sharing protocol for who initiates or verifies that rotation. A dealer generating and distributing the pieces is implicitly trusted at the moment of the split, since the scheme as described gives no mechanism for the n recipients to verify that the pieces they receive are consistent with a single degree-(k-1) polynomial without a separate verifiable-secret-sharing extension, which this paper does not describe.

### Contradicts
None found within this corpus batch.

### References worth retrieving
- competing: G. R. Blakley, "Safeguarding cryptographic keys," Proc. AFIPS 1979 NCC, Vol. 48, pp. 313-317 — an independently developed, differently structured threshold scheme from the same year, explicitly cited as a comparison point.
- foundational: R. Rivest, A. Shamir, L. Adleman, "A method for obtaining digital signatures and public-key cryptosystems," Communications of the ACM 21(2), 1978, pp. 120-126 — the RSA construction cited as the signature scheme the multi-executive check-signing example is built on.
- foundational: D. Knuth, "The Art of Computer Programming, Vol. 2: Seminumerical Algorithms," Addison-Wesley, 1969 — cited for the polynomial evaluation and interpolation algorithms referenced.

### Verbatim extracts
- "knowledge of any k or more Di pieces makes D easily computable"
- "knowledge of any k- 1 or fewer Di pieces leaves D completely undetermined"
- "the minimal solution uses 462 locks and 252 keys per scientist"
- "sixteen bit modulus ... suffices for applications with up to 64,000 Di pieces"
- "there is absolutely nothing the opponent can deduce about the real value of D"
