## [HENZINGER-USENIXSEC-23] One Server for the Price of Two: Simple and Fast Single-Server Private Information Retrieval
**Citation:** Alexandra Henzinger, Matthew M. Hong, Henry Corrigan-Gibbs, Sarah Meiklejohn, Vinod Vaikuntanathan. "One Server for the Price of Two: Simple and Fast Single-Server Private Information Retrieval." USENIX Security Symposium, 2023.
**Retrieved:** full text via https://eprint.iacr.org/2022/949.pdf
**Source URL:** https://eprint.iacr.org/2022/949.pdf
**Domain:** G

### What it does
Private information retrieval (PIR) lets a client fetch one record from a server-held database
without the server learning which record was requested. The paper defines two single-server PIR
schemes — meaning the database lives on one server, with no non-colluding-server assumption — built
around a preprocessing step that shifts almost all server computation to a one-time offline phase,
independent of any client query.

Mechanism (SimplePIR): the server represents the N-record database as a square matrix D of
dimension roughly sqrt(N) by sqrt(N). Using Regev's learning-with-errors (LWE) based linearly
homomorphic encryption, the server precomputes, once per database and independent of any query, a
"hint" matrix that lets it later evaluate most of the matrix-vector product needed to answer a
query. This hint is not specific to any client; every client downloads and reuses the same hint
across an unbounded number of queries. To make one query, the client sends an encrypted
sqrt(N)-dimensional selection vector; the server computes the encrypted matrix-vector product using
its precomputed hint, needing per database byte fewer than one 32-bit multiplication and one 32-bit
addition at query time; the client decrypts to recover the requested column, then extracts its
desired record from that column using its own copy of the hint. The client holds no secret state
across queries (in contrast to schemes like SealPIR, whose clients keep persistent long-term
cryptographic secrets); the paper proves in an appendix that a malicious server can mount a
state-recovery attack against such stateful designs, breaking both past and future query privacy,
and states its stateless schemes are not vulnerable to that attack class.

Mechanism (DoublePIR): applies SimplePIR recursively to its own hint. In SimplePIR, of the
downloaded hint and the encrypted sqrt(N)-dimensional vector, the client actually needs only one
small part of the hint and one component of the vector to recover its record. DoublePIR runs
SimplePIR a second time over the hint matrix itself (using a non-black-box construction that saves a
factor equal to the lattice dimension — 1024 for the paper's chosen parameters — over a naive
recursive design), shrinking the client-downloaded hint to a size independent of the number of
records in the database, at the cost of higher per-query online communication and lower throughput
than SimplePIR.

Mechanism (private approximate set membership, applied to Certificate Transparency signed-certificate-timestamp
(SCT) auditing): the paper builds a new data structure for private set membership using either PIR
scheme, tolerant of a constant false-positive rate. Where a standard Bloom filter or PIR-by-keyword
approach requires the client to run PIR over a lambda*N-bit database (lambda approximately 128, the
security parameter, N the set size), this structure requires PIR over only 8N bits, a roughly
16x reduction in the size of the database the PIR is run over for this application.

### Measured results
All throughput measurements: single-threaded execution on an AWS c5n.metal instance running Ubuntu
22.04; each throughput figure is the average of five runs, with reported standard deviations under
10% of the measured throughput in all cases. Implementation: fewer than 1,200 lines of Go plus 200
lines of C for SimplePIR, plus 210 additional lines of Go for DoublePIR, no external library
dependencies, published under an MIT license.

