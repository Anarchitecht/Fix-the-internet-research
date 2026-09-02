## [ZHANG-INFOCOM-05] CoolStreaming/DONet: A Data-Driven Overlay Network for Efficient Live Media Streaming
**Citation:** Xinyan Zhang, Jiangchuan Liu, Bo Li, Tak-Shing Peter Yum. "CoolStreaming/DONet: A Data-Driven Overlay Network for Efficient Live Media Streaming." IEEE INFOCOM, 2005. DOI 10.1109/INFCOM.2005.1498486.
**Retrieved:** full text via https://www.cs.sfu.ca/~jcliu/Papers/CoolStreaming.pdf
**Source URL:** https://www.cs.sfu.ca/~jcliu/Papers/CoolStreaming.pdf
**Domain:** K

### What it does
DONet (Data-driven Overlay Network) distributes a live video stream to many peers without building or repairing a fixed relay tree. Each node holds a sliding-window buffer of stream segments and periodically exchanges a Buffer Map (BM) with a set of partner nodes — a bitmap recording which segments in the current window the node already holds. Given the BMs of its partners, a node schedules which segment to pull from which partner. A node is receiver, supplier, or both for a given segment depending only on that segment's current availability among its partners; there is no fixed upstream/downstream role and no tree structure to rebuild when a partner leaves.

Three modules run at each node. The membership manager keeps a partial view of other overlay nodes (the membership cache, mCache) populated through a gossip protocol (SCAM, cited from Ganesh, Kermarrec, Massoulie 2003) that periodically distributes 4-tuples of (sequence number, node id, current partner count, time-to-live). The partnership manager establishes and maintains partner connections; a new node joins by contacting the origin node, which redirects it to a random deputy drawn from the deputy's own mCache, and the new node then contacts partner candidates supplied by the deputy. The scheduler solves a per-round assignment: for each segment a node still needs, it counts how many current partners hold that segment (the potential-supplier count), processes segments in ascending order of that count (segments with only one potential supplier are assigned first, since they are most likely to miss their playback deadline), and for segments with multiple candidate suppliers picks the partner offering the highest bandwidth with enough available time before the segment's deadline. The scheduling algorithm's time complexity is bounded by O(W times B times M), where W is the sliding-window size in segments, B is the number of partners' buffer maps considered, and M is the number of partners.

NAT traversal: a node behind NAT is not restricted to a receiver-only role. A TCP connection to a partnership is used instead of UDP; because the TCP connection is bidirectional once established, either side can push or pull data across it even when one side is behind NAT, so a NATted node can still relay to a partner that opened the connection to it.

