## [ADLER-ARXIV-24] Personhood Credentials: Artificial Intelligence and the Value of Privacy-Preserving Tools to Distinguish Who Is Real Online
**Citation:** Steven Adler, Zoë Hitzig, Shrey Jain, and 28 additional co-authors spanning OpenAI, Microsoft, MIT, and multiple civil-society and standards organizations. "Personhood Credentials: Artificial Intelligence and the Value of Privacy-Preserving Tools to Distinguish Who Is Real Online." arXiv preprint (CoRR), 2024. DOI 10.48550/ARXIV.2408.07892.
**Retrieved:** full text via https://arxiv.org/pdf/2408.07892
**Source URL:** https://arxiv.org/abs/2408.07892
**Domain:** E

### What it does
A personhood credential (PHC) lets a person prove to an online service, without disclosing any personal information, that a trusted issuer believes them to be a real human who has not already received a credential from that same issuer. The mechanism has two stages. During enrollment, a person presents evidence to an issuer (a government, nonprofit, consortium, or private company); the issuer runs validity checks — is this a real person, and has this person already received a credential — and, if the checks pass, issues one credential. During usage, the credential holder proves to a service provider, through a zero-knowledge proof (a cryptographic protocol in which a prover convinces a verifier that a statement is true without revealing anything beyond the statement's truth), that they hold a valid credential from that issuer, without revealing which specific credential they hold. The holder can additionally prove, again without revealing which credential, that the credential has not already been used with this particular service, or has been used fewer times than the service's stated limit.

The paper defines two requirements a system must meet to count as a PHC system. First, credential limits: the issuer gives at most one credential per person, checked at enrollment through one of three methods — matching against existing identity documents (for example, requiring a passport or birth certificate that is itself finite per person), matching biometric measurements (palm, iris, or fingerprint) against prior enrollees, or Web-of-Trust vouching (an unenrolled person is authenticated by receiving sufficient vouches from already-enrolled people, with the graph itself seeded from one of the other two methods or from in-person "pseudonym parties"). Loss or theft of a credential is mitigated through periodic re-authentication or a bounded credential expiry, since re-authentication that preserves privacy is difficult to build. Second, unlinkable pseudonymity: the issuer stores the minimum identifying information needed to enforce the one-per-person limit and to support recovery or revocation, a credential-usage proof discloses nothing beyond "this holder has a valid credential," and, by default, neither the issuer nor colluding service providers can link a given usage event back to a specific enrollee or link usage of the same credential across different service providers.

For minimal disclosure and unlinkability during usage, the paper describes a public-key scheme: an issuer maintains a list of public keys, one per valid credential, with each corresponding private key held only by the enrollee; a service-specific pseudonym is constructed with a cryptographic nullifier, a value computed from the credential and the service's identity, so a service can detect repeated use of the same credential within its own context (enabling per-credential rate limits) without being able to derive the credential itself or correlate the nullifier with any other service's records.

The paper argues, as a design conclusion rather than a proof, that a credential-limit ecosystem functions best when each person can hold a bounded number of credentials greater than one (via multiple issuers, each independently enforcing one credential per person) rather than either extreme: unlimited credentials per person (which fails to bound the scale of any individual's ability to act as many actors) or exactly one credential from a single issuer (which concentrates all users' minimal-necessary information with one institution and removes redundancy if that issuer is compromised or unavailable).

### Measured results
None measured by the authors. This is a framework and requirements paper: it defines a mechanism category, states design requirements for it, and analyzes benefits, risks, and implementation choices; it runs no experiment, testbed, or simulation of its own. Every quantitative figure the paper states is an external estimate the authors cite from another source, not a measurement performed for this paper, so per Rule 1 none of these figures is usable as this paper's own measured evidence; they are recorded below only as attributed external citations appearing in the paper's text, each with the number and its source as the paper states it.

| Figure (external citation, not authored by this paper) | Context as stated in the paper |
|---|---|
| Worldcoin reported 6 million signups | As of the paper's citation, dated July 2024 [ref 273 in the paper's bibliography] |
| Idena had on the order of several thousand members | As of April 2022 [refs 129, 192] |
| Proof of Humanity had roughly 17,000 members | As of 2022 [ref 170] |
| Underground market for fraudulent account registration estimated at USD 4.8-128.1 million per year | As of 2022 [ref 106] |
| Approximately 850 million people worldwide lack an official identity document | [ref 272] |
| Approximately 3.3 billion people worldwide lack access to an official digital identity for online transactions | [ref 272] |
| Nearly 18 million bot-generated comments compromised the US FCC's 2017 net-neutrality public comment process | [ref 191] |

