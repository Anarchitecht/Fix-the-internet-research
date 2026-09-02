## [CHOR-JACM-98] Private Information Retrieval
**Citation:** Benny Chor, Oded Goldreich, Eyal Kushilevitz, Madhu Sudan. "Private Information Retrieval." Journal of the ACM, 1998. DOI 10.1145/293347.293350.
**Retrieved:** full text via https://www.wisdom.weizmann.ac.il/~oded/PS/pir.ps — NOTE: the retrieved PostScript file's own embedded metadata (dvips source comment `%%Title: focs.dvi`, 10 pages) identifies it as the FOCS 1995 conference extended-abstract typesetting of this paper, not a re-typeset of the JACM 1998 journal version the citation in the target registry names. Title and all four authors match the registry record exactly; the theorems, proofs, and reference list extracted below are the FOCS 1995 content. Where the JACM 1998 journal version adds material beyond the FOCS extended abstract, that added material is not reflected here. The source file is raw dvips PostScript (glyph-placement commands, not linear extracted text); every quantity below was reconstructed by concatenating the file's parenthesized glyph strings and reading the result, cross-checked against the paper's own theorem numbering.
**Source URL:** https://www.wisdom.weizmann.ac.il/~oded/PS/pir.ps
**Domain:** G

### What it does
Private information retrieval (PIR) lets a user fetch one bit (or block) from a database without
the database learning which bit was fetched. The paper defines PIR for the multi-server, replicated
setting: k identical, non-communicating copies of an n-bit string x are held by k databases DB_1,
..., DB_k; the user wants bit x_i without any single database learning i. Privacy is defined as
follows: for every database DB_l, every possible database content x, and any two indices i and j,
the communication that DB_l observes must be identically distributed whether the user wants x_i or
x_j — an unconditional (not computational-hardness-based) guarantee, since no cryptographic
assumption appears in any of the paper's protocols. The paper's motivating fact, stated and proved,
is that a single database achieves this only by sending the user the entire n-bit database, so every
construction in the paper depends on having at least two non-colluding copies.

Mechanism (basic two-database scheme, Section 3.1): the user picks a uniformly random subset S of
[n] (each index included independently with probability 1/2), sends S to DB_1 and the symmetric
difference of S with the singleton {i} to DB_2. Each database replies with the exclusive-or (XOR) of
the bits at its received index set. The user XORs the two replies to recover x_i. Each database sees
only a uniformly random subset of [n], independent of i, so neither learns which bit was retrieved;
this scheme sends n bits total (no better than trivial download) but is the base case generalized
below.

Mechanism (multi-database cube scheme, Section 3.2): for k = 2^d databases, embed the n-bit string
in a d-dimensional hypercube of side length n^(1/d), associate the target index i with a d-tuple of
cube coordinates, and associate each of the 2^d databases with a distinct binary string of length d
indicating which "side" of each cube dimension it queries. Each database is asked for the XOR of
bits in a uniformly random d-dimensional subcube, with the subcubes across databases correlated so
that XORing all k replies recovers x_i; each individual database sees a uniformly distributed
subcube description, revealing nothing about i. Total communication is 2^d * (d * n^(1/d) + 1).