### Measured results
| Result | Conditions |
|---|---|
| Control overhead under 2% of total (video) traffic even with 5-6 partners; roughly 1% at the adopted M=4 | PlanetLab testbed, 10 to 200 nodes, streaming rate 500 Kbps, 1-second segments, 60-segment sliding window, stable environment (nodes join within ~1 min, persist for 120 min) |
| Control overhead per node is essentially independent of overlay size | Same PlanetLab runs, 10 to 200 nodes; overhead attributed to purely local BM exchange |
| Continuity index (fraction of segments arriving by their playback deadline) improves with M up to about 4 partners; improvement beyond M=4 is marginal | Same stable-environment PlanetLab runs, M swept 2 to 6, streaming rate swept 100-500 Kbps at overlay size 200 nodes |
| Under churn (ON/OFF sojourn model, exponential with mean T), control overhead rises only slightly as T shortens; continuity index degrades only slightly even at T under 1 minute | PlanetLab, 10-200 nodes, T swept over roughly 1-800 s |
| DONet achieves better average overlay hop-count than a degree-matched tree overlay (tree internal-node fan-out capped at 3, root at 4, so total node degree 4 to match a DONet node's M=4) | PlanetLab, 50 and 200 nodes, ON/OFF period T swept 50-800 s |
| DONet continuity index is markedly higher than the tree overlay's, especially at larger overlay size and shorter ON/OFF periods; example: tree continuity index dropped by about 0.4 in one observed 100 s window following the departure of a child of the root | Same PlanetLab tree-vs-DONet comparison, 200-node case sampled continuously over a 20-minute window |
| Analytical (not measured) expected fraction of nodes suffering discontinuity is higher for the tree than for DONet across swept overlay size (500-5000 nodes) and swept node-failure probability Pf (0-0.1), at M=4, Po=0.1, Ps=0.5, segment rate R=0.001, recovery window delta-t=10 | Closed-form model (equations 9-10 in the paper), not an experimental run; a sample tree snapshot of 231 nodes with degree cap 3 had height 19 versus 5 for a balanced tree of the same size, illustrating why the tree model is pessimistic for DONet's comparison |
| CoolStreaming v0.9 (public Internet deployment, not PlanetLab): over 30,000 distinct users total, up to 4,000 simultaneous at peak; continuity index stayed above 0.95 most of the time in a sampled broadcast on a specific date; continuity index observed to improve as the number of simultaneous users grew | Real Internet deployment, no controlled topology; 2,000-line Python implementation |
| About 30% of CoolStreaming users were behind NAT; after the bidirectional-TCP-connection fix, over 95% of nodes were able to act as relaying nodes | Same CoolStreaming v0.9 deployment logs |
| DONet reachability model: for a 500-node overlay with M=4 (partner count), about 95% of nodes are reachable within 6 hops | Closed-form coverage-ratio formula, not a live measurement |

### Parameters
- M, number of partners per node: swept 2-6; M=4 adopted as the practical default after that sweep (control overhead vs. continuity-index tradeoff).
- Segment length: 1 second of stream per segment.
- Sliding window: 60 segments (60 seconds) in the PlanetLab evaluation; a 120-segment (120-bit) buffer map is described as the value used in the prototype/CoolStreaming implementation.
- Playback delay: playback begins 10 seconds after the first segment arrives.
- Streaming rate: 500 Kbps default in the stable-environment tests; swept 100-500 Kbps in the continuity-vs-rate test.
- Overlay size: swept 10, 50, 100, 150, 200 nodes in PlanetLab tests; up to 5,000 nodes in the analytical comparison.
- Churn model: exponential ON and OFF sojourn periods, mean T, swept from roughly 1 s to 800 s.
- Scheduling heuristic execution time: about 15 ms per invocation in the implementation (no swept range given).
- Membership message tuple: (sequence number, node id, partner count, time-to-live); mCache entry additionally stores last-update time.

### Stated limitations
The scheduling problem (assigning segments to suppliers under deadline and bandwidth constraints) is a variant of parallel-machine scheduling, stated by the authors to be NP-hard; DONet uses a fast heuristic rather than an optimal solver. The paper's analytical discontinuity comparison (equations 9-10) is stated by the authors to overestimate DONet's discontinuity rate, because it ignores the possibility that multiple active partners collaboratively serve a node. VCR-like functions (fast-forward, rewind, random seek) were not implemented at the time of writing; the authors state only that the buffer-map mechanism should make adding them easier than in a structured overlay, without demonstrating it. The authors explicitly disclaim solving copyright/content-authorization issues for commercial providers. PlanetLab-node geographic distribution is skewed toward North America and Europe, so the deployment's diversity of network paths is stated as unrepresentative of the wider Internet. The authors state they do not yet know whether an optimal overlay size exists; the observed trend (larger overlay, better continuity) is reported as unexplained and under continuing investigation at the time of writing.

### Requirements it places on the rest of the system
Every node needs a stable, addressable identifier (the paper uses IP address) usable for the lifetime of the join process, and needs a persistently reachable origin node whose address is known in advance to bootstrap new joins. Buffer-map exchange assumes bounded and roughly known clock/segment-lag skew across nodes: the sliding-window size (120 segments in the prototype) is chosen on the basis of an observed inter-node lag of under 1 minute, so a system with larger lag needs a correspondingly larger window or the buffer map stops covering the segments a partner might actually want. The scheduler needs each partner to report accurate, current buffer-map and bandwidth information; the paper does not evaluate behavior under partners that misreport buffer contents or bandwidth. NAT traversal as implemented needs at least one side of a partnership to be non-NATted so a bidirectional TCP connection can be opened; a partnership between two NATted nodes has no described solution in this paper. The gossip-based membership protocol (SCAM) needs periodic message exchange to keep mCache entries fresh; entries expire and are dropped once their time-to-live is exhausted, so any component relying on live overlay membership must tolerate mCache staleness on the order of the gossip period.

### Contradicts
None found within this corpus. The paper's own result that DONet (unstructured, data-driven) achieves *better* end-to-end hop-count and much better continuity than a comparably-constrained tree overlay runs against the general intuition, stated by the authors themselves, "that a tree achieves shorter delay" — the paper's measured result contradicts that general belief, not another paper in this corpus.

### References worth retrieving
- foundational: A. J. Ganesh, A.-M. Kermarrec, L. Massoulie, "Peer-to-peer membership management for gossip-based protocols" (SCAM), IEEE Transactions on Computers 52(2), 2003 — the gossip membership protocol DONet depends on.
- competing: M. Castro, P. Druschel, A.-M. Kermarrec, A. Nandi, A. Rowstron, A. Singh, "SplitStream: high-bandwidth multicast in cooperative environments," ACM SOSP 2003 — tree-based (multiple-tree) multicast alternative.
- competing: D. Kostic, A. Rodriguez, J. Albrecht, A. Vahdat, "Bullet: high bandwidth data dissemination using an overlay mesh," ACM SOSP 2003 — a competing mesh-based dissemination design.
- competing: Y.-H. Chu, S. G. Rao, H. Zhang, "A case for end system multicast," ACM SIGMETRICS 2000 — foundational tree-based application-layer multicast (Narada line).
- competing: M. Hefeeda, A. Habib, B. Botev, D. Xu, B. Bhargava, "PROMISE: peer-to-peer media streaming using CollectCast," ACM Multimedia 2003 — competing P2P streaming system.
- competing: R. Rejaie, A. Ortega, "PALS: peer to peer adaptive layered streaming," NOSSDAV 2003 — competing layered-streaming design.

### Verbatim extracts
"every node periodically exchanges data availability information with a set of partners"
"the larger the overlay size, the better the streaming quality it can deliver"
"M=4 is a good practical choice, which is adopted in the following experiments"
"our results show that, under both stable and dynamic environments, the delay measures of the tree-based overlay are slightly worse"
"around 30% CoolStreaming users are behind NAT"
"more than 95% of the nodes can become relaying nodes with this solution"
"We have not implemented VCR-like functions as yet."
"We do not claim that our current scheme totally solves the issues of providing copyright-protected contents."
