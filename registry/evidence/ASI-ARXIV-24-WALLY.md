## [ASI-ARXIV-24-WALLY] Wally: Batched Private Nearest Neighbor Search at Scale
**Citation:** Hilal Asi, Fabian Boemer, Nicholas Genise, Muhammad Haris Mughees, Tabitha Ogilvie, Rehan Rishi, Guy N. Rothblum, Kunal Talwar, Karl Tarbe, Akshay Wadia, Ruiyu Zhu, Marco Zuliani. "Wally: Batched Private Nearest Neighbor Search at Scale." arXiv:2406.06761, Apple Inc., 2024 (revision retrieved dated July 2026).
**Retrieved:** full text via arXiv (retrieved for the corpus's `interactive-private-search.md` open-problem entry)
**Source URL:** https://arxiv.org/abs/2406.06761
**Domain:** G

### What it does
Wally answers a private nearest-neighbor query — finding which stored vector is closest to a client's
query vector without the server learning the query — for a batch of many simultaneous, non-coordinating
clients, trading the cryptographic query-hiding guarantee (computational indistinguishability, the
guarantee that no efficient adversary can tell which of two queries a client sent) that fully oblivious
schemes such as Tiptoe and Pacmann provide for a weaker, (epsilon, delta)-differential-privacy guarantee
over the batch: the server's view of the batch is statistically close (within a factor of e^epsilon,
except with probability delta) between the case a specific honest client participated and the case it did
not. The construction requires two parties: the search server, assumed semi-honest (follows the protocol
but tries to infer queries from what it observes), and a separate anonymization service — the paper's
threat model requires this service not to collude with the server, arguing existing deployed
anonymization infrastructure (Tor, mix networks) already carries this non-collusion property because
those services have "strong disincentives to collude with individual servers." Time is divided into
fixed-length epochs; every real query submitted in an epoch is routed through the anonymization service,
and every participating client independently adds a randomized number of fake queries per epoch, drawn
from a negative binomial distribution (chosen because it is non-negative and infinitely divisible, so many
clients' independently added noise still composes into the target aggregate noise distribution without
coordination). The server processes only the clusters actually queried (real or fake) in that epoch's
batch, computing scores homomorphically as in Tiptoe, rather than scanning the whole database — the
server never learns which of the queries routed to it in a given epoch were real and which were fake,
which is what produces the differential-privacy guarantee.

### Measured results
Server-side computation measured on a 6-core Intel Xeon w3-2423 central processing unit (CPU) with 32 GB
RAM; queries-per-second (QPS) figures extrapolate this single-core, single-query latency to a hypothetical
10,000-core server ("consistent with large-scale search deployments," the paper's own stated
justification, not a measurement of an actual 10,000-core deployment), a linear extrapolation the paper
states is valid because queries are processed independently with no inter-query synchronization. Dataset:
MS MARCO document ranking, roughly 3.2 million passages, embeddings generated from document title and
body. All reported communication and QPS figures for Wally include the overhead of fake queries,
amortized over each real query.

Head-to-head comparison against Tiptoe and Pacmann (Table 2), same MS MARCO corpus, differential-privacy
parameters epsilon = 0.1, delta = 2^-26, Wally figures computed assuming U = 500,000 participating honest
clients:

| System | Client storage | Communication (per query) | Queries per second | Mean Reciprocal Rank at 100 (MRR@100) |
|---|---|---|---|---|
| Tiptoe | 0.61 MB | 17.4 MB | 909 | 0.11 |
| Pacmann | 614 MB | 61.6 MB | 34,482 | 0.26 |
| Wally (K=256 clusters, Δ=1 cluster probed) | 0.04 MB | 0.56 MB | 25,974 | 0.12 |
| Wally (K=256, Δ=3) | 0.04 MB | 1.7 MB | 9,881 | 0.16 |
| Wally (K=256, Δ=5) | 0.04 MB | 2.6 MB | 6,667 | 0.18 |