Mechanism (covering-codes scheme, Section 3.3, Theorem 1): improves the constant number of databases
needed for a given exponent by mapping database indices to codewords of a covering code — a set of k
binary strings of length d such that every binary string of length d is within Hamming distance 1 of
some codeword — instead of requiring all 2^d corners of the cube. For any (d, k) pair admitting a
radius-1, k-word covering code of {0,1}^d, there exists a k-database PIR scheme with communication
complexity k + (2d + (d-1)*k) * n^(1/d). Instantiated at d=3 with the 2-word covering code
{(0,0,0),(1,1,1)} of {0,1}^3, this gives the paper's headline two-database scheme with communication
O(n^(1/3)). At d=4, a 4-word covering code gives a four-database scheme; the paper tabulates the best
known covering codes up to d=8 (citing Honkala's bounds) together with the resulting communication
complexity for each.

Mechanism (polynomial-interpolation scheme, Section 4, Corollary 6): represents the user's desired
index i implicitly via a low-degree polynomial over a finite field GF(q); the user sends field
elements derived from k-1 random polynomials to each of k databases, and each database returns one
field-element evaluation of a related polynomial built from the database contents. Interpolating the
k received values (using that the sum of k such polynomials, evaluated at 0, equals x_i) lets the
user recover the bit while each individual database sees only field elements from polynomials whose
free terms are uniformly random. This scheme generalizes to arbitrary constant k with communication
complexity k * (s + k*sqrt(n) + k) * log_2(q), where s is a function of k and n stated explicitly for
k=2 through k=4 and asymptotically for k >= 5; for general constant k this gives O(n^(1/k))
communication, and is asymptotically better than the covering-codes scheme except at k=2 and k=4,
where covering codes remain superior (O(n^(1/3)) versus O(n^(1/2)) for k=2, matching orders for k=4).

Mechanism (polylogarithmic-database scheme, Section 4, Theorem 14): setting the number of databases
to grow with n — specifically (1/3)*log_2(n) + 1 databases — the same polynomial-interpolation
framework yields communication complexity (1/3)*(1+o(1)) * log_2^2(n) * log_2(log_2(2n)),
polylogarithmic in n. More generally (Theorem 14), for any integer function t(n) and any d(n) =
c*t(n) for constant c > 1, there exists a t-private information-retrieval scheme for d(n) databases
with communication O(t(n) * c^(sqrt(n))) [the paper's own stated bound, sqrt applied to n inside the
c-exponent form as printed]; and for d(n) = t(n)*log_2(n), a t-private scheme exists with
communication polylog(n) * t(n).

Mechanism (privacy against coalitions, Section 7): the schemes above guarantee privacy only against
any single database observed in isolation ("1-private"); the paper states explicitly that in every
scheme given, any two databases jointly can extract information about i from their combined queries,
and in some schemes two colluding databases can fully recover i. Section 7 generalizes the
polynomial-interpolation scheme to guarantee privacy against any coalition of up to t colluding
databases: using t(k-1)+1 databases, field elements distributed via t random degree-t polynomials per
user query (rather than one), and interpolation at t(k-1)+1 points, the resulting scheme is proved
t-private with communication complexity (t(k-1)+1) * (s+1) * log_2(q), reducing to the 1-private
scheme's parameters when t=1.

Mechanism (block retrieval, Section 6): Propositions 10-11 and Corollaries 12-13 show how to convert
a scheme retrieving a single bit per query into one retrieving an m-bit block at m times the
per-block communication of retrieving a single bit from a database of size scaled by m, and,
separately, that for block length ℓ >= n the basic two-database scheme (Section 3.1) gives a
one-round protocol with total communication exactly 4*ℓ — a constant-factor (4x) overhead over
non-private transfer once the retrieved block is at least as large as the database being queried
against.

### Measured results
This is a theoretical paper: every "result" below is a proven asymptotic communication-complexity
bound for a stated construction under stated parameters (number of databases, privacy level, field
size), not an empirical measurement from a running system. No hardware, dataset, or implementation is
described; Section 5 ("Numeric Results," referenced as Figure 2) numerically compares the
covering-codes and polynomial-interpolation schemes at specific database counts and sizes (k = 2, 4,
7, 16; n = 2^20, 2^30, 2^40), but the paper's own tabulated bit-counts for those combinations could
not be reliably recovered from the retrieved PostScript source's glyph-placement encoding (table
cells are positioned by absolute coordinates rather than linear text flow, which the extraction
method used here does not reconstruct), so no specific figure from that table is recorded here. The
paper's own qualitative conclusion from that table is recorded as a comparative finding, not a
number: for k=2, the covering-codes scheme is superior to the polynomial-interpolation scheme
(matching the asymptotic result that covering codes give O(n^(1/3)) versus polynomial interpolation's
O(n^(1/2)) at k=2); for k=4, k=7, and k=16, the polynomial-interpolation scheme is superior,
increasingly so for larger n.

