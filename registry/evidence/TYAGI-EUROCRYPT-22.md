## [TYAGI-EUROCRYPT-22] A Fast and Simple Partially Oblivious PRF, with Applications
**Citation:** Nirvan Tyagi, Sofía Celi, Thomas Ristenpart, Nick Sullivan, Stefano Tessaro, Christopher A. Wood. "A Fast and Simple Partially Oblivious PRF, with Applications." EUROCRYPT, 2022. DOI 10.1007/978-3-031-07085-3_23.
**Retrieved:** full text via https://eprint.iacr.org/2021/864.pdf
**Source URL:** https://eprint.iacr.org/2021/864.pdf
**Domain:** I

### What it does
A partially oblivious pseudorandom function (POPRF) lets a client obtain a keyed function output on a private input `x` bound to a public input `t` (called a tag), while the server that holds the key learns neither `x` nor which output resulted from which request. "Partially oblivious" distinguishes the tag `t`, visible to both parties, from `x`, hidden from the server. The paper's construction, 3HashSDHI, computes `Ev(sk, t, x) = H2(x, H1(x)^(1/(sk+H2'(t))))`, combining the 2HashDH oblivious pseudorandom function (OPRF) of Jarecki, Kiayias, and Krawczyk (JARECKI-ASIACRYPT-14) with the Dodis-Yampolskiy pseudorandom function. To request an evaluation, the client blinds its input as `B = H1(x)^r` for random `r`, sends `B` and the public tag `t`; the server returns `B' = B^(1/(sk+H2'(t)))`; the client unblinds by computing `(B')^(1/r)` and finishing with `H2`. The server additionally produces a Chaum-Pedersen non-interactive zero-knowledge (NIZK) proof of discrete-log equality so the client can verify the response was computed under the claimed public key, without which a malicious server could return arbitrary values undetected. Security is proved in the random oracle model by reduction to a new assumption, one-more gap strong Diffie-Hellman inversion, itself shown implied by the q-discrete-log assumption in the algebraic group model.

Applied to Privacy Pass token issuance, binding a token to a public tag `t` (for example a coarse timestamp such as the current day, or a client autonomous system number) lets a server enforce that a client's tokens are scoped to that tag without needing per-scope secret keys or client-verified key rotation.

### Measured results
All measurements from a Go implementation using the CIRCL cryptographic library, ristretto255 group (bn256 curve for the pairing-based Pythia baseline), on a 2.6 GHz 6-core Intel Core i7 with 32 GB RAM, macOS 10.15.7, averaged over 1000 measurements per operation, input size L fixed at 16 bytes, tag size T varied at 1, 8, and 64 bytes.

| Scheme | T (bytes) | KeyGen (µs) | KeyVerify (µs) | Req (µs) | BlindEv (µs) | Finalize (µs) | Full Ev (µs) |
|---|---|---|---|---|---|---|---|
| 2HashDH | 1 | 0 | 0 | 73 | 222 | 392 | 77 |
| 2HashDH | 64 | 0 | 0 | 84 | 256 | 447 | 89 |
| 3HashSDHI | 1 | 0 | 0 | 85 | 369 | 527 | 125 |
| 3HashSDHI | 64 | 0 | 0 | 75 | 328 | 471 | 110 |
| Pythia | 1 | 168 | 0 | 849 | 4068 | 6070 | 2871 |
| Pythia | 64 | 171 | 0 | 809 | 3922 | 5849 | 2768 |
| ABVOPRF | 1 | 294 | 292 | 74 | 517 | 684 | 370 |
| ABVOPRF | 64 | 15053 | 19196 | 80 | 15305 | 19702 | 15163 |

Excluding precomputable operations (the KeyGen/KeyVerify columns above), 3HashSDHI Finalize cost at T=64 bytes is 472 µs against 447 µs for 2HashDH (approximately 25% relative overhead, per the paper's own framing including all operations), 5843 µs for Pythia, and 19721 µs for ABVOPRF — an order of magnitude above 3HashSDHI at large tag size, attributed by the authors to ABVOPRF's tag-length-linear proof cost.

### Parameters
- Group: ristretto255 for 2HashDH, 3HashSDHI, ABVOPRF; bn256 pairing-friendly curve for Pythia.
- Input size L: fixed at 16 bytes across all measurements.
- Tag size T: 1, 8, 64 bytes, the tested range.
- Averaging: 1000 measurements per operation, on the stated single-machine hardware.

### Stated limitations
3HashSDHI does not support key rotation: distributing per-tag rotation tokens analogous to Pythia's compact rotation token trivially reveals both the old and new secret keys, because the tag hashes are publicly computable. The authors state finding a pairing-free POPRF that also supports key rotation is an open problem. The one-more gap strong Diffie-Hellman inversion assumption's tightness under the algebraic group model reduction is stated as open to further tightening. Binding a token to a public tag reduces the anonymity set of redemption to only the clients issued tokens under that same tag value, a property the authors state holds for the key-rotation alternative as well; the authors state that choosing how to use the tag "requires care and further work to identify best practices." Extending the construction to also carry a private metadata bit (indistinguishable-but-server-decodable, as in Kreuter et al., KREUTER-FC-22's antecedent construction) is left to future work; the authors state a randomized variant would likely be needed, since a deterministic pseudorandom function cannot achieve indistinguishability between private-metadata values.

### Requirements it places on the rest of the system
Verification of a POPRF response requires the client to have the server's public key `pk` in advance and to run the Chaum-Pedersen zero-knowledge proof check on every response; without this check a malicious server can return an arbitrary value. Any protocol using tag-scoped tokens (for example a rate-limiting scheme selecting `t` as an autonomous-system number or time window) needs a mechanism, external to the POPRF itself, for client and server to agree on the tag value before the request — the POPRF does not negotiate or authenticate the tag. Because binding to a tag narrows the anonymity set to clients sharing that tag, any system composing this primitive with an unlinkability requirement must independently bound how coarse-grained the tag partition is; the paper does not supply that bound. The random-oracle-model proof requires hash functions `H1`, `H2` in the construction to be modeled as random oracles; a real deployment must instantiate them with cryptographic hash functions believed to behave as such.

### Contradicts
None found.

### References worth retrieving
- **JARECKI-ASIACRYPT-14** [JKK14] — already in this corpus; 2HashDH OPRF, foundational.
- **[JKX18]** Jarecki, Krawczyk, Xu, "OPAQUE: an asymmetric PAKE protocol secure against pre-computation attacks," EUROCRYPT 2018 — foundational, one of this paper's three target applications.
- **[DGS+18]** Davidson, Goldberg, Sullivan, Tankersley, Valsorda, "Privacy Pass: Bypassing Internet Challenges Anonymously," PoPETs 2018(3) — foundational, defines Privacy Pass and the hoarding/farming attack this paper addresses.
- **[ECS+15]** Everspaugh, Chatterjee, Scott, Juels, Ristenpart, "The Pythia PRF Service," USENIX Security 2015 — competing pairing-based construction, directly benchmarked against.
- **[HIJ+21]** Huang et al. (Facebook), "PrivateStats: De-Identified Authenticated Logging at Scale," 2021 — competing attribute-based VOPRF (ABVOPRF), directly benchmarked against.
- **KREUTER-FC-22** [KLOR20 in this bibliography, listed as CRYPTO 2020 "Anonymous tokens with private metadata bit"] — already in this corpus; competing construction for private-metadata tokens.
- **[SS21]** Silde, Strand, "Anonymous tokens with public metadata and applications to private contact tracing," ePrint 2021/203 — concurrent independent work describing the same 3HashSDHI-equivalent construction with an incomplete security analysis; superseded-by relationship is the reverse (this paper's proof supersedes SS21's incomplete one for the same construction).
- **[JKX21]** Jarecki, Krawczyk, Xu, "On the (in)security of the Diffie-Hellman oblivious PRF with multiplicative blinding," Public Key Cryptography 2021 — attack/critique, on multiplicative-blinding variants of 2HashDH-style OPRFs.
- **[TPY+19]** Thomas et al., "Protecting accounts from credential stuffing with password breach alerting," USENIX Security 2019 — foundational for the breach-alerting application discussed.
- **[CMZ14]** Chase, Meiklejohn, Zaverucha, "Algebraic MACs and keyed-verification anonymous credentials," CCS 2014 — foundational, algebraic-MAC line that KREUTER-FC-22 builds on.

### Verbatim extracts
- "We build the first construction of a partially oblivious pseudorandom function (POPRF) that does not rely on bilinear pairings."
- "the POPRF introduces approximately a 25% overhead (in terms of µs to compute)"
- "the 3HashSDHI construction does not support key rotations even if one omits the final H2 evaluation"
- "Some loss of privacy is fundamental to restricted token use, and choosing how to make use of t requires care"
- "a deterministic primitive (like a PRF) is insufficient to achieve indistinguishability between private metadata bits"
