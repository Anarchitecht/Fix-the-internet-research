## [DUARTE-ABAKOS-20] Beware: NAT Traversal is a Simple and Efficient Approach to Open Firewall Holes
**Citation:** Elias P. Duarte Jr., Kleber V. Cardoso, Micael O. M. C. de Mello, João G. G. Borges. "Beware: NAT Traversal is a Simple and Efficient Approach to Open Firewall Holes." Abakós, 8(2), 2020. Pages 29-41. DOI 10.5752/p.2316-9451.2020v8n2p29-41.
**Retrieved:** full text via periodicos.pucminas.br PDF
**Source URL:** https://periodicos.pucminas.br/abakos/article/download/19643/17354
**Domain:** L

### What it does
The paper demonstrates that the same NAT (Network Address Translation) and firewall traversal technique that lets peer-to-peer applications communicate directly also lets an unauthorized server on an internal host become reachable from arbitrary Internet clients, with no firewall configuration and no special privilege, because the two outcomes share one mechanism. It builds a system with two process roles: a client that runs on the host behind NAT/firewall, and a rendezvous that runs on a host with a public, unfiltered address. A client logs in to a rendezvous over UDP, retrying login a configurable number of times; the rendezvous can redirect a client to a different rendezvous. On accepting a login, the rendezvous assigns the client an IPv6 address and the client creates a virtual TUN/TAP network interface bound to that address; from the application's point of view this interface behaves as an ordinary IPv6 interface, and traffic sent through it is carried inside UDP datagrams across the IPv4 or IPv6 Internet. The rendezvous maintains a table of active client sessions (public IPv4 endpoint, assigned IPv6 address, last-seen timestamp) and expires entries after a configurable inactivity timeout. Connectivity between two clients behind independent NATs is established with UDP hole punching, coordinated through the rendezvous, following the same connection-reversal-then-punch sequence documented in FORD-USENIX-05: each host learns the other's public and private endpoints from the rendezvous and sends UDP packets to both, opening a hole in its own NAT in the process.

