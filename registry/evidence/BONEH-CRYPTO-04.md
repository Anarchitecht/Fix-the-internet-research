## [BONEH-CRYPTO-04] Short Group Signatures
**Citation:** Dan Boneh, Xavier Boyen, Hovav Shacham. "Short Group Signatures." CRYPTO, 2004. DOI 10.1007/978-3-540-28628-8_3.
**Retrieved:** full text via https://crypto.stanford.edu/~xb/crypto04a/groupsigs.pdf
**Source URL:** https://doi.org/10.1007/978-3-540-28628-8_3
**Domain:** E

### What it does
A group signature scheme lets any member of a registered group sign a message so a verifier is convinced some group member signed, without learning which one, while a separate group manager holding a trapdoor key can later trace a specific signature back to its signer (de-anonymize it on demand). This paper — the BBS group signature scheme — constructs one whose signatures are shorter than prior constructions, so it fits applications with a hard per-message size limit.

The scheme (KeyGen, Sign, Verify, Open) works over a bilinear group pair (G1, G2) with an efficient isomorphism from G2 to G1 and a bilinear pairing e: G1 x G2 -> GT, and it uses two hardness assumptions: the Strong Diffie-Hellman (SDH) assumption and a new assumption the paper introduces, called the Decision Linear (Linear) assumption, needed because the standard decisional Diffie-Hellman problem is easy in these bilinear groups and so cannot supply hardness on its own. KeyGen(n) picks group generators, an SDH secret gamma known only to the private-key issuer, and for each of n users a tuple (A_i, x_i) with A_i = g1^(1/(gamma+x_i)); the group public key is (g1, g2, h, u, v, w) and the group manager's tracing key is (xi_1, xi_2), a pair of discrete logarithms used to decrypt a Linear-encryption component embedded in every signature. To sign, a user produces a nine-element signature of knowledge (a zero-knowledge proof, made non-interactive by the Fiat-Shamir heuristic, that the signer holds a valid (A_i, x_i) pair) over the message. Signing requires no pairing computation, only eight (multi-)exponentiations, because three pairing values can be precomputed and cached by the signer. Verification recomputes the proof's five checked values and requires six multi-exponentiations plus one pairing computation. To trace a signature, the group manager treats its first three elements as a Linear ciphertext and decrypts it with (xi_1, xi_2) to recover the signer's A_i, then looks up which registered user that A_i belongs to.

Section 6 gives a revocation mechanism: a Revocation Authority publishes a Revocation List of revoked users' full private keys, and every signer and verifier recomputes an updated group public key from that list; each unrevoked user locally updates its own private key to match, using field arithmetic over the revoked keys, while a revoked user cannot construct a matching private key for the new public key (proved reducible to breaking SDH). Section 7 describes a JOIN protocol variant achieving strong exculpability, where the key issuer never learns the user's complete private key and so cannot forge signatures on that user's behalf, at the cost of an interactive key-issuing protocol instead of the base scheme's single-step key generation.

### Measured results
A group signature in the base scheme comprises three elements of G1 and six elements of Zp. Using the pairing-friendly curve families the paper cites, choosing a 170-bit prime p and a group G1 whose elements are each 171 bits gives a total signature length of 1533 bits, or 192 bytes — under the paper's 200-byte target and under half of a 512-byte size, at a security level the paper states is approximately that of a 1024-bit RSA signature (128 bytes). No benchmarked wall-clock signing or verification time is reported; the paper instead counts operations: signing takes eight exponentiations and zero pairing computations (three pairings are precomputable and cached), and verification takes six multi-exponentiations plus one pairing computation, with every exponent a 170-bit number at these parameters. These figures are derived from the scheme's algebraic structure and the cited curve family's element sizes, not from a running implementation.

The paper's motivating deployment figure, cited from a US Department of Transportation vehicle-safety-communication system design, states a hard requirement that each signature be under 250 bytes because of the volume of vehicles transmitting concurrently; this is reported by the paper as an external requirement, not a measurement this paper performed.

