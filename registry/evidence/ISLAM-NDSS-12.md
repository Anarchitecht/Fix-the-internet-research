## [ISLAM-NDSS-12] Access Pattern disclosure on Searchable Encryption: Ramification, Attack and Mitigation
**Citation:** Mohammad Saiful Islam, Mehmet Kuzu, Murat Kantarcioglu. "Access Pattern disclosure on Searchable Encryption: Ramification, Attack and Mitigation." Network and Distributed System Security Symposium (NDSS), 2012.
**Retrieved:** full text via https://www.ndss-symposium.org/wp-content/uploads/2017/09/06_3.pdf
**Source URL:** https://www.ndss-symposium.org/wp-content/uploads/2017/09/06_3.pdf
**Domain:** G

### What it does
The attack recovers which keyword a query encrypts by observing only the pattern of which encrypted
documents a Searchable Symmetric Encryption (SSE) scheme returns for each query, without decrypting
anything. Searchable Symmetric Encryption lets a client store encrypted documents on a remote server and
later retrieve, by keyword, only the documents containing that keyword; every efficient scheme in the
paper's threat model reveals the access pattern — the set of encrypted document identifiers returned for
each query — even though it hides the plaintext keyword and plaintext documents. The attacker, named
Mallory in the paper, observes a sequence of queries and their returned document-identifier sets and
builds an m×m co-occurrence matrix M over the m possible keywords, where cell (i, j) holds the
probability both keyword i and keyword j appear together in a randomly sampled document; Mallory obtains
M either by statistical analysis of a large public document collection topically similar to the target
corpus, or, for an insider attacker, from a subset of the real corpus already in hand. Mallory formulates
keyword identification as an optimization problem matching each query's observed document-response
pattern against the co-occurrence matrix, and solves it approximately with Simulated Annealing, a
probabilistic search heuristic for large search spaces that accepts worsening moves with a
decreasing probability to escape local optima. The paper's mitigation adds fake positive matches (never
removes true ones, so no legitimate document is ever dropped from a result) to the encrypted index until
every keyword's response pattern is identical, within a bounded Hamming distance, to at least alpha − 1
other keywords' patterns, so an attacker who observes one response cannot narrow the querying keyword
below a 1-in-alpha guess.

### Measured results
All figures below are from a single implementation run against one dataset, described by the paper as
using a serial (non-parallel) implementation on an AMD Phenom II X6 1045T central processing unit (CPU)
at 2.70 GHz with 8 GB of system memory, Windows 7, with no single experiment run in this paper exceeding
14 hours.

Dataset: the Enron email corpus's "sent mail" folders across roughly 150 users, 30,109 documents, reduced
to 77,000 unique keywords after stemming (Porter Stemming Algorithm) and removal of the 200 most common
words. Queries are synthetic, drawn under a Zipfian distribution over the keyword set (the paper states
its attack does not use query frequency and is applicable under any query distribution), with query
repetition suppressed so no keyword is queried twice.

| Experiment | Fixed parameters | Varied parameter | Result |
|---|---|---|---|
| Accuracy vs. keyword-set size | 150 queries, 15% known-query rate | Keyword set size 500–2,500 (multiples of 500) | Near-100% at 500 keywords, decreasing but still identifying "most" queries at 2,500 keywords (exact curve values not stated numerically in text, only graphically) |
| Accuracy vs. query-set size | Keyword set size 1,500, 15% known-query rate | Query set size 50–250 (multiples of 50) | Accuracy rises as query-set size rises, from a lower baseline at 50 queries |
| Accuracy vs. known-query fraction | Keyword set 1,500, query set 150 | Known-query fraction 5%–25% | Little sensitivity — accuracy is "almost similar" across this range |
| Accuracy at very low known-query fraction | Keyword set 1,500, query set 150 | Known-query fraction 0%–6% | Roughly 80% accuracy even at 0% known queries (no known-plaintext queries at all) |
| Accuracy vs. noise scaling factor C (robustness to an inaccurate background matrix) | Keyword set 1,500, query set 150, 15% known | C from 0 to 1.0 | Accuracy remains high through low C and stays "a reasonable number" even at C = 1.0, the paper's maximum tested noise level |
| Aggregate headline figure | Large keyword and query sets (unspecified exact combination for this single summary number) | — | "over 80% queries for large datasets" correctly identified |

Mitigation cost (Section 13, Figure 5b): overhead is defined as the fractional increase in the number of
documents returned per query after adding fake matches (`cost = (q − p) / p`, where p is the original
document count returned and q the new count); overhead increases as the target separation parameter
alpha increases, no single overhead number given without alpha specified. Compared analytically (not
empirically re-implemented by this paper) to the Oblivious RAM (ORAM) construction of Williams, Sion, and
Carbunar (cited as reference [22]), which the paper states has computational overhead O(log n log log n)
per request including a constant factor the paper approximates at roughly 100: at n = 1,024 (2^10) data
items, that ORAM construction is estimated to require more than 1,000 data-item accesses per single data
access (100 × log2(1024) = 100 × 10), a cost that "grows much larger" as n increases, versus the paper's
own mitigation requiring 3 to 5 accesses per request, a number the paper states "does not change as n
increases."