| Scheme | Servers | Communication scaling | Max. measured throughput/core |
|---|---|---|---|
| DPF-based two-server PIR | 2 | O(log N) | 5,381 MB/s |
| XOR-based two-server PIR (constant-time) | 2 | O(sqrt N) | 6,067 MB/s |
| XOR-based two-server PIR (non-constant-time, side-channel-vulnerable) | 2 | O(sqrt N) | 11,797 MB/s |
| SealPIR | 1 | O(sqrt N) | 97 MB/s |
| MulPIR | 1 | O(sqrt N) | 69 MB/s (figure taken from the MulPIR paper; no public implementation available to these authors) |
| FastPIR | 1 | O(N) | 215 MB/s |
| OnionPIR | 1 | O(log N) | 104 MB/s |
| Spiral family | 1 | O(log N) | 1,314 MB/s |
| Kushilevitz-Ostrovsky + Paillier | 1 | O(N^epsilon) | 0.131 MB/s |
| XPIR | 1 | O(sqrt N) | 142 MB/s (figure taken from the SealPIR paper) |
| FrodoPIR (concurrent work) | 1 | O(sqrt N) | 1,256 MB/s |
| SimplePIR (this paper) | 1 | O(sqrt N) | 10,305 MB/s |
| DoublePIR (this paper) | 1 | O(sqrt N) | 7,622 MB/s |

Throughput figures normalized per core (two-server figures divided by two). Database and record
sizes underlying each figure are listed in the paper's Appendix A; for each competing scheme the
authors used the entry size that produced the highest reported throughput for that scheme.

