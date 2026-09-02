## [GOLDREICH-JACM-96] Software Protection and Simulation on Oblivious RAMs
**Citation:** Oded Goldreich, Rafail Ostrovsky. "Software Protection and Simulation on Oblivious RAMs." Journal of the ACM, 1996. DOI: 10.1145/233551.233553.
**Retrieved:** full text via https://www.wisdom.weizmann.ac.il/~oded/PSX/soram.ps — the file on disk is Rafail Ostrovsky's May 1992 MIT PhD thesis (advisor Silvio Micali). Its own front matter states the JACM 1996 journal version was co-authored with Oded Goldreich, with a shorter proof of the bucket-reshuffle step in section 5.5. The theorem statements and proofs extracted below (the O((log2 t)^3) hierarchical simulation, the Omega(log t) lower bound) are the results the journal version carries forward under the same theorem numbers, per the thesis's own note.
**Source URL:** https://www.wisdom.weizmann.ac.il/~oded/PSX/soram.ps
**Domain:** G

### What it does
An oblivious RAM (ORAM) lets a central processing unit (CPU) run an arbitrary program against untrusted external memory so that the sequence of memory addresses the CPU touches reveals nothing about which addresses the program actually reads or writes, defeating an observer who watches only the address bus. A random-access machine (RAM) is oblivious if the probability distribution over its sequence of accessed memory addresses depends only on the input length, not on the input itself or on the sequence of logical (virtual) addresses the program requested.

The paper's main construction, the hierarchical solution, organizes external memory into N = log(memory size) levels of hash tables of geometrically increasing size, each level i holding 4^i buckets of O(log t) words each, where t is the number of program steps simulated so far. Every logical read or write scans one bucket per level, starting from the smallest level and stopping once the target virtual address is found, then always writes the accessed item back into the first (smallest) level. Once the first level fills, its contents are obliviously reshuffled (via a random hash function acting as a random oracle) into the next level up, cascading a full rebuild of level i into level i+1 once every 4^i accesses, so most accesses touch only the smallest levels. Because every level above the first is only ever modified by this oblivious re-hashing step (never by a direct in-place write), each level is touched at a fixed frequency depending only on its size and elapsed time — this is what makes the simulation "time-labeled," meaning an adversary who tampers with a stored value and observes when it is later touched cannot distinguish a tampered access pattern from a legitimate one.

A simpler "square root" construction (presented first, as a stepping stone) uses two buffers instead of a full hierarchy: a small buffer of size O(sqrt(m)) holding recently touched items, and a main array of size m accessed through a random permutation that changes every sqrt(m) accesses; every logical access scans the small buffer plus one location in the permuted main array.

Applying either oblivious simulation to a physically shielded CPU with k bits of internal memory gives a software-protection compiler: a program is transformed into an encrypted form such that a polynomial-time adversary who can tamper with the external (encrypted) memory learns nothing beyond the program's running time, because the CPU's access pattern to external memory is oblivious.

### Measured results
All results are asymptotic bounds proved by construction and by an information-theoretic counting argument; there is no implementation or empirical measurement.

| Result | Bound | Conditions |
|---|---|---|
| Hierarchical oblivious simulation overhead (Theorem 3 / Theorem B) | O((log_2 t)^3) additional accesses per original step | simulating t steps of an m-memory-location RAM (t <= 2^k) with a probabilistic oblivious RAM of memory size m*(log_2 m)^2, using a random oracle; simulation is on-line and time-labeled |
| Square-root solution overhead (Section 4) | amortized O(sqrt(m) * log^2 m) actions per instruction | permutation of the m-cell main array refreshed after every sqrt(m) original accesses; stated as strictly worse than the hierarchical solution and presented only as an intermediate step |
| Naive full-memory-scan overhead | O(m) | reading and rewriting every one of m memory cells on every access, m = total memory size |
| Naive lookup-table overhead | O(t) | building an address-value table of size max(n, t) and scanning the whole table on each access, where n = input length, t = running time, assuming t > n |
| Software-protection compiler overhead, information-theoretic case (Theorem 4) | O((log_2 t)^3) | combines the hierarchical simulation (Theorem 3) with the reduction from tampering-resistant software protection to oblivious simulation (Theorem 2); uses a random oracle |
| Software-protection compiler overhead, computational case (Theorem 5 / Theorem A) | k^O(1) steps for t original instructions, external-memory blowup bounded by a factor of k | assumes existence of a one-way function with security parameter k; random oracle replaced by a pseudorandom function family (Goldreich-Goldwasser-Micali construction); valid once t is polynomial in k so that (log_2 t)^3 < k^c |
| Lower bound on any oblivious simulation (Theorem 6 / Theorem C) | at least max(m, (t-1) * log_2 m) memory accesses to simulate t steps | proved via a combinatorial "balls in cells" game between a CPU player (bounded to c balls held at once, access to a random function) and an observer; holds even for simulations that see the entire request sequence in advance (i.e. off-line), so it bounds on-line and off-line obliviousness equally |
| Bucket-overflow probability (footnote 8) | negligible, i.e. asymptotically less than 1/n^O(1) | throwing n balls into 4n boxes (buckets), measuring the probability any box receives more than c*log(n) balls, for the hierarchical construction's hashing step |

