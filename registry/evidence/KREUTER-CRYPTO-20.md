## [KREUTER-CRYPTO-20] Anonymous Tokens with Private Metadata Bit
**Citation:** Ben Kreuter, Tancrède Lepoint, Michele Orrù, Mariana Raykova. "Anonymous Tokens with Private Metadata Bit." CRYPTO 2020, Part I, LNCS 12170, pages 308-336. Also posted as IACR ePrint Archive, Report 2020/072 ("Efficient anonymous tokens with private metadata bit"), revised April 21, 2022.
**Retrieved:** full text via https://eprint.iacr.org/2020/072.pdf
**Source URL:** https://eprint.iacr.org/2020/072.pdf
**Domain:** I

**Registry note:** `targets-deduped.json` holds one row keyed `KREUTER-FC-22` whose `title` field
("Anonymous Tokens with Public Metadata and Applications to Private Contact Tracing") belongs to a
different paper — the one extracted in this batch under key `SILDE-FC-22` — while that same row's
`authors` field and `candidate_urls` entry (`https://eprint.iacr.org/2020/072.pdf`) belong to this
paper. The first 2000 characters of `sources/text/KREUTER-CRYPTO-20.txt` state this paper's own
title as "Anonymous Tokens with Private Metadata Bit" by Kreuter, Lepoint, Orrù, and Raykova,
matching the registry row's authors and URL but not its title. Both this paper and the
`SILDE-FC-22` paper cite each other directly (Silde and Strand cite this paper as `[KLOR20a]`; see
that entry), confirming both are real, distinct, correctly retrieved papers rather than the same
document under two keys. The registry row conflates the two; a human should split it into two rows
before the corpus's citation list is generated from `targets-deduped.json`.

### What it does
PMBTokens lets a token issuer embed one secret bit of trust information into an anonymous,
single-use token, readable only by the issuer at redemption time and hidden from everyone else,
including the user who holds the token. The primitive extends Privacy Pass (Davidson et al., PETS
2018), a scheme a content delivery network uses to let a user prove she solved a CAPTCHA once and
redeem that proof many times without the network learning which redemption corresponds to which
issuance. Privacy Pass carries no metadata: every token looks the same regardless of why it was
issued. PMBTokens adds a private metadata bit (PMB) so an issuer can silently mark a user
untrustworthy (assign the PMB value indicating do-not-serve) without the user detecting the mark,
because a marked and an unmarked token remain indistinguishable to anyone without the issuer's
secret key. The paper states this matters operationally: if an issuer instead just stops handing
tokens to a suspected malicious user, the user learns she has been detected and can adjust her
behavior or train a detection-evading model against the visible signal.