Stated aggregate comparison: Wally reaches 7–29× higher QPS and 6.7–31× lower communication than Tiptoe,
and roughly 15,000× lower client storage than Pacmann; Pacmann reaches 1.3–5.6× higher QPS than Wally but
23–123× higher communication (depending on Δ), and the paper notes it did not include network round-trip
delay in Pacmann's QPS figure, while Pacmann's own multi-round-trip design would add such delay in
practice.

Database-size scaling (Table 3), Δ = 1 cluster probed, each configuration at (epsilon=0.1, delta=2^-26)-DP:

| Database entries | Users (U) | Clusters (K) | Expected fake queries per client | Request size | Response size | QPS (thousands) | Epoch size |
|---|---|---|---|---|---|---|---|
| 1,000,000 | 100,000 | 128 | 1.7 | 0.76 MB | 0.17 MB | 22,000 | 10 s |
| 1,000,000 | 500,000 | 256 | 0.3 | 0.36 MB | 0.04 MB | 66,000 | 10 s |
| 16,000,000 | 100,000 | 256 | 3.3 | 1.18 MB | 2.3 MB | 1,400 | 2 min |
| 16,000,000 | 500,000 | 512 | 1.7 | 0.76 MB | 1.5 MB | 3,200 | 3 min |
| 100,000,000 | 100,000 | 512 | 6.7 | 2.17 MB | 13.9 MB | 470 | 4 min |
| 100,000,000 | 500,000 | 1,024 | 2.6 | 1.01 MB | 3.03 MB | 1,390 | 6 min |

Cluster-count sensitivity (Table 4, U=100,000, Δ=3, 1 million entries): QPS falls from 31,000 (K=64 or
128) to 22,000 (K=256) to 15,000 (K=512) as K rises, with request size rising from 0.45 MB to 1.35 MB.
Cluster-probe-count sensitivity (Table 5, U=100,000, K=128, 1 million entries): QPS falls from 37,000
(Δ=1) to 21,000 (Δ=10) as Δ rises, with response size rising from 0.08 MB to 0.14 MB.

### Parameters
- Differential-privacy target used throughout the main evaluation: epsilon_0 = 0.05, delta_0 = 2^-30 per
  mechanism, composing (by the paper's own Theorem 6.1) to a per-epoch guarantee of (2 epsilon_0,
  2 Delta delta_0) = (0.1, 2 Delta · 2^-30) — for Delta (clusters probed per client) at most 5, this gives
  delta ≤ 2^-26; at most 10, delta ≤ 2^-25.
  measured directly as fake-query counts).
- Fake-query distribution: each client samples a random count of fake queries per cluster from a negative
  binomial distribution NB(r/U, p); the paper derives an expected-fake-queries bound of at most 0.006 ×
  Delta × K for U = 500,000, and states this is "a modest estimate for large-scale applications."
- Cluster count K and clusters probed per client Delta: swept from K=64 to K=1,024 and Delta=1 to Delta=10
  across the reported tables; the paper states it selected configurations minimizing the K·Δ product
  (which drives fake-query overhead) while keeping search accuracy acceptable.
- Assumed server hardware for QPS extrapolation: 10,000 cores, justified only as "consistent with
  large-scale search deployments" — not derived from a specific named deployment's published
  specification, and not itself a measured figure.

### Stated limitations
The paper states its own privacy guarantee requires the server and anonymization service to remain
independent, non-colluding parties — a second-party trust assumption neither Tiptoe nor Pacmann's
single-server designs need. It states a client's own query is not answered until its epoch closes, with
epoch length ranging "from tens of seconds to a few minutes" in the paper's tested configurations (10
seconds at 1 million entries and 100,000–500,000 users, up to 6 minutes at 100 million entries and 500,000
users) — the paper's own motivating example states this trade-off explicitly, framing Wally for background
retrieval (a photo-context lookup for on-device models) where "high throughput is a must, while low
latency can be relaxed," not for a query a client is waiting on interactively. It states the fake-query
volume needed to keep per-client overhead low depends on having a large pool of simultaneous,
non-coordinating queriers within one epoch, with the paper's own tested range at 100,000 to 500,000 users
— a volume the paper does not claim a small or specialized corpus is likely to have. Malicious clients who
withhold their fake queries can weaken the privacy guarantee for other honest clients in the same batch,
a threat the paper's model explicitly separates from server misbehavior and states is bounded, not
eliminated, by the protocol's design (Section on "Privacy due to malicious clients").

