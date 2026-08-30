## [MELARA-USENIXSEC-15] CONIKS: Bringing Key Transparency to End Users

**Citation:** Marcela S. Melara, Aaron Blankstein, Joseph Bonneau, Edward W. Felten, Michael J. Freedman. "CONIKS: Bringing Key Transparency to End Users." USENIX Security Symposium, 2015. Pages 383-398. DOI: none listed (USENIX open-access paper).
**Retrieved:** full text via https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-melara.pdf
**Source URL:** https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-melara.pdf
**Domain:** E

### What it does
CONIKS lets a user detect whether an identity provider has inserted a false public key for that user's name, without any user having to inspect the full list of registered names. Each identity provider maintains a directory that maps user names to public keys, stored as a Merkle prefix tree: a binary tree in which each node stands for a bit-prefix, an interior node hashes its two children, a leaf node hashes a commitment to a name and its key data, and an empty node marks a prefix with no entry. At fixed intervals called epochs, the provider signs the tree root together with the previous epoch's signed root, producing a signed tree root (STR) that chains epoch to epoch into a linear history. A client holding an STR can request a proof of inclusion (the sibling hashes on the path from a leaf to the root) or a proof of absence (the path to the longest matching prefix) and recompute the root locally to check consistency, without trusting the provider's word.

To keep a user's own directory position from leaking who else is registered, CONIKS computes each user's tree index with a verifiable unpredictable function (VUF) of the username, keyed to a provider secret, rather than a plain hash: an index computed by any publicly computable function would let an attacker probe for other registered names sharing a tree prefix with a known name. A verifiable unpredictable function requires the private key to compute but lets anyone with the public key check that a given index was computed correctly; it differs from a verifiable random function only in dropping the pseudorandomness requirement. The value stored at each leaf is a cryptographic commitment to the key data, not the key itself, so an authentication path alone reveals neither the key nor whether an index answers a particular username.

Three protocols use this structure. Lookup: a client requesting another user's key receives the authentication path and the current STR and checks the path recomputes to that root. Monitoring: every client fetches, each epoch, the authentication path to its own binding and checks that the binding has not changed unexpectedly; because only the hashes on that user's path that changed since the last epoch need be sent, and the number of tree-wide changes per epoch is n, the number of expected changed nodes on a given path is log2(n). Auditing: any party (clients auditing their own provider, providers auditing each other, or third parties) tracks the hash chain of STRs and checks it never forks; a fork can only be created by the provider showing two different STRs to two different parties for the same epoch, which is a non-equivocation violation and, for a fork the two parties can compare notes on, produces cryptographic evidence.

### Measured results

