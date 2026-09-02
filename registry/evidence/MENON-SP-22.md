## [MENON-SP-22] Spiral: Fast, High-Rate Single-Server PIR via FHE Composition
**Citation:** Samir Jordan Menon, David J. Wu. "Spiral: Fast, High-Rate Single-Server PIR via FHE Composition." IEEE Symposium on Security and Privacy, 2022. DOI 10.1109/SP46214.2022.9833700.
**Retrieved:** full text via https://eprint.iacr.org/2022/368.pdf
**Source URL:** https://eprint.iacr.org/2022/368.pdf
**Domain:** G

### What it does
Single-server private information retrieval (PIR) lets a client retrieve one record from a database
held by a single server without the server learning which record was requested, without replicating
the database across non-colluding servers. Spiral achieves this by composing two lattice-based fully
homomorphic encryption (FHE) schemes — Regev encryption and the Gentry-Sahai-Waters (GSW) scheme —
inside one protocol, using new ciphertext-translation procedures the paper introduces to convert
between the two schemes' ciphertext formats mid-computation.

Mechanism: the client's query is one Regev ciphertext (single-ciphertext query, unlike prior schemes
whose queries grow with database size). The server represents the database as a multi-dimensional
hypercube and answers in three steps. Step 1, query expansion: the server homomorphically expands the
single received ciphertext into the full set of per-dimension selection ciphertexts needed to index
into the hypercube, using a family of automorphism and modulus-switching operations over the query
ciphertext and reusable server-held public parameters (the "packing keys"); this step requires a
key-dependent message (KDM) security assumption because it operates on encryptions of the client's
own secret key material, an assumption the paper notes prior query-expansion schemes (SealPIR,
Onion Ring ORAM) already require. Step 2, first-dimension processing: the server evaluates the first
hypercube dimension using ciphertext multiplication under the Regev-to-GSW ciphertext translation the
paper introduces, at a computational cost that scales quadratically with the size of that first
dimension, so the first-dimension size is capped by the tolerable noise growth. Step 3, folding: the
server homomorphically collapses the remaining dimensions using GSW ciphertext operations. Two
protocol variants trade communication for computation: SpiralStream reuses a public query across many
records to reach higher throughput, and SpiralPack applies ciphertext packing to raise rate (the
fraction of a returned response that is genuine record content) at the cost of larger reusable public
parameters.

### Measured results
All measurements taken on a single Amazon EC2 c5n.2xlarge instance (8 vCPUs, Intel Xeon Platinum
8124M at 3 GHz, 21 GB RAM), Ubuntu 20.04, compiled with Clang 12, AVX2/AVX-512 SIMD enabled,
single-threaded execution, running times averaged over a minimum of 5 trials, database represented
implicitly to equalize memory effects across systems (measured effect at most 1% on server compute
time). Monetary costs are computed from AWS long-term reserved-instance rates of $0.0195/CPU-hour
and $0.09/GB outbound traffic quoted at the time of writing (2022); the paper labels these public
parameters and per-query costs as excluding the one-time offline generation and transmission of
public parameters.

| Database configuration | System | Query size | Response size | Server computation | Rate | Throughput | Server cost/query |
|---|---|---|---|---|---|---|---|
| 2^20 records x 256 B (268 MB) | SealPIR | 66 KB | 328 KB | 3.19 s | 0.0008 | 84 MB/s | $0.000047 |
| 2^20 x 256 B | FastPIR | 33 MB | 66 KB | 1.44 s | 0.0039 | 186 MB/s | $0.000014 |
| 2^20 x 256 B | OnionPIR | 63 KB | 127 KB | 3.31 s | 0.0020 | 81 MB/s | $0.000029 |
| 2^20 x 256 B | Spiral | 14 KB | 21 KB | 1.69 s | 0.0122 | 159 MB/s | $0.000011 |
| 2^20 x 256 B | SpiralStream | 8 MB | 20 KB | 0.85 s | 0.0125 | 314 MB/s | $0.000006 |
| 2^18 records x 30 KB (7.9 GB) | SealPIR | 66 KB | 3 MB | 74.91 s | 0.0092 | 105 MB/s | $0.000701 |
| 2^18 x 30 KB | FastPIR | 8 MB | 262 KB | 50.52 s | 0.1144 | 156 MB/s | $0.000297 |
| 2^18 x 30 KB | OnionPIR | 63 KB | 127 KB | 52.73 s | 0.2363 | 149 MB/s | $0.000297 |
| 2^18 x 30 KB | Spiral | 14 KB | 84 KB | 24.46 s | 0.3573 | 322 MB/s | $0.000140 |
| 2^18 x 30 KB | SpiralStream | 15 MB | 62 KB | 8.99 s | 0.4803 | 875 MB/s | $0.000054 |
| 2^14 records x 100 KB (1.6 GB) | SealPIR | 66 KB | 11 MB | 19.03 s | 0.0092 | 86 MB/s | $0.001076 |
| 2^14 x 100 KB | FastPIR | 524 KB | 721 KB | 23.27 s | 0.1387 | 70 MB/s | $0.000191 |
| 2^14 x 100 KB | OnionPIR | 63 KB | 508 KB | 14.38 s | 0.1969 | 114 MB/s | $0.000124 |
| 2^14 x 100 KB | Spiral | 14 KB | 242 KB | 4.92 s | 0.4129 | 333 MB/s | $0.000048 |
| 2^14 x 100 KB | SpiralStream | 8 MB | 208 KB | 2.38 s | 0.4811 | 688 MB/s | $0.000032 |

