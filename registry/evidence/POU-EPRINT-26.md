## [POU-EPRINT-26] Proof-of-Uniqueness: Sybil-Resistant Privacy-Preserving Decentralized Identity through Threshold-OPRF and zk-SNARK Registry
**Citation:** Adam Vozda, Martin Perešíni, Juraj Mariani, Ivan Homoliak. "Proof-of-Uniqueness: Sybil-Resistant Privacy-Preserving Decentralized Identity through Threshold-OPRF and zk-SNARK Registry." IACR Cryptology ePrint Archive, 2026.
**Retrieved:** full text (no `targets-deduped.json` record for this key)
**Source URL:** not recorded in the registry for this key
**Domain:** E

### What it does
Proof-of-Uniqueness enforces a one-account-per-person invariant — at most one active registry entry per
real-world identity — for systems that require it (the paper names blockchain-based voting, universal
basic income disbursement, quadratic funding, and Proof-of-Social-Capital consensus as examples) without
revealing the person's identity to the registry or to public observers. The mechanism composes four
components. First, an issuer signs a verifiable credential (VC) certifying a canonical subject identifier
uid_I for the holder, under an issuance domain rho; the paper's Equation 1 states the two properties this
identifier must satisfy for person-level deduplication to hold — renewal invariance (the same real person
always receives the same uid_I, even after credential renewal) and subject injectivity (different real
people always receive different uid_I values). Second, the holder generates a first zero-knowledge proof,
pi_1 (an authorization proof, using the zk-SNARK proving system UltraPlonk), that some issuer-signed key
authorizes an oblivious pseudorandom function (OPRF) request without revealing which key or which issuer.
Third, a threshold committee of OPRF nodes (t of n nodes must cooperate; the paper's prototype uses a
2-of-3 committee) evaluates a verifiable OPRF over the holder's blinded identity secret H_id, producing
shares that the holder combines into a global nullifier nf — a value that is identical for the same person
across separate enrollment attempts but does not itself reveal the person's identity to the committee,
because the holder's blinding scalar beta randomizes what the committee sees. Fourth, the holder submits a
second zero-knowledge proof, pi_2 (an enrollment proof), together with the nullifier nf, to a public
smart-contract registry on an Ethereum Virtual Machine (EVM) blockchain; the registry rejects any
enrollment whose nullifier already exists, giving the deduplication guarantee, while the underlying
identity claims stay off-chain and unrevealed by either proof.

### Measured results
Client-side proving measured on an Intel Core i5-10400 CPU at 2.90 GHz (6 physical cores, 12 hardware
threads, 15 GiB RAM, Linux), Barretenberg limited to one software thread, Node.js 18.20.2, Noir 0.36.0,
Barretenberg wrapper 0.36.0, bb.js 0.58.0. Gas costs measured with Foundry Forge 0.2.0, solc 0.8.34, 200
optimizer runs, EVM Paris ruleset.

