## [SHACHAM-ASIACRYPT-08] Compact Proofs of Retrievability
**Citation:** Hovav Shacham, Brent Waters. "Compact Proofs of Retrievability." ASIACRYPT, 2008. DOI: 10.1007/978-3-540-89255-7_7.
**Retrieved:** full text via https://eprint.iacr.org/2008/073.pdf
**Source URL:** https://eprint.iacr.org/2008/073.pdf
**Domain:** C

### What it does
A proof-of-retrievability (POR) protocol lets a verifier confirm that a storage server holds a client's file in full, without the verifier downloading the file. The client first erasure-encodes the file into n blocks so that any rho-fraction of the n blocks reconstructs the whole file, then computes one homomorphic authenticator per block and uploads blocks plus authenticators to the server. To audit, the verifier sends a challenge naming a random subset of l block indices, each paired with a random coefficient. The server computes one aggregated response: a linear combination of the challenged blocks (weighted by the coefficients) and the matching linear combination of their authenticators, using the homomorphic property to combine many authenticators into one value instead of returning them individually. The verifier checks the aggregated pair against one equation instead of checking each block-authenticator pair separately. The paper gives two constructions: a private-verification scheme built from a pseudorandom function (PRF), secure in the standard model, where only the holder of the secret key can audit; and a publicly-verifiable scheme built from BLS (Boneh-Lynn-Shacham) signatures over a bilinear group, secure in the random oracle model, where anyone holding the public key can audit. Both proofs show that any server that answers an epsilon-fraction of challenges convincingly can have a rho-fraction of the file blocks extracted from it by an algorithm that repeatedly rewinds and re-queries the server.

### Measured results
This is a cryptographic-construction and proof paper with no implementation benchmark or systems evaluation section; its stated results are asymptotic response-length and interaction-count bounds, not measured wall-clock or throughput numbers.

