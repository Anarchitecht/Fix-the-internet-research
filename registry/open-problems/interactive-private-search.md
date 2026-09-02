# Private search at interactive latency

## Verdict: partly

Private information retrieval (PIR) — a protocol letting a client fetch one record from a
server-held database without the server learning which record was fetched — now reaches
sub-second-to-low-second latency for a single-record fetch by known index, using one untrusted
server and no assumption that a second party stays uncorrupted. Search is a harder problem: the
client does not know the index in advance and must find which record matches a query, which means
some mechanism must rank or narrow candidates without revealing the query. One published system,
Tiptoe (Henzinger, Dauterman, Corrigan-Gibbs, Zeldovich, ACM Symposium on Operating Systems
Principles (SOSP) 2023), reaches full private search — hiding the query from a single, possibly
malicious server, over 360 million web pages — at 2.7 seconds of end-to-end latency. That figure
is the best published one under the condition a decentralized deployment can supply: one untrusted
server, no non-collusion assumption. It is not sub-second. Every published system that reaches
sub-second or high-throughput figures for search does so by adding an assumption a decentralized
deployment cannot cheaply supply: a second, non-colluding party, a relaxation from cryptographic
query-hiding to differential privacy over a crowd of simultaneous queriers, or both.

## What "interactive latency" means here

The brief supplying this problem states no numeric latency bound, and none of the retrieved papers
measures human perception of interactivity — so no number is asserted here as a threshold. The
retrieved papers describe their own latency in the same terms: Tiptoe's authors write that their
design goal is to "keep the client-perceived latency on the order of seconds," and separately
describe the tension their design resolves as searching hundreds of millions of documents "all in
the span of seconds." This entry reports each system's own measured latency figure, under its own
stated network conditions, so a reader can compare it against whatever latency bound their own
deployment requires.

## Current best single-server throughput, query size, and response size (record fetch by known index)

Two related schemes, evaluated on the same AWS `c5n.metal` or `r6i.16xlarge` hardware, define the
current state of the art for single-server PIR — one server holds the database in the clear, and
the privacy guarantee needs no assumption about a second party.

