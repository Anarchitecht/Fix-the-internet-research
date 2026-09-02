## [BONEH-ASIACRYPT-01] Short Signatures from the Weil Pairing
**Citation:** Dan Boneh, Ben Lynn, Hovav Shacham. "Short Signatures from the Weil Pairing." ASIACRYPT 2001 (journal version: Journal of Cryptology, 2004). DOI 10.1007/3-540-45682-1_30.
**Retrieved:** full text via https://crypto.stanford.edu/~dabo/pubs/papers/BLSsignatures.ps (converted, matches published pages 514-532 numbering visible in the text)
**Source URL:** https://crypto.stanford.edu/~dabo/pubs/papers/BLSsignatures.ps
**Domain:** E

### What it does
The scheme (later called BLS, after the authors' initials) produces a digital signature roughly half the bit length of a Digital Signature Algorithm (DSA) signature offering comparable security, so a signature can be typed in by a person or sent over a low-bandwidth channel. It works over a Gap Diffie-Hellman (GDH) group: a group in which the Computational Diffie-Hellman problem (recovering g^(ab) from g, g^a, g^b) is hard, but the Decisional Diffie-Hellman problem (deciding whether a given tuple g, g^a, g^b, g^c satisfies c=ab) is easy. The paper instantiates a GDH group using a bilinear pairing (the Weil pairing) on certain supersingular elliptic curves over fields of characteristic three, which supplies an efficient decision procedure for Diffie-Hellman tuples while leaving the computational problem hard.

Key generation picks a base point P of prime order q on the curve, samples a private key x uniformly from Z_q, and sets the public key to R = xP. Signing a message M applies a hash-to-curve function (MapToGroup, built from a conventional hash function h′ into the field plus an extra bit that selects one of two curve points sharing an x-coordinate) to obtain a curve point P_M, computes S_M = xP_M, and outputs the x-coordinate of S_M as the signature — a single field element rather than the pair of elements standard discrete-log signatures require. Verification recomputes P_M from M, uses the Weil pairing e to test whether e(P, S) equals e(R, P_M) or its inverse (since either sign of the y-coordinate could have produced the signature), and accepts if either equality holds; this pairing check substitutes for direct recomputation of xP_M, which the verifier cannot do without the private key. The paper proves that if a Gap Diffie-Hellman group is (τ,t,ε)-secure (no algorithm running in time t and using at most τ decision-oracle calls solves CDH with the given group with probability above ε) and MapToGroup is modeled as a random oracle, an adversary that can forge a signature after qH hash queries and qS signature queries can be turned into an algorithm solving Computational Diffie-Hellman in that group with related running time and success probability.

### Measured results
| Curve field size l | Signature length (bits) | Discrete-log security (bits) | MOV-reduction field-size security (bits) | Verification time (seconds, one signature) |
|---|---|---|---|---|
| 79 (curve E−) | 126 | 126 | 752 | 1.6 |
| 97 (curve E+) | 154 | 151 | 923 | 2.9 |
| 149 (curve E+) | 237 | 220 | 1417 | 9.6 |
| 163 (curve E+) | 259 | 256 | 1551 | 13.3 |
| 163 (curve E−) | 259 | 259 | 1551 | 13.4 |
| 167 (curve E+) | 265 | 262 | 1589 | 14.0 |

Verification times measured on a single machine: a 1 GHz Pentium III running GNU/Linux, one run per data point (no repetition count or variance stated). Signing time is stated only qualitatively as much cheaper than verification, since verification computes two pairings and signing computes one scalar multiplication; no signing-time figures are given. At l=97 (154-bit signature, 923-bit discrete-log security), the paper reports this as under half the length of a standard 320-bit DSA signature at 1024-bit-modulus discrete-log security — a length comparison, not an equal-security comparison, since 923-bit and 1024-bit security levels differ.

### Parameters
- Curve family: E: y² = x³ + 2x ± 1 over F_(3^l), supersingular, restricted to prime l to avoid Weil-descent attacks.
- Security multiplier α (also called the MOV-reduction embedding degree): fixed at α=6 for this curve family under the security parameters used, stated as the maximum achievable for these particular curves; the field size the MOV attack reduces to is 6·l bits.
- l (base-field exponent): the tested values are 79, 97, 149, 163, 167, each yielding one row of the results table above; no continuous range is stated, only these specific instantiated curves.
- Random-oracle hash function h′ (part of MapToGroup): mapped to F_(3^l) × {0,1}, instantiated but no concrete hash function or benchmark for it is given separately from the whole-scheme verification timings.

### Stated limitations
The scheme is proved secure only in the random oracle model, an idealization of the hash function used inside MapToGroup; the paper does not provide a proof in the standard model. Security depends on the specific supersingular curve family used being a Gap Diffie-Hellman group with security multiplier at most α=6 for currently known constructions; the paper poses as an explicit open problem building an elliptic- or hyper-elliptic-curve family with security multiplier higher than 6 (the paper suggests α≈10 as a target) while keeping signatures the same short length — solving this would raise achievable security without lengthening signatures, and the paper states this is unsolved. A second explicit open problem, also unsolved in the paper, asks whether a family of genus-3 hyperelliptic curves exists with the needed properties. Signing requires only one scalar multiplication, but verification requires two pairing computations, which the measured running times show scale from 1.6 to 14.0 seconds on 2001-era hardware as the security level rises — the paper states these times could potentially be reduced by using higher-genus curves over characteristic-two fields or techniques from a cited prior work, but does not implement or measure either improvement.

### Requirements it places on the rest of the system
Requires a source of a Gap Diffie-Hellman group: a group with an efficient algorithm for deciding Diffie-Hellman tuples but no known efficient algorithm for computing them, which in this paper is supplied only by the Weil-pairing-equipped supersingular elliptic curves described, not by an arbitrary discrete-log group. Requires a hash function that can be treated as a random oracle for the MapToGroup construction (mapping arbitrary message strings onto curve points of the correct order); the security proof does not carry through for an arbitrary non-random-oracle hash function. Requires the verifier to have access to the signer's public key R = xP and to be able to compute the Weil pairing efficiently, which the paper's own benchmark shows costing seconds per verification at 2001 hardware speeds and security levels in the hundred-bit range — any system embedding this scheme must budget verification latency accordingly rather than treat it as free.

### Contradicts
This paper does not define, construct, or prove anything about aggregating multiple signatures into one constant-size value; it presents a single-signer, single-message scheme only. Any claim that this specific paper establishes signature aggregation is not supported by its text — that property was introduced in a later paper by an overlapping set of authors (Boneh, Gentry, Lynn, Shacham, EUROCRYPT 2003), not this one, and any evidence-file entry using this KEY as the citation for aggregate-signature results would misattribute it. No other paper in this corpus's evidence file yet measures this scheme's parameters directly, so no cross-paper numeric contradiction is recorded.

### References worth retrieving
- foundational: Boneh, Franklin. "Identity-Based Encryption from the Weil Pairing." CRYPTO 2001 (companion pairing-based construction from the same period, source of related pairing-based cryptographic techniques).
- foundational: Joux. "A One Round Protocol for Tripartite Diffie-Hellman." ANTS IV, 2000 (the pairing-based key-exchange construction whose gap-group idea this signature scheme's security model builds on).
- competing: Mironov. "A Short Signature as Secure as DSA." Preprint, 2001 (a contemporaneous alternative short-signature construction cited as related work).
- attack: Galbraith, Smart. "A Cryptographic Application of Weil Descent." Cryptology and Coding, 1999 (the Weil-descent attack this paper's restriction to prime l is designed to avoid).
- attack: Gaudry, Hess, Smart. "Constructive and Destructive Facets of Weil Descent on Elliptic Curves." University of Bristol Technical Report CSTR-00-016, 2000 (further Weil-descent attack analysis motivating the same restriction).
- foundational: Menezes, Okamoto, Vanstone. "Reducing Elliptic Curve Logarithms to Logarithms in a Finite Field." IEEE Transactions on Information Theory, 1993 (the MOV reduction whose resulting field-size security this paper's Table 1 reports).
- foundational: Frey, Muller, Ruck. "The Tate Pairing and the Discrete Logarithm Applied to Elliptic Curve Cryptosystems." IEEE Transactions on Information Theory, 1999 (Tate-pairing computation technique used for verification).

### Verbatim extracts
- "The signature length is half the size of a DSA signature for a similar level of security."
- "a level of security similar to 320-bit DSA signatures"
- "It is an open problem to build elliptic curves" with security multiplier above 6.
- "This is under half the size of the standard 320-bit DSS signature"
- "verification is much more expensive than signature generation because it requires computing two pairings"
- "open problem whether one can build a family of hyper-elliptic curves of genus 3"