SealPIR and OnionPIR provide 115 and 111 bits of security respectively (weaker than the target); all
other schemes here provide at least 128 bits. Spiral's public parameter size ranges 14-18 MB across
these three configurations (versus 3 MB for SealPIR, 1 MB for FastPIR, 5 MB for OnionPIR);
SpiralStream's public parameters range 344 KB-3 MB.

Packing effect (SpiralPack, SpiralStreamPack versus non-packed variants), same three configurations:
packing raises public parameter size to 14-47 MB but raises rate up to 30% further on larger
databases; on the 2^18 x 30 KB database SpiralStreamPack reaches 1.48 GB/s throughput and 0.3117-0.6677
rate depending on record size, a 10x throughput increase over the best prior system (FastPIR/OnionPIR)
and a 1.7x increase over the non-packed SpiralStream.

Streaming-setting throughput as a function of record count (query-expansion cost excluded, since
amortized across many queries reusing one query in the streaming model), at record count 2^20:
FastPIR 201 MB/s (34 MB query), OnionPIR 158 MB/s (63 KB query), Spiral 355 MB/s (14 KB query),
SpiralPack 521 MB/s (14 KB query), SpiralStream 1.46 GB/s (30 MB query), SpiralStreamPack 1.94 GB/s
(30 MB query). At 2^12 records, SpiralStreamPack reaches 1.57 GB/s with rate 0.8057, and FastPIR
reaches only 23 MB/s with rate 0.1392 at the same record count. Peak reported throughput across the
whole streaming sweep: SpiralStreamPack at approximately one million records reaches 1.9 GB/s,
stated as 9.7x higher than FastPIR's throughput at the same point and a 5.8x higher rate (5.8x fewer
bits the client downloads).

Server-computation scaling with database size (Figure 2): for 10 KB records, Spiral matches existing
systems at small record counts but is up to 2x faster at one million records; for 100 KB records,
Spiral is 1.8-3x faster than competitors across every record count tested (2^10 to 2^20).

Application-scenario cost estimates (analytical, derived from the measured per-byte and per-CPU-hour
costs above, not independently re-measured end-to-end):
- Private video streaming of a 2 GB movie from a library of 2^14 movies, using SpiralStreamPack:
  30 MB upload, 2.5 GB download, 5.6 CPU-hours, $0.33 server cost, versus $0.18 for the no-privacy
  baseline of direct download (1.9x more expensive). The same task under OnionPIR: 63 KB upload,
  8.3 GB download, 59.3 CPU-hours, 17x more expensive than the no-privacy baseline and 9x more
  expensive than SpiralStreamPack.
- Private voice calls modeled on the Addra application (5-minute call, 625 rounds, 96 bytes
  downloaded per round), using SpiralStream at up to 2^20 users: 29 MB upload, 11 MB download,
  112 seconds of CPU time, $0.0016 per-user server cost, a 3.9x improvement over FastPIR (the system
  Addra itself used); at a million users the paper states the system remains costly, over $300/minute.