| Scheme | Databases (k) | Privacy level | Communication complexity | Condition |
|---|---|---|---|---|
| Trivial single-database | 1 | none possible beyond full download | n bits | Proved as a lower bound: any 1-database scheme with privacy requires communicating the whole n-bit database |
| Basic two-database XOR scheme (Section 3.1) | 2 | 1-private | n bits (no improvement; base case for later constructions) | one round, XOR-based |
| Cube scheme (Section 3.2) | k = 2^d, any d >= 1 | 1-private | 2^d * (d*n^(1/d) + 1) | one round, XOR-based |
| Covering-codes scheme (Theorem 1) | k = size of a radius-1 covering code of {0,1}^d | 1-private | k + (2d + (d-1)*k) * n^(1/d) | requires a known radius-1, k-word covering code for the chosen d; volume bound requires k >= 2^d/(d+1) |
| Covering-codes scheme instantiated at d=3, k=2 | 2 | 1-private | O(n^(1/3)) | codewords {(0,0,0),(1,1,1)}, a Hamming-perfect code |
| Polynomial-interpolation scheme (Corollary 6) | any constant k >= 2 | 1-private | k * (s + k*sqrt(n) + k) * log_2(q), giving O(n^(1/k)) | q a prime power >= k+1; s given explicitly for k=2 (s = sqrt(n)+2), k=3 (s = sqrt(2) * cube-root(n) + 3), k=4 (s = cube-root(6) * fourth-root(n) + 3), and asymptotically s = (k-1) * k-th-root(n) for k >= 5 |
| Polylogarithmic-database scheme (Theorem 14, specific case) | (1/3)*log_2(n) + 1 | 1-private | (1/3)*(1+o(1)) * log_2^2(n) * log_2(log_2(2n)) | asymptotic in n; the paper states this is close to optimal given the state of knowledge on 1-private schemes at the time |
| General t-private scheme (Theorem 14, general case 1) | d(n) = c*t(n), constant c>1 | t-private (survives coalitions of up to t databases) | O(t(n) * c^sqrt(n)) [as stated in the paper] | any integer function t(n) |
| General t-private scheme (Theorem 14, general case 2) | d(n) = t(n)*log_2(n) | t-private | polylog(n) * t(n) | any integer function t(n) |
| t-private coalition-resistant polynomial scheme (Section 7) | t*(k-1)+1 | t-private, any coalition of up to t databases | (t*(k-1)+1) * (s+1) * log_2(q) | reduces to the 1-private Corollary 6 scheme's parameters at t=1 |
| Block-retrieval overhead, block length ℓ >= n (Corollary 13) | 2 | 1-private | 4*ℓ total communication | one round, built from the Section 3.1 two-database scheme via Proposition 10 |
| Lower bound, two databases, single binary query each | 2 | 1-private | user messages must have length linear in n | proved only for the restricted case of a single binary query per database, stated by the authors as a limited but illustrative lower bound |

Related-work comparison the paper itself draws: Pudlak and Rodl's construction (unrelated
motivation, complexity theory) yields an equivalent two-database PIR scheme with o(n) communication,
more precisely O(n*log_2(log_2(n))/log_2(n)) — an improvement over the trivial n-bit bound but weaker
than this paper's O(n^(1/3)). Babai, Kimmel, and Lokam's independent, concurrent work yields, for
general k, total communication O(k*n^(H_2(1/(k+1)))) where H_2 is binary entropy; at k=2 this gives
O(n^(H_2(1/3))) which the paper approximates as O(n^0.92), better than the Pudlak-Rodl bound but
still worse than this paper's O(n^(1/3)) result at k=2.

### Parameters
Number of databases k: instantiated at k=2 (headline result), general constant k, k=2^d for the cube
scheme, and k growing as (1/3)*log_2(n) for the polylogarithmic scheme. Field size q: any prime power
with q >= k+1 for the polynomial-interpolation scheme. Privacy coalition bound t: t=1 (standard
"1-private," the default across Sections 3-6) generalized to arbitrary t in Section 7. Block length
ℓ: the block-retrieval overhead result is stated specifically for ℓ >= n. Covering-code radius: fixed
at 1 throughout Theorem 1's construction (the paper notes larger radii, e.g., 2 or 3, are applicable
in principle but does not work out their resulting complexity in the extracted text). Dimension d for
the covering-codes scheme: tabulated by the paper (Figure 1, not independently recoverable in this
extraction) for d up to 8, using the best covering codes known at the time, citing Honkala's bounds;
the paper notes the d=3 and d=7 codes used are Hamming codes, which are perfect codes (all
radius-1 balls around codewords are disjoint).

### Stated limitations
Every scheme in Sections 3 through 6 guarantees privacy only against a single database observed in
isolation (1-privacy); the paper states explicitly that in all of these schemes, any two databases
that pool their received queries obtain some information about the desired index i, and in some of
the schemes two colluding databases can fully recover i. The stronger t-private construction of
Section 7 requires t*(k-1)+1 databases for the same underlying k-database polynomial scheme,
increasing communication accordingly, so the paper's own t-private bound is a large-constant-factor
cost for coalition resistance rather than a free upgrade. The paper's own lower-bound result (Section
8 discussion) is explicitly limited: it applies only to the very restricted case of two databases
where the user is permitted a single binary (one-bit) query to each database; the authors state this
"is very restricted with respect to what we want," i.e., it does not establish a general lower bound
for schemes with longer per-database queries, and no stronger general lower bound is proved in this
extended-abstract version. The paper does not address a computational (cryptographic-hardness-based)
relaxation of privacy anywhere in the extracted text — every scheme here provides unconditional,
information-independent privacy against one (or t) databases, with no discussion of a single-database
computational PIR variant; that direction is developed only in later, separate papers (Kushilevitz
and Ostrovsky, FOCS 1997, is the earliest single-server construction and is not this paper).

