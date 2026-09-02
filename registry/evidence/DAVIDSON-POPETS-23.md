## [DAVIDSON-POPETS-23] FrodoPIR: Simple, Scalable, Single-Server Private Information Retrieval
**Citation:** Alex Davidson, Goncalo Pestana, Sofia Celi. "FrodoPIR: Simple, Scalable, Single-Server Private Information Retrieval." Proceedings on Privacy Enhancing Technologies (PoPETs), 2023. DOI 10.56553/POPETS-2023-0022.
**Retrieved:** full text via https://eprint.iacr.org/2022/981.pdf
**Source URL:** https://eprint.iacr.org/2022/981.pdf
**Domain:** G

### What it does
FrodoPIR lets a client download one item from a server-held database, at a server-chosen index, without revealing to the server which index the client read. The server cannot distinguish a query for index i from a query for any other index. The construction splits into an offline phase and an online phase. In the offline phase the server derives a pseudorandom Learning-With-Errors (LWE) matrix A (dimension n times m, from a lambda-bit seed) and multiplies it by the database (arranged as an m by omega matrix D) to produce a public parameter matrix M = A times D; the client independently derives the same A from the published seed and, per future query, samples a secret vector and computes preprocessed values that do not depend on which index will later be queried. Because this preprocessing is client-independent (the server does the same work once no matter how many clients query later) and query-independent (the client does the same work once no matter which index it will later query), a single offline computation amortizes across every client and every query. In the online phase the client picks the actual query index, adds a small correction to one entry of its preprocessed vector, and sends the modified vector; the server computes one vector-matrix multiplication against its database and returns the result; the client subtracts its own secret to recover the requested item. Security rests on the Matrix-LWE assumption: an adversary given the query vector cannot distinguish which index was targeted.

### Measured results
All computation measured single-threaded on an Amazon EC2 t2.2xlarge (8 CPU cores, 32 GB RAM), except Table 7 which uses a c5n.2xlarge to match a comparison paper's hardware. Database elements are 1 KB (w = 2^13 bits) unless stated otherwise. Security parameter n = 1774 (conservative setting for 2^52 client queries at 128-bit security) unless stated otherwise.

Non-amortized performance by database size (Table 6, 1 KB elements, single client, single server, lattice dimension n = 1774):

| log2(m) items | Client download, offline (KB) | DB preprocessing (s) | Client query (KB, online) | Server response (KB, online) | Server response time (ms) |
|---|---|---|---|---|---|
| 16 | 5682 | 104.6 | 256 | 3.203 | 45.0 |
| 17 | 5682 | 206.3 | 512 | 3.203 | 94.5 |
| 18 | 5682 | 429.1 | 1024 | 3.203 | 188.4 |
| 19 | 6313 | 936.4 | 2048 | 3.556 | 417.9 |
| 20 | 6313 | 1895.2 | 4096 | 3.556 | 825.4 |

Server response size grows less than 3.6 times the original 1 KB element across all measured database sizes, versus 128 times for SOnionPIR and 320 times for PSIR at the same 2^20-element database size, comparison run on the same t2.2xlarge hardware with each client making 500 queries.

Financial cost, at $0.09 per GB of server-to-client transfer and $0.0464 per CPU hour (AWS on-demand pricing, August 2022): offline database preprocessing for a 2^20-element database costs slightly above 1 US cent (a one-time, globally amortizable cost); the online per-query cost is about 0.001 cent at the largest measured database size.

Comparison against Spiral (Menon and Wu) on a shared c5n.2xlarge instance, single-threaded, at three database shapes (Table 7):

| Database shape | Metric | Spiral | FrodoPIR |
|---|---|---|---|
| 2^20 items x 256 B | Query size | 14 KB | 4 MB |
| 2^20 items x 256 B | Response size | 20 KB | 912 B |
| 2^20 items x 256 B | Server computation time | 1.37 s | 0.16 s |
| 2^20 items x 256 B | Throughput | 196 MB/s | 1.56 GB/s |
| 2^18 items x 30 KB (FrodoPIR extrapolated from 2^16 items for memory reasons) | Server computation time | 17.69 s | 4.27 s |
| 2^18 items x 30 KB | Throughput | 434 MB/s | 1.76 GB/s |
| 2^14 items x 100 KB | Server computation time | 4.58 s | 0.89 s |
| 2^14 items x 100 KB | Throughput | 358 MB/s | 1.76 GB/s |

