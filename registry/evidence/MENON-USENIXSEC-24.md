## [MENON-USENIXSEC-24] YPIR: High-Throughput Single-Server PIR with Silent Preprocessing
**Citation:** Samir Jordan Menon, David J. Wu. "YPIR: High-Throughput Single-Server PIR with Silent Preprocessing." USENIX Security Symposium, 2024.
**Retrieved:** full text via https://eprint.iacr.org/2024/270.pdf
**Source URL:** https://eprint.iacr.org/2024/270.pdf
**Domain:** G

### What it does
Single-server private information retrieval (PIR) schemes built on a precomputed "hint" (SimplePIR,
DoublePIR — see HENZINGER-USENIXSEC-23 in this corpus) reach high throughput but require the client
to download that hint — tens to hundreds of megabytes — in an offline phase before any query, and to
re-download it whenever the underlying database changes. YPIR removes that offline hint download
entirely while keeping throughput close to DoublePIR's, a property the paper calls "silent
preprocessing": the server still performs a one-time preprocessing pass over the database, but the
client needs no offline communication with the server to obtain the result of that preprocessing.

Mechanism: YPIR runs the DoublePIR protocol (client sends learning-with-errors (LWE) encryptions of
two indicator vectors selecting a row and column of the database matrix; server computes the
response using its precomputed database-derived state) and then appends a post-processing step that
compresses DoublePIR's response before sending it. DoublePIR's response, absent this step, consists
of kappa*(n+1)^2 elements over Z_q (n the LWE lattice dimension, around 1024 for target security
levels, kappa = log(q)/log(p)), because each element of the response is itself an LWE-encrypted LWE
ciphertext; most of this response depends only on the database, not the query, and prior work
(SimplePIR/DoublePIR) prefetched that database-dependent portion offline as the hint. YPIR instead
compresses the DoublePIR response online using ring learning-with-errors (RLWE, operating over a
polynomial ring R = Z[x]/(x^d+1)) via an LWE-to-RLWE packing transformation adapted from Chen, Dai,
Kim, Song (CDKS21). Packing d LWE ciphertexts encoding d messages under key s produces a single RLWE
ciphertext encoding the same d messages as a polynomial under a derived key, taking d(d+1) elements
over Z_q down to 2d elements — for d approximately 1024, roughly a 1000x reduction in ciphertext
expansion factor. The query must now include a "packing key" — RLWE key-switching matrices the
server needs to perform this transformation — which increases query size relative to DoublePIR
(reported as a 2x increase, from 724 KB to 1.5 MB for an 8 GB database). Because the packing
transformation is applied to query-independent components, most of its computational cost can be
moved to the server's offline preprocessing phase; the paper reports a 9x reduction in online
computation from doing this. A variant, YPIR+SP, applies the same packing approach to SimplePIR
instead of DoublePIR, extending support to large records (plain DoublePIR supports only
single-element-of-Z_p records).

Application (Certificate Transparency signed-certificate-timestamp (SCT) auditing, following the
Bloom-filter-based approach of Henzinger et al., HENZINGER-USENIXSEC-23 in this corpus): a log
operator encodes the roughly five billion currently active SCTs as an 8 GB (2^36-bit) database; each
audit is a single PIR query against that database. Because YPIR needs no offline hint, clients can
audit against the log's current state without waiting for a periodic hint refresh, unlike the
DoublePIR-based deployment this paper compares against, which the authors state does not support
real-time auditing because its update strategy is a weekly hint refresh.

### Measured results
All measurements: AWS EC2 r6i.16xlarge instance, Ubuntu 22.04, 64 vCPUs (Intel Xeon Platinum 8375C
at 2.9 GHz), 512 GB RAM, single-threaded execution, GCC 11, AVX2/AVX-512 SIMD enabled, runtimes
averaged over at least 5 sample runs with standard deviation at most 5%. Reference implementations
benchmarked on the same machine: SimplePIR/DoublePIR (commit e9020b0), Tiptoe's PIR scheme (commit
f053a81), HintlessPIR (commit 4be2ae8). YPIR itself: 3,000 lines of Rust plus a 1,000-line C++ kernel
for 32-bit matrix multiplication adapted from the public SimplePIR implementation.

