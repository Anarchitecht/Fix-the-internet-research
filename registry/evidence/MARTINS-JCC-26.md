## [MARTINS-JCC-26] Matrix Protocol: A Comprehensive Systematic Mapping Study
**Citation:** José A. P. Martins, Paulo A. L. Rego, José A. F. de Macêdo, Francisco Airton Silva, Vinícius Lagrota. "Matrix protocol: a comprehensive systematic mapping study." Journal of Cloud Computing, 2026. DOI: 10.1186/s13677-025-00829-7.
**Retrieved:** full text via https://link.springer.com/article/10.1186/s13677-025-00829-7
**Source URL:** https://link.springer.com/article/10.1186/s13677-025-00829-7
**Domain:** J

### What it does
This paper classifies the published research literature on the Matrix protocol (a federated, decentralized real-time-communication protocol) rather than measuring the protocol itself. It follows the systematic-mapping-study method of Petersen, Vakkalanka, and Kuzniarz (2015): define research questions, construct a search string, screen candidate papers against stated inclusion/exclusion criteria, classify the surviving papers by keyword, and report frequency counts per category. The authors searched digital libraries with 15 unified search-string expressions, screened 156 candidate papers, and retained 21 as primary studies. Each primary study was classified along four research questions: RQ01 whether the paper uses Matrix in practice or only mentions it, RQ02 the paper's main research area, RQ03 the paper's main contribution type, and RQ04 which Matrix feature the paper explores.

### Measured results
The paper's own measured output is a classification count over its 21-paper corpus, not a protocol-performance benchmark. No throughput, latency, or scalability figures for the Matrix protocol itself are reported as the mapping study's own measurements; such figures belong to the individual primary studies it cites (each would need retrieval and full-text verification separately before use as evidence).

| Research question | Result | Corpus |
|---|---|---|
| RQ01 — uses Matrix in practice vs. only mentions it | 13 of 21 papers implement or formally analyze Matrix in practice; 8 of 21 only mention/reference it | 21 primary studies, drawn from 156 screened candidates |
| RQ02 — main research area | Security and Privacy is the largest category; Networks and Communications second; Human-Computer Interaction has 2 papers; Forensic Analysis, Natural Language Processing, and Educational Technology each have 1 paper (a paper may count in more than one category) | Same 21-paper corpus |
| RQ03 — main contribution type | Four categories reported: Matrix Protocol Analysis, Security and Privacy Approaches, Protocol Development, Tool Development (Tool Development named as exactly 4 papers in the text; other category counts given only as figure references, not stated inline) | Same 21-paper corpus |
| RQ04 — Matrix feature explored | Three categories: Group Communication (most frequent), Security Issues, Matrix Architecture | Same 21-paper corpus |

### Parameters
Not applicable in the sense of a system parameter — this is a literature-classification methodology, not a mechanism with tunable inputs. The methodological "parameters" are the search and screening choices: 15 unified search-string expressions (Table 14 in the source), inclusion/exclusion criteria (Table 12), and the four research questions (Table 10), each defined and applied uniformly across the 156 screened papers.

### Stated limitations
The authors state the study is restricted to 21 primary studies drawn from academic literature; papers not indexed by the searched digital libraries or not matching the search strings would not appear. The conclusion states several unresolved technical gaps found across the surveyed literature (not gaps in the mapping study's own method): limited formal-verification coverage of Matrix's access-control and security models, unresolved scalability limits in event synchronization and message propagation at large scale, unresolved cross-platform interoperability between Matrix and non-Matrix systems, unquantified cryptographic overhead from end-to-end encryption (E2EE), and no unified security model across independently operated federated homeservers. The paper does not itself measure any of these; it reports that the surveyed primary studies raise them as open issues.

### Requirements it places on the rest of the system
This entry is a literature survey and places no mechanical requirement on a system design. Its value to the architecture synthesis is as a bibliography index over Matrix-specific primary studies (listed below) and as a map of which technical questions about federated real-time messaging remain open in the published literature as of this survey's search date, each of which would need its own full-text entry before any measured figure from it is used.

### Contradicts
None found. This paper reports no protocol-performance figures for Matrix that could disagree with another entry in this corpus.

### References worth retrieving
- foundational: Weidner M, Kleppmann M, Hugenroth D, Beresford AR, "Key Agreement for decentralized secure group messaging with strong security guarantees," ACM CCS 2021 — the DCGKA (Decentralized Continuous Group Key Agreement) construction that BeeKEM (already in this corpus, ePrint 2026/1434) supersedes; cited here as foundational to Matrix's own group-messaging security discussion.
- attack: Albrecht MR, Celi S, Dowling B, Jones D, "Practically-exploitable cryptographic vulnerabilities in Matrix," IEEE Symposium on Security and Privacy (S&P), 2023 — demonstrated practical attacks on Matrix's key-management and authentication workflows.
- attack: Albrecht MR, Dowling B, Jones D, "Device-oriented group messaging: a formal cryptographic analysis of Matrix core," IEEE S&P, 2024 — formal security model for Matrix's core group-messaging cryptography, follow-up to the 2023 attack paper.
- attack: Wichelmann J, Berndt S, Pott C, Eisenbarth T, "Help, my Signal has bad Device! Breaking the Signal Messenger's Post-Compromise Security Through a Malicious device," DIMVA 2021 — device-compromise attack analysis Matrix's own post-compromise security is compared against.
- competing: Jacob F, Grashöfer J, Hartenstein H, "A glimpse of the Matrix: scalability issues of a new message-oriented data synchronization middleware," ACM Middleware 2019 Demos and Posters — direct measurement of Matrix server-to-server scalability and centralization.
- competing: Jacob F, Beer C, Henze N, Hartenstein H, "Analysis of the Matrix event Graph Replicated data type," IEEE Access 9, 2021 — formal analysis of Matrix's event graph as a CRDT (Conflict-free Replicated Data Type), directly relevant to this corpus's domain D (replicated state).
- competing: Jacob F, Becker L, Grashöfer J, Hartenstein H, "Matrix decomposition: analysis of an access control approach on transaction-based DAGs without finality," ACM SACMAT 2020 — access-control analysis of Matrix's non-finalizing event DAG (directed acyclic graph).
- competing: Chowdhury PD, Sameen M, Blessing J, Boucher N, Gardiner J, Burrows T, Anderson R, Rashid A, "Threat models over space and time: a case study of E2EE messaging applications," arXiv:2301.05653, 2023 — threat-model comparison across six end-to-end-encrypted desktop messaging clients using STRIDE and LINDDUN frameworks, including Matrix.
- competing: Rahman M, Wang Y, De D, "Implementation of dew-inspired matrix-mesh communication protocol," in Dew Computing: the sustainable IoT perspectives, Springer Nature Singapore, 2024 — hybrid cloud-dew/client-server/peer-to-peer (P2P) messaging protocol built on Matrix, evaluated for operation under limited connectivity.
- irrelevant: Schipper GC, Seelt R, Le-Khac NA, "Forensic analysis of Matrix protocol and Riot.Im application," Forensic Science International: Digital Investigation 36, 2021 — digital-forensics extraction study, outside this corpus's architecture-selection scope.

### Verbatim extracts
- "a broad review of primary studies in a specific topic area that aims to identify what evidence is available"
- "identification and categorization of 156 papers, leading to the selection of 21 primary studies"
- "Thirteen papers have used the Matrix protocol in practice"
- "Eight papers were assigned the Only Mentions category"
- "no unified security model across federated servers is an ongoing concern"
- "formal verification methods for access control and security models need to be developed"
