## [TWOSERVER-EPRINT-25] Two-Server Private Information Retrieval in Sublinear Time and Quasilinear Space
**Citation:** Alexandra Henzinger, Seyoon Ragavan. "Two-Server Private Information Retrieval in Sublinear Time and Quasilinear Space." IACR Cryptology ePrint Archive, Report 2025/2008, July 2, 2026 (accepted to Eurocrypt 2026).
**Retrieved:** full text via https://eprint.iacr.org/2025/2008 (retrieved for the corpus's `interactive-private-search.md` open-problem entry)
**Source URL:** https://eprint.iacr.org/2025/2008
**Domain:** G

### What it does
This construction answers a Private Information Retrieval (PIR) query — a client fetches one record from
a server-held database by known index, without either server learning which record was fetched — using
two servers under a collusion threshold of t=1 (a 2-out-of-2 scheme: either server alone, individually,
learns nothing about the query; the guarantee holds only if the two servers do not compare what each
received). The guarantee is information-theoretic — unconditional given non-collusion, not resting on any
computational hardness assumption — a strictly stronger privacy property than the learning-with-errors
(LWE)-based computational security of single-server PIR schemes such as SimplePIR or Tiptoe. The
mechanism is PIR-with-preprocessing: before any query arrives, both servers jointly transform the
database into a compact data structure sized rougly 1.5·sqrt(log2(n))·n bits (n the database size in
bits) — the paper's own stated headline is that this is the first information-theoretic PIR at any
constant server count to combine quasilinear server storage (n^(1+o(1)), only a logarithmic-factor blowup
over the raw database) with polynomially sublinear per-query server time (n^(1-Omega(1))), rather than the
linear-in-n server time every non-preprocessing single-server or two-server PIR scheme requires. The
construction builds on a 2000 PIR-with-preprocessing protocol (Beimel, Ishai, Malkin, CRYPTO 2000) and
improves it with a compact data structure for evaluating a multivariate polynomial and its derivatives:
the paper's key technical insight is that Hasse derivatives (a generalization of ordinary polynomial
derivatives usable over finite fields) can be computed on the fly from finite differences between the
polynomial's own evaluations, avoiding the need to store the derivative values separately.

### Measured results
Implemented in 900 lines of Go and 100 lines of C, evaluated on a single AWS `r7a.metal-48xl` instance
(192 cores, 1,536 GB RAM) for a no-networking server-throughput baseline, and across two separate AWS
regions (`us-east-1` and `us-east-2`) for a networked measurement including real inter-region round-trip
cost. Throughput is reported as queries answered per second, using enough execution threads to saturate
the machine.

| Database size (1-byte records) | Encoded structure size | Download per query | Throughput, no networking (queries/s) | Throughput, with networking (queries/s) | Storage blowup vs. raw database | Throughput gain over XOR PIR baseline |
|---|---|---|---|---|---|---|
| 11 GB | 1 TB | 4.4 MB | 1,646 | 636 | 93× | 9.0× |
| 2 GB | 1 TB | 0.7 MB | 7,620 | 3,804 | 512× | 10.2× |
| 250 MB | 1 TB | 0.1 MB | 43,614 | 24,252 | 4,022× | 6.6× |
| 122 GB | 1 TB | 356.3 MB | 29 | 6 | 8× | 1.0× (no gain) |

(All rows drawn from the paper's Table 2, "databases with 1-byte records"; the paper reports separate rows
for 32-byte and 64-byte records at similar sizes and throughput-gain magnitudes, generally lower gains at
the same nominal database size, e.g., 0.3–3.9× for 32-byte records, 0.2–3.4× for 64-byte records.)

Baseline comparison, XOR PIR (Chor, Goldreich, Kushilevitz, Sudan, 1995, the fastest known linear-time
two-server PIR, requiring the paper states 4·sqrt(n) bits of communication and O(n) server time per
query): the paper implements XOR PIR itself in Go and C, including a "XOR PIR fast" optimization from a
cited prior work, for a controlled, same-hardware, same-methodology comparison — this is a genuine
head-to-head benchmark, not an estimate from published figures, unlike some comparisons in other papers in
this batch.

Storage comparison against prior PIR-with-preprocessing schemes (Beimel-Ishai-Malkin 2000; Ghoshal et al.,
TCC 2025): the paper states its own scheme shrinks server storage by four to six orders of magnitude on
gigabyte-scale databases relative to these prior schemes, while matching their communication and per-query
bits-read cost — for the specific 11 GB database example, the paper states its own 1 TB encoded structure
is 4,500,000× smaller than prior two-server PIR-with-preprocessing schemes' structure at the same database
size.

### Parameters
- Collusion threshold t = 1 for the core two-server construction (s = 2 servers, t ∈ [s−1] = {1}) —
  identical to the classic two-server PIR trust assumption: privacy holds only if the two servers do not
  collude.
- Storage-versus-time tradeoff parameter D/m (the polynomial degree D over the number of variables m used
  to encode the database): the paper states the smaller this ratio, the larger the storage blowup but also
  the larger the server-throughput speedup; as D/m approaches 1/2, storage blowup shrinks but communication
  overhead grows enough that the scheme "does not show a throughput gain (when including network costs)."
