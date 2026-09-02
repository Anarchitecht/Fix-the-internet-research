## [LUBY-FOCS-02] LT Codes
**Citation:** Michael Luby. "LT Codes." IEEE Symposium on Foundations of Computer Science (FOCS), 2002. DOI: 10.1109/SFCS.2002.1181950.
**Retrieved:** full text via https://doi.org/10.1109/SFCS.2002.1181950 (matching PDF text; ICSI tech-report mirror also listed in target record)
**Source URL:** https://doi.org/10.1109/SFCS.2002.1181950
**Domain:** C

### What it does
An LT (Luby Transform) code lets a sender produce an unbounded stream of coded symbols from k source symbols, so that a receiver who collects any sufficient set of coded symbols — regardless of which ones were lost in transit — recovers all k source symbols. The sender needs no advance estimate of the channel loss rate, because it stops generating symbols only when the receiver signals it has decoded, or after a fixed number if the channel is one-way.
Encoding one symbol: draw a degree d from a fixed degree distribution, choose d distinct source symbols uniformly at random as neighbors, and exclusive-or (XOR) them together to form the symbol value. Each encoded symbol carries or implies its degree and neighbor list (by explicit list, by a shared pseudo-random seed keyed to the symbol, or by reception order), so the decoder can reconstruct the encoding graph.
Decoding: repeatedly find an encoded symbol with exactly one not-yet-recovered neighbor, set that source symbol equal to the encoded symbol's value (adjusting for already-recovered neighbors already XORed out), then remove that source symbol as a satisfied neighbor from every other encoded symbol referencing it. The paper calls the set of encoded symbols currently reducible to degree one the "ripple." Decoding succeeds only while the ripple never empties before all k source symbols are recovered.
The central design problem is the degree distribution: it must keep the ripple non-empty with high probability throughout decoding while using as few total encoded symbols as possible. The paper introduces the Ideal Soliton distribution (ρ(1) = 1/k; ρ(i) = 1/(i(i−1)) for i = 2..k) as the distribution that makes the expected total received-symbol count exactly k, but states it fails in practice because the ripple's expected size (one) has too much variance and disappears with realistic probability. The Robust Soliton distribution (Definition 11) adds a spike term τ(i) to ρ(i), parameterized by a target failure probability δ and a constant c, engineered to keep the expected ripple size near c·ln(k/δ)·sqrt(k) throughout the process.

### Measured results
This is a theoretical paper: every quantitative claim is a proved asymptotic bound, not an empirical measurement from an implementation or simulation run. The paper states explicitly (Section 3.4) that its proofs use pessimistic estimates chosen for provability, and that better constants are attainable "based on computer simulations" whose description it places out of scope. No simulation parameters, node counts, or run counts are given anywhere in the text.

| Bound (Robust Soliton distribution, over k source symbols, target failure probability δ) | Statement |
|---|---|
| Number of encoded symbols needed for successful decoding with probability ≥ 1 − δ (Theorem 12) | K = k + O(sqrt(k) · ln²(k/δ)) |
| Average degree of an encoded symbol (Theorem 13) | D = O(ln(k/δ)) |
| Average symbol operations (XORs/copies) per generated encoded symbol | O(ln(k/δ)) |
| Total decoder symbol operations | O(k · ln(k/δ)) |
| Decoding failure probability from K encoded symbols (Theorem 17) | at most δ |

Comparative bound against a degree-one-only ("All-At-Once") baseline: both require the same total sum of encoded-symbol degrees, approximately k·ln(k/δ), but the Robust Soliton distribution concentrates that degree sum into close to the minimum possible number of encoded symbols, while the all-degree-one baseline needs one encoded symbol per unit of degree.

### Parameters
- k: number of source symbols. Free parameter, arbitrary.
- δ: target decoding-failure probability. Free parameter chosen by the implementer; appears in every asymptotic bound above.
- R = c · ln(k/δ) · sqrt(k), for a "suitable constant c > 0": the target ripple size in the Robust Soliton distribution. The paper does not state a numeric value for c; it is left as a free constant in the construction (labeled here as NOT DERIVED for our purposes — the paper gives no worked value or measured range).
- Symbol length ℓ: stated to be arbitrary, from single-bit to general ℓ-bit symbols; the paper notes only that per-symbol overhead makes the scheme "efficient in practice for larger values of ℓ" without giving a threshold.