FrodoPIR wins on computation throughput at every measured shape; Spiral wins on response-size-to-element ratio and bandwidth when elements are large (30 KB or 100 KB).

Reducing the LWE dimension n from 1774 to 1572 or 1288 (Table 10, log2(m) = 16 and 20, same t2.2xlarge hardware): bandwidth (client download) falls by more than 11% at n = 1572 and by 27% at n = 1288, relative to n = 1774, at both database sizes; client derivation of the matrix A falls by about 20% at the smaller dimensions.

Applied worked example, Google SafeBrowsing-style URL blocklist checking, using a single 2^18-element, 1 KB-element database shard with the parameters of Table 5 at m = 2^18, on the same t2.2xlarge instance (Table 8): offline client download 180 KB, database preprocessing 28.6 s, online client query 1024 KB, online server response 0.1 KB, online server response time 5.223 ms.

Comparison against the two-server PIR constructions of Kogan and Corrigan-Gibbs (dpfPIR, ooPIR) and against the non-private baseline, all scaled to 1 billion users, using each scheme's stated per-query latency to derive server counts (Table 9):

| Indicator | Non-private | dpfPIR (2-server) | ooPIR (2-server) | FrodoPIR (1-server, estimated) |
|---|---|---|---|---|
| Servers needed for 1B users | 143 | 9047 | 1348 | 9778 |
| Latency (ms) | 90 | 122 | 91 | 90 |
| Client running time (s/month) | 0.5 | 0.8 | 8.0 | 1272.0 |
| Online communication (MB/month) | 3.0 | 3.6 | 9.0 | 539.7 |
| Max client storage (MB) | 4.5 | 4.5 | 26.1 | 30.69 |

FrodoPIR's server count and per-client monthly bandwidth are both worse than the two-server schemes in this specific comparison; the paper attributes this to the SafeBrowsing usage pattern (many small, frequent queries against a large database) rather than to a general FrodoPIR weakness, and states this comparison, unlike Table 7, is not a favorable case for FrodoPIR's design.

### Parameters
- LWE modulus q = 2^32 (fixed across all reported parameter sets, chosen to match 32-bit unsigned integer arithmetic).
- LWE dimension n: 1774 used as the primary conservative setting (128-bit security for up to 2^52 client queries); 1572 and 1288 tested as less conservative alternatives (Table 10) trading security margin for bandwidth.
- Plaintext modulus rho: 2^10 for database sizes m <= 2^18, 2^9 for m > 2^18 (Table 5).
- Number of tolerated queries before matrix A must be re-derived, l (script-l): 2^52 in the primary parameter sets.
- Error distribution chi: uniform ternary.
- Element size w: 1 KB (2^13 bits) in the main experiments (Section 6); 256 B, 30 KB, and 100 KB tested in the Spiral comparison (Table 7).
- Per-client number of preprocessed queries c: 500, fixed across the amortization comparisons with SOnionPIR and PSIR.
- Improvement factor kappa = (log(rho) times m) / (n times log(q)): reported as 13.0 to 187.6 across the five parameter rows of Table 5, rising with m.

### Stated limitations
The paper states the main limitation of FrodoPIR is that online client query size grows linearly in the database size m, unlike SOnionPIR and PSIR whose online query sizes grow more slowly; at m = 2^20, the client query reaches 4 MB. A second stated limitation is that the server's transformed database representation is roughly 3 times the size of the original database. The paper states this can be mitigated (query size, not the 3x storage factor) by sharding the database into s parallel instances, at the cost of a client download that grows by a factor of s and a public-parameter download per shard. The paper states it does not provide a fully optimized implementation: it explicitly excludes computational optimizations such as sub-cubic matrix multiplication and query batching, leaving them as unexplored future work. The paper states it does not evaluate the "DoublePIR" optimization of concurrent work (Henzinger et al.) applied to FrodoPIR, though it states the underlying observation should apply. The paper states its security analysis assumes a semi-honest (not malicious) server, and that no attack against the specific Matrix-LWE variant used is currently known, but does not prove none exists.