The construction starts from the verifiable oblivious pseudorandom function (VOPRF) Privacy Pass
uses, `F_x(t) = x * H_t(t)`, where `H_t` maps an arbitrary string to a group element, `x` is the
issuer's secret key, and the user blinds her input `t` by a random scalar `r` before sending it, so
the issuer's response can be unblinded to the PRF output without the issuer learning `t`. A naive
two-secret-key version (one key per metadata bit) fails: because the VOPRF is deterministic, a user
who requests two tokens on the same input `t` under different keys gets two different outputs, and
a user who requests the same input twice under the same key gets identical outputs — letting a
malicious user probe which of two tokens shares a metadata bit by requesting duplicate inputs. The
paper's fix randomizes issuance: the function becomes `F_(x,y)(t; S) = x * H_t(t) + y * S`, where
`S` is randomness a value both parties contribute to (`S = r^-1 * H_s(r * H_t(t); s)`, with `r` the
user's blinding factor and `s` an issuer-chosen random value sent back with the response), so two
requests on the same `t` under the same key now yield different, unlinkable outputs. Applying two
key pairs `(x_0, y_0)` and `(x_1, y_1)` to this randomized function, one per metadata-bit value,
yields PMBTokens: the issuer picks the key pair matching the bit `b` it wants to embed, computes a
token, and proves in zero knowledge (a DLEQOR proof: an OR of two discrete-log-equality relations)
that the token was computed correctly under one of the two published public keys, without revealing
which one.

The paper additionally removes the zero-knowledge proof from both Privacy Pass and PMBTokens
issuance, at the cost of a weaker unlinkability guarantee: instead of proving correctness, the
issuer's response is either genuinely valid or, if the issuer misbehaves, unblinds to an
indistinguishable-from-random value; the user cannot tell the two cases apart until redemption. The
user regains a batched verification capability by requesting one extra token on a random linear
combination of her already-received tokens' hash inputs and checking that the corresponding linear
combination of outputs matches, letting her verify `n` tokens by one additional token request.
Removing the proof reduces issuer computation, stated as the bottleneck in a high-request-volume
deployment, to a single group-element multiplication per token.

### Measured results

| Result | Conditions |
|---|---|
| Multiplication and communication cost, asymptotic count | Table 1: Privacy Pass (PP) — 6 user multiplications, 3 issuer multiplications, 2 group elements transferred. Okamoto-Schnorr Privacy Pass variant (OSPP) — 9 user, 6 issuer, 2 elements. PMBTokens with DLEQOR proof (PMBT) — 15 user, 12 issuer, 2 elements. Proof-free Privacy Pass (PPB) — 4 user, 1 issuer, 2 elements. Proof-free PMBTokens (PMBTB) — 12 user, 2 issuer, 3 elements |
| Benchmarked wall-clock cost per operation, Rust implementation, Ristretto group over Curve25519, single thread of an Intel Xeon E5-2650 v4 @ 2.20GHz, Ubuntu 18.04.3 LTS, kernel 4.15.0 | Table 2: PP — DLEQ prove 212 µs, DLEQ verify 181 µs, token generation 111 µs, unblinding 286 µs, key generation 84 µs, signing (issuance) 303 µs, redemption 95 µs. PMBT — DLEQOR prove 576 µs, verify 666 µs, token gen. 135 µs, unblinding 844 µs, key gen. 234 µs, signing 845 µs, redemption 235 µs. PPB (proof-free PP) — no DLEQ step; token gen. 197 µs, unblinding 164 µs, key gen. 190 µs, signing 87 µs, redemption 95 µs. PMBTB (proof-free PMBTokens) — no DLEQ step; token gen. 368 µs, unblinding 678 µs, key gen. 512 µs, signing 155 µs, redemption 247 µs |
| PMBTokens issuance and redemption compared to Privacy Pass, same benchmark setting | PMBTokens issuance 845 µs versus Privacy Pass issuance 303 µs; PMBTokens redemption 235 µs versus Privacy Pass redemption 95 µs |
| Speedup over the prior Privacy Pass implementation from Davidson et al. (PETS 2018) | Stated as "between ten and one thousand faster," attributed by the authors jointly to using Curve25519 in place of NIST P-256 and to the choice of implementation language (Rust versus the earlier implementation's language), not isolated as a per-cause figure |
| Chosen Target Gap Diffie-Hellman hardness margin for the paper's unforgeability reduction, an analytical bound (not a wall-clock measurement) | Stated in an appendix as `O(2^94)` security requiring `O(2^64)` sequential adversary queries, concluded to make the underlying attack impractical even for an adversary in close network proximity, given key rotation |

### Parameters
| Parameter | Value used in the paper | Tested range |
|---|---|---|
| Security parameter λ | Instantiated for the benchmark via Ristretto group over Curve25519 | Not varied; single instantiation benchmarked |
| Metadata bit cardinality | 2 (one private bit, values 0 or 1) | Fixed; the construction is defined only for a single bit, not a multi-valued metadata field |
| Hash-to-group method | Elligator 2 map with SHA-512 | Not varied |
| Benchmark hardware | Single thread, Intel Xeon E5-2650 v4 @ 2.20GHz | Single hardware configuration; no scaling study across thread counts or CPU classes |
| WebAssembly cross-compilation target | Compiled via rust-wasm and exercised from JavaScript in Chromium 79.0.3945.130 to generate blinded tokens | Reported as a feasibility demonstration, without its own timing table |

### Stated limitations
The paper's formal treatment of unlinkability explicitly excludes man-in-the-middle adversaries who
intercept and replay a token at redemption time to spend it on a resource other than the one the
user intended — the authors call this token hijacking and state it is "not covered in our
definitions," relying instead on the assumption that user-issuer communication runs over a secure
channel; they sketch a message-authentication-code-based mitigation in an appendix rather than
proving it as part of the core scheme. The proof-free variants (PPB, PMBTB) achieve only a weaker
unlinkability notion than the DLEQ/DLEQOR-proof variants: a user cannot tell, until redemption,
whether a token she received is valid or is an indistinguishable-from-random value the issuer
produced by misbehaving. The security proofs for the verification-oracle-supporting construction
(Appendix J) explicitly do not grant the adversary a Read oracle that returns the private metadata
bit of an adversary-chosen token, only a Verify oracle that checks validity; the authors state this
restriction directly, without arguing security holds if a Read oracle is also exposed.

### Requirements it places on the rest of the system
The scheme requires a random-oracle-model hash function `H_t` mapping arbitrary strings to group
elements (instantiated here via Elligator 2 with SHA-512), and a second random oracle `H_s` used to
derive the shared per-issuance randomness `S`; both are treated as ideal random oracles in the
security proofs, not merely collision-resistant hashes. Unforgeability rests on the Chosen Target
Gap Diffie-Hellman (CTGDH) assumption and unlinkability and metadata-bit privacy rest on the DDH
assumption in the same group, so any deploying system must instantiate a group where DDH is
believed hard (the paper uses Ristretto over Curve25519, a group chosen specifically because DDH
holds there, in contrast to constructions built on pairing groups where DDH is easy). The issuer
must hold, and keep confidential, one secret key pair per metadata-bit value (two key pairs total
for a single private bit); a system supporting `k` independent private bits or a larger metadata
alphabet is not directly given by this construction, since the two-key-pair technique is specific to
a binary embedded value. The construction assumes the transport between user and issuer is a secure
channel, which a deploying system must supply itself; the paper's core protocol does not defend
against a token being intercepted and redeemed by a party other than the one it was issued to. An
issuer wanting the verification-oracle-secure variant (Appendix J) must accept that it can answer
"is this token valid" queries about adversary-supplied tokens but must never expose a means for
answering "what is this token's metadata bit" for an adversary-chosen token, since the security
proof assumes the latter oracle is never available to the adversary.

### Contradicts
None found against other entries in this batch. This paper is the specific competing construction
[`SILDE-FC-22`] argues against on the public-metadata axis: Silde and Strand's paper, in this
corpus, states its own public-metadata protocol achieves smaller communication than an extension of
this paper's construction that would add public metadata to it (their Table 1, "Kreuter et al." row:
`514 * 2N` bits of public key versus their own scheme's constant 1028 bits, for `2^N` possible
metadata strings) — a comparison this paper does not itself make, since this paper defines a private
metadata bit, not public metadata. This is not a contradiction of a measured value; it is two
different papers measuring two different protocol variants for two different problems (private
versus public metadata), and no entry in this batch found a case where the two papers report
different numbers for the same construction.

### References worth retrieving
- foundational: A. Davidson, I. Goldberg, N. Sullivan, G. Tankersley, F. Valsorda. "Privacy Pass: Bypassing Internet Challenges Anonymously." PoPETs 2018. (`[DGS+18]`) — the VOPRF-based scheme this paper extends; every efficiency comparison in this paper and in `SILDE-FC-22` is against this construction.
- foundational: S. Jarecki, A. Kiayias, H. Krawczyk. "Round-Optimal Password-Protected Secret Sharing and T-PAKE in the Password-Only Model." ASIACRYPT 2014. (`[JKK14]`) — source of the 2HashDH-NIZK VOPRF that Privacy Pass and this paper build on.
- competing: S. Jarecki, H. Krawczyk, J. Resch. "Updatable Oblivious Key Management for Storage Systems." (`[JKR18]`, cited for a threshold partially oblivious PRF) — the source of the additive-blinding technique this paper adapts to remove the DLEQ proof.
- competing: M. Chase, S. Meiklejohn, G. Zaverucha. "Algebraic MACs and Keyed-Verification Anonymous Credentials." ACM CCS 2014. (`[CMZ14]`) — a keyed-verification anonymous-credential scheme the paper states could support a similar primitive at higher cost, and notes no extension to a private metadata bit is known for it.
- competing: P. Tsang, M. Au, A. Kapadia, S. Smith. "Blacklistable Anonymous Credentials: Blocking Misbehaving Users without TTPs." (`[TAKS07]`) — a bilinear-map-based blacklisting credential scheme, an alternative approach to marking misbehaving users anonymously.
- attack: D. Boneh, B. Lynn, H. Shacham. "Short Signatures from the Weil Pairing." ASIACRYPT 2001. (`[BLS01]`) — source of the Chosen Target [Gap] Diffie-Hellman assumption family this paper's unforgeability proof formalizes and relies on.
- foundational: D. Chaum. "Blind Signatures for Untraceable Payments." CRYPTO 1982. (`[Cha82]`) — the origin of the blind-signature line of anonymous-credential constructions this paper's related-work section situates itself within.
- superseded-by: This paper's own ePrint revision history (noted in the acknowledgments) records a correction ("2021-01-13" revision) to an error found in the CMBT construction (Appendix J) by an external reviewer; the version on disk is the April 21, 2022 revision, already reflecting that correction.

### Verbatim extracts
"We present new techniques to remove the need for NIZKs, while still achieving unlinkability."
"Our results are between ten and one thousand faster than the previous implementation"
"we do not consider man-in-the-middle adversaries that can steal tokens from honest users"
"we crucially require that the adversary does not get an oracle access that reads the private metadata bit"
"PMBTokens issuance runs in 845 µs and redemption takes 235 µs"
