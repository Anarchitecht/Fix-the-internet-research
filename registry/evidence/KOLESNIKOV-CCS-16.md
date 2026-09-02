## [KOLESNIKOV-CCS-16] Efficient Batched Oblivious PRF with Applications to Private Set Intersection
**Citation:** Vladimir Kolesnikov, Ranjit Kumaresan, Mike Rosulek, Ni Trieu. "Efficient Batched Oblivious PRF with Applications to Private Set Intersection." ACM CCS, 2016. DOI 10.1145/2976749.2978381.
**Retrieved:** full text via https://eprint.iacr.org/2016/799.pdf
**Source URL:** https://eprint.iacr.org/2016/799.pdf
**Domain:** G

### What it does
BaRK-OPRF (batched, related-key oblivious pseudorandom function) lets two parties run many instances of an oblivious PRF (OPRF) evaluation in one batch, each instance costing about as much as one 1-out-of-2 oblivious transfer (OT). In an OPRF, a receiver holding input r learns F(s, r) for a PRF F and a sender-held seed s, and the sender learns nothing about r. The construction extends the IKNP OT-extension protocol (Ishai, Kilian, Nissim, Petrank, CRYPTO 2003) and the Kolesnikov-Kumaresan (KK, CRYPTO 2013) coding-theoretic reformulation of it. IKNP encodes the receiver's OT choice bit as a repetition code inside an OT-extension matrix; KK replaces the repetition code with a short error-correcting code to pack multiple choices per matrix row. This paper replaces the error-correcting code with a pseudorandom code (PRC): a function C, instantiated from AES, such that for any two distinct receiver inputs r and r', the Hamming distance between C(r) and C(r') is at least the computational security parameter kappa with overwhelming probability. Because a PRC need not be efficiently decodable, its input domain is unbounded, so the same matrix-row mechanism that gave KK a bounded 1-out-of-n OT gives BaRK-OPRF a 1-out-of-poly OT over an unbounded string domain, which the paper interprets as an OPRF. The receiver obtains one PRF output value t = q xor (C(r) . s) per instance; the sender can compute the PRF value for any input string but not which one the receiver holds. The protocol is proved secure in the semi-honest model, in the random-oracle model or under a correlation-robustness assumption generalizing IKNP's.

Applied to private set intersection (PSI), the two parties (Alice with set A, Bob with set B) learn only A intersect B. Bob places his n items into 1.2n Cuckoo-hash bins using 3 hash functions plus a stash of size s; Alice evaluates the OPRF on (3+s)n values, one per Cuckoo-hash slot Bob could have used, and the two parties compare masked outputs to find matches. Because the OPRF output no longer depends on the item's bit length (unlike the prior PSSZ15 protocol, which used one OT per input bit), running time and communication become independent of item bit length.

### Measured results
Server: Intel Xeon E5-2699 v3 2.30GHz, 256 GB RAM, both parties run on the same machine with simulated network conditions via Linux `tc`. LAN: 0.2 ms latency; WAN: 50 MB/s average bandwidth, 96 ms average round-trip latency. Single thread per party. Statistical security parameter sigma=40, computational security parameter kappa=128. Comparison baseline: the PSSZ15 protocol (Pinkas, Schneider, Segev, Zohner, USENIX Security 2015), implemented and run by the same authors on the same hardware for a fair comparison.

Running time in milliseconds, PSI of n elements per party, LAN setting, 128-bit items: PSSZ15 307 ms (n=2^8) to 213,597 ms (n=2^24); BaRK-OPRF-PSI (bit-length-independent) 192 ms (n=2^8) to 58,567 ms (n=2^24). At n=2^20 (LAN), BaRK-OPRF-PSI is 2.8x faster than PSSZ15 for 64-bit items and 3.6x faster for 128-bit items. At n=2^24 (LAN), the corresponding improvements are 2.3x and 3.6x. Computing the intersection of two 2^24-item sets of 128-bit strings takes about one minute with BaRK-OPRF-PSI versus 214 seconds with PSSZ15.

| n (items/party) | PSSZ15 LAN, 128-bit (ms) | BaRK-OPRF-PSI LAN (ms) | PSSZ15 WAN, 128-bit (ms) | BaRK-OPRF-PSI WAN (ms) |
|---|---|---|---|---|
| 2^8 | 307 | 192 | 624 | 556 |
| 2^12 | 443 | 211 | 746 | 585 |
| 2^16 | 1,352 | 387 | 2,198 | 1,259 |
| 2^20 | 13,814 | 3,780 | 23,546 | 7,455 |
| 2^24 | 213,597 | 58,567 | 381,913 | 106,828 |

Communication cost, PSI of n elements per party, 128-bit items: BaRK-OPRF-PSI 2.9x-3.3x lower than PSSZ15; at n=2^20, 3.2x lower. In absolute terms (MB): PSSZ15 411.6 MB at n=2^20 (128-bit), BaRK-OPRF-PSI 127.2 MB at n=2^20 (bit-length-independent). Naive insecure hashing baseline for comparison: 10.0 MB at n=2^20. BaRK-OPRF-PSI is 4.3x slower than the insecure naive-hashing baseline for the largest tested sets.

OT-extension matrix cost per OPRF/OT instance (bits), from Table 1, varying item bit length l and set size n: BaRK-OPRF holds constant at 424-448 bits across all tested (n, l) pairs, while PSSZ15's OT cost scales with l, from 256 bits (n=2^24, l=32) to 3,840 bits (n=2^8, l=128). The ratio of BaRK-OPRF cost to PSSZ15 cost ranges from 0.11 (n=2^8, l=128, BaRK-OPRF cheaper) to 1.75 (n=2^24, l=32, BaRK-OPRF more expensive) — BaRK-OPRF is worse than PSSZ15 for short items (32 bits) at large set sizes.

Parameters used in the implementation (Table 2), by set size n: stash size s (Cuckoo hashing, failure probability bound 2^-40): 12 (n=2^8) down to 2 (n=2^24). Pseudorandom-code width k: 424 bits (n=2^8) to 448 bits (n=2^24). OPRF output length v: 56 bits (n=2^8) to 88 bits (n=2^24).

### Parameters
- Computational security parameter kappa = 128.
- Statistical security parameter sigma = 40.
- Cuckoo hashing: 3 hash functions, load factor 1.2 (n items into 1.2n bins), stash size s chosen per PSSZ15's numbers to bound hashing-failure probability to 2^-40; s ranges 2-12 over the tested n = 2^8 to 2^24.
- Pseudorandom-code output width k, chosen so minimum Hamming distance >= kappa with overwhelming probability; empirically k = 4*kappa suffices (paper states output length k=4kappa is sufficient to make near-collisions negligible), rounded up to a multiple of 8; tested values 424-448 bits.
- OPRF output length v = sigma + log2(n^2), rounded up to a multiple of 8; tested values 56-88 bits.
- Item bit length l tested at 32, 64, and 128 bits; BaRK-OPRF-PSI running time and communication are independent of l by construction, confirmed empirically across all three.
- Set size n tested at 2^8, 2^12, 2^16, 2^20, 2^24 elements per party.
- Base OTs: 128 base-OTs via Naor-Pinkas construction, extended via IKNP OT extension.

### Stated limitations
The protocol and its security proof are stated and proved only in the semi-honest adversary model; the paper explicitly separates this from the malicious-adversary line of OT-extension work (ALSZ15, KOS15) and the publicly-verifiable-covert model (KM15), none of which this paper's construction covers. The receiver's OPRF learns t = q xor (C(r).s) rather than the hashed value H(t), which the paper states is a functionality subtlety relative to a standard OPRF definition. The construction realizes many OPRF instances with related keys (the same seed s and code C shared across all instances in a batch), not independent keys. For short items (32 bits) at the largest tested set size (2^24), the prior PSSZ15 protocol is faster than BaRK-OPRF-PSI, so the paper states a hybrid selecting the best subprotocol per (n, l) would be straightforward but was not implemented — results are reported even where BaRK-OPRF is worse, to show the tradeoff.

### Requirements it places on the rest of the system
Requires both parties to run in a semi-honest (honest-but-curious) threat model; the construction offers no defense if either party deviates from the protocol, so a caller needing security against an actively malicious counterparty cannot use this construction as specified. Requires a private symmetric channel over which to run OT-extension messages (base OTs plus subsequent symmetric-key rounds); the paper does not specify network transport. Requires both parties to agree in advance on set-size-dependent parameters (Cuckoo-hash stash size s, pseudorandom-code width k, OPRF output length v) from Table 2, so the calling system must communicate or fix n before the protocol starts, or bound n from above. Requires a source of AES computation for the pseudorandom code C; the paper reports this is cheap only because of hardware AES acceleration, so a caller on hardware without AES-NI would see different concrete cost than measured here. The PSI application requires each item to fit in the tested bit-length range (32-128 bits, upper bound 128 bits per the paper's own hash-then-PSI recommendation for larger item domains).

### Contradicts
None found within this corpus. No other retrieved paper in this batch reports competing PSI running-time or communication figures under comparable conditions.

### References worth retrieving
- **Foundational**: Ishai, Kilian, Nissim, Petrank, "Extending Oblivious Transfers Efficiently," CRYPTO 2003 (IKNP OT extension, the base protocol this work modifies).
- **Foundational**: Kolesnikov, Kumaresan, "Improved OT Extension for Transferring Short Secrets," CRYPTO 2013 (the KK coding-theoretic reformulation this work extends).
- **Competing**: Pinkas, Schneider, Segev, Zohner, "Phasing: Private Set Intersection Using Permutation-Based Hashing," USENIX Security 2015 (PSSZ15, the direct performance baseline throughout this paper).
- **Competing**: Pinkas, Schneider, Zohner, "Faster Private Set Intersection Based on OT Extension," USENIX Security 2014 (PSZ14, the paradigm PSSZ15 and this work both build on).
- **Competing**: Freedman, Ishai, Pinkas, Reingold, "Keyword Search and Oblivious Pseudorandom Functions," TCC 2005 (FIPR05, introduces OPRF, alternative construction based on Naor-Reingold PRF requiring exponentiations).
- **Foundational**: Huberman, Franklin, Hogg, "Enhancing Privacy and Trust in Electronic Communities," EC 1999 (Diffie-Hellman-paradigm PSI with lower communication but, per PSSZ15's measurement cited here, over 200x slower computation than OT-based protocols).
- **Attack-adjacent (malicious-model OT extension)**: Asharov, Lindell, Schneider, Zohner, "More Efficient Oblivious Transfer Extensions with Security for Malicious Adversaries," EUROCRYPT 2015.
- **Attack-adjacent (malicious-model OT extension)**: Keller, Orsini, Scholl, "Actively Secure OT Extension with Optimal Overhead," CRYPTO 2015.

### Verbatim extracts
- "requires only 3.8 seconds to securely compute the intersection of 220-size sets"
- "our protocol is only 4.3× slower than the insecure naïve hashing approach"
- "our communication cost is 2.9–3.3 × faster than Pinkas et al."
- "our work is strictly in the semi-honest security model"
- "Diffie-Hellman-based protocols to be over 200× slower than the OT-based ones"
