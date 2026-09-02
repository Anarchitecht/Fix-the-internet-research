## [HENZINGER-SOSP-23] Private Web Search with Tiptoe
**Citation:** Alexandra Henzinger, Emma Dauterman, Henry Corrigan-Gibbs, Nickolai Zeldovich. "Private Web Search with Tiptoe." ACM Symposium on Operating Systems Principles (SOSP), 2023.
**Retrieved:** full text via https://pdos.csail.mit.edu/papers/tiptoe:sosp23.pdf (the paper's own posted PDF, used after its DOI-listed ACM page proved closed-access; retrieved for the corpus's `interactive-private-search.md` open-problem entry)
**Source URL:** https://pdos.csail.mit.edu/papers/tiptoe:sosp23.pdf
**Domain:** G

### What it does
Tiptoe is a search engine that lets a client search hundreds of millions of documents while revealing no
information about the search query to the server, using cryptography alone — no anonymizing proxy (Tor,
a mix-net), no hardware enclave, and no assumption that a second server stays uncorrupted. The mechanism
reduces private full-text search to private nearest-neighbor search: every document is represented as a
semantic embedding, a fixed-length numeric vector produced by a machine-learning model such that
documents with related meaning produce vectors close together under inner-product distance; the query is
embedded into the same vector space, and the server must find the document vector maximizing inner-product
score against the query vector without learning the query vector itself. To keep this sublinear rather
than scanning every document per query, documents are grouped into roughly sqrt(N) clusters (N the corpus
size) at indexing time; at query time the client first uses a private-information-retrieval (PIR)
sub-protocol to learn, without revealing which cluster it is, which cluster centroid its query vector is
nearest to, then a second PIR-like round has the server compute inner-product scores under linearly
homomorphic encryption between the (still-encrypted) query and every document embedding in that one
cluster, returning an encrypted ranked list the client decrypts locally. Because the server only ever
computes on ciphertexts and the message flow and packet sizes are independent of the query string, the
protocol satisfies the paper's formal definition of query privacy — an adversarial search service, even
one that deviates arbitrarily from the protocol, cannot distinguish which of two query strings a client
sent, up to a standard cryptographic hardness assumption (learning with errors, LWE). A final stage uses
a separate PIR protocol against a URL-lookup service to let the client retrieve the human-readable URLs
for its top-ranked document IDs without revealing which documents it selected.

### Measured results
Measured on a 45-machine cluster of AWS `r5.xlarge` instances (the paper states the workload is
bottlenecked by memory bandwidth, not compute), over the C4 web crawl corpus of 364 million pages
(elsewhere in the paper stated as "over 360 million" and "360 million-document"), under a simulated
client network link of 100 Mbps and 50 ms round-trip time:

| Metric | Measured value | Conditions |
|---|---|---|
| End-to-end query latency | 2.7 seconds | Full pipeline: cluster identification, in-cluster ranking, URL fetch |
| Total server compute per query | 145 core-seconds | Same run |
| Total client-server communication per query | 56.9 MiB | 74% of this completes before the client enters its query (the cluster-identification PIR round, independent of query content) |
| Search-quality: average rank of the correct result | 7.7 out of 100 | MS MARCO benchmark; compared by the paper against a state-of-the-art non-private neural retriever (rank 2.3) and classical term-frequency-inverse-document-frequency (tf-idf) search (rank 6.7) |
| Corpus-update download cost | at most 18.7 MiB | Full refresh of all cluster centroids and metadata, compressed, for the 360-million-document corpus, even if every centroid changes |
| Cost comparison against prior state of the art | more than 1,000× lower AWS cost | Against Coeus, a tf-idf-based private Wikipedia search system, extrapolated by the paper's own authors to web scale for this comparison — not a head-to-head run of both systems on identical hardware |

The paper states plainly that its own design goal was to "keep the client-perceived latency on the order
of seconds" and to search hundreds of millions of documents "all in the span of seconds" — the 2.7-second
figure is reported by the paper as meeting, not exceeding, this stated target.

### Parameters
- Cluster count: chosen at roughly sqrt(N) for a corpus of N documents, to keep per-query PIR
  communication and the in-cluster homomorphic-scoring computation both sublinear in corpus size.
- Embedding model: the paper does not require any specific embedding model for query privacy — the paper
  states explicitly that Tiptoe "only relies on the embedding model for search result correctness — not
  privacy," so a weaker or biased embedding degrades relevance without weakening the privacy guarantee.
