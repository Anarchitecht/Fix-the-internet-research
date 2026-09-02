## [LI-HCC-24] MISMATCH — NOT THE PAPER
**Citation (expected):** Chuanlei Li, Minghui Xu, Jiahao Zhang, Hechuan Guo, Xiuzhen Cheng. "SoK: Decentralized Storage Network." High-Confidence Computing, 2024. DOI 10.1016/j.hcc.2024.100239.
**Retrieved:** MISMATCH — file on disk is a different paper, not usable as evidence for LI-HCC-24
**Source URL:** (unresolved — the fetched text does not correspond to the candidate URLs in the target registry)
**Domain:** C

### Mismatch record
The file at `sources/text/LI-HCC-24.txt` is not "SoK: Decentralized Storage Network." Its first 3,000 characters give the title "Compact Key Storage in the Standard Model," authors Yevgeniy Dodis and Daniel Jost (New York University), an abstract about Compact Key Storage (CKS) as a backup primitive for end-to-end secure applications, and a table of contents covering trapdoor key-derivation functions (TKDFs) and CKS protocol constructions. This is a cryptographic key-management paper, unrelated in subject to a systematization-of-knowledge survey of decentralized storage networks. The tail of the file (game-based integrity-notion definitions for CKS, oracle pseudocode for CreateUser/Append/Erase/Grant/Accept/Retrieve) confirms the same identity throughout; there is no point in the file where the expected title, authors, or subject matter (proof of replication, proof of spacetime, proof of storage, redundancy schemes, incentive designs across deployed decentralized storage networks) appears.

Per the batch rules, nothing is extracted from this file under the key LI-HCC-24. No mechanism, parameter, measured result, or limitation is recorded. This mismatch is reported to the orchestrating process so LI-HCC-24 can be re-retrieved from one of its registry candidate URLs (https://doi.org/10.1016/j.hcc.2024.100239 or https://eprint.iacr.org/2024/) or another source for "SoK: Decentralized Storage Network."

### What the mismatched file actually is (for registry bookkeeping only — not evidence for LI-HCC-24)
Dodis, Jost, "Compact Key Storage in the Standard Model" (a 2024/2025-era paper building on Dodis, Jost, Marcedone's CRYPTO 2024 Compact Key Storage work). It shows CKS's original random-oracle-model construction cannot be replicated in the standard model for the full class of "CKS-compatible games," proposes a weaker standard-model CKS definition recovering a derived key instead of the original secret, and instantiates it from one-way functions (passive security) or collision-resistant hashes plus dual-PRFs (stronger notions). This paper is outside domain C (storage) as understood in this brief and is not classified or mined further here; if it is independently a useful source for domain E (identity, keys, key recovery) it should be logged and assigned its own key by whichever agent owns that domain, not folded into this entry.

### Verbatim extracts (confirming the mismatch only)
- "Compact Key Storage in the Standard Model"
- "Yevgeniy Dodis... and Daniel Jost, New York University"
- "we first show that this reliance is inherent" (referring to the random oracle model)