### Requirements it places on the rest of the system
Wally requires an anonymization service, deployed and operated separately from the search server, that
the client already trusts to route its query and fake queries without linking them to the client's
identity and without colluding with the search server — the paper states this is "practical" by pointing
to existing infrastructure (Tor, mix networks) rather than by building or measuring one itself in this
paper. The protocol requires a population of simultaneous, non-coordinating clients large enough that each
individual client's added fake-query noise, once aggregated across the whole epoch's batch, produces the
target aggregate differential-privacy guarantee — a downstream deployment with too few concurrent queriers
in a given epoch does not get the guarantee the paper's parameters target. The scheme requires the same
cluster-based document index structure Tiptoe uses (documents grouped by nearest-centroid clustering), so
any change to indexing strategy (for example, moving to Pacmann's graph-traversal index) is not a drop-in
substitution without re-deriving the fake-query and epoch-length parameters this paper's tables are
computed for.

### Contradicts
None found against other corpus entries on a measured fact. This entry's figures match, and were the
source for, the figures already recorded under this KEY in the corpus's `interactive-private-search.md`
open-problem synthesis. Note for downstream synthesis: Wally's own Table 2 comparison figures for Tiptoe
(0.61 MB storage, 17.4 MB communication, 909 QPS, MRR@100 = 0.11) are Wally's own authors' re-measurement
or re-estimation of Tiptoe's metadata-fetch step using the SimplePIR open-source implementation, run in
Wally's own environment — not figures directly copied from HENZINGER-SOSP-23's own paper text, which
reports different headline figures (2.7 s end-to-end latency, 56.9 MiB communication) measured on
different hardware (a 45-machine cluster) and a different corpus (364 million web pages, not the 3.2
million MS MARCO passages Wally's Table 2 uses). The two papers are not directly comparable on identical
conditions; a downstream synthesis citing "Wally is 7–29× faster than Tiptoe" must state this is under
Wally's own re-implementation on the smaller MS MARCO corpus, not a re-run of Tiptoe's own web-scale
benchmark.

### References worth retrieving
- **Competing** — Alexandra Henzinger, Emma Dauterman, Henry Corrigan-Gibbs, Nickolai Zeldovich. "Private
  Web Search with Tiptoe." SOSP 2023. (Cited as reference [46]; already retrieved in this batch as
  HENZINGER-SOSP-23 — the fully-oblivious baseline Wally's Table 2 re-benchmarks.)
- **Competing** — cited as reference [87] in this paper (Pacmann). (Zhou, Shi, Fanti, "Efficient Private
  Approximate Nearest-Neighbor Search," IACR ePrint 2024/1600 / ICLR 2025 — already read in full for the
  corpus's `interactive-private-search.md` entry, though not separately registered under its own KEY in
  this batch; the graph-traversal-based competing baseline Wally's Table 2 also re-benchmarks.)
- **Foundational** — cited as reference [38] and [50] in this paper's related-work discussion of PIR in
  the shuffle model, described as "closer to Wally" than classic multi-server PIR but relying on
  non-standard cryptographic assumptions and requiring many sub-queries per real query — bibliography
  detail not fully captured in this extraction pass; retrieve to confirm identity.
- **Foundational** — cited as reference [77], the "generic 2PC-based solution" the paper's own threat-model
  section argues its anonymization-service approach is more practical than — bibliography detail not
  fully captured in this extraction pass; retrieve to confirm identity.

### Verbatim extracts
- "We assume the server and anonymization service do not collude."
- "high throughput is a must, while low latency can be relaxed."
- "Wally achieves 7-29× higher QPS and 6.7-31× lower communication than Tiptoe, and 15,000× lower client
  storage than Pacmann."
- "hint-based protocols cannot directly handle database updates" — stated of Pacmann, as a contrast to
  Wally.
- "Epoch size ranges from 20 seconds to two minutes for varying values of Δ" (Table 2 caption) / "ranging
  from tens of seconds to a few minutes" (general statement) — both appear in the paper for related but
  not identical configurations.
