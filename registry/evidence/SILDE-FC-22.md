## [SILDE-FC-22] Anonymous Tokens with Public Metadata and Applications to Private Contact Tracing
**Citation:** Tjerand Silde, Martin Strand. "Anonymous Tokens with Public Metadata and Applications to Private Contact Tracing." Financial Cryptography and Data Security (FC) 2022. DOI 10.1007/978-3-031-18283-9_9.
**Retrieved:** full text via a Financial Cryptography 2022 preprint copy (candidate URL recorded in `targets-deduped.json` under the conflated row discussed below)
**Source URL:** unresolved in this pass; see registry note
**Domain:** I

**Registry note:** `targets-deduped.json` holds one row keyed `KREUTER-FC-22` whose `title` field
matches this paper exactly, while that same row's `authors` field ("Ben Kreuter, Tancrède Lepoint,
Michele Orrù, Mariana Raykova") and its one `candidate_urls` entry
(`https://eprint.iacr.org/2020/072.pdf`) belong to a different paper — the one extracted in this
batch under key `KREUTER-CRYPTO-20`. The first 2000 characters of `sources/text/SILDE-FC-22.txt`
state this paper's own title and byline as "Anonymous Tokens with Public Metadata and Applications
to Private Contact Tracing," Tjerand Silde (NTNU) and Martin Strand (Norwegian Defence Research
Establishment), matching the registry row's title but not its authors or URL. This paper cites the
other paper directly, as `[KLOR20a]` (Kreuter, Lepoint, Orrù, Raykova, CRYPTO 2020) and `[KLOR20b]`
(the ePrint report 2020/072) in its own bibliography, confirming these are two distinct, correctly
retrieved papers, not one document misfiled under two keys. The registry row conflates the two; a
human should split it into two rows, and should locate a source URL for this paper specifically
(the DOI above resolves to the Springer LNCS chapter) since the one candidate URL on file points to
the other paper instead.

### What it does
This paper extends Privacy Pass-style anonymous single-use tokens (Davidson et al., PETS 2018) with
public metadata: a value attached to a token, such as an expiration date, that is visible to
everyone, including the user, rather than hidden as in the private-metadata-bit construction of
Kreuter, Lepoint, Orrù, and Raykova (`[KLOR20a]`). The stated purpose is mass token revocation
without redistributing keys: an issuer that rotates its signing key daily and encodes the date as
public metadata can invalidate every token issued on a prior day simply by no longer accepting that
day's key, rather than running an individual-token revocation protocol. A rate-limiting or
trust-tier deployment (the paper's example is a content-delivery-network trust signal, the same
setting Privacy Pass targets) uses the public metadata to mark tokens with a category — a date, a
trust tier — that both the issuer and the token holder can read at redemption.

The core mechanism transforms a single Privacy-Pass-style key pair `(x, X = xG)` into a
metadata-dependent key pair by a public, deterministic derivation function `f` applied to the
metadata string `md`: the issuer signs using a derived secret key computed from `x` and `md`, and
publishes (or lets any party recompute) the corresponding derived public key from `X` and `md`,
without needing to generate and publish a distinct key pair for every possible metadata value in
advance. Because both parties can compute the same derived key pair from the metadata value and the
base key, no additional communication is needed to convey which metadata-derived key was used —
in the paper's own words, this differs from Privacy Pass, which needs a fresh, separately published
public key for every distinct metadata string it wants to support, so that supporting `2^N` possible
metadata values costs Privacy Pass `2^N` published public keys, versus a single constant-size public
key for this paper's construction regardless of `N`.

