## [CORRIGANGIBBS-CCS-10] Dissent: Accountable Anonymous Group Messaging

**Citation:** Henry Corrigan-Gibbs, Bryan Ford. "Dissent: Accountable Anonymous Group Messaging." ACM CCS, 2010. DOI 10.1145/1866307.1866346.
**Retrieved:** full text via https://www.brynosaurus.com/pub/net/dissent-ccs.pdf
**Source URL:** https://www.brynosaurus.com/pub/net/dissent-ccs.pdf
**Domain:** G

### What it does
Dissent provides anonymous group broadcast in which every message a group member sends is unlinkable to that member, while making denial-of-service disruption by a misbehaving member traceable to that member. This combines two prior families that separately lack one property: dining-cryptographers networks (DC-nets), a construction giving unconditional anonymity through every member XORing pseudorandom bit streams together so an observer cannot determine which member's bits produced the output, which lack denial-of-service resistance because a malicious member can corrupt the shared output without being identified; and mix-networks, which route messages through relays to hide the sender but remain vulnerable to traffic analysis under sustained observation.

The protocol runs in two phases per round. First, all N group members cooperatively construct and verifiably shuffle an N-by-N matrix of pseudorandom seeds, using an accountable shuffle protocol built on Brickell and Shmatikov's anonymous data-collection protocol; each member's identity is unlinked from its position (its assigned DC-net role) in the resulting permutation. Second, the members use the seeds from the shuffled matrix to run N "pre-planned" DC-nets instances, one per member, so each DC-nets run transmits exactly the message belonging to the member whose seed occupies that slot, using the minimum number of bits required for anonymity under the paper's own attack model, including for a variable-length message.

