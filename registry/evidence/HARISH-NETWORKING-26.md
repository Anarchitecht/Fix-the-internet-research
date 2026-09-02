## [HARISH-NETWORKING-26] ListGuard: Mitigating Pollution Attacks on In-Network Invertible Bloom Lookup Tables
**Citation:** Harish S A, Vignesh S, Sathwik Kodamarthi, Bikraj Shrestha, Gollapudi Sasank, Mahanth Kumar Valluri, Pravein G. Kannan, Praveen Tammana. "ListGuard: Mitigating Pollution Attacks on In-Network Invertible Bloom Lookup Tables." IFIP Networking Conference, 2026. DOI 10.23919/IFIPNETWORKING70592.2026.11579227.
**Retrieved:** full text via https://doi.org/10.23919/IFIPNetworking70592.2026.11579227
**Source URL:** https://doi.org/10.23919/IFIPNetworking70592.2026.11579227
**Domain:** D

### What it does
ListGuard restores flow statistics in an Invertible Bloom Lookup Table (IBLT — a hash table variant that XORs inserted keys and values into cells shared by multiple hash functions, and recovers elements by repeatedly extracting cells holding exactly one element) after an adversary has injected crafted entries that stall this extraction. An IBLT extracts elements by iterative peeling: a cell with count 1 (a pure cell) holds exactly one element, so that element is read off directly, then XORed out of every other cell it hashed to, which can expose new pure cells. An adversary who controls a compromised host observes IBLT traffic as a man-in-the-middle, keeps a local shadow copy of the IBLT to infer which cells hold entries, and injects flows crafted to hash into already-occupied cells on all their hash indices. Driving cell counts up removes pure cells and halts peeling before all real elements are extracted, without needing to alter the IBLT structure itself. ListGuard adds two data-plane components alongside the unmodified IBLT: an item counter that records how many flows were inserted this epoch, and a flow sampler that independently samples "completely colliding flows" (CCFs — flows whose hash outputs all land in cells that were already non-empty) with fixed probability p. Detection compares the extracted-flow count after peeling against the item counter; if the fraction undecoded exceeds a threshold R, recovery runs. Recovery subtracts the sampled CCFs one at a time from the stalled IBLT and re-invokes peeling after each subtraction, since removing a colliding flow's contribution can reveal a new pure cell; each newly extracted flow is pruned from the remaining sample set to avoid double-subtracting it (the recovery would otherwise corrupt the state through XOR of an already-removed value). The system does not distinguish malicious from benign CCFs at the point of sampling — it treats the union of colliding flows as the useful recovery signal because malicious flows are disproportionately likely to be CCFs by construction of the attack.