Headline server-throughput comparison: SimplePIR reaches 10 GB/s/core (stated as 81% of the tested
machine's memory bandwidth), and DoublePIR reaches 7.4 GB/s/core, roughly 8x faster than the fastest
prior single-server PIR designed for the streaming setting (SpiralStreamPack) and roughly 30x faster
than the fastest prior single-server PIR designed for short entries (Spiral), both compared on the
same c5n.metal instance under the same methodology. SimplePIR/DoublePIR's per-core throughput
exceeds the per-server throughput of two-server PIR from distributed point functions (5.3 GB/s/core
cited). A hard upper bound for linear-work two-server PIR, measured by running only XOR operations
over the database, was 5.9 GB/s/core (full linear scan) and 11.5 GB/s/core (scan of a random half of
the database, non-constant-time).

| Quantity | SimplePIR | DoublePIR |
|---|---|---|
| Server compute per query, on a 1-byte-record database | fewer than one 32-bit multiplication and one 32-bit addition per database byte | same order, plus one additional SimplePIR-style recursive step |
| Hint size, general formula | roughly 4*sqrt(N) KB for a database of N bytes | roughly 16 MB for a database of one-byte records, independent of record count |
| Per-query online communication, 1 GB database | 242 KB | 345 KB |
| Hint size, 1 GB database | 121 MB | not separately stated at this size; the general 16 MB figure is for one-byte records |

Communication/throughput trade-off (Figure 6, database of 2^33 bits, entry sizes swept from 100 KB
to 10 MB, communication amortized over 100 queries): on databases with short entries, DoublePIR's
amortized communication is comparable to the most communication-efficient prior schemes (Spiral,
SpiralPack, SealPIR, OnionPIR); as entry size grows, DoublePIR's amortized communication rises
because the client downloads more hints. SpiralStream, SpiralStreamPack, and FastPIR — the schemes
with throughput closest to SimplePIR/DoublePIR — have much larger amortized communication than
either SimplePIR or DoublePIR on entry sizes below one kilobit.

Certificate Transparency SCT-auditing application: roughly five billion active SCTs exist in the web
today (cited to a third-party measurement source, not measured by this paper), with roughly six
million added or removed per day. Google Chrome's deployed approach provides k-anonymity for k=1000
and requires 24 bytes average client communication per TLS connection. This paper's PIR-based
construction, providing full cryptographic privacy rather than k-anonymity, requires 150 bytes and
0.0003 core-seconds of server compute per TLS connection on average, plus 16 MB of client download
and 150 KB of client storage per month to maintain the hint.

### Parameters
Security: plain learning-with-errors (LWE) assumption (Regev's encryption scheme), stated by the
authors as a weaker, more standard cryptographic assumption than the ring-LWE or NTRU-style
assumptions some prior lattice-based single-server PIR schemes use. Lattice dimension used for the
paper's concrete parameters: 1,024 (the value the DoublePIR construction's stated savings factor is
computed against). LWE parameters (n, q, chi) and plaintext modulus p are defined generically in the
construction (Section 4-5 formal descriptions) with p much less than q, delta = floor(q/p); the paper
does not give one single fixed numeric (n, q, chi, p) tuple as "the" deployment parameter set in the
text extracted here — parameters are chosen per database size via the paper's own selection
procedure, with database and record sizes for each comparison point tabulated in Appendix A. Security
notion: (T, epsilon)-security, indistinguishability of query distributions for any two indices i, j
against an adversary running in time at most T, with distinguishing advantage at most epsilon.
Certificate Transparency false-positive tolerance: the client's approximate-membership check is
correct in that a member string always returns "valid," but a non-member string returns "valid" with
probability at most 1/2 (a single check); correctness against a malicious auditor is explicitly not
required, since a malicious auditor could trivially misstate its own set of SCTs. Private
approximate-set-membership data-structure size: 8N bits for a set of size N, versus lambda*N bits
(lambda approximately 128) for a standard Bloom filter run under PIR, a stated 16x size reduction
driving a corresponding throughput speedup in the SCT application.

### Stated limitations
Two limitations are stated directly by the authors. First, the client must download a hint before
making any query; on databases of gigabyte scale the hint is tens of megabytes, and if a client makes
only a single query, hint download dominates total communication. Second, both schemes' online
per-query communication is on the order of hundreds of kilobytes, roughly 10x larger than some prior
single-server PIR schemes achieve. The authors state these as an intentional trade-off — large
computation savings and a small, simple codebase, at the cost of communication and storage overhead —
rather than as unresolved problems. Constructing a linearly homomorphic encryption scheme with
preprocessing that produces a smaller hint than sqrt(N) hints of sqrt(N) inputs each is stated as an
open direction for future work, which would reduce the offline communication in the resulting PIR
schemes. The Certificate Transparency auditing protocol does not require correctness to hold against
a malicious auditor (an auditor that lies about its own SCT set is not defended against), only privacy
for an honest client interacting with such an adversary; the paper explicitly limits its stated
security property to client privacy in that setting, not universal correctness. Extending the private
set-membership construction so that a malicious auditor cannot cause a legitimate website to be
flagged incorrectly is stated as an intriguing direction for future work, not solved in this paper.

### Requirements it places on the rest of the system
A deployment must give every client an offline channel to download the per-database hint (121 MB for
a 1 GB database under SimplePIR, or 16 MB independent of record count under DoublePIR for one-byte
records) before that client's first query, and must re-distribute an updated hint whenever the
underlying database's content changes materially enough to invalidate the old hint's precomputed
structure; the paper does not analyze hint refresh cost under a continuously updating database, so a
system with frequent updates needs a separate accounting of that cost. Because clients hold no secret
state across queries, a system built on these schemes does not need the persistent per-client
key-management infrastructure that stateful schemes like SealPIR require, and is immune to the
state-recovery attack the paper describes against stateful designs — but the hint's non-client-specific,
reusable nature means the server must serve the identical hint to every client, so a design cannot
customize per-client database views through the hint mechanism. Security relies on the plain LWE
assumption; the throughput and communication figures reported here presuppose the AWS c5n.metal
single-threaded benchmarking environment the paper used, and porting the throughput number to a
different core or memory-bandwidth profile requires re-measurement, since SimplePIR's headline
throughput is explicitly reported relative to that machine's own memory bandwidth (81%). The
Certificate Transparency application requires the auditor (Certificate Transparency log server or
proxy) to hold the full SCT set the client will query against and to serve the same hint to all
clients; the paper's stated 16x speedup over Bloom-filter-based approaches for this application
assumes acceptance of a constant false-positive rate rather than exact membership.

### Contradicts
None found. The paper positions SimplePIR/DoublePIR as new points on a throughput-communication
trade-off curve, not as invalidating prior schemes' claims. Cross-paper in this corpus: this entry's
1,314 MB/s figure attributed to "the Spiral family" (their Table 1, sourced by these authors from the
Spiral paper or a related paper for the entry size that produced Spiral's own best reported
throughput) is not directly comparable, entry-size for entry-size, to the specific per-configuration
throughput numbers recorded in MENON-SP-22's own Table 2/3/4 in this corpus (which range from
159 MB/s to 1.94 GB/s across configurations); a reader combining the two entries should use each
paper's own reported configuration rather than treat the single 1,314 MB/s figure as Spiral's
throughput in general. MENON-USENIXSEC-24 (YPIR, this corpus) is the authors' own later paper
explicitly built to reach SimplePIR-class throughput while retaining Spiral-style small per-query
communication; a synthesis combining all three entries should check MENON-USENIXSEC-24's comparison
table against the SimplePIR/DoublePIR numbers recorded here rather than assume consistency.