- The paper generalizes its core two-server result to s ≥ 2 servers with a general collusion threshold t ∈
  [s−1] (Theorem 5.3/5.4): for a fixed collusion threshold t = 1, increasing the server count s pushes
  server time closer to sqrt(n).
- Database sizes tested: from 250 MB up to 135–139 GB across the three record-length tables (1-byte,
  32-byte, 64-byte records), each fixed to encode into the same 1 TB per-server data structure size.

### Stated limitations
The paper states its own main limitation directly in the abstract: "large communication complexity."
Communication is imbalanced — upload scales as Theta(log n) bits (concretely tens of bits) while download
scales as Theta(n^epsilon) for a constant 1/2 < epsilon < 1, concretely tens of megabytes to gigabytes in
the tested range — one to three orders of magnitude larger than the XOR PIR baseline's communication at
comparable database sizes, per the paper's own Table 2 "Comm. blowup" column (ranging from 6× to over
3,700×, depending on configuration). The paper states this larger download, not memory-access savings,
becomes the throughput bottleneck once the ratio D/m grows large enough, at which point the scheme shows
no throughput gain over XOR PIR when network cost is included, even though its raw memory-access count is
still far lower. The paper states a proposed fix — shrinking communication to n^0.31 · poly(security
parameter lambda) using compact linearly homomorphic encryption — but explicitly leaves "implementing and
optimizing these communication-shrinking techniques ... to future work," so this fix is not built or
measured in this paper.

### Requirements it places on the rest of the system
The scheme requires a preprocessing phase in which both servers jointly (or, per the paper's PIR-with-
preprocessing model, independently but consistently) transform the raw database into the 1-TB-scale
encoded data structure before any query can be answered; the paper does not measure or report the time
this preprocessing itself takes, and any deployment must account for it as a setup cost separate from the
per-query figures above, paid again whenever the underlying database is updated in a way this paper does
not itself measure. The information-theoretic privacy guarantee requires two independently operated
servers that genuinely do not communicate about the query they each received — a decentralized deployment
adopting this scheme must supply two operators whose independence is verifiable or trusted by some
mechanism outside this paper's own construction, since the paper's cryptography offers no way to detect or
punish collusion, only to define the guarantee that holds in its absence. The networked throughput figures
depend on the specific inter-region link measured (AWS `us-east-1` to `us-east-2`); the paper does not
claim these figures generalize to two servers operated by mutually independent organizations on arbitrary,
possibly higher-latency or lower-bandwidth, network paths.

### Contradicts
None found against other corpus entries on a measured fact. This entry's figures match, and were the
source for, the figures already recorded under this KEY in the corpus's `interactive-private-search.md`
open-problem synthesis, including its comparison there to single-server schemes (SimplePIR, DoublePIR,
YPIR, Piano) on communication, throughput, and trust assumption.

### References worth retrieving
- **Foundational** — Amos Beimel, Yuval Ishai, Tal Malkin. "Reducing the Servers' Computation in Private
  Information Retrieval: PIR with Preprocessing." CRYPTO 2000. (Cited as [BIM00]; the original
  PIR-with-preprocessing protocol this paper directly builds on and benchmarks its storage reduction
  against.)
- **Foundational** — Ghoshal, Li, Ma, Dai, Shi. TCC 2025. (Cited as [GLM+25]; the paper this work's
  many-server generalization builds on, also used as a storage-comparison baseline.)
- **Competing** — Benny Chor, Oded Goldreich, Eyal Kushilevitz, Madhu Sudan. 1995. (Origin of XOR PIR,
  cited as [CGKS95]; the linear-time baseline this paper implements itself and benchmarks against
  head-to-head.)
- **Competing** — cited as [HHCG+23] in this paper (source of the "XOR PIR fast" optimization this paper's
  own XOR PIR implementation uses) — bibliography detail not fully captured in this extraction pass;
  retrieve to confirm identity, likely overlapping with HENZINGER-SOSP-23's or a related SimplePIR/
  DoublePIR author set already in this corpus.
- **Competing** — Samir Jordan Menon, David J. Wu. "YPIR: High-Throughput Single-Server PIR with silent
  preprocessing." (Cited as [MW24]; already summarized via this corpus's `interactive-private-search.md`
  entry, not independently retrieved under its own KEY in this batch.)
- **Foundational** — cited as [LLF+25] in this paper, described as showing three non-colluding servers can
  achieve information-theoretic privacy with o(n) communication — bibliography detail not fully captured
  in this extraction pass; retrieve to confirm identity and compare its communication figure against this
  paper's own stated n^0.31-scale future-work target.

### Verbatim extracts
- "the first information-theoretic PIR with any constant number of servers that has quasilinear server
  storage n^(1+o(1)) and polynomially sublinear server time n^(1-Ω(1))."
- "The main limitation of our protocol is its large communication complexity."
- "by blowing up the storage by 93×, our PIR scheme provides a 2,560× decrease in the number of memory
  accesses per query."
- "when the ratio D/m is sufficiently close to 1/2, our schemes do not show a throughput gain (when
  including network costs)."
- "We leave implementing and optimizing these communication-shrinking techniques for future work."
