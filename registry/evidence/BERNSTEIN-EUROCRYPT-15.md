## [BERNSTEIN-EUROCRYPT-15] SPHINCS: Practical Stateless Hash-Based Signatures
**Citation:** Daniel J. Bernstein, Daira Hopwood, Andreas Hülsing, Tanja Lange, Ruben Niederhagen, Louiza Papachristodoulou, Michael Schneider, Peter Schwabe, Zooko Wilcox-O'Hearn. "SPHINCS: Practical Stateless Hash-Based Signatures." EUROCRYPT, 2015. DOI 10.1007/978-3-662-46800-5_15.
**Retrieved:** full text via https://sphincs.cr.yp.to/sphincs-20141001.pdf
**Source URL:** https://sphincs.cr.yp.to/sphincs-20141001.pdf
**Domain:** E

### What it does
SPHINCS produces digital signatures whose security rests only on properties of a cryptographic hash function (one-wayness, second-preimage resistance, and a related "subset-resilience" property), so security holds even against an attacker with a large-scale quantum computer, without requiring the signer to update or track any secret state between signatures.

Every prior practical hash-based signature scheme is stateful: signing reads the secret key and produces both a signature and an updated secret key, and if that update is lost — because a key was copied to a second device, or restored from an old backup — the scheme's security breaks. SPHINCS avoids this by building on a binary certification tree of one-time signature (OTS) key pairs, following a construction proposed by Goldreich: each non-leaf node's OTS key pair signs the hash of its two children's public keys, leaf OTS key pairs sign messages, and the root OTS public key is the overall public key. Every leaf's private key is regenerated pseudorandomly from a single seed whenever needed, so no state persists between signing operations. Goldreich's original construction is stateless but produces multi-megabyte signatures because tree height must equal the full hash output length (256 bits) to bound collision probability, and one-time-signature size grows quadratically in that height.

SPHINCS reduces signature size with two changes. First, it replaces the leaf one-time-signature scheme with a hash-based few-time signature (FTS) scheme, so a leaf can safely sign a small number of colliding messages rather than exactly one, permitting a smaller tree height for the same security level; the paper's chosen FTS is HORST (HORS with trees), an improvement of the existing HORS few-time scheme that replaces HORS's large public key with the root of a binary hash tree over the HORS public-key elements, so the FTS public key becomes a single hash value instead of t separate values, and a signature carries an authentication path per revealed key element rather than the full key set. Second, SPHINCS decomposes the certification tree into a hyper-tree of d layers of height h/d each, generalizing Goldreich's flat h-layer tree of height-1 sub-trees; only the top layer is generated during key generation, reducing key-generation and signing cost from exponential to a function of h and d, at a signature-size cost that scales linearly with d.

The concrete instantiation, SPHINCS-256, targets 128-bit security against quantum attackers and fixes hash-function output length n=256, message-hash length m=512, hyper-tree height h=60 across d=12 layers, Winternitz parameter w=16 for the one-time-signature component, HORST secret-key-element count t=2^16, and k=32 revealed elements per HORST signature. All hash, pseudorandom-function (PRF), and pseudorandom-generator (PRG) primitives are built from the ChaCha and BLAKE permutation families rather than a purpose-designed hash function, because the paper states these were selected for measured short-input performance rather than the long-input performance the SHA-3 competition optimized for.

### Measured results