### Parameters
- Security parameter and prime p: worked example uses a 170-bit prime; G1 elements are 171 bits under the cited curve families.
- n: number of group members, an input to KeyGen; no upper bound on n is stated as a scheme limitation, though the revocation list length is separately bounded by r (see below).
- r: number of revoked users whose keys sit on the Revocation List at a given time; the paper states processing r revocations one at a time is less efficient than processing the whole list at once when keys arrive incrementally, but gives no numeric comparison.
- gamma: the SDH secret held only by the private-key issuer during initial key generation; never held by any other party, including the group manager.
- (xi_1, xi_2): the group manager's tracing key, a pair of discrete logarithms of u and v to base h, distinct from gamma and known only to the manager.

### Stated limitations
The base revocation mechanism requires updates to the Revocation List to reach every verifier simultaneously; the paper states that otherwise, someone who has obtained a new revocation-list entry can produce a signature that a verifier still holding the old public key erroneously accepts. The base scheme provides only ordinary exculpability (no user can be framed by another member, matching the standard full-traceability security definition the paper adopts from Bellare et al.), not strong exculpability (protection from framing by the key issuer itself); the stronger property requires the separate interactive JOIN protocol of Section 7, at the cost of interaction during key issuance. The paper states no benchmarked implementation timing, only algebraic operation counts, so any latency figure for this scheme in a downstream synthesis is not directly supported by this paper's own measurements.

### Requirements it places on the rest of the system
A pairing-friendly bilinear group pair (G1, G2) with an efficient isomorphism from G2 to G1 must be available, and the group manager's tracing key (xi_1, xi_2) must be generated and held separately from the SDH secret gamma used at key-issuing time — gamma must not survive key generation in the hands of any party, including the group manager, or every user's untraceability guarantee is void. The base (non-JOIN) key-issuing process requires a single trusted key issuer who computes and hands out each user's full private key (A_i, x_i); this issuer is trusted not to forge signatures on behalf of users unless the system instead runs the Section 7 JOIN protocol, which requires an additional interactive round between issuer and user before that trust assumption can be dropped. The base revocation mechanism requires a broadcast channel able to deliver every Revocation List update to all verifiers before any signature under the old public key is accepted elsewhere; a verifier that misses an update can be fooled by a signer whose key has already been revoked. Verifier-Local Revocation, cited as a fix (Boneh and Shacham, cited as a manuscript in this paper), instead requires the revocation list to reach only verifiers, not signers, removing the requirement that unrevoked signers update their own keys.

### Contradicts
None found.

### References worth retrieving
- Ateniese, Camenisch, Joye, Tsudik, "A practical and provably secure coalition-resistant group signature scheme," CRYPTO 2000 — competing (the Strong-RSA-based group signature scheme this paper compares signature length against, and the source of the JOIN protocol technique Section 7 adapts).
- Boneh, Boyen, "Short signatures without random oracles" — foundational (introduces the SDH assumption this paper's construction is based on).
- Boneh, Shacham, "Group signatures with verifier-local revocation," 2004 manuscript — foundational (shows how to modify this paper's scheme for Verifier-Local Revocation, the fix to the simultaneous-broadcast revocation requirement).
- Ateniese, Tsudik, Song, "Quasi-efficient revocation of group signatures," Financial Cryptography 2002 — competing (an alternative Strong-RSA revocation mechanism the paper's own revocation design follows the structure of).
- Bellare, Micciancio, Warinschi, (security definitions for group signatures) — foundational (the security model and terminology, including full-traceability and exculpability, that this paper's Section 5 and Section 7 adopt directly).
- Chaum, van Heyst, (introduces group signatures) — foundational (the original definition of the group signature primitive this paper constructs a short instance of).

### Verbatim extracts
"there is a hard requirement that the length of each signature be under 250 bytes"
"We construct short group signatures whose length is under 200 bytes"
"Signature generation requires no bilinear pairing computations"
"it is crucial that updates to the revocation list be sent simultanously to all veriﬁers"