The shuffle protocol includes a go/no-go verification phase and a blame phase: if a member detects a shuffle inconsistency, the group runs a blame phase in which faulty members are exposed with proof (a third-party-verifiable transcript showing the culprit's misbehavior) and can then be excluded from later runs. The paper proves that any group of k colluding members up to N-2 cannot match an honest member's message to its author with probability better than random guessing (following the anonymity definition of Brickell and Shmatikov), and that after any run either every honest member obtains every other honest member's message or every honest member obtains proof exposing at least one faulty member.

### Measured results

Prototype: Python implementation using OpenSSL, 1024-bit RSA-OAEP with AES-256 for public-key encryption and signing, AES-256 in counter mode as the bulk protocol's pseudorandom generator, SHA-1 as the hash function. Tested on the Emulab network emulation testbed, x86 PCs running Ubuntu 7.04 and Python 2.5, simulated star topology with every node connected to a central switch over a 5 Mbps link at 50 ms latency (giving 100 ms node-to-node latency). The prototype implements only the normal-case protocol (no secure PKI, no blame phase, no full wrapper protocol), though message signing and verification are included so measured costs reflect normal-case overhead.

| Condition | Group size | Message size | Result |
|---|---|---|---|
| Full Dissent protocol, single sender (OneSender load) | 16 nodes | 16 MB | About 31 minutes total, 3.6x longer than one node broadcasting the same data unencrypted and unanonymized to the other 15 nodes |
| Full Dissent protocol, all loads (balanced and unbalanced) | 16 nodes | large messages (up to 16 MB) | About 3.5x the time of non-anonymized TCP group messaging |
| Full Dissent protocol, varying group size, balanced load | 4 nodes | 1 MB | Under 1 minute |
| Full Dissent protocol, varying group size, balanced load | 20 nodes | 1 MB | About 4 minutes |
| Full Dissent protocol, varying group size, balanced load | 40 nodes | 1 MB | About 14 minutes |
| Startup latency (shuffle and other fixed costs) | 16 nodes | 16 MB anonymously distributed, 100 ms inter-node delay | 1.4-minute latency before bulk transfer begins |

The shuffle protocol's own runtime is constant with respect to message size and becomes negligible as total message length grows, since it operates on fixed-size descriptors independent of payload. Balance of the message load across members does not affect the full protocol's communication cost, but does affect its computation cost: when only one member sends, that member computes and combines N-1 pseudorandom streams of the message's length, while every other member computes only one such stream, producing a measurable timing difference between senders under unbalanced load, which the authors state could enable a side-channel attack if not mitigated by precomputing bit strings before a send begins (no such mitigation was analyzed in this paper). Group sizes tested for scaling ranged up to 44 nodes on simulated wide-area links; the O(N^2) shuffle scaling is stated to manifest only slightly at the small group sizes tested.

### Parameters
- Group size N: tested up to 44 nodes in the prototype; the paper's own summary figures are quoted for 4, 16, 20, and 40 nodes.
- Simulated link: 5 Mbps per node, 50 ms one-way to the switch (100 ms node-to-node), star topology via Emulab.
- Public-key cryptosystem: 1024-bit RSA-OAEP.
- Symmetric cipher: AES-256 (counter mode for the bulk protocol's pseudorandom generator).
- Hash function: SHA-1.
- Anonymity threshold: security holds against up to N-2 colluding members (all but one honest member colluding voids anonymity by definition, since one honest member alone cannot be confused with any other).

### Asymptotic complexity (shuffle protocol, Section 3.4, and bulk protocol, Section 4)
- Shuffle protocol per-node communication: O(N * L~) bits, where L~ = L + O(N) is the size of an L-bit input message after 2N iterated public-key encryptions (ciphertext expansion accounted for); total shuffle communication O(N^2 * L~).
- Shuffle protocol blame-phase communication (only on an unsuccessful run): up to O(N^3 * L~) total for all honest members to expose a faulty member; an attacker can trigger at most O(N) such runs before all faulty members are exposed and excluded.
- Shuffle protocol latency: dominated by N serial communication rounds, each requiring O(N * L~) bits per node, giving O(N^2 * L~) total transmission bit-times.
- Shuffle protocol per-node computation: dominated by 2N public-key operations on O(L~)-bit plaintexts, giving O(N * L~) per node (O(N^2 * L~) total); the blame phase adds a further O(N) factor if members must replay other members' encryptions.
- Bulk (DC-nets) protocol startup latency: O(N^3), from N nodes serially shuffling N descriptors of length O(N); data transmission is fully parallelizable, giving total bulk-protocol latency O(N^3 + L_tot) transmission bit-times, where L_tot is total message data across all members.
- Bulk protocol per-node computation: O(N^2 + N * L_tot).
- Optimality condition stated by the authors: when N is small relative to L_tot, only one member transmits, and the data is incompressible, Dissent's communication is asymptotically optimal for its attack model, because trivial traffic analysis already reveals that any member sending fewer than L_tot bits cannot be the sender.

### Stated limitations
The authors state Dissent "may not scale to large groups" and that the shuffle protocol's per-round startup delay makes it "impractical for latency-sensitive applications," restricting it to delay-tolerant use. The authors state Dissent provides only a limited form of coercion resistance (Section 5.3): the deniable-keying wrapper protects only against an attacker who requires third-party-verifiable proof of which message a member sent; it does not protect against an attacker who treats its own network traffic logs (which the paper's attack model already grants the attacker) as sufficient proof. The core protocol as analyzed assumes all members remain connected and correctly signing until a run completes (Section 2.4, assumption (d)); liveness under members going silent is deferred to a separately sketched "wrapper protocol" that is not formally defined or analyzed. If all but one member colludes, the paper states no anonymity is possible by definition, since one honest member cannot be confused with any other. The authors state they made no attempt to analyze the protocol for side-channel timing attacks arising from unbalanced-load computation-time differences. The authors state the question of whether better communication efficiency is achievable while several members transmit simultaneously, without weakening traffic-analysis resistance, is left open for future work.

### Requirements it places on the rest of the system
Every member must hold a public encryption key and a nonrepudiable signing key known to every other member before a run begins (Section 2.4); the paper's core analysis assumes this key distribution is already solved and does not itself provide key management. All N members participating in a run must remain connected and continue sending correctly signed messages until the run completes; the paper's own core protocol proof does not cover the case of members silently dropping out, and defers that liveness case to a sketched, unanalyzed wrapper. The blame phase requires every honest member to be able to replay other members' encryptions and requires nonrepudiable signatures for third-party verifiability; a deployment that wants Dissent's coercion resistance instead must add the separate deniable-keying wrapper (Section 5.3), which requires a leader to run a deniable authenticated key exchange (the paper cites SKEME) with each participant before every round, and this repudiability is stated to defend only against an attacker who needs cryptographic proof, not one who accepts its own traffic-analysis logs as sufficient evidence. A byzantine-consensus layer is needed above the shuffled-send primitive if the deploying group additionally wants reliable-broadcast semantics or consistent state across runs; the paper states this requires over two-thirds of members to remain live, but does not itself supply that consensus layer.

### Contradicts
None found within this corpus. This paper's own measured scaling (4 nodes under 1 minute, 20 nodes about 4 minutes, 40 nodes about 14 minutes, all for 1 MB) replaces any unquantified claim that DC-net coordination cost merely "grows with group size" with the specific figures above, at the stated topology (5 Mbps links, 100 ms node-to-node latency, Emulab-simulated).

### References worth retrieving
- foundational: Justin Brickell, Vitaly Shmatikov. "Efficient anonymity-preserving data collection." KDD 2006 (cited as the anonymous data-collection protocol Dissent's shuffle directly builds on; not separately numbered in this bibliography extract but referenced throughout as [7]).
- foundational: David Chaum. "The dining cryptographers problem: Unconditional sender and recipient untraceability." Journal of Cryptology, 1988 (the DC-nets construction Dissent's bulk protocol is inspired by; cited as [10] in this bibliography).
- attack: Andreas Haeberlen, Petr Kouznetsov, Peter Druschel. "PeerReview: Practical accountability for distributed systems." SOSP 2007. (accountability framework Dissent's exposure definition follows)
- competing: Michael Waidner, Birgit Pfitzmann. "The dining cryptographers in the disco: Unconditional sender and recipient untraceability with computationally secure serviceability." EUROCRYPT 1989.
- competing: Philippe Golle, Ari Juels. "Dining cryptographers revisited." EUROCRYPT 2004. (DC-net DoS-resistance strengthening the paper compares against)
- competing: Michael K. Reiter, Aviel D. Rubin. "Anonymous web transactions with crowds." Communications of the ACM, 1999.
- competing: David Goldschlag, Michael Reed, Paul Syverson. "Onion routing for anonymous and private internet connections." Communications of the ACM, 1999.
- attack: Andrei Serjantov, Roger Dingledine, Paul Syverson. "From a trickle to a flood: Active attacks on several mix types." Information Hiding, 2003.
- competing: Jun Furukawa, Kazue Sako. "An efficient scheme for proving a shuffle." CRYPTO 2001.
- competing: C. Andrew Neff. "A verifiable secret shuffle and its application to e-voting." ACM CCS 2001.
- competing: Luis von Ahn, Andrew Bortz, Nicholas J. Hopper. "k-anonymous message transmission." ACM CCS 2003.
- foundational: Eugene Vasserman, Rob Jansen, James Tyra, Nicholas Hopper, Yongdae Kim. "Membership-concealing overlay networks." ACM CCS 2009.

### Verbatim extracts
- "Dissent's shuffle protocol and other startup costs incur a 1.4-minute latency"
- "Dissent can send a 1MB message anonymously in less than 1 minute in a 4-node group"
- "4 minutes in a 20-node group, and 14 minutes in a 40-node group"
- "Dissent ran in about 31 minutes on the experimental topology, or 3.6x longer"
- "it may not scale to large groups, it provides only a limited form of coercion resistance"
- "a group of k <= N-2 colluding members cannot match an honest participant's message to its author"
