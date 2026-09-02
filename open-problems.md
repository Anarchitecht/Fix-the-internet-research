# Open problems

A problem appears here when a literature check found no published solution, or found one that reaches
the goal only under an assumption a decentralized deployment cannot supply. Each entry states what has
been tried, what the best published result achieves with its measured figures and conditions, the
assumption doing the work in that result, and where it falls short.

Each entry also records what was searched, because a problem recorded as open without that record is
a guess rather than a finding.

## Four of eleven are partly solved, and every one of the four buys the improvement with a party this architecture exists to remove

| Problem | Verdict |
|---|---|
| Ranked full-text search across peers at web scale | **partly** |
| Distributed approximate-nearest-neighbour search resisting inserted adversarial vectors | **open** |
| Forgery resistance without trusted seed identities | **open** |
| Private search at interactive latency | **partly** |
| Repair economics for volunteer erasure-coded storage under measured churn | **open** |
| Continuous participation from mobile devices | **open** |
| Removing illegal material from content-addressed storage | **open** |
| Verifiable bandwidth accounting | **partly** |
| Honest capacity reporting in a capacity-ordered overlay | **open** |
| Forward secrecy under long partitions | **open** |
| Secondary indexes and range queries over content-addressed stores | **partly** |

The four partial results are not partial in the same way, but they fail in the same place. Ranked
web-scale search drops below the standing bound only given a secure uniform peer-sampling substrate
and third-party content signing, neither of which the paper supplies. Private search reaches 2.7
seconds against one untrusted server, and every faster system adds a second non-colluding party or
relaxes cryptographic query-hiding to differential privacy over simultaneous queriers. Verifiable
bandwidth accounting works where a measuring party is trusted. Secondary indexing over
content-addressed data works where one party builds the index.

The distributed-vector-search entry states the same pattern most sharply: the result measured at
scale controls host placement and scoring code from one operator, and its own authors write that no
mechanism defends against a host returning false distance scores.

---

# Ranked full-text search across peers at web scale

## Verdict: partly

A published paper reports a lower per-query byte count than the standing bound, at a larger
document collection. It reaches that number by solving a different, restricted problem: bounded
probabilistic accuracy instead of exact retrieval, and an external random-peer-sampling and
content-signing dependency the architecture would still have to supply. No published paper
measures ranked full-text search bandwidth at web scale under adversarial peers, and no 2023-2026
paper — including the two found using learned dense or generative retrieval — reports a per-query
byte figure at anywhere near a billion-document collection.

## The standing bound, read from the primary source

Li, Loo, Hellerstein, Kaashoek, Karger, and Morris (IPTPS 2003, "On the Feasibility of
Peer-to-Peer Web Indexing and Search") pose a fixed budget of 1 megabyte of network traffic per
query, derived from a 1999 U.S. Internet backbone bisection-bandwidth figure, an assumed 10 percent
of that bandwidth allocated to web search, and 1,000 queries per second. Against that budget they
evaluate two peer-to-peer (P2P) search architectures. Partition-by-document gives each peer a
shard of documents and floods a query to every peer; at a 3-billion-document web index held across
60,000 peers at 1 gigabyte of storage each, flooding one 100-byte packet to every peer costs about
6 megabytes per query — 6 times the budget. Partition-by-keyword assigns each peer, through a
distributed hash table, the posting list for one or more words, and answers a multi-word query by
shipping the smaller posting list to the peer holding the larger one for intersection; scaled from
an 81,000-query trace against 1.7 million real web pages up to the assumed 3-billion-document web,
this averages about 530 megabytes per query, 530 times the budget, and a specific two-common-term
query ("the who") costs about 4 gigabytes.

The paper then applies a sequence of optimizations to partition-by-keyword, each measured on the
same 1.7-million-page trace: caching previously fetched posting lists reduces average cost by only
38 percent, because the paper states most queries in the trace occur only once; precomputing
intersections for the 7.5 million most popular term pairs reduces it by 50 percent; Bloom-filter-
based approximate set exchange reaches roughly 50 times compression in the best case; gap
compression of sorted document identifiers reaches 30 times; adaptive set intersection on top of
gap compression reaches 40 times; clustering documents by topic similarity so related documents
get numerically adjacent identifiers, combined with gap compression and adaptive intersection,
reaches 75 times. The 75-times figure is the paper's best combined result and leaves the average
query about 7 times over the 1-megabyte budget — the paper states this final gap is closed only by
two further compromises outside the optimization set: streaming partial, incrementally ranked
results instead of full posting-list intersection (which the paper shows brings the "the who"
query down to about 4 kilobytes, but works only with ranking functions compatible with incremental
sorted-list merging, explicitly excluding term-proximity ranking), or replicating the full index
once per Internet service provider to trade structural purity for aggregate bandwidth. The paper's
own conclusion is that naive partition-by-document and partition-by-keyword are both infeasible at
its stated budget, and that feasibility requires one of these two compromises on top of the 75-times
optimization stack. The paper evaluates no adversarial peers and no churn.

I found no distinct 2011 paper by Li's own group revisiting this bound. The paper matching the
"2011 follow-up" description in the assignment is Asthana, Fu, and Cox, "On the Feasibility of
Unstructured Peer-to-Peer Information Retrieval" (ICTIR 2011) — it cites Li et al. 2003 by name as
the paper it is positioned against, addresses the identical feasibility question, and is the entry
point of the probably-approximately-correct (PAC) search line the corpus already holds in depth
(2009-2014, University College London). The corpus's own evidence entry for this paper states
explicitly that its own headline numbers are not the 6-megabyte, 3-billion-document Li figure, so I
treat the two papers as separate, correctly attributed sources below rather than merging them.

## What overturns the raw byte figure, and what it assumes to do it

Asthana, Fu, and Cox replace posting-list intersection with a different mechanism entirely: every
peer holds a random subset of the full document collection with its own local index, a query is
broadcast to z peers sampled uniformly at random from the network, and each responds with its own
top-ranked local matches. Retrieval accuracy — the overlap between the top-k results this method
returns and what an exhaustive search over the whole collection would return, divided by k — follows
a closed-form probability P(d) = 1 − (1 − r/n)^z, where r is a document's replication count and n is
the network size. At n = 1,000,000 nodes and m = 10 billion documents — more than three times Li's
assumed web size — reaching 90 percent expected top-1 accuracy costs, depending on the replication
strategy and the fitted power-law query-popularity exponent, between about 1.0 and 3.6 megabytes per
query, below Li's 6-megabyte partition-by-document figure and two orders of magnitude below the
530-megabyte partition-by-keyword figure, at a larger document count.

This number is not a free improvement on Li's problem; it is the answer to a narrower one, and four
assumptions do the work.

First, the accuracy target itself is probabilistic, not exact: 90 percent expected overlap with an
exhaustive search's top-1 result, not guaranteed retrieval of every matching document. Li's
architecture targets deterministic completeness through posting-list intersection; trading
completeness for a bounded miss rate is what makes random sampling of a small peer subset a workable
substitute for querying (or precomputing an index over) every document-holding peer.

Second, query resolution depends on uniform-random sampling of z peers out of the full network on
every query, a primitive the paper assumes exists and does not itself supply or evaluate. The
corpus's Richardson and Cox follow-up (SIGIR 2014, "Estimating Global Statistics for Unstructured
P2P Search in the Presence of Adversarial Peers") extends this same PAC framework to compute the
collection-wide statistics (document frequency, average document length) that BM25 and
language-model ranking need, and finds that once those statistics are estimated from the sampled
peers' own responses, an adversarial minority can manipulate rank: at z = 2,000 peers queried and
just 10 percent of peers malicious, a censorship attack on one target document moves its rank from
5 to 582, and a promotion attack moves an unrelated document from rank 20,778 into the top 10. A
skewness-based filter (discarding the response contributing most to statistical skew before
computing the global estimate) holds these attacks off up to roughly 40 percent malicious peers, but
that defense itself sits on top of the random-sampling assumption from the first paper, and the
authors state directly that the actual deployed bound is set by whatever secure peer-sampling
service supplies that sampling — they cite Brahms, a Byzantine-resilient sampling protocol, whose
own published tolerance is 20 percent malicious peers, lower than the statistics defense's own
40 percent. The paper further assumes malicious peers cannot forge document content that scores well
under an honest ranker, attributing that assumption to content signing by a trusted third party that
neither paper supplies.

Third, the low bandwidth figure carries a cost the byte count does not show: it assumes each of 1,000,000
peers has already independently crawled and locally indexed its assigned 10 million documents (0.1
percent of the 10-billion-document collection). The paper's own estimate for that crawl, at 25
percent of a 2010-era average home connection continuously dedicated to it, is about 58 days per
full crawl cycle, plus 5 to 10 gigabytes of local disk. Li's partition-by-keyword architecture
carries no equivalent cost, because each peer there holds only posting lists for the keywords it is
responsible for, not a locally indexed copy of a document subset.

Fourth, every number in the 1.0-3.6-megabyte range is a closed-form analytical result over the
paper's own stated network, corpus, and hardware parameters, not a measurement from a running system
or a large-scale simulation. No implementation at 1,000,000 nodes or 10 billion documents is
reported anywhere in the paper.

## What has been validated at scale, and at what scale

Two entries in this same PAC line report results beyond closed-form arithmetic, at scales well
below the web-scale regime the bandwidth figures are computed for.

Mayor and Cox (IEEE P2P 2013) deployed the identical random-peer-query mechanism live on the actual
BitTorrent network — 5.4 million real nodes, 1.6 million real torrents, measured by scraping 13
public trackers over 64 days — but for a different task, finding which peers hold a given torrent's
tracking data, not ranked full-text keyword search. Even for that simpler task, the base PAC formula
needed a protocol addition (every peer that receives a query records the querying peer as an
indexer, and a torrent's publisher issues bootstrap queries at publication time) because 76 percent
of observed torrents were held by 10 or fewer nodes, too few for the base formula to give a workable
success probability.

Asthana's PhD thesis (University College London, 2014) simulated the ranked-keyword-search case
directly, at n = 100,000 nodes, not the 1,000,000-node/10-billion-document regime the bandwidth
figures use. Per-node sustained bandwidth in the churn-resilient configuration was 6.64 kilobytes
per second (about 17.2 gigabytes per month), which the thesis states directly is "currently not
viable for a mobile phone." Keyword-search accuracy computed from each peer's own local ranking
statistics reached only 84.97 percent at rank 10 (versus 95.46 percent for simple post retrieval
under the same configuration), recovering to 92.80 percent only once every peer was given the true
global ranking statistics — the same statistics whose adversarial manipulability Richardson and Cox
demonstrate separately. This thesis is a discrete-event simulation of the actual node logic, not a
live deployment, and its accuracy measurement itself depends on a centralized "gold standard"
database used only for evaluation, which the thesis states a real deployment has no equivalent of.

No experiment in this line — analytical, simulated, or deployed — combines web-scale document count
(billions), web-scale network size (millions of nodes), ranked retrieval, and an adversarial peer
population in the same result.

## Learned sparse and dense retrieval

I found no published paper, in the corpus or through DBLP, Semantic Scholar, and arXiv search, that
measures per-query network traffic for a decentralized deployment of a learned sparse (SPLADE-style)
or dense (embedding, approximate-nearest-neighbor, or generative-retrieval) ranker at anywhere near
web scale. Two 2025 preprints from the same research group put a learned model inside a decentralized
search system and were retrieved in full for this corpus. SwarmSearch (Gregoriadis et al., arXiv
2505.07452) has each peer run a locally fine-tuned T5-base generative-retrieval model that maps a
query directly to document identifiers, merges (docid, score) pairs across queried peers by
softmax-normalized summation, and reports top-1 accuracy as "nearly perfect" on a 100-document corpus
that visibly degrades once the corpus grows to 1,000 and 5,000 documents — five to six orders of
magnitude below the 3-to-10-billion-document scale Li's and Asthana's bandwidth figures are computed
for — and reports no byte-level communication figure anywhere in the retrieved text. Semantica
(Neague et al., arXiv 2502.10151) routes a query through a trie of peer clusters built from BERT
document embeddings and is evaluated on a 187,521-document dataset filtered to 6,978 users, also well
below web scale, and likewise reports hop counts and recall, not bytes transmitted. Neither paper's
own bibliography, nor the citation lists of the PAC-search line's core papers checked through
Semantic Scholar's API (Asthana ICTIR 2011: most recent citation 2019; Richardson SIGIR 2014: most
recent citation 2017; Li IPTPS 2003: most recent citations through 2026, none engaging the bandwidth
figure directly), turned up a paper that extends a learned-retrieval bandwidth measurement toward
billions of documents.

The one paper found that pairs a large language model with peer-to-peer query routing and reports a
message-count figure, Xu et al.'s "Distributed Retrieval-Augmented Generation" (arXiv 2505.00443,
in the corpus as XU-ARXIV-25), measures messages, not bytes, on a simulated Barabási-Albert network
of 20 to 100 peers answering from cached local-language-model knowledge bases, not ranked search
over a document collection — its reported 6.87-to-29.37-messages-per-query figures are not
denominated in the same unit as Li's or Asthana's results and are not comparable to either.

## The most recent systematic treatment found

Keizer, Ascigil, Król, Kutscher, and Pavlou's survey (ACM Computing Surveys 56(8), 2024, in the
corpus as KEIZER-CSUR-24) is the most recent systematic treatment retrieved, and is within the
2023-or-later window the assignment asks for. The survey states directly, as of 2024, that no
existing project achieves full decentralization across search, name resolution, and file storage
simultaneously, and that most decentralized search-engine research proposals it reviews address only
one search component — typically indexing or index storage — in isolation, without addressing
ranking or delivering a complete end-to-end system; it identifies this as an open issue rather than treating
it as solved by any system it surveys. Checking Semantic Scholar's citation index for this survey and
for Li's original paper through 2026 turned up no additional paper directly engaging the bandwidth
question; the only other 2023-2026 citer of Li's paper with an evaluated system, a 2026 Brazilian
regional-conference paper on Kademlia-plus-QUIC scientific-document storage, reports latency
reductions from a transport-protocol change, not a per-query bandwidth figure, and does not address
ranked keyword search.

## Structural consequence for a decentralized deployment

A deployment able to supply Asthana-Fu-Cox's assumptions — a secure random-peer-sampling substrate
tolerating whatever adversarial fraction it actually faces, a way to prevent forged document content
from scoring well under an honest ranker, sustained per-peer crawl-and-storage capacity for a random
document subset, and a target accuracy short of exact retrieval — has a published, though only
analytically demonstrated, path to a lower per-query byte count than Li's naive bound, at a larger
document collection. A deployment that instead needs exact retrieval, or that cannot bound the
fraction of colluding or malicious peers reaching the sampling and ranking-statistics layers below
today's roughly 20-to-40-percent published tolerances, remains where Li et al. left it: within about
an order of magnitude of a self-chosen 1-megabyte budget after the best published compression stack,
closeable only by giving up either deterministic ranking-function compatibility or single-overlay
structural purity. Nothing published measures whether a learned sparse or dense ranker changes this
picture at web scale in either direction.

## What was searched

Corpus: read the measurement index (`registry/index-measurements.md`) in full for entries matching
search, retrieval, P2P, PAC, posting list, and inverted index; opened in full the entries directly
bearing on the question — LI-IPTPS-03, ASTHANA-ICTIR-11, ASTHANA-PHD-14, RICHARDSON-SIGIR-14,
MAYOR-P2P-13, LOO-IPTPS-04, GREGORIADIS-ARXIV-25, NEAGUE-ARXIV-25, XU-ARXIV-25, and KEIZER-CSUR-24.

External: DBLP publication-search API (`dblp.org/search/publ/api`) for "peer-to-peer web search",
"decentralized search engine", "decentralized full-text search", and the exact title match for
Fantar and Youssef's "Peer-to-Peer Full-Text Keyword Search of the Web" (NETYS 2015, DHT-plus-Bloom-
filter design named BI-Chord; closed-access, full text not retrieved, so its figures are not usable
under this corpus's evidentiary rule and are not cited above). Semantic Scholar's paper-search and
citations API for Li's IPTPS 2003 paper (100 citing papers checked, all 2022-2026 entries read in
full for relevance — one 2024 survey (Keizer et al.), one 2026 Brazilian-conference paper on
DHT-plus-QUIC document storage, none else engaging the bandwidth question), for Asthana-Fu-Cox's
ICTIR 2011 paper (11 citing papers, most recent 2019), and for Richardson-and-Cox's SIGIR 2014 paper
(9 citing papers, most recent 2017). General web search for decentralized-search surveys and
Systematization-of-Knowledge papers from 2023 or later (none found dedicated to this problem beyond
Keizer et al.), for learned-sparse/dense-retrieval bandwidth in peer-to-peer settings (none found),
and for DatashareNetwork (Edalatnejad et al., USENIX Security 2020), a decentralized private-search
system that scales, by its own description, to thousands of users and millions of documents — three
to six orders of magnitude below the web-scale document counts this problem concerns, so treated as
out of scope rather than a candidate solution.

No paper was found, in the corpus or through this search, that measures ranked full-text search
bandwidth for a decentralized deployment at a billion-document scale under an adversarial peer
population, with or without a learned sparse or dense retrieval component.

---

# Open problem: distributing an ANN index across untrusted participants while resisting inserted adversarial vectors

## Verdict: open

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

---

# Forgery resistance without trusted seed identities

## Verdict: open

No published mechanism admits identities into a decentralized network and bounds the count an
adversary can forge, without relying on some party or population that the protocol itself must
trust in advance. Every mechanism retrieved for this pass substitutes one anchor for another —
a seed node, a seed committee, an issuer, a hardware manufacturer, or a platform's own ground
truth — and states that substitution as an explicit assumption, not as a solved elimination of
trust.

## Two analyses established the shared failure mode; a third confirms it by an independent route

