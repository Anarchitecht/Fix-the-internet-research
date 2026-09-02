## [BHAGWAN-NSDI-04] Total Recall: System Support for Automated Availability Management

**Citation:** Ranjita Bhagwan, Kiran Tati, Yu-Chung Cheng, Stefan Savage, Geoffrey M. Voelker. "Total Recall: System Support for Automated Availability Management." USENIX Symposium on Networked Systems Design and Implementation (NSDI), 2004.
**Retrieved:** full text via https://www.usenix.org/conference/nsdi-04/total-recall-system-support-automated-availability-management
**Source URL:** https://www.usenix.org/conference/nsdi-04/total-recall-system-support-automated-availability-management
**Domain:** C

### What it does

TotalRecall delivers a storage system in which a user states a target file availability (a probability the file can be read at any instant) and the system automatically picks the redundancy level and repair timing needed to meet it, instead of a system administrator statically fixing a replica count. It measures each host's short-term availability by periodic probing, uses that measured distribution to compute the redundancy a file needs to meet its target instantaneous availability, and separately tracks long-term host departures to decide when to spend bandwidth regenerating lost redundancy.

The redundancy calculation has a closed form for two encodings. For pure replication, given target availability `a` and measured mean host availability `p`, the required replica count `c` solves `a = 1 - (1-p)^c`. For erasure coding with `m` blocks per file and stretch factor `s` (storage overhead multiplier), the delivered availability is the probability that at least `m` of the `sm` coded blocks are present, computed from the binomial distribution and approximated with the normal distribution when `m` is moderately large. At availability target 0.999 and mean host availability 0.5, the paper's own worked example gives 10 full replicas for pure replication against a storage overhead of 2.49 for erasure coding — an order-of-magnitude difference in storage cost between the two mechanisms for the same target.

Repair follows one of two policies. Eager repair reacts to every host departure immediately, replacing lost redundancy the moment a host leaves, at low storage overhead (the redundancy factor needed only covers instantaneous availability) but at bandwidth cost proportional to churn, because it cannot distinguish a transient disconnection from a permanent departure. Lazy repair instead holds extra redundancy (a "long-term redundancy factor" above the short-term repair threshold) and defers repair until measured available redundancy for a file drops below the repair threshold, at the cost of tracking explicit per-file metadata about which hosts hold which blocks — a requirement eager repair avoids because it can rely on the implicit host-to-data mapping of consistent hashing. The prototype's default policy assigns eager repair and replication to files under 32 KB and lazy repair with erasure coding to larger files, using a repair threshold of 2 and a long-term redundancy factor of 4.

The system is built as a distributed hash table (DHT)-based storage manager (TRSM) on top of a modified Chord DHT and the SFS toolkit, with an NFSv3 (Network File System version 3)-compatible file system layer (TRFS) that translates file system calls into TRSM read/write/repair operations through a user-level loopback NFS server.

### Measured results

