## [BEURDOUCHE-RFC-25] The Messaging Layer Security (MLS) Architecture

**Citation:** Benjamin Beurdouche, Eric Rescorla, Emad Omara, Srinivas Inguva, Alan Duric. "The Messaging Layer Security (MLS) Architecture." IETF RFC 9750, 2025. DOI 10.17487/RFC9750.
**Retrieved:** full text via https://www.rfc-editor.org/rfc/rfc9750.html
**Source URL:** https://www.rfc-editor.org/rfc/rfc9750.html
**Domain:** H

### What it does
The document specifies the deployment architecture that surrounds the MLS protocol (RFC 9420, BARNES-RFC-23): the two external services the protocol depends on, the guidance for choosing among the protocol's configurable behaviors, and the operational parameters two independent deployments must agree on to interoperate. It states explicitly that its recommendations are not mandatory for protocol-level interoperability, but that following or ignoring them changes the security guarantees actually achieved.

The document assigns MLS two external roles. An Authentication Service (AS) issues, validates, and optionally revokes credentials binding an identity to a client's signature key; the AS may be a single service provider, a federated system, or a peer-to-peer mechanism such as gossiping or trust-on-first-use, and the document states MLS depends on correct AS behavior for endpoint authentication and hence for the confidentiality of the group key. A Delivery Service (DS) stores each client's initial keying material (a KeyPackage — a signed bundle carrying an AS-issued credential, an encryption public key, and supported-capability information) and routes MLS messages between clients; the document states MLS's core cryptographic guarantees do not depend on correct DS behavior — even a fully compromised DS cannot read messages, inject acceptable messages, or add itself to the group — but a compromised DS can still degrade availability and metadata privacy.

Because an MLS group has one linear sequence of epochs, all members must agree on exactly one Commit message as the one that ends each epoch. The document frames the two ways a Delivery Service can supply that agreement using the CAP theorem (Brewer, PODC 2000, cited as [CAPBR]): a Strongly Consistent DS gives every client the same view of message order, trusted to break ties when two members submit a Commit for the same epoch simultaneously, at the cost of clients needing to handle a rejected Commit; an Eventually Consistent DS — including a distributed peer-to-peer message-broadcast mechanism, given as an explicit example — stays available under network partition but may deliver messages to different clients in different orders, pushing reconciliation onto the clients themselves through a deterministic tie-breaking policy applied once multiple Commits for the same epoch are observed.

### Measured results
None. This is an architecture and deployment-guidance document; it states no experiment, benchmark, or measured figure.

### Parameters
Not applicable in the numeric sense — the document lists which operational parameters an MLS deployment must fix and agree on with any deployment it interoperates with, without recommending values:
- the maximum acceptable total lifetime of a KeyPackage
- how long to retain a resumption pre-shared key (PSK) for a past epoch
- the degree of tolerance for out-of-order message delivery
- how long to retain unused nonce/key pairs for a sender, and the maximum count of such pairs to retain
- the maximum number of steps a client will advance a secret-tree ratchet in response to one message before rejecting it

### Stated limitations
The document states it does not itself specify all mechanisms required for federation between independent MLS deployments, deferring the mechanism to a separate federation document. It states the Authentication Service's internal design is left entirely to infrastructure designers — the architecture defines only the interface (issue, validate, revoke credentials), not an implementation. It states a malicious DS can mount total or partial denial-of-service by refusing to forward some or all messages, and that clients generally cannot detect this without an out-of-band channel; it states this class of failure "must be dealt with as a customer service matter, not via technology." It states a malicious DS can cause an undetected partition of the group by selectively partitioning key-exchange messages, detectable only by out-of-band comparison of each client's epoch_authenticator value, and that the per-sender "generation" counter that prevents message tampering does not by itself prevent this partitioning. It states MLS provides no built-in mechanism preventing a service provider or push-notification provider from learning which devices receive a given message, even though message content stays encrypted. It states desynchronization between a Delivery Service's internal epoch-tracking state and clients' actual state can leave a group permanently unable to have any Commit accepted, and that recovery mechanisms such as automatic external rejoin carry their own security and denial-of-service risk, because the client must then trust the DS-supplied GroupInfo to reflect the true current group state rather than an earlier, possibly compromised state.

