## [CRITES-CCS-25] SyRA: Sybil-Resilient Anonymous Signatures with Applications to Decentralized Identity
**Citation:** Elizabeth Crites, Aggelos Kiayias, Markulf Kohlweiss, Amirreza Sarencheh. "SyRA: Sybil-Resilient Anonymous Signatures with Applications to Decentralized Identity." ACM CCS, 2025. DOI 10.1145/3719027.3744806.
**Retrieved:** full text via https://eprint.iacr.org/2024/379.pdf (IACR ePrint 2024/379, pre-publication text of the CCS 2025 paper)
**Source URL:** https://eprint.iacr.org/2024/379
**Domain:** F

### What it does
SyRA (Sybil-Resilient Anonymous signatures) lets a user sign messages under a context-specific pseudonym so that two signatures from the same user in the same context are linkable to each other, while signatures from the same user across different contexts reveal nothing that connects them, and each real-world identity can obtain at most one working key. The construction, SASSI (SyRA via Stateless Issuing), realizes this without any issuer having to retain a per-user record after issuance.

A set of n issuers jointly holds shares of one secret key isk. A user proves possession of a real-world identity string s to a threshold t of the n issuers, using an abstract personhood relation the paper leaves unspecified so the construction stays compatible with different real-world identity checks (a signed government certificate, a biometric reading, or an OAuth identity token are all named as possible instantiations). The t issuers then jointly compute, via a distributed verifiable random function (VRF, a function whose output is indistinguishable from random but comes with a proof that it was computed correctly from a hidden key), a pair of values deterministically derived from s and isk: (g^(1/(s+isk)), ĝ^(1/(s+isk))). This pair is the user's secret key. Because the pair is a deterministic function of s and isk, an issuer needs to store nothing after issuance to prevent a repeat issuance from producing a different key — recomputing the function on the same s always yields the same key, so a second issuance attempt on the same identity string yields no new capability. The user then signs a message for a context ctx by evaluating a second VRF using their secret key, producing a pseudonym T = e(h(ctx), û) via a bilinear pairing, and proves in zero knowledge that T was computed correctly. Because T is deterministic in (s, ctx), two signatures under the same identity and context always carry the same T, giving intra-context linkability, while T under two different contexts is pseudorandom and unlinkable to any adversary who does not hold s. The two VRF layers use asymmetric (Type-III) bilinear pairing groups; the paper extends the Dodis-Yampolskiy VRF construction to asymmetric groups to support this.

### Measured results
Performance was measured on one machine: a MacBook Pro with an M3 Max processor, 16-core CPU, 48 GB RAM, macOS 15.1, implementation in Rust 1.83, using the BLS12-381 elliptic curve. Reported figures are median times over 10 iterations per configuration.

| Metric | Value | Configuration |
|---|---|---|
| Signature generation time | 10.42 ms | includes context switching |
| Signature verification time | 11.24 ms | — |
| Signature size | 5.703 KB | — |
| Share aggregation by user (threshold issuance) | 1.08–1.29 ms | rises with issuer-set size, from 5–10 issuers (t=5, n=10) to 150–300 issuers (t=150, n=300) |
| Threshold issuance protocol time among issuers | 0.0651 s to 72.6 s | same six configurations: (t,n) = (5,10), (15,30), (30,60), (50,100), (70,140), (150,300); threshold t fixed at n/2 |

Issuance time rises from 0.0651 s at (t=5, n=10) to 72.6 s at (t=150, n=300); share-aggregation time rises far more slowly, from 1.08 ms to 1.29 ms over the same range. The threshold issuance evaluation assumed an honest-majority adversary corrupting at most t_c = n/2 − 1 participants.

### Parameters
| Parameter | Value used | Range tested |
|---|---|---|
| Issuance threshold t | n/2 | fixed ratio across all six configurations tested |
| Total issuers n | 10 to 300 | six point values: 10, 30, 60, 100, 140, 300 |
| Adversary corruption bound (issuance evaluation) | n/2 − 1 | honest-majority assumption, not varied |
| Elliptic curve | BLS12-381 | not varied |

