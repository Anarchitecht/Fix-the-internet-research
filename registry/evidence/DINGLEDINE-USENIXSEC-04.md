## [DINGLEDINE-USENIXSEC-04] Tor: The Second-Generation Onion Router

**Citation:** Roger Dingledine, Nick Mathewson, Paul Syverson. "Tor: The Second-Generation Onion Router." USENIX Security Symposium, 2004.
**Retrieved:** full text via https://www.usenix.org/legacy/event/sec04/tech/dingledine.html
**Source URL:** https://www.usenix.org/legacy/event/sec04/tech/dingledine.html
**Domain:** G

### What it does
Tor provides low-latency anonymous communication for TCP-based applications by routing a connection through a sequence of relays (onion routers, OR) chosen by the client, so that each relay knows only its immediate predecessor and successor in the path, and no single relay observes both the client's identity and the destination. Traffic between the client and the first relay, and between each pair of relays along the path, moves in fixed-size cells of 512 bytes (payload portion 509 bytes, reported as 498 bytes of usable data once the relay-cell header is subtracted), each layer-encrypted so that every hop removes exactly one layer, analogous to peeling a layer off an onion.

A circuit is built incrementally: the client's onion proxy (OP) negotiates a symmetric key with the first relay using a Diffie-Hellman handshake, then sends a `relay extend` cell instructing that relay to negotiate a further symmetric key with the next relay, repeating one hop at a time until the full path is established. Because each hop's key is negotiated over the already-encrypted circuit rather than embedded in a single onion data structure prepared in advance (as in the first-generation Onion Routing design), a relay that is later compromised cannot decrypt previously recorded traffic from that circuit — this property is perfect forward secrecy. Multiple TCP streams are multiplexed onto one circuit rather than each stream building its own circuit, reducing the number of circuit-construction handshakes; clients build circuits preemptively in the background and default to rotating to a fresh circuit about once a minute of use. Tor uses a leaky-pipe circuit topology: in-band signaling lets the client direct a given stream's traffic to exit at any relay along the built circuit, not only the last one, so an external observer of a given relay cannot be certain whether that relay is the circuit's final exit point.

Congestion control operates at two levels using end-to-end acknowledgment cells (`relay sendme`) rather than relying on each hop's own TCP flow control, because a circuit multiplexes many TCP streams over one connection between relays and per-hop TCP semantics do not extend to circuit-level flow. At the circuit level, each relay tracks a packaging window and a delivery window (each initialized to 1000 data cells in the reported implementation); the relay sends a `sendme` cell for every 100 data cells received, and receiving a `sendme` cell increments the corresponding window by 100; if a packaging window reaches 0, the relay stops reading from the corresponding TCP stream until it receives a `sendme` cell. At the stream level, a separate packaging window starts at 500 cells and increments by 50 upon receiving a stream-level `sendme` cell. Directory servers, a small set of more-trusted nodes, publish signed lists of participating relays with their keys, bandwidth, and exit policy, giving clients a consistent view of the network without requiring a fully decentralized discovery mechanism. Location-hidden services are supported through rendezvous points: a service establishes circuits to introduction points in advance, publishes their addresses, and a client connects by building its own circuit to a rendezvous point and having both parties meet there, so neither party's network location is revealed to the other.

### Measured results

