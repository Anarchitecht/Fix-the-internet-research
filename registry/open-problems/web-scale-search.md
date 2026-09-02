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
