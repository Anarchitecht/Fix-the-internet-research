## [DIMAKIS-TIT-10] Network Coding for Distributed Storage Systems
**Citation:** Alexandros G. Dimakis, P. Brighten Godfrey, Yunnan Wu, Martin J. Wainwright, Kannan Ramchandran. "Network Coding for Distributed Storage Systems." IEEE Transactions on Information Theory, 2010. DOI 10.1109/TIT.2010.2054295.
**Retrieved:** full text via https://arxiv.org/abs/cs/0702015 (arXiv preprint cs/0702015v1, 2 Feb 2007; earlier version of the work later published as the cited 2010 IEEE Transactions on Information Theory article — see Contradicts)
**Source URL:** https://arxiv.org/abs/cs/0702015
**Domain:** C

### What it does
A regenerating code lets a distributed storage system replace a lost fragment of an erasure-coded file by downloading less data than either full-file reconstruction or standard Maximum-Distance-Separable (MDS) erasure-code repair requires. An MDS code stores a file of M bytes as n fragments of M/k bytes each, any k of which reconstruct the file; when a fragment is lost, the paper's first construction, called Optimally Maintained MDS (OMMDS), lets a replacement node ("newcomer") connect to the n−1 other surviving fragment-holders and download exactly M/k bytes total in the extreme case demonstrated (k=7, n=14: 0.27M bytes, a 73% reduction from downloading the whole file). OMMDS is proved (Proposition 2) to be the minimum bandwidth achievable by any scheme that keeps fragments at MDS size.

The paper's second and main construction, the Regenerating Code (RC), relaxes the requirement that fragments stay at MDS size. A newcomer connects to exactly k existing fragment-holders (the minimum possible) and downloads αM/k bits from each, where α is a free parameter. Theorem 1 gives the minimum feasible α (called α_c) below which reconstruction is information-theoretically impossible for any code, and shows that at α = α_c a linear network code exists — and randomized linear network coding across the storage nodes succeeds with probability approaching 1 as the finite-field size grows — that lets any k-subset of nodes reconstruct the file. This makes fragments larger than MDS fragments by a factor β_RC = k²/(k²−k+1), so a data collector reconstructing the full file downloads β_RC times the file size instead of exactly the file size.

### Measured results
| Result | Value | Conditions |
|---|---|---|
| OMMDS newcomer download vs. naive full-file download | 0.27M bytes; 73% reduction | k=7, n=14 (the k value used in the DHash++ system), newcomer connects to n−1=13 surviving nodes |
| RC newcomer download vs. naive; vs. OMMDS | 0.16M bytes; 84% less than naive, 39% less than OMMDS | k=7, newcomer connects to k=7 nodes |
| RC maintenance-bandwidth reduction vs. Hybrid (one full replica + (n,k) erasure code) | up to 25% lower bandwidth for equal availability, or more than 3 orders of magnitude lower unavailability at equal bandwidth | PlanetLab trace (527 days, 303 nodes, f=0.017 fraction failed/day, mean availability a=0.97), k=7; simulation using the analytical availability/bandwidth model of Rodrigues and Liskov (IPTPS 2005) |
| RC vs. Hybrid, larger k | benefit grows; RC better than Hybrid in every trace tested | k=14, same four traces |
| RC vs. Hybrid on the least stable trace | RC can be very slightly worse than Hybrid | Gnutella trace (2.5 days, 1,846 nodes, f=0.30/day, a=0.38), k=7 |
| Reduction in unavailability and bandwidth vs. Hybrid | 100× lower unavailability using about 58× less bandwidth for a 1 GB file | PlanetLab trace, target unavailability 0.01 |
| RC read-time overhead β_RC | 14% extra data transferred to reconstruct a file at k=7; 7.1% at k=14; 3.1% at k=32 | β_RC = k²/(k²−k+1), asymptotically approaches 1 as k grows |

The four availability traces used for the bandwidth/unavailability simulations: PlanetLab (527 days from Jan 2004, 303 nodes, f=0.017, a=0.97), Microsoft PCs (35 days from Jul 6 1999, 41,970 nodes, f=0.038, a=0.91), Skype superpeers (25 days from Sep 12 2005, 710 nodes, f=0.12, a=0.65), Gnutella (2.5 days from May 2001, 1,846 nodes, f=0.30, a=0.38). A node is considered permanently failed after a 1-day timeout with no response; f is the fraction of nodes failing permanently per day under that timeout, a is the mean fraction of non-permanently-failed nodes that are reachable at a given time.

### Parameters
- k: number of fragments needed to reconstruct the file (values tested: 7, 14, and, for the read-overhead calculation only, 32)
- n: total number of fragments (n = k·R for redundancy factor R)
- α: bits stored per fragment as a fraction of M/k; minimum feasible value α_c = (1/k) · 1/(1 − 1/k + 1/k²)
- β_RC = k²/(k²−k+1): storage/read overhead factor for Regenerating Codes relative to an MDS fragment
- β_MDS = (n−1)/(n−k): repair bandwidth overhead factor for OMMDS, approaching 1/(1−R) as k,n→∞ at fixed rate R=k/n
- f, a: per-trace permanent-failure rate and mean node availability, both derived from the four traces at a fixed 1-day failure-detection timeout
- Newcomer connects to exactly k nodes for the RC scheme (the minimum possible number, fixed by the authors to simplify the construction) and to n−1 nodes for OMMDS