### Requirements it places on the rest of the system
The document requires an Authentication Service the deploying application trusts for identity-to-key binding, whatever its internal structure; MLS's confidentiality guarantee for the group key is conditioned on correct AS behavior, not on correct DS behavior. It requires a Delivery Service that can store and serve one-time-use KeyPackages, route messages to specific clients or to a whole group, and (except where the deployment tolerates unbounded reordering) supply enough ordering information that all members converge on one Commit per epoch — either by the DS itself enforcing a single order (Strongly Consistent) or by clients running a deterministic tie-breaking policy over multiple observed Commits (Eventually Consistent). It requires that any recovery path from a desynchronized or forked group state be paired with tie-breaking logic for Welcome messages, so a newly joining member processes only the Welcome tied to the Commit that ultimately succeeded. It requires that copies of previous or forked group states be deleted within a bounded time after a tie-break resolves, stated as necessary to preserve forward secrecy. For two independently operated deployments to interoperate at all, it requires them to agree on the AS credential types, cipher suites, and the operational parameters listed above (KeyPackage lifetime, PSK retention window, out-of-order tolerance, and the rest).

### Contradicts
None found. This entry supplies the deployment-role context (AS, DS, the CAP-theorem framing of DS consistency choices) that BARNES-RFC-23's Section 14 sequencing requirement and Section 16.9/16.10 security considerations assume without spelling out; nothing in this document's claims conflicts with BARNES-RFC-23. The bibliography's citation of Bhargavan, Barnes, Rescorla, "TreeKEM: Asynchronous Decentralized Key Management for Large Dynamic Groups," HAL ID hal-02425247, 2018, confirms the exact document and HAL identifier already targeted in this corpus as BHARGAVAN-HAL-18.

### References worth retrieving
- Alwen, Coretti, Dodis, Tselekounis, "Modular Design of Secure Group Messaging Protocols and the Security of MLS," ePrint 2021/1083 — foundational (already surfaced via BARTUSEK-EPRINT-26's bibliography as ACDT21)
- Alwen, Coretti, Jost, Mularczyk, "Continuous Group Key Agreement with Active Security," ePrint 2020/752 — foundational (active-adversary CGKA security, the extension BARTUSEK-EPRINT-26 states is left to future work for its own construction)
- Alwen, Hartmann, Kiltz, Mularczyk, "Server-Aided Continuous Group Key Agreement," ePrint 2021/1456 — competing (a server-assisted CGKA design, an alternative point in the centralization-of-DS design space this architecture document surveys)
- Alwen, Jost, Mularczyk, "On the Insider Security of MLS," ePrint 2020/1327 — foundational (insider/active-adversary analysis of the TreeKEM paradigm)
- Bhargavan, Beurdouche, Naldurg, "Formal Models and Verified Protocols for Group Messaging: Attacks and Proofs for IETF MLS," HAL ID hal-02425229, 2019 — foundational (formal verification of the protocol this architecture document sits above)
- Bhargavan, Barnes, Rescorla, "TreeKEM: Asynchronous Decentralized Key Management for Large Dynamic Groups," HAL ID hal-02425247, 2018 — foundational (already a corpus target: BHARGAVAN-HAL-18)
- Brzuska, Cornelissen, Kohbrok, "Security Analysis of the MLS Key Distribution," ePrint 2021/137 — foundational (security proof for the DS-mediated KeyPackage/key-distribution mechanism this document describes)
- Brewer, "Towards Robust Distributed Systems," PODC 2000, DOI 10.1145/343477.343502 — foundational (the CAP theorem this document applies to classify Delivery Service designs)
- Cremers, Günsay, Wesselkamp, Zhao, "ETK: External-Operations TreeKEM and the Security of MLS in RFC 9420," ePrint 2025/229 — foundational (security analysis of the standardized RFC 9420 TreeKEM variant)
- Cremers, Hale, Kohbrok, "The Complexities of Healing in Secure Group Messaging: Why Cross-Group Effects Matter," USENIX Security 2021 — attack (cross-group healing/post-compromise-security attacks against tree-based group messaging)

### Verbatim extracts
- "MLS depends on correct behavior by the AS ... these properties do not depend on correct behavior by the DS"
- "even a malicious DS cannot add itself to groups or recover the group key"
- "the members of the group must agree on the order in which changes are applied"
- "Per the CAP theorem, there are two general classes of distributed systems that the DS might fall into"
- "the DS is trusted to break ties when two members send a Commit message at the same time"
- "failure of the DS to provide reasonable service must be dealt with as a customer service matter, not via technology"
- "the AS may not be a centralized system and could be realized by ... gossiping, or using trust on first use"