### Parameters
- Keyword set size (m): tested 500 to 2,500 keywords, drawn as the most frequent x words from the
  corpus's 77,000 unique stemmed keywords.
- Query set size (l): tested 50 to 250 queries, generated without repetition under a Zipfian distribution.
- Known-query fraction (k/l, background knowledge of some true query-keyword pairs): tested 0% to 25%.
- Noise scaling factor C (how inaccurate the attacker's co-occurrence matrix M is allowed to be while
  still supporting the attack): tested 0 to 1.0.
- Mitigation target separation parameter alpha (minimum count of keywords sharing an identical, or
  within Hamming distance t, response pattern): swept in the cost-versus-alpha experiment (Fig. 5), no
  single fixed operating value stated as a recommended default.

### Stated limitations
The paper states its mitigation "does not guarantee the overall security of a searchable encryption
scheme" and explicitly names a residual exposure: an attacker using query frequency information or other
domain knowledge, a different attack model than the one this paper builds, could still extract sensitive
information even with the mitigation applied; a full security study of every such vulnerable aspect is
left as future work. The mitigation only ever adds fake positive matches, never removes true ones, and
the paper states this is a deliberate design choice — "even a very small false negative rate is
unacceptable" — because a client cannot detect a missing document but can trivially detect and discard an
added false positive after decryption. The paper explicitly contrasts its own mitigation against ORAM:
ORAM hides the access pattern completely, at higher, size-growing computational overhead, while the
paper's own scheme leaves the underlying access pattern partially structured (choosing this because
"efficiency is a major concern") and only bounds the maximum single-query keyword-identification
probability to 1/alpha, so it is explicitly offered as a lower-guarantee, lower-cost alternative to ORAM
rather than an equivalent replacement. The attack's own background-knowledge requirement (the co-
occurrence matrix M) is stated as obtainable from public data statistically similar to the target corpus
or from an insider's partial access to the real corpus; no experiment in the paper tests a co-occurrence
matrix built from a corpus topically dissimilar to Enron.

### Requirements it places on the rest of the system
The attack requires an eavesdropper (Mallory) with full access to the communication channel between
client and server, observing both the sequence of submitted (encrypted, indistinguishable) queries and
the sequence of returned document-identifier sets for each query — any Searchable Symmetric Encryption
deployment that hides which document identifiers were returned (not merely their contents) defeats this
specific attack construction, though the paper does not test or claim this for any real scheme. The
attack's accuracy depends on the attacker holding a keyword co-occurrence matrix approximating the target
corpus's true statistics; a search system whose corpus has no comparable public analogue and that
provides no other exploitable channel for an insider to sample the real corpus removes this input. The
paper's own mitigation requires the searchable index to be represented as a binary keyword-by-document
matrix that the server can modify by adding, but never removing, positive entries — any indexing scheme
that already returns document sets to the client with no server-side opportunity to inject extra
candidate matches (for example, one relying on client-side or oblivious index construction) cannot apply
this specific mitigation mechanism without modification.

### Contradicts
None found against other corpus entries. This paper's own headline aggregate ("over 80% queries for
large datasets") is a summary claim spanning the several parameter sweeps in the Measured Results table
above and is not a single controlled measurement at one fixed parameter combination — a reader citing
"80%+" without specifying keyword-set size, query-set size, and known-query fraction is citing an
imprecise compression of these results, not a distinct measured figure.

### References worth retrieving
- **Foundational** — Dawn Song, David Wagner, Adrian Perrig. "Practical techniques for searches on
  encrypted data." (Cited as reference [20]; an originating construction for the class of Searchable
  Symmetric Encryption schemes this paper's attack targets.)
- **Attack/competing baseline** — Peter Williams, Radu Sion, Bogdan Carbunar. "Building castles out of
  mud: practical access pattern privacy and correctness on untrusted storage." (Cited as reference [22];
  the Oblivious RAM construction the paper's mitigation is benchmarked against for overhead.)
- **Foundational** — Benny Pinkas, Tzachi Reinman. "Oblivious RAM revisited." IACR Cryptology ePrint
  Archive. (Cited as reference [18]; source of the O(log n log log n) Oblivious RAM overhead bound and
  its 1.44c constant-factor analysis used in the paper's comparison.)
- **Foundational** — Bryan Klimt, Yiming Yang. "Introducing the Enron Corpus." (Cited as reference [16];
  source of the dataset this paper's every measured figure depends on.)

### Verbatim extracts
- "Mallory has a very high probability of succeeding" given the two background-knowledge assumptions.
- "our attack scheme does not use query frequency."
- "the model can successfully identify nearly 80% of the queries correctly even if there are no known
  queries."
- "the required overhead is only 3-5 accesses per request and does not change as n increases."
- "it does not guarantee the overall security of a searchable encryption scheme."
