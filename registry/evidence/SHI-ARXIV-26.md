## [SHI-ARXIV-26] Tight Bandwidth Lower Bounds and Optimal Constructions of Locally Repairable Convertible Codes in the Global Split Regime

**Citation:** Haoming Shi, Weijun Fang. "Tight Bandwidth Lower Bounds and Optimal Constructions of Locally Repairable Convertible Codes in the Global Split Regime." arXiv preprint, 2026. DOI 10.48550/ARXIV.2606.26742.
**Retrieved:** full text via https://arxiv.org/abs/2606.26742
**Source URL:** https://arxiv.org/abs/2606.26742
**Domain:** C

### What it does
The paper states, and proves matching, the minimum data-transfer cost of converting one erasure-coded object into several smaller erasure-coded objects that together hold the same data, for a class of locally repairable codes (LRCs). An LRC is a code that adds, alongside its global parity nodes, extra local parity nodes so that a single failed storage node can be reconstructed by reading only a small local group of nodes rather than the whole object. A locally repairable convertible code (LRCC) is a pair of an initial LRC and a final LRC together with a conversion procedure: a coordinator downloads data from the initial code's storage nodes and computes the nodes of the final code(s), retiring some initial nodes and creating new ones while keeping as many nodes unchanged as possible (a "stable" conversion). The "global split regime" is the case where one initial codeword is broken into two or more final codewords covering disjoint parts of the data, with the same per-group parameters (r information nodes per local group, ℓ local parity nodes per group) preserved across the split. "Read bandwidth" is the total number of symbols the conversion coordinator must download from the initial code's nodes to perform the conversion.

The paper first proves a structural lemma: in any stable conversion in this regime, every initial global parity node must be retired, every final global parity node must be newly computed, and every local parity node that is kept must stay attached to the same information nodes. From this it derives two entropy-based lower bounds on the read bandwidth (Theorems IV.1 and IV.2), which combine into a single tight bound (Theorem IV.3) covering the entire parameter range where the initial and final global-parity counts (g_I, g_F) are each at most the local group size r. It then gives explicit constructions, built from Maximum-Distance-Separable (MDS) array codes with prescribed repair or alignment properties via a piggybacking technique (each code symbol is decomposed into aligned sub-symbols so that repair or conversion of one symbol can reuse partially-computed data from another), that meet this lower bound exactly (Theorem V.1) over any sufficiently large finite field, for the three cases g_F = g_I, g_F > g_I, and g_F < g_I separately.

### Measured results
This is a theory paper: every quantitative claim is a proven mathematical bound or a construction that provably attains it, not an experimental measurement, and there is no simulation, testbed, or hardware. The results are stated as closed-form formulas over the LRCC parameters (k_I, g_I, r, ℓ; k_F, g_F, r, ℓ, α), where k_I and k_F are the initial and final numbers of information nodes, g_I and g_F the initial and final numbers of global parity nodes, r the local-group size, ℓ the number of local parity nodes per group, α the sub-packetization level (symbols per node), and λ_F ≥ 2 the number of final codewords the initial codeword splits into (with k_I = λ_F · k_F and µ = k_F / r the number of local groups per final codeword).

| Result | Formula | Condition |
|---|---|---|
| Lower bound on read bandwidth γ_R (Theorem IV.3) | γ_R ≥ λ_F g_F [(λ_F−1)(k_F+µℓ)+g_I+ℓ] / [(λ_F−1)(g_F+ℓ)+g_I+ℓ] · α | when g_F ≤ g_I |
| Lower bound on read bandwidth γ_R (Theorem IV.3) | γ_R ≥ [λ_F g_F/(g_F+ℓ)]·(k_F+µℓ)·α − g_I·[(k_F+µℓ)/(g_F+ℓ) − 1]·α | when g_F > g_I |
| Achieved read bandwidth of the paper's own construction (Theorem V.1) | matches the Theorem IV.3 bound exactly, both cases | over a sufficiently large finite field size q; explicit sub-packetization α = g_F+ℓ (if g_F ≥ g_I) or α = λ(g_F+ℓ)+(g_I−g_F) (if g_F < g_I) |
| Read bandwidth of the prior Maturana-Rashmi global-split construction, γ_R^MR | γ_R^MR − γ_R^LB = λ_F g_F ℓ (λ_F−1)(S−g_F−ℓ) / [D(D+ℓ)]·α (g_F ≤ g_I case), or g_I ℓ(λ_F g_F − g_I)(S−g_F−ℓ) / [(g_F+ℓ)(λ_F g_F(g_F+ℓ)−g_I ℓ)]·α (g_F > g_I case), with S := k_F+µℓ, D := (λ_F−1)(g_F+ℓ)+g_I | the difference is proven ≥ 0 always, and strictly positive unless µ=1 and g_F=r |

The last row is the paper's comparison result: the previously published Maturana-Rashmi construction for this regime is proven not bandwidth-optimal in general (it downloads strictly more than the new lower bound except at the single boundary case µ=1, g_F=r), which is a proven inequality between two closed-form formulas, not a benchmark run on data.

