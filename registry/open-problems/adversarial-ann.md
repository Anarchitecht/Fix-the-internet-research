# Open problem: distributing an ANN index across untrusted participants while resisting inserted adversarial vectors

**Verdict: open.** No retrieved paper distributes a navigable-small-world graph or a quantized
inverted-file index across participants who are not under one operator's administrative control,
while measuring retrieval accuracy under adversarial vector insertion. The corpus and an
additional 2026 search turned up three separate literatures that each solve one piece of the
problem and explicitly decline the other two pieces.

## What was searched

Corpus entries opened in full: `ADAMS-ARXIV-25`, `ANDONI-ARXIV-26`, `MALKOV-TPAMI-20`,
`JEGOU-TPAMI-11`, `ZHONG-EMNLP-23`, `LI-SIGIR-25`, `ZOU-USENIX-25`, `XU-ARXIV-25`,
`GREGORIADIS-ARXIV-25`, `GOLD-ARXIV-23`. DBLP query `adversarially robust nearest neighbor`
returned exactly one hit, `ANDONI-ARXIV-26` itself, confirming the corpus already holds every
DBLP-indexed paper under that phrase. Further web searches: "distributed vector search index
untrusted peers Byzantine adversarial poisoning", "decentralized approximate nearest neighbor
search peer-to-peer survey 2025 2026", "vector database security survey SoK poisoning attack
2024 2025", "HNSW graph index poisoning malicious node insertion attack recall degradation",
"sharded vector index across untrusted nodes trust decentralized recall preserving", and
"corpus poisoning defense detection dense retrieval 2025 2026". These surfaced three further
2025-2026 distributed-vector-search performance papers (SPIRE, CoTra, BatANN, all Microsoft
Research or industry-affiliated, all evaluated on clusters of dozens of nodes under one
operator) and a 2026 survey of Retrieval-Augmented Generation (RAG, an architecture where a
language model's answer is conditioned on text retrieved by a similarity search over a corpus)
security, "Securing Retrieval-Augmented Generation: A Taxonomy of Attacks, Defenses, and Future
Directions" (arXiv:2604.08304, six-stage pipeline taxonomy, April-June 2026). None of these
seven papers combines untrusted-participant index distribution with measured adversarial-vector
resistance; each is discussed below at the point it bears on the verdict. The most recent
directly relevant publication found is `ANDONI-ARXIV-26`, dated January 2026.

## The two attack families the brief warns against merging

**Corpus poisoning** inserts crafted vectors into the searched collection so that a query
retrieves the attacker's vectors instead of, or ranked above, the genuinely relevant ones. The
attack succeeds or fails entirely inside the retrieval step; no downstream model is involved.
`ZHONG-EMNLP-23` and `LI-SIGIR-25` both measure this attack directly: inserting 50 crafted
passages into a Natural Questions corpus of millions of passages makes 99.4% of held-out test
queries retrieve at least one crafted passage in their top 20 results (`ZHONG-EMNLP-23`,
Contriever retriever). `LI-SIGIR-25` reaches a comparable 98.4% top-1 attack-success rate on
TREC DL 19 while producing crafted text with roughly 30-fold lower perplexity than the
`ZHONG-EMNLP-23` method, specifically to defeat perplexity-based detection.

**Generation-level corruption** goes one step further: it does not merely change what a search
returns, it changes what a language model concludes after reading what was returned.
`ZOU-USENIX-25` (PoisonedRAG) demonstrates this as a distinct mechanism, splitting each crafted
text into a retrieval-condition part and a separately engineered generation-condition part, and
reaches a 0.97 attack-success rate on Natural Questions for making GPT-4 state an
attacker-chosen wrong answer, using only 5 crafted texts against a corpus of 2,681,468 passages.
A text can satisfy the retrieval condition without satisfying the generation condition, or the
reverse; `ZOU-USENIX-25`'s own comparison table shows `ZHONG-EMNLP-23`'s corpus-poisoning attack,
applied unmodified to PoisonedRAG's task, reaches only a 0.01 attack-success rate on the
generation outcome despite a near-perfect retrieval F1-score of 0.99, because a passage
optimized to rank highly is not thereby optimized to make a language model state a specific
answer. This is the paper's own evidence that the two attack families are mechanically
independent, not two names for one thing.

Both families assume a corpus under one administrative party's control, with the attacker as an
outside contributor able to add documents. Neither considers a setting where the index
structure itself, not merely the document set, is jointly built and served by mutually
distrusting nodes.

## The distributed-index literature assumes a managed cluster

`ADAMS-ARXIV-25` (DistributedANN) is the only corpus entry that distributes a single
navigable-graph-style index (a DiskANN-derived graph, the mechanism family this problem
statement calls a "navigable small world" index) across more than a thousand machines while
measuring retrieval accuracy: 90.8% recall at 5 results returned, on a 50-billion-vector,
384-dimensional slice of the Bing web index, at over 100,000 queries per second. Its own
"Requirements" section states the threat model directly: "no participant identity is
authenticated as adversarial-resistant, no mechanism defends against a storage host returning
corrupted node data or false distance scores." The paper's near-data scoring service, the
component that computes each candidate's distance to the query, runs code the paper's operator
places on each storage host; the paper states this placement is a precondition the design
requires and that "a system without control over storage-host code placement (as in an
untrusted peer storage layer) could not deploy the near-data scoring service as described."
Every measured recall figure in the paper, including the reliability sweep down to 96% of
node-scoring hosts available, holds only because host failure is modeled as random unavailability,
not as a host returning a wrong answer on purpose. Two further 2025-2026 papers found by search,
SPIRE (arXiv:2512.17264, Microsoft Research and University of Science and Technology of China,
up to 8 billion vectors across 46 nodes) and CoTra (arXiv:2507.06653, RDMA-based), both target
the same single-operator cluster setting and do not evaluate any adversarial-host condition.
This is the assumption doing the work in every distributed-scale result the search turned up: a
decentralized deployment cannot supply operator-placed, trusted node-scoring code, so none of
these measured recall figures transfers to it.

