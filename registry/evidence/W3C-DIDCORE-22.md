## [W3C-DIDCORE-22] Decentralized Identifiers (DIDs) v1.0

**Citation:** W3C Decentralized Identifier Working Group (Manu Sporny, Amy Guy, Markus Sabadello, Drummond Reed, editors). "Decentralized Identifiers (DIDs) v1.0." W3C Recommendation, 2022.
**Retrieved:** full text via https://www.w3.org/TR/did-core/ — VERSION CAVEAT, see below.
**Source URL:** https://www.w3.org/TR/did-core/
**Domain:** E

**Version caveat:** The document at this URL, as fetched, is titled "Decentralized Identifiers (DIDs) v1.1" and is marked a W3C Candidate Recommendation, not the "v1.0" W3C Recommendation of 2022 the registry entry cites. The W3C `/TR/did-core/` URL is a living "latest version" pointer and has moved past the cited document. The retrieved text's own changelog ("Changes since the DID v1.0 Recommendation") lists the deltas: editorial rewording, an updated fragment-resolution algorithm, media-type consolidation to `application/did`, a new JSON-LD context for v1.1, and moving the DID-resolution function definitions out of this document into a separate DID-RESOLUTION specification. The core data model (the properties table below), the DID and DID URL syntax, and the security- and privacy-considerations content are stated by that same changelog to be otherwise carried forward, not rewritten, so those sections are extracted below as applying to both v1.0 and v1.1. Nothing below is drawn from a `resolve()`/`resolveRepresentation()` function-signature section, because v1.1 removed that section from this document; a v1.0-specific claim about that interface is not extracted from this text and would require the v1.0 archived Recommendation.

### What it does
A Decentralized Identifier (DID) provides a global identifier for a subject (a person, organization, thing, or abstract entity) that resolves to a document describing how to interact with and cryptographically verify control over that subject, without depending on a central registry, identity provider, or certificate authority. A DID is a Uniform Resource Identifier (URI) of the form `did:<method-name>:<method-specific-id>`. The method name selects a DID method specification, an independently defined and independently versioned specification that states how DIDs of that type are created, resolved, updated, and deactivated against some concrete verifiable data registry (for example a blockchain, a distributed ledger, or a distributed hash table); this specification defines the identifier syntax and the document data model that every DID method must produce, not the registry or the resolution algorithm itself. Resolving a DID yields a DID document: a set of key/value properties comprising an `id` (the DID itself, required), an optional `controller` (one or more DIDs authorized to make changes), an optional `alsoKnownAs` set of alternate identifiers, an optional `service` set (endpoints for interacting with the subject), an optional `verificationMethod` set (public key material), and five optional verification-relationship properties — `authentication`, `assertionMethod`, `keyAgreement`, `capabilityInvocation`, `capabilityDelegation` — each of which points into `verificationMethod` entries to state which keys are authorized for which purpose. A DID URL extends the DID syntax with an optional path, query, and fragment to address a specific resource inside or reachable from a DID document (for example one verification method by its fragment identifier); dereferencing a DID URL is defined as first resolving the DID it contains, then applying the DID URL's path/query/fragment against the resulting document or an external resource it names.

### Measured results
None. This is a normative specification, not an experimental paper; it defines syntax, a data model, and conformance requirements and reports no implementation count, benchmark, or field measurement. The document's own exit criteria (Candidate Recommendation stage) require at least two independent conforming implementations per machine-testable normative feature, but the retrieved text does not report the results of that implementation survey — it states the requirement, not the outcome.

### Parameters
Not applicable in the sense of a tunable numeric parameter; the specification instead sets required and optional fields. Extracted as the closest equivalent — the DID document's core-property requirement table:

| Property | Required? |
|---|---|
| `id` | yes |
| `controller` | no |
| `alsoKnownAs` | no |
| `service` | no |
| `verificationMethod` | no |
| `authentication` | no |
| `assertionMethod` | no |
| `keyAgreement` | no |
| `capabilityInvocation` | no |
| `capabilityDelegation` | no |