- Private Wikipedia article retrieval from a 31 GB database (English Wikipedia text plus a subset of
  article images, maximum article size 30 KB), split into 16 partitions processed in parallel on a
  16-core, 42 GB machine costing $229/month on AWS, with median mobile network speeds of 8 Mbps
  upload / 29 Mbps download: SpiralPack delivers an article in 4.3 seconds, a 2.1x reduction versus
  OnionPIR; the paper states this non-streaming setting remains much slower than non-private
  retrieval, unlike the streaming video and voice scenarios.

Noise/correctness measurement: error-rate distribution over 163,000 error coefficients from 20
independent protocol executions on a 2^20 x 256 B database, compared against the paper's own
heuristic noise-growth prediction; the measured error margin sits below the 2^-40 correctness target
the paper designs for, meaning the actual scheme meets a stronger correctness guarantee than the
target.

### Parameters
Correctness target: 2^-40 failure probability, used to select lattice parameters via the paper's
automatic parameter-selection search (Section 5.1), which estimates monetary cost from the same AWS
rate model used for evaluation and selects parameters within a stated 10% margin of measured running
time. Security target: at least 128 bits for Spiral/SpiralStream/SpiralPack/SpiralStreamPack (versus
115 bits for SealPIR and 111 bits for OnionPIR in the same comparison, both below target). Query-size
cap imposed for the streaming-throughput comparison (Table 4, Figure 3): 33 MB, chosen to match
FastPIR's own query size for a balanced comparison; a halved-cap variant SpiralStream_(1/2) at 16 MB
query size is also measured, peaking at a smaller database (2^14 records instead of 2^16). First
hypercube dimension size: capped at 2^9 for Spiral and SpiralPack, beyond which coefficient-expansion
noise exceeds the correctness target without moving to larger lattice parameters. Record sizes swept:
256 B, 30 KB, 100 KB (main comparison table), 10 KB and 100 KB (server-computation scaling figure),
1 MB (Table 5, maximum-rate/maximum-throughput search). Database record counts swept: 2^10 through
2^20.

### Stated limitations
Spiral's public parameters are larger than every compared prior scheme: 14-18 MB versus 3.4 MB
(SealPIR), 1.4 MB (FastPIR), 4.6 MB (OnionPIR); SpiralPack's parameters range 14-47 MB. The paper
states this as Spiral's stated limitation, attributing it to the additional keys the new
ciphertext-translation procedures require, and notes the cost is amortized because the parameters are
reused across many queries. Query expansion (Step 1 of the server's Answer procedure) requires a
key-dependent message security assumption, which the paper notes prior schemes (SealPIR, Onion Ring
ORAM) already require, so this is not a new assumption Spiral introduces but is a precondition Spiral
still carries. First-dimension processing cost scales quadratically with the message dimension, so
increasing the first dimension beyond the point at which coefficient-expansion noise exceeds the
correctness target requires moving to a larger set of lattice parameters instead; scaling to more
records at a fixed first-dimension size instead increases the number of folding rounds, which the
paper states leads to lower throughput. For SpiralStream and SpiralStreamPack, the limiting factor
on how the database is split between the first dimension and subsequent dimensions is query size,
since query size scales linearly with first-dimension size; once the imposed query-size cap is
reached, throughput decreases as record count grows further. Even Spiral's fastest streaming
configuration remains 2.9x slower than the best two-server PIR construction using hardware-accelerated
AES cited by the authors (Hafiz and Henry, USENIX Security 2019), a multi-server, non-single-server
comparison. In the non-streaming Wikipedia scenario, the paper states private retrieval remains much
slower than non-private retrieval, unlike the streaming video and voice scenarios where the private
and non-private costs are close. At a million users, the paper's own extrapolation of the Addra-style
voice-call scenario states the system "remains costly," exceeding $300/minute to support that user
count.

### Requirements it places on the rest of the system
A deployment must supply and distribute Spiral's public parameters (14-47 MB depending on variant) to
every client before that client's first query, in a phase the paper explicitly separates from the
online per-query costs it measures; a design that cannot amortize this transfer over many queries per
client will pay this cost on every query, unlike the comparison schemes' smaller 1-5 MB parameter
sets. The query-expansion step's key-dependent message security assumption must hold for the server's
homomorphic operations on client-key-derived ciphertexts to be safe; a system substituting a different
FHE backend without an equivalent assumption would need to re-derive or drop this step. The streaming
variants (SpiralStream, SpiralStreamPack) require an application structure where the same query is
reused across many separate PIR invocations against different databases (the paper's own examples:
successive movie-stream chunks, successive voice-call rounds) to amortize the larger one-time query
cost; a workload issuing one query per unrelated database lookup gets no benefit from the streaming
variant and should use the non-streaming Spiral or SpiralPack instead. The single-server model assumed
throughout requires no cross-server non-collusion assumption (unlike multi-server PIR), but correctness
and privacy both rely on the server correctly executing the protocol on the stated database; the paper
does not analyze a malicious (rather than honest-but-curious) server.

### Contradicts
None found — the paper's own comparisons against SealPIR, FastPIR, OnionPIR, and MulPIR are presented
as its contribution, not as a contradiction of those papers' claims. Cross-paper in this corpus: this
entry's own measured Table 2 row for the 2^18 x 30 KB database (Spiral: 14 kB query, 84 kB response,
24.46 s computation) differs slightly from the figure cited in the target registry's rationale
("24.5 s server computation on a 7.9 GB database"), a rounding difference only, not a substantive
disagreement. No other entry in this corpus yet reports SimplePIR/DoublePIR throughput on the same
database sizes for direct comparison; see MENON-USENIXSEC-24 and HENZINGER-USENIXSEC-23 in this
corpus for the throughput figures needed to complete that comparison.