**SimplePIR and DoublePIR** (Henzinger, Hong, Corrigan-Gibbs, Meiklejohn, Vaikuntanathan, USENIX
Security 2023, "One Server for the Price of Two"). SimplePIR precomputes a "hint" — a matrix
derived from the database, downloaded once by every client and reused across an unbounded number
of later queries — from a learning-with-errors (LWE) linearly homomorphic encryption scheme. At
query time the server performs fewer than one 32-bit multiplication and one 32-bit addition per
database byte. Measured single-threaded on an AWS `c5n.metal` instance: SimplePIR reaches 10.3
GB/s per core (81 percent of the machine's memory bandwidth), DoublePIR 7.6 GB/s per core, at a
per-query online communication of 242 KB (SimplePIR) or 345 KB (DoublePIR) for a 1 GB database.
The unavoidable cost is the hint: 121 MB for a 1 GB database under SimplePIR, or a database-size-
independent 16 MB under DoublePIR, downloaded before the first query and re-downloaded whenever the
database changes enough to invalidate it.

**YPIR** (Menon, Wu, USENIX Security 2024, "High-Throughput Single-Server PIR with Silent
Preprocessing"). YPIR removes the hint download by compressing DoublePIR's response online using a
ring-LWE packing transformation, at the cost of a larger query. Measured single-threaded on an AWS
`r6i.16xlarge`: at a 32 GB database, YPIR reaches 12.1 GB/s per core (97 percent of SimplePIR's
throughput on the same hardware, no hint required), with an 846 KB-to-2.5 MB query (across the 1
GB-to-32 GB range tested) and a 12 KB response. The same paper's own benchmark of Tiptoe's PIR
scheme, run on identical hardware, measured 415 MB/s to 1.5 GB/s across the same size range — 8 to
19 times slower than YPIR, because Tiptoe's response-compression step (built for a different design
point, described below) consumes over 85 percent of its server time.

**Piano** (Zhou, Park, Zheng, Shi, IEEE Symposium on Security and Privacy (S&P) 2024, "Extremely
Simple, Single-Server PIR with Sublinear Server Computation"). Piano trades a one-time linear
streaming download of the database (client-side preprocessing) for sublinear per-query
communication, computation, and client storage, all of order the square root of the database size,
each amortized over roughly that many later queries. On two AWS `m5.8xlarge` instances at a 100 GB,
1.68-billion-entry database, with a wide-area-network round-trip time of about 60 ms: 72.6 ms
online query latency, 100 KB online communication, 839 MB client storage — a 7 to 20 percent
latency overhead over a non-private linear-scan baseline measured on the same link, and roughly 150
times faster than the same paper's extrapolated SimplePIR figure at that scale. Piano's own security
proof is against a probabilistic-polynomial-time adversary that may deviate from the protocol
(stronger than an honest-but-curious assumption), still with a single server and no non-collusion
requirement.

For a known-index record fetch, this half of the problem is solved under the condition a
decentralized deployment can supply — one untrusted server, no second party required — at latency
from roughly 70 ms (Piano, 100 GB database, 60 ms round trip) up to single-digit seconds
(SimplePIR/DoublePIR/YPIR's own server compute time, before adding network latency, ranges from 74
ms to 3.2 s across 1-32 GB databases). The unresolved costs are the ones each paper itself states:
a hint download that must be repeated on database change (SimplePIR/DoublePIR), or a full-database
streaming download at setup and after roughly root-N queries (Piano), or a larger query that
carries a packing key (YPIR).

## Current best multi-server figures, non-collusion assumption stated

Multi-server PIR splits the database (or its encoding) across multiple servers and asks the client
to query all of them; privacy holds only if the servers do not share what they each received —
this is the non-collusion assumption the brief asks to be stated explicitly wherever it appears.

**Classic linear-time two-server PIR**, benchmarked by Henzinger et al. on their own `c5n.metal`
hardware as a baseline (not the paper's own contribution): a distributed-point-function-based
two-server scheme reaches 5.4 GB/s per core (each server does one linear scan under a
pseudorandom-function-masked query); an XOR-based two-server scheme, which is only constant-time
under a side-channel-vulnerable implementation, reaches up to 11.8 GB/s per core. Both figures are
for a known-index fetch, not search, and both require the client to trust that the two servers do
not compare notes on the query they each received.

**Two-server PIR with preprocessing** (Henzinger, Ragavan, IACR ePrint 2025/2008, "Two-Server
Private Information Retrieval in Sublinear Time and Quasilinear Space" — accepted to Eurocrypt
2026). This is the most recent published advance in the multi-server line and provides
information-theoretic privacy (unconditional given non-collusion, not resting on a computational
hardness assumption) against a 2-out-of-2 collusion threshold — either server alone learns nothing,
identical to the classic two-server assumption above. It precomputes a data structure of size
roughly 1.5 times the square root of log(n) times n bits (n the database size in bits) and answers
each query by reading roughly n^0.82 bits from it, the first information-theoretic PIR with any
constant server count to combine quasilinear server storage with polynomially sublinear per-query
server time. Measured on an AWS `r7a.metal-48xl` instance, with the two servers placed in different
AWS regions (`us-east-1` and `us-east-2`) to include real network cost: on an 11 GB database with
1-byte records, encoded into a 1 TB per-server structure (a 93-times storage blowup), each query
reads and returns 4.4 MB, giving 636 queries per second — 9 times the throughput of the classic
XOR-based two-server baseline on the same hardware. On a 250 MB database the same construction
reaches 24,252 queries per second, a 6.6-times gain. The paper's own stated limitation is
communication: its download grows as a database-size exponent between one-half and one, tens of
megabytes to gigabytes in the tested range, one to three orders of magnitude larger than the
XOR-PIR baseline's, and the authors state the throughput gain vanishes once that larger download
saturates the network link before the memory-access savings can be realized.

Two-server PIR remains faster, per core, than any single-server scheme measured above (5.4-11.8
GB/s baseline, 636-24,252 queries/second for the newest preprocessing variant) at the cost of a
trust assumption a decentralized deployment cannot verify by cryptography alone: that two
server-hosting parties, both reachable by the client, do not collude. All multi-server figures
above are for a known-index fetch, not search.

## Whether any construction reaches interactive latency for search — the harder problem

Search differs from a record fetch by known index in one respect that drives every design choice
below: the client does not know which record answers its query, so some component must locate a
matching record without seeing the query in the clear. Four published systems address this
directly, each retrieved and read in full for this entry.

**Tiptoe** (cited above). Tiptoe maps documents to short vectors — semantic embeddings, a
machine-learning technique where documents close in meaning produce vectors close in inner-product
distance — and reduces private full-text search to private nearest-neighbor search: find the
document vector maximizing inner-product score against the client's query vector. The server
computes inner-product scores under linearly homomorphic encryption over every document, so it
never sees which score the client later decodes; to keep communication sublinear, documents are
grouped into roughly root-N clusters, and the client uses a PIR-like sub-protocol to fetch only the
cluster nearest its query without revealing which cluster that is. Measured on a 45-machine AWS
`r5.xlarge` cluster (bottlenecked by memory bandwidth, not compute) over the C4 web crawl, 364
million pages, with a simulated 100 Mbps, 50 ms round-trip-time client link: 2.7 seconds end-to-end
latency, 145 core-seconds of total server compute, 56.9 MiB of communication (74 percent of which
completes before the client enters its query). Search quality on the MS MARCO benchmark: average
rank of the correct result, 7.7 out of 100 — worse than a state-of-the-art non-private neural
retriever (2.3) but close to classical term-frequency-inverse-document-frequency (tf-idf) search
(6.7), and the paper states the method performs worst on exact-string queries such as phone
numbers or addresses. Trust model: a single logical server, which the paper's own privacy
definition allows to be fully adversarial (it may deviate from the protocol arbitrarily) without
breaking query privacy — correctness and availability, not privacy, are what a malicious server can
break. No non-collusion assumption anywhere in the core protocol; the 45 physical machines are one
trust domain sharded for parallel throughput, not separate non-colluding parties. Against the
prior state of the art (Coeus, a tf-idf-based private Wikipedia search system, extrapolated to web
scale), Tiptoe's own comparison states more than 1,000 times lower AWS cost.

**Pacmann** (Zhou, Shi, Fanti, IACR ePrint 2024/1600, later ICLR 2025, "Efficient Private
Approximate Nearest-Neighbor Search"). Pacmann replaces Tiptoe's clustering with graph traversal:
the client runs the search itself, walking a server-built, fixed-out-degree navigable graph and
fetching each visited vertex's neighbor list through Piano (described above), so the server never
sees which vertices were fetched. Measured on a single-thread, single-CPU server (2.4 GHz Intel
Xeon E5-2680), wide-area-network setting (50 ms round-trip time): 3.0 seconds online query latency
at 100 million SIFT vectors, 1.1 seconds at 3.2 million MS MARCO documents, reaching about 90
percent of a non-private graph-search baseline's recall. Trust model: single server, semi-honest
(the security proof explicitly does not cover a malicious server, unlike Tiptoe's). The requirement
that drives Pacmann's cost: every client must complete a full linear-cost streaming download of the
encoded graph before any query — 59.6 GB of preprocessing communication and 272 seconds of
preprocessing time at the 100-million-vector scale — and this preprocessing must repeat whenever
the database changes, since the paper states dynamic updates are unsupported and left as an open
problem. Pacmann's own authors calibrate their numbers directly against Tiptoe's and report a 60
percent latency reduction over Tiptoe's cluster-based approach at matched scale (100 million
records), but at a materially different, heavier client-storage cost (roughly 3 GB versus Tiptoe's
kilobyte-scale per-query state).

**Panther** (Li, Huang, Zhang, Hong, Liu, Wei, Chen, ACM Conference on Computer and Communications
Security (CCS) 2025, IACR ePrint 2024/1774). Panther is the only one of the four search systems
retrieved here that also protects the database from the client — the client learns only its
top-k result, not the rest of the corpus — using an interactive two-party protocol between client
and server combining secret sharing, garbled circuits, and homomorphic encryption. Measured on a
64-vCPU, 256 GB cloud instance, both under a local-area network (4,000 Mbps, 1 ms round-trip) and a
wide-area network (320 Mbps, 74 ms round-trip): at 10 million points (the Deep1B-10M dataset), 3.89
seconds local-area, 18.3 seconds wide-area, 284 MB of communication; at 1 million points, 1.49-1.50
seconds local-area, 8.71-9.32 seconds wide-area, 93-99 MB. Trust model: explicitly semi-honest, a
weaker guarantee than Tiptoe's malicious-tolerant query privacy. Panther requires multiple
interactive communication rounds between client and server, so its wide-area latency is dominated
by round-trip count rather than raw computation — the paper's own comparison to a two-server scheme
(Preco/Servan-Schreiber et al.) shows that scheme reaching 6.13 seconds at 10 million points, 3
times faster than Panther under Panther's wide-area setting, but only because that comparison's two
servers sit in the same AWS region as each other rather than being placed to reflect two genuinely
independent, geographically separated operators — the condition non-collusion in practice requires.

**Wally** (Asi, Boemer, Genise, Mughees, Ogilvie, Rishi, Rothblum, Talwar, Tarbe, Wadia, Zhu,
Zuliani, arXiv 2406.06761, Apple). Wally reaches the highest throughput of any system in this
section — up to 66,000 queries per second at 1 million entries, 500,000 concurrent users — by
changing what is being guaranteed. Instead of cryptographically hiding each query, Wally batches
queries from many simultaneous, non-coordinating clients into fixed-length epochs, has each client
independently add a randomized number of fake queries (drawn from a negative binomial distribution,
chosen because it is non-negative and infinitely divisible, so many clients can add noise
independently without coordinating), and routes every query — real and fake — through a separate
anonymization service assumed not to collude with the search server. The server then computes only
over the clusters actually queried in that epoch, not the whole database, and the guarantee is
(epsilon, delta)-differential privacy over the batch, not per-query cryptographic
indistinguishability: the paper's own tested setting is epsilon = 0.1, delta = 2^-26. Three
conditions do the work behind Wally's throughput figures, none of which the paper claims to remove:
first, a second, non-colluding party — the anonymization service — exactly the two-party trust
assumption single-server PIR was built to avoid, though the paper argues existing anonymization
infrastructure (Tor, mix networks) already satisfies it; second, tens to hundreds of thousands of
simultaneous, non-coordinating queriers within one epoch (the paper's own tested range is 100,000
to 500,000 users) — a volume the paper itself flags as required to keep the number of fake queries
per client low, and a volume a small or specialized corpus is unlikely to have; third, and directly
relevant to interactive latency, a client's own query is not answered until its epoch closes — the
paper states epoch length "ranges from tens of seconds to a few minutes" (10 seconds at 1 million
entries and 100,000 users, up to 6 minutes at 100 million entries and 500,000 users) — so Wally's
gain is in aggregate server throughput under sustained concurrent load, not in the latency any
single query experiences, which is worse than Tiptoe's 2.7 seconds at every tested configuration.
The paper's own motivating example — background retrieval of photo context for on-device models,
not a query a person waits on — states this trade explicitly: "high throughput is a must, while low
latency can be relaxed." Wally's own authors position the system for that class of workload, not
for a query a client is waiting on.

## What the assumption does in each case

Ranking the four search systems by measured single-query latency against the trust and volume
condition each one needs:

| System | Latency (stated setting) | Trust condition beyond "one untrusted server" | What it protects |
|---|---|---|---|
| Tiptoe | 2.7 s (360M docs, 50 ms RTT) | none | query only, against a possibly malicious server |
| Pacmann | 1.1-3.0 s (3M-100M vectors, 50 ms RTT) | none, but semi-honest only | query only, against a semi-honest server |
| Panther | 1.49-18.3 s (1M-10M points, 1-74 ms RTT) | none, but semi-honest only, and interactive (multi-round) | query and database contents |
| Wally | tens of seconds to minutes per epoch | a second, non-colluding anonymization service; 100K-500K concurrent queriers per epoch | query only, to (0.1, 2^-26)-differential privacy, not cryptographic indistinguishability |

No entry in this table reaches sub-second single-query latency without adding an assumption. The
two entries that add no extra trust party (Tiptoe, Pacmann) both land in the 1-to-3-second range at
their tested scale, not sub-second. The one entry that reaches sub-second-equivalent throughput
(Wally) does so by trading per-query latency for aggregate throughput under a batch, adding a
non-colluding second party, and requiring a query volume most decentralized deployments will not
have. The one entry closest to sub-second latency at small scale (Panther, 1.49 s local-area at 1
million points) needs a local-area-class network round trip to get there — its own wide-area figure
at the same scale is 8.71-9.32 seconds — and even then only under a semi-honest server, a strictly
weaker guarantee than Tiptoe provides at the same latency order.

## Where this leaves a decentralized deployment

A single node, individually untrusted and possibly malicious, can serve private search over a
public corpus at 1-to-3-second latency at hundred-million-document scale (Tiptoe) or
million-to-hundred-million-vector scale (Pacmann), with no requirement that any second party stay
honest or uncorrupted — the condition this architecture is built to supply. Reaching materially
lower latency, or higher throughput under load, in every published construction retrieved here
means adding one of: a second party that must not collude with the first (classic two-server PIR,
Wally's anonymization service, Panther's semi-honest-only relaxation weakening what "untrusted"
covers), a query volume in the hundreds of thousands of simultaneous users (Wally), or acceptance
of a differential-privacy guarantee instead of cryptographic query-hiding (Wally). None of these
three is free for a decentralized deployment to supply: a second non-colluding party is exactly the
trust assumption absent in a network of mutually distrusting, individually operated nodes; a
guaranteed pool of hundreds of thousands of concurrent queriers does not exist for a small or
young network, or for any corpus narrower than a web-scale crawl; and a differential-privacy
guarantee is a different, weaker claim about what a query reveals than the "computationally
indistinguishable from any other query" claim cryptographic PIR makes, a distinction any
consuming component would need to state explicitly rather than treat as equivalent.

Exact-match search (a phone number, a URL, a specific string) is a further gap inside this partial
result: Tiptoe's own evaluation states its embedding-based approach performs worst exactly on this
query class, and its own proposed fix — a separate private key-value backend per exact-match query
type, queried through keyword PIR — is described in the paper's future-work section, not built or
measured there.

## What was searched

Corpus entries opened in full: `ANGEL-SP-18`, `CHOR-JACM-98`, `CORRIGANGIBBS-CCS-10`,
`CORRIGANGIBBS-SP-15`, `DAVIDSON-POPETS-18`, `DAVIDSON-POPETS-23`, `HENZINGER-USENIXSEC-23`,
`MENON-SP-22`, `MENON-USENIXSEC-24`, `MUGHEES-CCS-21`, `ZHOU-EPRINT-24`, `ZHOU-SP-24`, plus the
measurement and requirements index rows for each. Beyond the corpus: DBLP
(`dblp.org/search/publ/api`) queried for "tiptoe private web search," "wally scalable private
search," "Panther private approximate nearest neighbor search single server," "two-server private
information retrieval," "private nearest neighbor search 2025," "private information retrieval
survey systematization," "real-time private search encryption," and "private information retrieval
attack 2025." IACR ePrint searched directly for the Panther and two-server-PIR preprocessing
papers once their ePrint identifiers were found through DBLP's cross-reference. No 2023-2026
systematization-of-knowledge or survey paper on private search or private nearest-neighbor search
turned up in any of these queries; the most recent items found were the individual system papers
already retrieved (Wally's own arXiv revision is dated July 2026; the two-server preprocessing
paper is dated July 2026 and accepted to Eurocrypt 2026). Full text retrieved and read for four
papers not previously in the corpus: `HENZINGER-SOSP-23` (Tiptoe, via
`pdos.csail.mit.edu/papers/tiptoe:sosp23.pdf`, the paper's own posted PDF, after its DOI-listed ACM
page proved closed-access), `ASI-ARXIV-24-WALLY` (via arXiv), `LI-CCS-25-PANTHER` (via IACR
ePrint 2024/1774), and `TWOSERVER-EPRINT-25` (via IACR ePrint 2025/2008). All four are full text,
not abstracts; every figure reported above under those keys was read from the retrieved text, not
carried over from a search snippet.
