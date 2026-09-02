## [ZHOU-SP-24] Piano: Extremely Simple, Single-Server PIR with Sublinear Server Computation
**Citation:** Mingxun Zhou, Andrew Park, Wenting Zheng, Elaine Shi. "Piano: Extremely Simple, Single-Server PIR with Sublinear Server Computation." IEEE Symposium on Security and Privacy, 2024. DOI 10.1109/SP54263.2024.00055.
**Retrieved:** full text via https://eprint.iacr.org/2023/452.pdf
**Source URL:** https://eprint.iacr.org/2023/452.pdf
**Domain:** G

### What it does
Piano lets a client fetch one entry from a server-held database of n entries while hiding from the server which entry it fetched, without the server running a scan whose cost grows linearly with n on every query. Piano is single-server private information retrieval (PIR): one server holds the whole database in the clear and the privacy guarantee holds against that one server, unlike multi-server PIR schemes that split trust across several non-colluding servers. Piano uses the client-specific preprocessing model: before making queries, the client downloads a linear-size stream of the database once and derives from it a set of "hints," compact enough to store client-side, that let later individual queries be answered with sublinear server work.

Mechanism. The database indices 0..n-1 are divided into sqrt(n) chunks of sqrt(n) entries each. A "hint" is a randomly chosen set S containing exactly one index from every chunk, together with the parity (XOR) of the database bits at those sqrt(n) indices. The client's local state (learned during one linear streaming pass over the database) is three tables: a primary table of order sqrt(n) such hints (compressed to a short pseudorandom-function, PRF, key per hint rather than the raw index set, cutting client storage from O(n) to order sqrt(n)); a set of order-1 replacement entries per chunk, each storing one raw (index, value) pair; and a backup table of order-1 spare hints per chunk for reuse across future queries. To answer a query for index x, the client finds the primary-table hint whose set S contains x, sends the server a modified set (S with x replaced by a fresh random index drawn from x's own chunk), and the server returns the parity of the database bits at exactly that modified set — one round trip, one message each way. The client then recovers DB[x] by XORing the returned parity against the parity it already held for its original, unmodified set, using its own replacement-entry value for x's chunk. After the query, the client consumes one backup-table entry to refresh the hint that was spent, so it is never queried twice with the same set — this refresh is what keeps the distribution of sets the server sees indistinguishable from uniformly random across many queries, which is the privacy argument (Theorem 3.2, proof sketched in the paper, full proof in its Appendix C).

The privacy definition (Definition 3.1) is against a server acting as a probabilistic polynomial-time adversary that may deviate arbitrarily from the protocol and adaptively choose each next query — not merely an honest-but-curious server that follows the protocol.

The preprocessing pass to learn the hints takes O(n) server and client computation but is amortized over the roughly sqrt(n)·ln(n) queries the resulting hint set supports, giving amortized order sqrt(n) computation per query on both sides, order sqrt(n) online communication per query, and order sqrt(n) client storage. The paper proves this matches, up to poly-logarithmic factors, the Corrigan-Gibbs–Henzinger–Kogan lower bound that client storage S and amortized server computation T must satisfy S·T = Omega(n) for any PIR scheme (a bound the paper cites as [CHK22], not reproved here). The only cryptographic primitive Piano needs is a pseudorandom function, which the implementation instantiates with AES via AES-NI hardware acceleration; the paper states this is the first single-server PIR scheme with sublinear server computation built from one-way functions alone, without homomorphic encryption or privately programmable/puncturable PRFs.

Section B.2 (appendix) describes extending the static scheme to a dynamic database supporting Insert, Update, and Delete, using a hierarchical multi-level structure in which the client always keeps the most recent Q updates locally and at the server, merging levels periodically; the merge and rebuild costs are amortized over the update stream the same way preprocessing is amortized over queries.

### Measured results

| Metric | 1 GB (n=2^27, 8-byte entries) | 2 GB (n=2^28, 8-byte entries) | 100 GB (n≈1.68×10^9, 64-byte entries) |
|---|---|---|---|
| Preprocessing client time, SimplePIR vs Piano | 293s / 629s (1 thread), 111s (8 threads) | 608s / 1471s (1 thread), 257s (8 threads) | 425 min / 192 min (1 thread), 32 min (8 threads) |
| Preprocessing communication, SimplePIR vs Piano | 123MB / 1GB | 173MB / 2GB | 1.2GB / 100GB |
| Online time per query, SimplePIR vs Piano | 131.6ms / 3.0ms | 219.5ms / 3.4ms | 10.9s (extrapolated) / 11.9ms |
| Online communication per query, SimplePIR vs Piano | 238KB / 32KB | 338KB / 64KB | 2.3MB / 100KB |
| Client storage, SimplePIR vs Piano | 123MB / 61MB | 173MB / 71MB | 1.2GB / 839MB |