| Metric | Value | Conditions |
|---|---|---|
| Authorization proof (pi_1) witness generation | median 1.554 s | 3 runs |
| Authorization proof (pi_1) proving time | median 21.603 s | 3 runs |
| Enrollment proof (pi_2) witness generation | 3.348 s | single run — the paper states this single observation "does not support a variance estimate" |
| Enrollment proof (pi_2) proving time | 43.389 s | single run |
| Total client-side latency, both proof stages | ~65 s proving, ~70 s including witness generation | Benchmark synthesizes the OPRF transcript locally, explicitly excluding real committee and network latency |
| Compiled circuit size, authorization artifact | 59,221 Abstract Circuit Intermediate Representation (ACIR) opcodes, witness index 76,288 | Decoded Noir 0.36 opcode-vector length, not a backend gate count |
| Compiled circuit size, enrollment artifact | 120,980 ACIR opcodes, witness index 160,138 | Same caveat |
| Proof size | 2,144 bytes | Both pi_1 and pi_2 |
| Real enrollment gas cost, empty registry (N=0) | 614,701 gas, of which 376,631 gas is proof verification | Foundry gas profile |
| Mock enrollment gas, N=1 / N=100 / N=1,000 | 215,272 / 191,111 / 191,309 gas | First insertion is 12.64% higher (collection-state initialization); flat thereafter, supporting O(1) registry lookup — the paper explicitly notes a real proof "was not retested at every N," so this O(1) claim rests on mock (non-cryptographic) enrollments at scale |
| Verifier / registry contract deployment | 2,526,248 gas / 1,562,760 gas | One-time cost |
| Wallet revocation | 52,297 gas | — |
| Storage purge, scan-only cost | G_scan(N) = 24,810.8 + 9,251.1·N gas, R² > 0.999999 | Linear regression over measured purge runs |
| Storage purge, full removal cost | G_remove(N) = 21,470.7 + 27,550.5·N gas, R² > 0.999999 | Same regression family; this is total scan-plus-deletion cost, not deletion overhead alone |
| Generated on-chain verifier's cryptographic operation count | 39 elliptic-curve multiplications (ecMul), 39 elliptic-curve additions (ecAdd), 1 pairing check over 2 pairs | Priced by the paper at 6,000 gas per ecMul and 45,000 + 34,000 gas per pairing, per the applicable EIP gas schedule — fixed cost, independent of registry size N |

### Parameters
- Threshold OPRF committee size in the prototype: 2-of-3 (t=2, n=3), run locally by the researchers, not
  as a live distributed deployment — the paper states this explicitly as a gap from the target design.
- Credential shape in the prototype: a fixed 12-field profile in a 16-leaf Poseidon Merkle tree with a
  custom Baby Jubjub EdDSA signature — described by the paper as "a W3C-shaped demonstration credential,
  not one under a standardized Data Integrity cryptosuite."
- Cryptographic assumptions the security argument rests on (stated explicitly): knowledge soundness and
  zero knowledge of the deployed UltraPlonk proving system; binding KZG polynomial commitments; a
  correctly generated universal structured reference string; the Fiat-Shamir transform in the random
  oracle model; unforgeable Baby Jubjub EdDSA signatures; collision resistance of Poseidon and Poseidon2
  hash functions; correct elliptic-curve subgroup checks; correct implementation of all of the above.
- Threat-model collusion bound: fewer than t of the OPRF committee's n nodes collude (t=2 in the
  prototype's 2-of-3 configuration).

### Stated limitations
The paper reports its own gaps against its target design directly, rather than only in general terms — a
distinction from most survey-style limitation statements. Circuit pi_1 keeps the signing public key
private and proves only that some key signed the credential, so a self-signed credential passes the
authorization check and "the evaluated service has no effective rate control boundary." Mock issuance
draws a fresh random subject identifier each time, so re-issuing a credential to the same person changes
the nullifier and "breaks renewal invariance" — one of the two properties (Equation 1) the paper's own
formal deduplication guarantee depends on. The registry contract checks that the public OPRF key K is on
the curve but does not validate its prime-subgroup membership, which the paper states an upstream circuit
audit requires of any integrating verifier; replacing K also leaves earlier records still active. The
compiled discrete-log-equality (DLEQ) gadget interprets a Poseidon2 challenge modulo the group order
instead of the paper's own targeted HashToScalar value. The wallet field is truncated to 160 bits, and
each registry owner holds unilateral administrative authority with no timelock. No recovery circuit,
contract transition, or test exists for lost-key recovery. The paper's own nine-requirement coverage table
(Table 2) states, per requirement: deduplication is "record only" (reissuance untested); holder binding is
met; recovery is "design only," with no circuit; durable revocation is "No" — no generation counter or
tombstone mechanism stops replay of an archived (revoked or superseded) enrollment or revocation
authorization; credential lifecycle checking is partial (only validUntil is checked, not start time or
issuer-status); client equipment requirement is met on desktop, untested on mobile; confidentiality is
partial (private claims are hidden, but metadata and query-probing remain, an exposure the paper does not
close); decentralization is partial (node code exists, but no live multi-node committee run was measured);
governance is partial (any single registry owner can change policy or the OPRF key K without a timelock).
An adversary holding two credentials with distinct canonical identifiers for one real person derives two
distinct nullifiers, and the paper states plainly that "no check in the protocol rejects the second
record, because the registry observes nullifiers alone" — cross-credential Sybil resistance depends
entirely on the issuer-side uniqueness invariant (Equation 1) holding, which the protocol itself cannot
enforce cryptographically. The issuer itself sits inside the paper's own stated privacy boundary: an
issuer that knows a subject's (blinding value rho, canonical identifier uid_I) pair can issue a shadow
credential, evaluate it itself, and search the registry for that person's nullifier — the paper states
privacy from the issuer specifically requires the issuer not do this, an assumption on issuer behavior
the protocol does not enforce.