### Stated limitations
The paper states the Ideal Soliton distribution "works poorly in practice" because its expected ripple size of one is too small and any downward variation empties it, failing decoding. The Robust Soliton analysis is explicitly pessimistic ("in several places we make pessimistic estimates that enable a simple, comprehensive, and complete analysis"); the authors state that heuristic, simulation-based tuning gives lower reception overhead and average degree than the proved bounds, but state that description is beyond the paper's scope. The paper does not analyze or bound encoding/decoding time for non-Robust-Soliton distributions, does not address adversarial manipulation of received symbols, and gives no networking-layer mechanism for signaling degree/neighbor metadata beyond listing candidate options (explicit lists, timing-based implicit computation, or a shared-seed keyed function) without recommending one.

### Requirements it places on the rest of the system
- The encoder and decoder must agree on the same degree distribution (the Robust Soliton distribution, parameterized by k and δ) before encoding begins; this is stated as the only required preprocessing.
- The decoder must be able to determine, for each received encoded symbol, its degree and its exact set of neighbor source-symbol indices — the paper requires this metadata to reach the decoder but leaves the transport mechanism open (explicit signaling, deterministic ordering, or a shared pseudo-random seed correlated with the symbol).
- The channel is assumed to be an erasure channel: received symbols are assumed correct (not corrupted), only some are assumed lost; the paper gives no integrity-check or authentication mechanism for encoded symbols.
- Decoding requires collecting K = k + O(sqrt(k)·ln²(k/δ)) encoded symbols from any subset the channel delivers; nothing in the mechanism enforces or verifies which subset arrives, so the surrounding transport must ensure the receiver eventually accumulates that many distinct symbols (via retransmission, a return channel, or an assumption of sufficient redundancy).
- The source data must be pre-partitioned into k equal-length symbols before encoding; the paper does not address padding, symbol-length negotiation, or variable-length objects.

### Contradicts
None found within this corpus; no other entry addresses fountain codes with conflicting figures.

### References worth retrieving
- foundational: J. Byers, M. Luby, M. Mitzenmacher, A. Rege, "A Digital Fountain Approach to Reliable Distribution of Bulk Data," ACM SIGCOMM 1998, pp. 56-67 — origin of the "digital fountain" concept LT codes realize.
- foundational: M. Luby, M. Mitzenmacher, A. Shokrollahi, D. Spielman, V. Stemann, "Practical Loss-Resilient Codes," ACM STOC 1997 — Tornado codes, the fixed-rate predecessor whose degree-distribution technique LT codes generalize to the rateless setting.
- foundational: M. Luby, M. Mitzenmacher, A. Shokrollahi, D. Spielman, "Efficient Erasure Correction Codes," IEEE Trans. Information Theory 47(2), 2001 — Tornado codes' full analysis, cited for the linear-time encode/decode comparison baseline.
- competing: I. S. Reed, G. Solomon, "Polynomial Codes Over Certain Finite Fields," J. Soc. Indust. Appl. Math 8, 1960 — Reed-Solomon codes, the fixed-rate optimal-recovery baseline this paper compares encode/decode time against.
- foundational: M. Luby, M. Mitzenmacher, A. Shokrollahi, "Analysis of Random Processes via And-Or Tree Evaluation," ACM-SIAM SODA 1998 — analytical technique referenced for degree-distribution proofs.
- competing: J. W. Byers, J. Considine, M. Mitzenmacher, S. Rost, "Informed Content Delivery Across Adaptive Overlay Networks," ACM SIGCOMM 2002 — contemporary overlay-based bulk-data delivery using erasure coding.

### Verbatim extracts
- "LT codes are the first realization of a class of erasure codes that we call universal erasure codes."
- "the k original input symbols can be recovered from any k+O(√k ln²(k/δ)) of the encoding symbols with probability 1 − δ"
- "Although the Ideal Soliton distribution works poorly in practice, it does give insight into a robust distribution."
- "Heuristic techniques can be used to provide a design and analysis that leads to lower reception overhead and average degree based on computer simulations"
- "LT codes are not systematic."
