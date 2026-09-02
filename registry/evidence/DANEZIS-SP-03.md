## [DANEZIS-SP-03] Mixminion: Design of a Type III Anonymous Remailer Protocol

**Citation:** George Danezis, Roger Dingledine, Nick Mathewson. "Mixminion: Design of a Type III Anonymous Remailer Protocol." IEEE Symposium on Security and Privacy, 2003. DOI 10.1109/SECPRI.2003.1199323.
**Retrieved:** full text via https://www.freehaven.net/anonbib/cache/minion-design.pdf
**Source URL:** https://www.freehaven.net/anonbib/cache/minion-design.pdf
**Domain:** G

### What it does
Mixminion delivers message-based anonymous email so that a well-funded adversary observing the whole network cannot link a sender to a receiver, even when that adversary generates, modifies, deletes, or delays traffic, and operates or compromises some mixes (relay nodes that hold and reorder messages) in the network. It replaces the previous deployed system, Mixmaster, by adding secure single-use reply blocks (SURBs) so a recipient can reply anonymously to a message without revealing an identity, while making reply messages indistinguishable from forward messages to every relay, including the exit relay, so both message types share the same anonymity set (the group of possible senders or recipients an observer cannot distinguish between).

Each message is routed through a free-route mix-net (a network topology in which the sender chooses an arbitrary sequence of relays, as opposed to a fixed cascade): the sender layers encryption so each relay can decrypt only its own layer, learn only the next relay's address, and cannot determine the message's total path length (up to 32 hops) or its own position in that path. The header is split into a main header and, for two-leg routes (used for replies and for forward messages built from a SURB), a secondary header; each header holds up to 16 subheaders (one per hop for that leg), giving a maximum of 32 hops split across two legs of at most 16 each. A "swap" operation at the crossover point between the two legs exchanges the header and payload roles cryptographically so that even a relay at the crossover point cannot tell whether it is processing a forward message or a reply. Message tagging (an attacker flipping bits in a ciphertext to mark it and later recognize the corresponding output) is resisted because the header and payload are cryptographically interdependent in a structure the authors compare to a Luby-Rackoff construction, so a modified header is detected immediately via checksums and a modified payload becomes unrecoverable garbage rather than a recognizably altered payload.