### Requirements it places on the rest of the system
Every scheme (Sections 3-6) requires at least two physically or organizationally separate copies of
the database that do not communicate their received queries to each other; the 1-privacy guarantee is
voided the moment any two of the k databases pool what they each received, since the paper states
directly that colluding pairs can extract information about, and in some schemes fully recover, the
desired index. A design wanting resistance to coalitions of up to t colluding database operators must
use the Section 7 construction specifically, provision t*(k-1)+1 separate database replicas instead
of k, and accept the correspondingly larger per-query communication; the ordinary Corollary 6 scheme
gives no partial coalition resistance at any intermediate t. Every database replica must hold an
identical, static copy of the n-bit string x for the stated bit-recovery correctness proofs to apply;
the paper's protocols are not proven correct against a database that returns an answer to a
different data content than the one the other replicas hold. The user must generate and send
uniformly random field elements or subsets on every query (the source of the privacy guarantee); a
weakened randomness source at the user directly weakens the proved privacy bound, though the paper
does not itself analyze partial-randomness degradation. The described one-round protocols require no
persistent per-user server-side state and no shared secret key between user and database — privacy
holds unconditionally for any adversary, without a cryptographic hardness assumption — so a system
built on these schemes does not need a key-management or key-distribution component for the PIR layer
itself, unlike later single-server, cryptographic-assumption-based PIR schemes.

### Contradicts
None found within the extracted text; this is the field's foundational multi-server PIR paper and the
paper positions its own results as new upper bounds against the prior related work it cites (Pudlak
and Rodl; Babai, Kimmel, and Lokam), not as contradicting them. Cross-paper in this corpus: this
paper's results concern multi-server, non-colluding-server PIR exclusively; MENON-SP-22,
HENZINGER-USENIXSEC-23, and MENON-USENIXSEC-24 in this corpus all address single-server PIR (a
setting this paper does not construct a scheme for, and does not claim is impossible — it simply is
not addressed in the extracted text), so no direct numeric comparison applies between this entry and
those three.

### References worth retrieving
- Pudlak, Rodl, "Modified Ranks of Tensors and the Size of Circuits," STOC 1993 — foundational
  (the first construction, via an unrelated complexity-theory motivation, implying a two-database PIR
  scheme with o(n) communication, the direct predecessor this paper improves on for k=2).
- Babai, Kimmel, Lokam, "Simultaneous Messages vs. Communication," STACS 1995 (appeared) — competing
  (an independent, concurrent construction giving O(k*n^(H_2(1/(k+1)))) communication for general k,
  the paper's own stated comparison point, better than Pudlak-Rodl but worse than this paper's bound).
- Beaver, Feigenbaum, "Hiding Instances in Multioracle Queries," STACS 1990 — foundational (introduces
  low-degree polynomial techniques this paper's polynomial-interpolation scheme, Section 4, builds
  on and cites as its starting point).
- Beaver, Feigenbaum, Kilian, Rogaway, "Security with Low Communication Overhead," CRYPTO 1990 —
  foundational (further develops the polynomial technique; the paper states its Section 4.2 scheme is
  an improved variant of a construction derivable from this paper's Remark 5.2).
- Abadi, Feigenbaum, Kilian, "On Hiding Information from an Oracle," Journal of Computer and System
  Sciences 39:1, 1989 — foundational (the instance-hiding model, related to but distinct from this
  paper's PIR model, discussed explicitly in the related-work section).
- Honkala, "Modified Bounds for Covering Codes," IEEE Transactions on Information Theory 37:2, 1991 —
  foundational (the source of the best-known covering-code sizes this paper's Theorem 1 construction
  and Figure 1 table depend on).
- Rivest, Adleman, Dertouzos, "On data banks and privacy homomorphisms," in Foundations of Secure
  Computation, 1978 — foundational (early work on computing over encrypted/hidden data, cited in the
  paper's introductory discussion of related privacy models).

### Verbatim extracts
"each individual database gets no information on the identity of the item retrieved by the user."
"achieving this type of privacy requires communicating the whole database, or n bits."
"a two database scheme with communication complexity of O(n^1/3)."
"any two databases get some information about the desired index i from their joint queries."
"privacy requires the user to send long messages (i.e., of length linear in the length of the database)."