| Result | Conditions |
|---|---|
| Repair threshold of 2 (from redundancy Equation 4 at mean host availability 0.65, target 0.99) meets and exceeds a 0.99 delivered file availability target | trace-driven simulation, File Sharing workload (5,500 files, sizes per Table 1), File Sharing host availability trace (scaled-down Overnet trace), long-term redundancy factor fixed at 4, delivered availability = ratio of completed periodic reads to total read attempts |
| Average system repair bandwidth over the full trace: 35.6 MB/s total, 6.5 KB/s per file | same File Sharing simulation; number of available hosts fluctuates between roughly 800 and 1,000 over the 7-day trace |
| Bandwidth breakdown by repair type: 0.6% for eager repair of inodes, 99.4% for lazy repair of data blocks | same File Sharing simulation run |
| Eager repair produces the highest per-host bandwidth of the five policies tested; increasing long-term redundancy factor from 4 to 6, 8, and 10 progressively lowers bandwidth | trace-driven simulation, File Sharing workload and host trace, 5 policies compared: eager, and lazy at redundancy factors 4/6/8/10 |
| At long-term redundancy factor 10 and target availability 0.99 (repair threshold 2 for erasure coding, versus 5 replicas needed for pure replication at the same target), average bandwidth per host: 655 bytes/s for lazy erasure-coded repair versus 75 KB/s for lazy replicated repair | same simulator, File Sharing workload and host trace, redundancy factor 10 fixed for both policies |
| File System host availability trace (average host uptime 109 hours) produces less bandwidth usage than File Sharing trace (average host uptime 28.6 hours) for the same repair policies | trace-driven simulation comparing the two host availability traces under identical repair policies |
| For the File Sharing workload, eager repair uses less bandwidth than lazy repair for files under approximately 4 KB; lazy repair uses less for all larger files; no such crossover appears for the File System workload | per-file bandwidth measurement across a range of file sizes, both host traces, eager vs. lazy repair |
| Hybrid policy (eager for files <4 KB, lazy otherwise) shows very little bandwidth difference from pure lazy repair on the same host trace | same simulation setup, File System workload on both host traces |
| TotalRecall's bandwidth usage is close to an order of magnitude above an oracle-optimal system: 49 KB/s average for TotalRecall versus 7 KB/s for the optimal system that repairs a file exactly when its redundancy first drops below availability (redundancy = 1) | simulation, long-term redundancy factor 4 for both TotalRecall (repair threshold 2) and the optimal variant |
| Modified Andrew Benchmark total execution time: 392 seconds | prototype (TRFS) deployment, 32 PlanetLab hosts distributed across the U.S., one local client machine mounting via NFS loopback; compared against a cited prior result of 376 seconds for the Ivy peer-to-peer file system on 4 Internet hosts running the same benchmark |
| 25% of the 32 PlanetLab nodes had RPC (remote procedure call) latency over 100 ms; 87% of the time spent writing a 4 KB file (Figure 11) was spent in Chord lookups and block transfers | same 32-node PlanetLab prototype deployment |

### Parameters

| Parameter | Value used |
|---|---|
| Simulated file population | 5,500 hosts, 5,500 files, 32 blocks per file before encoding |
| File Sharing file sizes (Table 1) | 4 MB (50%), 10 MB (30%), 750 MB (20%) |
| File System file sizes (Table 1) | 256 B (10%), 2 KB (30%), 4 KB (10%), 16 KB (20%), 128 KB (20%), 1 MB (10%) |
| Host availability trace length | 1 week, both File Sharing and File System traces |
| File Sharing trace average host uptime | 28.6 hours |
| File System trace average host uptime | 109 hours |
| Repair threshold (prototype default) | 2 |
| Long-term redundancy factor (prototype default, lazy repair) | 4 |
| Eager/lazy file-size cutoff (prototype default) | 32 KB |
| Lazy-repair block fragmentation | minimum 32 blocks per file, maximum block size 64 KB |
| Erasure code used | Maymounkov's online codes, a sub-optimal linear-time erasure-coding algorithm |
| Availability-monitor probe interval | 60 seconds |
| PlanetLab prototype deployment size | 32 hosts |
| Prototype code size | over 5,700 semicolon-terminated lines of new C++ |

### Stated limitations

The redundancy analysis assumes host failures are statistically independent over short time scales; the paper states this in Section 3.2 and cites its own prior work as experimental support for the assumption, meaning TotalRecall is explicitly stated not to be designed to survive catastrophic or correlated failures (widespread network outages, coordinated attacks) but only "localized outages, software crashes, disk failures and user dynamics." The consistency mechanism for inode replicas assumes no network partitions and assumes the underlying DHT provides consistent routing (lookups for the same identifier from different hosts return the same result); the paper states this as a current assumption, not a proven property. Some advanced policy-module behavior — choosing redundancy mechanism and repair policy by criteria other than a fixed file-size cutoff — is stated as remaining future work; the prototype's policy choice is solely file-size-based. The 60-second periodic-probing approach to availability monitoring is stated as sufficient only for the PlanetLab-scale experiments in this paper and would require a more scalable mechanism, such as random subsets, for larger deployments — the paper does not measure that scalable alternative itself. The oracle-comparison experiment shows TotalRecall's bandwidth use is roughly an order of magnitude above the theoretical minimum, attributed to prediction error given system dynamics and to TotalRecall's deliberately conservative repair-triggering choice, which the paper states as an accepted design tradeoff to guarantee availability rather than as a defect to be closed. The prototype's absolute I/O performance is stated as unoptimized and not a focus of the work; the paper attributes a large share of measured latency to underlying Chord lookup and network variance rather than to the availability-management logic itself.

### Requirements it places on the rest of the system

