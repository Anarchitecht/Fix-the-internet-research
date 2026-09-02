## [WACHS-CANS-14] A Censorship-Resistant, Privacy-Enhancing and Fully Decentralized Name System

**Citation:** Matthias Wachs, Martin Schanzenbach, Christian Grothoff. "A Censorship-Resistant, Privacy-Enhancing and Fully Decentralized Name System." International Conference on Cryptology and Network Security (CANS), 2014. DOI 10.1007/978-3-319-12280-9_9.
**Retrieved:** full text via https://grothoff.org/christian/gns.pdf
**Source URL:** https://grothoff.org/christian/gns.pdf
**Domain:** E

### What it does
The GNU Name System (GNS) resolves human-memorable names to cryptographic keys and other records without a global registry, a certificate authority, or a blockchain. Each user holds one or more zones; a zone is an ECDSA (Elliptic Curve Digital Signature Algorithm) public/private key pair over Curve25519 plus a set of records (label, type, value, expiration time), stored locally in a namestore database the zone owner controls. A user designates one zone as a master zone and resolves names starting from it, in place of a DNS (Domain Name System) root zone. A user delegates a subdomain to another user's zone by adding a PKEY record naming that zone's public key under a locally chosen label; resolving a multi-label name follows the chain of PKEY delegations one zone at a time. Public records are additionally published into a distributed hash table (DHT) so other users can resolve names that cross into zones they do not hold locally. A record can instead be marked private and kept only in the local namestore. The scheme sets label assignment per delegating user rather than globally, so the same string can point to different zones for different observers; a NICK record lets a zone owner suggest a default label so other users adopt it as a default when they add a delegation to that zone, without making the label globally unique. The "+" placeholder in a name is replaced by the resolving client with the label of the zone from which resolution started, so a link authored in one zone still resolves to the correct target when a different zone imports it under a different local label (a relative-name mechanism). The ".zkey" pseudo top-level domain names a zone directly by encoding its public key as a DNS label, giving an absolute identifier for a zone that has no memorable delegation path yet.

Query privacy: for a zone with private key x and public key P = xG (G the elliptic-curve generator), and a label represented as l, the publisher computes h = x·l mod n, publishes the record block under the DHT key Q(l,P) = H(hG), and encrypts the record block with a key derived by a hash-based key derivation function (HKDF) from (l, P). A peer who knows both l and P computes Q(l,P) = H(lP) = H(lxG) = H(hG) to find the block, then decrypts it. A peer holding only the DHT key material without knowing both l and P cannot compute the query or decrypt the reply.

Revocation: a zone owner creates a revocation notice in advance of key loss or compromise. On use, the notice is flooded peer-to-peer (every peer forwards every previously unseen valid notice to all neighbors) rather than looked up on demand, because an on-demand revocation check would add latency and bandwidth to every zone access and would reveal to observers which zone a user is resolving. A proof-of-work requirement on the revocation notice bounds flooding abuse, paid once by the revoker rather than checked by resolvers. Peers that were partitioned from the network, or newly joined, exchange only the difference between their revocation sets using Eppstein's set-reconciliation method, so healing costs bandwidth proportional to the size of that difference rather than to the full revocation set.

### Measured results
None. The paper presents a design and a security analysis; it reports no experiment, testbed, node count, or timing measurement. Section 1 states usability experiments with GNS as future work ("experiments to find out which usability problems arise with GNS," line 474) and does not report results from them.

### Parameters
| Parameter | Value stated |
|---|---|
| Signature scheme | ECDSA over Curve25519 |
| DHT used in the reference implementation | R5N (Randomized Recursive Routing for Restricted-Route Networks) |
| GNS reply payload limit | up to 63 kB |
| DNS packet size limit noted for comparison | often 512 bytes |
| Maximum trusted computing base (TCB) per individual name | fewer than about 125 entities, following from DNS label length restrictions carried into GNS names |
| Revocation notice size | a few bytes |
| BOX record fields | 16-bit port, 16-bit protocol identifier, 32-bit embedded record type, embedded record value |