### Parameters
None stated as tunable numeric parameters with tested values or ranges — the paper is a requirements and design-space document, not an implementation. Where it discusses parameter-like design choices (for example, "at most three verified accounts" per credential per service, or a credential's expiry period), it presents them as illustrative or issuer-configurable, not as values it tested or recommends.

### Stated limitations
The paper explicitly declines to evaluate whether any deployed proof-of-personhood system (Idena, Worldcoin, Proof of Humanity, BrightID) actually satisfies the two PHC requirements it defines, stating that "a fuller evaluation of existing proof-of-personhood systems... is beyond the scope of this paper."

The paper states that Web-of-Trust-based credential-limit enforcement struggles specifically with the uniqueness half of the credential-limit requirement: a person can obtain multiple credentials by enrolling through multiple, sufficiently separate social circles, because vouching validates that a person exists without bounding how many distinct graphs will vouch for the same person.

The paper states that an issuer storing no identifying information after enrollment (to maximize privacy) creates a structural difficulty for account recovery: the issuer then has no record linking a lost or stolen credential to a specific enrollee, and existing cryptographic literature on anonymous-credential recovery offers only partial solutions to this problem.

The paper states that unlinkable pseudonymity does not defend against pervasive existing web-tracking techniques (browser fingerprinting, third-party tracking) that operate independently of the credential mechanism, so credential holders remain traceable through unrelated means the credential itself does not touch.

The paper states that Web-of-Trust seeding and biometric-based enrollment both face an availability gap: not everyone has a government-issued identity document, and not everyone is well-connected in a vouching graph, so different credential-limit methods systematically exclude different populations rather than one method dominating.

The paper states a governance risk it does not resolve: an issuer or a coalition of colluding service providers with government-compulsion power could be compelled to disclose usage records despite the credential's default unlinkability design; the paper calls this "one risk of government-issued personhood credentials" without proposing a technical countermeasure beyond noting that resistance to this compulsion is a stated design goal.

The paper states that its own threat-model discussion in the robustness section is explicitly non-exhaustive: "these threat models and considerations are by no means comprehensive."

### Requirements it places on the rest of the system
The credential-limit check (one credential per person per issuer) requires the issuer to have access, at enrollment time, to some external one-per-person-bounded signal: an identity document system with its own finite-per-person guarantee, a biometric-matching system capable of comparing a new enrollee against every prior enrollee's stored (or hashed/encrypted) biometric template, or a pre-existing Web-of-Trust graph seeded by one of the other two methods. Without one of these three external inputs, the issuer has no mechanism to detect a person re-enrolling under a different guise.

The usage-side unlinkable pseudonymity property requires public-key infrastructure at the issuer (a maintained list of valid public keys, one per issued credential) and a zero-knowledge proof system that lets a holder prove membership in that list without revealing which entry is theirs; the rest of the system must supply a zero-knowledge proof construction (the paper mentions zk-SNARKs, zk-STARKs, and ring signatures as candidate constructions without selecting one) before usage-time unlinkability can be implemented.

Per-service rate limiting (detecting repeated use of one credential with one service, without identifying which credential) requires a cryptographic nullifier scheme: each service provider must be able to compute and store a nullifier per usage event, deterministic in the credential and the service's identity, and must trust that this nullifier construction does not leak information usable to correlate activity across different services.

Recovery and revocation of a lost or stolen credential require the issuer to retain some minimal recovery-enabling information (encrypted, per the paper's guidance) or to substitute a non-identifying recovery mechanism (back-up codes, security questions chosen to be non-identifying, hardware tokens); the paper states this design choice directly trades against the privacy goal of storing zero identifying information, so whichever choice is made constrains what the issuer can offer for account recovery.

The credential-limit method interacts with the rest of the ecosystem's design: the paper's own argument for bounded (greater-than-one, not-too-many) credentials per person requires multiple independent issuers to exist simultaneously, each separately enforcing its own one-per-person limit, for the ecosystem-level privacy/anti-deception balance the paper argues for to hold; a single-issuer deployment does not produce the trade-off the paper's Figure 4 argument describes.

### Contradicts
None found against other entries in this corpus. The paper explicitly avoids making the empirical claims that would be checkable against measurement papers — it neither states nor implies specific accuracy, false-positive, or Sybil-resistance figures for any concrete proof-of-personhood system, which forecloses the most likely axis of disagreement with a measurement-based paper on the same systems.

### References worth retrieving
- Borge, M.; Kokoris-Kogias, E.; Jovanovic, P.; Gasser, L.; Gailly, N.; Ford, B. "Proof-of-Personhood: Redemocratizing permissionless cryptocurrencies." 2017 IEEE European Symposium on Security and Privacy Workshops (EuroS&PW), pp. 23-26, IEEE, 2017. DOI 10.1109/EuroSPW.2017.46. — foundational (introduces the proof-of-personhood concept this paper's PHC category generalizes and distinguishes itself from).
- Siddarth, D.; Ivliev, S.; Siri, S.; Berman, P. "Who watches the watchmen? A review of subjective approaches for Sybil-resistance in Proof of Personhood protocols." Frontiers in Blockchain, 3, 2020. — competing/survey (directly surveys Sybil-resistance in the proof-of-personhood systems this paper discusses; a Sybil-resistance domain paper worth cross-referencing against this domain's brief).
- Druschel, P.; Kaashoek, M. F., editors. "First International Workshop on Peer-to-Peer Systems, Revised..." 2002. — foundational (cited by this paper as the foundational treatment of Sybil attacks; likely proceedings volume containing Douceur's "The Sybil Attack").
- Decentralist.com. "Proof of personhood project round-up." Coinmonks, 2023. — competing (survey of deployed proof-of-personhood systems including Idena, Worldcoin, Proof of Humanity, BrightID; a secondary source, not a substitute for retrieving primary papers on each system).

### Verbatim extracts
- "digital credentials that empower users to demonstrate that they are real people—not AIs—to online services, without disclosing any personal information"
- "a fuller evaluation of existing proof-of-personhood systems... is beyond the scope of this paper"
- "these systems can struggle to confirm uniqueness: A person may be able to get multiple credentials"
- "there are always difficulties in determining what sensitive information can be inferred"
- "these threat models and considerations are by no means comprehensive"
- "one risk of government-issued personhood credentials is that the government may be able to compel service providers"
- "Around 850 million people worldwide do not currently have an official identification document"