### References worth retrieving
- Chor, Goldreich, Kushilevitz, Sudan, "Private information retrieval," FOCS 1995 (journal version CHOR-JACM-98 in this corpus) — foundational (defines PIR and the multi-server construction).
- Kushilevitz, Ostrovsky, "Replication is not needed: Single database, computationally-private information retrieval," FOCS 1997 — foundational (originates the single-server PIR paradigm this paper's construction follows).
- Angel, Chen, Laine, Setty, "PIR with compressed queries and amortized query processing," IEEE S&P 2018 (SealPIR) — competing (direct throughput/rate/query-size comparison target in Table 2).
- Ahmad, Yang, Agrawal, El Abbadi, Gupta, "Addra: ..." (FastPIR) — competing (direct comparison target; also the application this paper's private-voice-call cost estimate is modeled on).
- Mughees, Chen, Ren, "OnionPIR: Response efficient single-server PIR," 2021 — competing (direct comparison target throughout).
- Ali, Lepoint, Patel, Raykova, Schoppmann, Seth, Yeo, "MulPIR" — competing (comparison target for query/response size on a similarly sized database, no public implementation available to the authors so numbers are taken from the cited paper rather than independently measured).
- Corrigan-Gibbs, Henzinger, Kogan, "Single-server private information retrieval with sublinear amortized time," EUROCRYPT 2022 — competing (a distinct single-server PIR construction with an amortized-time model, not the same paper as HENZINGER-USENIXSEC-23 in this corpus).
- Corrigan-Gibbs, Kogan, "Private information retrieval with sublinear online time," EUROCRYPT 2020 — foundational/competing (predecessor sublinear-online-time construction).
- Gentry, Sahai, Waters, "Homomorphic encryption from learning with errors: Conceptually-simpler, asymptotically-faster, attribute-based," CRYPTO 2013 (GSW13) — foundational (defines the GSW encryption scheme this paper composes with Regev encryption).
- Regev, "On lattices, learning with errors, random linear codes, and cryptography," STOC 2005 — foundational (defines the learning-with-errors hardness assumption underlying Regev encryption).
- Hafiz, Henry, "A bit more than a bit is more than a bit better: Faster (essentially) optimal-rate many-server PIR," 2019 — competing (multi-server PIR with hardware-accelerated AES, cited as the still-faster comparison point Spiral's streaming throughput falls short of by 2.9x).
- Gupta, Crooks, Mulhern, Setty, Alvisi, Walfish, "Scalable and private media consumption with Popcorn," NSDI 2016 — foundational (the private video-streaming application scenario this paper's cost estimate models itself on).
- Melchor, Barrier, Fousse, Killijian, "XPIR: Private information retrieval for everyone," PoPETs 2016 — foundational (an earlier practical lattice-based single-server PIR system).

### Verbatim extracts
"a 4.5× reduction in query size, 1.5× reduction in response size, and 2× increase in server throughput."
"1.9 GB/s for databases with over a million records (compared to 200 MB/s for previous protocols)."
"only 1.9× greater than that of the no-privacy baseline where the client directly downloads."
"the main limitation of Spiral is its larger public parameter size."
"running a system like Addra using SpiralStream remains costly at over $300/minute."