Viswanath, Post, Gummadi, and Mislove (SIGCOMM 2010) took four published social-graph Sybil
defenses — SybilGuard, SybilLimit, SybilInfer, and SumUp — and showed each reduces to the same
operation: given one trusted node, rank every other node by proximity to it, then cut the ranking
at a threshold. The four schemes' rankings agree most strongly exactly where graph conductance
(the ratio of edges leaving a node set to edges inside it) has a local minimum — the boundary of a
locally dense cluster around the trusted node. Substituting an off-the-shelf local
community-detection algorithm for any of the four schemes' own procedures produces comparable
accuracy, which is how the reduction was demonstrated. Across eight real social graphs (514 to
446,181 nodes), detection accuracy correlates with network modularity at −0.81: the more the
honest population itself splits into distinct communities, the worse every scheme performs. On the
Facebook graduate-student graph (514 nodes), an adversary who places attack edges only among the k
nodes nearest the trusted node — rather than uniformly at random — drives detection accuracy below
0.5 as k shrinks toward zero, meaning Sybil nodes rank above honest ones. The paper states as an
open question whether the assumption every scheme needs, that Sybils can form only a bounded
number of edges into the honest region, holds in any real online social network today.

Alvisi, Clement, Epasto, Lattanzi, and Panconesi (IEEE Security and Privacy 2013) reduced
universal Sybil defense to a random-walk membership test relative to one seed, then reframed the
achievable goal from classifying every node in the network to finding one seed's local, sparsely
cut community (their Problem 1), solved by a Personalized PageRank algorithm called ACL. Under an
attack pattern observed on the Renren social network — many isolated Sybil nodes, each with a few
attack edges, rather than one dense Sybil cluster — every tested scheme performs close to random
guessing on the Facebook-New Orleans graph: SybilLimit 0.45, SybilGuard 0.44, community detection
0.34, GateKeeper 0.49, ACL 0.37, where 0.5 is the random-guessing point. The paper states plainly
that community-detection-based Sybil defense is often described as solved and that this is false
in general: an adversary using only two attack edges from one honest node to two Sybil endpoints
can force the community-detection algorithm to admit an entire attacker-built Sybil chain.

Furutani, Shibahara, Akiyama, and Aida (IEEE Transactions on Information Forensics and Security
2023) reached the same conclusion by a third, independent route: they showed five propagation-based
detectors (CIA, SybilRank, SybilWalk, SybilSCAR, SybilBelief) are each one instance of graph-signal
low-pass filtering, and that every one of them collapses once community strength falls below a
theoretical detectability threshold, regardless of which filter or which graph shift matrix is
used. The mathematical form differs from the first two analyses; the conclusion — detection
accuracy is governed by how strongly the honest and Sybil regions separate into communities, and
collapses when they do not — is the same one three independent groups reached from three different
directions.

## A measurement on a 21-million-node network shows the assumption already fails at scale

Gao, Wang, Gong, Kulkarni, Thomas, and Mittal (IEEE CNS 2018, the SybilFuse paper) measured network
modularity directly on a labeled Twitter follower graph of 21,297,772 nodes and 265,025,545 edges,
with ground truth obtained by re-crawling every account through Twitter's own suspension API. The
modularity of the benign/Sybil partition is 0.0042, and rises only to 0.0046 when restricted to the
Sybil region's largest connected component — far below the 0.3 threshold the paper cites as the
point above which a partition counts as a detectable community structure at all. Under this
measured condition, every structure-only baseline the paper tests performs near-random to modest:
SybilRank reaches Area Under the Curve (AUC, the probability a randomly chosen Sybil node ranks
above a randomly chosen benign node) 0.57, Integro 0.48 to 0.54, SybilBelief 0.74, SybilSCAR 0.74.
The paper's own hybrid method, SybilFuse, reaches AUC 0.85 by adding a locally trained classifier
signal on top of structure — but that classifier is itself trained on 3,000 labeled benign and
3,000 labeled Sybil nodes drawn from Twitter's own centralized suspension decisions, a ground-truth
source the paper states its own method sits on top of, not one it replaces. A manual audit of the
100 top-ranked accounts still active after Twitter's own moderation found 82.8% of the 29 still-active
accounts show Sybil-like characteristics anyway, meaning the platform-supplied ground truth this
detector depends on is itself imperfect.

Mohaisen, Yun, and Kim (ACM IMC 2010) independently measured why: the fast-mixing property every
random-walk-based scheme in this family assumes — that a random walk from any node reaches the
graph's overall distribution within O(log n) steps — does not hold at the walk lengths those
schemes' own evaluations used. Real graphs need walk lengths of 100 to 2,500 steps to reach a
total-variation distance of 0.1 from the stationary distribution, one to two orders of magnitude
larger than the 10-to-15-step walks SybilGuard and SybilLimit's own published evaluations used.
Forcing a graph to mix faster by removing low-degree nodes, the trimming step those evaluations
also used, removed over 85% of the WikiTalk graph's nodes before the assumption held.

## What has been published since 2023, and what each result assumes

**Graph neural network detectors.** Heeb, Plesner, and Wattenhofer (arXiv 2024, SybilGAT) replace
the fixed propagation weights of SybilRank, SybilBelief, and SybilSCAR with a Graph Attention
Network, a graph neural network layer that learns a separate weight per neighbor rather than one
global weight per edge. On a real 269,640-node Twitter graph, the four-layer variant reaches AUC
0.8489 against SybilSCAR's 0.8022. Under a targeted attack-edge placement — the same class of
attack Viswanath et al. and Alvisi et al. showed degrades every prior scheme — performance on a
pre-trained, larger evaluation graph falls to AUC 0.6021, barely above the 0.5 random-guessing
point, and the paper's own robustness sweep shows the gap over baselines widening only because the
baselines degrade faster, not because SybilGAT stays accurate. The mechanism requires a small,
already-labeled set of honest and Sybil nodes before training or inference proceeds (5% of each
region's true size by default); SybilGAT does not determine which nodes to trust as ground truth,
it consumes a trusted label set exactly as the schemes it replaces do. The authors state that
robustness against an attack targeting the attention mechanism specifically "remains to be fully
explored."

**Resource-based admission.** Gupta, Saia, and Young's resource-burning framework (SIROCCO 2020,
surveying their own prior algorithms including ERGO) bounds the fraction of Sybil identifiers at
any time to a constant α, given that the adversary's resource-spending rate stays within a bound
relative to the rate at which honest identifiers join. This substitutes a resource-parity
assumption — the honest population's aggregate spending capacity must not be swamped by the
adversary's — for a graph-connectivity assumption; it removes the social graph, but not the
requirement that some population supply a bounded, sustained resource commitment the adversary
cannot outmatch by spending more. For the specific case that matters to a decentralized network —
extending the bound to a Distributed Hash Table under permissionless churn — the paper's own
Section 4.2 states this requires a committee, "a small identifier set with a good majority," to
issue and validate the resource-burning challenges, and states outright that decentralizing that
committee is itself unresolved (their Open Problem 3). Resource burning does not eliminate the
pre-trusted anchor for this case; it relocates the anchor from a seed node in a social graph to a
seed committee coordinating admission, and the paper states that relocation as an open problem, not
a solved one.

**Proof-of-personhood constructions.** Every reviewed or retrieved construction requires an anchor
outside the protocol.

- Borge, Kokoris-Kogias, Jovanovic, Gasser, Gailly, and Ford (IEEE EuroS&PW 2017) build
  proof-of-personhood on in-person pseudonym parties under an anytrust assumption: at least one
  organizer, and at least one of that organizer's independent servers, must be honest and
  non-colluding. The paper runs no experiment; it states that preventing one person from attending
  two simultaneous parties in different regions relies on travel-time infeasibility, not on a
  cryptographic guarantee.
- Siddarth, Ivliev, Siri, and Berman (Frontiers in Blockchain 2020) reviewed seven deployed
  proof-of-personhood systems. Four of seven anchor Sybil resistance to a social graph seeded from
  trusted starting points (BrightID) or to vouching networks with a stated minimum connection
  density (Duniter, Kleros/Proof of Humanity, Humanity DAO). The paper states there is "no
  evidence of the Web of Trust schemes' effectiveness for Sybil-resistance in the presence of
  multiple attack vectors" for any of the four. It states a reverse-Turing-test approach (Idena's
  FLIP test) stops automated bots but not "human-generated attacks, in which one individual passes
  the test multiple times and creates multiple different identities" — an unresolved gap, because
  nothing in the mechanism stops a market for completing the test on another person's behalf.
- The BrightID whitepaper (2020) anchors its own Sybil-ranking algorithm to seed groups from the
  start, and states as an open question, unresolved in the document itself, who holds the
  authority to grant seed status to the first seed group with no existing parent group.
- Crites, Kiayias, Kohlweiss, and Sarencheh (ACM CCS 2025, SyRA) remove the requirement that an
  issuer retain a per-user record after issuing a credential, using a distributed verifiable random
  function so the issued key is a deterministic function of the identity string and never needs to
  be looked up again. The construction still requires an external personhood-verification input —
  a signed government certificate, a biometric reading, or an OAuth token, none of which the paper
  builds — and requires a threshold t of n issuers to act honestly (t = n/2 in the paper's own
  evaluated configurations, measured at 0.0651 to 72.6 seconds of issuance time across six
  committee sizes from 10 to 300 issuers on one MacBook Pro). The paper states explicitly that
  privacy and Sybil resistance both fail once fewer than t issuers are honest, and does not
  evaluate the personhood-check step itself.