| Quantity | Value | Conditions |
|---|---|---|
| Query length, publicly-verifiable scheme | 20 bytes | 80-bit security level (lambda=80); shortest query of any POR scheme with public verifiability, per the paper |
| Response length, publicly-verifiable scheme | 40 bytes | 80-bit security level; shortest response of any POR scheme with public verifiability |
| Response length, privately-verifiable scheme | 20 bytes | 80-bit security level; matches the response length of the Naor-Rothblum scheme, which uses a weaker security model; the query is longer than in the public scheme |
| Storage overhead, base construction (s=1 sector per block) | 2x beyond the erasure code's own expansion | one authenticator per block, authenticator equal in length to the block |
| Storage overhead, s-sector construction | (1+1/s)x beyond the erasure code's own expansion | one authenticator per block of s sectors; response length becomes (1+s)x the length of one authenticator |
| Extraction interaction count | O(n/(epsilon-omega)) interactions with the cheating prover | n = number of file blocks, epsilon = fraction of challenges the prover answers convincingly, omega = 1/#B + (rho*n)^l/(n-l+1)^l, where #B is the size of the coefficient set, rho is the erasure code rate, l is the number of challenged indices per query |
| Extraction time | O(n^2*s + (1+epsilon*n^2)*n/(epsilon-omega)) | same parameters as above |
| Challenge-coefficient bit length reduction | 80 bits suffices at 80-bit security, versus 160 bits proposed in a prior scheme (Ateniese et al.) | derived from the paper's own security proof, which the authors state gives a tighter bound than the earlier analysis |
| Attack on a related scheme (E-PDP, by Ateniese et al.) | The paper's own attack cheats with almost 9% success probability using no more storage than honestly storing the file | contrasted with Ateniese et al.'s own claim that a malicious server needs 10^140 blocks of storage to cheat with 100% probability under E-PDP; the two figures describe different attack goals (near-certain cheating vs. a lower but nonzero cheating probability under the compact scheme's own model) |

### Parameters
| Parameter | Meaning | Value used / range stated |
|---|---|---|
| lambda | security parameter | typically 80; also discussed at up to 128 |
| p | prime field modulus | lambda bits (private-verification scheme) or 2*lambda bits (public-verification scheme, so that the discrete-log problem is 2*lambda-secure) |
| n | number of file blocks | assumed n >> lambda; no fixed value, file-size dependent |
| rho | erasure code rate (fraction of blocks sufficient to decode) | conservative choice rho = 1/2; can be reduced for applications tolerant of higher error |
| l | number of challenged indices per query | conservative choice l = lambda (e.g., l=80); reducible to l=22 if a 1-in-1,000,000 extraction-failure rate is acceptable |
| B | set from which challenge coefficients are drawn | conservative choice B = {0,1}^lambda (80-bit coefficients); reducible to 22-bit strings under the relaxed error-rate tolerance above |
| s | sectors per block (storage/response tradeoff knob) | s=1 gives the base scheme; larger s reduces storage overhead to (1+1/s)x at the cost of a longer, (1+s)x, response |
| curve choice (public-verification scheme) | pairing-friendly elliptic curve | Barreto-Naehrig curves recommended for lambda up to 128 |

### Stated limitations
The paper does not specify an extraction algorithm as part of the deployed scheme, because the authors do not expect the extraction algorithm to run in production outsourced-storage deployments; it exists only inside the security proof. Deriving short queries in the standard model (rather than the random-oracle model used for the public scheme) is stated as the major remaining open problem. The scheme requires the encoding erasure code to tolerate adversarial (not just random) erasure for the stated security proof to hold; the paper notes that Reed-Solomon-derived codes have this property but are slow to encode and decode for large files, and defers a discussion of faster codes secure only against random erasure to an appendix of the full paper. The authors state that weaker proof-of-data-possession models, which guarantee only that some percentage of blocks (or only the sum of challenged blocks) is available, are unsatisfactory for most practical applications, because partial loss of accounting data or of compression tables destroys the value of the retrieved bytestream.

### Requirements it places on the rest of the system
The client must run an erasure-encoding step over the file before storage; the code's rate rho and the challenge parameters l and #B are jointly constrained so that epsilon-omega stays positive and non-negligible in lambda, so a system deploying this construction cannot pick rho, l, and B independently of each other. The verifier must be able to generate and hold either a private key (private-verification scheme) or a private signing key at file-storage time (public-verification scheme, whose public key alone suffices thereafter for verification) — key management for that per-file secret or per-file authenticator-generation key is external to the paper. The construction assumes the storage server returns responses honestly computed from stored data or fails detectably; the extraction guarantee holds only for a server that is "well-behaved" in the sense of always computing its response as the honest prover algorithm would, conditional on passing verification, which the paper proves follows from the unforgeability of the underlying signature or PRF. Any system layering multiple audits atop this scheme (for example, to bootstrap the weaker E-PDP-style guarantee up to individual-block guarantees) must independently prove that composition sound and account for the added computational and communication overhead, which this paper does not provide.

### Contradicts
The paper explicitly disputes the extraction guarantee claimed for the "E-PDP" scheme of Ateniese et al. (CCS 2007): it shows that E-PDP provides only a guarantee about the sum of challenged blocks, not about individual blocks, and that the authors' own claim of 10^140 blocks needed to cheat with 100% probability describes a different, weaker attack goal than the one this paper's own model addresses. No other paper in this corpus (NEW-8 batch) makes claims about proof-of-retrievability response lengths. None found among the other five keys in this batch.

### References worth retrieving
- Ateniese, Burns, Curtmola, Herring, Kissner, Peterson, Song. "Provable data possession at untrusted stores." CCS 2007. — competing (the RSA-based homomorphic-authenticator scheme this paper improves on and partly refutes the extraction claims of)
- Juels, Kaliski. "PORs: Proofs of retrievability for large files." CCS 2007. — foundational (defines the security model this paper's proofs are cast against)
- Naor, Rothblum. "The complexity of online memory checking." FOCS 2005. — foundational (the "authenticators" model and the 1-bit-MAC scheme compared throughout)
- Bowers, Juels, Oprea. "Proofs of retrievability: Theory and implementation." ePrint 2008/175. — competing (a contemporaneous framework trading off single-audit cost against multi-audit extraction efficiency, explicitly contrasted in section 1.1)
- Boneh, Lynn, Shacham. "Short signatures from the Weil pairing." J. Cryptology 17(4), 2004. — foundational (BLS signatures, the basis of the public-verification scheme)
- Ateniese, Di Pietro, Mancini, Tsudik. "Scalable and efficient provable data possession." SecureComm 2008. — competing

### Verbatim extracts
- "the shortest query and response of any proof-of-retrievability with public verifiability"
- "gives a 2× overhead beyond that imposed by the erasure code"
- "would need to store 10140 blocks in order to cheat with probability 100%"
- "requires no more storage than were the server faithfully storing the file"
- "derandomizing the query in this scheme is the major remaining open problem"