Within a `verificationMethod` map, `id` and `type` and `controller` are each required.

### Stated limitations
The specification states that mapping a human-friendly identifier (a name, domain name, phone number, or social-media handle) to a DID, in a way that can be verified and trusted, is explicitly out of scope; it states this trade-off follows Zooko's Triangle and defers the problem to separate specifications. The specification states there is no common DID recovery mechanism that applies across all DID methods; recovery mechanics (quorum-based, time-locked, or otherwise) are left to each DID method, and cross-method recovery (one DID method recognizing control asserted by a DID registered under a different method) is stated as not guaranteed. Non-repudiation of a DID document update is stated to hold only conditionally: it requires the underlying verifiable data registry to supply verifiable timestamps and requires that the subject had adequate opportunity to revert a malicious update under that DID method's authorization mechanism; the specification does not itself supply either property. Verifying a signature made with a since-revoked key in a "trustless" system (one where every trust judgment derives from cryptographic assertions alone) is stated to require the DID method to expose both `versionId`/`versionTime` on the proof and both `updated`/`nextUpdate` DID-document metadata timestamps; without all four, such verification is not stated to be possible under this specification alone. The specification states that encrypting data inside a DID document is not an appropriate long-term protection for that data, because advances in cryptography or computing power are expected to eventually make currently encrypted data recoverable in clear text to whoever can already see the ciphertext.

### Requirements it places on the rest of the system
A DID cannot be resolved or updated without a separate, independently specified DID method that defines the concrete verifiable data registry and the create/resolve/update/deactivate operations for that method; this specification supplies the identifier syntax and document data model the method's output must conform to, not the operations themselves. A DID resolver is required as a system component that accepts a DID and returns a conforming DID document; a DID URL dereferencer is a further required component that accepts a DID URL and returns the resource it identifies, built on top of DID resolution. Achieving non-repudiation of document updates requires the DID method's verifiable data registry to supply verifiable timestamps, a property this specification does not itself provide and does not require every method to provide. Verifying a proof made under a revoked key inside a trustless system requires the DID method to expose `versionId` or `versionTime` on the proof, and both `updated` and `nextUpdate` in the resolved document's metadata; a DID method lacking these fields cannot support that verification path. Mapping a human-friendly name to a DID requires a separate specification (the document cites `DNS-DID` as one example) layered on top of this one; this specification supplies no mechanism for that mapping and states the security and correlation risks of building one are the responsibility of whichever specification does.

### Contradicts
None found. This entry supersedes no other entry in this corpus and no other corpus entry addresses DID Core directly.

### References worth retrieving
- foundational: [[CID]] — the Controlled Identifier Document specification this version of DID Core is stated to be layered on top of (a restructuring introduced in v1.1; not present as a dependency in the original v1.0 Recommendation).
- foundational: [[?DID-RESOLUTION]] — the specification the DID-resolution function definitions were moved into for v1.1; needed to extract the resolve()/resolveRepresentation() input-output contract that v1.0 stated inline and v1.1 does not.
- competing/related: [[?DID-EXTENSIONS]] — the repository of registered DID method names, verification method types, and DID parameters; needed to check any specific DID method's conformance claims against the registry this specification defers to.
- competing: [[?DID-RUBRIC]] — the "Decentralized Characteristics Rubric" the document cites as a tool for comparing DID methods' persistence guarantees; likely the source of any cross-method comparison data, if such data exists.
- foundational: [[?RFC3552]] — the IETF threat-model document this specification states its Security Considerations section elaborates on.
- foundational: [[RFC8141]] — Uniform Resource Names (URNs), cited for the security considerations a DID controller using a DID as a persistent resource identifier is advised to also follow.

### Verbatim extracts
- "no central authority to mandate which DID method specification is to be used"
- "There are currently no common recovery mechanisms that apply to all DID methods."
- "Encrypting all or parts of a DID document is not an appropriate means to protect data in the long term."
- "the problem of mapping human-friendly identifiers to DIDs...is outside the scope"
- "A DID resolver is a system component that takes a DID as input and produces a...DID document as output"