The redundancy calculation (Equations 1-5) requires a measured, current, empirical distribution of host availability specific to the deployment population; the paper explicitly rejects using a single assumed mean-time-to-failure figure because host populations are heterogeneous and must be measured, not assumed. Lazy repair requires the storage layer to maintain explicit per-file metadata recording which hosts hold which blocks or replicas, in contrast to eager repair, which can rely on an implicit consistent-hashing placement rule and needs no such metadata — a system choosing lazy repair for bandwidth efficiency inherits this metadata-maintenance requirement. The inode-consistency mechanism requires the underlying DHT to provide consistent routing (identical lookup results for the same key from any requesting host) and requires the absence of network partitions during a write; a partition-tolerant DHT layer beneath TotalRecall would violate this assumption and the paper does not describe a fallback. The independence assumption behind the redundancy formulas requires that the set of hosts holding a given file's replicas or blocks not share a common failure cause; any placement policy that correlates replica location with a shared point of failure (same subnet, same power source, same administrative domain) invalidates the formulas' input without the system detecting the violation.

### Contradicts

None found within this batch. The paper's own eager-repair baseline is later measured to require more bandwidth than lazy repair under the same churn trace (Figure 5), which the paper presents as the trade-off its lazy-repair design exploits, not as a contradiction of a claim made elsewhere. Cross-reference: BHAGWAN-IPTPS-03 (Understanding Availability) supplies the Overnet availability measurements this paper's File Sharing host trace is a scaled-down version of, and CHUN-NSDI-06 (Carbonite) is cited in that paper's own framing as a direct response to and improvement on this paper's repair-policy design — a later reader comparing the two should expect Carbonite to report the comparison from its own side.

### References worth retrieving

- Bhagwan, Savage, Voelker, "Replication strategies for highly available peer-to-peer systems," UCSD Technical Report CS2002-0726, 2002 — foundational (the stochastic redundancy analysis this paper's Equations 1-5 are derived from)
- Bhagwan, Savage, Voelker, "Understanding availability," IPTPS 2003 — foundational (already in this corpus as BHAGWAN-IPTPS-03; source of the File Sharing host availability trace)
- Blake, Rodrigues, "High availability, scalable storage, dynamic peer networks: Pick two," HotOS 2003 — foundational (already in this corpus as BLAKE-HOTOS-03)
- Dabek et al., "Wide-area cooperative storage with CFS," SOSP 2001 — competing (CFS/DHash's eager-repair, five-way replication design is the direct comparison baseline for this paper's eager-repair policy)
- Stoica et al., "Chord: A scalable peer-to-peer lookup service for Internet applications," SIGCOMM 2001 — foundational (the DHT layer TotalRecall's prototype is built on)
- Kubiatowicz et al., "OceanStore: An architecture for global-scale persistent storage," ASPLOS 2000 — competing (OceanStore's periodic-refresh mechanism is cited as similar in spirit to lazy repair)
- Bolosky et al., "Feasibility of a serverless distributed file system deployed on an existing set of desktop PCs," SIGMETRICS 2000 — foundational (source of the synthetic File System availability trace)
- Maymounkov, Mazières, "Rateless codes and big downloads," IPTPS 2003 — foundational (the online-codes erasure-coding algorithm implemented in the prototype)
- Muthitacharoen et al., "Ivy: a read-write peer-to-peer file system," OSDI 2002 — competing (comparison point for the Modified Andrew Benchmark result)
- Douceur, Wattenhofer, "Optimizing file availability in a secure serverless distributed file system," SRDS 2001 — competing
- Kostic et al., "Using random subsets to build scalable services," USITS 2003 — foundational (the scalable-availability-tracking alternative the paper cites as needed beyond PlanetLab scale)

### Verbatim extracts

- "no single assignment of storage to hosts can provide a predictable level of availability over time"
- "hosts joined and left the system over 6 times per day on average" [citing their own Overnet study]
- "TotalRecall is not designed to survive catastrophic attacks or widespread network failures"
- "an erasure-coded representation only requires a storage overhead of 2.49" [at availability target 0.999]
- "the overall average system repair bandwidth ... is 35.6 MB/s"
- "average bandwidth per host for lazy repair with erasure coding is 655 Bps, while lazy repair with replication is 75 KBps"
- "bandwidth usage in TotalRecall is almost an order of magnitude more than the optimal system"
- "some advanced behavior remains future work"