Conditions: two AWS m5.8xlarge instances, 128GB RAM each; local-area-network figures run on a single machine; SimplePIR figures use the open-source implementation from Henzinger et al.; the 100GB SimplePIR column is extrapolated, not measured, because the open-source SimplePIR implementation does not support a database that large or cross-machine connections; online-time figures are averaged over 1,000 queries; amortization is over Q = sqrt(n)·ln(n) queries. For 1GB/2GB, Piano is 43.9x-64.6x faster than SimplePIR on online query latency; at 100GB, the gap widens to about 915x (11.9ms vs the extrapolated 10.9s).

Wide-area-network experiment: server on the US west coast, client on the US east coast, TLS over a 2Gbps link, round-trip time about 60ms, 1,000-query average. For the 100GB database (64-byte entries): non-private baseline 61.0ms online time, SimplePIR 10.9s (extrapolated), Piano 72.6ms online time, 100KB online communication, 839MB client storage. Piano's online time is a 7%-20% latency overhead versus the non-private baseline across the tested sizes; SimplePIR's overhead over the same baseline is 4.6x-178.7x. In the paper's headline figure for this setup, Piano achieves 73ms response time for the 100GB database at 60ms RTT, versus an 11s-or-more extrapolated figure for SimplePIR, a claimed 150x+ speedup, and a 1.2x slowdown relative to the non-private baseline.

