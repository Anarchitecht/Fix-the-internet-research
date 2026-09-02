## [LI-CCS-25-PANTHER] Panther: Private Approximate Nearest Neighbor Search in the Single Server Setting
**Citation:** Jingyu Li, Zhicong Huang, Min Zhang, Cheng Hong, Jian Liu, Tao Wei, Wenguang Chen. "Panther: Private Approximate Nearest Neighbor Search in the Single Server Setting." ACM SIGSAC Conference on Computer and Communications Security (CCS), 2025. Also IACR Cryptology ePrint Archive, Report 2024/1774.
**Retrieved:** full text via IACR ePrint 2024/1774 (retrieved for the corpus's `interactive-private-search.md` open-problem entry)
**Source URL:** https://eprint.iacr.org/2024/1774
**Domain:** G

### What it does
Panther answers an approximate nearest-neighbor search (ANNS) query — find the k stored vectors closest
to a query vector — while protecting both parties: the server learns nothing about the client's query or
the result, and the client learns nothing about the server's dataset beyond the ANNS result itself. This
is the only one of the four private-search systems retrieved for this corpus's private-search analysis
that hides the database from the client as well as the query from the server; Tiptoe, Pacmann, and Wally
protect only the query. Panther runs as an interactive two-party secure computation between one client
and one server, combining three cryptographic primitives across its pipeline: additive secret sharing (a
value is split into two shares, each individually random, that together reconstruct it) for intermediate
values, garbled circuits for the top-k selection step, and homomorphic encryption for the distance
computation and point-retrieval steps. The server's dataset is pre-clustered (as in Tiptoe); Panther's
core technical contribution replaces the retrieval-of-points-in-a-cluster step, done in a prior
single-server design (SANNS) with a Distributed Oblivious RAM (DORAM) protocol the paper shows is
"inherently costly" (citing several megabytes of communication for a single oblivious query over ten
thousand entries), with a batch Private Information Retrieval (PIR)-to-secret-shares construction: since
both the query indices and the retrieved points need only end up secret-shared, not fully hidden from both
parties throughout, a lighter PIR-based protocol suffices instead of a full DORAM.

### Measured results
Measured on cloud instances with 64 virtual CPUs (vCPU) at 2.80 GHz and 256 GB RAM, client and server both
running 32 threads, under two simulated network conditions matched to the SANNS comparison paper's own
settings: Local Area Network (LAN), 4,000 Mbps bandwidth, 1 ms round-trip time (RTT); Wide Area Network
(WAN), 320 Mbps bandwidth, 74 ms RTT. Four datasets: SIFT-1M (n=1,000,000, dimension d=128), Deep1B-1M
(n=1,000,000, d=96), Deep1B-10M (n=10,000,000, d=96), Amazon (n=2^20, d=50). Hyperparameters (cluster
count, approximate-top-k bin count) matched to SANNS's own published values for a fair comparison of the
secure-computation layer alone, not the plaintext clustering algorithm.

Total end-to-end time and communication, Panther versus SANNS (Table 9; SANNS is not open-source, so the
paper estimates SANNS's time from its own reported communication and bandwidth, explicitly stating this
"neglect[s] their computational cost, thus the numbers in this table are in great favor of" SANNS — a
methodological caveat the paper states itself):

| Dataset | LAN total (SANNS → Panther) | WAN total (SANNS → Panther) | Communication (SANNS → Panther) | Speedup (WAN) |
|---|---|---|---|---|
| SIFT-1M | 3.62 s → 1.49 s | 45.3 s → 9.32 s | 1.77 GB → 92.9 MB (↓95%) | 2.4× (LAN) / 4.9× (WAN) |
| Deep1B-1M | 3.23 s → 1.50 s | 40.4 s → 8.71 s | 1.58 GB → 94.6 MB (↓94%) | 2.2× (LAN) / 4.6× (WAN) |
| Deep1B-10M | 11.3 s → 3.89 s | 142 s → 18.3 s | 5.53 GB → 284 MB (↓95%) | 2.9× (LAN) / 7.8× (WAN) |
| Amazon | 2.29 s → 1.25 s | 28.7 s → 8.83 s | 1.12 GB → 98.9 MB (↓91%) | 1.8× (LAN) / 3.3× (WAN) |

The paper states point retrieval alone (batch PIR versus SANNS's DORAM-based approach) reduces
communication by up to 99%, and states its overall improvement across datasets is "up to 95%" lower
communication and "up to 7.8×" faster search time.

Comparison against a two-server private-ANNS system (Servan-Schreiber, Langowski, Devadas, "Private
Approximate Nearest Neighbor Search with Sublinear Communication," IEEE S&P 2022, cited as reference
[48]): that system answers a query on Deep1B-10M in 6.13 seconds, which the paper states is 3.0× faster
than Panther under WAN but 1.6× slower than Panther under LAN — with an explicit caveat that the compared
system's own two servers "reside in the same region of AWS regardless of WAN or LAN," meaning that
comparison's own WAN condition does not reflect two genuinely independent, geographically separated
non-colluding operators.

Accuracy (Table 10): Panther's 10-nearest-neighbor accuracy is stated to match SANNS's own reported 0.9
(9 of 10 points correct on average, per SANNS's own Section 5.3) because both systems share the same
underlying plaintext clustering algorithm and hyperparameters; Panther's own measured accuracy with and
without a possible one-bit error in its "H2A" (homomorphic-to-arithmetic) distance-computation step is
88.85% (SIFT-1M) and 89.16% (Deep1B-1M), identical in both configurations, indicating the possible one-bit
error does not measurably affect accuracy in these two tested cases.

### Parameters
- Homomorphic-encryption scheme: BFV (a specific fully homomorphic encryption construction operating over
  integers), with parameters summarized in the paper's Table 6; the paper states its H2A (homomorphic-to-
  arithmetic-share) protocol lets it use "more user-friendly," lower-overhead parameters than a naive
  instantiation would need, and requires the second-dimension plaintext modulus p to equal the
  first-dimension modulus q1.
- Threat model: static semi-honest adversary — a computationally bounded adversary that corrupts either
  the client or the server at protocol start and follows the protocol specification exactly, never
  deviating (a strictly weaker guarantee than Tiptoe's malicious-tolerant query privacy).
- Dataset dimensionality tested: d = 50 (Amazon) to d = 128 (SIFT-1M); dataset size tested: n = 2^20
  (roughly 1,048,576, Amazon) to n = 10,000,000 (Deep1B-10M).

### Stated limitations
The paper explicitly states it does not consider leakage from the query results themselves — prior work
(cited as reference [29]) has explored reconstructing a database from many ANNS query results, and the
paper's stated justification for excluding this from its threat model is that a server could charge per
query, which "naturally limits the query rate and discourages adversarial querying" — a mitigation
argument, not a cryptographic guarantee, and the paper does not claim it closes the leakage channel. The
paper's semi-honest threat model is explicitly weaker than malicious security: it assumes both corrupted
parties follow the protocol honestly, so it provides no guarantee against a party that deviates from the
protocol, unlike Tiptoe's stated malicious-server tolerance for query privacy. The paper states an earlier
design attempt using the DUORAM protocol (a more communication-efficient DORAM than the Floram protocol
SANNS uses) proved infeasible because DUORAM's underlying Naor-Pinkas protocol requires re-encrypting the
entire database on every oblivious read, making it impractical for the batch retrieval Panther performs —
recorded by the paper as a failed approach, not merely an unexplored alternative.

### Requirements it places on the rest of the system
Panther requires an interactive session between client and server across multiple protocol rounds (secret
sharing, garbled-circuit evaluation for top-k selection, and homomorphic-encryption operations for
distance computation and retrieval each require message exchange), so its wide-area performance is
dominated by round-trip count rather than raw computation — the paper's own comparison to the two-server
scheme of Servan-Schreiber et al. shows that scheme reaching lower latency under WAN specifically because
it needs fewer interactive rounds, at the cost of a second-server trust assumption Panther does not need.
The construction requires the server's dataset to already be organized into the same clustering structure
SANNS's plaintext algorithm produces — Panther's own hyperparameters (cluster count, approximate-top-k bin
count) are matched to SANNS's for the paper's comparison, and the paper states explicitly that changing
the plaintext clustering algorithm or hyperparameters could change performance for both systems, so
Panther's reported numbers are conditioned on this specific upstream clustering choice, not
architecture-independent. Because Panther protects the database contents from the client (unlike Tiptoe,
Pacmann, and Wally), any system composing Panther with a component that needs the client to independently
verify or audit database contents (for example, a content-moderation or provenance check the client itself
performs) cannot do so without violating Panther's own privacy guarantee, since revealing database
contents to the client for such a check reintroduces exactly the leakage Panther is built to prevent.

### Contradicts
None found against other corpus entries on a measured fact. This entry's figures match, and were the
source for, the figures already recorded under this KEY in the corpus's `interactive-private-search.md`
open-problem synthesis. Note for downstream synthesis: the paper's own comparison table against SANNS
(Table 9) is explicitly not a head-to-head measurement — SANNS's time figures are the paper's own estimate
from SANNS's reported communication cost, excluding SANNS's actual computation time, and the paper states
this estimate favors SANNS; a downstream synthesis citing "Panther is 2.2–7.8× faster than SANNS" should
carry this caveat rather than presenting it as a controlled head-to-head benchmark.

### References worth retrieving
- **Foundational/competing** — Hao Chen, Ilaria Chillotti, Yihe Dong, Oxana Poburinnaya, Ilya P.
  Razenshteyn, M. Sadegh Riazi. "SANNS: Scaling Up Secure Approximate k-Nearest Neighbors Search." USENIX
  Security 2020, 2111–2128. (Cited as reference [11]; the prior single-server ANNS system Panther directly
  replaces the DORAM-based retrieval step of and benchmarks against throughout.)
- **Competing** — Sacha Servan-Schreiber, Simon Langowski, Srinivas Devadas. "Private Approximate Nearest
  Neighbor Search with Sublinear Communication." IEEE Symposium on Security and Privacy (S&P) 2022,
  911–929. (Cited as reference [48]; the two-server private-ANNS system Panther compares against, with the
  caveat that its own two servers were co-located in the same AWS region for the comparison.)
- **Foundational** — Sebastian Angel, Hao Chen, Kim Laine, Srinath T. V. Setty. "PIR with Compressed
  Queries and Amortized Query Processing." IEEE S&P 2018, 962–979. (Cited as reference [2]; a foundational
  PIR construction in this paper's technical lineage.)
- **Foundational** — cited as reference [17] in this paper: Floram, the DORAM protocol SANNS uses for
  oblivious point retrieval, whose per-query communication cost (several megabytes for ten thousand
  entries, per this paper's own citation) motivates Panther's batch-PIR replacement — bibliography detail
  not fully captured in this extraction pass; retrieve to confirm identity.
- **Foundational** — cited as reference [55] in this paper: DUORAM, the more communication-efficient DORAM
  Panther's authors attempted and rejected as infeasible for batch retrieval due to its Naor-Pinkas-based
  full-database re-encryption requirement — bibliography detail not fully captured in this extraction
  pass; retrieve to confirm identity.

### Verbatim extracts
- "The server learns nothing about the query or the result, while the client learns nothing about the
  dataset beyond the ANNS result."
- "we do not consider leakage from the query results themselves."
- "the numbers in this table are in great favor of them" — of the SANNS comparison in Table 9.
- "our scheme consistently outperforms SANNS in various datasets. We achieve a reduction in communication
  costs of up to 95%, while improving search times by up to 7.8×."
- "Note that their two servers reside in the same region of AWS regardless of WAN or LAN."
