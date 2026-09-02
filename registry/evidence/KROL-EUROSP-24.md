## [KROL-EUROSP-24] DISC-NG: Robust Service Discovery in the Ethereum Global Network
**Citation:** Michał Król, Onur Ascigil, Sergi Rene, Alberto Sonnino, Matthieu Pigaglio, Ramin Sadre, Felix Lange, Etienne Rivière. "DISC-NG: Robust Service Discovery in the Ethereum Global Network." IEEE European Symposium on Security and Privacy (EuroS&P), 2024. DOI 10.1109/EUROSP60621.2024.00019.
**Retrieved:** full text via https://eprints.lancs.ac.uk/id/eprint/218598/3/main.pdf
**Source URL:** https://eprints.lancs.ac.uk/id/eprint/218598/3/main.pdf
**Domain:** A

### What it does
DISC-NG lets a node in the Ethereum Global Network (EGN — the set of decentralized services, including the Ethereum blockchain itself, that share one Kademlia-based distributed hash table, DHT, for peer discovery) find peers offering a given service, at a rate close to an undefended DHT lookup while resisting eclipse and censorship attacks a plain DHT lookup does not resist. An advertiser for service s builds an advertise table centered on the hash of s (rather than on the advertiser's own node identifier, as a normal Kademlia routing table is) and places a fixed number of ad copies (parameter K_register) into a random registrar in each bucket of that table. A discoverer builds the mirror search table and queries a bounded number of registrars per bucket (K_lookup), starting from the bucket farthest from the service hash and proceeding toward it, stopping once it has collected advertisements from a set number of distinct advertisers (F_lookup). Placement is randomized within each bucket but biased toward registrars close to the service hash, so that a popular service's ads are still reachable from far buckets — the buckets an attacker would need to control most of to build an eclipse are the largest fraction of the key space, since the farthest bucket alone covers roughly half of all possible registrar identifiers.

A registrar decides whether to admit an incoming ad using a waiting-time function rather than a fixed-size LRU (least-recently-used) or LFU (least-frequently-used) cache-replacement policy: on each registration attempt the registrar computes a waiting time from the ad cache's current occupancy, the number of ads already held for the same service, and a similarity score between the registering IP address and IP addresses already present in the cache, then returns a signed ticket recording how long the advertiser must still wait. The advertiser resubmits its ticket on a later attempt; the registrar recomputes a fresh waiting time against the ticket's accumulated wait and admits the ad once the remaining wait reaches zero. The registrar holds no per-advertiser state between requests — the ticket alone carries the accumulated wait — which the paper states denies an attacker the ability to exhaust registrar memory by abandoning in-progress registrations.

### Measured results

| Result | Conditions |
|---|---|
| DISC-NG discovers ten times more peers per time slot than DISCv5 (Ethereum's deployed discovery protocol) while reaching a similar or lower eclipse probability against a powerful attacker | Stated in the abstract; the concrete discovery-count comparison is Figures 19–20, network sizes 5,000/25,000/50,000 nodes and 100/300/600 services in the PeerSim-based simulator |
| DISC-NG reduces load on the busiest nodes by two orders of magnitude compared to vanilla DHT lookup, and eliminates the vulnerability of vanilla DHT lookup to resource-constrained attackers | Stated in the abstract, elaborated in the message-overhead measurements (Figures 17-18) comparing DISC-NG to the DHT baseline (16 closest nodes to the service-ID hash, LRU eviction) |
| Lookup eclipse rate at 20% / 33.33% / 50% Sybil (malicious) nodes: DHT baseline 21.4% / 37% / 59.7%; DHTTicket (DHT placement plus DISC-NG's admission control) 1.6% / 4.9% / 6.5%; DISCv5 0.3% / 0.3% / 0.3% up to moderate attacker fractions but rising with more resourceful attackers to 7.2% / 10.6% / 17.8% in a different plotted metric; DISC-NG stays under roughly 0.3-0.5% across the same range | Simulator, default 25,000-node network, service popularity following a Zipf distribution with exponent 1.0, target a moderately popular service with approximately 500 participating nodes, attacker identifiers uniformly distributed in the address space (worst case for the compared baselines, best case for DISC-NG per the paper's own statement), 5 attacker nodes reusing each IP address by default, malicious nodes register ads at 10 times the honest rate and return only malicious peers |
| With non-uniform Sybil placement (16 malicious nodes concentrated close to the target service ID), the DHT and DHTTicket baselines reach a 100% eclipse rate, versus 0% for DISCv5 and DISC-NG | Same simulator setup; the paper states these results are reported qualitatively, not plotted |
| Eclipse rate versus IP-pool size: DHT 39.5%/37%/37%, DHTTicket 2.8%/4.9%/11.4%, DISCv5 0.3%/0.3%/0.5%, DISC-NG 10.6%/10.6%/10.6%, for attacker IP pools of 50/5/1 IPs shared among attackers respectively — DISC-NG's worst case across this sweep stays under 0.5% per the paper's prose, meaning the 10.6% row is read from the DHTTicket line, not DISC-NG (see note below) | Same simulator setup, 33.33% malicious nodes fixed, IP-reuse pool size varied |
| PlanetLab-scale prototype: incoming/outgoing bandwidth and message counts cross-validated between a 50-server devp2p/Geth testbed (up to 1,000 nodes) and the PeerSim simulator | Testbed: 50 servers, 18-core Intel Xeon Gold 5220, 96 GB RAM, network sizes 200/500/1,000 nodes, tc-based network emulation reproducing round-trip latencies from an IPFS all-pairs latency dataset (8-91 ms, average 34 ms), each node's connection capped at 20 KB/s, 30 services with Zipf(α=1) popularity, F_lookup = 30 |
| Full ad-cache lookup: 66 µs local processing time; registration admission: 58 µs, largely independent of cache occupancy | Testbed prototype, per-request local processing time measurement (Figure 13) |
| Lookup latency remained on the order of a few hundred milliseconds across all tested network sizes | Testbed, 200/500/1,000-node configurations, cross-validated against the simulator |

Note on the IP-pool sweep: the text states DISC-NG's eclipse rate stays below 0.5% even in its worst tested configuration under increasing attacker IP diversity, and separately states DHT and DISCv5 show "significantly higher" rates that do not change much with IP count. The four percentage series printed together in the source text (39.5/37/37, 2.8/4.9/11.4, 0.3/0.3/0.5, 10.6/10.6/10.6) are not individually re-labeled by protocol in the extracted text at the point they appear; a reader needing the exact per-protocol assignment for this specific figure should consult Figure 22 in the original PDF rather than rely on this transcription's ordering.

### Parameters
| Parameter | Meaning | Default value |
|---|---|---|
| C | ad-cache capacity per registrar | 1,000 entries |
| K_register | ads placed per advertise-table bucket | 3 |
| K_lookup | parallel registrar queries per search-table bucket during lookup | 5 |
| E | ad expiry time (ad lifetime) | 15 minutes |
| F_lookup | number of distinct advertisers a discoverer tries to collect | 30 |
| F_return | maximum service-specific peers a single registrar returns per query | 10 |
| P_occ | occupancy exponent in the waiting-time formula | 10 |
| G | safety parameter scaling the influence of IP/service similarity on waiting time | 10^-7 |
| δ | registration-window during which a ticket is valid for reuse | 1 second |
| X_size | average advertisement request size | 1,000 bytes |
| m | number of buckets in the advertise/search table | 16 |
| T_max | assumed upper bound on traffic a single registrar can receive | under 1,125 (units as stated in Table 1; the paper states this is far above the reported real-world fiber speed record of about 10^14 bits per second, so it argues the bound is not restrictive in practice) |
| Simulation default network size | \|N\| | 25,000 nodes, extended up to 50,000 |
| Simulation default service count | \|S\| | 300 services |
| Service popularity distribution | Zipf exponent | 1.0 |
| Default malicious-node fraction | \|N_m\|/\|N\| | 33% |
| Default IP-reuse group size | attackers sharing one IP | 5 |

The paper states the waiting-time minimum formula as w_c = G·E / (1 − c/C)^P_occ, where c is current cache occupancy — the derivation for why larger P_occ deters cache overflow while smaller P_occ preserves usable cache space under normal traffic.

### Stated limitations
The paper's threat model assumes the underlying DHT already defends against DHT-level eclipse attacks — stated as Assumption 2, "at all times, all honest peers in the DHT overlay are connected through at least one other honest peer" — and DISC-NG's own security analysis holds only conditional on that assumption; DISC-NG defends against eclipse and censorship only at the service-discovery layer built on top of an already-uneclipsed DHT. The paper states it imposes no threshold on the fraction of malicious nodes to guarantee this discovery-layer protection, in contrast to schemes that require a bound on adversarial fraction. The paper assumes partial synchrony (bounded but unknown message-delivery delay ∆) and justifies this by citing that the Ethereum mainnet blockchain itself requires a strictly stronger synchrony assumption, so the paper is not proposing a weaker network model than what the deployment already needs. The conclusion states an explicit unsolved direction: "add Sybil identities detection mechanism" — DISC-NG does not itself detect or bound the number of Sybil identities an attacker registers, only limits their effect on ad-cache admission and placement. The paper states a single lookup query can still fail with a probability that increases with the number of malicious nodes and the diversity of attacker-controlled IP addresses, even though DISC-NG guarantees liveness across repeated queries (Theorems 2 and 3) — a discoverer needing certainty must retry, not rely on one query.

### Requirements it places on the rest of the system
DISC-NG requires an underlying Kademlia-style DHT whose own routing-table maintenance already resists eclipse attacks, and cites specific such mechanisms as preconditions rather than building one itself. It requires every advertisement to carry a verifiable digital signature — the lookup algorithm asserts `ad.hasValidSignature()` before accepting an advertisement — so a signing key-management scheme must exist elsewhere in the system. It requires partial synchrony: messages between honest nodes must be delivered within a bounded but not necessarily known delay ∆, and if the network partitions rather than delays, the paper's liveness proofs do not apply. It requires a per-node identifier space compatible with Kademlia-style bucket partitioning, since the advertise table and search table are both organized as buckets by XOR-distance-like proximity to the service hash. It requires a service-identification hash function to derive the service ID that both advertise and search tables center on. It requires no clock synchronization between advertisers and registrars, since a ticket only carries a duration to wait, not absolute timestamps — a property the design achieves rather than a requirement, worth noting for a synthesis step comparing this design's dependencies against a clock-dependent one.

### Contradicts
None found within this corpus. Note for cross-paper synthesis: the brief's own registry entry for this paper flagged the search-snippet figures "17.8%" and "59.7%" as needing their exact conditions verified from the full text before use — the full text confirms 17.8% as DISCv5's eclipse rate at the higher end of the tested attacker-fraction sweep in the figure discussed in the text (not the 0.3% headline figure reported at lower attacker fractions in Figure 21) and 59.7% as the DHT baseline's eclipse rate at 50% malicious nodes; both figures are usable now that their conditions are attached, per the table above.

### References worth retrieving
- Maymounkov, Mazières. "Kademlia: A peer-to-peer information system based on the XOR metric." IPTPS 2002. — foundational, the DHT this protocol is built on top of (already read per brief §7)
- Heilman, Kendler, Zohar, Goldberg. Eclipse attacks paper. — attack-or-critique (already in this corpus as HEILMAN-USENIXSEC-15)
- Marcus, Heilman, Goldberg. "Low-Resource Eclipse Attacks on Ethereum's Peer-to-Peer Network." — attack-or-critique, cited as one of the DHT-level eclipse-prevention mechanisms DISC-NG's Assumption 2 relies on
- Henningsen, Teunis, Florian, [fourth author cut off in extraction]. Eclipse-attack-resistance paper for the Ethereum DHT, cited alongside Marcus et al. as a precondition mechanism. — attack-or-critique / foundational precondition
- Singh, Ngan, Druschel, Wallach. "Eclipse attacks on overlay networks." — attack-or-critique, foundational for the eclipse-attack model this paper inherits
- Urdaneta, Pierre, Van Steen. "A Survey of DHT Security Techniques." — survey (already in this corpus as URDANETA-CSUR-11)
- Baumgart, Mies. "S/Kademlia." — competing/foundational Sybil-resistance mechanism cited as an alternative approach requiring proof-of-work (already read per brief §7)
- Al-Ameen, Wright. "Design and evaluation of Persea, a sybil-resistant DHT." ASIA CCS 2014. — competing, social-relations-based Sybil resistance cited as an alternative
- Bortnikov, Gurevich, Keidar, Kliot, Shraer. "Brahms: Byzantine resilient random membership sampling." — competing, cited among resilient peer-sampling systems the paper states cannot be easily adapted to Ethereum's application-specific peer-sampling need
- Sridhar, Ascigil, Keizer, Genon, [others]. Cited for the censorship-attack definition this paper's threat model uses. — foundational
- Trautwein, Raman, Tyson, Castro, [others]. IPFS/InterPlanetary File System measurement paper providing the all-pair latency dataset used for network emulation. — foundational (dataset source, not a competing mechanism)
- Rowstron, Druschel. "Pastry." — foundational DHT design, cited among prior DHT-based service-discovery approaches
- Ratnasamy, Francis, Handley, Karp, [Shenker]. "A Scalable Content-Addressable Network" (CAN). — foundational, cited among DHT-based discovery approaches
- Stoica, Morris, Liben-Nowell, Karger, [others]. "Chord." — foundational, cited among DHT-based discovery approaches
- He, Yan, Yang, Kowalczyk, [others]. "Chord4S," cited as a DHT-based service-discovery scheme that reduces (but the paper states does not eliminate) vulnerability to Sybil attacks. — competing

### Verbatim extracts
- "DISC-NG discovers ten times more peers per time slot"
- "reduces the load on the busiest nodes in the network by two orders of magnitude"
- "DISC-NG achieves ≈ 0% eclipse rate, even with a high number of malicious nodes"
- "DHT achieves the worst performance, reaching up to 59.7% eclipse rate"
- "the random approach of DISCv5 ... reaching up to 17.8% eclipse rate"
- "we assume that, at all times, all honest peers in the DHT overlay are connected through at least one other honest peer"
- "We do not impose further constraints such as a threshold on the ratio of malicious nodes"
- "add Sybil identities detection mechanism" (stated future direction)
- "DISC-NG does not require clock synchronization between advertisers and registrars"