| Quantity | Value | Conditions |
|---|---|---|
| Server epoch computation | 2.6 s average | Prototype Java server, 2.4 GHz Intel Xeon E5620, 64 GB RAM allotted to OpenJDK 1.7 JVM; Merkle prefix tree pre-loaded with 10 million users; batch of 1,000 insertions per epoch (about 3x the paper's assumed 221 updates/epoch at 232 users); mean over runs shown in Figure 7, error bars = standard deviation over 10 executions |
| Client verification of one authentication path | 159 microseconds average, sigma = 30 | 2 GHz Intel Core i7 laptop, 10-million-user directory, sampled over 1,000 runs, EC-Schnorr signature scheme |
| Client signature verification | approximately 400 microseconds | Same setup; dominates authentication-path verification cost |
| Client bandwidth: one lookup | 1,568 B (RSA) / 1,216 B (EC-Schnorr) / 1,120 B (BLS) | N ~ 2^32 total users, so ~lg2(N)+1 = 33 hashes at 32 B each plus one VUF proof (96 B EC) plus one signature |
| Client bandwidth: monitor one epoch | 928 B (RSA) / 726 B (EC) / 704 B (BLS) | n ~ 2^21 directory changes/epoch (assumed 1% of 2^32 users change/add keys per day, ~24 epochs/day); expected lg2(n) = 21 changed hashes on the user's path |
| Client bandwidth: monitor one day | 22.6 kB (RSA) / 17.6 kB (EC) / 16.1 kB (BLS) | k ~ 24 epochs/day, k signatures aggregated where the scheme (BLS) supports it, else k separate signatures; assumes users update randomly through the day, the paper's stated worst case for bandwidth versus bursty updates |
| Auditing one provider, one epoch's STR | 288 B (RSA) / 96 B (EC) / 64 B (BLS) | Minimal STR form: signature + 32 B root + 8 B timestamp, previous STR and epoch number inferred |
| Auditing one provider, one day | 6.9 kB (RSA) / 2.3 kB (EC) / 0.8 kB (BLS) | 24 epochs/day |
| Probability neither of two colluding-free users detects an equivocation after k checks each with random auditors | epsilon <= (1/4)^k; 99.9% detection after 5 checks each | Single equivocating provider, no colluding auditors, worst-case split fraction f = 1/2 of auditors shown each of the two STRs |
| Probability of non-detection with a colluding fraction p of auditors | epsilon <= ((1+p)/2)^(2k); 99.7% detection after 5 checks each at p = 0.1; over 94% detection within 5 checks whenever fewer than 50% of auditors collude | Provider colludes with fraction p of auditors, remaining honest auditors split according to worst-case f = 1/2 |

### Parameters
- Assumed scale: N ~ 2^32 users per provider, n ~ 2^21 directory updates per average epoch (assuming up to 1% of users change or add keys per day), k ~ 24 epochs per day (roughly hourly epochs), 128-bit cryptographic security level.
- Hash function: SHA-256.
- Three evaluated signature/VUF choices: EC-Schnorr (512-bit signature, 768-bit/96-byte VUF proof), RSA-2048 with PKCS#1v1.5 padding (deterministic, ~112-bit security, 2048-bit proof), BLS pairing-based short signatures (256-bit signature, supports aggregation of multiple signatures under one key into one).
- The paper's own discrete-log VUF/VRF construction (Appendix A) uses a group of prime order q with generator g; proof size for a 256-bit elliptic curve is 768 bits (96 bytes).

### Stated limitations
The prototype (CONIKS Chat, built on the OTR plugin for Pidgin over an unmodified Tigase XMPP server) does not support key changes and implements only the default lookup policy. CONIKS does not defend against a communication provider who can reliably block all of a client's network access, since whistleblowing requires an out-of-band channel the provider does not control. A malicious provider can ignore all requests for one name, denying service to that binding for as long as the denial continues, though any binding modification made during the denial becomes visible once service resumes. Device pairing across multiple client devices is stated as unsolved in practice: the paranoid key-change policy that lets a client automatically distinguish a legitimate new device from a malicious insertion requires a manual pairing step, whereas the alternative (auto-enrolling a new device with password authentication) removes the client's ability to make that distinction automatically. Obfuscating which users communicate with each other is left as a design sketch (proxying lookups through other providers, or a full mixnet), not implemented or measured. Randomizing directory-entry order to stop cross-entry leakage between adjacent tree positions requires rebuilding the whole tree, and doing so every epoch is stated as a full efficiency-versus-privacy tradeoff with no measurement given. If a client's device is compromised and its private key stolen while the client has already declared its old binding "lost," a future attacker with that stolen key can assume the identity for that binding.

### Requirements it places on the rest of the system
Every client needs persistent local storage across sessions to retain the most recent verified STR and to check monitoring proofs epoch to epoch; the paper states this explicitly as an assumption. Detecting a whistleblowable equivocation requires that at least one of a user's client devices retain network access the identity provider cannot fully block. Non-equivocation detection with cryptographic evidence, rather than mere private awareness, requires at least one other client or auditor to independently observe a divergent STR and requires auditors to gossip so that a fork must be maintained forever by an equivocating provider or be discovered; the scheme provides no mechanism to force that gossip to happen, only the format of the evidence once it does. The VUF used for private indices must be a deterministic, existentially unforgeable signature scheme; a non-deterministic scheme would let a provider register multiple valid bindings for one name at different indices. Providers must publish an epoch-numbered, monotonically increasing (not necessarily sequential) STR on a schedule agreed with clients; nothing in the mechanism enforces that a provider publishes on time, only that any two STRs it does publish for the same epoch are detectable as a fork once compared.

### Contradicts
None found.

### References worth retrieving
- **Foundational:** J. Li, M. Krohn, D. Mazières, D. Shasha, "Secure untrusted data repository (SUNDR)," OSDI 2004 — fork consistency, the property CONIKS's STR chain relies on to make equivocation costly.
- **Foundational:** S. Micali, M. Rabin, S. Vadhan, "Verifiable random functions," FOCS 1999 — defines the VRF family CONIKS's VUF weakens.
- **Competing:** B. Laurie, A. Langley, E. Kasper, "RFC 6962 Certificate Transparency," 2013 — the transparency-log design CONIKS explicitly compares against and says requires third-party monitors scanning the full issued-certificate list, unlike CONIKS's per-user monitoring.
- **Competing:** M. D. Ryan, "Enhanced certificate transparency and end-to-end encrypted email," NDSS 2014 — adds efficient current-validity queries to CT via a second Merkle tree, but the paper states auditing it costs effort linear in total log changes, versus CONIKS's constant per-STR audit cost.
- **Competing:** T. H.-J. Kim, L.-S. Huang, A. Perrig, C. Jackson, V. Gligor, "Accountable key infrastructure (AKI)," WWW 2013 — combines append-only logs with other infrastructure; classified by the paper alongside Sovereign Keys as a related certificate-validation proposal.
- **Foundational:** N. Unger, S. Dechand, J. Bonneau, S. Fahl, H. Perl, I. Goldberg, M. Smith, "SoK: Secure Messaging," IEEE S&P 2015 — systematization this paper cites for the broader secure-messaging landscape CONIKS integrates into.

### Verbatim extracts
- "downloading less than 20 kB per day to do so even for a provider with billions of users."
- "this requires downloading a constant 2.5 kB per provider per day."
- "computing a new Merkle tree with 1000 insertions takes on average 2.6 s."
- "verifying the authentication path returned by a server with 10 million users, required on average 159 µs."
- "If fewer than 50% of auditors are colluding, Alice and Bob will detect an equivocation within 5 checks with over 94% probability."
- "CONIKS Chat currently does not support key changes."
- "device pairing has proved cumbersome and error-prone for users in practice."
