## [SHI-WWW-26] Eclipse Attacks on Ethereum's Peer-to-Peer Network

**Citation:** Ruisheng Shi, Yuxuan Liang, Zijun Guo, Qin Wang, Lina Lan, Chenfeng Wang, Zhuoyi Zheng. "Eclipse Attacks on Ethereum's Peer-to-Peer Network." ACM Web Conference (WWW), 2026. DOI 10.1145/3774904.3792231.
**Retrieved:** full text via https://arxiv.org/pdf/2601.16560
**Source URL:** https://arxiv.org/abs/2601.16560
**Domain:** A

### What it does
The paper isolates an Ethereum execution-layer node from all benign peers after the node restarts, so an attacker controls every message the node sends and receives. The attack runs five stages against Ethereum's post-Merge peer-discovery stack (the discv4/discv5 Kademlia-style discovery table, the DNS-based peer list defined in EIP-1459, and libp2p-style outgoing/incoming connection slots). Stage one floods the target's discovery table with unsolicited Ping messages from attacker-controlled node records, evicting benign entries because Ethereum's discovery table applies no rate limit to incoming Ping messages. Stage two poisons the DNS-based peer list that Ethereum's official crawler publishes, by identifying the crawler's source IP from repeated log analysis and feeding it attacker node records that accumulate the crawler's maximum per-crawl score. Stage three occupies idle incoming-connection slots across the wider network before the target restarts, by running attacker nodes that continuously attempt connections to every reachable node with a free slot, so that when the target does reconnect fewer benign peers have a slot to offer. Stage four exploits the fact that a restarting node selects outgoing-connection targets by generating a random target ID and querying its own (now-poisoned) discovery table and DNS list for the closest match, so a discovery table and DNS list dominated by attacker entries causes outgoing connections to resolve to attacker nodes. Stage five races benign peers to fill the target's incoming-connection slots in the seconds after restart, using attacker nodes pre-registered as static peers so they reconnect immediately.

### Measured results

| Stage | Metric | Value | Conditions |
|---|---|---|---|
| Discovery-table filling (single round) | Attacker occupancy of discovery table | 95% occupancy within 24 hours | Sepolia testnet, 272 attacker nodes continuously pinging one target node, IP-based admission limits disabled on the target |
| Discovery-table filling (repeated rounds) | Refill time after terminating a batch | Refilled to near 100% within about 1 hour, sustained over 6 rounds at 2-hour intervals | Same Sepolia setup, 272 attacker nodes per round |
| Discovery-table filling (per-round success) | Nodes inserted per 272 attempted | 91.5%-97.4% across 6 rounds, round 1; 93.4%-97.1%, round 2 | Sepolia testnet, 10 measured rounds |
| Bucket-targeted DB filling | Last-2-bucket / last-5-bucket occupancy at 66% overall DB fill rate, without attacker ID tuning | 76% / 44% | Sepolia testnet, 257 initial benign seed nodes, attacker node IDs not adapted |
| Bucket-targeted DB filling | Last-2-bucket / last-5-bucket occupancy at 66% overall DB fill rate, with attacker ID tuning | 83% / 51% | Same setup, attacker IDs adapted to target the last 8 buckets |
| DNS list poisoning feasibility | Attacker nodes reaching maximum crawler score | 5 of 10 experiments had at least one attacker node accepted; 1 of 10 had all 5 attacker nodes reach maximum score | Controlled 2-server testbed (not the live Ethereum crawler), 5 attacker nodes against one target, 10 trials |
| DNS list poisoning, estimated time to replace X% of entries | 0%/25%/50%/75%/100% -> 54/64/100/166/538 days | Derived from measured Sepolia DNS-list score distribution (275-2,688) as of July 17, 2025, assuming an attacker gains 3 points per crawl versus 1 point per crawl for a benign node (net daily score advantage of 5 points) |
| Available incoming slots, network-wide | 80.1% of Sepolia nodes with available slots, and 62.7% of mainnet nodes with available slots, have 10 or fewer slots free | 362 Sepolia nodes and 102 mainnet nodes found to have any available slots, out of node sets drawn from the public DNS list, over a 7-hour detection window |
| Available slots occupation attack | About 90% of nodes with available slots occupied, 34 nodes left with slots | Sepolia testnet, 200 attacker nodes launched from one public server against 1,268 static nodes drawn from the official DNS list, 2-hour attack window |
| Outgoing-connection hijacking, before network-wide slot occupation | 0% DNS-list poisoning -> 0/20 (0%); 25% -> 4/20 (20%); 50% -> 8/20 (40%); 75% -> 13/20 (65%); 100% -> 19/20 (95%) | Sepolia testnet, DB filling rate fixed at 50%, 20 trials per DNS-list poisoning rate |
| Outgoing-connection hijacking, after network-wide slot occupation | At 25% DNS-list poisoning / 50% DB filling: 4/20 (20%) -> 6/20 (30%); at 50% DNS-list poisoning / 50% DB filling: 8/20 (40%) -> 19/20 (95%) | Same setup, slot occupation from the stage-three attack applied first |
| Incoming-connection hijacking, Sepolia | 30/30 (100%) success within 30 seconds of target restart | 3 target full nodes on one server, 40 attacker nodes pre-registered as static peers on a second server, 30 trials, per-IP 30-second reconnection rate limit disabled on the target |
| Incoming-connection hijacking, mainnet | 24/40 (60%) success within 2 days of restart; 18/40 (45%) within 30 seconds; 23/40 (57%) within 1 day | Same attacker setup against mainnet full nodes, 40 trials |
| Public IP addresses required, full attack chain | 304 IP addresses for Sepolia; 720 for mainnet | Derived: 208 (or 624 for mainnet) for 50% DB pre-filling, 28 for DNS-list poisoning, 28 for outgoing-connection hijacking (shared /24-subnet limit of 10 discovery-table entries per subnet), 40 for incoming-connection hijacking; stages one and three reuse IP addresses |