| Measurement | Conditions | Result |
|---|---|---|
| Network scale, mid-May 2004 | Deployed public Tor network | 32 relays (24 US, 8 Europe); comparable contemporary remailer network cited at about 40 nodes |
| Per-relay traffic volume | Same deployment | Roughly 800,000 relay cells per relay per week (a bit under half a gigabyte) |
| Cell payload fill, client-bound direction | Same deployment, 498-byte usable payload per cell | About 80% full on average |
| Cell payload fill, client-originated direction | Same deployment | About 40% full on average, attributed by the authors to interactive protocols (e.g. SSH) lowering the average against bulk web traffic |
| File-download latency, controlled test | 4 Tor nodes co-located on one heavily loaded 1 GHz Athlon machine; 60 MB file from debian.org fetched every 30 minutes for 54 hours (108 sample points) | Averaged about 300 seconds through Tor versus about 210 seconds for a direct download |
| Page-fetch latency, production network | Live public Tor network of 32 relays; fetching the 55 KB front page of cnn.com; direct download baseline about 0.3 s consistently | Through Tor: fastest observed 0.4 s, median 2.8 s, 90th percentile 5.3 s |
| Prior-generation deployment reference (not Tor itself) | Original Onion Routing single-machine proof-of-concept, cited as prior work | Processed connections from over 60,000 distinct IP addresses worldwide, at roughly 50,000 connections per day |

The authors state expected scaling limits for the deployed clique topology (every relay connects to every other relay) and full-visibility directories (every client holds the complete relay list): a few hundred relays and roughly 10,000 users before the design would need to become more distributed, given as an expectation rather than a measured ceiling.