### Parameters
- k: security parameter of the one-way function used to instantiate the pseudorandom function that replaces the random oracle in the practical (computational) variant; the CPU carries k bits of internal shielded memory and the resulting compiler overhead is k^O(1). The thesis states t must remain polynomial in k (t << 2^k) for the practical bound to hold.
- m: total memory size available to the RAM being simulated (m is at most max(input length, running time)); the hierarchical simulation's oblivious RAM uses memory of size m*(log_2 m)^2.
- c: the number of "balls" (memory items) the CPU player in the lower-bound proof can hold simultaneously; the lower bound Omega(log m) per access is proved for every constant c.
- N: number of hierarchy levels, set to log(m); level i holds 4^i buckets, each bucket of size O(log t) words.
- Bucket capacity: O(log n) words per bucket in the restricted (non-hierarchical) construction and O(log t) words per bucket at hierarchy level i, chosen so bucket overflow under random hashing is negligible (footnote 8).

### Stated limitations
The paper's own lower bound (Theorem 6) proves that the poly-logarithmic overhead achieved cannot be reduced below a logarithmic factor: at least Omega(log m) accesses per original step are unavoidable for any oblivious simulation, so the O((log_2 t)^3) upper bound and the Omega(log t) lower bound leave a gap (log^3 versus log^1) that the paper does not close.

The obliviousness and time-labeling guarantees for the practical (computational) variant rest on treating a pseudorandom function as a substitute for a true random oracle; the paper states this substitution is valid "assuming the existence of a strong one-way function," so the guarantee is conditional on that unproven computational assumption rather than unconditional.

The paper explicitly leaves an extension for future work: a more powerful adversary model for the "obliviously accessed distributed database" application (hiding which communication line in a distributed database is used) is attributed to unpublished work by Simon and Rackoff, cited as personal communication, not solved in this paper.

### Requirements it places on the rest of the system
A physically shielded central processing unit is required to hold the k-bit internal secret state (the pseudorandom function seed and working registers); the security proof assumes this internal region cannot be observed or tampered with by the adversary, only the external memory access pattern is exposed.

The external memory store must let the CPU perform arbitrary reads and rewrites of individual buckets and support a periodic full re-hash (reshuffle) of an entire hierarchy level into the next; a storage layer that cannot be rewritten in place, or that charges materially more for a write than a read, changes the asymptotic overhead analysis, which counts reads and writes uniformly as "accesses."

The construction assumes access to a random oracle in the information-theoretic version, and to a pseudorandom function family (built from a one-way function, per Goldreich-Goldwasser-Micali) in the computational version; whichever a deployment uses must be available to the CPU on every access, since every bucket lookup depends on it.

The time-labeling property (Lemma 1, Section 5.7) requires that data only ever move into the lowest hierarchy level via the defined access protocol, never through any other write path; a system that allows an out-of-band write into a bucket at a level above 1 breaks the fixed per-level touch frequency the tampering-resistance proof relies on.

### Contradicts
None found.

### References worth retrieving
- **Foundational:** N. Pippenger, M. J. Fischer, "Relations Among Complexity Measures," Journal of the ACM 26(2), 1979, pp. 361-381 — the single-tape oblivious Turing Machine simulation result this paper's Theorem B generalizes to the RAM model.
- **Foundational:** R. Ostrovsky, "Efficient Computation on Oblivious RAMs," STOC 1990 — the preliminary conference version of this thesis/paper's own results.
- **Foundational:** O. Goldreich, "Towards a Theory of Software Protection and Simulation by Oblivious RAMs," STOC 1987 — the paper that first posed the software-protection problem this work solves.
- **Foundational:** O. Goldreich, S. Goldwasser, S. Micali, "How to Construct Random Functions," Journal of the ACM 33(4), 1986, pp. 792-807 — supplies the pseudorandom function construction substituted for the random oracle in the computational-security variant.
- **Foundational:** R. Impagliazzo, L. Levin, M. Luby, "Pseudo-Random Generation from One-Way Functions," STOC 1989 — underlies the one-way-function-to-pseudorandomness reduction the practical theorem depends on.
- **Attack/critique-adjacent:** M. Blum, W. Evans, P. Gemmell, S. Kannan, M. Naor, "Checking the Correctness of Memories," FOCS 1991 — the memory-checking application this paper's technique is stated to extend.

### Verbatim extracts
- "the probability distribution of the sequence of ... addresses accessed ... is independent of the particular input" (Section 1.2, definition of oblivious RAM).
- "t steps of an arbitrary RAM(m) program can be simulated (on-line) by less than O(t·(log2 t)3) steps" (Theorem B).
- "any oblivious simulation of arbitrary RAMs should have an average Ω(log t) overhead" (Section 1.2, informal Theorem C).
- "we do not have to modify the bucket when we scan it. Modifications happen only during re-hashing" (Lemma 1 proof, Section 5.7).
- "it must be the case that q > t·Ω(log m)" (Theorem 6 proof, lower bound).
- "the above proof does not use the fact that the simulation needs to be done on-line" (Remark following Theorem 6).