| Result | Value | Conditions |
|---|---|---|
| Signature size | 41,000 bytes | SPHINCS-256 parameters (n=256, m=512, h=60, d=12, w=16, t=2^16, k=32) |
| Public-key size | 1,056 bytes | Same SPHINCS-256 parameters |
| Private-key size | 1,088 bytes | Same SPHINCS-256 parameters |
| Signing time | 47,466,005 cycles (single core) | Intel Xeon E3-1275 (Haswell), 3.5 GHz, Turbo Boost and hyperthreading disabled |
| Signing throughput | More than 200 signatures per second | Same CPU, all 4 cores used simultaneously |
| Verification time | 1,369,060 cycles | Same CPU, single core |
| Key-pair generation time | 3,051,562 cycles | Same CPU, single core |
| Hashing throughput | About 1.6 cycles/byte | Same CPU |
| Parallel F evaluation (8-way) | 405 cycles to hash 8 independent 256-bit inputs to 8 256-bit outputs | Same CPU, AVX2 vectorized implementation |
| Parallel H evaluation (8-way) | 801 cycles | Same CPU, AVX2 vectorized implementation |
| Seed expansion cost | About 1,650,000 cycles | Same CPU |
| HORST signing cost | 14,176,422 cycles (implementation); lower bound 9,879,451 cycles from 65,536 F-evaluations and 65,535 H-evaluations | Same CPU, k=32, t=2^16 |
| WOTS authentication path computation | 2,391,574 cycles (implementation); lower bound 1,842,667 cycles from 32,160 F-evaluations and 2,143 H-evaluations | Same CPU |
| HORS-to-HORST public-key/signature-size reduction | From 2^16 hash values (2 MB) to fewer than 16·32=2^9 hash values (16 KB) for the FTS portion | SPHINCS-256 parameters, t=2^16, k=32 |
| Signature-size comparison to non-quantum-safe classical schemes | Goldreich's original stateless construction produces signatures above 1 MB at n=256, using the Winternitz OTS with straightforward optimizations | n=256, no FTS or hyper-tree optimization applied (baseline the paper improves on) |
| Software footprint | 104 KB total, including BLAKE for message hashing | Complete SPHINCS-256 signing software |
| Memory usage | Fits within the Linux default 8 MB stack limit, no dynamic memory allocation | Implementation keeps the complete HORST tree in memory rather than using treehash to compute authentication paths on the fly |

### Parameters
| Parameter | Meaning | SPHINCS-256 value |
|---|---|---|
| n | Bit length of hashes in HORST and WOTS (Winternitz one-time signature) | 256 |
| m | Bit length of the message hash | 512 |
| h | Height of the hyper-tree | 60 |
| d | Number of layers of the hyper-tree | 12 |
| w | Winternitz parameter for WOTS signatures | 16 |
| t | Number of secret-key elements of HORST | 2^16 |
| k | Number of revealed secret-key elements per HORST signature | 32 |

Derived values from these: signature length ℓ=67, x=6, a=64 (not independently tested — computed from the primary parameters above). The paper states the tested range is a single point (SPHINCS-256) chosen after "searching a large parameter space," not a swept range; it notes that other instantiations could shift the trade-off toward speed or signature size without giving specific alternate values.

Randomized-index tree-height trade-off (Goldreich's construction, cited as background, not SPHINCS-256's own value): choosing tree height h=128 instead of h=256 saves a factor of 2 in signature size and signing speed, at a roughly 2^-30 probability of one-time-signature-key reuse within 2^50 signatures.

### Stated limitations
The implementation is explicitly not optimized for memory usage: it keeps the complete HORST tree in memory during signing rather than computing authentication-path entries incrementally with the treehash algorithm, a choice the authors state trades memory efficiency for implementation simplicity — "although the software is not optimized for memory usage."

The paper states that "designing a new hash function is not within the scope of this paper," so SPHINCS-256's security depends on ChaCha- and BLAKE-derived primitives whose short-input performance the authors selected empirically rather than primitives purpose-built and separately analyzed for this construction.

Security is stated as conditional on a named list of standard-model hash-function properties holding under quantum attack — one-wayness, second-preimage resistance, undetectability of F, second-preimage resistance of H, and subset-resilience of the HORST hash family — each assumed to individually provide 2^128 security; the paper's Theorem 1 states existential unforgeability under this assumption set, not unconditionally.

The paper states the primary attack vector it identifies against the construction is targeting subset-resilience of the HORST hash family directly, rather than any weakness in the tree or hyper-tree structure.

### Requirements it places on the rest of the system
A verifier must have access to the same hash-function definitions (F, H, the message-hash function, and the PRG) as the signer, since signature verification recomputes hash-tree paths using these exact functions; substituting a different hash function without renegotiating the scheme breaks compatibility, not just security.

The scheme requires no persistent mutable state at the signer between signing operations — each leaf's private key material is deterministically regenerated from a single fixed seed — so a system deploying SPHINCS does not need synchronized state across multiple devices holding a copy of the same private key, unlike a stateful hash-based scheme (the paper states this as the specific practical motivation: "if a key is copied from one device to another... security disintegrates" under a stateful scheme, and SPHINCS is designed to avoid this dependency).