### Stated limitations
GNS cannot return an equivalent of DNS's NXDOMAIN (non-existent domain) response, because doing so would require a query round trip that GNS's privacy construction avoids; the client therefore cannot distinguish "record absent" from "record not yet found" and faces indefinite lookup latency for records that do not exist. The paper introduces the BOX record specifically to reduce, not eliminate, indefinite latency for the SRV/TLSA case by placing dependent records under one lookup. A confirmation attack cannot be prevented: an adversary who already knows both a zone's public key and a specific label can perform the same query as any peer and thereby confirm that a specific record exists and read it. A user's ability to reach a name at all depends on having previously obtained a delegation from someone who already knows the target zone, so first discovery of an unfamiliar zone requires an out-of-band channel (the paper gives no in-band bootstrap for an entirely unknown zone). GNS does not address censorship below the naming layer, such as IP-address blocking of a server that a resolved name points to; the paper states this is out of scope and recommends pairing GNS with Tor for that threat. The paper states it cannot give a numeric estimate of the damage from a successful social-engineering attack on a user's delegations, because "the system is not deployed yet" and no measurement of the resulting GNS delegation graph exists.

### Requirements it places on the rest of the system
Resolution of any name outside a user's own zones requires a prior delegation the user (or one of their contacts, transitively) obtained out of band; the system supplies no mechanism for a first, trust-free discovery of an arbitrary unfamiliar zone. Publication of any record intended for other users requires a DHT that the paper explicitly treats as untrusted for integrity — every published record must carry its own signature and expiration, because the paper's threat model allows the DHT to degrade availability and performance but relies on the signature scheme, not the DHT, for authenticity. The revocation mechanism requires a peer-to-peer overlay beneath the DHT capable of flooding to all neighbors, and requires that a proof-of-work check gate acceptance of revocation notices to bound denial-of-service flooding. Resolving a name that crosses zones requires the resolving client to hold, or be able to fetch through the DHT, every zone's public record in the delegation chain, so delegation-chain length translates directly into the number of DHT lookups an application must complete before a name resolves, and each additional zone in a chain adds to the trusted computing base a resolving user takes on for that name.

### Contradicts
None found within this corpus. The paper's own account of Namecoin (a proof-of-work timeline naming system) states that Namecoin's ledger-consensus approach fails under its own adversary model — an adversary with more computational power than all other participants combined can construct an alternative valid timeline — a structural consequence, not a value judgment about Namecoin.

### References worth retrieving
- foundational: Stiegler, M. "An introduction to petname systems." (petname-system origin)
- foundational: Rivest, R.L., Lampson, B. "SDSI – a simple distributed security infrastructure." (SDSI/SPKI, the delegation model GNS builds on)
- foundational: Wilcox-O'Hearn, Z. "Names: Decentralized, secure, human-meaningful: Choose two." (Zooko's triangle)
- competing: Nakamoto, S. "Bitcoin: A peer-to-peer electronic cash system." (ledger-consensus naming's underlying mechanism)
- competing: "The Dot-BIT project, A decentralized, open DNS system based on Bitcoin technology." (Namecoin)
- competing: Ford, B.A. "UIA: A Global Connectivity Architecture for Mobile Personal Devices." (the other SDSI-derived personal-naming system, compared directly in Related Work)
- competing: D. J. Bernstein. "DNSCurve: Usable security for DNS." (confidentiality-only DNS alternative, compared directly)
- attack: Anonymous. "The collateral damage of internet censorship by DNS injection." ACM SIGCOMM CCR. (measured cross-border DNS censorship effect the paper cites as motivation)
- attack: Deccio, C., Sedayao, J., Kant, K., Mohapatra, P. "Quantifying DNS namespace influence." (DNS trust-chain-depth measurement, source of the "over a hundred DNS zones" claim GNS compares its TCB against)
- foundational: Evans, N., Grothoff, C. "R5N: Randomized Recursive Routing for Restricted-Route Networks." (the DHT GNS is built on; its Eclipse-attack resistance is asserted here by citation, not re-derived)
- competing: Ulrich, A., Holz, R., Hauck, P., Carle, G. "Investigating the OpenPGP Web of Trust." (independent measurement of the mesh structure of a deployed delegation graph, the closest existing analog to a GNS delegation graph)

### Verbatim extracts
- "no name system can provide globally unique and memorable names and be secure"
- "the worst an adversary can do here is reduce performance and availability, but not impact integrity"
- "in GNS NXDOMAIN is not possible, largely due to GNS's provisions for query privacy"
- "an adversary that is unable to guess both the zone's public key and the label cannot determine" it
- "for an individual name it is always less than about 125 entities"
- "GNS is not intended as an answer to this kind of censorship"