### Parameters
No experimental parameters exist (no run, no dataset, no hardware). The paper's construction requires a finite field F_q of size large enough for the piggybacking matrices used in the construction to exist (stated as "sufficiently large finite field" with no numeric threshold derived in the excerpted sections). The construction restricts to the parameter range g_I ≤ r and g_F ≤ r, where r is the local-group size; the paper states this restriction explicitly and does not claim results outside it.

### Stated limitations
The authors state the parameter range g_I, g_F ≤ r as the boundary of what the paper proves; whether matching lower bounds and constructions exist when g_I or g_F exceeds r is left as an open problem in the conclusion. The paper also states, as future work, that conversions between different code types (LRC-to-LRC conversions with different locality parameters, MDS-to-LRC, LRC-to-MDS) and other code families (Reed-Muller codes, regenerating codes, algebraic geometry codes) are not addressed. The construction is proven only for a field size large enough for the piggybacking matrices to exist; no explicit minimum field size or convergence rate is given in the sections read.

### Requirements it places on the rest of the system
A system adopting this construction needs: (1) a coordinator process that can read from every initial-code storage node during conversion and write to every new storage node — the read-bandwidth accounting assumes a single coordinator performs the whole download, not a peer-to-peer diffusion; (2) the initial and final codes fixed to the "global split" shape, meaning the local-group size r and the local parity count ℓ are identical before and after conversion, and only the global parity count and the number of independent final objects change; (3) systematic codes, so the k information nodes hold the message data uncoded and are identified directly between initial and final codewords with no data movement for those nodes; (4) a finite field large enough for the underlying MDS array code's piggybacking matrices to exist, which the storage system must be able to allocate (field size grows with the code parameters, no closed-form minimum stated in the read sections); (5) the conversion must be "stable" in the paper's sense — every local group preserved, all initial global parity nodes retired, all final global parity nodes freshly computed — which the paper proves is the unique way to maximize the count of untouched nodes for this regime.

### Contradicts
The Maturana-Rashmi (2023 ISIT) global-split LRCC construction is shown not bandwidth-optimal in general in the g_I, g_F ≤ r regime; this is a proof within the same paper, not a disagreement with another paper in this corpus. No other entry in this corpus is contradicted; no other entry in this corpus reports a competing measurement of read-bandwidth-optimal LRCC conversion (searched: no other LRCC-conversion paper is in this batch).

### References worth retrieving
- Maturana, Rashmi, "Locally Repairable Convertible Codes: Erasure Codes for Efficient Repair and Conversion," ISIT 2023, pp. 2033-2038 — foundational (the construction this paper improves on and disproves optimality of)
- Maturana, Rashmi, "Convertible Codes: Enabling Efficient Conversion of Coded Data in Distributed Storage," IEEE Trans. Inf. Theory 68(7), 2022, pp. 4392-4407 — foundational (introduces convertible codes generally)
- Chopra, Singhvi, Rashmi, "Bandwidth Cost of Locally Repairable Convertible Codes in the Global Merge Regime," 2026, arXiv:2604.15282 — foundational (the merge-regime counterpart this paper's split-regime result completes; explicitly posed the open problem this paper answers)
- Singhvi, Chopra, Rashmi, "Tight Lower Bounds on the Bandwidth Cost of MDS Convertible Codes in the Split Regime," 2025, arXiv:2511.12279 — foundational (the information-theoretic method this paper extends from plain MDS codes to LRCs)
- Kong, "Locally Repairable Convertible Codes With Optimal Access Costs," IEEE Trans. Inf. Theory 70(9), 2024, pp. 6239-6257 — competing (same LRCC conversion problem, different cost metric: access cost rather than bandwidth cost)
- Ge, Cai, Tang, "Locally Repairable Convertible Codes: Improved Lower Bound and General Construction," IEEE Trans. Inf. Theory 72(5), 2026, pp. 2915-2930 — competing (access-cost LRCC bounds, adjacent to this paper's bandwidth-cost bounds)
- Xia, Saxena, Blaum, Pease, "A Tale of Two Erasure Codes in HDFS," FAST 2015, pp. 213-226 — foundational (earliest deployed system motivating LRC conversion between hot/cold data tiers, pre-dating the formal convertible-code framework)
- Rashmi, Shah, Gu, Kuang, Borthakur, Ramchandran, "A hitchhiker's guide to fast and efficient data reconstruction in erasure-coded data centers," SIGCOMM 2014, pp. 331-342 — foundational (production repair-bandwidth measurement on the Facebook warehouse cluster, cited as motivation for bandwidth as the relevant cost metric)
- Ye, Barg, "Explicit Constructions of High-Rate MDS Array Codes With Optimal Repair Bandwidth," IEEE Trans. Inf. Theory 63(4), 2017, pp. 2001-2014 — foundational (Theorem II.2 in this paper, the existence result for optimal-repair MDS array codes the constructions build on)

### Verbatim extracts
- "we show that their constructions are not bandwidth-optimal in general in this regime"
- "This answers the open problem raised in [27] for this parameter range."
- "all initial global parity nodes are retired nodes"
- "all final global parity nodes are new nodes"
- "a conversion is stable if and only if it attains the upper bound"
- "A natural problem is to study whether lower bounds and matching constructions can be obtained"
