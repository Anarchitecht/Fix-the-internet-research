## [AMBATI-SACMAT-26] SoK: Self-Sovereign Digital Identities

**Citation:** Sushanth Ambati, Kainat Adeel, Jack Myers, Nikolay Ivanov. "SoK: Self-Sovereign Digital Identities." ACM Symposium on Access Control Models and Technologies (SACMAT), 2026. DOI: 10.1145/3750555.3811903.
**Retrieved:** full text via https://arxiv.org/pdf/2603.06896 (arXiv:2603.06896v2 [cs.CR], 11 Mar 2026)
**Source URL:** https://arxiv.org/pdf/2603.06896
**Domain:** E

### What it does
This is a systematization of knowledge (a structured survey that classifies existing work rather than proposing a new mechanism) on self-sovereign digital identity (SSDI), a paradigm in which a user, rather than a service provider or a federated identity broker (such as Google or Facebook), holds their own authentication keys and data and presents them on demand as digital credentials. The paper follows a five-step method: it reviews eight prior surveys published 2018-2023 to establish what has already been systematized; it draws on 80 sources (active SSDI projects, peer-reviewed papers, standards-body reports, and privacy-advocacy manifestos) to distill six recurring adoption challenges; it structurally classifies 47 scientific publications proposing SSDI systems along five dimensions (system type, trust infrastructure, cryptographic technique, which of the six challenges each addresses, evaluation method); it evaluates 12 production-deployed SSDI systems along five self-sovereignty dimensions; and it synthesizes five forward-looking research frontiers from the first four steps.

The six challenges it identifies: (1) identity binding — establishing that one decentralized identifier (DID, a self-generated identifier not issued by any central authority) corresponds to one real-world individual or organization, addressed in the literature by credential-based binding (a trusted issuer such as a government or university attests to the correspondence), web-of-trust binding (peers vouch for one another across a social graph), or biometric binding (tying identity to a physical characteristic); (2) key management and protocol immaturity — users must generate, store, back up, rotate, and recover their own cryptographic keys with no central password-reset mechanism, and over 100 registered DID methods remain largely non-interoperable; (3) usability — the shift from username-and-password to key-based authentication and selective disclosure (revealing only specific attributes of a credential) imposes cognitive load unfamiliar to typical users; (4) oversight and regulation — legal frameworks such as GDPR's right to be forgotten assume a centralized party capable of deleting data, in tension with immutable ledger anchoring, and no single party exists for law enforcement to serve a subpoena on; (5) critical-mass adoption — a cold-start problem in which users will not adopt SSDI credentials until verifiers accept them, and verifiers will not integrate verification until enough users hold credentials; (6) single infrastructure dependence — the great majority of proposed systems anchor identity to one specific blockchain, so a consensus failure, a 51% attack, or a smart-contract vulnerability in that one chain endangers every identity anchored to it, a risk the paper calls meta-centralization because it exists at the ecosystem level even when the chosen chain is itself internally decentralized.

### Measured results