### Requirements it places on the rest of the system
The client must know, before the online phase, the specific numeric index it wants to query; the paper states elsewhere (Section 7, referring to Kogan and Corrigan-Gibbs) that mapping a real-world key (such as a URL hash) to that index requires a separate mechanism the client downloads out of band, distinct from the FrodoPIR protocol proper. The scheme requires an offline phase before any query: the client must download the server's public parameters (the seed and matrix M) before making its first query, so a client cannot query cold. Database updates require the server to redistribute updated public parameters for whichever shard changed, and require every client to re-run preprocessing for that shard before it can query updated data; this couples update frequency to client-side computational and bandwidth allowance. The security guarantee (128-bit, against up to 2^52 or 2^32 queries depending on chosen n) decays as the server answers more queries against the same matrix A, and the server must eventually resample A to reset the guarantee; the paper assumes, under its semi-honest model, that the server does this resampling honestly. The scheme provides no defense if multiple non-colluding servers are required elsewhere in a design: it is explicitly single-server, so a system relying on FrodoPIR cannot also assume the multi-server non-collusion property that dpfPIR and ooPIR rely on.

### Contradicts
None found within this corpus at time of writing. The paper's own Table 9 comparison contradicts an unqualified claim that FrodoPIR is cheaper than multi-server PIR in general: for the SafeBrowsing workload specifically, FrodoPIR uses more servers, more client compute time per month, and more monthly bandwidth than the two-server dpfPIR and ooPIR schemes of Kogan and Corrigan-Gibbs. The general throughput and financial-cost advantage claimed in Sections 6.1-6.2 holds against single-server stateful competitors (SOnionPIR, PSIR) under the amortized multi-client comparisons, not against multi-server schemes.

### References worth retrieving
- foundational: A. Henzinger, M. M. Hong, H. Corrigan-Gibbs, S. Meiklejohn, V. Vaikuntanathan. "One server for the price of two: Simple and fast single-server private information retrieval" (SimplePIR/DoublePIR), Cryptology ePrint 2022/949 — concurrent work using the same LWE mechanism; not yet in this corpus.
- competing: M. H. Mughees, H. Chen, L. Ren. "OnionPIR: Response efficient single-server PIR" — this is the SOnionPIR baseline compared against in Figures 6-7.
- competing: S. Patel, G. Persiano, K. Yeo. "Private stateful information retrieval" (PSIR) — the second single-server baseline compared against.
- competing: S. J. Menon, D. J. Wu. "SPIRAL: fast, high-rate single-server PIR via FHE" — the Table 7 comparison target for large database elements.
- competing: H. Corrigan-Gibbs, A. Henzinger, D. Kogan. "Single-server private information retrieval with sublinear amortized time" (CHKPIR), EUROCRYPT 2022 — the sublinear-online-time comparison in Section 6.2.
- competing: D. Kogan, H. Corrigan-Gibbs. Two-server PIR constructions (dpfPIR, ooPIR) for SafeBrowsing, cited as [54] — source of the Table 9 comparison numbers and the usage-model assumptions (query rate, update rate) FrodoPIR's SafeBrowsing example reuses.
- foundational: E. Boyle, N. Gilboa, Y. Ishai. "Function secret sharing: Improvements and extensions" — underlies distributed-point-function PIR-by-keyword approaches discussed as an alternative to FrodoPIR's index-based model.
- attack: M. R. Albrecht, R. Player, S. Scott. "On the concrete hardness of learning with errors" — the lattice-hardness estimator FrodoPIR's security parameters are derived from.

### Verbatim extracts
- "requires < 1 second for responding to a client query...financial costs are ∼ $1 for answering 100,000 client queries."
- "the server response size compared with the original 1KB data element" grows "< 3.6× overhead."
- "SOnionPIR (128×) and PSIR (320×)" response-size overhead at the same database size.
- "Clearly, FrodoPIR involves heavier usage costs compared to all known solutions" (SafeBrowsing comparison).
- "The main limitation of the FrodoPIR approach is that online client queries are linear in the size of the database."
