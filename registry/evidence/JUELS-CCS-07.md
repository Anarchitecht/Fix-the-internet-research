## [JUELS-CCS-07] PORs: Proofs of Retrievability for Large Files
**Citation:** Ari Juels, Burton S. Kaliski Jr. "PORs: Proofs of Retrievability for Large Files." ACM Conference on Computer and Communications Security (CCS), 2007. DOI 10.1145/1315245.1315317.
**Retrieved:** full text via https://doi.org/10.1145/1315245.1315317
**Source URL:** https://doi.org/10.1145/1315245.1315317
**Domain:** C

### What it does
A proof of retrievability (POR) lets a storage archive prove to a verifier that it still holds a specific file in full, through a short challenge-response exchange that never transmits the file. The verifier obtains this assurance without needing a copy of the file itself. The construction, called Sentinel-PORSYS, prepares a file for storage in four steps. First, the verifier splits the file into k-block chunks and applies an (n,k,d)-error-correcting code to each chunk over an l-bit alphabet, expanding the file. Second, the verifier encrypts the expanded file with a cipher that can decrypt each block independently of the others, so missing blocks do not block decryption of the rest. Third, the verifier generates s sentinels — indistinguishable-from-random check values produced by a one-way function keyed on a secret — and appends them to the encrypted blocks. Fourth, the verifier applies a keyed pseudorandom permutation to scatter the positions of all blocks, including sentinels, so an archive cannot locate and selectively preserve only the sentinels. To challenge the archive, the verifier picks q sentinel positions (using the permutation and a counter, so no per-sentinel storage is needed beyond the keys) and asks the archive to return the values at those positions. The archive fails the check if it returns an incorrect value for any queried sentinel. Because sentinel positions are indistinguishable from data-block positions to an archive that has deleted or corrupted some fraction of the file, an incorrect sentinel response is evidence the archive corrupted enough of the file to also have hit that data. To retrieve the file, the verifier requests all blocks, reverses the permutation, strips the sentinels, decrypts, and applies error-correcting decoding to recover the original file even if the archive lost or altered some blocks.

### Measured results
This is a cryptographic construction and security proof, not a system with runtime measurements. The paper works through one worked numerical example of its own security bound rather than running an implementation.

| Parameter set | Derived result |
|---|---|
| File size b = 2^27 blocks (2 gigabytes), block size l = 128 bits, (255,223,32)-Reed-Solomon code (n=255, k=223, d=32), s = 1,000,000 sentinels | Error-coded file expands to b' = 153,477,870 blocks; total file expansion (error coding plus sentinels) is around 15% |
| Same setup, adversary corrupts fraction epsilon = 0.005 of data blocks and unused sentinels | Probability the adversary renders the file unretrievable (bound rho from Theorem 1) is less than 1 in 200,000 |
| Same setup, verifier queries q = 1,000 sentinels per challenge, s = 1,000,000 sentinels total | Verifier can issue 1,000 challenges over the file's life (about one challenge per day for three years); probability of detecting the epsilon = 0.005 corruption on a single challenge is about 71.3%; 12 challenges bring detection-failure probability below 1 in 1,000,000 |

The paper states an example proof size on the order of 32 bytes and an example challenge seed on the order of 128 bits, both as design targets rather than a measured runtime cost.

