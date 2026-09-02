## [GREENE-EPRINT-25] Making Post Quantum Key Exchange Efficient: An Implementation with the MLS Protocol
**Citation:** Noah Greene, Britta Hale. "Making Post Quantum Key Exchange Efficient: An Implementation with the MLS Protocol." IACR Cryptology ePrint Archive, 2025.
**Retrieved:** full text via https://eprint.iacr.org/2025/1881.pdf
**Source URL:** https://eprint.iacr.org/2025/1881.pdf
**Domain:** H

### What it does
The Amortized Post-Quantum (APQ) Combiner for Messaging Layer Security (MLS) reduces the per-operation cost of adding post-quantum protection to MLS, a group continuous key agreement (CKA) protocol standardized as RFC 9420. MLS advances a group through epochs, each epoch holding a shared secret derived from a tree-structured key encapsulation mechanism (KEM); replacing the classical KEM with a post-quantum (PQ) KEM secures every epoch update against a future quantum adversary but pays the PQ KEM's bandwidth and computation cost on every update.

The APQ-MLS Combiner, defined in an IETF draft RFC (Joël, Hale, Mularczyk, Tian, draft-ietf-mls-combiner), runs two MLS sessions in parallel with identical membership: one using a traditional (classical) cipher suite, one using a PQ cipher suite. Most epoch updates are Partial Updates, which advance only the traditional session. Periodically a Full Update advances the PQ session, exports a PQ-derived secret from it, and injects that secret into the traditional session as a pre-shared key (PSK) proposal, tying the traditional session's key schedule to PQ-derived material. This paper implements and benchmarks the PQ/T Confidentiality-Only mode, which uses the PQ KEM but no PQ signatures, protecting against harvest-now-decrypt-later attacks but not quantum impersonation. A Full Update is mandatory whenever group membership changes; between membership changes, an application chooses the Full Update frequency, trading PQ forward secrecy for reduced overhead.

The paper built the first implementation of this draft, as a fork of OpenMLS (a Rust MLS implementation), adding a Kyber-based PQ cipher suite (MLS_128_KYBER_AES256GCM_SHA256_Ed25519) alongside a standard classical cipher suite (MLS_128_DHKEMX25519_CHACHA20POLY1305_SHA256_Ed25519). Kyber lacks HPKE's DeriveKeyPair operation, so the implementation feeds Kyber's key generation function an input-keying-material value used as a random-number-generator seed to meet the DeriveKeyPair interface.

### Measured results
All measurements ran on one machine: AMD FX(tm)-6300 six-core processor, 3500 MHz, 3 cores / 6 logical processors, 4x8 GB Corsair Vengeance Pro 1600 MHz DDR3 RAM, Windows 10, with unstated background load. Simulations ran single-threaded, on one machine, sequentially, with no network simulation (message transmission time not modeled). Five configurations were compared: Traditional (classical cipher suite only), PQC (PQ cipher suite only, Full Update every epoch), and three APQC ratios naming the count of traditional Partial Updates per PQC Full Update: APQC-100 (5 Full Updates across 500 epochs), APQC-50 (10 Full Updates), APQC-10 (50 Full Updates). Group sizes tested: 2, 3, 4, 5, then 10 through 100 in steps of 5 up to 50, then 60, 70, 80, 90, 100. Each session ran 500 epochs (499 Update-plus-Commit rounds after the initial Add).

Experiment 1 (full 500-epoch session including initiation), execution time, N=100 samples per configuration per group size via the criterion.rs Rust benchmarking library (100 iterations after a 3-second cache warm-up):
- At group size 100: Traditional 230.50 s, APQC-100 226.05 s, APQC-50 247.13 s, APQC-10 308.95 s, PQC 433.32 s.
- APQC-100 was faster than PQC by 33-50% depending on group size (Table IV, e.g., 26.48% at size 2, up to 50.35% at size 40); APQC-50 by 40-45%; APQC-10 by 20-35% (as low as 0.99% at group size 2).
- CPU cycles (derived by multiplying runtime by the 3500 MHz clock rate, not independently measured) follow the same percentage advantages as runtime, since the figure is a unit conversion of the runtime data.
- Control-message bytes transmitted per epoch by the group owner (average across 500 epochs, single run, no statistical replication because message size is deterministic for fixed parameters): at group size 100, Traditional 8,775.10 bytes, APQC-100 9,957.67, APQC-50 10,926.61, APQC-10 18,678.13, PQC 87,887.32. APQC configurations transmitted 68-88% fewer bytes than PQC (Table VII: 68.54%-88.69% depending on group size and ratio).

Experiment 2 (steady-state, per-epoch cost only, session initiation excluded from the measurement window), average CPU cycles per epoch across the same group-size range, N=100 criterion.rs samples for Traditional and PQC directly; APQC per-epoch cost computed as a weighted average of measured Full-Update cost and measured Partial-Update cost (Partial Update = the Traditional per-epoch measurement, reused), weighted by the ratio's Full:Partial split (e.g., APQC-100 averaged over 5 Full and 495 Partial epochs): at group size 100, Traditional 1,061.86 million cycles, APQC-100 1,082.68, APQC-50 1,103.50, APQC-10 1,270.05, PQC 1,969.88. APQC per-epoch CPU cost was 30-45% lower than PQC (Table IX: 13.30% at group size 2 up to 45.04% at group size 100).

At group sizes 60 and 70, APQC-100 and APQC-50 measured runtime exceeded the Traditional configuration's runtime in some cases; the authors attribute this to uncontrolled confounding variables in the single-machine benchmarking environment, not to a real performance inversion, and instruct readers to rely on the trend lines rather than these individual data points.