| Database | Metric | SimplePIR | DoublePIR | Tiptoe | HintlessPIR | YPIR |
|---|---|---|---|---|---|---|
| 1 GB | Prep. throughput | 3.7 MB/s | 3.4 MB/s | 1.6 MB/s | 4.8 MB/s | 39 MB/s |
| 1 GB | Offline download (hint) | 121 MB | 16 MB | none | none | none |
| 1 GB | Upload | 120 KB | 312 KB | 33 MB | 488 KB | 846 KB |
| 1 GB | Download | 120 KB | 32 KB | 2.1 MB | 1.7 MB | 12 KB |
| 1 GB | Server time | 74 ms | 94 ms | 2.47 s | 743 ms | 129 ms |
| 1 GB | Throughput | 13.6 GB/s | 10.6 GB/s | 415 MB/s | 1.3 GB/s | 7.8 GB/s |
| 8 GB | Prep. throughput | 3.1 MB/s | 2.9 MB/s | 1.6 MB/s | 5.2 MB/s | 46 MB/s |
| 8 GB | Offline download (hint) | 362 MB | 16 MB | none | none | none |
| 8 GB | Upload | 362 KB | 724 KB | 33 MB | 1.4 MB | 1.5 MB |
| 8 GB | Download | 362 KB | 32 KB | 8.6 MB | 1.7 MB | 12 KB |
| 8 GB | Server time | 708 ms | 845 ms | 9.75 s | 1.62 s | 687 ms |
| 8 GB | Throughput | 11.3 GB/s | 9.5 GB/s | 840 MB/s | 4.9 GB/s | 11.6 GB/s |
| 32 GB | Prep. throughput | 3.3 MB/s | 3.3 MB/s | 1.4 MB/s | 5.7 MB/s | 48 MB/s |
| 32 GB | Offline download (hint) | 724 MB | 16 MB | none | none | none |
| 32 GB | Upload | 724 KB | 1.4 MB | 34 MB | 2.4 MB | 2.5 MB |
| 32 GB | Download | 724 KB | 32 KB | 17 MB | 3.2 MB | 12 KB |
| 32 GB | Server time | 3.08 s | 3.22 s | 21.00 s | 5.00 s | 2.64 s |
| 32 GB | Throughput | 10.4 GB/s | 9.9 GB/s | 1.5 GB/s | 6.4 GB/s | 12.1 GB/s |