Comparison against TreePIR (two-server, non-colluding-server model, not single-server): for an 8GB database with 2^28 entries, TreePIR's best reported amortized online time is 23ms (non-recursive variant) or 84ms (recursive variant with poly-logarithmic communication); Piano reports an amortized 8ms per query under the same database size, at 4x TreePIR's local client storage (the paper attributes the extra storage to Piano's backup hints and setup-phase deamortization, both required only in the single-server setting).

### Parameters
- Chunk size: 2·sqrt(n), rounded up to the nearest power of 2 (for efficient modulo). Set size follows from chunk size; the paper states performance is more sensitive to set size than chunk size, and chunk size does not change the asymptotics.
- Q (queries supported per preprocessing round): sqrt(n)·ln(n).
- Statistical security parameter kappa = 40.
- Computational security parameter lambda = 128.
- PRF keys: 128 bits, instantiated with AES (AES-NI hardware acceleration).
- M1 (primary table size) = sqrt(n)·ln(kappa·alpha(kappa)); M2 (backup entries per chunk) = 3·ln(kappa·alpha(kappa)), where alpha(kappa) is any super-constant function of kappa — used in the correctness proof (Theorem 3.3/C.3) to bound failure probability by 2^-kappa across all Q queries, matching SimplePIR's target failure probability.
- Optimization tested: a single lambda-bit master PRF key plus a unique 32-bit tag per hint (instead of one full PRF key per hint), measured to cut client storage by 30% and give a 2-3x concrete speedup in PRF evaluation.
- Database index width in the implementation: 64-bit integers.
- Implementation size: about 800 lines of Go for the full scheme; about 160 lines for a separate tutorial-only reference implementation.
- Preprocessing parallelization: client-side preprocessing parallelized across 8 threads in the reported experiments (server-side and online computation stay single-threaded).

### Stated limitations
The paper states Piano's main limitation is communication cost: the client must download the entire database once during setup, and per-query online communication is order sqrt(n), worse than prior theoretical schemes ([ZLTS23], [LP22], cited by the paper as achieving order-1 (up to poly-logarithmic factors) communication per query). The paper states this tradeoff is deliberate: avoiding fully homomorphic encryption (FHE) during the offline phase, and avoiding privately programmable PRFs (needed by the order-1-communication schemes and, the paper states, known only in theory, not as a practical primitive), are what make Piano concretely implementable. The paper states that a single-server PIR scheme with order-1 communication that is also practical is an open question for future work.

Batch PIR schemes (an alternative approach the paper compares against but does not implement) are stated to have two limitations Piano avoids: they need many parallel queries submitted simultaneously to amortize server cost (only at about sqrt(n) parallel queries does the amortized time match Piano, per the paper's analysis), and they still require the server to run homomorphic-encryption evaluation over the full database per batch, an O(n) server operation, versus Piano's order-sqrt(n) plaintext-only server operation.

The dynamic-database extension (Appendix B.2) is described as "not hard" to build via a hierarchical structure but is not evaluated experimentally in this paper — no measured figures are given for update throughput or dynamic-scheme performance.

### Requirements it places on the rest of the system
- A single server holds the full database in the clear; Piano's privacy guarantee is a property of client-server interaction, not of splitting the database across non-colluding servers, so anything that requires multi-server non-collusion assumptions (e.g., two-server PIR) is a different deployment model with different trust requirements.
- The client must complete a one-time (and periodically repeated) linear streaming pass over the entire database — full download or full network scan — before any query benefits from the sublinear-computation property; a client that cannot download order-n data at setup (or every ~sqrt(n)·ln(n) queries thereafter) cannot use this scheme as described.
- Client-side storage of order sqrt(n) (839MB for the 100GB/1.68-billion-entry configuration tested) must be available and persist between queries; losing the local hint tables between queries forces a fresh preprocessing pass.
- The scheme assumes queries within one preprocessing window are not repeated/duplicated (the correctness proof, Theorem C.3, explicitly assumes the client does not make duplicate queries among the Q queries covered by one preprocessing round); a system that needs to re-query the same index inside one window is outside what the stated correctness bound covers.
- The database is treated as static bits indexed 0..n-1 for the core scheme; a caller needing inserts, updates, or deletes must adopt the separate hierarchical dynamic-database construction in Appendix B.2, which the paper does not benchmark.
- Preprocessing communication equals a full database download (100GB for the 100GB-database test), so the network and storage budget for the initial (and periodic) sync must accommodate transferring the entire dataset, not just per-query traffic.

### Contradicts
None found. The 100GB SimplePIR figures used for comparison are the paper's own extrapolation, not a measurement of a run SimplePIR actually completed at that size — that qualifier is stated in the paper's own footnote and is preserved above rather than presented as a direct measurement.

### References worth retrieving
- foundational: Beimel, Ishai, Malkin, "Reducing the Servers' Computation in Private Information Retrieval: PIR with Preprocessing" [BIM00] — proves the linear-server-computation lower bound for PIR without preprocessing that motivates this entire line of work.
- foundational: Chor, Goldreich, Kushilevitz, Sudan, "Private Information Retrieval" [CGKS95] — originates the PIR problem.
- competing: Henzinger, Hong, Corrigan-Gibbs, Meiklejohn, et al., "One Server for the Price of Two: Simple and Fast Single-Server Private Information Retrieval" (SimplePIR) [HHCG+22] — the paper's own primary experimental baseline throughout, state-of-the-art linear-server-computation single-server PIR.
- competing: Corrigan-Gibbs, Henzinger, Kogan, "Single-Server Private Information Retrieval with Sublinear Amortized Time" [CHK22] — source of the S·T = Omega(n) lower bound Piano claims to match, and a competing sublinear-server-computation scheme using linear homomorphic encryption at worse asymptotics (order n^(2/3) client storage/server computation).
- competing: Zhou, Lin, Tselekounis, Shi, "Optimal Single-Server Private Information Retrieval" [ZLTS23] and Lazzaretti, Papamanthou, "Single-Server PIR with Sublinear Communication and Computation" [LP22] — theoretical schemes achieving order-1 communication per query that Piano explicitly trades away for practicality.
- competing: Lazzaretti, Papamanthou, "TreePIR: Sublinear-Time and Polylog-Bandwidth Private Information Retrieval from DDH" [LP23] — two-server model competitor with the closest measured online-time figures (23ms/84ms at 8GB) cited directly against Piano's 8ms at the same size.
- competing: Corrigan-Gibbs, Kogan, "Private Information Retrieval with Sublinear Online Time" [CK20] — introduces the client-side-preprocessing idea in the two-server model that Piano's single-server scheme is compared against.
- foundational: Lin, Mook, Wichs, "Doubly Efficient Private Information Retrieval and Fully Homomorphic RAM Programs from Ring LWE" [LMW22] — global-preprocessing-model breakthrough cited for its server-storage/communication tradeoff.
- attack (lower bound, not an attack on a deployment but a negative result relevant to any order-1-communication claim): the [CHK22] lower bound already listed above.

### Verbatim extracts
- "Piano is the first practical single-server sublinear-time PIR scheme"
- "we outperform the state-of-the-art single-server PIR by 40x-900x"
- "for a 100GB database and with 60ms round-trip latency, Piano achieves 73ms response time"
- "the only cryptographic primitive we need is pseudorandom functions (PRFs)"
- "if the client stores S bits and the amortized server computation time is T, it must be that ST = Omega(n)"
- "The main limitation of Piano is its communication cost"
- "the client has to download the whole database during the setup phase"