- Ľaš, Homoliak, and Mariani (IACR ePrint 2026/1723, De-SyRIS) combine facial-biometric matching
  inside a Trusted Execution Environment (TEE, a hardware-isolated processor region meant to keep
  code and data confidential from the machine's own operating system) with zero-knowledge
  social-graph path proofs, to avoid publishing the graph itself. The paper's own discussion states
  TEE security "remains an open question" in decentralized settings and cites a 2025 hardware
  attack (Seto et al., ACM CCS 2025) that discontinued a comparable TEE-based identity project. The
  paper labels its biometric-embedding database "a centralized but encrypted repository." Its own
  100-entity simulation states that the Holme-Kim graph model needs 8% to 30% of entities holding
  externally supplied reputation, depending on trust-distribution mode, before the protocol's
  intrinsic reputation mechanism can bootstrap at all — the system cannot start from zero
  externally supplied trust. The paper states outright, as an unresolved weakness rather than a
  theoretical one, that a coalition using real, highly reputable identities as gateways can
  legitimize a large Sybil cluster, with no defense against it inside the current design.
- Vozda et al. (IACR ePrint 2026/1725, Proof-of-Uniqueness) compose an issuer-signed verifiable
  credential with a threshold verifiable oblivious pseudorandom function evaluated by n nodes with
  reconstruction threshold t, so that no single node holds the deduplication key. The paper's own
  stated assumptions are that fewer than t OPRF (Oblivious Pseudorandom Function) nodes collude and
  that canonical issuance is honest; it states directly that privacy fails against "an issuer that
  actively probes its own identifiers," and that person-level deduplication holds only under the
  assumption of honest canonical issuance by that same issuer. The construction distributes trust
  across a committee; it does not remove the requirement that an issuer and a threshold of that
  committee be trustworthy.

**A structurally identical pattern outside social graphs and biometrics.** Shi and Joo (arXiv,
October 2025) built TraceRank, a reputation-ranking algorithm for a payment-gated service
marketplace, where each payment functions as an endorsement and reputation propagates along
payment flows weighted by transaction value and time. The paper states plainly that TraceRank
"seeds addresses with precomputed reputation metrics" before propagation begins, and states
TraceRank "is agnostic to seed provenance" — the seed-selection problem is left to whatever
upstream source supplies it (trading history, a social-graph platform, labeled organizations, or
an external attestation registry), not solved by the mechanism itself. Substituting a payment
graph for a social graph reproduces the identical structure Viswanath et al. and Alvisi et al.
analyzed: a ranking computed relative to a pre-supplied trusted set, with the trust-origination
problem left outside the paper.

## The pattern across every mechanism family

Six different substrates were checked against the same question — what must already be trusted
before the mechanism runs — and every one names something.

| Mechanism family | What replaces the social-graph seed | Paper's own statement of the residual trust requirement |
|---|---|---|
| Classical social-graph ranking (SybilRank, SybilLimit, ACL) | A trusted seed node or seed set | Ranking is seed-relative; accuracy depends on the seed's placement and the honest region's community structure |
| Graph neural network detection (SybilGAT) | A labeled training set of honest and Sybil nodes | 5% of each region must already be correctly labeled before training or inference runs |
| Resource burning (DefID/ERGO family) | A resource-parity bound on the adversary, and for decentralized deployment, a coordinating committee | Decentralizing that committee is stated as an open problem, not solved |
| Pseudonym parties | At least one honest, non-colluding organizer and server | The anytrust assumption is a stated precondition the protocol does not itself enforce |
| Web-of-trust proof of personhood | A seed group or a minimum-density vouching network | No reviewed system is stated to have proven effectiveness against multiple attack vectors |
| Threshold-issuer cryptographic constructions (SyRA, Proof-of-Uniqueness) | A threshold of honest issuers or committee members, plus an external personhood check | Both privacy and Sybil resistance are stated to fail once the honest threshold is not met |
| Payment-graph reputation (TraceRank) | Seed reputation scores from an external source | The paper states it is agnostic to where those scores come from |

## Where the state of the art stops

The best published result for the specific claim — bound the count of forged identities an
adversary can register, without any party the protocol itself must trust in advance — is that no
such result exists. The strongest results move the bound within one substrate (SybilFuse's local
classifier lifts AUC from 0.57–0.74 to 0.85 on the 21-million-node graph; SybilGAT lifts AUC by up
to five points over SybilSCAR on the 269,640-node Twitter graph) while keeping the same
pre-trusted-anchor requirement every earlier scheme in that substrate needed. The threshold-issuer
constructions (SyRA, Proof-of-Uniqueness) are a genuine advance on a narrower, different claim:
they let issuers stop retaining state after issuance, closing a specific storage and
correlation risk, while both papers state directly that the underlying trust requirement — a
threshold of honest issuers, plus an external personhood check neither paper builds — is
unchanged. Resource burning is a genuine advance on a different axis still: it removes the social
graph entirely, at the cost of a resource-parity assumption on the adversary and, for a
decentralized deployment, an unresolved committee-decentralization problem the paper's own authors
list as open.

## Assumption doing the work

Every mechanism in this pass supplies its stated guarantee only because some population or party
is already assumed honest before the protocol runs: a seed node's placement, a labeled training
set, a resource-spending population the adversary cannot outmatch, an anytrust organizer, a
vouching network's density, a threshold of issuers, or an externally supplied reputation score. A
decentralized deployment, by definition, has no operator positioned to guarantee any of these in
advance — no party is in a position to hand-pick a seed node, manually label a training set, or
convene an issuer committee and vouch for its honesty. Every mechanism surveyed here answers a
different question than the one this architecture needs answered: not "how do we bound forgery
given a trusted anchor" but "how do we bound forgery with no trusted anchor to give." The former is
solved, repeatedly, in different ways. The latter has no published answer.

## What was searched

Corpus: `registry/index-measurements.md` and `registry/index-requirements.md` were read in full and
grepped for `sybil`, `forgery`, `seed`, `community detection`, `social graph`, `proof of
personhood`, `admission`, `graph neural`, `GNN`, and the individual scheme names (SybilGuard,
SybilLimit, SybilRank, SybilInfer, Whanau, Bazaar, Canal). Every matching evidence file was opened
in full: `ALVISI-SP-13`, `VISWANATH-SIGCOMM-10`, `MOHAISEN-IMC-10`, `GAO-CNS-18`, `FURUTANI-TIFS-23`,
`HEEB-ARXIV-24`, `CRITES-CCS-25`, `LAS-EPRINT-26`, `FORD-EUROSPW-17`, `SIDDARTH-FRONTIERS-20`,
`BRIGHTID-WP`, `CAO-NSDI-12`, `GUPTA-SIROCCO-20`, `SAFARPOOR-DEHKORDI-ARXIV-25`, and
`SAFARPOOR-DEHKORDI-AAMAS-25`.

Beyond the corpus: DBLP's publication-search API for `sybil detection without seed` and `sybil
resistance trusted seed` returned zero hits. Web searches covered `sybil defense without
pre-trusted seed set 2025`, `proof of personhood survey 2025 systematization of knowledge`,
`Worldcoin World ID sybil resistance attack analysis 2024 2025`, `Bankrupting Sybil churn
resource-based admission`, `graph neural network sybil detection without labeled seeds
unsupervised 2024 2025`, `arxiv 2025 2026 sybil resistance decentralized identity no trusted issuer
seedless`, and `sybil resistance decentralized 2026 no pre-trusted seed set survey`. Two candidates
that looked like they might solve the problem — `Proof-of-Uniqueness: Sybil-Resistant
Privacy-Preserving Decentralized Identity through Threshold-OPRF and zk-SNARK Registry` (IACR
ePrint 2026/1725, Vozda et al.) and `Sybil-Resistant Service Discovery for Agent Economies` (Shi
and Joo, arXiv 2510.27554, October 2025) — were retrieved in full text with
`tools/fetch-paper.py` (47,139 and 10,737 characters respectively) rather than judged from their
abstracts; both state the residual trust requirement directly in their own text, quoted above. The
most recent directly relevant full-text retrieval is Ľaš, Homoliak, and Mariani's De-SyRIS, IACR
ePrint 2026/1723. A third 2026 candidate, `Human Challenge Oracle: Designing AI-Resistant,
Identity-Bound, Time-Limited Tasks for Sybil-Resistant Consensus` (arXiv 2601.03923), was found but
only its abstract was reachable in this pass; it addresses a different problem (rate-limiting how
many identities one already-admitted party can sustain over time) rather than bounding forgery at
admission, and is recorded here as unretrieved — no measurement from it is used above.

---

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

---

# Open problem: repair economics for volunteer erasure-coded storage under measured churn

## Verdict: open

**Verdict: open.** No retrieved paper measures the repair traffic a regenerating code consumes
when deployed on a population of independently operated, high-turnover storage participants. The
corpus contains a real feasibility disagreement between two papers that model different churn
regimes, a regenerating-code simulation whose own highest-churn trace erases most of the
mechanism's advantage, and — from an additional 2026 search — a live measurement of churn on a
deployed decentralized storage network that does not use regenerating codes and does not publish
repair-traffic bytes, plus a live repair-traffic measurement from a deployed network that does not
use regenerating codes and does not run on volunteer-scale churn. The two literatures never meet
inside one measurement.

## What was searched

Corpus entries opened in full: `BLAKE-HOTOS-03`, `CHUN-NSDI-06`, `BHAGWAN-NSDI-04`,
`DIMAKIS-TIT-10`, `RASHMI-TIT-11`, `VAJHA-FAST-18`, `WILKINSON-STORJ-18`, `VORICK-SIA-14`,
`DANEZIS-WALRUS-25`, `HUANG-ATC-12`, `SATHIAMOORTHY-VLDB-13`, `ANDERSON-CCGRID-06`,
`BENET-FILECOIN-17`, `PAPAILIOPOULOS-TIT-14`, `PATRA-TIT-25`, `MATURANA-TIT-22`,
`MATURANA-ISIT-23`. DBLP queries `regenerating codes repair bandwidth churn`,
`peer-to-peer storage churn repair`, and `volunteer storage erasure coding` returned zero hits
each (the service also returned intermittent 503s during this pass; queries were re-run after a
delay and confirmed empty, not blocked). Web searches run: "regenerating codes repair bandwidth
measured churn peer-to-peer storage volunteer 2024 2025", "'repair traffic' decentralized storage
network measured deployment Filecoin Storj Sia real operation 2024 2025", "'erasure coding'
survey 2024 2025 'systematization of knowledge' distributed storage repair", "Filecoin storage
network measurement study sector churn 2023 2024 2025 empirical", "'Storj' OR 'Sia' network
measurement study node churn repair empirical academic paper", and "arxiv 2025 regenerating codes
storage node departure rate real trace measurement repair volunteer". These surfaced three papers
not previously in the corpus, retrieved in full text below. No paper found in any of these
searches reports a measured, in-bytes repair-traffic figure for a regenerating-coded object under
continuous volunteer-scale churn. The most recent directly relevant publication found is
`DANEZIS-WALRUS-25` (arXiv v4, 10 Aug 2026), which reports live repair-traffic figures from a
deployed network — but for a two-dimensional Reed-Solomon mechanism, not a regenerating code, and
from a staked, well-provisioned node committee, not a volunteer population.

## The two feasibility papers, and which churn regime does the work

`BLAKE-HOTOS-03` derives a bandwidth lower bound for maintaining redundancy against membership
turnover and applies it to an original crawl of roughly 33,000 Gnutella hosts (April 2003). Under
that trace's churn — mean host availability 0.38, 30% of hosts permanently failing per day at a
1-day timeout — the paper states storing 1 TB of unique data at high availability is "hopeless"
with Gnutella-like participation and cable-modem bandwidth. Restricting to the most-available 5%
of hosts (a 10-fold cut in aggregate service time) brings required bandwidth down roughly
1,000-fold from the paper's worst-case point, which the paper itself frames as converting the
problem into "a garden variety distributed systems problem" of building storage from a smaller
set of reliable collaborators — not a property that comes free to a design that keeps admitting
arbitrary volunteers.

`CHUN-NSDI-06` (Carbonite) measures live PlanetLab data — 632 hosts, 21,255 transient failures,
219 disk failures over one year — and reports Carbonite uses only 44% more network traffic than
an oracle that repairs solely on true disk failure, versus a near-2x oracle overhead for
Total-Recall- and DHash-style designs on the same trace. The paper states explicitly that it
reaches a different conclusion from `BLAKE-HOTOS-03` because it analyzes "a relatively stable
system membership where data loss is driven by disk failure" rather than continual membership
turnover — a difference in modeled scenario, not a numeric disagreement over the same population.
PlanetLab is a research testbed of institutionally hosted machines with implicit uptime
commitments; its measured mean time between disk failures (2.23 years per disk) and its derived
sustainability ratio θ = repair-rate / failure-rate ≈ 6.85 both describe a population far more
stable than Gnutella's, SETI@home's, or any population recruited from arbitrary home
participants. Neither paper is about regenerating codes; both are about the replication- and
classic-erasure-coding maintenance-bandwidth question the regenerating-code literature later
built on.

## What the regenerating-code paper itself shows on the highest-churn trace

`DIMAKIS-TIT-10` defines the regenerating-code construction and evaluates its bandwidth
advantage over a Hybrid (one full replica plus an erasure code) design by simulation, using the
availability/bandwidth model of Rodrigues and Liskov (2005) applied to four real availability
traces: PlanetLab (527 days, a = 0.97, f = 0.017/day), Microsoft desktop PCs (35 days, a = 0.91),
Skype superpeers (25 days, a = 0.65), and Gnutella (2.5 days, a = 0.38, f = 0.30/day — the same
population character as `BLAKE-HOTOS-03`'s trace). On PlanetLab, regenerating codes reach 100x
lower unavailability at roughly 58x less bandwidth than Hybrid for a 1 GB file. On Gnutella, the
paper states plainly: "RC can be very slightly worse than Hybrid" — the mechanism's advantage,
measured by the paper's own simulation on its own least-stable trace, is gone. This is not a
field measurement of repair bytes moved; it is a simulation using the same analytic
availability/bandwidth cost model `BLAKE-HOTOS-03` and `CHUN-NSDI-06` build on, applied to traces
collected between 1999 and 2005. No retrieved source re-runs this comparison against a churn
trace collected after 2005, and none instruments an actual regenerating-code implementation to
report bytes transferred.

## Deployed systems: churn is measured, or repair traffic is measured, never both together

`WILKINSON-STORJ-18`'s only repair-bandwidth figures (Table 7.2, reproduced in the evidence file)
come from a 10,000-node, 1,000-run, 24-month Monte Carlo simulation under an assumed constant
monthly piece-loss rate, not from operation of the live network. `VORICK-SIA-14` gives no
measurement at all — it is a design whitepaper recommending regenerating codes for multi-host
placement without reporting any run of the mechanism. `VAJHA-FAST-18` measures real repair
network traffic for an MSR (minimum-storage-regenerating) code family, Clay codes, but on a
26-node Amazon EC2 Ceph cluster with node failures injected by the experimenters, not on a
population under real churn, and the deployment context is a managed cluster (the paper's own
motivating figure is Facebook's warehouse cluster moving a median of 0.2 petabytes/day in
repair), not independently operated volunteer nodes.

Two papers retrieved in this pass close part of the gap from opposite sides, and neither closes
it fully.

`LI-IWQOS-23-STORJ` ("An Empirical Study of Storj DCS: Ecosystem, Performance, and Security," Hao
Li, Xianghang Mi, Yanzhi Dou, Shanqing Guo, IEEE/ACM IWQoS 2023) crawls the live Storj network —
32,881 unique storage nodes observed, roughly 13,000 daily active — and measures real
month-by-month churn between May 2021 and August 2022: a range of 4.55% to 15.28%, averaging
9.6% per month, with only 44% of nodes present in April 2021 still active by August 2022. This is
a measured churn rate from an actual population of independently operated, incentive-compensated
storage nodes — a closer match to "volunteer" than PlanetLab or a managed cluster. But Storj does
not use a regenerating code: it repairs by downloading k of n Reed-Solomon shares to fully
reconstruct a segment and re-uploading replacement shares (the mechanism `WILKINSON-STORJ-18`
describes and `DANEZIS-WALRUS-25` cites Storj's own documentation for, at a 29-of-80 configuration
and a stated "key limitation" — inability to efficiently heal lost parts without full
reconstruction). The paper reports no repair-traffic byte count, measured or estimated, at all.

`DANEZIS-WALRUS-25` (Walrus, arXiv:2505.05370, CCS '26) is the one source in this pass reporting
repair-traffic bytes from a live network rather than simulation: at epoch 9, one joining node
received 636 GB of blob metadata plus 890 GB of slivers (79.5 million slivers) over roughly 15
hours; at epoch 20, recovering 7 shards after a node went offline moved data for roughly 3.6
million blobs and took up to 64 hours, with one shard requiring 16 hours and another interrupted
and resumed only after its holding node returned online. These are real operational costs, not
simulated ones. But the mechanism is RedStuff, a two-dimensional Reed-Solomon code achieving
O(|blob|/n) recovery through a different structural route than the Dimakis/Rashmi
regenerating-code family (helper nodes supply row/column symbols verified against a vector
commitment, not linear combinations at the minimum-bandwidth or minimum-storage operating point),
and the paper does not cite the regenerating-code literature as what it implements. More
importantly for this problem, Walrus's roughly 100-node committee runs on staked, well-provisioned
hardware (the paper's own operator survey: median node capacity in the tens of terabytes,
predominantly ≥16 CPU cores, 128 GB RAM, 1 Gbps bandwidth) with epoch-scheduled, committee-governed
membership changes — not the continuous, uncoordinated churn of an open volunteer population.
Whether Walrus's measured recovery durations (tens of hours per multi-shard event) would hold, or
degrade, under Storj-like 9.6%-per-month uncoordinated churn is not addressed by either paper.

## The most recent systematization of knowledge does not update this

`CHENG-TOS25-ECSURVEY` ("A Survey of the Past, Present, and Future of Erasure Coding for Storage
Systems," Shen, Cai, Cheng, Lee, Li, Hu, Shu, ACM Transactions on Storage, Vol. 20 No. 4,
December 2024 / January 2025) is the field's current systematization of knowledge on erasure
coding and repair. It cites peer-to-peer, churn-driven repair exactly twice, both in passing: once
crediting `RODRIGUES-IPTPS-05` (2005) as the source of "lazy recovery" in peer-to-peer networks,
and once citing the same paper's finding that erasure coding's benefit over replication "may be
limited and even negated by the complexity of deploying erasure coding" in peer-to-peer DHTs. The
survey's entire repair-optimization discussion — proactive repair, concurrent repair, repair
parallelization, reliability modeling — is drawn from data-center deployments (Facebook, Azure,
Backblaze, Ceph, HDFS). No volunteer-churn or decentralized-network repair measurement from 2006
onward appears anywhere in a 39-page, December-2024-dated survey whose stated scope is exactly
this literature. `LI-EPRINT-24-SOKDSN` ("SoK: Decentralized Storage Network," Li, Xu, Zhang, Guo,
Cheng, IACR ePrint 2024/258, also published in High-Confidence Computing 2024) surveys DSN
protocol design across Filecoin, Storj, Sia, and Swarm but reports no churn-driven repair-bandwidth
measurement of its own; its erasure-coding discussion restates Storj's analytic Poisson-durability
model from `WILKINSON-STORJ-18` rather than adding a new figure.

## Where this leaves the two brief-stated modeled-churn conclusions

The brief's two-papers-disagree observation is confirmed and is traceable to a single cause: the
churn regime assumed. `CHUN-NSDI-06`'s feasibility result holds because PlanetLab's population
loses data almost exclusively to disk failure at a slow, roughly-known rate (θ ≈ 6.85), which lets
a system that reintegrates returning replicas build a working surplus without ever estimating
availability directly. `BLAKE-HOTOS-03`'s infeasibility result holds because Gnutella's population
churns continuously and unpredictably, so that even distinguishing transient disconnection from
departure (the paper's own best lever, a roughly 30x bandwidth saving) leaves 1 TB at high
availability "hopeless" without also restricting membership to the most reliable 5% of hosts. A
decentralized deployment that recruits arbitrary consumer participants rather than institutionally
hosted or staked, well-provisioned ones supplies the Gnutella-like regime, not the PlanetLab-like
or Walrus-like one — `ANDERSON-CCGRID-06`'s own measured BOINC/SETI@home host lifetime, 89.5 days
average as of 2005, sits closer to Gnutella's turnover than to PlanetLab's 2.23-year mean disk
lifetime. `DIMAKIS-TIT-10`'s own Gnutella-trace result is the closest thing in the corpus to a
regenerating-code-specific answer to this question, and it says the mechanism's simulated
advantage nearly disappears exactly in that regime — but it is a 2007-era simulation over a
2001-era trace, not a measurement of a real regenerating-code deployment, and nothing published
since updates it with newer trace data or a live implementation.

## What remains unestablished

No retrieved source instruments a deployed system that (a) uses a regenerating code — MSR, MBR,
or a mechanism the authors themselves derive from that framework — and (b) runs on a population
whose measured churn resembles Storj's 9.6%-per-month or Gnutella's higher continuous turnover,
while (c) reporting repair traffic in bytes moved rather than a simulated or analytically derived
figure. Establishing this requires either instrumenting a live regenerating-code deployment
recruiting genuinely open participants, or re-running `DIMAKIS-TIT-10`'s or `WILKINSON-STORJ-18`'s
simulation methodology against a churn trace measured after 2020 — `LI-IWQOS-23-STORJ`'s 16-month
Storj crawl is the most recent such trace this pass located and is not yet paired with any
regenerating-code repair-cost model in a published source.

---

# Continuous participation from mobile devices

## Verdict: open

Apple and Google publish, in detail, which background mechanisms exist and what they permit; no
published paper measures a peer-to-peer (P2P) application accepting inbound requests, relaying for
another peer, or holding a Distributed Hash Table (DHT) routing-table slot while an iOS or Android
process sits in the state those mechanisms actually produce. Every "mobile P2P" measurement the
corpus holds or this search found either kept the app in the foreground (DTube), tested a mobile ad
hoc network rather than an OS-managed smartphone process (Kademlia-in-MANET), or is a project's own
engineering account (Berty) rather than a controlled measurement. The corpus's own note on this
domain — before this pass added anything — already stated this as a gap; the search below confirms
it and quantifies the platform mechanisms in place of the missing measurement.

## What iOS permits, read from the current vendor documentation

An iOS app that moves to the background is, by default, suspended shortly afterward: its process
stays resident in memory but executes no code and its open sockets close. Apple's current
documentation states the transition callback itself — `applicationDidEnterBackground` — "has five
seconds to perform any tasks and return," after which "the system puts your app into the suspended
state" (`developer.apple.com/documentation/uikit/extending-your-app-s-background-execution-time`,
fetched 2026-09-02). An app can ask for more time by calling `beginBackgroundTask`, but the
documentation no longer states a fixed number of seconds — it directs the developer to read the
system-supplied `backgroundTimeRemaining` property at run time instead, because the granted duration
is dynamic; third-party developer reports (not Apple's own documentation, so recorded here as
unverified) describe approximately 30 seconds when the extension is requested from an
already-backgrounded state and approximately 3 minutes when requested at the moment of
backgrounding.

Beyond that short extension, iOS supplies five mechanisms for code to run later, each with a
distinct trigger and a distinct scope of what it is for, catalogued in Apple's "Configuring
background execution modes" page (`developer.apple.com/documentation/xcode/configuring-background-
execution-modes`, fetched 2026-09-02):

- **Background fetch** and **`BGAppRefreshTaskRequest`** — the system wakes the app "at regular
  intervals" it chooses, for a task Apple's own reference describes only as "a short refresh task"
  (`developer.apple.com/tutorials/data/documentation/backgroundtasks/bgapprefreshtaskrequest.json`);
  no fixed interval or duration is published, and the system can skip a scheduled refresh entirely
  based on the device's charge state, network conditions, and the app's own history of how the user
  actually opens it.
- **`BGProcessingTaskRequest`** — a longer task, Apple's own description stating it "can take minutes
  to complete," typically scheduled by the system for a period when the device is plugged in and idle
  (the same source as above); this is a maintenance window, not a standing execution grant.
- **Remote notifications with `content-available`** ("silent push") — a push arrives over the Apple
  Push Notification service (APNs) and wakes the app briefly to fetch new content before it is
  displayed; Apple's own background-execution-modes catalog states this mode exists so "the app uses
  push notifications as a signal that new content is available to download," which makes every
  invocation of this mechanism conditional on APNs itself having delivered the triggering push — a
  channel with its own reliability limits, covered below.
- **PushKit VoIP pushes** — the one mechanism Apple documents as reliably launching a suspended app
  regardless of the background-fetch scheduling algorithm, but restricted by policy to actual
  incoming calls: since iOS 13, the app must report the call to `CallKit` "in the same run loop" as
  receiving the push, and Apple's own developer forum states that failing to do so repeatedly causes
  the system to stop delivering further VoIP pushes to that app
  (`developer.apple.com/forums/thread/124134`, `developer.apple.com/forums/thread/128370`). A
  non-call use of this channel is a policy violation, not merely a missed opportunity.
- **`URLSession` background transfer** — a download or upload configured with a background session
  identifier is handed to a separate system daemon (`nsurlsessiond`) that continues the transfer
  after the app suspends or is even terminated by the system for memory pressure, relaunching the app
  in the background to deliver the completed transfer to its delegate. This is the one mechanism that
  survives suspension for an operation already in flight; it does not let the app accept a new
  inbound request while suspended; it moves one bounded file, not a standing bidirectional channel.

None of these five mechanisms opens a listening socket. An inbound TCP or UDP listener an app held
before backgrounding is closed with the rest of its sockets at suspension, and no publicly documented
API reopens one without the app first being woken by one of the five triggers above. A suspended iOS
app cannot be dialed; it can only be told, through one of these channels, that something is waiting
for it once the channel itself succeeds in reaching it.

## What Android permits, read from the current vendor documentation

Android's restriction path is graduated rather than binary. Two independent mechanisms narrow what a
background process can do: Doze mode, triggered when the device is stationary, unplugged, and
screen-off for a system-determined interval, and App Standby Buckets, which classify every installed
app by recent-use pattern independently of Doze.

Doze suspends network access and ignores wake locks outside periodic maintenance windows; deferred
alarms scheduled through `setAndAllowWhileIdle` or `setExactAndAllowWhileIdle` are throttled to at
most once every 9 minutes per app while idle, and app standby's own network access for an app with no
other exemption is granted "approximately once per day" during prolonged inactivity
(`developer.android.com/training/monitoring-device-state/doze-standby`, fetched 2026-09-02).

The standby buckets carry their own numeric job-execution quotas, published on Android's power-
management reference page (`developer.android.com/topic/performance/power/power-details`, fetched
2026-09-02):

| Standby bucket | Regular job quota | Expedited job quota | Alarm rate |
|---|---|---|---|
| Active | up to 20 min per rolling 60 min | up to 30 min per rolling 24 h | unlimited |
| Working set | up to 10 min per rolling 4 h | up to 15 min per rolling 24 h | 10/hour |
| Frequent | up to 10 min per rolling 12 h | up to 10 min per rolling 24 h | 2/hour |
| Rare | up to 10 min per rolling 24 h | up to 10 min per rolling 24 h | 1/hour |
| Restricted | once per day, up to 10 min | up to 5 min per rolling 24 h | 1/day |

An app enters the Restricted bucket automatically after 8 days of no use on Android 13 and later (45
days on Android 12), independent of any Doze state
(`developer.android.com/topic/performance/appstandby`, fetched 2026-09-02). A **foreground service**
— a background component the user can see, through a persistent notification, and that the user can
therefore choose to end — is the one Android mechanism exempt from these quotas and from Doze's
network suspension, and it is how a small number of production messaging apps hold a standing
connection open on Android today; Android 12 and later restrict which app states are allowed to
start one, and Android 14 requires the service to declare which of a fixed set of use-case types
(`connectedDevice`, `dataSync`, and others) it is claiming, each with its own eligibility rule.

Firebase Cloud Messaging (FCM), the delivery channel most Android apps use to trigger a wake, offers
a **high-priority** message class that Google's own documentation states FCM "attempts to deliver
... immediately even if the device is in Doze mode," granting the woken app "very limited" network
access and a partial wake lock for the duration of the callback
(`firebase.google.com/docs/cloud-messaging/concept-options`, search-cache fetched 2026-09-02); the
same documentation states the system will silently downgrade an app's high-priority messages to
normal priority if the app does not consistently show the user a visible result from them, at which
point Doze deferral applies again.

## The wake channel is itself a capacity-bounded, best-effort relay

Both platforms implement their push-wake channel as a store-and-forward relay with a stated,
non-negotiable capacity, not as a queue that grows to match demand. Apple's current documentation
states APNs "stores only one notification per bundle ID" per device — a second notification arriving
before the device reconnects replaces, rather than queues behind, the first — for at most 30 days by
default, adjustable per notification via the `apns-expiration` header, delivered "as a best-effort
service" with no delivery guarantee and explicit permission to reorder, throttle, batch, or drop
notifications depending on "the power state of the device"
(`developer.apple.com/tutorials/data/documentation/usernotifications/sending-notification-requests-
to-apns.json`, fetched 2026-09-02). Google's FCM documentation states the equivalent bound in more
granular form: the server holds at most four distinct **collapsible** messages per device
simultaneously, one per declared collapse key, replacing the oldest under a given key when a new one
with the same key arrives; a separate pool of up to 100 **non-collapsible** messages queues per
device, and once that pool fills, FCM discards every queued message and replaces them all with one
"limit exceeded" signal that tells the app only that it must perform a full resynchronization against
its own server, not what it missed (`firebase.google.com/docs/cloud-messaging/customize-messages/
collapsible-message-types`, search-cache fetched 2026-09-02); the default and maximum time-to-live
for any FCM message is four weeks, after which an undelivered message is discarded outright.

Neither platform vendor's own infrastructure — built with a managed server fleet, unlimited storage
budget by any single application's standard, and no adversarial peer to defend against — chose to
build unbounded, guaranteed-delivery message storage for a device that might stay unreachable. Both
capped the queue at a small fixed size, and both fell back to "tell the client to resynchronize" once
that cap is exceeded rather than attempting to preserve every individual item.

## No published paper measures a P2P application under these conditions

Corpus search and external search converge on the same result: the corpus's Domain L (transport and
reachability) holds NAT-traversal and QUIC-migration measurements, and separately a smartphone
power-consumption paper and a push-notification-latency citation, but no entry measures a P2P
application's server-side behavior — accepting an inbound stream, forwarding for another peer,
answering a DHT lookup — while the requesting process sits in the suspended or Doze-restricted state
the sections above describe.

**DBLP** (`dblp.org/search/publ/api`) returns zero hits for `mobile background execution`,
`background app refresh`, `iOS background execution measurement`, `push notification wake latency`,
`smartphone DHT participation`, `decentralized messaging mobile survey`, and `smartphone always-on
connectivity`. It returns results only for the adjacent, and distinct, literature on mobile ad hoc
networks (MANET) — multi-hop wireless routing among moving devices, a different problem from an
OS-managed smartphone process reaching the ordinary Internet — including Kademlia-in-MANET
(`ICUFN 2018`) and hierarchical-DHT churn mitigation for mobile networks (`Comput. Commun. 2016`),
neither of which tests OS-level suspension because a MANET simulation or testbed does not run the
routing code inside a sandboxed app process subject to iOS or Android's background policy. The two
DBLP hits that do concern an OS-managed phone and P2P networking — "Battery life of mobile peers with
UMTS and WLAN in a Kademlia-based P2P overlay" (PIMRC 2009) and "Silent Battery Draining Attack
against Android Systems by Subverting Doze Mode" (GLOBECOM 2016) — were found but not retrieved in
full for this pass; both predate, respectively by seven and by two years, the App Standby Bucket
system in the table above (introduced in Android 9, 2018), so neither can be read as a measurement
of the current restriction regime even once retrieved.

**arXiv** full-text abstract search for `"background execution" AND "peer-to-peer"`, `"background app
refresh"`, and `"Doze mode"` each return zero results.

**A 2013 clinical-engineering measurement**, Rothman, Dexter, and Epstein, "Communication Latencies
of Apple Push Notification Messages Relevant for Delivery of Time-Critical Information to Anesthesia
Providers" (*Anesthesia & Analgesia* 117(2), 2013), sent one probe push per minute to fixed iOS
devices in high-signal-strength locations for four months and reports, in its published structured
abstract (full text paywalled, not retrieved — this figure is recorded as **abstract-only** under
this corpus's evidentiary rule, not as verified full-text evidence): mean latency under 4 seconds for
iPhone over cellular, under 1 second for iPad/iPod over WLAN, with a 95% upper confidence bound of 42%
of days containing at least one delivery exceeding 100 seconds on iPhone. This is the closest
retrievable figure to a measured reliability bound on the push-wake channel itself, and it still does
not measure a P2P application, does not test a device actually left backgrounded by a user under
Doze- or App-Standby-equivalent restriction (no such restriction existed on iOS in 2013), and predates
the current APNs single-slot coalescing behavior's documentation by over a decade.

**Berty**, a deployed libp2p-and-IPFS-based mobile messenger, is the one project account found that
directly engages this problem on a real mobile P2P stack, in an engineering blog post rather than a
peer-reviewed measurement: "computing resources (CPU, battery, network) are relatively limited on
mobile devices," and holding several hundred simultaneous peer connections has, in the team's own
words, "a huge impact on a smartphone" even a high-end one
(`berty.tech/blog/bluetooth-low-energy`, fetched 2026-09-02). This is a project's own qualitative
account, not a controlled measurement with stated conditions, and is recorded here only as evidence
that the gap is recognized by at least one production team, not as a quantified result.

**DTube on Android** (`DOAN-NETWORKING-20`, already in the corpus) measured a mobile P2P-adjacent
video app for ten months across four physical Android phones, but every measurement session ran the
app in the foreground for exactly the duration of one video's playout; the paper does not report the
app moving to the background during measurement and does not test IPFS retrieval, gateway
connectivity, or DHT participation continuing once the app is backgrounded.

**TRAUTWEIN-ARXIV-26** (DCUtR hole-punching on IPFS, already in the corpus), the largest field
measurement in the corpus's transport domain, ran its 212 volunteer clients as ordinary libp2p/IPFS
peers; the paper records client mobility only as a network-identity artifact ("one highly mobile
client from 28 distinct networks," consistent with a laptop changing Wi-Fi networks) and states
nothing about client operating system or app-lifecycle state, so it cannot be read either way on
whether any client ran as a backgrounded phone app.

**GUPTA-MOBICOM-24** (already in the corpus, Domain L) measures cellular- and Wi-Fi-radio power draw
on stock Android phones with per-rail hardware instrumentation, including a standby-power figure — the
closest corpus entry to a cost measurement for holding a device reachable. It measures power only, not
whether or for how long the process delivering or receiving that traffic is permitted to run; it does
not bear on the scheduling question this open problem concerns and is not a candidate solution.

## What a store-and-forward relay must supply as a consequence

The requirement follows from combining the platform mechanisms above with one mechanism already in
the corpus: libp2p's Circuit Relay v2 (`VYZOVITIS-SPECS-23`), the P2P relay protocol the field
already uses to make a NAT-behind peer reachable. Circuit v2's own specification states the private
peer's reservation "becomes invalid if [it] disconnects," and requires that peer to "keep its
connection to R alive and refresh the reservation before it expires." A backgrounded, suspended iOS
process — sockets closed, no code executing — cannot hold that connection open, and cannot refresh a
reservation it has no running code to refresh. The same failure applies to Keizer et al.'s relay-
incentive mechanism (`KEIZER-MOBIHOC-20`), whose Proof-of-Timely-Relay verification "requires the
client to have simultaneous, independent contact with two separate relay-capable nodes" for the
duration of every relay session, and whose smart-contract settlement "requires constant blockchain
monitoring by both parties" as a design assumption the paper states outright. Both mechanisms assume
what a suspended mobile process cannot supply: a live, continuously monitorable connection held by
the reachable-but-behind-NAT device itself.

A relay a mobile client depends on for reachability, therefore, cannot be one that treats the client's
own liveness as the thing keeping its address valid. It must hold state on the client's behalf across
the client's own process suspension, and it must resume normal peer-to-peer operation once the client
process wakes rather than requiring the client to re-establish standing infrastructure state (a
reservation, a synchronous verification session) from scratch. Concretely, three properties are
required of it, each following directly from a mechanism documented above:

1. **A finite, disclosed queue capacity with an explicit overflow signal, not silent unbounded
   growth.** Both platform vendors' own push infrastructure — APNs with one slot per app per device,
   FCM with four collapsible slots plus a 100-message non-collapsible pool — cap at a small fixed size
   and, once exceeded, discard the backlog and tell the client only to resynchronize. A relay serving
   a mobile client should adopt the same discipline explicitly (a stated, bounded queue depth and a
   defined resynchronization signal once it is exceeded) rather than attempting unbounded storage that
   either exhausts the relay's own resources or silently drops data with no signal to the client at
   all.

2. **A wake path that does not depend on the relay dialing the client directly.** Because no
   documented mechanism on either platform reopens a listening socket on a suspended process, a relay
   cannot itself wake the client; it can only hold data ready for a request the client's OS-level
   background-fetch or push-wake mechanism will eventually issue. This makes the relay's freshness
   guarantee only as good as the platform's own wake scheduling — opportunistic and vendor-scheduled on
   iOS background fetch, quota-limited by standby bucket on Android jobs, or dependent on a push
   provider (APNs or FCM) the relay does not control and whose own delivery is stated by both vendors
   as best-effort, not guaranteed.

3. **Reservation and verification state that survives the client's absence rather than expiring with
   it.** Where Circuit v2 invalidates a relay reservation on client disconnect and Keizer et al.'s
   incentive scheme requires the client's synchronous participation in every settlement round, a relay
   built for mobile participation needs the inverse property: a reservation, subscription, or
   verification credential that remains valid across an interval of client absence bounded by a stated
   policy (an expiry the client renews on its own schedule when next reachable, not one that lapses at
   the first suspension) — with the tradeoff, not evaluated by any measurement this search found, that
   a longer-lived credential is also a longer-lived target for replay or impersonation if the relay
   does not separately verify the client is still the legitimate holder each time it becomes reachable
   again.

No published measurement establishes what queue depth, wake latency, or credential lifetime these
three properties should actually use for a P2P relay under real mobile deployment; the figures in
this section are read from platform vendor specifications, which state what the platforms permit, not
from any experiment that ran a P2P relay against them.

## What was searched

Corpus: `registry/index-measurements.md` and `registry/index-requirements.md` grepped for `mobile`,
`background`, `push`, and `APNs`/`FCM`/`GCM`; every Domain L entry read from `registry/targets-
L.json`; evidence files opened in full for `GUPTA-MOBICOM-24`, `DOAN-NETWORKING-20`,
`TRAUTWEIN-ARXIV-26`, `KEIZER-MOBIHOC-20`, `VYZOVITIS-SPECS-23`, and `SINGH-ARXIV-26`; confirmed
`EPSTEIN-ANESTHANALG-13` was a listed target with no evidence file (unretrieved) before attempting
retrieval.

Retrieval attempt: `tools/fetch-paper.py` against the DOI and journal URL for
`EPSTEIN-ANESTHANALG-13` returned a 2,774-character paywall stub, below the corpus's 6,000-character
full-text threshold; the paper's structured medical-journal abstract (which reports its key figures
directly, unlike a typical computer-science abstract) is used above and labeled abstract-only rather
than treated as full-text evidence.

External: DBLP publication-search API for `mobile background execution`, `background app refresh`,
`iOS background execution measurement`, `Android Doze`, `push notification wake latency`, `P2P mobile
battery`, `Briar mobile messaging`, `background transfer service`, `Kademlia mobile`, `mobile DHT
churn`, `smartphone DHT participation`, `P2P messaging smartphone measurement`, `decentralized
messaging mobile survey`, `peer discovery mobile network`, `gossip protocol mobile devices`, and
`mobile ad hoc P2P energy`. arXiv full-text search for `"background execution" AND "peer-to-peer"`,
`"background app refresh"`, and `"Doze mode"` (each zero results). Semantic Scholar's search API was
rate-limited (HTTP 429) throughout this pass and returned no results. General web search for Apple
and Google's own current developer documentation (fetched directly from `developer.apple.com` and
`developer.android.com`, with Apple's JSON documentation API used where the rendered HTML page is a
client-side application shell with no server-rendered text), for academic measurement of push
notification reliability in 2023-2026 (industry benchmarking reports and user-experience diary studies
found; no controlled reliability measurement more recent than the 2013 clinical study above), and for
mobile-deployed decentralized messengers with a published measurement of background behavior (Berty,
Scuttlebutt/Manyverse, Session/Oxen, Signal — engineering documentation and blog posts found for
Berty and Scuttlebutt; no peer-reviewed measurement of background-execution behavior for any of the
four). The most recent directly relevant publication found and retrieved is `TRAUTWEIN-ARXIV-26`
(2026), which does not itself address mobile OS background state; the most recent publication found
whose own subject is mobile background execution is Rothman, Dexter, and Epstein (2013),
abstract-only.

---

# Removing illegal material from content-addressed storage

## Verdict: open

No published construction makes a peer cryptographically unable to serve a specified piece of
already-published content in a permissionless, content-addressed network. Every mechanism found,
deployed or proposed, is one of two kinds: a voluntary identifier denylist that a node operator may
or may not consult, or a key-destruction scheme that presupposes a cooperating uploader and a
pre-established custody committee — a condition an adversary who deliberately publishes illegal
material will never supply. Deny-list compliance in a real deployed network, IPFS, has been measured
directly, repeatedly, and as recently as 2026: compliance is high only at the one operator that
maintains the list, falls to under a fifth of requests at independent gateways, and is defeated
outright, at zero cost, by re-encoding the same bytes under a different hash.

## What the deployed mechanism is, and how it is measured

Sokoto, Balduf, Trautwein, Wei, Tyson, Castro, Ascigil, Pavlou, Korczyński, Scheuermann, and Król
("Guardians of the Galaxy: Content Moderation in the InterPlanetary File System," USENIX Security
2024) ran the first full measurement of IPFS's only deployed moderation mechanism, Protocol Labs'
"badbits" denylist. A Content Identifier (CID) in IPFS is a hash of the data itself, so any peer can
verify what it serves against the identifier requested; the denylist stores, for each blocked item,
the hex-encoded SHA-256 of the base32-encoded CID rather than the CID itself, so an operator can test
membership without holding a plaintext list of blocked material — a privacy technique for checking
membership, not an enforcement mechanism, since nothing compels a node to run the check or to act on
a match. Protocol Labs applies the list only to gateways it operates itself.

The paper's dataset: 411,522 of the list's then-410,000+ entries recovered by hash-matching against
CIDs collected from roughly 300 billion Bitswap requests (mid-2021 to January 2024, covering about 1
billion unique CIDs) and 1.3 billion DHT requests (September 2022 to January 2024, 120 million CIDs);
368,762 of the resulting 417,912-CID denylist (badbits plus phishing URLs mined from four Web2
anti-phishing feeds) successfully downloaded and classified. By content type: 87.97% copyright
material (mostly PDF/ePub academic texts migrated from shadow libraries such as Anna's Archive and
the Nexus project), 5.81% phishing, 0.06% terrorist material (255 CIDs), and under 0.01% content the
authors' automated classifier flagged as explicit, of which a subsequent check against the Internet
Watch Foundation's hash database matched three images, all classified as hentai (Japanese
pornographic anime/manga) rather than genuine CSAM; content the takedown senders themselves labeled
CSAM was excluded from download entirely and handled through separate coordination with the IWF, so
the paper reports no independent verification of how much CSAM the badbits list holds.