### Requirements it places on the rest of the system
The mechanism requires an issuer that already assigns a stable, injective, renewal-invariant canonical
subject identifier per real person (Equation 1) — the protocol's own cryptography deduplicates on top of
this identifier but does not itself verify or guarantee that the issuer's identity-proofing process
produces one. It requires threshold OPRF committee nodes running on genuinely independent infrastructure
for the collusion-bound assumption (fewer than t of n colluding) to hold in practice — the paper's own
measurements use a single local process simulating the committee, not independently operated nodes, so
none of the reported latency figures include real inter-node network cost. It requires the public
blockchain hosting the registry contract to give every observer a consistent, ordered view of enrollment
transactions, since deduplication is enforced by rejecting a nullifier already present in that shared
contract state. It requires paginated, bounded-size storage-purge operations for any deployment expecting
registry size N to grow large, since the paper's own measured purge cost grows linearly in N (both the
scan-only and full-removal slopes above) with no batching mechanism evaluated.

### Contradicts
None found against other corpus entries on a measured fact.

### References worth retrieving
- **Foundational/competing** — cited as reference [40] in this paper: World ID 4.0's own specification.
  (The paper's own architectural comparison, Table 3, states World ID 4.0 shares this paper's two-proof-
  stage-plus-authenticated-threshold-vOPRF structure but scopes its uniqueness tag to one relying party per
  proof, removing any single shared global uniqueness record — the design choice this paper's own
  "global registry" scope is contrasted against.)
- **Competing** — cited as reference [35] in this paper: Self, a government-ePassport-chip-rooted
  on-chain-attestation system requiring Near Field Communication (NFC) and a Trusted Execution Environment
  (TEE).
- **Competing** — cited as reference [28] in this paper: CanDID, which imports attributes from unmodified
  web identity providers through oracles and runs a Multi-Party Computation (MPC) committee over a
  secret-shared deduplication-attribute table.
- **Foundational** — cited as reference [10] in this paper: SyRA, which turns a legacy low-entropy
  identifier into a high-pseudoentropy key via a distributed issuer's verifiable random function evaluation,
  producing one unlinkable pseudonym per context with no per-user issuer state.
- **Foundational** — cited as reference [36] in this paper: Semaphore, a Merkle-tree group-membership
  nullifier construction allowing one signal per scope per member, explicitly noted by this paper as
  carrying "no personhood root, because group admission sits outside the protocol."
- **Foundational** — cited as reference [6] in this paper: BrightID, whose uniqueness derives from a
  social graph of video-verified meetings, giving a probabilistic (not cryptographic) guarantee and
  exposing social-contact edges — noted by this paper as a contrasting non-cryptographic approach to the
  same Sybil-resistance goal.
- **Foundational** — cited as reference [22] in this paper: the TACEO threshold-nullifier protocol
  specification this paper's own OPRF committee implementation is built on (verifiable threshold OPRF over
  Baby Jubjub with Poseidon2, blinded evaluation, per-node DLEQ proofs).

### Verbatim extracts
- "identical issuer-canonical inputs under a stable master key yield a single wallet-bound nullifier, while
  credential claims stay off-chain."
- "the evaluated service has no effective rate control boundary."
- "no check in the protocol rejects the second record, because the registry observes nullifiers alone."
- "privacy from an issuer requires that it issues no shadow credential and runs no surveillance
  evaluation."
- "the benchmark synthesizes the OPRF transcript locally, so it excludes committee and network latency."
