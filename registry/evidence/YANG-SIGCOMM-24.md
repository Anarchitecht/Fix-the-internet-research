## [YANG-SIGCOMM-24] Practical Rateless Set Reconciliation
**Citation:** Lei Yang, Yossi Gilad, Mohammad Alizadeh. "Practical Rateless Set Reconciliation." ACM SIGCOMM 2024 Conference (ACM SIGCOMM '24), 2024. 18 pages. DOI 10.1145/3651890.3672219.
**Retrieved:** full text via https://arxiv.org/pdf/2402.02668
**Source URL:** https://arxiv.org/abs/2402.02668
**Domain:** D

### What it does
Rateless IBLT (Invertible Bloom Lookup Table) lets two parties, each holding a set of fixed-length bit strings, learn the symmetric difference between their sets — the items each has that the other lacks — while transmitting an amount of data proportional to the size of that difference rather than to the size of either set, and without either party knowing the difference size in advance.

The sender encodes its set into an infinite sequence of coded symbols s_0, s_1, s_2, ... A coded symbol holds three fields: a `sum` (the bitwise exclusive-or, XOR, of every source symbol mapped to it), a `checksum` (the XOR of the hashes of those source symbols), and a `count` (the number of source symbols mapped to it). A deterministic mapping rule decides, for any source symbol x and any coded-symbol index i, whether x maps to the i-th coded symbol; the mapping probability for index i is rho(i) = 1/(1+alpha*i), so earlier coded symbols receive more source symbols on average than later ones. Because both parties derive coded symbols with the same mapping rule, subtracting (XOR) the two parties' coded symbol sequences pairwise cancels every source symbol held by both parties and leaves only the symmetric difference encoded. The receiver decodes with a peeling procedure: a coded symbol is "pure" when exactly one source symbol maps to it (detectable by comparing checksum against the hash of sum); the receiver recovers that source symbol, removes it (by XOR) from every other coded symbol it maps to, and repeats until no pure symbols remain or all difference items are recovered. The receiver requests additional coded symbols only until decoding succeeds — it needs no prior estimate of the difference size, and the sender needs no prior estimate either, distinguishing this scheme from a regular (non-rateless) IBLT, whose parameters m (symbol count) and k (symbols per source item) must be fixed in advance and which fails outright if the realized difference exceeds m.

The scheme sets alpha = 0.5 in its final design, chosen because computing the inverse mapping function under alpha = 0.5 requires only a square root rather than raising a value to an arbitrary non-integer power, which the authors found substantially slower on older CPUs; simulations show alpha = 0.5 costs only 3% more communication overhead than the numerically optimal alpha = 0.64.

Against adversarial input — a party able to craft items it inserts into its own or a counterparty's set, for example a rogue post in a distributed social-media application — the mechanism uses a keyed hash function (SipHash) with a secret key shared between the two reconciling peers, rather than a long, unkeyed hash. A short unkeyed hash lets an adversary who does not know the key still search for a hash collision against a known item computationally, but cannot target the collision at a specific peer pairing because the peer-specific key is unknown to the adversary; each additional peer key the sender uses adds a separate checksum-computation cost.

An extension, Irregular Rateless IBLT, partitions source symbols into c mutually exclusive subsets by hash value and applies a distinct alpha_j to each subset (regular Rateless IBLT is the special case c=1, alpha_0=0.5), lowering communication overhead further at additional encoding and decoding cost.

### Measured results

| Result | Value | Conditions |
|---|---|---|
| Asymptotic communication overhead | Converges to 1.35x the set-difference size, in coded symbols, as difference size d -> infinity | alpha = 0.5; proved by density evolution analysis (Corollary 5.2) |
| Overhead across finite d | 1.35x-1.72x average, converging to 1.35x when d reaches the low hundreds | alpha = 0.5; Monte Carlo simulation, 100 runs per data point, item length not fixed (asymptotic analysis) |
| Overhead vs. alpha choice | alpha=0.5 gives eta*=1.35; numerically optimal alpha=0.64 gives eta*=1.31 (3% lower) | Density evolution analysis compared against Monte Carlo simulation, 100 runs per point |
| Communication overhead vs. competing schemes | Rateless IBLT 2-4x lower overhead than regular IBLT and MET-IBLT when set difference < 50 items; PinSketch achieves overhead of 1 (37-60% lower than Rateless IBLT) | Set size 1,000,000 items, item length 32 bytes (SHA-256 hash size), set differences of 1-400 items, 100 repetitions per data point for Rateless IBLT/MET-IBLT, decoding-failure threshold for regular IBLT tuned below 1/3,000 |
| Merkle trie overhead | Over 40x, across all tested difference sizes | Same setup as above; Merkle trie overhead insensitive to difference size in the tested range |
| Encoding throughput vs. PinSketch | 2-2000x higher | Item size fixed at 8 bytes (PinSketch's implementation maximum), differences of 2-10^5 items, single-threaded, pinned to one CPU core of a server with two Intel Xeon E5-2697 v4 CPUs |
| Encoding time growth | Grows less than 6x as difference size increases 50,000x | Same hardware/setup as above; PinSketch's encoding time grows 5,000x over the same range |
| Decoding throughput vs. PinSketch | 10-10^7x higher | Same hardware/setup; decoding throughput independent of set size N |
| Decoding time at scale | 0.01 s to decode 10^5 differences (Rateless IBLT) vs. over one minute for PinSketch to decode 10^4 differences | Same hardware/setup |
| Encoding time vs. set size N | 2.9 ms at N=10^4 vs. 294 ms at N=10^6, for 1,000 differences | Same hardware; scaling matches N (100x change in N gives 100x change in time) |
| Slowdown vs. item length | Sublinear below 2 KB items (under 4x slowdown as item length grows 16x from 8 to 128 bytes); linear above 2 KB | Fixed difference size (implied from Fig. 11 context), item lengths 8 bytes-32 KB |
| Data rate at 1,000-item difference | 124.8 MB/s encoding throughput | Same hardware |
| Ethereum ledger sync: completion time / communication cost vs. state heal (Merkle-trie-based production system) | 4.8-13.6x lower completion time, 4.4-8.6x lower communication cost | 230 million Ethereum accounts (20-byte keys, 72-byte values) as of Jan 4, 2024; ledger snapshots from blocks 18,908,312-18,938,312 (100-hour span, Dec 31 2023-Jan 4 2024); staleness varied 20 min-100 hours; network link 50 ms one-way propagation delay, 20 Mbps bandwidth cap via Dummynet; two Intel Xeon E5-2698 v4 CPUs, FreeBSD 14.0; state heal via unmodified Geth v1.13.10 |
| Round-trip requirement vs. state heal | State heal needs at least 11 rounds of interactivity (descending Merkle trie in lock step); Rateless IBLT needs half a round (Alice streams without waiting for feedback) | Same Ethereum setup; example: Rateless IBLT 8.2x faster than state heal when Bob's state is 1 block (12 s) stale |
| Completion time vs. bandwidth | Rateless IBLT 4.8x faster at 10 Mbps, 16x faster at 100 Mbps; state heal's completion time plateaus after 20 Mbps because it becomes compute-bound | Bob's snapshot fixed at 10 hours stale, 50 ms propagation delay, bandwidth cap varied 10-100 Mbps |
| Uncapped bandwidth completion time | Rateless IBLT: 2.5 s, saturating a 170 Mbps link on one CPU core per side | Same Ethereum setup, bandwidth cap removed |
| Incremental update cost | 11 ms to update 50 million coded symbols (7 GB) for one average Ethereum block | One CPU core |
| Irregular Rateless IBLT overhead | Converges to 1.10 (19% lower than regular Rateless IBLT, 10% above the information-theoretic lower bound); encoding/decoding 1.88x slower | c=3 subsets, weights w=(0.18, 0.56, 0.26), alpha=(0.11, 0.68, 0.82), found by brute-force search over simulations, 100 runs per data point |
| Count-field compression | 1.05 bytes per coded symbol on average | Encoding a set of 10^6 items into 10^4 coded symbols, using variable-length quantity encoding of the count-field delta from its expected value |
| Fixed per-symbol overhead | Checksum and count fields together occupy about 9 bytes per coded symbol | Rateless IBLT construction, independent of item length; 4-byte hashes found sufficient to reliably reconcile differences of tens of thousands of items |

### Parameters
- alpha (mapping-probability decay parameter, rho(i) = 1/(1+alpha*i)): set to 0.5 in the final design; optimal value found by search is 0.64 (gives 3% lower overhead but is computationally more expensive per symbol).
- Item length: tested from 8 bytes to 32 KB.
- Set difference size d: tested from 1 to 10^5-10^6 items across different experiments.
- Set size N: tested from 10^4 to 10^8 (Fig. 10) and fixed at 1,000,000 for the main communication-overhead comparison (Fig. 7).
- Hash function for checksums under adversarial workloads: SipHash, a keyed hash function with 64-bit (short) output, keyed per peer pair.
- Irregular Rateless IBLT: c=3 subsets, weights 0.18/0.56/0.26, alpha values 0.11/0.68/0.82 (found by brute-force search, not derived in closed form).
- Regular IBLT and MET-IBLT comparison baselines: 8 bytes allocated for checksum and count fields each, per each scheme's own recommended parameters.

### Stated limitations
Irregular Rateless IBLT has no closed-form parameter derivation; its (c, w_j, alpha_j) configuration was found by brute-force search over simulations, and the authors state they "leave further optimizations of the parameters and the implementation to future works."

The scheme does not address reconciliation across more than two parties simultaneously; the authors list "designing efficient solutions for reconciliation across more than two parties" as future work.

The scheme as analyzed assumes each party's set is static during a reconciliation session; "considering scenarios where Alice and Bob's sets change in the middle of reconciliation" is listed as future work, not solved.

The adversarial-workload defense (keyed hashing) requires the two reconciling peers to share a secret key coordinated in advance; the paper does not specify a key-distribution mechanism, and using a distinct key per peer pair increases the sender's per-peer checksum-computation cost.

Regular (non-rateless) IBLT and MET-IBLT, used as comparison baselines, are stated to fail to decode probabilistically even when correctly parameterized, and MET-IBLT requires selecting a small number of target difference sizes in advance, with 4-10x higher overhead for difference sizes not among those selected.

PinSketch, a comparison baseline, achieves lower communication overhead (the paper reports 37-60% lower) but has quadratic decoding complexity in the number of coded symbols, becoming, in the authors' words, "intractable even at moderate" set and difference sizes.

### Requirements it places on the rest of the system
The transport between the two reconciling peers must preserve ordering of coded symbols, because the receiver reconstructs an implied index i for each coded symbol from position in the stream (after the sender transmits set size N with the 0th symbol) rather than the sender attaching an explicit index to each symbol; this is stated as an assumption for the variable-length count-field compression specifically.

Both peers must independently compute the same deterministic source-to-coded-symbol mapping (same rho(i), same hash functions) for subtraction of their coded symbol sequences to correctly encode the symmetric difference; any divergence in this shared mapping rule breaks the linearity property the scheme depends on.

Defense against adversarial workload requires the two peers to share a secret key for the keyed hash function (SipHash) before reconciliation; without a shared key, an adversary who can inject items into either party's set can construct a hash collision against a target item and permanently block reconciliation of that item (the paper states this failure mode explicitly for the unkeyed case).

The mechanism assumes items are fixed-length bit strings ("bit strings of the same length ℓ"); the paper does not address reconciling variable-length items directly, only fixed-length symbols, so the rest of the system must fix or pad item length before invoking reconciliation.

The receiver must be able to determine when it has recovered every item in the symmetric difference (decoding termination) in order to signal the sender to stop transmitting; the paper's protocol relies on this termination signal traveling back to the sender (Bob "notifies Alice to stop"), requiring a return channel from receiver to sender even though the main data flow is one-directional.

### Contradicts
The paper's own comparison shows PinSketch achieves strictly lower communication overhead (overhead of exactly 1, the information-theoretic optimum, versus Rateless IBLT's 1.35-1.72x) for the same difference sizes (1-400 items, 1,000,000-item sets, 32-byte items) — a reader crediting Rateless IBLT with unconditionally superior performance to all prior schemes would be wrong on the communication-cost axis specifically; the paper's claim is unconditional superiority on computation cost (2-2000x lower) traded against 0-60% higher communication cost depending on scheme compared.

None found against other entries in this corpus.

### References worth retrieving
- Eppstein, David; Goodrich, Michael T.; Uyeda, Frank; Varghese, George. "What's the difference? efficient set reconciliation without prior context." ACM SIGCOMM 2011, pp. 218-229. DOI 10.1145/2018436.2018462 — foundational (defines the regular IBLT construction and recommended parameters this paper builds on and compares against).
- Goodrich, Michael T.; Mitzenmacher, Michael. "Invertible Bloom Lookup Tables." 49th Annual Allerton Conference, IEEE, 2011, pp. 792-799. DOI 10.1109/ALLERTON.2011.6120248 — foundational (introduces IBLTs).
- Lázaro, Francisco; Matuz, Balázs. "A Rate-Compatible Solution to the Set Reconciliation Problem." IEEE Trans. Commun. 71(10), 2023, pp. 5769-5782. DOI 10.1109/TCOMM.2023.3296630 — competing (MET-IBLT, the closest concurrent work; directly compared in Figure 7, 4-10x higher overhead for un-optimized difference sizes).
- Minsky, Yaron; Trachtenberg, Ari; Zippel, Richard. "Set reconciliation with nearly optimal communication complexity." IEEE Trans. Inf. Theory 49(9), 2003, pp. 2213-2218. DOI 10.1109/TIT.2003.815784 — foundational (Characteristic Polynomial Interpolation, CPI; states the information-theoretic lower bound dℓ this paper measures against; already in this corpus).
- Wuille, Pieter. "Minisketch: a library for BCH-based set reconciliation." 2018 — competing (PinSketch implementation used as the low-communication-overhead comparison baseline, deployed in Bitcoin).
- Han, Yilin; Li, Chenxing; Li, Peilun; Wu, Ming; Zhou, Dong; Long, Fan. "Shrec: bandwidth-efficient transaction relay in high-throughput blockchain systems." ACM Symposium on Cloud Computing (SoCC 2020), pp. 238-252. DOI 10.1145/3419111.3421283 — competing/attack (found PinSketch's computation complexity limits blockchain transaction-relay throughput in practice, corroborating this paper's stated PinSketch limitation).
- Lázaro, Francisco; Matuz, Balázs. "Irregular Invertible Bloom Look-Up Tables." 11th International Symposium on Topics in Coding (ISTC 2021), pp. 1-5. DOI 10.1109/ISTC49272.2021.9594198 — foundational (irregular-graph technique this paper's Irregular Rateless IBLT extension applies to the rateless setting).
- Yue, Cong; Xie, Zhongle; Zhang, Meihui; Chen, Gang; Ooi, Beng Chin; Wang, Sheng; [additional authors]. (Merkle trie work) — competing (defines the Merkle trie baseline against which the Ethereum application results are measured).
- Naumenko, Gleb; Maxwell, Gregory; Wuille, Pieter; Fedorova, Alexandra; [additional author]. — foundational/competing, cited regarding difficulty of predicting set-difference size in deployed systems.
- Ozisik, A. Pinar; Andresen, Gavin; Levine, Brian N.; Tapp, Darren; Bissias, George; [additional authors] — foundational/competing, cited alongside difficulty (sometimes stated as impossibility) of predicting set-difference size ahead of time.
- Summermatter, E.; Grothoff, C. "Byzantine Fault Tolerant Set Reconciliation." 2022 — competing (extends set reconciliation to a Byzantine-fault setting, directly relevant to this domain's Byzantine-tolerant replication scope).
- Taverna, Massimiliano; Paterson, Kenneth G. "Snapping Snap Sync." 2023 — attack/competing (cited regarding Geth state-sync bootstrapping consistency, directly relevant to the state heal baseline measured against in this paper).

### Verbatim extracts
- "the first set reconciliation protocol... that achieves low computation cost and near-optimal communication cost"
- "reconciling d differences with 1.35d communication" as d goes to infinity
- "Rateless IBLT achieves 3–4× lower communication cost than non-rateless schemes"
- "2–2000× lower computation cost than schemes with similar communication cost"
- "5.6× lower end-to-end completion time and 4.4× lower communication cost"
- "IBLTs are not rateless."
- "Rateless IBLT has no parameters and does not need an estimate of the set difference size."
- "it takes Rateless IBLT 0.01 second to decode 10^5 differences"
- "we leave further optimizations of the parameters and the implementation to future works"