Gateway compliance, measured by sending HTTP HEAD requests for a daily sample of 5,000 badbits and
5,000 Web2-denylist CIDs across 431 gateways through January 2024: gateways operated by Protocol Labs
itself block essentially all badbits content; gateways run by large CDNs block about 18%; other
public gateways cluster similarly low. Content persists a mean of 713 days between first observation
on the network and inclusion on the denylist, against under a day for the Web2 anti-phishing feeds the
same paper compares against. Within the IPFS peer-to-peer layer itself — Bitswap and the DHT, as
opposed to the HTTP gateways — the paper finds no evidence of enforcement at all; filtering is a
gateway-side, not a protocol-side, phenomenon.

Kastantin, Balduf, Ascigil, Sokoto, Scheuermann, Duda, Król, and Korczyński ("Netting Phish in the
IPFS Ocean," ACM Web Conference 2026), overlapping in authorship with the 2024 paper, ran an
eleven-month follow-up (September 2024–July 2025) focused on phishing specifically, sampling under 1%
of daily Bitswap traffic (a stated lower bound) and 3.3 million CID-bearing passive-DNS requests. It
found 10,489 phishing CIDs, twice the number carried by the combined public anti-phishing feeds
(APWG, OpenPhish, PhishTank) for the same period, and reports that the badbits denylist "adds no
additional CIDs beyond the union of APS and our detections" — the central curated list contributed no
coverage the independent web-facing feeds and the authors' own pipeline had not already found,
nineteen months after the 2024 paper documented the same list's coverage gaps. During the measurement
window 196 gateways updated their blocking policies, moving 569 CIDs from allowed to blocked; the
paper frames this as a lower bound on active moderation activity across the gateway population, not
as evidence the list itself is comprehensive.

## Circumvention: alternative-hash re-encoding, not a partial gap

Both the 2024 and 2026 papers, and an independent third paper, converge on the same finding by three
different methods, which raises it from an isolated result to a structural property of hash-derived
content addressing.

Sokoto et al. re-added 100 already-blocked phishing files to the network using a different hash
function for the CID (Kubo, the reference IPFS implementation, supports 72), then re-requested them
through the gateways that had been blocking the originals. Of 57 gateways blocking any of the sampled
content, 56 served the re-hashed copy, and content-level evasion succeeded for 97.4% of individually
tested CIDs; the single resistant gateway also proved to be the one gateway vulnerable to the paper's
separate directory-wrapping evasion (requesting blocked content by a relative path inside an
unblocked parent directory succeeded for 67 of 68 tested CIDs, 98.5%, on that gateway; the authors
disclosed both findings, and cite an earlier private test that found and fixed four more vulnerable
Protocol-Labs-operated gateways before publication).

Karapapas, Pittaras, Polyzos, and Patsakis ("Hello, won't you tell me your name?: Investigating
Anonymity Abuse in IPFS," arXiv 2506.04307, June 2025) independently confirmed the same class of
evasion by choosing a different chunk size when re-adding content, which likewise yields an unrelated
CID, and states plainly that "a malicious actor can circumvent it by simply choosing an alternative
chunking size when adding the file to IPFS," citing the Sokoto paper's own hash-function-substitution
result as the precedent. The same paper measured pinning-service Know-Your-Customer practices
directly: Pinata and Fleek accepted the first disposable email address the authors generated;
Filebase accepted one after four attempts; 4EVERLAND required only a cryptocurrency wallet, itself
creatable with no identifying information; all three email-gated services worked over Tor. Uploading
a functioning, VirusTotal-flagged WannaCry sample and a synthetic malware stub to five pinning
services succeeded on every one, with no service performing content inspection before accepting or
serving the file.

Kastantin et al.'s 2026 measurement documents the same defeat occurring in deployed attacker
behavior, not as an experiment the researchers ran themselves: clustering 10,489 collected phishing
pages by content similarity, the paper finds that in the two largest clusters (1,459 and 256
instances) attackers vary only HTML comments or whitespace between successive uploads, which is
sufficient to generate a fresh, unlisted CID each time while leaving the rendered page identical, and
states the general mechanism directly — "any modification, no matter how small, yields a new CID."
The same paper ran a controlled test of a second, independent circumvention path: it published a
file through its own IPFS node, fetched it once through each gateway, then withdrew the only copy
from its node. Every gateway that had returned the file in the first round still returned it in the
second, because fetching through the gateway had caused the gateway's own backend IPFS node to
announce itself as a new content provider — nineteen such new providers appeared after a single round
of gateway fetches, entirely independent of whether the original publisher remained online. A voluntary
denylist enforced only at the point of retrieval cannot outrun a protocol property in which the act of
retrieval itself creates a new, unlisted, independently persistent copy.

## Why key-destruction cryptography does not reach this problem

The corpus and a broader search turned up one 2026 systematization of the general technique closest
to "make serving cryptographically impossible": Aikebaier, "SoK: Cryptographic Erasure on Public
Ledgers" (IACR ePrint 2026/1109), which classifies application-layer schemes that leave a ledger or
store untouched and instead destroy the decryption key needed to read data already committed to it —
crypto-shredding. It organizes the field into a twelve-cell grid crossing data locus (ciphertext
on-chain, an off-chain store such as IPFS anchored by an on-chain commitment, or a hybrid) against key
custody (single custodian, (t, n)-threshold committee, time-lock, or witness encryption), and proves
a formal equivalence between a "Destruction-IND" security notion and the EU's GDPR Article 17 "render
unrecoverable" erasure criterion for a cooperating data controller.

The scheme does not solve, or claim to solve, the problem this pass asked about, for two reasons the
paper's own definitions make explicit rather than requiring inference.

First, every one of the paper's seven evaluated reference architectures assumes a single controller
who both creates the data and either holds or empanels the committee that later destroys the key —
the paper's worked example throughout is a UK law firm's audit-trail records under a compliance
mandate, and its equivalence theorem is a tool for that controller to document a defensible erasure
claim to a regulator. Nothing in the taxonomy addresses who selects a custody committee, or under what
process, in a permissionless network with anonymous, adversarial uploaders who have every incentive
not to cooperate. A committee empanelled to revoke content over an open network's objection is a
trusted party by another name, and the paper never proposes how one would be selected without
reintroducing exactly that trust.

Second, and structurally decisive independent of the first point: the paper's own security game
(Definition 2, "Destruction-IND") is explicitly voided once an adversarial party has reconstructed the
plaintext before the destruction event — the paper states this as Remark 1, "if k ≥ t, the adversary
reconstructs Dec from the coerced shares before Destroy is ever invoked and wins trivially," and
frames its whole model around measuring security only for an adversary who has not yet crossed that
threshold. For illegal material on a real content-addressed network, that threshold has already been
crossed by the time anyone requests removal: Sokoto et al. measured a 713-day mean gap between first
appearance and denylist inclusion, during which any number of independent nodes may already have
retrieved, decoded, and independently re-published the plaintext, exactly as Kastantin et al.
demonstrated gateways do automatically on ordinary retrieval. A key-destruction scheme secures a
single ciphertext behind a committee; it has no mechanism for, and its own formal model does not even
define security against, a party who already holds the plaintext and re-inserts it under a CID the
committee never touched.

A separate, earlier proposal specific to IPFS — Politou, Alepis, Patsakis, Casino, and Alazab,
"Delegated content erasure in IPFS" (Future Generation Computer Systems 112, 2020) — could not be
retrieved in full text (the publisher copy is paywalled; the institutional-repository copy at Charles
Darwin University sits behind a Cloudflare challenge that blocked automated retrieval). Its mechanism,
as described consistently across the publisher abstract and independent third-party summaries, is a
protocol for propagating a signed erasure request across IPFS nodes, restricted so that "only the
original content provider or delegates" may issue one. That restriction is reported here as an
unverified, secondary-source characterization rather than a measured fact, per this pass's own
sourcing standard, and it is enough on its own to place the scheme outside the scope of this problem:
a mechanism gated on the uploader's own request cannot remove content an uploader deliberately
published and has no interest in withdrawing. Independent evidence that the scheme was never adopted
comes from its own co-author: Patsakis is also a co-author of the 2025 Karapapas et al. paper, which
states without qualification, five years after the erasure proposal, that "there is no official
deletion mechanism for IPFS," citing the 2020 paper only as the source for that absence, not as a
deployed remedy.

## The one structural property that does resist a classical peer-to-peer countermeasure

Content poisoning — flooding a network with corrupted copies of a targeted item so that a downloader
is likely to retrieve a broken file, deployed historically by copyright holders against BitTorrent and
earlier file-sharing networks — is defeated by the same property that makes deny-list circumvention
trivial. A content identifier is the hash of the exact bytes requested, so IPFS's Bitswap protocol
(and BitTorrent's own per-chunk hashing, for the same reason) lets a downloader verify each block it
receives against the CID it asked for, per Benet's original IPFS design description already in this
corpus (`BENET-ARXIV-14`) and per Trautwein et al.'s deployed-system description cited throughout the
papers above. A poisoned block simply fails verification and is discarded, so it is the identical
mechanism that makes removal-by-denylist gameable (any single-byte change produces an unlisted,
independently valid identifier) that makes removal-by-poisoning impossible (any corrupted block is
independently checkable and discarded). No source in this pass measures content poisoning against
IPFS specifically; the point is structural, not a separate measured result, and is recorded here only
to close off a mechanism family a synthesis step might otherwise propose.

## Assumption doing the work

Every mechanism examined supplies its guarantee only because some party is assumed to cooperate
voluntarily: a gateway operator choosing to consult a hash-based denylist it has no protocol-level
obligation to honor; a custody committee that must be empanelled, and trusted, before an adversarial
upload ever occurs; an uploader who must be the one requesting their own content's erasure. A
decentralized deployment, by definition, has no operator positioned to compel any of these — no party
can force an independent gateway operator to adopt a denylist, empanel a committee an anonymous
adversary will accept in advance, or compel a malicious uploader to request deletion of the material
they deliberately published. The measured deployed reality is a voluntary honor system with
partial, heterogeneous, and empirically falling-further-behind compliance (the central curated list
added zero unique coverage over independent detection fully nineteen months after its own gaps were
published), defeated at the protocol layer by the same hash-derived addressing that gives
content-addressed storage its integrity guarantee in the first place: change one byte, and the
"same" content is a different, unlisted object.

## What was searched

Corpus: `registry/index-measurements.md` and `registry/index-requirements.md` were read in full and
grepped for `deny.?list`, `removal`, `illegal`, `csam`, `takedown`, `moderat`, `redact`, `censor`,
`content.address`, `chameleon`, `mutable`, `forget`, `gdpr`, `badbits`, `blocklist`, `poison`, and
`unlinkab`. Full evidence entries opened: `BALDUF-IMC-23`, `BALDUF-IMC-24`, `BENET-ARXIV-14`,
`BENET-FILECOIN-17`, `DANEZIS-WALRUS-25`, `KEIZER-CSUR-24`, `WEI-NSDI-24`, `ZHANG-ARXIV-25`,
`ZHANG-PACMHCI-24`, `WOLCHOK-WOOT-10`. `KEIZER-CSUR-24` (2024 survey) supplied the pointer that
motivated the rest of this pass: it states the badbits process was, at the time of that survey,
undocumented ("little is known about the moderation process involved in preparing the bad bits
list") and its adoption unmeasured.

Beyond the corpus: DBLP's publication-search API for `IPFS content moderation`, `IPFS illegal
content`, `denylist IPFS`, `redactable blockchain` (30 hits, all chain-rewriting constructions
explicitly out of scope per the SoK's own §1.1 and therefore not pursued further), `NeuralHash
attack`, `content addressable network censorship`, and `InterPlanetary File System security`, the
last of which surfaced both `SOKOTO-USENIXSEC-24` and the 2022 IPFS eclipse-attack paper (Prünster,
Marsalek, Zefferer, USENIX Security 2022 — disrupts availability network-wide, not a moderation
mechanism, not pursued further). Web searches covered `IPFS content-addressed storage illegal content
removal survey 2025 systematization of knowledge`, `threshold decryption revocable access
content-addressed storage cryptographic erasure 2024 2025` (surfaced the crypto-erasure SoK),
`content poisoning copyright enforcement peer-to-peer measurement effectiveness`, `IPFS content
moderation 2026 badbits denylist measurement follow-up study` (surfaced the 2026 WWW phishing
paper), and `decentralized storage CSAM detection cryptographic 2026 arxiv` (no relevant result).

Full text retrieved with `tools/fetch-paper.py` and read in full: `SOKOTO-USENIXSEC-24` (Guardians of
the Galaxy, USENIX Security 2024, 92,483 characters via the USENIX-hosted PDF after the DBLP `ee`
link resolved only to a landing page), `POLITOU-ARXIV-25` (Karapapas et al., arXiv 2506.04307, June
2025, 53,162 characters), `SOK-CRYPTOERASURE-EPRINT-26` (Aikebaier, IACR ePrint 2026/1109, 79,714
characters), and `KROL-WWW-26` (Kastantin et al., ACM Web Conference 2026, 60,193 characters, via the
KOR Labs-hosted author copy). `POLITOU-FGCS-20` (Politou et al., Future Generation Computer Systems
112, 2020) could not be retrieved: the Elsevier/ScienceDirect page and the ResearchGate page both
returned HTTP 403, and the Charles Darwin University institutional-repository PDF returned a
Cloudflare interstitial rather than the document; its mechanism above is therefore reported only from
secondary description and flagged as such, per this pass's rule against citing measurements from
unretrieved sources. The most recent directly relevant full-text retrieval is `KROL-WWW-26`
(April 2026 conference date, retrieved September 2026).

---

# Open problem: verifying contributed bandwidth without trusting the contributor

## Verdict: partly

**Verdict: partly.** Published constructions cut the achievable self-report inflation from a
demonstrated 177x down to a proven 1.33x, and one 2024 construction measures a single link's
capacity directly, from ordinary peers, within about 10% error, without any of them trusting the
contributor. Every one of these constructions obtains that bound by spending something a fully
open, permissionless, decentralized deployment does not already have for free: a fixed
semi-trusted quorum of measurement infrastructure, a pre-existing Sybil-resistant method for
drawing a random, uncontrollable witness sample from the same population being measured, or
continuously funded dedicated measurement bandwidth separate from the network's own capacity.
None verifies one untrusted peer's bandwidth contribution from bare peer-to-peer primitives with
no privileged quorum and no Sybil-resistance assumption supplied from outside the mechanism.

## What was searched

Corpus entries opened in full: `GHOSH-HOTPETS-14` (TorPath/TorCoin), `JANSEN-HOTPETS-14` (TEARS),
`JANSEN-PAM-21` (Tor bandwidth-estimation accuracy), `JOHNSON-POPETS-17` (PeerFlow),
`TRAUDT-ICDCS-21` (FlashFlow), `SHENG-NDSS-24` (Proof of Backhaul), `KEIZER-MOBIHOC-20` (Proof of
Timely Relay for NAT-traversal relays), `LEVIN-SIGCOMM-08` (BitTorrent PropShare, local
reciprocity rather than third-party verification), `ANDERSON-CCGRID-06`, `AIYER-SOSP-05` (BAR
fault tolerance, storage-audit accountability model, checked for a bandwidth analogue and found
none). Index files searched by keyword: `bandwidth`, `proof.of.bandwidth`, `proof.of.relay`,
`proof.of.coverage`, `reciprocal`, `tit.for.tat`, `bandwidth.token`, `bandwidth.credit`,
`torflow`, `peerflow`, `eigenspeed`, `bandwidth auth`.

Beyond the corpus: DBLP queries `q=proof of bandwidth` (5 hits, all already known or off-topic —
`LighTx`, a closed-access proof-of-bandwidth transaction-transfer system from NETYS 2021, and two
"Securing Proof-of-Stake Nakamoto Consensus Under Bandwidth Constraint" entries that use
"bandwidth" as a network-model parameter, not as a measured contributor claim) and `q=verifiable
bandwidth` (0 hits). Web searches run: "verifiable bandwidth accounting decentralized
peer-to-peer 2024 2025", `"proof of bandwidth" attack sybil 2024 2025 arxiv`, "DePIN bandwidth
verification survey SoK systematization 2024 2025", "Helium proof of coverage attack spoofing
measurement paper", `"Selfied" sybil defense bandwidth consumption blockchain paper`, `"Sharing Is
(S)caring" DePIN security privacy arxiv`, and `"Proof of Backhaul" attack critique follow-up
citation 2025`. These surfaced `Selfied` (Hou, Yu, Sun, Computer Networks, Nov. 2024 — in-protocol
bandwidth *consumption* as a Sybil-resistance resource for block production, a different problem
from verifying a contributor's bandwidth *supply* claim, not retrieved in full because it does not
bear on this problem), `FairRelay` (arXiv:2405.02973, 2024 — payment-channel atomicity between
content delivery and payment, which prevents a relay from being cheated of payment or a client of
content, but does not itself verify a bandwidth-capacity claim to a third party; abstract read via
WebFetch, not retrieved in full for the same reason), and a DePIN security survey ("Sharing Is
(S)caring," 18th International Conference on Network and System Security, Nov. 2024 / Springer
March 2025) whose direct PDF is captcha-gated and whose Springer and ResearchGate mirrors returned
403/redirect errors on this pass — its search-result summary describes only inherited Sybil and
consensus vulnerabilities in DePIN generally, with no bandwidth-specific mechanism named, so it is
recorded here as unretrieved rather than cited for any claim. No search surfaced a construction
published after `SHENG-NDSS-24` (NDSS 2024, the most recent directly relevant publication found)
that improves on its bound, and no search surfaced a published attack against it. EigenSpeed
(Snader and Borisov, IPTPS 2009), the peer-measurement predecessor every paper below cites and
attacks, was not independently retrieved; its measured attack figures are recorded below only as
`JOHNSON-POPETS-17`'s own re-implementation and measurement of attacks against it, not from
EigenSpeed's own text.

## The scale of the problem this corpus establishes first

Before any mitigation, `JANSEN-PAM-21` measures how bad self-report is even absent an adversary.
Tor's deployed pipeline derives a relay's advertised bandwidth from the relay's own two
self-measured numbers; an active 51-hour experiment adding a real measurement burst to 4,867
relays found total advertised network capacity rose from 360 Gbit/s to 550 Gbit/s — a 52.9%
underestimate the authors state is itself a lower bound, because their measurement machine was
capped at 1 Gbit/s and could not test every relay. The error concentrates exactly where it is most
useful to an adversary: relays in the top capacity quartile discovered a median 32.5% more
capacity than they had reported (median annual uptime 56.6%), against 0.0% for the two lowest
quartiles (median uptime 93.2%) — so a self-report pipeline is not merely noisy, it specifically
under-rewards large, low-uptime relays and over-rewards small, stable ones, and the paper states a
relay can detect when it is being measured and adjust its behavior accordingly. This is the
starting condition every construction below is measured against, not a hypothetical.

## Peer-measurement bounds a lie; it does not need a trusted authority to see the traffic, but it does need Sybil-resistance to bound the coalition

`JOHNSON-POPETS-17` (PeerFlow) replaces both self-report and a centralized probe (TorFlow) with
peer measurement: a subset of relays — the largest fraction µ=0.75 by capacity per circuit
position — each keep an application-layer byte count of every relay they directly interact with,
and Directory Authorities aggregate those peer reports rather than trusting either party's own
number. Implemented and measured against a real attack: a relay falsely reporting 125,000 KB of
bandwidth while selectively dropping non-measurement traffic raised its consensus-weight share
from 7% to 11% against TorFlow (a measured 177x bandwidth-inflation factor, Shadow simulation, 498
relays). Under PeerFlow's own peer-measurement design, the same class of attack is proven bounded
by a factor γ — a worked numerical example gives γ=4.52 — provided the adversary's voting-weight
fraction stays below a trim threshold λ=0.256. The paper is explicit about what supplies that
precondition: "even without any trusted relays" the bound requires a single adversarial coalition
to stay under λ, and states this means "some other component" — a Sybil-resistance mechanism
controlling how much aggregate weight one identity can acquire — must keep any single coalition
under that threshold for the bound to hold at all. PeerFlow supplies the bounded-inflation
mechanism; it consumes, rather than produces, Sybil-resistance. It also still requires a
functioning Directory Authority infrastructure to collect, trim (discarding the fraction λ=0.256
of most-disagreeing measurements), and noise (calibrated Laplace differential-privacy noise,
δnoise=1 MiB, εnoise=0.1) the aggregated peer reports before publishing them, because raw
peer-to-peer byte counts would otherwise leak which relay pairs exchanged how much traffic — a
side channel the mechanism must actively suppress at a stated cost, not one it can ignore. Achieving even the
bounded γ is stated by the authors to require an adversary to send traffic in only one direction
or concentrate it on a minority-weight subset of measuring relays, patterns the paper calls
"highly observable" but does not itself detect or block beyond the stated bound.

## Active load-testing narrows the bound further; the cost moves to a dedicated, funded measurement quorum

`TRAUDT-ICDCS-21` (FlashFlow) replaces both self-report and passive peer measurement with active
load-testing: a coordinated team of measurers forces a target relay to carry traffic large enough
to approach its claimed capacity, cross-checking a sampled fraction of returned cells
byte-for-byte so a relay that fabricates responses is caught with probability approaching 1 as
more responses are checked. The measured result is the strongest bound in this corpus: an
analytic inflation ceiling of 1.33x true capacity (derived from a traffic-ratio cap with
recommended parameter r=0.25), against the 177x PeerFlow demonstrated for TorFlow and PeerFlow's
own 4.52x bound for its recommended parameters — FlashFlow's own Table II states this comparison
directly. Real-Internet trials (Fremont, Santa Rosa, Washington DC, Bangalore, Amsterdam; 7 runs
per configuration over 24 hours) measured relay capacity within 11% of ground truth in 95% of
trials and within 20% in 99.8%. A Shadow simulation at 5% of Tor's scale (328 relays) found
FlashFlow cut network weight error from TorFlow's 29% to 4% and eliminated transfer timeouts
entirely at every tested load level. This bound has a real, ongoing cost: the design requires a
measurement team's aggregate bandwidth to exceed the highest capacity among target relays by a
factor f=2.84 in the deployed-scale simulation — 3 Gbit/s per team, provisioned and funded as an
ongoing operational cost separate from the bandwidth being measured — and requires the same
Directory-Authority/Bandwidth-Authority infrastructure Tor already runs, with a majority of both
sets required to be honest for the security bound to hold. The authors state their own design
explicitly shares TorFlow's Sybil weakness: a relay controlling several IP addresses on one
physical machine can be measured separately at different times and obtain a full-machine-capacity
estimate for each alias, with only an unimplemented "measure co-resident relays simultaneously and
average" proposed as a mitigation. FlashFlow also measures capacity, not delivered service — the
authors state explicitly that a relay could pass every load test while carrying little real client
traffic on non-measurement circuits, and call detecting that an unresolved future-work item shared
with TorFlow.

## The 2024 construction: peers measuring peers, with no measurer required to be individually trusted, but with the challenger sample itself needing to already be Sybil-resistant

`SHENG-NDSS-24` (Proof of Backhaul) is the most recent published construction and the only one
that verifies a link's bandwidth using a crowd of *ordinary*-bandwidth peers ("challengers")
instead of a dedicated high-bandwidth measurement server or a fixed authority set, tolerating
Byzantine (corrupted) challengers directly rather than assuming an honest quorum by
administrative fiat: proven correct for a corrupted-challenger fraction β<1/3 with no verifier
timer, and up to β<1/2 with one. Measured accuracy on a controlled testbed: under 5% error at 250
Mbps with 6 or more challengers and a 100 ms challenge; on a real deployment of roughly 25-30
active Ethereum-wallet challengers spread across the US, Europe, and Asia, backhauls of 500/700/
1000 Mbps measured with 4.2%/4.1%/9.9% average error. Two participant attacks are named and
bounded rather than merely observed: a withholding attack (a corrupted challenger under-sends)
degrades accuracy only slightly (3.6% raw error at 20% Byzantine challengers); a rushing attack (a
corrupted challenger colludes with a corrupted prover to shortcut the measured path and inflate
the result) is curtailed by a correction factor α=(n−2f)/(n−f) applied to every measurement,
which the authors state necessarily lowers the reported "guaranteed bandwidth" even when every
challenger is honest — 28% below the true value at the tested β=0.2 setting — because the
protocol cannot distinguish an honest run from a rushing attack after the fact and must discount
uniformly to stay safe. Against three prior bandwidth-estimation techniques at 500 Mbps
(pathchar, MagicTrain, speedtest), Proof of Backhaul matched speedtest's accuracy while using
roughly 73x less data (6.88 MB versus speedtest's 501 MB), and comfortably beat pathchar and
MagicTrain's accuracy despite their using still less data than either. This is the strongest
published bound on data cost, accuracy, and Byzantine tolerance simultaneously found in this
search, and it achieves all three from an untrusted, ordinary-bandwidth peer population rather
than a designated authority — but the paper itself states, unprompted, two of the preconditions
that make this possible: the verifier or challenge coordinator must be able to select "a fresh,
randomly drawn subset of challengers per measurement from a larger active pool" so a corrupted
prover cannot predict who will test it, and eliminating the rushing attack's residual bandwidth
discount entirely — rather than merely bounding it — requires an added shuffle-coordination round
(PoB-Shuffle) that the authors describe as "an active area of research" to implement efficiently
in practice, not something the base protocol delivers. The random, uncontrollable sampling of
challengers from the participant pool is exactly a Sybil-resistance precondition, supplied to the
mechanism from outside it — Proof of Backhaul answers "how do you verify one link's bandwidth once
you already have an unpredictable, bounded-Byzantine sample of the network to draw challengers
from," not "how do you obtain that sample in an open-membership network with no admission
control." The protocol's liveness (whether a challenge completes and produces a result, as
opposed to whether the result is correct) also depends on a challenge coordinator that the authors
state is not itself Byzantine-fault-tolerant, mitigated only by economic incentives and a pool of
redundant coordinators, not proven. And the measured object is a single link's instantaneous
capacity at one measurement window, not a running account of bytes a peer actually forwarded on
behalf of other peers over an accounting period — the object a reciprocal-exchange credit ledger
needs is closer to the latter than the former.

## Fully decentralized, circuit-cooperative proof exists, but its guarantee is statistical across a population, not per-relay, and it was never measured past a preliminary simulation

`GHOSH-HOTPETS-14` (TorPath/TorCoin) is the one construction in this corpus with no designated
authority at all: a circuit's own four participants (client, entry, middle, exit) jointly produce
a cryptographic proof obtainable only if all four actually forwarded traffic to each other — no
proper subset can reconstruct the shared blob alone — and Bitcoin's blockchain prevents the
resulting coin from being claimed twice. This genuinely verifies, without any single contributor's
self-report and without a bandwidth authority, that real forwarding occurred on one specific
circuit. Three limits keep it from answering this problem for an open decentralized deployment.
First, circuit assignment itself depends on a majority-honest quorum of decentralized "assignment
servers" running a verifiable shuffle — a group-trust assumption, not zero-trust, and one the
paper illustrates with "if there are 10 assignment servers, we might require at least 6" without
adopting a tested value. Second, the guarantee the mechanism gives is a population statistic, not
a per-relay one: under the paper's own stated assumption that at most half of network identities
collude, only 1/16 of assigned circuits are fully colluding and able to mint coins for zero
genuine transfer — the authors state explicitly that coin possession proves goodput on one
specific circuit at mint time, not an ongoing, per-relay measure, and that a higher colluding
fraction was not analyzed. Third, the reported packet-overhead figures (roughly 5% of Tor traffic
at a tuning parameter m≥10) come from a Python-Twisted message-passing simulation the authors
themselves describe as "preliminary," with no stated relay count, run count, or live-network
deployment — no measurement in this corpus validates these figures against a real network. The
Sybil case this problem exists to prevent — the same operator running many relay identities to
occupy more than one position on its own circuit — is explicitly out of scope: the authors state
this "should be rare" and defer building any detection mechanism to future work. Its
contemporaneous companion paper, `JANSEN-HOTPETS-14` (TEARS), states the underlying problem this
whole line of work responds to in as many words: "measuring relay bandwidth securely is an open
research problem," and supplies no bandwidth-audit mechanism of its own, requiring one as an
unspecified external component.

## The narrow case with a working check node is not collusion-free either

`KEIZER-MOBIHOC-20`'s Proof of Timely Relay, built for NAT-traversal relays rather than an
anonymity network, verifies one relay's forwarding by routing a hash-and-timestamp report through
a second, independently chosen "check" node in parallel with the data path, so the working relay's
own report is never trusted alone — settled through an Ethereum smart contract that withholds
payment from both parties until each submits a mutual trust score. This requires the client to
reach two independent relay-capable nodes simultaneously for every session, and the paper's own
security analysis addresses only a rational adversary motivated by resource gain, not one willing
to collude: it does not analyze what happens when the working relay and the check node the client
selected are the same coalition, which is exactly the case a Sybil-heavy or a colluding relay
population would try to arrange. Per-transaction settlement cost, measured on a private Ganache
chain at April-2020 Ethereum gas prices, ran roughly $0.10-$0.20 for the relay and $0.40-$0.60 for
the client per contracted relationship — a real, non-zero cost of the on-chain accountability
layer, not free verification.

## What remains unestablished

No retrieved source verifies an untrusted peer's bandwidth contribution to a third party using
only primitives available to that peer's own open-membership network — every published bound
requires, as an input rather than an output, one of: a fixed quorum assumed majority-honest by
administrative design (Directory Authorities, Bandwidth Authorities, TorPath's assignment
servers), a pre-existing Sybil-resistant method for drawing an unpredictable challenger or witness
sample from the same population being measured (Proof of Backhaul's challenger pool), or
continuously funded dedicated measurement bandwidth provisioned separately from the network's own
capacity (FlashFlow's measurer teams). Where the bound is tightest (FlashFlow's 1.33x, Proof of
Backhaul's sub-10% error) the authority or witness-sampling precondition is most explicit; where no
authority or witness precondition is required at all (TorPath), the guarantee weakens to a
population-level statistic with no field measurement past a preliminary simulation, and the
paper's own contemporaneous companion states plainly that secure bandwidth measurement was still
an open research problem. No search in this pass located a published construction after
`SHENG-NDSS-24` (2024) that removes the challenger-sampling precondition, nor a published attack
against it. Closing this gap for a fully open, permissionless deployment — one drawing its
challenger or measuring-relay population from the same unauthenticated pool of contributors it is
trying to keep honest, with no fixed authority set and no external Sybil-resistance mechanism
supplied — is not demonstrated anywhere in the retrieved literature.

---

# Open problem: honest capacity reporting in a capacity-ordered overlay

## Verdict: open

**Verdict: open.** No retrieved paper defends a structured overlay that places participants at a
position, or rank, determined by self-reported bandwidth against a participant that misreports to
gain that position. The published defenses closest to this problem — for Tor's bandwidth-weighted
relay-selection pipeline — bound a different quantity, a flat selection *probability* over an
unordered relay set, not a *position* in an ordered structure, and every one of them either
assumes a semi-trusted measurement quorum or a challenger sample that is itself assumed
Sybil-resistant rather than made so by the mechanism. HSkip+, the specific design this problem
names, states its bandwidth-ordering property assumes honest reporting; two independent surveys,
four years apart, find no published follow-up that revisits that assumption.

## What was searched

Corpus entries opened in full: `JOHNSON-POPETS-17` (PeerFlow), `TRAUDT-ICDCS-21` (FlashFlow),
`SHENG-NDSS-24` (Proof of Backhaul), `JANSEN-PAM-21` (Tor bandwidth-estimation accuracy),
`GHOSH-HOTPETS-14` (TorPath/TorCoin), `JANSEN-HOTPETS-14` (TEARS), `ELAHI-WPES-12` (Tor guard
rotation), `FELDMANN-CSUR-21` (self-stabilizing overlay survey, already keyed for its HSkip+
forward-citation check), `JACOB-JACM-14` (Skip+). Index files searched by keyword: `bandwidth`,
`capacity`, `misreport`, `self-report`, `overlay position`, `freerid`, `incentive`, `whitewash`,
`reciprocity`. This confirmed the corpus already holds every directly relevant Tor
bandwidth-measurement paper and the two surveys that forward-cite HSkip+.

Beyond the corpus: DBLP queries `capacity-ordered overlay bandwidth misreport` (0 hits),
`self-stabilizing skip graph bandwidth heterogeneous` (0 hits), `verifiable bandwidth claim
peer-to-peer` (0 hits), `skip graph bandwidth` (0 hits), `proof of bandwidth` (5 hits, all already
known or off-topic — a closed-access transaction-transfer system and two unrelated
proof-of-stake papers using "bandwidth" as a network-model parameter). arXiv queries
`abs:"bandwidth" AND abs:"overlay" AND abs:"misreport"` (0 hits), `abs:"self-reported bandwidth"`
(0 hits), `abs:"capacity-aware" AND abs:"peer-to-peer" AND abs:"Sybil"` (0 hits). OpenAlex and
Semantic Scholar keyword searches on "self-reported bandwidth peer-to-peer overlay attack" and
"Sybil-resistant bandwidth reporting peer-to-peer overlay" returned no on-topic result beyond what
DBLP and general web search already found. General web search for `"bandwidth-ordered" OR
"capacity-ordered" overlay peer-to-peer misreport attack defense`, `skip graph OR DHT
self-stabilizing bandwidth heterogeneous adversarial misreport 2024 2025`, and `verifiable
bandwidth claim decentralized peer-to-peer overlay position Sybil 2024 2025 2026` surfaced two
papers not previously in the corpus, both retrieved in full text and checked directly rather than
from their abstracts: `IHLE-CSUR-23` (a 2023 systematic review of peer-to-peer incentive
mechanisms, 178 primary papers) and `PATEL-ARXIV-25` (a September 2025 survey of secure
peer-to-peer networks). A third paper, `ARADHYA-ARXIV-25` (self-stabilizing graph linearization
with untrusted advice, April 2025), was retrieved in full because its title is the closest textual
match to "self-stabilizing," "linearization," and "overlay" found anywhere in this search; its
full text confirms it does not bear on this problem, recorded below. The most recent publication
found that measures a capacity-misreporting defense of any kind is `SHENG-NDSS-24` (NDSS 2024);
the most recent survey checked and found silent on this specific mechanism is `PATEL-ARXIV-25`
(September 2025).

## The mechanism HSkip+ leaves undefended

`FELDMANN-CSUR-21`, a survey of self-stabilizing overlay designs, states HSkip+ (Feldotto,
Scheideler, Graffi, P2P 2014) "reduces the stabilization time in practice and needs less work for
single join or leave events" relative to its predecessor Skip+, and that HSkip+ orders nodes by
bandwidth rather than by an arbitrary identifier so that "routing never transits a node with less
bandwidth than min of endpoints" — a property that concentrates routing load onto high-bandwidth
nodes by construction. The survey's own bibliography and text, read in full, contain no mention of
bandwidth or capacity heterogeneity anywhere except in the title of the one reference it cites for
HSkip+ itself; no self-stabilizing overlay design published in the survey's window is presented as
revisiting HSkip+'s bandwidth-ordering property. A node that reports a higher bandwidth than it
has moves toward the position routing concentrates onto — the position from which it can observe,
delay, or drop a disproportionate share of traffic transiting the structure, and the position other
nodes stop routing around rather than through. HSkip+'s own asynchronous self-stabilization proof
assumes the reported value is simply given; it contains no check of it. `PATEL-ARXIV-25`, a
September 2025 survey of secure peer-to-peer networks covering skip graphs, skip nets, rainbow
skip graphs, skip-webs, and structured-overlay Byzantine defenses (Fireflies, GUARD, Saad and
Saia's group-based multiparty computation), was read in full for any post-2021 treatment of
capacity or bandwidth as an ordering key subject to attack; the word "capacity" appears only once,
in an unrelated definition of what peers may share, and "bandwidth" appears four times, none in
connection with overlay position. The structured-overlay defenses this survey does cover — GUARD's
cryptographic-signature isolation of misbehaving skip-graph peers, Fireflies' accusation-based
peer removal, Saad and Saia's quarantine-on-detection multiparty protocol — all defend against a
peer that drops, corrupts, or forges *messages* after occupying a position; none checks whether
the *claim that earned the position in the first place* was true. Two surveys four years apart,
one exhaustively checking the self-stabilizing-overlay literature and one exhaustively checking the
secure-peer-to-peer-networks literature, independently find nothing.

## The closest published defenses bound a different quantity under assumptions this problem cannot take for granted

The nearest published work is the Tor relay-bandwidth-measurement literature, already the subject
of this registry's companion entry on verifying contributed bandwidth
(`registry/open-problems/verifiable-bandwidth.md`, item 8 of `BRIEF.md`'s open-problem list). That
literature answers a structurally different question. Tor selects a relay for a circuit slot with
*probability* proportional to its consensus weight, drawn independently for every circuit, over a
flat set of relays with no ordering relation between them; `JOHNSON-POPETS-17` (PeerFlow) and
`TRAUDT-ICDCS-21` (FlashFlow) bound how far a lie can inflate that one number. A capacity-ordered
structured overlay in the family HSkip+ belongs to instead assigns each node a fixed *position* in
a sorted or ranked structure — the position determines who a node's neighbors are, which lookups
route through it, and, per the survey passage quoted above, that routing never transits a lower-
bandwidth node than the path's endpoints. Gaming a selection probability wins more circuits over
time, in proportion to the inflation achieved; gaming a position can win a specific, structurally
privileged place — adjacency to specific other nodes, or a hub role a skip-graph-style structure's
own routing rule guarantees will not be bypassed — for as long as the position is held, independent
of how many further lookups happen to route through it. No paper in this search measures whether
PeerFlow's peer-measurement design, FlashFlow's active load test, or `SHENG-NDSS-24`'s (Proof of
Backhaul) trustfree challenger-consensus protocol, composed with a rank-ordered structure in place
of Tor's flat weighted selection, would bound an adversary's achievable position the way each
bounds an adversary's achievable selection-probability share; none of the three was designed,
tested, or discussed by its authors as an ordering input rather than a weighting input.

Each also carries an assumption a capacity-ordered peer-to-peer overlay with no privileged
membership cannot take for granted, independent of the selection-versus-position distinction.
PeerFlow's bound (a proven inflation factor of 4.52x at its worked parameters, against a measured
177x for Tor's deployed TorFlow pipeline) requires Directory Authorities to aggregate trimmed,
noised peer measurements, and the paper states directly that even "without any trusted relays" the
bound holds only if a single adversarial coalition's weight stays under a trim threshold
λ=0.256 — a precondition the paper states some other, unsupplied Sybil-resistance mechanism must
enforce. FlashFlow's tighter bound (1.33x) requires a dedicated measurement team funded to
3 Gbit/s per team in the deployed-scale simulation, run by the same Directory/Bandwidth Authority
infrastructure, with a stated requirement that a majority of both sets be honest. Proof of Backhaul
achieves its bound (sub-10% measurement error at up to 1000 Mbps, tolerating up to a proven
corrupted-challenger fraction β<1/3 with no verifier timer) without a fixed authority set, using
instead a coordinator that draws challengers at random from a pool — but the paper states this
selection must draw "a fresh, randomly drawn subset of challengers per measurement from a larger
active pool" so a corrupted prover cannot predict who will test it, without specifying how that
pool's membership is itself kept free of the same participant's Sybil identities. Every one of the
three bounds a lie once a witness or authority population already known to be adequately honest is
available; none of the three, nor any paper citing or extending them found in this search, builds
that witness population from bare open-membership peer-to-peer admission with no external
Sybil-resistance assumption.

## Measurement without any adversary already defeats the naive assumption

`JANSEN-PAM-21` measures that Tor's deployed self-report pipeline underestimates total network
capacity by at least 52.9%, with the error concentrated on exactly the relays an adversary
mimicking to gain position would want to resemble: relays in the top capacity quartile discovered a
median 32.5% more true capacity than they had reported, against 0.0% for the bottom two quartiles.
No adversary is assumed in this measurement — the paper's active speed-test experiment ran against
ordinary, non-adversarial relays. A capacity-ordered overlay that orders participants by
self-report inherits this bias before any participant lies at all: a naturally low-uptime,
high-capacity node reports itself into a lower position than its true capacity would place it, and
the paper states directly that "a relay can detect when it is being measured" — the same detection
capability that, applied deliberately rather than incidentally, is the misreporting attack this
problem asks about. No paper retrieved in this search measures the analogous quantity — position
error, not consensus-weight error — for a rank-ordered structure.

## What remains open

Nothing published places participants in a capacity-ordered overlay position — a skip-graph rank,
a sorted-line position, or an equivalent ordering key that determines routing adjacency and hub
status — from an untrusted self-report while measuring resistance to a participant that
misreports to move up. The nearest published work bounds a related but distinct quantity (Tor's
flat selection-probability weight) under assumptions (a trusted or already-Sybil-resistant witness
population) that a capacity-ordered overlay with fully open membership does not automatically
have, and none of it has been composed with, or evaluated against, a position-determining
structure. HSkip+'s own bandwidth-ordering property is stated by its authors to assume honest
reporting; `FELDMANN-CSUR-21` (2021) and `PATEL-ARXIV-25` (2025), read in full and independently,
each find no published design that revisits that assumption. Making the position worthless to hold
falsely — the third approach this problem's statement names alongside measurement and mechanism
design — appears in this corpus only as resource-burning Sybil resistance for *identity* count
(`PATEL-ARXIV-25` §2.3: computational puzzles, proof-of-space-time, proof-of-useful-work bounding
how many identities an adversary can hold) and as `GHOSH-HOTPETS-14`'s per-circuit proof of actual
goodput transfer (TorCoin, unimplemented beyond a preliminary simulation, verified only after the
fact and per-circuit rather than as a precondition for occupying a structural position); neither
mechanism family has been applied to make a false capacity claim costly specifically at the moment
it is used to select a position in an ordered structure.

---

# Forward secrecy under long partitions in decentralized group key agreement

## Verdict: open

No published paper proves or disproves the conjecture. The paper stating it, Yen, Fábrega, Da,
Kleppmann, Mumm, Park, Zelenka, "BeeKEM: Decentralized, Secure and Efficient Group Key Agreement"
(IACR ePrint 2026/1434), calls it a conjecture in its own text and gives no proof. A companion
notebook page by the paper's first author, dated 31 July 2026 — after the mechanism was designed,
before or concurrent with the ePrint posting — states the same limitation directly: "We lack a
formal impossibility result; it seems inherent, but this is something I will be thinking about a
little more." Two other corpus results address a related but distinct question, worst-case update
communication and computation cost, and neither one's authors claim it bears on the retention
conjecture.

## The conjecture, stated precisely

BeeKEM is a decentralized continuous group key agreement (DCGKA) protocol: a group of users
derives a shared symmetric key, refreshed over time, with no central server and no requirement
that every user's device see every other user's operations in the same order. Membership changes
and key refreshes are recorded in a hash-linked operation graph each device replays locally; when
the network partitions, users on different sides can each keep issuing `Update` operations, and
when the partition heals, the two sides' operation graphs must merge.

BeeKEM defines a retention parameter κ: each user retains her κ most recent personal secrets. Two
correctness and security properties depend on κ in opposite directions:

- **Correctness Under Concurrency (CUC)**: after a partition heals, every user can recover every
  group secret produced by an `Update` on the other side, so long as she was a member on that
  side at the time. CUC holds only at κ = ∞ — retaining every past personal secret.
- **Forward secrecy (FS)**: compromising a user's current state must not expose group secrets
  from before her most recent update. Full FS requires deleting each personal secret immediately
  after it is superseded — κ = 1.

A user who deletes her old secret sk_old to gain forward secrecy, then reconnects after a
partition, cannot decrypt group secrets the other side produced from updates to sk_old — she has
destroyed the material needed to recover them. BeeKEM's own text states the mechanism explicitly:
"If Alice did an Update during the partition and deleted her old secret sk_old for the sake of FS,
she would lose her ability to 'catch up.'" The paper's precise sentence is: "We conjecture the
tradeoff between CUC and FS may be inherent in decentralized settings" — with an earlier passage
narrowing the scope further, to DCGKA schemes with sublinear update cost specifically.

The paper constructs both endpoints — BeeKEM itself (κ tunable, weakens FS to gain CUC) and a
sketched variant, BeeKEM^FS, that deletes immediately (full FS and full cross-fork security, at
the cost of losing recovery of any secret defined on a branch a user did not directly
participate in) — but states BeeKEM^FS is a sketch, not benchmarked, with "a full treatment"
deferred to future work. Constructing both extremes of a tradeoff is not a proof that no protocol
can do better than trade one against the other; it demonstrates the tradeoff is non-empty at both
ends, nothing about points in between or about whether a fundamentally different construction
could occupy neither.

## What the two adjacent corpus results actually measure, and why neither settles it

The task names two candidate results and asks whether either bears on the retention conjecture.
Both are read in full in this corpus and both answer a different question: the worst-case
communication or computation *cost* of a CGKA operation, not whether forward secrecy and
cross-branch recovery can coexist under a network partition.

**Bienstock, Dodis, Garg, Grogan, Hajiabadi, Rösler, "On the Worst-Case Inefficiency of CGKA"
(TCC 2022; corpus key BIENSTOCK-TCC-22).** This paper proves that any CGKA protocol using
public-key encryption only through its encrypt/decrypt interface — never its internal algebraic
structure — has worst-case communication Ω(n) in group size n, on a specific pattern of
operations: some users join and go passive while the remaining active users refresh keys among
themselves, a pattern forced by post-compromise security's requirement not to reuse key material
those passive users received. The proof goes through an intermediate primitive, Compact Key
Exchange, and a black-box separation adapted from Boneh, Papakonstantinou, Rackoff, Vahlis, and
Waters (FOCS 2008). The paper's own model is fully synchronous and non-concurrent — its text
states the bound "already holds for fully synchronous, non-concurrent CGKA executions" — and its
full text, checked directly, contains no mention of network partitions, forks, or branches; its
uses of "partition" refer to partitioning a set of tree nodes into paths inside the protocol's own
data structure, an unrelated sense of the word. This paper bounds how much a CGKA protocol must
communicate in the worst case; it says nothing about whether a protocol that has already paid that
cost can simultaneously keep full forward secrecy and full ability to recover secrets from an
unmerged concurrent branch.

**Bartusek, Bitansky, Dodis, Garg, Wu, "Fair-Weather No More: Guaranteed Efficiency in Secure
Group Messaging" (IACR ePrint 2026/1677; corpus key BARTUSEK-EPRINT-26).** This paper builds the
first CGKA with worst-case polylogarithmic cost for every core operation, by routing the
construction through a lattice-based primitive (incremental and updatable distributed broadcast
encryption, built on the decomposed Learning With Errors assumption from Abram, Malavolta, and
Roy, CRYPTO 2025) whose internal structure the construction uses directly, non-black-box. The
paper's text states plainly that this narrows the scope of Bienstock et al.'s impossibility result
by exploiting exactly the barrier that result identifies — PKE-as-sealed-component — without
refuting the result itself. Its own text, checked directly, contains no discussion of partitions,
forks, or branches either; the string "fork" occurs only as a verb describing test-user generation
inside a security-game reduction, and "branch" only as program control flow in the construction's
pseudocode. Crucially, the paper achieves post-compromise security with every operation
polylogarithmic, but forward secrecy costs a dedicated `FSRefresh` operation the paper states is
"the only linear-time operation in our new CGKA scheme" — and the paper lists as its own open
problem: "We leave it as an open problem to achieve a truly (computation-wise!) sublinear CGKA
scheme with forward secrecy." So even outside any decentralized or partition setting, achieving
low-cost updates and full forward secrecy together, in the same construction, is unresolved by
this paper's own account.

Read together, the two results establish a communication/computation cost floor and a way past a
specific instance of it, on an axis — worst-case update cost as a function of the primitive class
used — that is orthogonal to the retention conjecture's axis: whether recovering a group secret
defined on a branch a user did not participate in is compatible with that user having deleted the
personal secret from which that group secret derives. A protocol could in principle have cheap
(polylogarithmic) updates and still face the retention conjecture's tension, or expensive (linear)
updates and still face it — cost and the CUC/FS tension are different properties of a scheme, and
neither cited paper's proof or construction touches partitions, forks, or branch merging at all.
Bartusek et al.'s own unresolved gap (sublinear-cost forward secrecy, full stop) is suggestive
that the general tension between cheap updates and full forward secrecy is not confined to the
decentralized setting, which — if anything — weakens rather than supports treating decentralization
specifically as the source of the retention conjecture's tension, but neither paper states this
inference itself; it is not drawn in either paper's text and is recorded here as reasoning from
what is measured, not as a further published claim.

## The closest related formal result, and why it falls short of a proof

Alwen, Mularczyk, Tselekounis, "Fork-Resilient Continuous Group Key Agreement" (CRYPTO 2023;
corpus key ALWEN-CRYPTO-23) is the paper BeeKEM's own text cites as the prior work that "develop[s]
a scheme with security against this type of attack, which they call a cross-fork attack, albeit in
a different (centralized) setting from DCGKA." Fork-Resilient CGKA (FR-CGKA) targets exactly the
scenario the retention conjecture describes: a group whose members' views of the operation history
diverge, then must reconcile. Its formal model represents each client's local state as a set of
markers ("pebbles") on a history graph — a move pebble (can this client still act on this epoch),
a visited pebble (has a transition out of this epoch already been irreversibly processed, which
forward secrecy requires), and a key pebble (does the client still hold this epoch's key). Its
strongest construction, O-FREEK, achieves what the paper calls the optimal security predicate:
every epoch is secure "unless keeping it secure would be logically inconsistent with protocol
correctness" — meaning an epoch on a fork branch the client has not yet committed to abandoning
cannot be forward-secure, by the paper's own definition of what correctness requires, and only
becomes forward-secure once the client's visited pebble marks that branch as no longer
recoverable. This is a formal statement, in a different but closely related model, of the same
shape as BeeKEM's conjecture: forward secrecy for a given epoch and the ability to still recover
that epoch's key on an unresolved alternate branch are mutually exclusive by construction, not
merely in the two protocols this paper happens to have built.

This falls short of settling BeeKEM's conjecture for two reasons the corpus's own reading of the
paper states. First, FR-CGKA's "optimal predicate" is a property proved of the specific formal
framework the paper builds (pebbled history graphs over a server-relayed, causally-ordered
delivery channel) and of the specific constructions (FREEK and O-FREEK) proved to realize it — not
an unconditional impossibility theorem separate from any construction, of the kind Bienstock et
al. (TCC 2022) prove for worst-case cost. The paper does not claim, and this evidence entry finds
no claim, that every conceivable DCGKA construction, including ones outside the pebbled-history-
graph formalism, must exhibit the same tension. Second, FR-CGKA's delivery model requires only
causality-respecting delivery per sender-receiver pair through a server or mailboxing service that
need not behave correctly — close to, but not identical to, BeeKEM's fully peer-to-peer gossip
setting with no server role of any kind. Whether the pebbling framework's optimality result
transfers unchanged to BeeKEM's precise setting is not established in either paper.

## What would settle it

A proof would need to state a formal model general enough to range over every DCGKA construction —
not one specific protocol family — capturing partition and branch-merge as the model's own
primitive operations, and show that no construction in that model can simultaneously achieve (a)
recovery of every group secret produced on a branch a user was a member of, after that branch
merges back, and (b) forward secrecy for that user's state at every point before her most recent
update, including during the partition. Fork-Resilient CGKA's pebbling formalism and optimal-
predicate proof are the nearest published template for such an argument; extending it to a model
without any server role and checking whether its impossibility component (the "logically
inconsistent with protocol correctness" clause) is a property of the pebbling framework's own
definitions or a property of the underlying problem itself would be the direct next step. No
published paper retrieved for this pass performs that extension.

## What was searched

Corpus: read BeeKEM's evidence entry (YEN-EPRINT-26) and its full cached text
(`sources/text/YEN-EPRINT-26.txt`) directly for the conjecture's exact wording and surrounding
argument; read the two named corpus papers in full (BIENSTOCK-TCC-22, BARTUSEK-EPRINT-26) and
grepped their cached full text for "fork", "partition", and "branch" to check for any partition-
setting discussion the evidence-file summary might have missed; read every other H-domain
(group messaging) evidence entry bearing on forward secrecy, fork resolution, or decentralized
delivery, including ALWEN-CRYPTO-23 (Fork-Resilient CGKA), ALWEN-EUROCRYPT-22 (CoCoA),
ALWEN-SCN-24 (DeCAF), AUERBACH-CRYPTO-25, CHEVALIER-CCS-24 (Quarantined-TreeKEM), BIENSTOCK-TCC-20,
and MANGIPUDI-EPRINT-26 (Auditable CGKA); grepped `index-measurements.md` and
`index-requirements.md` for "retention," "partition," "conjecture," and "cross-fork."

Beyond the corpus: web search for `"BeeKEM" cross-fork forward secrecy decentralized group key
agreement`; `decentralized continuous group key agreement forward secrecy partition tolerance
impossibility 2026`; `"key retention" OR "retention parameter" forward secrecy fork DCGKA
impossibility proof`; `survey OR "SoK" decentralized secure group messaging continuous group key
agreement 2025 2026`; and a DBLP-directed search for citations of the Fork-Resilient CGKA paper.
Retrieved and read the Ink & Switch Keyhive project notebook page "06 · E2EE in the Local-First
Setting" (inkandswitch.com/keyhive/notebook/06/, authored by Derek Yen, BeeKEM's first author,
dated 31 July 2026), which states the same open status directly, in the author's own words, outside
the ePrint text itself. No 2023-or-later survey or Systematization of Knowledge specific to
decentralized CGKA or DCGKA was found; the most recent related work located is BeeKEM itself
(ePrint 2026/1434) and Bartusek et al. (ePrint 2026/1677), both from the weeks immediately
preceding this search.

---

# Secondary indexes and range queries over content-addressed stores

## Verdict: partly

Published work gives a specified, formally characterized mechanism for range access and
range-based reconciliation over one ordered attribute of a content-addressed store, and one
concrete backend realization of that mechanism has been measured, on one machine. No published
paper measures secondary-attribute indexing, multi-attribute range queries, or range-query serving
across peers, at any network scale, in a deployment without a blockchain consensus layer or a
semi-trusted service provider. The literature also does not resolve whether prolly trees, the one
content-addressed tree structure with real deployed implementations, are canonical under insertion
order at all — a 2026 paper building a new system on top of prolly trees states this is still
unverified.

## What a content-addressed store retrieves, and what "secondary index" adds

A content-addressed store maps a cryptographic hash of an object's bytes to the object; retrieval
requires the hash. A primary-key range query — "every object whose key falls between x and y," for
some application-defined ordering key distinct from the content hash — and a secondary-attribute
index — "every object whose field F equals or falls near v" — both require an ordered structure
built over the store's contents, because the content hash itself carries no order relation to
either the primary key or F. Every mechanism the corpus and this search turned up builds that
ordered structure the same way: a tree whose node boundaries are set deterministically from node
content (so independently-built trees over the same data converge to the same shape) and whose
nodes are then hashed Merkle-style, so the resulting index is itself a content-addressed object
and two replicas can compare, diff, and range-query it without transmitting the whole structure.
None of the retrieved work builds more than one such ordered dimension into a single measured
system; a true secondary index — one keyed on a field other than the store's own natural order —
requires either a second parallel tree of this kind per indexed attribute, or a multi-dimensional
generalization, and only the second has been specified (Willow, below), not measured.

## Merkle Search Trees: an ordered, content-addressed structure, with secondary-index use stated as unevaluated by its own authors

Auvolat and Taïani (SRDS 2019, `AUVOLAT-SRDS-19`) build a Merkle Search Tree (MST): items are
assigned to tree layers by a hash-derived rule, so any two replicas holding the same items
construct the identical tree, and any two trees can be diffed by comparing subtree hashes and
descending only into mismatches. Comparison between two trees holding n items with d differing
items costs O(d log_B n) messages; each read, insert, or delete costs O(log_B n), where B is a
fixed branching parameter (B = 16 in their experiments). Measured on a 1000-node (2000 in one
scaling test) actor-based simulation of a grow-only event store synchronized by gossip anti-entropy,
MST cuts bandwidth 66% and 99th-percentile delivery delay 31% against a vector-clock baseline
(Scuttlebutt) under light load; under heavy load at 2000 nodes, a competing hash-prefix-tree
baseline (Merkle Prefix Tree) fails to terminate at all from a message-count explosion, while MST's
bandwidth stays 45% below Scuttlebutt's, though MST's own diffusion uniformity (entropy metric) is
worse than Scuttlebutt's in every heavy-load configuration tested.

This measures anti-entropy propagation of one ordered event set, not secondary-attribute indexing.
The paper's own text proposes using an MST as a secondary index over data distributed across a
distributed hash table, and states directly: "The feasibility of such an approach when many updates
occur at many nodes has not yet been evaluated." No later paper in this search evaluates it either.

## Prolly trees: measured for insertion and creation cost, not for query cost, with canonicality itself unresolved as of 2026

Rawat, Vangani, Cornelius, and Daza (DLT Workshop 2024, `RAWAT-DLT-24`) build a prolly tree — a
content-addressed B-tree variant whose node ("chunk") boundaries are set by a hash-threshold rule
on each node's own content, giving it the same convergent-shape and range-navigable property as an
MST but with B-tree-style ordered access built in from the start. Their contribution, an
"Anchor Node" placed at the right edge of every level, bounds the number of chunks a sequential
insertion touches, measured against two real, deployed prolly-tree implementations — Dolthub's Dolt
and Canvas/okra (which uses libp2p in production) — on one machine (13th-gen Intel i7, 20 cores).
At 10 million entries, their tree-creation time is about 30-45% faster than Dolt's and their
insertion time about 24% faster than Dolt's and roughly 3.2 times faster than Canvas's, up to
17 million entries tested for creation.

Every figure measured is insertion or creation time. The paper states explicitly that "the
mechanisms by which two Prolly trees are compared" — the operation a range query or a secondary
index lookup would actually use — "fall beyond the scope of this paper," giving only sample code
in an appendix. No multi-node experiment, no query-latency figure, and no distributed deployment
appears anywhere in the paper.

Whether a prolly tree is even canonical — whether two replicas that received the same inserts in a
different order end up with byte-identical trees, the property every reconciliation mechanism in
this search depends on — remains unverified for the one prolly-tree implementation with the largest
deployed footprint. Deshpande's 2026 preprint building a new versioned-database storage engine on
top of a Dolt-derived prolly tree (`LIVINGDB-ARXIV-26`, arXiv 2605.00676, retrieved in full) states
plainly that the Dolt implementation "performs incremental updates rather than conceptually
rebuilding the tree from scratch" and that "it is not immediately clear from the documentation
whether the resulting structure is strictly canonical... under all insertion orders," naming this as
a question the authors plan to check empirically in future work — not yet checked, as of this
paper's own submission. That paper's own storage-sharing experiments (a single 50,000-row table
under 500 commits, one machine, no columnar storage yet implemented) measure how much disk space
content-based chunking saves across snapshots, not range-query or secondary-index performance, and
its one illustrated index structure is keyed on the table's own primary key, not a secondary
attribute. Meyer and Scherer's technical report (`MEYER-TR-24`, below) supplies the reason
canonicality is fragile for this specific structure: a prolly tree's chunk boundaries are set by a
rolling-hash window over consecutive items, so restricting the tree to an arbitrary subrange changes
which items fall inside that window and changes the resulting boundaries — the paper states plainly,
"Prolly-trees are not clamping-invariant."

## Range-based set reconciliation and range-summarizable order-statistics stores: the interface a secondary index needs, with one backend measured on one machine

Meyer's range-based set reconciliation (RBSR, already verified in this corpus per the brief) gives
two replicas holding ordered sets a way to compare a range, skip it if summaries match, split and
recurse if they mismatch, and enumerate directly below a size cutoff. Amparore (arXiv 2026,
`AMPARORE-ARXIV-26`) specifies exactly what storage backend RBSR needs — a Range-Summarizable
Order-Statistics Store (RSOS): `size`, `Aggregate(l,u)`, `Rank`, `Select`, `Enumerate(l,u)`, `Insert`,
`Delete` — and proves an aggregate-augmented B+-tree (caching, at every internal-node child pointer,
the subtree's element count and composable summary) realizes it, with `Rank`/`Select` at O(h),
`Aggregate` at O(Bh), `Enumerate` at O(h+k), for tree height h = Θ(log_B n). This bundle of
operations is precisely what a range-query or order-statistics secondary index needs to answer
"how many, and which, entries fall in this range" without a full scan.

The paper builds a concrete realization, AELMDB, extending the LMDB storage engine to hold this
aggregate metadata directly in B+-tree branch pages, and measures it against a from-scratch
implementation of the same interface (BTreeLMDB) on one machine (AMD 3700X, Linux), across six
synthetic workload families. AELMDB's reconciliation time is 4.69 to 13.98 times faster than
BTreeLMDB's, at 1.06 to 1.36 times the memory use, and 4% to 11% slower to insert into (because
every insert propagates aggregate deltas up the full root-to-leaf path). This is a real,
measured improvement in the cost of the operations a range or secondary index performs — but it
measures one storage backend on one machine, comparing two ways of computing the same range
aggregate locally; it does not measure query latency, throughput, or correctness across a network of
peers, and the paper states explicitly that concurrent transactions, crash recovery, cold-cache
behavior, and cross-engine portability are outside its evaluation. The paper also composes only one
ordered dimension per RSOS instance; realizing a true secondary index over a second attribute would
require a second RSOS instance kept in sync with the first as the underlying object set changes, a
composition this paper does not address.

## Willow: a specified multi-dimensional range index over a content-addressed store, with no measurement of any kind

The Willow protocol specification (`WILLOW-SPEC-23`, willowprotocol.org, NLnet-funded, not
peer-reviewed) generalizes one-dimensional RBSR to three dimensions — namespace, path, and
timestamp — over entries that reference content-addressed payloads directly (each entry carries a
`payload_digest`), which is the one mechanism found in this search that is both genuinely
multi-attribute and genuinely peer-to-peer: reconciliation is symmetric between two peers, requires
no blockchain, consensus mechanism, or privileged server, and the specification requires only that
each peer locally index its own held entries by the three coordinates well enough to split a range
into sub-ranges of roughly equal local cardinality. The document states no experiment, no benchmark,
no node count, and no dataset anywhere; its only quantitative claim is the asymptotic one inherited
by construction from recursive range-halving ("a logarithmic number of communication rounds"), not
measured on any concrete topology. Its own stated limitation: fingerprinting is called "not
mandatory for Willow, but it probably is a good idea," marking the entire construction optional
rather than a required guarantee, and a peer can supply "wildly inadequate" range-coverage metadata
with no defense given beyond noting a malicious peer already has other ways to disrupt
reconciliation.

## Which backing structures are actually safe to build a range index on: one proof, twelve unproven candidates, one proven failure

Meyer and Scherer (`MEYER-TR-24`, self-published technical report, Technical University Berlin,
2024) supply the property that decides whether any of the above ordered structures can serve
range-fingerprint queries correctly at all: a structure must be history-independent (equal sets
always produce structurally identical trees, which is what makes independent replicas agree) and,
additionally, clamping-invariant — restricting two structurally different trees holding the same
items to the same range must always yield the identical restricted subtree. The paper proves this
property in full only for treaps. It lists thirteen other candidate structures it believes are also
clamping-invariant — skip lists, zip trees, zip-zip trees, B-treaps, B-skip-lists,
randomized-block-search-trees, an external-memory history-independent B-tree and skip-list, skip
trees, dense skip trees, Merkle Search Trees, prolly trees, and G-trees — and states proving the
rest is "out of scope." One of the thirteen is proven false rather than merely unproven: prolly
trees, for the rolling-hash-window reason above. Merkle Search Trees are asserted, not proven,
clamping-invariant; no paper in this search proves it either way.

## The attack surface a working range index inherits: access-pattern leakage, scale-free in collection size

Grubbs, Lacharite, Minaud, and Paterson (IEEE S&P 2019, `GRUBBS-SP-19`) show that a server or peer
answering range queries over content whose access pattern is observable — which of the store's
records matched each query, without seeing plaintext query content or record values — lets an
observer reconstruct the approximate order of every record using only O(epsilon^-1 log epsilon^-1)
observed queries, a bound independent of both record count and value-domain size; on a real 61,000-
record ZIP-code dataset, 50 queries recovered the first two digits of a ZIP code (often identifying
a city) for a majority of records, and on a 600,000-record last-name dataset, roughly 500 prefix
queries recovered the first character of over 70% of names. This result targets encrypted-database
range queries specifically, but the mechanism it attacks — a server or peer returning which records
matched a range predicate — is exactly what any of the range-index constructions above does once
queries are served to a party the index owner does not fully trust. None of the range-index papers
in this search analyze or defend against this; the leakage is a property of answering range queries
at all, not of any one index structure's design, so it applies to Merkle Search Trees, prolly trees,
RSOS-backed stores, and Willow's 3d ranges alike whenever a query answer is observable to a party who
did not already hold the answer.

## Verifiable range queries: solved for a different problem, under a blockchain-plus-outsourced-server assumption

A distinct 2024-2026 line of work — found via DBLP search for "authenticated range query" and
confirmed by retrieving one paper's full text — solves range-query verifiability, not indexing
feasibility, and does so by assuming exactly the two things a decentralized content-addressed store
does not have: a blockchain supplying a global total order and trust anchor, and a semi-trusted
third-party service provider holding the raw data and the authenticated data structure (ADS). Yao,
Xin, Song, Mao, Torp, Ding, Srivastava, Li, Jensen, and Li's VTRQ (arXiv 2608.21314, retrieved in
full) states its own model directly: "a data owner sends raw data and an authenticated data
structure (ADS) to a service provider, while uploading a digest of the ADS to a blockchain," and the
querying client checks a returned result by recomputing the ADS root and comparing it against the
blockchain-anchored digest — a single data owner, a single (or small, named) service provider, and a
consensus mechanism supplying the trust anchor, none of which a peer-to-peer content-addressed store
without a blockchain layer supplies on its own. Three further 2024-2025 papers found on DBLP but not
retrieved in full — "Authenticated Range Querying of Historical Blockchain Healthcare Data Using
Authenticated Multi-Version Index" (`Distributed Ledger Technol. Res. Pract.` 2024), "New
Gas-Efficient Authenticated Range Query Schemes in Hybrid-Storage Blockchain" (`IEEE TNSE` 2025), and
"Consistency-Aware Scalable and Authenticated Learned Index for Range Query" (ICDE 2025) — advertise
the same outsourced-database-plus-blockchain model by their titles and venues (all explicitly
"blockchain" or index-authentication papers in the outsourced-verification tradition); none is cited
here as evidence of a measured result, only as further instances of the same assumption family,
because their full text was not retrieved.

## Adjacent infrastructure that does not address indexing or range queries

Two further 2026 results turned up in this search bear on content-addressed storage but not on
secondary indexing or range queries, and are recorded here only to mark them as checked and
irrelevant to this problem rather than missing. Tidehunter (arXiv 2602.01873, Web3-affiliated
authors, integrated into the Sui blockchain's validator storage in production) solves point-lookup
throughput for content-addressable, uniformly-keyed storage — 830,000 writes per second on a 1 TB
dataset with 1 KB values, 8.4 times RocksDB's throughput — by treating the write-ahead log as
permanent storage and using an "optimistic index" for single-round-trip point lookups; it explicitly
targets "content-addressable storage, deduplication systems, and blockchain validators" but its
index answers only exact-key point queries, not ranges or secondary attributes. The IPFS
provider-record indexer measured by Wei et al. (NSDI 2024, `WEI-NSDI-24`, already in this corpus)
holds 173,998,039,712 provider records and is centralized in practice at one operator; it indexes
content identifiers to locate providers, the primary-key lookup case, not a secondary attribute or a
range.

## What was searched

Corpus: read `registry/index-measurements.md` and `registry/index-requirements.md` in full for
entries matching Merkle search tree, prolly, secondary index, range query, order-statistics,
content-addressed, authenticated data structure, verifiable index, range proof, skip list, treap,
zip tree, B-tree, CRDT map, Dolt, okra, IPLD, and content-defined chunking; opened in full the ten
matching entries — `AMPARORE-ARXIV-26`, `AUVOLAT-SRDS-19`, `RAWAT-DLT-24`, `ALMEIDA-CSUR-25`,
`GRUBBS-SP-19`, `KLEPPMANN-CONEXT-24`, `KLEPPMANN-PAPOC-22`, `MEYER-TR-24`, `TRAUTWEIN-INFOCOM-24`,
`WILLOW-SPEC-23`.

External: DBLP publication-search API (`dblp.org/search/publ/api`) for "prolly tree," "Merkle search
tree," "order-statistics tree distributed," "range query DHT," "authenticated range query,"
"authenticated skip list," "Merkle B-tree," "verkle tree," "authenticated multi-version index
blockchain," "authenticated data structures survey," "verifiable database survey 2024," and
"distributed authenticated dictionary" (exact-phrase and exact-title queries for "prolly tree" and
"Merkle search tree" each return exactly the one paper already in this corpus, confirming no DBLP-
indexed venue has published a second paper under either name). arXiv API (`export.arxiv.org/api`)
title and full-text search for the same terms plus "range-summarizable" (returns exactly
`AMPARORE-ARXIV-26`) and "content-addressed storage"; retrieved full text via `fetch-paper.py` for
two candidates surfaced this way that were not already in the corpus — `LIVINGDB-ARXIV-26` (arXiv
2605.00676) and `VTRQ-ARXIV-26` (arXiv 2608.21314) — both read in full before being cited above.
Crossref bibliographic search for "merkle search tree" filtered to publications from 2024 onward (79,771
total matches on the broad bibliographic query; the ranked top 15 titles inspected, none matching a
generalized secondary-index or range-query mechanism for content-addressed stores). Semantic Scholar
and OpenAlex searches were attempted but returned HTTP 429 (rate limit) and a billing error
respectively on every retry available within this session; DBLP, arXiv, and Crossref together
covered the venues and preprint servers most likely to carry this literature, so the gap is noted
rather than silently absent. No 2023-or-later survey or Systematization of Knowledge paper
specifically on secondary indexing or range queries over content-addressed or peer-to-peer stores was
found through any of the above; the most recent systematic treatment touching the underlying
mechanism family is Almeida's 2025 ACM Computing Surveys CRDT survey (`ALMEIDA-CSUR-25`), which does
not engage indexing or range queries at all and does not cite either the Merkle Search Tree or the
prolly tree paper.

---