All figures for retrieving a single-bit record (each YPIR response encodes an element of Z_p; for
the paper's parameters each record is 8 bits). SimplePIR and DoublePIR figures in this table use the
reference implementation's own parameter choices; the paper also reports SimplePIR*/DoublePIR* (its
own re-implementation using YPIR's lattice parameters, Table 1) as a fairer comparison, finding YPIR
10% slower than SimplePIR*/DoublePIR* at 8 GB and 1% slower at 32 GB.

Scaling behavior: for a 1 GB database YPIR's throughput is 43% slower than SimplePIR and 26% slower
than DoublePIR, attributed to the LWE-to-RLWE transformation taking 30% of query-processing time at
that size (a cost roughly independent of database size); at 8 GB YPIR's throughput is 3-18% faster
than the reference SimplePIR/DoublePIR implementations and reaches 79% of the test machine's memory
bandwidth. At 32 GB, YPIR reaches 12.1 GB/s, stated as 97% of SimplePIR's throughput and 83% of
memory bandwidth. Compared to Tiptoe, YPIR is 8-19x faster (Tiptoe spends over 85% of its server time
on its own LWE-to-RLWE conversion, which YPIR needs only 1-10% of its own time for on large
databases). Compared to HintlessPIR, YPIR is 2-6x faster (peak 12.1 GB/s versus HintlessPIR's peak
6.4 GB/s); the gap is attributed to HintlessPIR packing O(sqrt(N)) LWE encodings (roughly 50% of its
time at 32 GB) where YPIR packs a fixed number of encodings independent of database size (1% of its
time at 32 GB).

Communication trade-offs: YPIR queries are 1.8-2.7x larger than DoublePIR's and 3.5-7x larger than
SimplePIR's; YPIR responses are 2.7x smaller than DoublePIR's and 10-60x smaller than SimplePIR's.
Total online communication (upload plus download) for YPIR is 1.8-3.6x larger than SimplePIR's and
1.8-2.5x larger than DoublePIR's, but YPIR needs no hint at all, versus a 724 MB hint (SimplePIR) or
16 MB hint (DoublePIR) for a 32 GB database; a client would need 681 queries to SimplePIR or 15
queries to DoublePIR before their cumulative communication exceeds YPIR's fixed per-query cost.
Compared to HintlessPIR, YPIR queries are 1.7-3x larger and responses are 125x smaller.

Large-record variant (YPIR+SP versus HintlessPIR, 32 KB records, 1 GB and 8 GB databases): YPIR+SP
has 6-15x smaller responses, similar query size, and similar throughput. For checking a password
against a set of 1 billion compromised credentials, YPIR+SP achieves 2.2x lower total communication
(7.4x smaller responses) at a less than 5% throughput reduction compared to HintlessPIR.

Certificate Transparency SCT-auditing cost estimate (AWS pricing at time of writing: $0.09/outbound
GB, $1.5x10^-5/core-second, inbound free; client model following Henzinger et al. and Chrome's own
usage assumption: 10^4 TLS connections/week, audits on a 1/1000 fraction of connections at 2 audits
each, totaling 20 PIR queries/week over an 8 GB database):

| Scheme | Weekly comm. cost/client-million | Weekly compute cost/client-million | Total weekly cost/client-million |
|---|---|---|---|
| DoublePIR, weekly hint download | $0.001569-derived total $1,822 (per HHC+23a instantiation) | included in total | $1,822 |
| DoublePIR, daily hint updates | higher (over 80% of weekly-download cost is the 16 MB hint) | — | $10,863 |
| YPIR | — | — | $228 |
| YPIR with cross-client batching (queue size 4) | — | — | $183 |

YPIR is stated as 8x cheaper than weekly-refresh DoublePIR and over 48x cheaper than daily-refresh
DoublePIR for this SCT-auditing workload; Tiptoe and HintlessPIR are also hint-free but the paper's
own Table 6 breakdown (not fully reproduced here) shows YPIR's lower per-query cost among the
hint-free schemes given its smaller response size.

### Parameters
Correctness error target: delta <= 2^-40 (Table 1). Security target: 128 bits. Lattice dimension n
approximately 1024 (n coincides with the RLWE ring dimension d in the packing step). Database unit
convention: KB/MB/GB denote 2^10/2^20/2^30 bytes. Database sizes swept in the main comparison: 1 GB,
8 GB, 32 GB, each with 2^36 or a corresponding count of 1-bit records for the headline single-bit
retrieval benchmarks (32 GB stated explicitly as 2^36 1-bit records in the earlier discussion of the
DoublePIR response breakdown). Large-record variant record sizes: 32-64 KB. SCT-auditing database
size: 8 GB (2^36 bits), modeling roughly five billion active SCTs. Client audit rate modeled: 10^4
TLS connections/week, a 1/1000 audit fraction at two audits per audited connection, giving 20 PIR
queries/week per client, following the same assumption used by Henzinger et al. and by Chrome.
Cross-client batching queue size tested for cost reduction: 4.

### Stated limitations
The main stated limitation of YPIR is larger query size relative to SimplePIR and DoublePIR: YPIR
queries are 1.8-3x larger than DoublePIR's (1.5 MB versus 724 KB for an 8 GB database) and 3-7x
larger than SimplePIR's, because the query must carry the RLWE packing key; for a 32 GB database the
minimum YPIR query size is 1.1 MB, and the authors state YPIR may not be appropriate for applications
with a small, fixed communication budget. DoublePIR itself (the base this paper builds on) only
supports retrieving small records — a single element of the plaintext space Z_p — which the paper
addresses only by introducing the separate YPIR+SP variant built on SimplePIR instead. The paper
explicitly does not benchmark against a separate class of PIR schemes that require streaming the
entire database in an offline phase (naming Piano, a scheme by Mughees, Sun, Ren, and a scheme by
Ghoshal, Zhou, Shi), nor against RLWE-based schemes requiring persistent client-specific server-held
keys (SealPIR, FastPIR, MulPIR, OnionPIR, Spiral), stating these belong to different deployment
models not directly comparable on the same axes. Designing a PIR scheme with a hint significantly
smaller than the 14 MB figure a related packing-based comparison point (Table headers around line
1299) still requires is stated as an open question by the authors. The paper explicitly restricts its
evaluation to single-threaded execution for ease of comparison across systems, though it notes the
core matrix-vector-product computation is highly parallelizable, so the reported absolute throughput
figures understate what multi-core execution would achieve. The paper does not evaluate security
against a malicious (as opposed to honest-but-curious) server; it cites separate lines of work on
verifiable and malicious-secure PIR (Ben-David, Kalai, Paneth; Dietz, Tessaro; de Castro, Lee) as
addressing that threat model rather than addressing it itself.

### Requirements it places on the rest of the system
A deployment adopting YPIR in place of SimplePIR/DoublePIR removes the requirement that clients
fetch and cache a per-database hint before querying and that they re-fetch or patch that hint on
every database update; this specifically removes the operational requirement Henzinger et al.'s
SCT-auditing deployment imposes — maintaining multiple time-indexed copies of the database to serve
hints for different time windows — since YPIR clients query the database's current state directly.
In return, every YPIR query must carry the RLWE packing key alongside the LWE selection vectors, so
a transport or protocol layer built assuming SimplePIR/DoublePIR's smaller queries (120 KB-1.4 MB
range) must accommodate YPIR's larger queries (846 KB-2.5 MB range across the tested database sizes).
The packing transformation requires the LWE lattice dimension n to coincide with the RLWE ring
dimension d; a system choosing LWE parameters independently of this constraint cannot apply YPIR's
packing step without modification. The offline preprocessing that YPIR performs to move most of the
packing transformation's cost out of the online path requires the server to precompute against the
current database state before serving queries, exactly as SimplePIR/DoublePIR already require for
their own hint computation; a database that changes faster than this preprocessing can complete
would force the server to either serve stale precomputation or fall back to unamortized online
packing cost.