The paper presents three protocol variants, sharing this key-derivation idea: (1) a public-metadata
extension of Privacy Pass itself (Figure 6), matching Privacy Pass's per-transaction communication
cost exactly; (2) a combined public-and-private-metadata extension of PMBTokens (Figure 7, building
directly on the two-key-pair PMBTokens construction of `[KLOR20a]`, extended with an OR-of-two-ANDs
zero-knowledge proof to prove the correct one of two metadata-derived key pairs was used without
revealing the private bit); and (3) a pairing-based construction (Figure 8, adapted from a partially
blind signature scheme of Zhang, Safavi-Naini, and Susilo) that additionally supports public
verifiability — meaning any party, not only the issuer, can check a token's validity, at the cost of
requiring a pairing-friendly group (the paper instantiates it with BLS12-381) rather than a plain
elliptic-curve group.

The paper also describes a deployed application: the authors reimplemented Privacy Pass as a
reusable C# package and integrated it into Smittestopp, the Norwegian government's COVID-19 contact
tracing app, to break an identifiable link between a user's authenticated positive-test verification
step and the anonymous upload of that user's exposure keys to the app's backend, using anonymous
tokens as the unlinking mechanism between the two steps.

### Measured results

| Result | Conditions |
|---|---|
| Communication size per protocol variant, general instantiation with `2^N` possible metadata strings, 128-bit security | Table 1 (bits): Privacy Pass — public key `257*2N`, request 257, signature 769, token 385. DIT (De-Identified Authenticated Telemetry) — public key `257*(N+2)`, request 257, signature `769*(N+1)`, token 385. This paper's public-metadata scheme (Figure 6) — public key 257 (constant, independent of N), request 257, signature 769, token 385. Kreuter et al. extended with public metadata — public key `514*2N`, request 257, signature 1921, token 642. This paper's public+private-metadata scheme (Figure 7) — public key 1028 (constant), request 257, signature 3203, token 642. Abe-Fujisaki RSA partially blind signature — public key 3202, request 3072, signature 3072, token 3200. This paper's pairing-based scheme (Figure 8) — public key 763, request 382, signature 382, token 510. Curve x25519 is used for all non-pairing, non-RSA rows; RSA-3072 for Abe-Fujisaki; BLS12-381 for Figure 8 |
| Concrete telemetry-collection comparison against DIT, modeling a Facebook/WhatsApp-style deployment | Table 2 (bits, one year, daily key rotation, one token signed per user per day): Privacy Pass — public key 93,805 (approximately 12 KB, one key per day for 365 days), request 257, signature 769, token 385. "Privacy Pass+" (Merkle-tree key-transparency variant) — public key 256 (Merkle root), request 257, signature `3330` (256-bit root plus 9 hashes of 256 bits for `ceil(log2(365))=9` plus proof and token overhead), token 385. DIT — public key 2313, request 257, signature 7690, token 385. This paper's Figure 6 scheme — public key 257, request 257, signature 769, token 385 |
| Aggregate daily bandwidth saved versus DIT, under the same one-year/daily-rotation scenario, assuming 2 billion daily-reporting users (the paper's stated WhatsApp-scale assumption) | Stated as "more than 1.7 TB of communication for the Facebook servers on a daily basis," derived from the per-token size difference between the Figure 6 scheme and DIT in Table 2, multiplied by an assumed 2 billion tokens per day; the 2-billion-user figure is stated as a scenario assumption, not independently sourced or measured in this paper |
| "Up to 90% savings in communication" against the state of the art | Stated in the conclusion as the paper's own summary of the Table 2 comparison ("for situations with frequent key-rotation, our protocols can save up to 90% in communication over the state of the art"); this is the same Table 2 computation, not an independent measurement |
| "77% and 90% amortized traffic savings compared to Privacy Pass and DIT respectively" | Stated once, in the abstract, as a headline figure; no worked derivation for the specific 77%-versus-Privacy-Pass figure was found anywhere in the paper's body (Table 1, Table 2, and the surrounding text derive and repeat only the 90%-versus-DIT figure with the WhatsApp/Facebook scenario above). Record the 77% figure as an abstract-only claim without a traceable experimental condition in this text; do not treat it as equivalent in evidentiary weight to the 90% figure |

### Parameters
| Parameter | Value used in the paper | Tested range |
|---|---|---|
| Security level λ | 128 bits, for all instantiated comparisons in Table 1 and Table 2 | Single value; not varied |
| Elliptic curve for non-pairing, non-RSA schemes | Curve x25519 | Fixed |
| Pairing curve for public-verifiability scheme | BLS12-381 | Fixed |
| RSA modulus size, for the Abe-Fujisaki comparison | RSA-3072, with public exponent fixed to 130 bits (at least two bits longer than the public metadata string) | Fixed |
| Key-rotation frequency, WhatsApp/Facebook telemetry scenario | Public key rotated once per year; signing key rotated daily; one token signed per user per day | Single scenario; stated as an assumption ("we assume that Facebook wants to update their public keys only once a year") |
| Metadata cardinality, general Table 1 comparison | `2^N` possible metadata strings, N symbolic | No concrete N is fixed for Table 1; N=365 (days in a year) is used specifically for the Table 2 telemetry scenario |
| Contact-tracing deployment: exposure-key rotation | Temporary Exposure Key (TEK) regenerated daily; Rotating Proximity Identifiers regenerated every 10-20 minutes | Values inherited from the dp3t/Exposure Notification System protocol this paper's tokens are layered onto, not derived within this paper |

### Stated limitations
For the public-plus-private-metadata construction (Figure 7), the paper states its own combined
OR-and-AND zero-knowledge proof is larger than the proof in Kreuter et al.'s private-metadata-only
construction, and states explicitly that "further improvement is an open problem." The
public-verifiability construction (Figure 8) requires pairing-based cryptography, which the authors
state they "would like to avoid ... altogether, but this seems necessary in practice" to achieve
public verifiability in one round of communication; they state achieving public verifiability
without pairings, while keeping a single round of communication, "remains an open problem," citing
two-round alternative constructions as the only known way to avoid pairings for this property. The
paper's conclusion lists three further directions the authors state they have not done: reducing
the number of proofs and group elements in the Figure 7 protocol; removing zero-knowledge proofs
entirely from their schemes as Kreuter et al. do for Privacy Pass and PMBTokens in that paper's
Section 7 (a proof-free variant); and extending the protocols to post-quantum security, which the
paper states as future work continuing prior lattice-based work by Albrecht et al. rather than
something this paper attempts. Separately, the paper's own deployment discussion of the Smittestopp
integration states an operational trust gap the cryptography does not close: the verification
service that issues daily keys could serve different public keys to different users to selectively
track them, and the paper states this attack is "detectable" only if users independently share and
compare their observed public keys with each other, not prevented by the protocol itself; the paper
records that this residual risk was accepted by the Smittestopp stakeholders given time constraints
rather than resolved.

### Requirements it places on the rest of the system
The key-derivation approach requires a public, deterministic function mapping a metadata string to
a key-pair transformation, so that both the issuer and any verifying party can independently
recompute the same derived public key from the base public key and the metadata value; a deploying
system must therefore fix and publish this derivation function and treat the metadata string itself
as public, unauthenticated-but-agreed-upon input both sides already know before the token exchange
(the paper's own efficiency comparison explicitly assumes "all parties know the public metadata ...
and this implicit knowledge is not sent," so the out-of-band agreement on the current metadata value
is a precondition the protocol does not itself provide). The public-and-private combined
construction (Figure 7) inherits every requirement the underlying PMBTokens construction
(`KREUTER-CRYPTO-20` in this corpus) places on the system, including a DDH-hard group and a
random-oracle-model hash function, since it is built as a direct extension of that construction. The
pairing-based public-verifiability construction (Figure 8) requires a pairing-friendly group
(BLS12-381 here), which the paper notes has few production-grade implementations outside academic
or specialized use (citing the Rust implementation used by Zcash as the one exception it is aware
of), so a system choosing this variant takes on a narrower, less-standardized cryptographic-library
dependency than the non-pairing variants. The Smittestopp deployment requires an external identity-
verification step (a government login plus a query to a health registry) to authorize the issuance
of a token in the first place; the anonymous-token layer itself supplies only unlinkability between
that identity-verification step and the later, anonymous upload of exposure keys, not the
verification of eligibility.

### Contradicts
None found against other entries in this batch. This paper is the direct public-metadata-axis
comparison to [`KREUTER-CRYPTO-20`] (which addresses private metadata only) and states its own
Table 1 comparison numbers for "Kreuter et al." as an extension the Kreuter et al. paper itself does
not present (since that paper defines only a private bit, not public metadata); this is not a
disagreement about a shared measurement, since the two papers measure different constructions for
different problems. The paper's own abstract claim of "77% ... amortized traffic savings compared
to Privacy Pass" could not be traced to a specific worked calculation elsewhere in this text (see
Measured Results above); a later synthesis step should not cite the 77% figure with the same
confidence as the 90%-versus-DIT figure, which the text does derive concretely.

