## [WEATHERSPOON-IPTPS-02] Erasure Coding Vs. Replication: A Quantitative Comparison

**Citation:** Hakim Weatherspoon, John D. Kubiatowicz. "Erasure Coding vs. Replication: A Quantitative Comparison." International Workshop on Peer-to-Peer Systems (IPTPS), 2002. DOI 10.1007/3-540-45748-8_31.
**Retrieved:** full text via https://link.springer.com/chapter/10.1007/3-540-45748-8_31
**Source URL:** https://link.springer.com/chapter/10.1007/3-540-45748-8_31
**Domain:** C

Note on source text: the extracted text substitutes glyph codes (e.g. "/BD" through "/BL") for the digits 0–9 throughout the equations and worked examples, a font-encoding artifact of the PDF extraction. The mapping was recovered by cross-checking decoded values against values the prose states in plain English (for example, the decoded repair-epoch value matches the paper's own words "four months" at the same location) and is internally consistent across every worked example in the paper. All numeric parameters below are reported as decoded under this mapping.

### What it does
The paper compares two ways to keep a data block durable in a peer-to-peer storage system that periodically sweeps and repairs lost redundancy: whole-block replication, and (n,k) erasure coding, which splits a block into k fragments and recodes them into n ≥ k fragments such that any k of the n fragments reconstruct the block. It states a closed-form model for the storage, bandwidth, and disk-seek cost of each approach as a function of system size, repair-epoch length, and redundancy factor, and it derives an equation for the mean time to failure (MTTF) of a single block under periodic sweep-and-repair, given a per-disk lifetime distribution. It then uses the model to run three fixed-parameter comparisons between a replicated and an erasure-coded system: (1) hold system MTTF and repair epoch fixed and compare bandwidth, storage, and disk seeks; (2) hold storage overhead and repair epoch fixed and compare block MTTF; (3) hold block MTTF and storage overhead fixed and compare repair bandwidth.

Mechanically: fragments (or replicas) of a block are placed on independently, uniformly randomly selected disks; a global sweep-and-repair process periodically reconstructs each block from any k surviving fragments and redistributes fresh fragments to replace lost ones, with the interval between sweeps of the same block defined as the repair epoch. Replication is modeled as the special case (k=1, n=r) of the same erasure-coding framework, so a system storing r whole replicas of a block is treated as an (1, r) code.

### Measured results
All results are analytical, from the paper's closed-form cost model, not from a simulation or a deployed system; no node count, topology, dataset, or runtime is reported anywhere in the paper.

Availability example (Section 4): with 1,000,000 machines, 10% of them unavailable at any time, storing 2 whole replicas gives 2 nines of availability (0.99). A rate-1/2 code split into 32 fragments, at equal total storage and bandwidth to the 2-replica case, gives over 8 nines of availability (0.99999999).

| Comparison (fixed variables) | Replicated system parameters | Erasure-coded system parameters | Result |
|---|---|---|---|
| Fix system MTTF (1000 years) and repair epoch (4 months), N = 2^24 users, block size 8 kB, disk block size 8 kB, u = 10^19 total blocks | r = 22 replicas | rate-1/2 code, n = 64 fragments | Replicated system uses 11× the bandwidth, 11× the storage, and 11× the disk seeks of the erasure-coded system for the same block count and repair epoch. |
| Fix storage overhead (factor of 2) and repair epoch (4 months) | r = 2 replicas | rate-1/2 code, n = 64 fragments | Replicated block MTTF = 74 years. Erasure-coded block MTTF = 10^20 years, at the same storage overhead and repair epoch. |
| Fix block MTTF (10^6 years), storage overhead (factor of 4), u = 1,000 blocks, system MTTF (1000 years) | r = 4 replicas, repair epoch = 1 month | rate-1/4 code, n = 64 fragments (k=16), repair epoch = 28 months | Replicated system uses 28× the repair bandwidth of the erasure-coded system at the same block MTTF and same storage overhead. |
| Fix block MTTF (10^20 years), storage overhead (factor of 4), u = 10^19 blocks, system MTTF (1000 years) | r = 4 replicas, repair epoch → "almost instant and continuous" (not numerically bounded by the paper) | rate-1/4 code, n = 64 fragments (k=16), repair epoch = 12 months | Erasure coding sustains the required durability with a 12-month repair epoch; the paper states the equivalent replicated system would have to repair continuously, without giving it a finite repair-epoch value. |

### Parameters
| Parameter | Symbol | Value(s) used |
|---|---|---|
| Block size | q | 8 kB |
| Disk block size | dbsz | 8 kB |
| Number of users | N | 2^24 |
| Repair epoch (both systems, example 1) | e | 4 months |
| Target system MTTF | MTTF_system | 1000 years (examples 1, 3, 4); 10^20 years is used as a target block MTTF in example 4, not a system MTTF |
| Replicas, example 1 | r | 22 |
| Code, example 1 | rate, n | rate 32/64 = 1/2, n = 64 |
| Disk lifetime distribution | — | drawn from Patterson & Hennessy, augmented by discarding any disk still in service after 5 years, along with its data |
| Failure model | — | disks fail independently and identically distributed; failed disks are replaced immediately with new, blank disks |

### Stated limitations
The independent-and-identically-distributed failure assumption is stated by the authors as "the most troubling assumption" of the analysis; correlated failures across storage servers (natural disaster, denial-of-service, shared administrative boundary) are not modeled, and the paper proposes only two unevaluated mitigations: routing-overlay-based geographic diversity in fragment placement, or measurement-driven selection of maximally independent node sets. The sweep-and-repair process is described as simplistic because it reconstructs every block on a periodic schedule regardless of whether that specific block needs repair, consuming repair resources proportional to total data volume rather than to actual loss. Reads in an erasure-coded system contact more distinct servers than in a replicated system and read "logical" fragments smaller than a whole replica; the paper argues (without measurement) that this is mitigated by aggregating clients across many servers and by message/disk-block aggregation, and states this aggregation assumption is implicit in its bandwidth and disk-seek metrics rather than separately modeled. The paper explicitly separates durability from latency: it recommends erasure coding be used only for durability and that replica-based caching, constructed and destroyed as soft state, be used for read latency, and states this combination as an unevaluated design recommendation rather than a measured result.

### Requirements it places on the rest of the system
The model requires a placement mechanism that distributes each block's fragments or replicas onto independently and uniformly randomly selected disks; the durability numbers are conditioned on that independence, which the authors state they cannot themselves guarantee without an unevaluated geographic-diversity mechanism from an overlay network such as CAN, Chord, Pastry, or Tapestry. The scheme requires a data-integrity layer able to positively identify a corrupted fragment before reconstruction; the paper states that without such identification, reconstructing a block from a mix of corrupted and correct fragments enumerates the combinations of which k of n fragments are correct, and recommends a secure verification hash per fragment be added at the cost of extra bandwidth and storage the paper does not quantify. Erasure-coded reads require a client to contact k distinct servers concurrently, more distinct servers per read than the replicated case requires, so a deployment needs enough concurrently reachable, available servers per block to complete k-out-of-n reads without added latency; the paper does not measure this latency, only bandwidth and storage.

### Contradicts
None found.

### References worth retrieving
- foundational: Chen, Y., Edler, J., Goldberg, A., Gottlieb, A., Sobti, S., Yianilos, P. "Prototype implementation of archival intermemory." IEEE ICDE, 1996. (first system with erasure-code-based durability; the paper states it lacks a repair mechanism)
- competing: Bolosky, W., Douceur, J., Ely, D., Theimer, M. "Feasibility of a serverless distributed file system deployed on an existing set of desktop PCs." Sigmetrics, 2000. (source of the per-workstation data-rate measurement used as a model input)
- competing: Kubiatowicz, J., et al. "OceanStore: An architecture for global-scale persistent storage." ASPLOS, 2000. (the hybrid replication-for-caching plus coding-for-durability design the paper's Discussion section recommends without evaluating)
- competing: Druschel, P., Rowstron, A. "Storage management and caching in PAST, a large-scale, persistent peer-to-peer storage utility." ACM SOSP, 2001. (a purely replication-based system cited as a comparison point)
- foundational: Rhea, S., Wells, C., Eaton, P., Geels, D., Zhao, B., Weatherspoon, H., Kubiatowicz, J. "Maintenance free global storage in OceanStore." IEEE Internet Computing, 2001. (source of the durability-derivation method reused and verified in Section 5.2)
- attack/critique: none identified in this bibliography; the paper is itself an analytical model with no adversarial evaluation.

### Verbatim extracts
- "erasure-resilient systems use an order of magnitude less bandwidth and storage"
- "the most troubling assumption of the previous sections are that failures are independent"
- "mechanisms for durability should be separated from mechanisms for latency reduction"
- "the sweep and repair is simplistic because it assumes that all data...is reconstructed"
- "a replicated system...would have to repair all blocks almost instantly and continuously"