The abstract states that "slots hijacking raises outgoing redirection success from 45% to 95%"; the closest matching table entry (Table 4, 50% DNS-list poisoning combined with 50% database filling) shows an increase from 40% (8/20) before slot occupation to 95% (19/20) after. The two abstract-and-table figures do not exactly agree on the starting value; this entry records both because the exact correspondence is not stated in the body text.

### Parameters
- Discovery table (Kademlia-style, XOR distance): 256 buckets by leading-zero-bit count; bucket k receives a randomly generated ID with probability P_k = 1/(2^(16-k)) - 1/(2^(16-(k-1))) = 1/2^(17-k).
- Attacker nodes per discovery-table-filling round: 272 (128 per targeted bucket across the last 8 buckets, since the paper reports each round inserts 8x16=128 nodes but uses 272 as the total attack-node count in the primary experiment).
- Per-/24-subnet discovery-table admission limit: 10 IP addresses.
- Per-IP incoming-connection rate limit: rejects repeated connection attempts from the same IP within 30 seconds.
- Default incoming-connection slot count per Ethereum node: up to 34 (default), the value used to size the incoming-hijacking attack at 40 attacker nodes.
- Geth client release cadence measured from the Merge (2022-09-15) to 2025-05-05: 56 versions over 32 months, about 1.75 releases per month, each release generally forcing a node restart.
- DB growth rate on an initially empty Sepolia full node: about 200 discovery-table entries per month.
- Sepolia network size (Ethereum official statistics, 2025-05-05): about 2,000 active nodes; mainnet: about 6,000 nodes (Appendix D).

### Stated limitations
The authors did not run the DNS-list poisoning attack against the live official devp2p crawler for ethical reasons; the feasibility figures for that stage come from a controlled 2-server testbed built to imitate the crawler's scoring logic, not from an attack on the production crawler. The paper reports no defense already deployed by Ethereum; the two countermeasures given (a ping-frequency blacklist and a DNS-node reporting/blacklist threshold) are proposed, not evaluated experimentally. The disclosure section states Ethereum's security team acknowledged the report but had not released a fix at the time of writing.

### Requirements it places on the rest of the system
A discovery-table implementation that rate-limits incoming Ping messages per source (the paper's own proposed countermeasure) removes the precondition stage one depends on: an attacker's ability to send unlimited unsolicited Ping messages without being dropped. A DNS-based peer list that caps the number of distinct node records permitted per source IP address or subnet removes the precondition stage two depends on. A node that retains a fixed reserve of incoming-connection slots exempt from network-wide occupation, or that rate-limits new incoming connections per unique remote IP at the network level rather than per pairwise IP, would raise the IP-resource cost the paper measures for stage three. Any component that relies on Ethereum's discovery table or DNS peer list as an honest source of peer identity (for example, a search or replication layer built on top of the same node-discovery stack) inherits the same restart-time exposure window this paper measures, because the underlying selection mechanism (closest-ID match against a table an attacker can dominate) is not specific to Ethereum's consensus logic.

### Contradicts
None found. LI-EPRINT-25 in this batch measures a related but distinct property (discv5 network size and connectivity on the broader Ethereum network) and does not report figures directly comparable to this paper's per-stage attack-success rates.

### References worth retrieving
- Marcus, Heilman, Goldberg, "Low-resource eclipse attacks on ethereum's peer-to-peer network," Cryptology ePrint Archive, 2018 — foundational (the two-attacker-host eclipse this paper's stage one and four build on and extend past the fixes made after that disclosure)
- Henningsen, Teunis, Florian, Scheuermann, "Eclipsing ethereum peers with false friends," EuroS&PW 2019 — foundational (prior Ethereum eclipse that did not require a restart)
- Heilman, Kendler, Zohar, Goldberg, "Eclipse attacks on Bitcoin's peer-to-peer network," USENIX Security 2015 — foundational (originating eclipse-attack technique)
- Tran, Shenoi, Kang, "On the Routing-Aware peering against Network-Eclipse attacks in bitcoin," USENIX Security 2021 — competing / attack (AS-level Erebus eclipse variant)
- Heo, Woo, Yoon, Kang, Shin, "Partitioning ethereum without eclipsing it," NDSS 2023 — competing (a partitioning attack on Ethereum that does not require full eclipse)
- Shi, Peng, Lan, Ge, Liu, Wang, Wang, "Eclipse attacks on monero's peer-to-peer network," NDSS 2025 — competing (same author group's prior eclipse work on a different network, the connection-reset technique referenced in Related Work)
- Li, Zhang, Gong, "A place for everyone vs everyone in its place: Measuring and attacking the ethereum global network," Cryptology ePrint Archive, 2025 — competing / independent measurement (LI-EPRINT-25 in this corpus)
- Kim, Ma, Murali, Mason, Miller, Bailey, "Measuring ethereum network peers," IMC 2018 — foundational (peer-measurement methodology)
- Wüst, Gervais, "Ethereum eclipse attacks," ETH Zurich technical report, 2016 — foundational

### Verbatim extracts
- "requires only 28 IP addresses over 100 days" (abstract, DNS list poisoning)
- "Slots hijacking raises outgoing redirection success from 45% to 95%" (abstract)
- "over 80% of public nodes do not leave sufficient idle capacity" (abstract)
- "the DB grows at an average rate of 200 nodes per month" (line 429)
- "a node rejects repeated incoming connections from the same IP within 30 seconds" (paraphrase of §2.3 reference at line 685)
- "no final fix has been released yet" (conclusion, disclosure status)
