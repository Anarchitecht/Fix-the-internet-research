## [CHENG-TOS25-ECSURVEY] A Survey of the Past, Present, and Future of Erasure Coding for Storage Systems
**Citation:** Zhirong Shen, Yuhui Cai, Keyun Cheng, Patrick P. C. Lee, Xiaolu Li, Yuchong Hu, Jiwu Shu. "A Survey of the Past, Present, and Future of Erasure Coding for Storage Systems." ACM Transactions on Storage, Vol. 20, No. 4, Article 1, December 2024 / January 2025.
**Retrieved:** full text (retrieved and read in full for the corpus's `volunteer-repair-economics.md` open-problem entry; no `targets-deduped.json` record for this key)
**Source URL:** not recorded in the registry for this key
**Domain:** C

### What it does
This survey systematizes erasure coding for storage systems — a redundancy technique that recovers lost
data from a subset of encoded fragments, using less total storage than keeping full copies at the same
failure tolerance — across three categories: new erasure-code constructions, algorithmic optimizations of
existing constructions, and deployment under emerging hardware architectures. An (n, k) erasure code
splits a data unit into k original chunks, encodes them into n total chunks (k data plus n−k parity), and
recovers the original data from any k of the n chunks; storage overhead is the redundancy ratio n/k. The
survey organizes repair-cost-reducing constructions around two families: regenerating codes, which repair
a single lost chunk by having each of the remaining nodes send a smaller, network-coded combination of
its own stored sub-chunks rather than a full chunk, reducing the total bytes transferred during repair
below what reading k full chunks would need; and locally repairable codes (LRCs), which add extra local
parity chunks covering only a subset of a stripe, so repairing one lost chunk in that subset reads only
the smaller local group instead of the full stripe. Regenerating codes split at their optimal boundary
into minimum-storage regenerating (MSR) codes, which hold storage overhead at the same optimum as a
plain erasure code while minimizing repair bandwidth for that storage level, and minimum-bandwidth
regenerating (MBR) codes, which instead hold repair bandwidth at its own minimum at the cost of higher
storage overhead than MSR.

### Measured results
Every figure below is a fact this survey states about another paper's or another deployed system's
result, most cited to a specific reference; none is an experiment this survey ran itself, consistent with
its own framing as a systematization of the field, not a new measurement.

| Figure | System / construction | Attributed source (as cited by this survey) |
|---|---|---|
| Erasure code parameters (n, k) and redundancy ratio n/k in production, by system | Google Colossus (9,6) 1.50; Quantcast File System (9,6) 1.50; Hadoop Distributed File System (9,6) 1.50; Baidu Atlas (12,8) 1.50; Facebook f4 (14,10) 1.40; Yahoo Cloud Object Store (11,8) 1.38; Microsoft Windows Azure Storage (16,12) 1.33; Tencent Ultra-Cold Storage (12,10) 1.20; Pelican (18,15) 1.20; Backblaze Vaults (20,17) 1.18 | Table reported in the survey's reference [61], a secondary compilation, not this survey's own measurement of each system |
| Fraction of stripe failure events that are single-chunk failures | "more than 98%" | Facebook's warehouse cluster, cited to reference [153] |
| MSR-code repair-bandwidth reduction over Reed-Solomon codes for a single-node failure | "close to 50%" | For the specific parameterization n − k = 2, a general analytical result the survey attributes to the regenerating-code literature it reviews, not one deployment's measurement |
| Azure-LRC configuration example | (k, l, g) = (6, 2, 2), stripe size n = k + l + g = 10 | Illustrative worked example from the survey's own description of Microsoft's Local Reconstruction Codes (its reference [66]), not a production-scale measurement |

### Parameters
- (n, k) erasure code: n total chunks, k required for reconstruction, redundancy ratio n/k — the survey
  states production deployments keep n typically at or below 20 "to limit the repair penalty."
  Every entry in the production-deployment table above uses this parameterization.
- Azure-LRC's three-parameter form (k, l, g): k data chunks split into l local groups of k/l chunks each,
  plus g global parity chunks computed over all k data chunks; stripe size n = k + l + g; the construction
  tolerates any g + 1 chunk failures within one stripe and repairs a single failed chunk within a local
  group by reading only that group's k/l chunks rather than k chunks across the whole stripe.
- MSR-code parameter restrictions the survey states exist in specific deployed constructions: n − k = 2
  for FMSR codes and Butterfly codes; n ≥ 2k − 1 for PM-RBT codes; Clay codes are stated to support
  general (n, k) without this restriction and are described by the survey as "the state-of-the-art MSR
  codes."

### Stated limitations
The survey states its own repair-optimization review is drawn from data-center deployments — Facebook,
Microsoft Azure, Backblaze, Ceph, Hadoop Distributed File System — and cites peer-to-peer, churn-driven
repair in only two places, both secondary: crediting a 2005 paper (Rodrigues and Liskov, cited as
reference [160]) as the origin of "lazy recovery" (deferring a repair operation rather than triggering it
immediately on every detected loss) in peer-to-peer networks, and citing that same paper's finding that
erasure coding's benefit over replication "may be limited and even negated by the complexity of deploying
erasure coding" in peer-to-peer distributed hash tables — a finding this survey repeats, not reproduces.
No volunteer-churn or decentralized-network repair measurement newer than 2005 appears anywhere in this
survey's text. The survey's own stated open problems (Section 6) are: erasure coding for DNA storage,
where synthesis and sequencing introduce substitution, deletion, and insertion errors (the survey cites
6.2% and 5.7% of error probabilities attributed to insertion and deletion errors respectively, from
reference [11]) that current erasure-code families are not designed around; applying AI techniques to
predict erasure-code parameters, predict hardware reliability for proactive redundancy changes, and guide
stripe placement, none of which the survey states has a published, evaluated system yet; and using
erasure coding to protect machine-learning model training state, where the survey states open issues
including how to encode periodically without degrading training throughput and how to encode
non-linear model components, again without a cited resolved system.

### Requirements it places on the rest of the system
A regenerating code's sub-packetization (splitting each chunk into smaller sub-chunks for encoding and
repair) requires every node holding a fragment of a stripe to compute and transmit a network-coded
combination of its sub-chunks during a repair, not merely forward a stored fragment unmodified — a repair
mechanism that only ever performs a full read from k surviving fragments (the survey's description of
plain Reed-Solomon repair) cannot realize a regenerating code's bandwidth reduction without this
computation step at each contributing node. A locally repairable code's local-group repair path requires
the storage layer to track which chunks of a stripe belong to which local group, so a failed chunk's
repair can be routed to only that group's members rather than to an arbitrary k-of-n selection across the
whole stripe; the survey states Azure-LRC's own limitation here explicitly — global parity chunks are not
covered by any local group, so repairing a lost global parity chunk still requires retrieving k chunks
across the full stripe, the more expensive path the local grouping was built to avoid for data and local
parity chunks.