| Quantity | Value | Conditions |
|---|---|---|
| Proportion of 47 classified scientific publications using blockchain as trust infrastructure | 39 of 47 (83%) | Structured literature review, inclusion criteria: concrete technical contribution (architecture, protocol, or system) explicitly targeting self-sovereign or fully decentralized identity; Ethereum, Hyperledger Indy, and Hyperledger Fabric the most common platforms cited |
| Proportion using purely peer-to-peer architecture with no blockchain dependency | 4 of 47 (9%) | Same 47-paper corpus |
| Proportion using hybrid or ledger-agnostic architecture | 4 of 47 (8%) | Same 47-paper corpus |
| Proportion of 47 papers using standard public-key cryptography only | 72.3% (calculated from paper's Fig. 4 percentage) | Same 47-paper corpus; RSA, ECDSA, EdDSA for DID authentication |
| Proportion using zero-knowledge proofs | 8 papers (17%) | Same 47-paper corpus, for selective disclosure or privacy-preserving authentication |
| Proportion using homomorphic encryption | 3 papers (6%) | Same 47-paper corpus, for privacy-preserving computation on identity attributes |
| Proportion using CL-signatures (Camenisch-Lysyanskaya, unlinkable credential presentation) | 2 papers (4%) | Same 47-paper corpus |
| Coverage of Challenge 2 (protocols and key management) | 38 of 47 papers (~81%) | Same 47-paper corpus |
| Coverage of Challenge 1 (identity binding) | 21 of 47 papers (45%) | Same 47-paper corpus |
| Coverage of Challenge 4 (oversight and regulation) | 11 of 47 papers (23%) | Same 47-paper corpus |
| Coverage of Challenge 5 (critical-mass adoption) | 10 of 47 papers (21%) | Same 47-paper corpus |
| Coverage of Challenge 3 (usability) | 7 of 47 papers (15%) | Same 47-paper corpus |
| Coverage of Challenge 6 (single infrastructure dependence) | 7 of 47 papers (15%) | Same 47-paper corpus |
| Papers with formal security proofs | 7 of 47 (15%) | Same 47-paper corpus |
| Papers with user studies or usability evaluations | 2 of 47 (4%) | Same 47-paper corpus |
| Papers relying on implementation benchmarks (throughput, latency, gas cost) as sole evaluation | 23 of 47 (49%) | Same 47-paper corpus |
| Papers with only informal security argument, no empirical evaluation | 15 of 47 (32%) | Same 47-paper corpus |
| Real-world SSDI deployments achieving full support on all five self-sovereignty dimensions (user key control, permissionless issuance, credential portability, selective disclosure, revocation resistance) | 0 of 12 | Assessment of 12 production-deployed or advanced-pilot SSDI systems (Sovrin, EU Digital Identity Wallet, British Columbia VON, DIF ION, SpruceID, uPort Veramo, Jolocom, Trinsic, Truvera/Dock, KILT, Ping Identity/ShoCard, IDunion), five dimensions scored fully/partially/not supported per system |
| Real-world SSDI projects fully operational as of February 2026 | 3 of 12 (25%) | Same 12-project cohort, status assessed from code repositories and/or public websites |
| Real-world SSDI projects defunct | 3 of 12 (25%) | Same 12-project cohort |
| Real-world SSDI projects inactive | 2 of 12 (17%) | Same 12-project cohort |
| Real-world SSDI projects under active development or partial deployment | 4 of 12 (33%) | Same 12-project cohort |
| World population lacking any officially recognized identity | over 1 billion | Cited from World Economic Forum figures, not independently measured by this paper |

### Parameters
Not applicable — this is a literature systematization with no runnable mechanism or tunable parameter of its own. The classification scheme applied to the 47-paper corpus used five fixed dimensions (type, trust infrastructure, cryptographic technique, which of 6 challenges addressed, evaluation method) and the 12-deployment assessment used five fixed self-sovereignty dimensions (key control, permissionless issuance, portability, selective disclosure, revocation resistance), each scored fully / partially / not supported.

### Stated limitations
The paper states that the scientific literature it surveyed treats usability "as an afterthought or ignore[s] it entirely," with only 2 of 47 papers reporting any user study, and calls this "a critical gap" because "systems that are not evaluated with real users risk optimizing for the wrong objectives." Key recovery is stated as "arguably the most critical unsolved problem": social-recovery schemes (a quorum of trusted contacts restoring access) introduce their own trust assumptions and coordination overhead, and hardware-backed key storage (secure enclaves, hardware security modules) protects keys at rest but does not solve backup if the device is lost or destroyed. Sybil resistance (preventing one actor from registering multiple identities) has no solution accepted as satisfactory among the three surveyed approaches: credential-based binding reintroduces dependence on a centralized issuing authority, web-of-trust binding is vulnerable to collusion and has bootstrapping problems in sparse networks, and biometric binding is irreversible once compromised and raises privacy concerns. The paper's own real-world evaluation found every one of the 12 deployed systems makes at least one compromise against full self-sovereignty, government-backed systems in particular sacrificing permissionlessness and revocation resistance by design because governments require the ability to revoke a credential. GDPR's right-to-be-forgotten conflicts with immutable ledger anchoring, and the paper states the legal sufficiency of the common workaround (storing only hashes on-chain, personal data off-chain) "remains contested." The paper explicitly frames its five-dimension deployment assessment as "a first step" toward a sovereignty-assurance framework, not a completed one, and identifies formalizing such a framework as future work.

### Requirements it places on the rest of the system
A credential-based identity-binding approach requires an external, already-trusted issuing authority (a government, university, or employer) willing to attest off-protocol that a given DID corresponds to a specific real-world entity; the protocol itself supplies no mechanism to establish that correspondence. A web-of-trust binding approach requires an existing social graph dense enough to avoid the bootstrapping failure the paper states occurs in sparse networks, and requires that colluding participants be detectable or economically discouraged elsewhere in the system, since the mechanism itself does not resist collusion. Key recovery via social recovery requires a quorum of contacts the user selects in advance to remain reachable and honest at the moment of recovery; hardware-backed key storage requires a physically available replacement device or backup channel, since the paper states it does not itself solve loss-of-device backup. Any mechanism anchoring identity to a single blockchain inherits that chain's consensus-failure and governance-crisis risk for every identity anchored to it, so avoiding this single-infrastructure dependence requires either a ledger-agnostic design or migration tooling across ledgers, for which the paper states "the current landscape falls far short" of existing cross-ledger interoperability standards. A design using zero-knowledge proofs for selective disclosure requires wallet software and verifier software to agree on a standardized proof format across DID methods, which the paper states does not yet exist.

### Contradicts
None found.

### References worth retrieving
- **Foundational:** Mühle, Grüner, Gayvoronskaya, Meinel. Survey identifying essential SSI components (DIDs, verifiable credentials, distributed ledgers) — one of the earliest SSI surveys, cited as an architectural-overview baseline this SoK extends with challenge- and deployment-level analysis.
- **Foundational:** Der, Jähnichen, Sürmeli. Early position paper on SSI opportunities and challenges, cited as anticipating several of this SoK's six challenges without a systematic survey methodology.
- **Competing:** Stokkink, Ishmaev, Epema, Pouwelse. "TrustChain"-style peer-to-peer SSDI system (paper [132] in this SoK's numbering) — one of only 4 of 47 surveyed systems avoiding blockchain dependency entirely; explicitly argued by its authors that a "truly self-sovereign" system should not depend on any single ledger, cited by this SoK as not having achieved significant adoption.
- **Competing:** Zaeem, Khalil, Lamison, Pandey, Barber. "On the usability of self sovereign identity solutions," University of Texas at Austin Center for Identity Technical Report 21-02, 2021 — one of the only empirical usability studies of SSDI found in the 47-paper corpus; source of the finding that users found onboarding confusing and expressed anxiety about losing private keys.
- **Attack-or-critique:** Giannopoulou — critical sociopolitical analysis questioning whether SSI decentralization empowers users or merely relocates power to different intermediaries, cited by this SoK as a sociopolitical-perspective survey it builds on.
- **Superseded-by:** none identified — this is itself the most recent (2026) SoK in the domain.

### Verbatim extracts
- "no deployed system achieves full self-sovereignty across all five dimensions."
- "Key recovery is arguably the most critical unsolved problem."
- "the vast majority of SSDI proposals rely on a single blockchain or distributed ledger as their trust anchor."
- "only 3 of the 12 surveyed projects (25%) were fully operational."
- "adopting the SSDI label without delivering its core properties" (describing "sovereignty washing").
- "usability is a precondition for adoption, not a secondary concern."
