## [W3C-VCDM-25] Verifiable Credentials Data Model v2.0

**Citation:** W3C Verifiable Credentials Working Group (Manu Sporny, Ted Thibodeau Jr., Ivan Herman, Michael B. Jones, Gabe Cohen, editors). "Verifiable Credentials Data Model v2.0." W3C Recommendation, 2025.
**Retrieved:** full text via https://www.w3.org/TR/vc-data-model-2.0/ — VERSION CAVEAT, see below.
**Source URL:** https://www.w3.org/TR/vc-data-model-2.0/
**Domain:** E

**Version caveat:** The document at this URL, as fetched, is titled "Verifiable Credentials Data Model v2.1," one revision past the "v2.0" W3C Recommendation the registry entry cites, for the same reason as W3C-DIDCORE-22: the `/TR/` URL is a living pointer to the latest version. The retrieved text's own revision history lists the deltas since the immediately preceding step ("v2.0 Second Candidate Recommendation"): editorial clarification, aligning error-condition fields across companion Working Group specifications, and clarified requirements for self-asserted credentials. No structural change to the credential data model, the status mechanism, or the zero-knowledge-proof securing-mechanism section is listed between v2.0 and this retrieved v2.1 text, so the data model, status, and privacy content below are extracted as applying to v2.0. A v2.0-specific wording claim is not extracted from this text where the changelog marks a difference.