- Cryptographic hardness assumption: learning with errors (LWE), the same assumption underlying the
  linearly homomorphic encryption scheme used for in-cluster scoring and the PIR sub-protocols.
- Client network conditions used for the headline latency figure: 100 Mbps bandwidth, 50 ms round-trip
  time (simulated, not a measurement of any specific real client's connection).

### Stated limitations
The paper states its own formal query-privacy definition explicitly does not cover four things: Tiptoe
does not hide when a client makes a query, does not hide how many queries a client makes, does not
protect a client's post-search web-browsing behavior (a client's subsequent HTTP/HTTPS requests to a
returned URL can leak information about the query to a network observer), and — against a malicious
server — guarantees neither availability nor correctness of results, since a malicious server can serve
an arbitrary corpus or lie about document contents; the paper calls this last limitation "inherent." The
paper states embedding-based semantic search "brings with it many of the limitations of machine
learning: bias, lack of interpretability, and difficulty to generalize beyond the embedding's training
set," and its own MS MARCO evaluation shows the method "performs worst" on exact-string queries such as
phone numbers or addresses — the paper's own proposed fix, a separate private key-value backend for
exact-match queries via keyword PIR, is described only as future work, not built or measured in this
paper.

### Requirements it places on the rest of the system
The construction requires an embedding function computed once at indexing time over the entire corpus and
periodically re-run for corpus updates, and requires the resulting cluster assignments and centroids to
be published to every client — a design that assumes a component upstream of Tiptoe (a crawler or
document ingestion pipeline) supplies documents in a form the embedding model can process. The
in-cluster homomorphic scoring step requires every document within a cluster to be scored on every query
touching that cluster, so cluster size directly sets per-query server compute and communication; a
downstream system choosing cluster count trades index-refresh cost (more, smaller clusters mean more
frequent full-embedding passes over affected documents) against per-query cost (larger clusters mean
more homomorphic computation per query). The security definition (query privacy under an arbitrarily
malicious, but singular, server) requires no second, non-colluding party of any kind — a property the
paper's own multi-server-PIR baselines and its comparison target (Coeus) do not share — so composing
Tiptoe with an incentive or reputation layer that assumes multiple mutually distrusting servers already
enforce honest behavior would add a trust assumption Tiptoe itself does not need.

### Contradicts
None found against other corpus entries on a measured fact. This entry's figures match, and were the
source for, the figures already recorded under this KEY in the corpus's `interactive-private-search.md`
open-problem synthesis.

### References worth retrieving
- **Competing** — Alexandra Henzinger, Matthew M. Hong, Henry Corrigan-Gibbs, [et al.]. "One Server for
  the Price of Two." USENIX Security 2023. (Cited as reference [56]; source of the SimplePIR/DoublePIR
  single-server PIR schemes this paper's own record-fetch PIR sub-protocols build on — the
  interactive-private-search.md entry in this corpus already retrieves and reports its figures.)
- **Foundational** — Benny Chor, Eyal Kushilevitz, Oded Goldreich, Madhu Sudan. (Cited as reference [28];
  the original private-information-retrieval construction this paper's URL-fetch step uses.)
- **Foundational** — Henry Corrigan-Gibbs, Alexandra Henzinger, [et al.]. (Cited as reference [29]; a
  related PIR construction by an overlapping set of authors.)
- **Attack/critique** — cited as reference [76] in this paper, on the general limitations of embedding-
  based machine-learning search (bias, interpretability, generalization) — bibliography detail not fully
  captured in this extraction pass; retrieve to confirm identity.
- **Competing** — Sebastian Angel, Hao Chen, Kim Laine, Srinath Setty. (Cited as reference [8]; a private
  database-query system this paper's related-work section situates itself against.)

### Verbatim extracts
- "an attacker that controls all Tiptoe servers should be able to learn no information about the
  clients' search queries."
- "Tiptoe hides what a client is searching for; Tiptoe does not hide when a client makes a query, or how
  many queries the client makes."
- "In the face of malicious servers, Tiptoe guarantees neither the availability of its service nor the
  correctness of its results."
- "fetching this data ... requires at most 18.7 MiB of download for our 360 million-document text-search
  corpus."
- "Tiptoe only relies on the embedding model for search result correctness — not privacy."