To resist blending attacks (an adversary manipulating which messages enter a relay's processing batch so the only unknown message is the one being traced) and timing correlation by a global observer, each relay uses a timed dynamic-pool batching strategy adapted from Mixmaster: incoming messages enter a pool; the relay fires every t seconds only if the pool holds at least a threshold number of messages; on firing, it delivers a fixed fraction of the pool's messages chosen at random (the paper's example: 60%). Because the fraction released is constant regardless of the incoming rate, an adversary cannot flush the pool in a single round, and is forced to spend multiple firing rounds — each independently detectable by other relays via a TLS heartbeat — to isolate a target message. Mix-to-mix dummy messages (extra traffic with no real payload, injected between relays and traveling a number of hops chosen uniformly between 1 and 4) are added at every firing round from a geometric distribution to further prevent an adversary from being certain it has isolated the real target once the pool empties of known messages. The design explicitly does not send dummy traffic to or from end users, because a relay would need to know every user in the system to make user-directed dummies indistinguishable from real messages, and the authors state no practical construction for that was known at the time of writing.

A set of directory servers distributes public keys and performance statistics for participating relays; clients trust a threshold of these servers to remain honest and to jointly sign identical directory listings.

### Measured results
The paper is a design paper rather than an experimental evaluation; it reports a single throughput figure from a working implementation rather than a systematic benchmark across topologies or adversary strengths.

| Measurement | Conditions | Result |
|---|---|---|
| Message-processing throughput | Single implementation instance, 1 GHz Athlon CPU, 2048-bit RSA keys used for per-hop decryption | 800 KB of messages processed per second |

No node-count, topology, or multi-relay deployment measurements are reported in this paper; it does not measure end-to-end latency, anonymity-set size, or attack success rate against a deployed or simulated network.

### Parameters
- Header/payload sizes: main header 2 KB, secondary header (for two-leg routes) 2 KB, payload 28 KB.
- Maximum subheaders per header: 16, giving a maximum total path length of 32 hops when both legs are used.
- Default path length used by the design: 4 hops per leg, except the second leg of a forward message (built from a SURB), which uses only 2 hops.
- Batching: relay fires every t seconds (value not numerically fixed in the paper — left as a tunable batching-strategy parameter), only if the pool holds at least a threshold number of messages (threshold not numerically fixed in the paper), releasing a constant fraction of the pool each firing (example given: 60%).
- Mix-to-mix dummy traffic: number of dummies per firing drawn from a geometric distribution (rate not numerically fixed); each dummy's hop count drawn uniformly between 1 and 4 hops.
- Directory update interval: nightly, with clients pulling updates as soon as possible after release.
- Cipher key size used in the reported throughput measurement: 2048-bit RSA.

### Stated limitations
The authors state a complete solution to the intersection attack (an adversary correlating which senders are active across multiple observation windows to narrow the anonymity set) "remains an open problem," and their dynamic-pool batching only increases its cost, not eliminates it. The design provides location anonymity, not data anonymity: the authors state users are responsible for ensuring message content itself does not reveal identity, and cite prior work documenting that such textual-analysis attacks are practical. Reply messages can still be distinguished from unencrypted plaintext forward messages specifically at exit relays, because replies exit as encrypted data and plaintext forward messages do not; the authors state this residual distinguishability is "unsettling" and leave finding a further mitigation as future work. The paper explicitly declines to incorporate dummy traffic to or from end users "until their effects on anonymity are better understood," despite having a design flexible enough to support it, because the authors state they have "not yet seen any convincing analysis" of dummy-traffic efficacy. The authors state stronger protection against message-delaying and traffic-partitioning attacks (Section 5.4) would require a synchronous batching approach with per-hop deadlines, at the stated cost of greater network synchronization overhead and reduced flexibility for individual relay operators — a tradeoff the design as presented does not take. The authors state they need a strategy, not yet designed, to fragment and reconstruct messages larger than the fixed 28 KB payload size, including whether to use retransmission or forward error correction on loss.

### Requirements it places on the rest of the system
The client must obtain relay public keys and per-relay performance/reliability statistics from a directory-server infrastructure before constructing any path; the design assumes a threshold of directory servers remains honest and requires clients to hold the entire directory rather than a partial view, to prevent an adversary from exploiting differences in client directory knowledge. Anonymity against the stated global passive adversary requires every relay on a message's path to implement the same timed dynamic-pool batching and dummy policy; a relay that instead forwards immediately on receipt reintroduces the timing-correlation vulnerability the batching strategy exists to close. The design assumes link encryption (TLS over TCP) between relays with ephemeral keys, needed for forward anonymity (protection of past traffic if a relay's long-term key is later compromised); a transport that cannot supply per-link ephemeral key exchange does not give this property. Because the maximum path length is capped by the fixed header format at 16 subheaders per leg (32 hops total across two legs), any component that increases the number of relays a message must traverse beyond that bound cannot be layered onto this header format without a redesign of the subheader count. The batching and dummy-traffic mechanisms require every relay to independently choose its own random release fraction and dummy schedule; the paper does not specify a coordination mechanism between relays and states this is intentional, to preserve mix-operator flexibility.

### Contradicts
None found within this corpus.

### References worth retrieving
- foundational: D. Chaum. "Untraceable electronic mail, return addresses, and digital pseudonyms." Communications of the ACM, 1981. (the original anonymous-remailer concept this design descends from)
- foundational: U. Möller, L. Cottrell. "Mixmaster Protocol — Version 2." (the predecessor deployed system Mixminion replaces)
- foundational: C. Gülcü, G. Tsudik. "Mixing E-mail with Babel." NDSS, 1996. (prior reusable-reply-block design Mixminion explicitly rejects in favor of single-use reply blocks)
- attack: A. Serjantov, R. Dingledine, P. Syverson. "From a trickle to a flood: Active attacks on several mix types." Information Hiding, 2003. (source of the blending-attack analysis this design's batching strategy directly answers)
- attack: A. Back, U. Möller, A. Stiglic. "Traffic analysis attacks and trade-offs in anonymity providing systems." Information Hiding, 2001.
- attack: O. Berthold, H. Langos. "Dummy traffic against long term intersection attacks." PET, 2002.
- attack: D. Kesdogan, M. Egner, T. Büschkes. "Stop-and-go MIXes: Providing probabilistic anonymity in an open system." Information Hiding, 1998.
- competing: P. Syverson, M. Reed, D. Goldschlag. "Onion Routing access configurations." DISCEX, 2000. (the low-latency alternative family this paper explicitly contrasts with its own high-latency, global-adversary threat model)
- attack: B. Pfitzmann, A. Pfitzmann. "How to break the direct RSA-implementation of MIXes." EUROCRYPT, 1989.
- attack: J. R. Rao, P. Rohatgi. "Can pseudonymity really guarantee privacy?" USENIX Security, 2000. (cited as evidence that textual-analysis attacks against message content are practical)

### Verbatim extracts
- "even intermediary nodes are not aware of the actual route length (which can be as long as 32 hops)"
- "we use a path length of 4 hops per leg, but with only 2 hops in the second leg"
- "800KB of messages per second on a 1GHz Athlon"
- "a complete solution remains an open problem"
- "Mixminion provides location anonymity, not data anonymity"
- "we plan to leave dummies out of the design ... until their effects on anonymity are better understood"