### Stated limitations
The authors state, as an explicit assumption in a footnote, that SyRA with a single centralized malicious issuer cannot provide privacy, because that issuer could impersonate any user with identity s and trace their signatures — privacy holds only when at least t of the n issuers behave honestly. They leave as an open question whether a construction relying solely on symmetric pairings (avoiding the asymmetric-group requirement) is achievable, noting that both symmetric pairing groups and DLIN-based encryption available as one such alternative reduce performance. Adaptive corruption of issuers is left for future work, and the leak-signatures adversarial interface's information exposure under adaptive corruption is stated as an open question, including whether key-evolving VRFs could reduce it. Comprehensive credential revocation is stated to be out of scope; the paper sketches an initial mechanism (publishing one group element û per revoked identity) but states this mechanism does not provide forward security in a non-interactive manner, because revealing û retroactively links all of that user's past pseudonyms. Extending SyRA to attribute-based credentials with better efficiency than the composition approach given (running SyRA and a separate attribute-based credential scheme side by side) is left for future work. The paper does not evaluate the personhood-relation-checking step itself (verifying a government certificate, biometric reading, or OAuth token) — the performance numbers cover only the cryptographic issuance and signing steps once a valid witness for the personhood relation is already available.

### Requirements it places on the rest of the system
SyRA requires an external mechanism supplying the personhood relation R_s — a way to verify that a claimed real-world identity string s is genuinely tied to one physical person and not previously used. The paper explicitly does not build this: it lists a signed government certificate (e.g., an X.509 attribute certificate over a national ID), a biometric reading (citing Worldcoin), or an OAuth/OpenID identity token (citing zkLogin) as possible instantiations, but the security of Sybil resistance is only as strong as whichever personhood check is plugged in. SyRA requires a set of n issuers of which at least a threshold t (t = n/2 in the evaluated configurations) act honestly; if fewer than t issuers are honest, both privacy and, per the ideal-functionality definition, Sybil resistance guarantees fail. The construction requires no communication channel from the issuers to a persistent state store — issuers hold only their long-term VRF key share and need not retain any per-user record — but each issuance protocol run does require the participating threshold of issuers to be online simultaneously to jointly compute the distributed VRF, using oblivious-transfer-based multiparty multiplication. Verification of a SyRA signature requires the verifying party to already hold the correct issuer verification key ivk for the session; the paper states it does not assume a public-key infrastructure for issuer verification keys or authenticated channels between verifiers and issuers, so a verifier using an incorrect ivk receives no guarantee from the construction. Detecting repeated signatures under the same identity and context requires a verifier to maintain a local key-value store mapping observed pseudonyms T to contexts.

### Contradicts
None found within this corpus. On the specific point the target record flagged for verification — whether the issuer is a genuinely new trusted party rather than a removed one — the paper does not claim to eliminate the trust requirement; it claims only to remove the requirement that issuers retain state, while still requiring a threshold t of n issuers to be honest for both privacy and Sybil resistance to hold. This is a narrower claim than "no trusted party" and should not be represented as the latter.

### References worth retrieving
- competing: A. Maram et al., "CanDID: Can-Do Decentralized Identity with Legacy Compatibility" — the paper states CanDID is the only prior attempt at the same issuer-state problem, using a shared PRF evaluation obfuscation, but requires each issuer to hold state linear in the number of credentials
- competing: F. Baldimtsi, K. K. Chalkias, Y. Ji, J. Wang et al., "zkLogin: Privacy-Preserving Blockchain Authentication with Existing Credentials" — paper states zkLogin does not provide Sybil resistance in either of its two operating modes
- competing: J. Park et al. (2023), "ZK Address Abstraction" — paper states this scheme also does not address Sybil resistance
- foundational: Y. Dodis, A. Yampolskiy (2005), the Dodis-Yampolskiy verifiable random function, extended here to asymmetric (Type-III) bilinear groups
- foundational: C. Gurkan et al. (2021), verifiable unpredictable function (VUF) construction the second VRF layer is inspired by
- competing: A. Sonnino, M. Al-Bassam, S. Bano, S. Meiklejohn, G. Danezis (2019), "Coconut: Threshold Issuance Selective Disclosure Credentials" — paper states Coconut does not provide guarantees the construction here does
- competing: J. Doerner et al. (2023), Threshold BBS+ signatures for distributed anonymous credentials
- foundational: R. Zhang et al. (2020), DECO, a three-party protocol (prover, verifier, TLS server) used here as one candidate mechanism to realize the personhood relation from legacy web services
- competing/attack: Worldcoin whitepaper (2023) — biometric (iris) personhood instantiation, cited as an alternative to certificate- or OAuth-based personhood

### Verbatim extracts
"failure to do so would permit a trivial attack against Sybil resilience" — on why issuers historically needed a persistent identity-to-credential mapping.
"our issuers can be stateless" — the construction's core claim.
"zkLogin ... does not provide Sybil resilience" — explicit statement about a competing system.
"privacy, since in that case, the issuer could always impersonate a real-world user" — the centralized-malicious-issuer limitation.
"Revocation ... is out of scope of this paper and an interesting direction for future work."
"this will not provide forward security, at least in a non-interactive manner" — on the sketched revocation mechanism's limitation.