`MALKOV-TPAMI-20` (HNSW), the base mechanism `ADAMS-ARXIV-25` builds on, states its own
distribution limit independent of any adversary: "total parallel throughput of the system does
not scale well with the number of computer nodes" once the graph is partitioned across machines,
because every search still funnels through one entry point's neighborhood at the top layer. The
paper describes this as an open problem in its own future-work section, not something the
73-citation literature since 2018 has closed for the untrusted case; the search above found no
paper claiming otherwise.

## The theoretical adversarial-robustness result targets a different adversary

`ANDONI-ARXIV-26` proves that specific constructions answer nearest-neighbor queries correctly
with high probability even when an adversary chooses the dataset and every subsequent query
adaptively. This is the only paper the search found, in the corpus or beyond it, proving a
formal adversarial-robustness bound for approximate nearest-neighbor search; it has no
implementation, no measured figure, and the authors state so directly: "a practical
implementation of our approach and the nuances it presents in a real system are also important
avenues to investigate."

Its threat model does not fit a decentralized index for two independent reasons, each
sufficient on its own. First, every one of the paper's three main constructions requires that
the algorithm's internal randomness, drawn once during preprocessing, stay hidden from the
adversary: "the adversary may know the code for A but not the specific instance of R_setup."
A distributed index built cooperatively by mutually distrusting nodes has no single party who
can hold that randomness privately, since the nodes doing the preprocessing are the same
population the randomness must be hidden from. Second, the paper's adversary supplies the
dataset once, before preprocessing, and afterward only queries; updates to the dataset are
"oblivious," meaning fixed in advance rather than chosen in response to the algorithm's answers,
and the paper states directly that it is "not concerned with robustness" against adaptively
chosen updates. A peer inserting a new adversarial vector after observing how prior insertions
were served is exactly the adaptive-update adversary the paper excludes.

## The one published decentralized retrieval system leaves this exact question as future work

`XU-ARXIV-25` (Distributed Retrieval-Augmented Generation, DRAG) is the corpus's only
peer-to-peer retrieval system evaluated with genuinely uncoordinated peers: each of up to 100
simulated peers holds its own local knowledge base and its own language model, and a query is
routed by a topic-weighted random walk (Topic-Aware Random Walk, TARW) rather than by a shared
index structure. This sidesteps the navigable-small-world and inverted-file mechanisms named in
the problem statement entirely — no peer ever writes into another peer's index, so there is no
shared graph or inverted list for an adversarial insertion to corrupt. What TARW cannot avoid is
trusting each queried peer's self-report: the paper states its design "assumes queried peers
answer truthfully about their own local knowledge-base content and relevance scores" and that
its own threat-model evaluation "addresses only traffic-observation deanonymization, not a peer
that misreports relevance to attract or divert queries." The paper lists peer rating of snippet
quality, consensus mechanisms for conflicting snippets, and reputation tracking as candidate
fixes, and states plainly that none of the three is implemented or evaluated.

`GOLD-ARXIV-23` (G-Rank) is adjacent evidence for what an unresisted version of this gap looks
like in a related, simpler mechanism: a gossip-based peer-to-peer ranking system with no
built-in Sybil resistance, tested with malicious peers at 10% and at a 75%-supermajority share
of a 100-peer network. Ranking quality measurably degrades under both attacks and never fully
recovers to the undegraded baseline by the end of the simulation at the 75% share, and the paper
states that whatever Sybil resistance limits how many malicious node identities a peer's local
view can absorb is a property "the surrounding system supplies," not one G-Rank supplies itself.
G-Rank ranks by click count over gossiped logs, not by vector similarity over an index, so it is
not a solution to this problem either — it demonstrates the same structural gap, an admission or
resistance mechanism assumed to exist "elsewhere," in a mechanism close enough in shape to make
the absence legible.

## What remains open

Nothing published measures retrieval accuracy for a navigable-small-world or quantized
inverted-file index whose structure — graph edges in the first case, inverted-list membership
and centroids in the second — is built and served by participants who can insert adversarial
content and are not subject to one operator's placement and screening of the scoring code. The
closest results bracket the problem from three directions without meeting in the middle:
`ADAMS-ARXIV-25` achieves distributed scale and measured recall by assuming the operator
controls every host; `ANDONI-ARXIV-26` achieves a proved robustness bound by assuming a
centralized preprocessing party whose randomness stays hidden and whose dataset is fixed before
any query is answered; and `XU-ARXIV-25` achieves genuine peer autonomy by giving up the shared
index structure and, with it, any mechanism to check what a peer reports. Every corpus-poisoning
defense measured in this corpus (embedding-norm clipping, perplexity filtering, duplicate-hash
filtering, retrieving more results to dilute the poisoned fraction, paraphrasing the incoming
query) is evaluated with a single trusted party applying the defense at ingestion or query time
over a corpus that party itself curates, and `ZOU-USENIX-25` reports that all four defenses it
tests still fail to fully stop the attack even in that single-operator setting — so the
centralized version of this problem is not fully closed either, before any decentralization
requirement is added.