### Contradicts
None found within this paper's own claims. Cross-paper in this corpus: this entry's 724 MB
SimplePIR hint and 16 MB DoublePIR hint figures for a 32 GB database are internally consistent with
HENZINGER-USENIXSEC-23's own stated general formula (roughly 4*sqrt(N) KB for SimplePIR, roughly
16 MB independent of record count for DoublePIR at one-byte records), and the two papers' reported
DoublePIR hint size of 16 MB matches across both entries for their respective database
configurations. This paper's own DoublePIR throughput measurements (10.6 GB/s at 1 GB, 9.9 GB/s at
32 GB, reference implementation on an r6i.16xlarge) are somewhat higher than HENZINGER-USENIXSEC-23's
own headline DoublePIR figure of 7.4 GB/s/core measured on a c5n.metal instance; this is a
cross-hardware discrepancy, not a same-condition contradiction, and a synthesis should cite each
paper's own hardware when quoting either figure rather than treat them as interchangeable. This
paper's 1,314 MB/s Spiral-family figure is not reproduced here (Spiral is explicitly excluded from
this paper's benchmarked comparison set because it uses persistent client-specific server-held keys,
a different deployment model); a synthesis combining this entry with MENON-SP-22 and
HENZINGER-USENIXSEC-23 should not average or directly rank Spiral's throughput against YPIR's without
noting they were measured under different deployment-model assumptions and on different hardware.