### Parameters
- Cell size: 512 bytes total; payload 509 bytes at the cell-protocol level, reported as 498 bytes of usable relay-cell payload after the relay-cell header.
- Default circuit path length: at least three relays unrelated to the client and the destination (the number 3 chosen specifically so that no two colluding relays on the path can, between just the two of them, be certain they have deanonymized both the client and destination — a two-hop path would let both endpoints' adjacent relays reach that certainty by colluding).
- Circuit rotation interval: clients default to rotating to a fresh circuit about once a minute of use.
- Circuit-level congestion-control window: packaging and delivery windows each initialized to 1000 data cells; `sendme` cell sent every 100 data cells received; each `sendme` increments the corresponding window by 100.
- Stream-level congestion-control window: packaging window initialized to 500 cells; incremented by 50 per `sendme` cell received.
- Relay hardware in the controlled latency test: 1 GHz Athlon, 4 co-located nodes.
- Relay bandwidth in the deployed network (mid-May 2004): each relay reported to hold at least a 768 Kb/768 Kb connection, with many holding 10 Mb connections.

### Stated limitations
The authors explicitly place several goals out of scope (Section 3, "Non-goals"), each stated as a deliberate deferral rather than an unrecognized gap. Not peer-to-peer: Tor does not attempt to scale to a fully decentralized network of many short-lived, possibly adversary-controlled relays, unlike Tarzan and MorphMix, which the authors cite as having many open problems of their own. Not secure against end-to-end attacks: the authors state Tor does not claim to solve end-to-end timing correlation or intersection attacks, and that an adversary who observes both the client's entry point and the destination's exit point can potentially confirm a connection through traffic-pattern correlation. No protocol normalization: Tor does not filter or normalize application-layer traffic (for example, HTTP header differences that could fingerprint a client); the authors state this must be handled by a separate filtering proxy layered on top, citing Privoxy as an example. Not steganographic: Tor does not attempt to hide the fact that a given host is connected to the Tor network at all. The authors state the threat model assumed throughout the paper is an adversary who observes and controls only some fraction of network traffic and relays, explicitly not the global passive adversary that high-latency mix designs (including their own earlier Mixminion work) are analyzed against; they state a global observer's traffic-timing correlation against a low-latency system "will immediately and automatically defeat" it, and the paper does not claim otherwise. The authors state the proper circuit-rotation interval and path-length-selection policy (fixed at three hops versus a randomized length drawn from a geometric distribution) remain open questions requiring further analysis, since frequent rotation raises intersection- and predecessor-attack exposure while infrequent rotation makes a user's traffic more linkable over time. The authors state volunteer relay operators have expressed unwillingness to run constant-bandwidth padding, and no efficient link- or long-range-padding scheme against timing observation had been shown workable at the time of writing.

### Requirements it places on the rest of the system
Every relay on a circuit must correctly maintain per-circuit packaging and delivery windows and respond to `sendme` cells; a relay that does not implement this specific end-to-end congestion-control protocol breaks the flow-control assumption the rest of the circuit relies on to avoid accidental denial-of-service against volunteer-operated relays. Clients need continuous access to a directory-server-published, threshold-signed list of active relays with current keys, bandwidth, and exit policy before building any circuit; the design assumes a small set of more-trusted directory servers is reachable and that a client holds the full relay list rather than a partial view. Any application wanting protection from protocol-level identity leaks (such as HTTP header fingerprinting) needs an external filtering proxy layered in front of Tor, since Tor's own design explicitly declines to perform protocol normalization. A client that wants resistance to end-to-end timing correlation beyond what Tor itself provides must supply that separately — the paper states this class of attack is out of scope for the design as presented, so any component built on top of Tor that assumes such protection is present is building on an unmet precondition. The minimum three-hop default path assumes at least three mutually non-colluding relays are available and selectable by the client; a deployment with fewer independent relay operators than that does not meet the assumption the three-hop rationale depends on.

### Contradicts
None found within this corpus. The paper's own reported figure of 60,000 distinct IP addresses at roughly 50,000 connections per day describes the earlier, single-machine Onion Routing proof-of-concept referenced as prior work in this paper's introduction, not the Tor deployment measured in Section 8 (32 relays, roughly 800,000 relay cells per relay per week); a claim attributing the 60,000-IP figure to Tor itself is not supported by this paper.

### References worth retrieving
- foundational: D. M. Goldschlag, M. G. Reed, P. F. Syverson. "Hiding Routing Information." Information Hiding, 1996. (the first-generation Onion Routing design this paper directly supersedes)
- foundational: P. Syverson, M. Reed, D. Goldschlag. "Onion Routing access configurations." DISCEX, 2000.
- foundational: G. Danezis, R. Dingledine, N. Mathewson. "Mixminion: Design of a Type III Anonymous Remailer Protocol." IEEE S&P, 2003. (this corpus's own DANEZIS-SP-03 entry; shared authorship, contrasting high-latency global-adversary design)
- competing: M. J. Freedman, R. Morris. "Tarzan: A peer-to-peer anonymizing network layer." ACM CCS, 2002.
- competing: M. Rennhard, B. Plattner. "Practical anonymity for the masses with morphmix." Financial Cryptography, 2004.
- competing: M. K. Reiter, A. D. Rubin. "Crowds: Anonymity for web transactions." ACM TISSEC, 1998.
- attack: M. Wright, M. Adler, B. N. Levine, C. Shields. "Defending anonymous communication against passive logging attacks." IEEE S&P, 2003. (predecessor attacks, cited directly for the circuit-rotation tradeoff)
- attack: B. N. Levine, M. K. Reiter, C. Wang, M. Wright. "Timing attacks in low-latency mix systems." Financial Cryptography, 2004.
- attack: A. Hintz. "Fingerprinting websites using traffic analysis." PET, 2002.
- attack: J. Douceur. "The Sybil Attack." IPTPS, 2002.
- attack: G. Danezis. "Statistical disclosure attacks." IFIP SEC, 2003.
- foundational: S. Goel, M. Robson, M. Polte, E. G. Sirer. "Herbivore: A scalable and efficient protocol for anonymous communication." (already in corpus as GOEL-CORNELLTR-03, currently flagged as a mismatched source file in this evidence set and needing re-retrieval)

### Verbatim extracts
- "we still expect the network to support a few hundred nodes and maybe 10,000 users"
- "Alice always chooses at least three nodes unrelated to herself and her destination"
- "It arrived in about 300 seconds on average, compared to 210s for a direct download"
- "median at 2.8s, and 90% finishing within 5.3s"
- "like all practical low-latency systems, Tor does not protect against such a strong adversary"
- "Tor does not claim to completely solve end-to-end timing or intersection attacks"
