## [LIANG-ARXIV-24] Implementing NAT Hole Punching with QUIC

**Citation:** Jinyu Liang, Wei Xu, Taotao Wang, Qing Yang, Shengli Zhang. "Implementing NAT Hole Punching with QUIC." arXiv preprint (CoRR), 2024. DOI 10.48550/ARXIV.2408.01791.
**Retrieved:** full text via https://arxiv.org/pdf/2408.01791
**Source URL:** https://arxiv.org/abs/2408.01791
**Domain:** L

### What it does
The mechanism establishes a direct connection between two nodes that each sit behind a network address translator (NAT), without a byte of application data transiting a third party, by having both nodes send connection attempts through their own NAT toward each other's NAT-mapped address at coordinated times so each NAT records an outbound session entry that then admits the peer's inbound packet. A rendezvous relay server, reachable by both nodes, first collects each node's private and NAT-mapped public address and hands each node the other's public address. Node A sends a connection request to node B's public address; NAT-A opens a session entry for that flow, but NAT-B, having no matching entry yet, discards the packet. Node B then sends its own connection request to node A's public address; NAT-B opens a session entry for that flow, and because NAT-A already holds a session entry from the earlier A-to-B attempt, NAT-A forwards B's inbound packet to A. Both NATs now hold matching session entries and the connection completes. The paper compares this procedure run over QUIC (Quick UDP Internet Connections, a transport protocol built on UDP) against the same procedure run over TCP, and separately proposes using QUIC's connection migration mechanism, rather than repeating the hole-punching procedure, to restore a punched connection after one endpoint's address changes.

Connection migration works because QUIC identifies a connection by a Connection ID (CID) carried in every packet rather than by the underlying IP address and port. When client A's private address changes, its NAT-mapped public address also changes, so a migration request A sends directly to B is discarded by NAT-B, which has no session entry for A's new address. The relay server S is used again, but only to exchange addressing information, not to carry data: A tells S its new address and asks S to relay this to B and to ask B to send a packet toward A; B's packet toward A is discarded by NAT-A (no session entry yet) but creates a NAT-B session entry for the B-to-A direction; A then sends its connection migration request to B, which now passes NAT-B because of that session entry, and the connection resumes under the same CID with no re-handshake.

### Measured results

| Result | Conditions |
|---|---|
| QUIC hole-punching time approximately 55 ms; TCP approximately 56 ms | RTT (round-trip time) 20 ms, 0% packet loss, Docker-container testbed with two simulated LANs, Endpoint-Independent NAT mapping enforced via iptables, 100 trials per condition, average reported |
| QUIC hole-punching time approximately 213 ms and 416 ms; TCP approximately 256 ms and 505 ms | RTT 100 ms and 200 ms respectively, 0% packet loss, same testbed and trial count |
| Theoretical hole-punching time: QUIC 2 to 2.5 RTTs; TCP 2.5 to 3 RTTs | Derived from protocol handshake counts (QUIC connection setup integrated with TLS 1.3 in 1 RTT vs. TCP three-way handshake at 1.5 RTTs, plus 1 RTT for the initial address exchange with the relay), under the assumption that the two connection-establishment attempts from A and B do not arrive at the peer NAT at exactly the same instant (adds 0.5 RTT) |
| QUIC packet-loss retransmission time exceeds 200 ms; TCP retransmission time exceeds 1000 ms | 1% packet loss injected in the Docker network; QUIC retransmission timeout fixed at 200 ms per draft-ietf-quic-recovery; TCP retransmission timeout computed per RFC 6298, floored at 1 s when the raw computed value is below 1 s |
| Bandwidth (unlimited, 10 Gbps, 100 Mbps, 1 Mbps) produces minimal variation in hole-punching time for either protocol | 100 trials per bandwidth condition, same Docker testbed; explained by hole punching not transmitting large data volumes |
| Restoring a punched connection via QUIC connection migration saves 2 RTTs versus QUIC re-punching, and 3 RTTs versus TCP re-punching | Derived algebraically from the step counts of the two restoration procedures (equations for T_migrate and T_re-punching in the paper), not separately measured on the testbed; the difference equals the two RTTs re-punching needs to re-establish the A-to-S and A-to-B connections that migration skips |