### Contradicts
None found against other corpus entries on a measured fact — this survey performs no primary measurement.
Consistent with the corpus's `volunteer-repair-economics.md` synthesis, this survey's own review confirms
it does not update or re-examine `BLAKE-HOTOS-03` or `CHUN-NSDI-06`'s conflicting feasibility conclusions
about churn-driven repair, and does not connect its regenerating-code and locally-repairable-code
constructions to any volunteer-scale churn measurement.

### References worth retrieving
- **Foundational** — Alexandros G. Dimakis, P. Brighten Godfrey, Yunnan Wu, Martin J. Wainwright, Kannan
  Ramchandran. (Cited as reference [32]; the seminal regenerating-code paper proving the storage-versus-
  repair-bandwidth trade-off curve and defining MSR and MBR codes — already present in this corpus as
  `DIMAKIS-TIT-10`, which `volunteer-repair-economics.md` already retrieved and analyzed.)
- **Foundational** — Cheng Huang, Huseyin Simitci, Yikang Xu, Aaron Ogus, Brad Calder, Parikshit Gopalan,
  Jin Li, Sergey Yekhanin. (Cited as reference [66]; source of Local Reconstruction Codes, the Azure-LRC
  construction this survey describes in detail.)
- **Foundational** — Rodrigo Rodrigues, Barbara Liskov. "High Availability in DHTs: Erasure Coding vs.
  Replication." International Workshop on Peer-to-Peer Systems (IPTPS), 2005, 226–239. (Cited as
  reference [160]; the paper this survey's only peer-to-peer-specific reliability finding rests on.)
- **Foundational** — Frank Dabek, Jinyang Li, Emil Sit, James Robertson, M. Frans Kaashoek, Robert Morris.
  "Designing a DHT for low latency and high throughput." (Cited as reference [29]; describes DHash++'s use
  of erasure coding in a distributed hash table, mentioned in this survey's adoption-history section.)
- **Competing** — Hank Weatherspoon, John Kubiatowicz. (Cited as reference [194]; compares replication and
  erasure coding by mean-time-to-failure, a different reliability-modeling approach than Rodrigues and
  Liskov's, reaching a more favorable conclusion for erasure coding — worth retrieving to check whether
  its more favorable finding and Rodrigues/Liskov's more skeptical one are reconcilable or genuinely
  disagree on the same modeled scenario.)
- **Foundational** — Mansoor Konwar, et al. (Cited as reference [88]; addresses erasure coding under
  disaggregated-memory architecture constraints, one of this survey's "emerging architecture" deployment
  challenges.)

### Verbatim extracts
- "more than 98% of failure events of a stripe are single-chunk failures in a Facebook's warehouse
  cluster."
- "MSR codes can reduce the repair bandwidth of RS codes for repairing a single-node failure by close to
  50%."
- "the benefits of erasure coding may be limited and even negated by the complexity of deploying erasure
  coding."
- "typical parameters of (n,k) are limited to no more than 20 to limit the repair penalty."
- "existing erasure coding designs are reactive to system changes."