### Parameters
| Parameter | Value(s) tested |
|---|---|
| Group size | 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100 |
| Total epochs per simulation | 500 (fixed) |
| Full Update ratios (APQC) | 1:100 (APQC-100, 5 Full Updates), 1:50 (APQC-50, 10 Full Updates), 1:10 (APQC-10, 50 Full Updates) |
| Criterion.rs samples per data point | 100, after a 3-second cache warm-up |
| PQ KEM | Kyber (predecessor to the standardized ML-KEM) |
| APQ mode | PQ/T Confidentiality Only (no PQ signatures on updates) |
| CPU clock rate used for cycle conversion | 3500 MHz |

### Stated limitations
Session initiation (group construction, credential assignment, initial Add) is included in Experiment 1's timing and is not representative of steady-state cost for a continuous key agreement session that in practice initiates once and can run for years; Experiment 2 was built to separate this out. The simulation used a single machine and a single Rust source file with no threading or parallel processing, so the results do not model concurrent multi-client execution. No network transport was simulated; the code measures message serialization only, treating transmission as instantaneous, so the byte figures are message sizes, not end-to-end latency. The APQC-MLS draft RFC calls for an additional synchronization extension to MLS to keep the two parallel sessions correctly matched; this extension was not implemented in the simulation, though the authors state they expect its computational cost to be negligible. The Windows 10 test machine ran unspecified background applications during measurement, an uncontrolled source of noise the authors identify as the likely cause of the anomalous APQC-vs-Traditional crossovers at group sizes 60-70. The implementation code path for APQC-MLS structurally differs from the Traditional-only and PQC-only code paths (APQC requires two concurrent groups with cross-group PSK injection), so the runtime comparison is not a pure like-for-like comparison of identical code doing different work. Peer-reviewed MLS implementation performance benchmarks are stated to be nearly nonexistent in the literature; the authors' methodology follows one master's thesis (Lenz) that benchmarked MLS and Signal implementations without a post-quantum variant.

### Requirements it places on the rest of the system
Requires maintaining two parallel MLS group sessions with identical membership at all times; any membership-management component must apply every Add/Remove to both sessions synchronously. Requires a mandatory Full Update (PQ session advance plus PSK injection into the traditional session) on every membership change; a system with frequent churn forces frequent PQ-cost operations regardless of the chosen amortization ratio. Requires the delivery/ordering layer to carry twice the Commit and Update traffic of a single-session MLS deployment (one traditional, one PQ, per Full Update), plus the PSK Proposal message linking them. Requires an unimplemented MLS extension (per the draft RFC) to keep the two sessions' epoch state synchronized; without it, correctness of the combiner is not established by this paper. Assumes an underlying MLS delivery service providing the same ordering and authentication guarantees ordinary MLS assumes; this paper does not address metadata privacy or delivery-service trust, and evaluates PQ/T Confidentiality-Only mode, so authenticity against a quantum-capable in-path adversary requires the separate Confidentiality+Authenticity mode (with added PQ-signature overhead) not benchmarked here.

### Contradicts
None found.

### References worth retrieving
- Joël, B. Hale, M. Mularczyk, X. Tian, "Flexible Hybrid PQ MLS Combiner," IETF Internet-Draft, Feb. 2025 — foundational (defines the APQC-MLS Combiner protocol this paper implements)
- R. Barnes, B. Beurdouche, R. Robert, J. Millican, E. Omara, K. Cohn-Gordon, "The Messaging Layer Security (MLS) Protocol," RFC 9420, 2023 — foundational
- K. Bhargavan, R. Barnes, E. Rescorla, "TreeKEM: Asynchronous Decentralized Key Management for Large Dynamic Groups," Inria Research Report, 2018 — foundational
- D. Sikeridis, P. Kampanakis, M. Devetsikiotis, "Assessing the overhead of post-quantum cryptography in TLS 1.3 and SSH," CoNEXT 2020 — competing (independent PQ-overhead measurement in a different protocol, reports up to 300% TLS overhead and up to 50% SSH overhead)
- B. Dowling, B. Hale, "Authenticated continuous key agreement: Active MitM detection and prevention," ePrint 2023/228 — foundational
- C. Cremers, B. Hale, K. Kohbrok, "The complexities of healing in secure group messaging: Why Cross-Group effects matter," USENIX Security 2021 — foundational
- J. Alwen, S. Coretti, D. Jost, M. Mularczyk, "Continuous Group Key Agreement with Active Security," TCC 2020 — foundational
- K. Cohn-Gordon, C. Cremers, L. Garratt, J. Millican, K. Milner, "On ends-to-ends encryption: Asynchronous group messaging with strong security guarantees," CCS 2018 — foundational
- K. Hashimoto, S. Katsumata, T. Wiggers, "Bundled authenticated key exchange: A concrete treatment of (post-quantum) signal's handshake protocol," ePrint 2025/040 — competing (post-quantum group-key-exchange alternative)
- F. Linker, R. Sasse, D. Basin, "A formal analysis of apple's iMessage PQ3 protocol," ePrint 2024/1395 — competing (deployed post-quantum messaging protocol)
- S. Lenz, "Evaluation of the messaging layer security protocol: A performance and usability study," Master's thesis, Linköping University — foundational (source of the benchmarking methodology this paper follows)

### Verbatim extracts
"first benchmarking of this method within the context of the Messaging Layer Security (MLS) protocol"
"a clear performance improvement is visible" between APQC and PQC configurations
"between 68% and 88% smaller than the PQC configuration of MLS at the ratios selected"
"between 30-45% faster than the PQC configuration of MLS" for in-session CPU cycles
"likely due to uncontrolled confounding variables in the simulation environment"
"OpenMLS does not support the entire set of cipher suites defined by the MLS specification"