### Parameters
- RTT values tested: 20 ms, 100 ms, 200 ms (three values, selected citing prior literature on typical Internet RTT).
- Packet loss rates tested: 0%, 1%, 1.5%, 2% (four values, citing a stated 1%-2% typical Internet packet loss range).
- Bandwidth conditions tested: unlimited, 10 Gbps, 100 Mbps, 1 Mbps (four values; found to not affect the result and excluded from the main 12-combination test matrix).
- Total test matrix: 3 RTT values times 4 packet-loss values = 12 combinations, 100 trials each.
- NAT mapping rule used in the testbed: Endpoint-Independent Mapping (the NAT-mapped address stays the same across different remote peers). The paper states that real NAT devices it tested against follow Address-and-Port-Dependent Mapping instead, and the controlled testbed was configured with iptables to force Endpoint-Independent Mapping so hole punching could proceed at all.
- TCP retransmission timeout formula used: RFC 6298's RTO, floored at 1 s when the computed value is below 1 s.
- QUIC retransmission timeout: fixed 200 ms, per draft-ietf-quic-recovery-16.

### Stated limitations
The testbed uses Endpoint-Independent Mapping NAT behavior deliberately, because the paper states that Address-and-Port-Dependent Mapping (the behavior it found on real NAT devices during preliminary testing) defeats the hole-punching procedure entirely by making each NAT assign a different external mapping per destination, so no result in the paper covers hole punching against that NAT behavior. The connection-migration restoration result is a closed-form time-difference derivation from step counts, not a separate testbed measurement; the paper's Section IV never reports a directly measured wall-clock time for either restoration scheme, only the algebraic RTT-count difference. The paper states a competing measurement (Seemann et al., 2022) compared QUIC and TCP hole-punching success rates and found QUIC superior, but did not measure punching-time overhead, which this paper states is exactly the gap it fills; the two papers therefore measure different quantities and neither should be read as a punching-time source for the other.

### Requirements it places on the rest of the system
A third-party relay server, reachable by both endpoints before their direct connection exists, must be available to exchange each side's NAT-mapped public address; the relay is required for connection setup and, separately, for connection-migration restoration (to re-exchange the changed address), but not for data transmission once punching succeeds. The mechanism requires the local NAT to run Endpoint-Independent Mapping; a system deploying this must either detect NAT mapping behavior first (this paper does not supply a detection method) or accept that the punching procedure fails silently for peers behind Address-and-Port-Dependent NATs. Connection migration requires the transport layer to be QUIC specifically, because the mechanism depends on QUIC's Connection ID persisting independent of network address; a TCP-based deployment cannot use this restoration path and must re-punch instead. Any timing-sensitive coordination of the two simultaneous connection attempts (from A and B) depends on the relay server's address-exchange step completing for both sides before either side times out its own NAT's temporary discard state.

### Contradicts
None found.

### References worth retrieving
- Seemann et al., "Peer-to-Peer Communication Across Network Address Translators" comparison study, ICDCSW 2022 — competing / independent measurement, cited [13] for QUIC-vs-TCP hole-punching success-rate comparison (not punching time); character-corrupted in the extracted bibliography, full citation not recoverable from this text.
- Ford, Srisuresh, Kegel, "Peer-to-peer communication across network address translators," USENIX Annual Technical Conference, 2005 — foundational, cited [5] as the origin of TCP-based hole punching.
- Biggadike, Ferullo, Wilson, et al., ACM SIGCOMM Asia Workshop, vol. 5, 2005 (STUNT paper) — foundational, cited [6] and again as [15], NAT traversal mechanism this paper's TCP baseline derives from.
- Iyengar, Swett, "QUIC Loss Detection and Congestion Control," draft-ietf-quic-recovery-16, IETF — foundational, cited [18], source of the 200 ms QUIC retransmission timeout parameter used in this paper's experiment.
- Paxson, Allman, Chu, Sargent, "Computing TCP's Retransmission Timer," RFC 6298 — foundational, cited [19], source of the TCP RTO formula used in this paper's experiment.
- Langley, Riddoch, Wilk, et al., "The QUIC transport protocol: Design and internet-scale deployment," ACM SIGCOMM 2017 — foundational, cited [9], QUIC design reference.

### Verbatim extracts
- "connection migration for connection restoration saves 2 RTTs compared to QUIC re-punching, and 3 RTTs"
- "we estimate the hole punching time to be between 2 and 2.5 RTTs for QUIC, and between 2.5 and 3 RTTs for TCP"
- "NAT devices in our current real network follow this rule" (Address and Port-Dependent Mapping)
- "bandwidth has little impact on the experimental results"
- "we conduct 100 tests for each of the 12 combinations"