### Measured results
| Result | Value | Conditions |
|---|---|---|
| Attack potency | Injecting 1-2% malicious flows renders more than 50% of stored statistics undecodable | FlowRadar (in-network telemetry system built on an IBLT), evaluated on 215 epochs of CAIDA 2018 "dirA March equinix nyc" traffic, 280 ms epochs |
| Deployment-aware vs. deployment-unaware attacker | Both degrade a non-trivial fraction of epochs even at 2-3% malicious flows; the aware attacker (knows IBLT parameters, targets occupied cells) affects more epochs than the unaware attacker (crafts flows without confirmed cell targeting) | Same 215-epoch CAIDA trace on FlowRadar, malicious-flow fractions swept 0-5% |
| Recovery completeness vs. sampling probability p | p = 0.10 recovers almost all affected epochs up to 5% malicious flows; p = 0.12 achieves full recovery consistently across that range | Same CAIDA trace and epoch definition, FlowRadar, sampling only completely colliding flows |
| Sampling overhead at recovery-sufficient p | p = 0.10-0.12 samples 0.34%-4% of total flows per epoch | Same trace/setup; contrasted against sampling all CCFs, which would take 33-45% of flows per epoch |
| Malicious-flow capture for downstream inspection | Selection probability 0.06 captures at least one malicious flow in nearly all epochs, except at the 0.5% malicious-flow-fraction case; at 1% malicious flows, probability 0.03 captures a malicious flow in over 99% of epochs | Same trace/setup; grouping 2-5 consecutive epochs raises capture rate further for the 0.5% case |
| Memory overhead vs. naive overprovisioning | ListGuard needs 1.93x-2.83x less additional memory than overprovisioning the IBLT to keep every epoch decodable, across malicious-flow fractions of 0.5%-5% (e.g. at 1%: 1.04% extra memory vs. 1.99% for standard IBLT; 0.84% vs. 1.99% for FlowRadar) | Same 215-epoch CAIDA trace; sizes given as percentage of baseline IBLT memory |
| Memory overhead vs. a stronger-guarantee IBLT construction | For approximately 24,000 flows, the LFFZ construction (Fleischhacker et al., "Invertible Bloom Lookup Tables with Less Memory and Randomness") needs 69 MB; ListGuard needs 0.3 MB, a 230x difference | Same trace, per-epoch flow count matching CAIDA average |
| Hash randomization does not eliminate the attack | With salted or pseudorandom-function hashing, malicious traffic at 1% or more still measurably degrades the fraction of undecodable flows relative to no attack | Same trace/setup, vanilla hash vs. salted vs. salted-PRF hash compared |
| Per-packet latency overhead | Tail latency rises 1.64%; average latency rises 0.52% | Netronome Agilio CX 1x40GbE SmartNIC prototype, two servers (2x Intel Xeon Silver 4316, 2.30 GHz, 80 cores, 256 GB RAM), CAIDA traffic replayed via TCPReplay |
| Throughput overhead | Reduced by 0.026% | Same SmartNIC prototype and CAIDA replay |
| Dynamic sampling-probability prediction | A Random Forest regressor, retrained on pure-cell ratio and total-flow-count features every 10 ms, predicts the optimal p (the smallest p that keeps all epochs decodable) with 89.12% accuracy | Simulation with varying attack intensities; described as a preliminary extension, not the evaluated static design |

### Parameters
- Selection probability p (fraction of CCFs sampled per epoch): swept, with p = 0.10 giving near-complete recovery up to 5% malicious flows and p = 0.12 giving full recovery; the paper states no single fixed operating value, treating p as tunable to the deployment's attack-intensity assumption.
- Undecodable-flow recovery threshold R: 50% (recovery triggers when the fraction of flows unextracted after peeling exceeds this).
- Epoch length: 280 ms (215 epochs total in the evaluation trace).
- Epoch flow count: average 23,000 flows per epoch, range 8,800-24,000.
- IBLT sizing: 1.3 x expected element count, following the sizing guideline in Goodrich and Mitzenmacher's original IBLT paper.
- CCF fraction of total flows per epoch: 33-45% (this bounds how much overhead would be needed if all CCFs, rather than a p-fraction, were sampled).

### Stated limitations
An attacker aware of ListGuard's CCF-based sampling can craft "partially colliding" flows — flows that collide on at least one but not all hash indices — which still push the IBLT toward undecodability while evading the sampler, since the sampler targets only completely colliding flows; the paper states this adaptive-adversary case is left to future work and does not evaluate a countermeasure for it. The detection module cannot distinguish a pollution attack from a benign traffic burst that happens to reduce pure cells the same way; the paper notes this as a design challenge it addresses only by treating both as "affected epochs" requiring recovery, not by distinguishing cause. The recovery algorithm runs in the worst case quadratic time in the size of the sampled set (each recovery step invokes a linear-time decode pass), which the paper states is acceptable only because both run in the control plane rather than the data plane. Only FlowRadar and LossRadar, both IBLT-based network telemetry systems, are evaluated; the paper argues generality to "in-network systems that rely on IBLT-based decoding" but tests only these two. The dynamic sampling-probability extension (Random Forest regressor) is called preliminary, with deeper study of adaptive policies and hardware feasibility left to future work. The paper's stated future work is to more precisely identify which flows within the sampled set are malicious, under diverse attack workloads — meaning the current system supplies a reduced candidate set for inspection but does not itself classify flows as malicious.

