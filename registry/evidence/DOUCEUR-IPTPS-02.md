## [DOUCEUR-IPTPS-02] The Sybil Attack

**Citation:** John R. Douceur. "The Sybil Attack." International Workshop on Peer-to-Peer Systems (IPTPS), 2002. Pages 251-260. DOI 10.1007/3-540-45748-8_24.
**Retrieved:** full text
**Source URL:** https://www.freehaven.net/anonbib/cache/sybil.pdf
**Source URL:** https://link.springer.com/content/pdf/10.1007/3-540-45748-8_24.pdf
**Domain:** F

### What it does
The paper proves that a large-scale distributed system cannot bound the number of distinct identities one faulty entity presents unless the system relies on a logically centralized authority to issue identities, or accepts assumptions the paper calls unrealizable at scale. It defines an entity (a physical participant) as distinct from an identity (an abstract token an entity presents to others), models communication as a broadcast medium in which entities can form authenticated point-to-point channels through public-key cryptography, and asks under what conditions a local entity can tell how many distinct entities lie behind a set of presented identities. It proves four lemmas covering two validation strategies: direct validation, where a local entity issues a resource-demanding challenge (communication bandwidth, storage, or computation) to each presented identity, and indirect validation, where a local entity accepts identities vouched for by other identities it has already accepted. Each lemma proves a specific way a faulty entity multiplies its identities within that strategy.

### Measured results
No experiments were run. The paper is a set of four formal lemmas with proofs, not an implementation or a simulation. Each lemma's bound is a symbolic ratio, not a number tied to any measured system, so none of the four results below can be recorded as a measured figure; they are reproduced here as the derived relationships the proofs establish.

| Lemma | Derived relationship | Condition it holds under |
|---|---|---|
| Lemma 1 | A faulty entity commanding resources equal to rho times a minimally-capable entity's resources can present g = rho distinct identities to a validator | Validator demands proof of resources (communication, storage, or computation) before accepting an identity; entities' resource ratios are assumed bounded |
| Lemma 2 | A single faulty entity presents an unbounded number of distinct identities | The validator does not challenge all presented identities simultaneously, so a faulty entity reuses the same resources across sequential presentations |
| Lemma 3 | A colluding set F of faulty entities presents an unbounded number of distinct identities once |F| >= q or F's combined resources reach those of q+|F| minimally-capable entities | Local entity accepts any identity vouched for by q already-accepted identities (indirect validation) |
| Lemma 4 | A single minimally-capable faulty entity presents g = floor(|C|/q) distinct identities | Correct entities in set C do not coordinate the time interval during which they perform resource challenges; local entity accepts an identity vouched for by q accepted identities |

### Parameters
The paper defines no numeric defaults. It states the constants that appear symbolically in the proofs: rho (ratio of a faulty entity's resources to a minimally-capable entity's resources), q (number of vouching identities a local entity requires before indirect acceptance), and phi (fraction of all identities a system can tolerate as faulty, which Lemma 4 reduces to phi/g once amplification by g = |C|/q applies). None of rho, q, or phi is assigned a numeric value in the paper; each is left as a free parameter of the deploying system.

### Stated limitations
The paper states its computational-puzzle challenge (finding x, z such that the least-significant n bits of hash(x|y|z) are zero) is combinable: an entity holding m simultaneous puzzles y1...ym can solve them together with one combined search, so simultaneous computational challenges from multiple validators do not multiply the resource cost to the faulty entity the way the model assumes, unless each validator checks for shared partial solutions across identities it is validating. The paper states storage challenges likely cannot be satisfied simultaneously by a single faulty entity for multiple validators, because each challenger's stored bits are incompressible and occupy separate storage, but does not prove this claim, only offers an information-theoretic argument for it. The paper states that its model's excluded case, direct physical links between entities, provides a form of centrally supplied identification that the paper's impossibility result does not cover; its result therefore applies only to systems where entities communicate over a shared broadcast-style medium without physical-layer identity guarantees. The paper states an example of an implicit certification authority (CFS, relying on centrally allocated IP addresses) becoming insecure when an unrelated mechanism changes (IPv6 privacy address extensions), without proving this generalizes beyond the cited example.

### Requirements it places on the rest of the system
A system relying on this paper's direct-validation defense must issue resource-demanding challenges (communication, storage, or computation puzzles) to every presented identity concurrently, system-wide, per Lemma 2; a validator that admits identities as they arrive rather than in synchronized rounds gets no bound on Sybil identity count. A system relying on indirect validation (vouching) must set the vouch threshold q so that q exceeds the total number of faulty entities the system tolerates, per Lemma 3, and must additionally synchronize all correct entities' validation rounds, per Lemma 4, or a single faulty entity multiplies its identity count by floor(|C|/q). Any deploying system must independently bound the resource-ratio rho between the most and least capable participants it admits, since Lemma 1 ties the number of identities a faulty entity can present directly to that ratio; the paper supplies no method for measuring or enforcing this ratio in a real deployment.

### Contradicts
None found. No other paper in this batch measures or restates this paper's specific lemma bounds.

### References worth retrieving
- Rowstron, Druschel. "Storage Management and Caching in PAST, a Large-Scale, Persistent Peer-to-Peer Storage Utility." 18th SOSP, 2001 — foundational (a system this paper's threat model targets)
- Dabek, Kaashoek, Karger, Morris, Stoica. "Wide-Area Cooperative Storage with CFS." 18th SOSP, 2001 — foundational (CFS, cited as an implicit-certification example)
- Boloky, Douceur, Ely, Theimer. "Feasibility of a Serverless Distributed File System Deployed on an Existing Set of Desktop PCs." SIGMETRICS 2000 — foundational (Farsite, cited as an explicit-certification example)
- Castro, Liskov. "Practical Byzantine Fault Tolerance." 3rd OSDI, 1999 — foundational (redundancy-based fault tolerance this paper's attack undermines)
- Dingledine, Freedman, Molnar. "Accountability." In Peer-to-Peer: Harnessing the Power of Disruptive Technologies, 2001 — competing (proposes computational puzzles for accountability in P2P systems, which this paper argues is insufficient against a resourceful attacker)
- Juels, Brainard. "Client Puzzles: A Cryptographic Defense against Connection Depletion Attacks." NDSS 1999 — foundational (source of the computational-puzzle technique this paper adapts)
- Narten, Draves. "Privacy Extensions for Stateless Address Autoconfiguration in IPv6." RFC 3041, 2001 — attack/critique (cited as the mechanism that undermines CFS's implicit IP-based identity assumption)

### Verbatim extracts
"Sybil attacks are always possible except under extreme and unrealistic assumptions"
"a faulty entity f can counterfeit an arbitrarily large number of distinct identities"
"All entities must perform their resource challenges concurrently"
"apparently unrelated changes to the relied-upon mechanism can undermine the security of the system"
