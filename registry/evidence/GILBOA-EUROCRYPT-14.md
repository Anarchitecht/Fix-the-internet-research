## [GILBOA-EUROCRYPT-14] Distributed Point Functions and their Applications
**Citation:** Niv Gilboa, Yuval Ishai. "Distributed Point Functions and their Applications." EUROCRYPT, 2014. DOI: 10.1007/978-3-642-55220-5_35.
**Retrieved:** full text via https://www.iacr.org/archive/eurocrypt2014/84410279/84410279.pdf
**Source URL:** https://www.iacr.org/archive/eurocrypt2014/84410279/84410279.pdf
**Domain:** G

### What it does
A distributed point function (DPF) splits a point function P_{x,y} — the function that returns y at input x and returns the all-zero string everywhere else — into two keys k0 and k1, such that evaluating each key alone reveals nothing about x or y, and evaluating both keys at any input x' and taking the exclusive-or (XOR) of the two results reproduces P_{x,y}(x'). A key generation algorithm Gen(x, y) produces the pair (k0, k1); an evaluation algorithm Eval(k_b, x') returns one server's share of P_{x,y}(x').

The construction builds a binary tree of depth ceil(log|x|) over the domain of x. Each level of the tree replaces a random portion of the key with a pseudorandom generator (PRG) seed, compressing the key by close to a square root at each level, with the two parties' seeds correlated so that the two evaluation paths cancel to zero everywhere except at the single leaf corresponding to x. The recursion needs only a one-way function (which implies a PRG), not public-key cryptography.

Two-server computationally private information retrieval (PIR): a user who wants bit i of an n-bit database held identically by two non-colluding servers generates DPF keys for the point function that is 1 at index i and 0 elsewhere, sends one key to each server, and each server returns the XOR of its share function over every database bit; the user XORs the two one-bit answers to recover the target bit. The same construction gives two-server private keyword search (membership test against a word set) and non-interactive "PIR writing" (updating one entry of a database secret-shared between two servers without revealing which entry).

### Measured results
No experimental implementation is reported. All figures are derived analytically from the recursive construction.

| Quantity | Value | Conditions |
|---|---|---|
| Key size (asymptotic bound) | roughly 8*kappa*\|x\|^(log_2 3) bits | kappa = PRG seed length, \|x\| = domain bit-length of the point function input, |y| = 1 |
| Key length, exact (recursion depth minimizing key size) | \|x\|=20: 1,298 bytes; \|x\|=40: 5,000 bytes; \|x\|=80: 18,906 bytes; \|x\|=160: 61,943 bytes | Table 1, |y| = 1, recursion depth chosen to minimize key size (depths 2, 4, 5, 6 respectively) |
| Key length, worst case (depth fixed at ceil(log\|x\|)) | \|x\|=20: 4,513 bytes; \|x\|=40: 20,003 bytes; \|x\|=80: 72,941 bytes; \|x\|=160: 241,256 bytes | Table 1, same |x| values, recursion depth fixed at Proposition 1's ceil(log\|x\|) rather than the depth minimizing key size |
| 2-server CPIR communication complexity | 2*m(b, log n, 1) + 2 bits total, where m is the maximum DPF key size for a domain of size n | n = database size in bits; single-bit answer per server (Theorem 2) |
| 2-server CPIR query complexity (using the DPF construction) | O(kappa * (log n)^(log_2 3)) | kappa = PRG seed length; answer complexity 1 bit per server (Corollary 2) |
| Server-side computational cost, naive | n * \|k_b\| pseudorandom bits | evaluating the DPF separately at every one of n domain points |
| Server-side computational cost, tree-optimized | fewer than n + 2*sqrt(n) pseudorandom bits | reusing the PRF tree so each internal node's children are computed once and shared across leaf evaluations |
| Private keyword search query length | O(kappa * nu * log_2 3) bits, answer length 1 bit per server | nu = keyword bit-length; two non-colluding servers, single communication round, no error probability (Theorem 3) |

### Parameters
- kappa: PRG seed length, set by the choice of one-way function; no default value stated, only its role in the key-size formula.
- Recursion depth l: either chosen to minimize key size (exact column of Table 1) or fixed at ceil(log2 |x|) (Proposition 1's bound); the paper reports both and states the fixed-depth bound is "somewhat pessimistic."
- |y|: output length of the point function; Table 1 and most theorems are given for |y| = 1 (binary answers), with the general case handled by an extension (Section on "a more efficient implementation is possible").

### Stated limitations
The paper proves a matching lower bound rather than stating an open engineering gap: any two-server PIR protocol with information-theoretic (not merely computational) secrecy and sublinear-size queries and short answers cannot exist, citing a linear lower bound from Chor, Goldreich, Kushilevitz, and Sudan (reference 8 in this paper's bibliography); this is why the DPF-based CPIR construction relies on a computational (one-way-function) assumption rather than achieving information-theoretic privacy. The paper also proves the converse direction, Theorem 5: any two-server CPIR protocol with sublinear query length and binary answers implies the existence of a one-way function, so the computational assumption cannot be removed.

The paper states, without giving a full proof, that a naive amortization technique is deferred to a "full version" for the case of evaluating a DPF once for every nonzero entry of a database (footnote, computational cost discussion). No implementation, benchmark, or wall-clock timing is reported anywhere in the text.

### Requirements it places on the rest of the system
Two servers that do not collude with each other; the secrecy proof (Theorem 2, Definition 2) is stated for exactly two non-colluding servers holding an identical copy of the database, and the security argument fails if the same party controls both servers or observes both queries.

A one-way function must exist in the deployment's cryptographic setting; if it is only a standard (not exponentially hard) one-way function, the resulting DPF and CPIR scheme achieve standard (polynomial-time) security rather than the stronger exponential-hardness guarantee (Theorem 1).

Both servers must hold byte-identical copies of the database at query time, since the reconstruction algorithm M XORs the two servers' per-bit answers computed over the same n-entry database (Definition 2); a query answered against divergent copies does not reconstruct correctly.

The client must generate a fresh key pair per query (or reuse one for repeated identical queries, which the paper flags as the useful case for the single-bit-answer feature); nothing in the construction supports a third party regenerating a lost key pair.

### Contradicts
None found.

### References worth retrieving
- **Foundational:** B. Chor, O. Goldreich, E. Kushilevitz, M. Sudan, "Private Information Retrieval," Journal of the ACM 45(6), 1998 — the linear lower bound this paper's Theorem 5 relies on.
- **Foundational:** B. Chor, N. Gilboa, "Computationally Private Information Retrieval," STOC 1997 — the 2^O(sqrt(log n)) query-length protocol this paper improves on.
- **Competing:** C. Cachin, S. Micali, M. Stadler, "Computationally Private Information Retrieval with Polylogarithmic Communication," EUROCRYPT 1999 — an earlier polylogarithmic single-server CPIR under a different (Phi-hiding) assumption.
- **Competing:** E. Kushilevitz, R. Ostrovsky, "Replication is NOT Needed: SINGLE Database, Computationally-Private Information Retrieval," FOCS 1997 — single-server CPIR alternative avoiding the two-non-colluding-server requirement.
- **Competing:** C. Gentry, Z. Ramzan, "Single-Database Private Information Retrieval with Constant Communication Rate," ICALP 2005 — competing single-server construction with constant-rate communication.
- **Foundational:** M. Freedman, Y. Ishai, B. Pinkas, O. Reingold, "Keyword search and oblivious pseudorandom functions," TCC 2005 — prior keyword-search protocol this paper's Theorem 3 improves on.
- **Foundational:** R. Ostrovsky, V. Shoup, "Private information storage," STOC 1997 — the "PIR writing" problem this paper's construction also solves.
- **Foundational:** R. Ostrovsky, W. E. Skeith III, "Private Searching on Streaming Data," Journal of Cryptology 20(4), 2007 — the streaming model the keyword-search extension supports.

### Verbatim extracts
- "each of k0 and k1 hides x and y" (Abstract).
- "the length of each query is polylogarithmic in the database size n" (Abstract).
- "This analytical bound is somewhat pessimistic" (Section 1, on the 8*kappa*|x|^log_2(3) key-size formula).
- "computation of each server on a database of size n roughly corresponds to producing n pseudorandom bits" (Section 1).
- "a two-server CPIR protocol with query length o(n) and binary answers. Then a one-way function exists" (Theorem 5).