### Requirements it places on the rest of the system
ListGuard requires a companion item counter to be maintained in the data plane alongside the IBLT, incremented on every insertion; the recovery threshold decision depends on comparing this counter against the number of flows the peeling process actually extracts, so any deployment must add this second data-plane primitive, not just the IBLT. It requires the flow sampler to run inline with insertion (sampling CCFs as they are inserted), because CCF status is determined by which cells are already occupied at insertion time, which cannot be reconstructed after the fact from the IBLT alone. It requires the control plane to hold the sampled flow list and to run the modified peeling and recovery loop there, since the paper places this logic outside the resource-constrained data plane. The paper assumes the standard IBLT threat boundary used throughout the evaluation: the control plane and control-data plane channels are uncompromised, and the adversary interacts with the IBLT only through packet insertion, never through direct memory access to the device holding the IBLT. It assumes the adversary knows the IBLT's public parameters (size, hash count, hash type) under Kerckhoffs's principle, but not any secret hash seed, and can infer only a partial, traffic-observed picture of which cells are occupied, not their exact contents. Recovery correctness depends on sampled flows being distinct identifiers that can be independently reinserted and subtracted via XOR without ambiguity; nothing in the design detects or corrects a sampled entry inserted with an incorrect value field.

### Contradicts
None found — no other entry in this batch addresses IBLT pollution or in-network telemetry structures.

### References worth retrieving
- foundational: Goodrich, Mitzenmacher, "Invertible Bloom Lookup Tables," IEEE Allerton, 2011.
- foundational: Li, Miao, Kim, Yu, "FlowRadar: A Better NetFlow for Data Centers," USENIX NSDI, 2016.
- foundational: Li, Miao, Kim, Yu, "LossRadar: Fast Detection of Lost Packets in Data Center Networks," ACM CoNEXT, 2016.
- competing (set reconciliation via IBLT — directly relevant to this corpus's synchronization domain): Mitzenmacher, Pagh, "Simple Multi-Party Set Reconciliation," Distributed Computing, vol. 31 no. 6, 2018.
- competing (set reconciliation via IBLT): Ozisik, Andresen, Levine, Tapp, Bissias, Katkuri, "Graphene: Efficient Interactive Set Reconciliation Applied to Blockchain Propagation," ACM SIGCOMM, 2019.
- competing (set reconciliation via IBLT): Eppstein, Goodrich, Uyeda, Varghese, "What's the Difference? Efficient Set Reconciliation Without Prior Context," ACM SIGCOMM CCR, vol. 41 no. 4, 2011.
- competing (stronger-guarantee IBLT construction, directly compared for memory cost): Mizrahi, Bar-Lev, Yaakobi, Rottenstreich, "Invertible Bloom Lookup Tables with Listing Guarantees," POMACS, vol. 7 no. 3, 2023.
- competing: Fleischhacker, Larsen, Obremski, Simkin, "Invertible Bloom Lookup Tables with Less Memory and Randomness," arXiv:2306.07583, 2023.
- attack: Gerbet, Kumar, Lauradoux, "The Power of Evil Choices in Bloom Filters," IEEE/IFIP DSN, 2015.
- attack: Reviriego, Rottenstreich, "Pollution Attacks on Counting Bloom Filters for Black Box Adversaries," IEEE CNSM, 2020.
- attack: Reviriego, Rottenstreich, Liu, Lombardi, "Analyzing and Assessing Pollution Attacks on Bloom Filters: Some Filters Are More Vulnerable Than Others," IEEE CNSM, 2021.
- attack: Reviriego, Gonzalez, Dayan, Huecas, Liu, Lombardi, "On the Security of Quotient Filters: Attacks and Potential Countermeasures," IEEE Transactions on Computers, vol. 73 no. 9, 2024.
- competing (defense against sketch-level compromise via secure enclaves rather than sampling-based recovery): Cheng, Apostolaki, Liu, Sekar, "TrustSketch: Trustworthy Sketch-Based Telemetry on Cloud Hosts," NDSS, 2024.

### Verbatim extracts
- "injecting as little as 1-2% malicious flows can render more than 50% of the stored statistics undecodable"
- "p = 0.12 consistently achieves full recovery"
- "These settings sample only 0.34%-4% of total flows per epoch"
- "Across attack intensities (0.5%-5%), ListGuard requires 1.93x-2.83x less memory than naive over provisioning"
- "LFFZ requires 69MB of memory, approximately 230x more than ListGuard which requires just 0.3MB"
- "Tail latency increases by 1.64%, while average latency rises by 0.52%"
- "ListGuard reduces throughput by only 0.026%"
- "the adaptive mechanism predicts an optimal p with 89.12% accuracy"