### References worth retrieving
- Henzinger, Hong, Corrigan-Gibbs, Meiklejohn, Vaikuntanathan, "One Server for the Price of Two"
  (HENZINGER-USENIXSEC-23 in this corpus) — foundational (SimplePIR/DoublePIR, the direct base this
  paper builds on and the direct comparison target throughout).
- Henzinger, Dauterman, Corrigan-Gibbs, Zeldovich, "Private web search with Tiptoe" — competing
  (introduces the hintless variant of SimplePIR this paper directly compares against and partially
  supersedes on throughput).
- Li, Micciancio, Raykova, Schultz, "Hintless single-server private information retrieval" (HintlessPIR)
  — competing (direct throughput/communication comparison target, the other hint-free scheme).
- Chen, Dai, Kim, Song, "Efficient homomorphic conversion between (ring) LWE ciphertexts," 2021
  (CDKS21) — foundational (the LWE-to-RLWE packing transformation YPIR's compression step is built
  on).
- Menon, Wu, "Spiral: Fast, high-rate single-server PIR via FHE composition" (MENON-SP-22 in this
  corpus) — competing/foundational (a persistent-client-key single-server PIR family this paper
  explicitly excludes from direct comparison but whose response-packing techniques it cites as
  conceptually similar to its own).
- Davidson, Pestana, Celi, "FrodoPIR: Simple, scalable, single-server private information retrieval"
  — competing (a hint-based single-server scheme in the same design space).
- Angel, Chen, Laine, Setty, "PIR with compressed queries and amortized query processing" (SealPIR)
  — competing (a persistent-client-key scheme this paper explicitly excludes from its direct
  benchmark comparison).
- Ahmad, Yang, Agrawal, El Abbadi, Gupta, "Addra" (FastPIR) — competing (excluded from direct
  benchmark comparison for the same reason, persistent client-specific keys).
- Mughees, Chen, Ren, "OnionPIR: Response efficient single-server PIR" — competing (same exclusion
  reason).
- Zhou, Park, Shi, Zheng, "Piano: Extremely simple, single-server PIR" — competing (a
  streaming-offline-phase PIR scheme this paper explicitly declines to benchmark against due to a
  different deployment model).
- Mughees, Sun, Ren, "Simple and practical amortized sublinear private information retrieval" —
  competing (another streaming-offline-phase scheme excluded from direct benchmark comparison for the
  same stated reason).
- Ben-David, Kalai, Paneth, "Verifiable private information retrieval" — attack/superseded-by context
  (addresses the malicious-server threat model this paper explicitly does not evaluate).
- Dietz, Tessaro, "Fully malicious authenticated PIR," CRYPTO 2024 — attack/superseded-by context
  (same malicious-server threat model, published after this paper).
- de Castro, Lee, "VeriSimplePIR: Verifiability in SimplePIR at no online cost for honest servers,"
  2024 — attack/superseded-by context (verifiability extension to the SimplePIR family this paper
  builds on).
- DeBlasio, "Opt-out SCT auditing in Chrome" — foundational (describes the deployed Chrome baseline
  and the client usage assumption, 20 audits/week, this paper's cost model reuses).

### Verbatim extracts
"YPIR achieves 12.1 GB/s/core server throughput and requires 2.5 MB of total communication."
"SimplePIR protocol achieves a 12.5 GB/s/core server throughput... but additionally requires downloading a 724 MB hint."
"the throughput of YPIR is 43% slower than SimplePIR and 26% slower than DoublePIR."
"the main limitation of YPIR is the larger query sizes compared to SimplePIR and DoublePIR."
"their approach does not support real-time auditing."