The paper's security proof requires an existential-unforgeability-under-adaptive-chosen-message-attack (EU-CMA) model in which the adversary can request q_s signatures on messages of its choosing before attempting a forgery; a deploying system must not expose signing oracles or signing patterns to an adversary in ways that violate the assumptions baked into this bound (for example, the security bound in Theorem 1 is stated as a function of q_s, the number of adaptive signature queries permitted to the adversary).

A system provisioning storage or bandwidth for signatures must budget 41,000 bytes per signature and 1,056/1,088 bytes for public/private keys respectively — roughly two orders of magnitude larger than typical elliptic-curve signatures — since these are fixed sizes of the concrete SPHINCS-256 instantiation, not tunable independently of the stated parameter set without re-deriving the security analysis.

A system requiring high signing throughput must provision multi-core hardware to reach the paper's "hundreds of signatures per second" figure; the single-core signing cost (47,466,005 cycles, about 13.6 ms at 3.5 GHz) implies roughly 73 signatures per second on one core, so throughput requirements beyond that scale with available parallel cores.

### Contradicts
None found against other entries in this corpus.

### References worth retrieving
- Merkle, Ralph. "A certified digital signature." Crypto'89, LNCS vol. 435, pp. 218-238, Springer, 1990. — foundational (introduces the Merkle tree construction this paper's hyper-tree generalizes).
- Goldreich, Oded. "Two remarks concerning the Goldwasser-Micali-Rivest signature scheme." Crypto '86, LNCS vol. 263, pp. 104-110, Springer, 1987. — foundational (the stateless certification-tree construction SPHINCS builds on directly).
- Buchmann, Johannes; Dahmen, Erik; Hülsing, Andreas. "XMSS - a practical forward secure signature scheme based on minimal security assumptions." Post-Quantum Cryptography 2011, LNCS vol. 7071, pp. 117-129, Springer, 2011. — competing (a stateful hash-based signature scheme this paper positions itself against as the alternative that requires state tracking).
- Reyzin, Leonid; Reyzin, Natan. "Better than BiBa: Short one-time signatures with fast signing and verifying." Information Security and Privacy 2002, LNCS vol. 2384, pp. 1-20, Springer, 2002. — foundational (introduces HORS, the few-time signature scheme HORST directly extends).
- Hülsing, Andreas. "W-OTS+ — shorter signatures for hash-based signature schemes." Africacrypt 2013, LNCS vol. 7918, pp. 173-188, Springer, 2013. — foundational (the Winternitz one-time signature variant used as the OTS component in SPHINCS-256).
- Song, Fang. "A note on quantum security for post-quantum cryptography." Cryptology ePrint Archive, Report 2014/709, 2014. — foundational (establishes that the classical security proofs for hash-based signatures remain valid against quantum adversaries, which this paper's post-quantum security claim relies on).
- Buchmann, Johannes; Dahmen, Erik; Klintsevich, Elena; Okeya, Katsuyuki; Vuillaume, Camille. "Merkle signatures with virtually unlimited signature capacity." ACNS 2007, LNCS vol. 4521, pp. 31-45, Springer, 2007. — foundational/competing (an earlier stateful hyper-tree hash-based signature scheme).
- Pieprzyk, Josef; Wang, Huaxiong; Xing, Chaoping. "Multiple-time signature schemes against adaptive chosen message attacks." SAC 2004, LNCS vol. 3006, pp. 88-100, Springer, 2004. — foundational (HORS++, a variant the paper states its HORS-to-HORST tree technique could also be applied to, producing "HORST++").

### Verbatim extracts
- "every practical hash-based signature scheme in the literature is stateful"
- "If the update fails... then security disintegrates."
- "they can sign hundreds of messages per second on a modern 4-core 3.5GHz Intel CPU"
- "SPHINCS is carefully designed so that its security can be based on weak standard-model assumptions, avoiding collision resistance and the random-oracle model"
- "designing a new hash function is not within the scope of this paper"
- "the software is not optimized for memory usage"
- "reduces the FTS part of the full signature from 2^16 hash values... to fewer than 16·32=2^9 hash values, i.e., from 2 MB to just 16 KB"