### What it does
A verifiable credential expresses a set of claims made by an issuer about a subject in a form a verifier can cryptographically check, without the verifier contacting the issuer at presentation time. The specification defines a three-party data flow: an issuer creates a credential and secures it with a cryptographic proof; a holder receives, stores, and later presents the credential (or a derived subset of it) to a verifier, optionally bundling multiple credentials into one verifiable presentation; a verifier checks the proof and, separately, checks any credentialStatus entry the credential carries. A credential's data model core is: `id`, `type` (must include `VerifiableCredential`), `issuer`, `validFrom`/`validUntil`, `credentialSubject` (the claims), and an optional `credentialStatus` object or set of objects. Two families of securing mechanism attach a cryptographic proof to this data: embedded proofs, of type `DataIntegrityProof`, add a `proof` property directly inside the credential's JSON-LD document, carrying a `cryptosuite` name, a `verificationMethod` identifying the signing key, a `proofPurpose`, and a `proofValue`; enveloping proofs (JOSE/COSE, referenced normatively from the companion `VC-JOSE-COSE` specification) instead wrap the whole credential as an opaque signed or encrypted object referenced by a `data:` URL. `credentialStatus` names a status mechanism (the specification's own example type is `BitstringStatusList`) by pointing a verifier at a separate published bitstring credential, in which the credential's `statusListIndex` selects one bit that encodes revocation or suspension state (`statusPurpose` states which); the specification defines only the pointer property and requires that whatever status-list mechanism a `credentialStatus` type names must not let the issuer learn, from a verifier fetching status, which specific individual's status was checked.

Zero-knowledge-proof securing mechanisms (an example instantiated with the BBS signature scheme, cross-referenced to a separate `VC-DI-BBS` specification) let a holder derive, from one issuer-signed base credential, a second proof that discloses only a chosen subset of the claims (selective disclosure) and that differs in value on every presentation so that separate presentations of the same underlying credential cannot be linked to each other by their signature bytes (unlinkable disclosure). The specification states that most such mechanisms require the issuer to sign the base credential in a form that supports the derivation, so a holder cannot retrofit unlinkable disclosure onto a credential the issuer signed with an ordinary (non-derivable) signature.

### Measured results
None. This is a normative data-model and vocabulary specification; it defines properties, syntax, and conformance requirements and reports no experiment, benchmark, deployment count, or implementation-count outcome. Exit-criteria implementation-count requirements are referenced by the surrounding W3C process but their results are not part of this document's text.

### Parameters
Not applicable as tunable numeric values; the closest equivalents are the required/optional status of core properties and the two named securing-mechanism specifications this document normatively points to:

| Property | Required? |
|---|---|
| `id` (credential) | no (but MUST follow identifier rules in Section 5 if present) |
| `type` | yes, MUST include `VerifiableCredential` |
| `issuer` | yes |
| `validFrom` / `validUntil` | no |
| `credentialSubject` | yes |
| `credentialStatus` | no; MAY be a single object or a set of objects |
| `credentialStatus.type` | required, if `credentialStatus` present |
| `credentialStatus.id` | optional, if `credentialStatus` present |

Normatively referenced securing mechanisms: `VC-DATA-INTEGRITY` (embedded `DataIntegrityProof`, cryptosuite examples include `bbs-2023`), `VC-JOSE-COSE` (enveloping proofs).

### Stated limitations
The specification states it does not define the data model, format, or protocol of any concrete credential-status scheme; `BitstringStatusList` appears only as an example, and the actual behavior of status checking (what a verifier fetches, and how often) is deferred entirely to whichever status-type specification a credential's `credentialStatus.type` names. It states that reconciling conflicting information across multiple `credentialStatus` entries on one credential is part of the verifier's own business logic and is out of scope of this specification. It states that how a verifier decides which issuers to trust, and for what data or purposes, is out of scope, deferring to external trust-list mechanisms (it cites ETSI trust lists and the Adobe Approved Trust List as existing examples, not as part of this specification). It states not every zero-knowledge-proof mechanism supports every one of selective disclosure, unlinkable disclosure, and non-correlatable holder identification, and that which of the three a given mechanism provides is defined by that mechanism's own specification, not by this data model. It states that a credential is, in general, expected to leak personally identifiable information when shared, in the same way a physical credential does, and that avoiding this leakage requires deliberately choosing a credential type and securing mechanism designed against correlation, not a property this specification supplies by default.

### Requirements it places on the rest of the system
A credentialStatus check requires a separately specified and separately hosted status mechanism (the specification names `BitstringStatusList` only as an example) that the verifier fetches; that mechanism is required, by this specification's own normative language, not to let the issuer learn which specific individual's status a verifier is checking — ruling out any status design in which a verifier's status check reaches the issuer's own server per individual lookup ("phoning home"), or in which the fetch pattern itself lets the issuer deduce verifier interest in a specific individual ("pseudonymity reduction"). Selective and unlinkable disclosure require the issuer to sign the base credential with a securing mechanism that itself supports derivation (the specification's own worked example uses the BBS cryptosuite `bbs-2023`); a credential signed with an ordinary non-derivable signature cannot be selectively disclosed after the fact by the holder alone. Identifying an issuer, subject, or verification method requires an identifier scheme that supports resolution and verification of associated key material; the specification's own examples resolve issuer and verification-method identifiers as DIDs (Decentralized Identifiers) and normatively cross-references the DID specification for that resolution, without itself constraining a credential to using DIDs specifically. Avoiding identifier-based correlation requires the holder's software to detect long-lived identifiers (subject IDs, email addresses, government-issued identifiers) inside a credential before sharing it and, where the issuer's securing mechanism supports it, to substitute a holder-generated or selectively-hidden identifier instead — a capability this specification requires securing-mechanism authors to make available, not one the base data model provides on its own.

### Contradicts
None found within this corpus.

### References worth retrieving
- foundational: `VC-DATA-INTEGRITY` — the Data Integrity specification defining the embedded `DataIntegrityProof` mechanism and its cryptosuite registry; needed for the actual signature-verification algorithm this document only references.
- foundational: `VC-JOSE-COSE` — the enveloping-proof specification (JOSE/COSE-based securing); needed for the alternative signature envelope this document only references.
- competing/extension: `VC-DI-BBS` — the BBS-based Data Integrity cryptosuite specification providing the unlinkable selective-disclosure mechanism whose worked example appears in this document; the primary place to find measured proof-size or verification-cost figures for BBS-secured credentials, none of which are in this document.
- foundational: `[[?DID]]` — the Decentralized Identifiers specification this document's issuer and verification-method examples resolve against (see W3C-DIDCORE-22 in this corpus).
- competing: `VC-JSON-SCHEMA` — the credential-schema validation mechanism referenced for the `credentialSchema` property, not itself defined in this document.
- foundational: `[[FIPS-186-5]]`, `[[NIST-SP-800-57-Part-1]]` — cited normatively for key-reuse restrictions on signing keys used to secure credentials.
- related: `[[?VC-EXTENSIONS]]` — the registry of available credential-status schemes this document defers to instead of defining one itself.
- related: `[[?ETSI-TRUST-LISTS]]` — cited as one existing external trust-list mechanism for issuer trust decisions this specification leaves out of scope.

### Verbatim extracts
- "Defining the data model, formats, and protocols for status schemes is out of the scope"
- "Credential status specifications MUST NOT enable tracking of individuals"
- "How verifiers decide which issuers to trust...is out of scope for this recommendation"
- "for the holder to make use of zero knowledge mechanisms...the issuer is required to secure" it
- "individuals are advised to assume that a verifiable credential...will leak personally identifiable information when shared"