### Stated limitations
The paper reports availability only, not durability, following the same restriction in the Rodrigues-Liskov methodology it compares against. Disk space used is not reported for any scheme except OMMDS, because bandwidth is treated as the more constrained wide-area resource; the paper states disk usage is proportional to bandwidth for every other scheme evaluated. The bandwidth-count model charges for permanent node failure only, not for node joins, unlike some designs it cites. The model assumes node availability is independent across nodes, an admitted simplification. The f/a estimates are stated as possibly biased: nodes returning after transient failures longer than the timeout are not reincorporated in this model (which would inflate the measured f), and uniform-random node selection in practice favors more-available, less-failure-prone nodes than the trace average, which the authors state is unlikely to affect the relative ranking of schemes but do not rule out. RC has a per-read overhead (β_RC extra bytes transferred) that can outweigh its maintenance-bandwidth savings when files are read frequently and k is small; the authors state RC is likely to be a net win specifically for archival or backup storage, where files are large and infrequently read.

### Requirements it places on the rest of the system
A newcomer generating a replacement fragment must be able to connect simultaneously to k (RC) or n−1 (OMMDS) other fragment-holders and receive coded data from each; this requires those holders to be locatable and reachable at repair time, which the paper does not itself provide (it assumes an underlying distributed storage substrate such as OceanStore, Total Recall, or DHash++ supplies node discovery). The RC construction requires linear network coding capability at storage nodes: fragments must be produced as linear combinations over a finite field, and the field must be large enough for randomized coding to succeed with high probability, which the proof states can be driven arbitrarily high by increasing field size but does not quantify a concrete field size or coding-computation cost. The system must track which k or n−1 nodes a newcomer connects to and treat all data collectors symmetrically (any k nodes suffice), which requires every fragment-holder to be able to serve fragment data on demand for repair, not only for read.

### Contradicts
The retrieved text is the 2007 arXiv preprint (cs/0702015v1), not the final 2010 IEEE Transactions on Information Theory version the registry citation names. This preprint does not use the terms "Minimum-Storage Regenerating (MSR)" or "Minimum-Bandwidth Regenerating (MBR)" anywhere in the text; it presents two named schemes, OMMDS (MDS-size fragments, higher repair bandwidth — the construction later literature calls the MSR point) and RC (fragments larger by factor β_RC, minimum bandwidth for a newcomer connecting to exactly k nodes — the construction later literature calls the MBR point), and proves a single feasibility bound (Theorem 1) rather than presenting a full storage-versus-bandwidth tradeoff curve with two labeled extremes. Any claim that this text states the MSR/MBR framework by name is not supported by the retrieved text; the framework is a later restatement of these same two constructions found in follow-on papers. No other entry in this batch disagrees with this paper's figures.

### References worth retrieving
- Rodrigues, Liskov, "High availability in DHTs: Erasure coding vs. replication," IPTPS 2005 — competing; supplies the Hybrid scheme and the evaluation methodology this paper's Section V directly extends, and its more pessimistic conclusion about erasure-code practicality is the one this paper's results are checked against
- Weatherspoon, Kubiatowicz, "Erasure coding vs. replication: a quantitative comparison," IPTPS 2002 — competing; reported an order-of-magnitude bandwidth reduction from erasure coding, a different scenario the paper cites for context
- Bhagwan, Tati, Cheng, Savage, Voelker, "Total Recall: System support for automated availability management," NSDI 2004 — foundational; one of the deployed systems whose design motivates the paper's redundancy problem
- Dabek, Kaashoek, Karger, Morris, Stoica, "Wide-area cooperative storage with CFS," ACM SOSP 2001 — foundational; a deployed erasure-coded storage system the paper cites as motivating context
- Ahlswede, Cai, Li, Yeung, "Network information flow," IEEE Trans. Info. Theory 46(4), 2000 — foundational; origin of network coding, the technique the paper applies to storage repair
- Dimakis, Prabhakaran, Ramchandran, "Ubiquitous Access to Distributed Data in Large-Scale Sensor Networks through Decentralized Erasure Codes," IPSN 2005 — foundational; the authors' own prior application of network coding to distributed storage in a sensor-network setting

### Verbatim extracts
- "Regenerating Codes can reduce maintenance bandwidth use by 25% or more compared with the best previous design"
- "if α < α_c then reconstruction at some data collector who connects to k storage nodes is information theoretically impossible"
- "RC has a small constant factor overhead compared with Ideal Erasure codes, while Hybrid has a rather large but only additive overhead"
- "the same 1 GB can be maintained with 100× lower unavailability using about 58× less bandwidth"