### References worth retrieving
- Kushilevitz, Ostrovsky, "Replication is not needed: Single database, computationally-private
  information retrieval," FOCS 1997 — foundational (the paper's explicit starting-point construction;
  SimplePIR's server matrix representation and the DoublePIR recursion both descend from this).
- Regev, "On lattices, learning with errors, random linear codes, and cryptography," STOC 2005 —
  foundational (defines the LWE assumption and the Regev encryption scheme SimplePIR is built on).
- Chor, Goldreich, Kushilevitz, Sudan, "Private information retrieval," (journal version CHOR-JACM-98
  in this corpus) — foundational (defines PIR in the multi-server setting).
- Angel, Chen, Laine, Setty, "PIR with compressed queries and amortized query processing" (SealPIR) —
  competing (direct throughput comparison target; also the subject of the stateful-client
  state-recovery attack this paper describes in its appendix).
- Menon, Wu, "Spiral: Fast, high-rate single-server PIR via FHE composition" (MENON-SP-22 in this
  corpus) — competing (direct throughput/communication comparison target across every table).
- Ahmad, Yang, Agrawal, El Abbadi, Gupta, "Addra" (FastPIR) — competing (direct comparison target).
- Mughees, Chen, Ren, "OnionPIR: Response efficient single-server PIR" — competing (direct comparison
  target).
- Ali, Lepoint, Patel, Raykova, Schoppmann, Seth, Yeo, "MulPIR" — competing (comparison target;
  throughput figure taken from the MulPIR paper directly, since no public implementation exists).
- Davidson, Pestana, Celi, "FrodoPIR" — competing (concurrent, near-identical throughput comparison
  target explicitly noted as concurrent work).
- Corrigan-Gibbs, Henzinger, Kogan, "Single-server private information retrieval with sublinear
  amortized time," EUROCRYPT 2022 — foundational (an earlier construction by an overlapping author
  set, a distinct paper from this one).
- Corrigan-Gibbs, Kogan, "Private information retrieval with sublinear online time," EUROCRYPT 2020 —
  foundational (predecessor sublinear-online-time PIR).
- Laurie, "Certificate transparency," Communications of the ACM — foundational (defines the
  Certificate Transparency system this paper's SCT-auditing application targets).
- DeBlasio, "Opt-out SCT auditing in Chrome" — foundational (describes Google Chrome's current
  k-anonymity-based SCT auditing approach, the deployed baseline this paper compares against).
- Bloom, "Space/time trade-offs in hash coding with allowable errors" — foundational (the Bloom
  filter, the baseline private-set-membership approach this paper's 8N-bit structure improves on).
- Chor, Gilboa, Naor, "Private information retrieval by keywords" — foundational (PIR-by-keyword,
  the second baseline approach for private set membership compared against this paper's structure).

### Verbatim extracts
"SimplePIR achieves 10 GB/s/core server throughput, which approaches the memory bandwidth."
"the client must download a 121 MB 'hint' about the database contents."
"DoublePIR, that shrinks the hint to 16 MB at the cost of slightly higher per-query communication."
"our client must download a 'hint': on databases gigabytes in size, the hint is tens of megabytes."
"requiring the client to perform PIR over a database of lambda*N bits... our data structure requires performing PIR over only 8N bits."