### Parameters
- l: block size in bits. Example: 128 (matches an AES block).
- (n,k,d): error-correcting code parameters. Example: (255,223,32) Reed-Solomon over GF(2^8), striped to GF(2^128) so a chunk holds n = 255 blocks. d must be even; the code corrects up to d/2 block errors per chunk.
- b: file size in blocks. Example: 2^27 (2 gigabytes).
- s: number of sentinels generated and stored. Example: 1,000,000.
- q: number of sentinels queried per challenge. Example: 1,000. Total challenges supportable is floor(s/q).
- epsilon: adversary's corrupted fraction of data blocks and unused sentinels, used as an input to the security bound, not a protocol parameter the verifier sets. Example value analyzed: 0.005.
- gamma: number of extractor queries per block during recovery, bounded below by 24(j ln 2 + ln b') per Theorem 1, so that extraction of uncorrupted blocks succeeds with overwhelming probability.
- j: security parameter controlling sentinel and key sizes.

### Stated limitations
The construction protects a static file only; the authors state that any naive partial update to the file undermines the security guarantees, because the archive can learn which blocks were touched and are therefore not sentinels, then alter or delete them with impunity once it knows they are not sentinels. Constructing a POR that supports dynamic partial updates is left as future work. The permutation step requires random access across the whole encoded file, which the authors describe as the most resource-intensive part of the scheme in practice, particularly for disk-resident files. Sorting through the paper's own listed design parameters and protocol variants to reach a fully specified, deployable POR system is stated as unfinished work of, in the authors' words, "formidable dimensions." The construction proves only that the archive still holds data sufficient to reconstruct the file; it does not by itself provide file robustness or availability if the sole copy is destroyed, and the authors state that robustness requires separate storage redundancy across multiple systems.

### Requirements it places on the rest of the system
The verifier must generate and retain the sentinel-generation key and the permutation key; loss of these keys makes future challenges and file recovery impossible, since sentinel positions and values are derived from them. The verifier (not the archive) must perform the initial encoding — error-correction, encryption, sentinel insertion, permutation — before handing the file to the archive, so the mechanism requires a trusted setup step outside the archive's control. The cipher used for encryption must support independent per-block decryption (a tweakable block cipher or stream cipher), because the extractor must recover any subset of surviving blocks without access to the missing ones. The system needs a component that supplies unpredictable, uniformly distributed challenge positions (via the keyed permutation) so that the archive cannot distinguish sentinel positions from data-block positions in advance. The number of challenges the verifier can issue over the file's lifetime is capped at floor(s/q); a caller needing more challenges than this must re-encode the file with a larger sentinel count s, which changes the stored ciphertext.

### Contradicts
None found.

### References worth retrieving
- Foundational: M. Blum, W. S. Evans, P. Gemmell, S. Kannan, M. Naor, "Checking the correctness of memories," Algorithmica 12(2/3), 1994 — first general formulation of verifying data integrity without full access.
- Foundational: M. Naor, G. N. Rothblum, "The complexity of online memory checking," FOCS 2005 — closest prior formal security definition; error-codes an entire file as one codeword and MACs blocks, checked by the paper as asymptotic rather than concrete and lacking an extractor definition.
- Competing: G. Ateniese, R. Burns, R. Curtmola, J. Herring, L. Kissner, Z. Peterson, D. Song, "Provable data possession at untrusted stores," 2007 (contemporaneous) — RSA-based homomorphic hashing over individual file blocks, computationally intensive, relies on a knowledge-of-exponent hardness assumption.
- Competing: D.L.G. Filho, P.S.L.M. Barreto, "Demonstrating data possession and uncheatable data transfer," IACR ePrint 2006/150 — RSA-modulus homomorphic hash scheme requiring the prover to exponentiate over the entire file.
- Competing: M. Lillibridge, S. Elnikety, A. Birrell, M. Burrows, M. Isard, "A cooperative Internet backup scheme," USENIX ATC 2003 — earliest POR-like protocol, peer-distributed files with error-coding and per-block spot-checks via separate MACs, no formal definitions or bounds.
- Competing: M. Shah, R. Swaminathan, M. Baker, "Privacy-preserving audit and extraction of digital contents" (cited as Shah et al. [37]) — third-party auditor verifying storage-provider possession via challenge-response MAC over the full encrypted file.
- Foundational: P. Golle, S. Jarecki, I. Mironov, "Cryptographic primitives enforcing communication and storage complexity," Financial Cryptography 2002 — storage-enforcing commitment schemes proving committed storage capacity without proving the specific file is stored.
- Foundational: J. Black, P. Rogaway, "Ciphers with arbitrary finite domains," CT-RSA 2002 — pseudorandom permutation constructions over non-power-of-two domains, used for the permutation step.

### Verbatim extracts
- "the archive retains and reliably transmits file data sufficient for the user to recover F"
- "the security of our POR system depends on q, the number of sentinels per challenge"
- "probability of detecting adversarial corruption of the file...is at least 1−(1−ϵ/4)^q ≈71.3% per challenge"
- "Any naïvely performed, partial updates to F would undermine the security guarantees of our protocol."
- "A POR does not by itself...protect against loss of file contents."
