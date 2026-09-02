## [SOK-CRYPTOERASURE-EPRINT-26] SoK: Cryptographic Erasure on Public Ledgers — Application-Layer Architectures, Key-Lifecycle Adversaries, and GDPR Art. 17 Equivalence
**Citation:** Yitebeier Aikebaier. "SoK: Cryptographic Erasure on Public Ledgers: Application-Layer Architectures, Key-Lifecycle Adversaries, and GDPR Art. 17 Equivalence." IACR Cryptology ePrint Archive, 2026. Author affiliation: Nexum Ledger Ltd, United Kingdom.
**Retrieved:** full text (no `targets-deduped.json` record for this key)
**Source URL:** https://www.nexumledger.com (author/company site cited in the paper's own header); IACR ePrint identifier not captured in the retrieved text
**Domain:** C (also relevant to E — key lifecycle and identity — and to a lesser extent J, given the paper's production-deployment measurement)

### What it does
This systematization of knowledge (SoK) classifies mechanisms that make personal data on an append-only,
tamper-evident public ledger legally erasable — satisfying obligations such as the European Union's
General Data Protection Regulation (GDPR) Article 17, the "right to erasure" — without rewriting the
ledger itself. Because a public blockchain is append-only by construction, the paper's whole design space
excludes chain-rewriting mechanisms (chameleon-hash-based redactable blockchains, hard forks,
permissioned-chain history rewrites) and instead classifies architectures that leave every on-chain byte
untouched and instead destroy the cryptographic key material needed to decrypt data referencing it,
rendering it permanently unreadable while every byte the ledger recorded remains exactly as written. The
paper organizes this design space along two axes into a twelve-cell grid: data locus (on-chain ciphertext,
anchor-only with off-chain ciphertext, or a hybrid combining both) and key custody (a single custodian; a
(t, n)-threshold committee, where any t of n custodians can jointly hold or destroy the key; a time-lock
scheme releasing the key automatically after a fixed delay; or witness encryption, which gates decryption
on the prover's ability to supply a witness to a stated mathematical problem rather than possessing a
literal key). It then defines a formal adversary model — a "destruction oracle" — parameterized by three
values: epsilon, the fraction of key material a side-channel might leak to an adversary during the
destroy operation itself; k/n, the fraction of a threshold custody committee an adversary can coerce or
corrupt before erasure fails; and T, the number of years the destruction claim's security is assumed to
hold against the best publicly known cryptanalytic attack. Under specific parameter choices, the paper
proves a formal equivalence, "Destruction-IND," between "the key is destroyed" and "the plaintext is
deleted," and bridges this cryptographic definition to the European Data Protection Board's (EDPB) own
2025 guidance defining what counts as "render[ing] unrecoverable" for Article 17 compliance on a
blockchain.

### Measured results
The paper evaluates seven representative architectures (labeled A0 through A6, one per populated grid
cell) against eleven engineering, cryptographic, and regulatory criteria. Critically, only one of the
seven — A3, the paper's own author's commercial product — is independently measured by benchmark; the
paper states this explicitly: "The reference implementation (A3 ...) supplies measured values; the other
six are assessed from published numbers and, where unavailable, conservative analytical bounds," and
again, "The A1–A6 estimates are meant to locate architectures relative to each other, not to substitute
for benchmarks; precise head-to-head measurement is future work." Every comparative claim in this entry
therefore rests on one measured system and six order-of-magnitude estimates the paper's own single author
derived, not on six independent benchmarks.

A3 (Nexum-style, anchor-only, single-custodian key) benchmark conditions: cryptographic-core benchmarks
measured with criterion-rs 0.5.1 (a Rust statistical benchmarking harness), 100 samples per measurement,
commit d22fb26, Rust 1.93.1 release build, on an Apple M2 (8-core, 8 GB RAM). End-to-end system benchmarks
measured on a production IONOS Virtual Private Server (VPS), 4 virtual CPUs (AMD EPYC-Milan), 3.5 GiB RAM,
PostgreSQL 16.11, commit 5fd90f1.

| Operation | Measured cost | Conditions |
|---|---|---|
| SHA-256 hash-chain step | 1.30 ± 0.02 µs | 256-byte payload; ~7.4×10^5 steps/s in pure computation |
| AES-256-GCM envelope encryption | 3.75 ± 0.05 µs (256 B), scaling to 148 MiB/s at 16 KB | Per-record data-encryption key (DEK) |
| DEK generation (OS entropy) | 940 ± 50 ns | — |
| DEK wrapping under master key | 2.62 µs | — |
| Merkle-tree root construction (rs_merkle, SHA-256) | 68 µs (100 leaves); 8.0 ± 0.2 ms (10^4 leaves); 79 ± 1 ms (10^5 leaves) | Throughput flat at ~1.26×10^6 leaves/s across all tested sizes |
| Merkle inclusion-proof verification | 6.4 µs (100 leaves); 13.9 µs (10^5 leaves) | O(log n) scaling confirmed |
| Total per-event cryptographic overhead | 7.02 ± 0.01 µs | DEK generation + AES-256-GCM encrypt of 256 B + DEK wrap |
| Event append (hash-chain link + PostgreSQL INSERT) | 390 ± 10 µs/event | ~2,560 events/s single-threaded; cryptographic fraction 1.8% of total |
| Cryptographic erasure (Kms::destroy_key: select key, zero-fill update, insert certificate, update record — 4 SQL operations) | 1.23 ± 0.03 ms/record | ~810 destructions/s |
| Seal and store DEK (generate + encrypt + wrap + INSERT) | 356 ± 4 µs/record | Cryptography is 7.02 µs of this, 2.0% |
| Projected throughput with 5-connection pool | ~10,000–12,000 events/s | Extrapolated, not directly measured at this concurrency; stated by the paper as validating its own "> 10^4 events/s" headline claim |

Comparative table (Table 4), stating explicitly which entries are measured versus estimated: A3's
single-threaded measured throughput is ~2.6×10^3 events/s; A4 ((t,n)-threshold custody) is estimated at
~10^3 events/s, attributed to threshold-reshare overhead each epoch, bounded from published CHURP and YOSO
reshare-cycle numbers, not measured by this paper; A6 (witness encryption) is estimated at ~10^2 events/s,
attributed to pairing-operation cost, bounded from Derler-Slamanig pairing-complexity numbers, also not
measured by this paper. A0 (plaintext, no cryptography, negative control) and A1 (hash-only anchor) are
estimated at greater than 10^5 events/s from Ethereum gas-cost analysis (a base transaction at 21,000 gas)
and standard cloud-storage anchor patterns, not measured.

### Parameters
- Destruction-oracle adversary model parameters: epsilon (side-channel leakage fraction during the
  destroy event), k/n (coercion threshold over a custody committee), T (years the security claim is
  assumed to hold against best-known cryptanalysis). The paper's Table 3 gives what it calls "defensible
  ranges" for three unspecified-in-this-extraction reference settings, not derived or measured values.
- A3's measured side-channel-leakage bound epsilon is reported as approximately 2^-40 under its current
  software-protected master-key deployment, versus a stated target of approximately 2^-60 once a planned
  migration to a FIPS 140-3 Level 4 Hardware Security Module (HSM) is complete — the paper states this
  migration "is on the deployment roadmap," meaning the tighter figure is a target, not a measured value.
- A3's anchor mechanism: SHA-256 Merkle roots over hash-chained event blocks submitted to public
  OpenTimestamps calendar servers, upgradeable from calendar-server attestation to full Bitcoin
  block-header inclusion proof within approximately 10 minutes.

### Stated limitations
The paper states four explicit caveats about its own A3 reference measurement, in its own words: first,
A3 inherits every limitation of a single-custodian (K1) design — its third-party-auditability criterion
reads "vendor" rather than "on-chain" because zeroization attestation depends on trusting the HSM vendor's
certification chain, not a primitive a third party can verify against the ledger itself, and the paper
states the threshold-custody architecture (A4) "genuinely outperforms A3" on this specific axis. Second,
the current production deployment uses a software-protected master key with explicit zeroization rather
than a hardware HSM, so the deployed leakage bound is the weaker ~2^-40, not the ~2^-60 FIPS-140-3-Level-4
target. Third, the production deployment "has not yet been benchmarked against an independent K2
implementation under matched workload" — the order-of-magnitude throughput gap the paper reports against
A4 is read off published numbers for a different system, not a head-to-head experiment on shared
hardware. Fourth, all A3 measurements are taken on one specific cloud configuration (an IONOS VPS with an
AMD EPYC-Milan processor) and one specific development machine (an Apple M2); the paper states their
"portability to other hardware and cloud regions is reported but not tested." Separately, the paper's own
Table 4 states every one of the seven evaluated architectures scores only "partial" on post-quantum
robustness, because AES-256-GCM is exposed to Grover's algorithm (halving effective key length) and the
secp256k1-based anchor signatures used by both Bitcoin and Ethereum are exposed to Shor's algorithm — the
paper states a controller declaring erasure today under an infinite time horizon (T = infinity) "is,
strictly, making a claim that current primitives do not discharge." The paper states time-lock encryption
(architecture A5) provides confidentiality, not erasure — after the delay elapses, the plaintext becomes
recoverable again, so under the paper's own formal definition (Definition 3) "a controller cannot claim
Art. 17 erasure using a pure time-lock." The paper states witness encryption's third-party destruction
auditability is an open problem, because it "reduces to proving a non-existence statement," which the
paper does not claim is currently feasible.

### Requirements it places on the rest of the system
Every architecture in the paper's grid requires an off-chain (or off-primary-chain, for hybrid designs)
component holding the actual key material subject to destruction — the on-chain anchor alone never
contains anything destroyable, so system availability of the off-chain store is a precondition for
verification even after "erasure," and the paper states this off-chain-availability dependency is a
shared failure mode of every anchor-only (L2) architecture in its grid, since "the encrypted store may
become unreachable independently of the on-chain anchor." Threshold-custody architectures (K2) require an
active custodian committee capable of performing a coordinated quorum-refusal or share-erasure action at
destruction time — a property the paper states directly trades vendor trust (single-custodian designs)
for a proactive-reshare protocol whose own overhead the paper's estimated figures attribute as the
dominant cost driving A4's roughly 2.6× lower throughput than A3's measured figure. The GDPR Article 17
equivalence proof the paper constructs depends on the specific parameter choices (epsilon, k/n, T) a
deployment declares matching the destruction-oracle model's requirements — the paper states its
equivalence theorem is "proved only under specific choices of these parameters," so a deployment adopting
a different epsilon/k/n/T combination than the paper's own worked examples must redo the equivalence
argument, not merely cite the paper's result.

### Contradicts
None found against other corpus entries on a measured fact — this is the first entry in this batch
covering exactly this mechanism. Note for downstream synthesis, stated as fact rather than judgment: six
of the seven systems in this paper's own comparative Table 4 are the paper's single author's own
analytical estimates, not independently obtained benchmarks, and the one measured system (A3) is that same
author's own commercial product, deployed by the company (Nexum Ledger Ltd) the author is affiliated with.
A downstream synthesis citing this paper's "A3 outperforms A4/A5/A6 by one to three orders of magnitude in
throughput" should carry this methodological asymmetry explicitly, since no comparison in Table 4 is
between two independently measured systems on matched hardware.

### References worth retrieving
- **Foundational** — cited as reference [17] in this paper: Benhamouda et al., source of the
  (t,n)-threshold destroyed-key construction underlying architecture A4 in this paper's grid.
- **Foundational** — cited as reference [25] in this paper: YOLO YOSO, a second source for the A4
  threshold-committee construction and its reshare-cycle cost figures this paper's A4 throughput estimate
  is bounded from.
- **Foundational** — cited as reference [64] in this paper: Rivest, Shamir, Wagner — the original time-lock
  puzzle construction underlying architecture A5.
- **Foundational** — cited as reference [27] in this paper: Derler, Slamanig — the algebraic-language
  witness-encryption construction underlying architecture A6, whose pairing-complexity numbers this
  paper's A6 throughput estimate is bounded from.
- **Foundational/competing** — cited as reference [52] in this paper: an ICA3PP 2025 systematic literature
  review already covering chameleon-hash and trapdoor-based redactable blockchains, which this paper
  explicitly excludes from its own scope on the stated grounds that this prior survey already covers that
  branch.
- **Foundational** — cited as reference [62] in this paper: Reardon et al. on secure deletion at the
  storage-media layer — explicitly out of this paper's scope but named as the paper covering the layer
  immediately below the one this SoK addresses.
- **Foundational** — cited as reference [56] in this paper: ML-KEM, the NIST-standardized post-quantum
  key-encapsulation mechanism the paper's OP1 (post-quantum open problem) names as one plausible route to
  post-quantum Destruction-IND security.

### Verbatim extracts
- "A controller writing 'we destroyed the key' today has no [formal equivalence proof without specific
  parameter assumptions]." (paraphrased connective; direct clause: "A controller writing 'we destroyed the
  key' today has no")
- "The A1–A6 estimates are meant to locate architectures relative to each other, not to substitute for
  benchmarks; precise head-to-head measurement is future work."
- "throughput gap is three orders of magnitude" — between A3 (measured) and A6 (estimated).
- "delay is not destruction" (Remark 3, on time-lock encryption).
- "a controller cannot claim Art. 17 erasure using a pure time-lock."
- "the production deployment has not yet been benchmarked against an independent K2 implementation under
  matched workload."