### References worth retrieving
- foundational: A. Davidson, I. Goldberg, N. Sullivan, G. Tankersley, F. Valsorda. "Privacy Pass: Bypassing Internet Challenges Anonymously." PoPETs 2018. (`[DGS+18]`) — the base scheme every construction in this paper extends with metadata.
- competing: Ben Kreuter, Tancrède Lepoint, Michele Orrù, Mariana Raykova. "Anonymous Tokens with Private Metadata Bit." CRYPTO 2020. (`[KLOR20a]`) — already retrieved in this batch as `KREUTER-CRYPTO-20`; the direct private-metadata construction this paper extends with public metadata and benchmarks against in Table 1.
- competing: (author names truncated in the extracted bibliography as `[HIJ+21]`) "DIT: De-Identified Authenticated Telemetry at Scale." 2021. — the WhatsApp/Facebook telemetry system this paper's concrete Table 2 comparison targets directly; retrieve to check the DIT-side figures independently.
- competing: M. Abe, E. Fujisaki. "How to Date Blind Signatures." ASIACRYPT 1996. (`[AF96]`) — the RSA partially blind signature scheme compared in Table 1 as the public-verifiability-via-RSA baseline.
- competing: N. Tyagi, S. Celi, T. Ristenpart, N. Sullivan, S. Tessaro, C. Wood. "A Fast and Simple Partially Oblivious PRF, with Applications." ePrint 2021/864. (`[TCR+21]`) — described as concurrent work extending the same oblivious-PRF line to partially oblivious PRFs; the paper refers to this work's own table for a computational-cost comparison it does not reproduce itself.
- foundational: F. Zhang, R. Safavi-Naini, W. Susilo. "Efficient Verifiably Encrypted Signature and Partially Blind Signature from Bilinear Pairings." INDOCRYPT 2003. (`[ZSS03]`) — the partially blind pairing-based signature this paper's public-verifiability construction (Figure 8) is adapted from.
- foundational: C. Troncoso et al. "Decentralized Privacy-Preserving Proximity Tracing." arXiv 2005.12273, 2020. (`[T+20]`, the dp3t protocol) — the contact-tracing protocol this paper's tokens are layered onto for the Smittestopp deployment described in Section 6.
- attack/critique: implicit — the paper states its own earlier version had a flaw in a security game and unforgeability proof, found by Tyagi, Celi, Ristenpart, and Wood and corrected before this version; no separate published critique paper is cited for this, only an acknowledgment.

### Verbatim extracts
"give 77% and 90% amortized traffic savings compared to Privacy Pass"
"our scheme in Figure 6 would decrease the size of the signed token ... by 90%"
"would save more than 1.7 TB of communication for the Facebook servers on a daily basis"
"Further improvement is an open problem."
"it remains an open problem to achieve this without pairings"
"detectable by the users if they share their view of the public keys"