### Measured results
| Metric | Result | Conditions |
|---|---|---|
| Tunnel setup delay | mean about 15 ms; none of 1,000 tests exceeded 40 ms | testbed with controllable routing and per-link delay, 1,000 tunnel-setup trials |
| RTT overhead, no added delay | direct routing 1.94 ms (std. dev. 1.15); through the NAT-traversal tunnel 2.06 ms (std. dev. 0.50) | ping/ping6, 1,000 probes of 1,400 bytes, one per second, per scenario |
| RTT overhead, fixed 50 ms added delay | direct routing 52.23 ms (std. dev. 0.49); tunneled 52.84 ms (std. dev. 0.66) | same probing method, netem-injected fixed 50 ms delay |
| RTT overhead, variable ~50 ms added delay | direct routing 53.996 ms (std. dev. 3.40); tunneled 54.05 ms (std. dev. 2.49) | same probing method, netem-injected variable delay with 50 ms mean |
| UDP throughput at 100 Mbps generation rate | direct routing 95.6 Mbps; tunneled without MTU tuning 85.7 Mbps; tunneled after MTU adjustment on the virtual interface 92.2 Mbps | Iperf generating 100 Mbps (the testbed's bottleneck throughput); each of 30 repeated 60 s runs per configuration, mean reported with a 95% confidence interval described as barely visible on the plotted curve |
| TCP throughput vs. RTT | tunneled throughput close to direct-routing throughput below 200 ms RTT; effectively no difference above 200 ms RTT, where bandwidth-delay product dominates | same 60 s × 30-run Iperf methodology, RTT varied via netem across 0-500 ms |
| Comparison against a relay-server alternative, similar-environment scenario | reversal technique 88.490 Mbps (std. dev. 0.596); relay server 89.903 Mbps (std. dev. 0.617) | Iperf TCP traffic; three-hop default path (NAT1-R1-R2-R3-NAT2) vs. an indirect relay path (NAT1-R1-RR-R3-NAT2) with similar characteristics to the default path |
| Comparison against a relay-server alternative, low-delay scenario | reversal technique 88.490 Mbps (std. dev. 0.596); relay server 86.587 Mbps (std. dev. 3.098) | default path RTT 10 ms; indirect (relay) path RTT 100 ms |
| Comparison against a relay-server alternative, high-capacity scenario | reversal technique 88.490 Mbps (std. dev. 0.596); relay server 9.282 Mbps (std. dev. 0.012) | default path bottleneck 100 Mbps; indirect (relay) path bottleneck limited to 10 Mbps |

### Parameters
| Parameter | Value | Source |
|---|---|---|
| Rendezvous session timeout | configurable; expires an inactive client session after a threshold interval | Section 3, rendezvous session-table description |
| Client login retry count | configurable number of retransmissions before giving up | Section 3 |
| Keepalive | client sends periodic UDP datagrams to the rendezvous to keep its session active | Section 3 |
| Interface type | Universal TUN/TAP driver, IPv6 address assigned by the rendezvous | Section 3 |
| Test object sizes | 1,400-byte probes for RTT; Iperf-generated streams for throughput | Section 4 |

### Stated limitations
The authors state the technique's security exposure directly rather than as a design refusal: NAT traversal and firewall hole-opening are the same mechanism, so any internal host can independently open a hole that makes an otherwise-unauthorized service reachable from the public Internet, without any change to the network's firewall configuration. Stated future work is to develop techniques that keep the connectivity functionality of NAT traversal while detecting malicious or unauthorized use of it; the paper states no such detection technique exists yet in this work.

### Requirements it places on the rest of the system
A design that relies on stateful NAT and firewall behavior to keep an internal host's unadvertised services unreachable from the public Internet cannot assume that property continues to hold once any peer-to-peer NAT-traversal client runs on a host inside the same private network: the traversal mechanism opens a bidirectional hole indistinguishable, from the firewall's perspective, from a hole opened for an authorized peer connection. A design that uses this rendezvous-plus-hole-punching pattern for connectivity needs a rendezvous host with a public, unfiltered address reachable by every client before any two clients can establish a direct session — the rendezvous is a single point of introduction, though the paper's own results show it does not become a session-relay bottleneck once the hole is open, unlike a relay-server design whose data-plane throughput degrades to the capacity of the relay path (measured at 9.28 Mbps against an 88.49 Mbps direct/reversal path in the high-capacity scenario above).

### Contradicts
None found. This is a corroborating, not competing, measurement of the connection-reversal and UDP-hole-punching mechanism documented in FORD-USENIX-05; it reports comparably low tunnel-setup and RTT overhead and does not challenge that paper's mechanism description.

### References worth retrieving
- **Foundational** — Ford, Srisuresh, Kegel. "Peer-to-peer communication across network address translators." USENIX Annual Technical Conference, 2005. — the hole-punching and connection-reversal mechanism this paper builds its traversal strategy on (already in this batch, FORD-USENIX-05).
- **Foundational** — Rosenberg. "Interactive Connectivity Establishment (ICE): A Protocol for Network Address Translator (NAT) Traversal for Offer/Answer Protocols." RFC 5245, 2010. — cited for TCP hole punching and general ICE mechanics.
- **Foundational** — Huitema. "Teredo: Tunneling IPv6 over UDP through Network Address Translations (NATs)." RFC 4380, 2006. — the paper states its own approach provides functionality similar to Teredo but works with either IPv4 or IPv6.
- **Foundational** — Mahy, Matthews, Rosenberg. "Traversal Using Relays around NAT (TURN): Relay Extensions to Session Traversal Utilities for NAT (STUN)." RFC 5766, 2010. — the relay-server alternative this paper measures against.
- **Competing** — Müller, Wohlfart, Carle. "Analysis and Topology-based Traversal of Cascaded Large Scale NATs." HotMiddlebox Workshop, 2013. — traversal specifically for multi-level/carrier-grade NAT topologies, a scenario this paper does not test.
- **Competing** — Novo. "Making Constrained Things Reachable: A Secure IP-Agnostic NAT Traversal Approach for IoT." ACM TOIT, 19(1), 2018. — the paper states this addresses resource-constrained devices unable to implement current NAT-traversal architectures, and states that a related SDN-based IoT NAT-traversal proposal (Wang et al., 2019) does not address security issues, which is exactly the exposure this paper's own contribution states.
- **Attack or critique** — Ho, C.Y. et al. "To call or to be called behind NATs is sensitive in solving direct connection problem." IEEE Communications Letters, 15(1), 2011. — bears on which endpoint should initiate the reversal request, relevant to the connection-reversal precondition this paper's mechanism relies on.

### Verbatim extracts
"mean delay to setup a tunnel is about 15 ms and none of the 1,000 tests"
"as a side effect, those techniques also freely proceed through firewalls"
"making unauthorized services easily available"
"the rendezvous does not become a bottleneck to the system"
"A relay server remains an active part of the communication"
