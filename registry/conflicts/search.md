# Search family: conflicts and disagreements

Scope: messages per query, recall fraction, bytes per query, posting-list
intersection cost, caching benefit, random-walk versus query-broadcast cost,
semantic-overlay recall, and index-size figures. Entries read in full:
`LI-IPTPS-03`, `ASTHANA-ICTIR-11`, `ASTHANA-PHD-14`, `COX-ICTIR-09`,
`COX-ECIR-10`, `RICHARDSON-ECIR-13`, `RICHARDSON-SIGIR-14`, `COHEN-SIGCOMM-02`,
`CHEN-TPDS-09`, `MICHEL-VLDB-05`, `REYNOLDS-MIDDLEWARE-03`, `TANG-CCR-03`,
`CRESPO-AP2PC-04`, `NEAGUE-ARXIV-25`, `HERRMANN-P2P-14`, `LOO-IPTPS-04`,
`YANG-ICDE-03`, `STRIBLING-IPTPS-05`, `MAYOR-P2P-13`, `ADAMS-ARXIV-25`,
`ZHOU-EPRINT-24`, `JEGOU-TPAMI-11`, `TERPSTRA-SIGCOMM-07` (retrieval mismatch,
noted below), and `DANEZIS-WALRUS-25` for one cross-family precondition check.

## 1. The 6-megabytes-per-query bound: nothing in the corpus overturns it, and one framing risk

`LI-IPTPS-03` states two separate baseline costs, for two separate
architectures, over a 3-billion-document, 1-megabyte-per-query target: naive
partition-by-document (query broadcast to every peer holding a shard) costs 6
megabytes per query; naive partition-by-keyword (a distributed hash table
routes each query term to the peer holding that term's posting list, which
intersects and ranks) costs 530 megabytes per query for a two-term query. The
paper's own optimization sequence — caching (38% reduction), precomputed
intersections, Bloom-filter and gap compression, semantic clustering,
incremental ranked retrieval — is applied only to the partition-by-keyword
architecture and its 530-megabyte baseline. Caching never touches the
6-megabyte partition-by-document baseline, because that architecture has no
posting lists to cache; it broadcasts the query itself. A synthesis that
writes "the 6-megabyte bound, reduced 38% by caching" attributes an
optimization to a baseline it was never applied to. `LI-IPTPS-03`'s own
combined-optimization result is a 75x reduction on the 530-megabyte baseline,
leaving cost about 7x above the 1-megabyte target — not a reduction of the
6-megabyte figure.

No entry in this family reports a lower cost than `LI-IPTPS-03`'s bound under
matching conditions (a full-text, ranked, multi-term query over a
multi-billion-document collection, keyword-partitioned across the network).
Every lower figure in the corpus changes at least one of those conditions:

- `ASTHANA-ICTIR-11` reports 1.0-3.6 megabytes per query at 90% top-1
  accuracy, but over a different architecture (broadcast to z randomly
  sampled peers, each holding a locally complete index of its own document
  share, no DHT keyword partitioning) and a different per-node storage
  assumption: 10 million documents per node (0.1% of a 10-billion-document
  collection), roughly 200 times the per-node share `COX-ICTIR-09`'s
  comparable worked example uses (below). `ASTHANA-ICTIR-11`'s own
  "Contradicts" section states directly that its 1.0-3.6 megabyte figures are
  not the same result as `LI-IPTPS-03`'s 6-megabyte bound.
- `REYNOLDS-MIDDLEWARE-03` reports under 1 kilobyte per query, but over a
  105,593-document, 1.17-million-word collection — four to five orders of
  magnitude smaller than the 3-billion-document target — and boolean-AND
  keyword matching with no relevance ranking on the compressed path. The
  entry's own "Contradicts" section states this directly.
- `MICHEL-VLDB-05` (KLEE) reports roughly 57 kilobytes per query for its
  best-performing variant (2,845,225 bytes over a 50-query batch), on a
  1.25-million-document GOV collection (8 gigabytes of index-list data) —
  three orders of magnitude smaller than the 3-billion-document target, and
  answering top-k ranked-attribute queries rather than full-text search.
- `STRIBLING-IPTPS-05` (OverCite) calculates roughly 34 kilobytes of
  per-query overhead (8.5 gigabytes/day over 250,000 searches/day, at
  n=100, k=20 partitions) on the production CiteSeer collection (715,000
  papers), and reaches that figure specifically by choosing document-based
  index partitioning over keyword-based partitioning, stating this choice is
  made "to avoid keyword-partitioning's join cost" — the cost `LI-IPTPS-03`
  measures. Avoiding the compared cost by choosing a different architecture
  is not a reduction of it.
- `LOO-IPTPS-04` reports 850 bytes of routing cost per query when its
  distributed join uses Join Indexes, on a 700,000-file sample drawn from a
  live Gnutella crawl — again several orders of magnitude below the
  3-billion-document target, and the paper's own selective-publishing
  mechanism indexes only items that already showed up in a small query
  result set, not the full collection `LI-IPTPS-03` assumes indexed.

No paper in this family runs a keyword-partitioned, full-text, ranked search
over a collection within two orders of magnitude of 3 billion documents. The
corpus therefore contains no measurement that confirms or overturns
`LI-IPTPS-03`'s bound at its own scale; every other figure changes scale,
architecture, or query semantics, usually several of the three at once. The
"2011 follow-up" `BRIEF.md` section 8 names alongside `LI-IPTPS-03` is not in
this corpus: `LI-INFOCOM-05` (2005, DHT performance-versus-cost under churn)
and `LI-EPRINT-25` (2025, Ethereum network measurement) are the only
`LI-*` entries retrieved, and neither is a P2P web-search feasibility
follow-up. Retrieving the actual follow-up, if one exists, is unfinished
work, not a corpus finding.

`TERPSTRA-SIGCOMM-07` (BubbleStorm, the other paper this family's brief item
names for random-walk-versus-broadcast and exhaustive probabilistic search)
is a retrieval mismatch: the file on disk is a Technische Universitat
Darmstadt technical report containing only analytic proofs, not the SIGCOMM
2007 paper's million-peer churn simulation. No BubbleStorm measurement is
usable evidence from that entry. `COX-ICTIR-09` cross-checks BubbleStorm's
own published match-probability formula (1 − e^(−k'g/K)) against its own PAC
estimate under matched parameters (K=1,000,000, k'=10,000) and gets the same
value, 0.03, from both — a formula-level agreement, not a retrieval of
BubbleStorm's simulation results.

## 2. Measurement disagreement: PAC-search accuracy at web scale, 780-2,750 nodes queried against 340,000

`ASTHANA-ICTIR-11` (Asthana, Fu, Cox, ICTIR 2011) states that reaching 90%
top-1 retrieval accuracy over a 10-billion-document collection needs between
780 and 2,750 of 1,000,000 nodes queried, depending on replication strategy
and the query-popularity exponent, at a per-node storage share of 10 million
documents (0.1% of the collection). `COX-ICTIR-09` (Cox, Fu, Hansen, ICTIR
2009 — Asthana's own cited foundational source, same lead author and one
shared co-author) works a peer-to-peer example with K=1,000,000 machines,
N=17 billion documents, and a per-node storage share of 50,000 documents
(1-gigabyte capacity, 20-kilobyte documents), and derives 63% retrieval
overlap only at 340,000 nodes queried — two orders of magnitude more than
`ASTHANA-ICTIR-11`'s figure, for a lower accuracy target (63% overlap-with-
deterministic-result versus 90% top-1 accuracy) and a comparable collection
size (17 billion versus 10 billion documents).

Both papers use the same underlying probability model (P = 1 −
(1 − r/n)^z, or the equivalent overlap form) and the same collection-size
order of magnitude. This is a genuine difference in measured outcome, not a
difference in what was measured — both compute nodes-queried for a target
accuracy over a large document collection under random sampling. The
difference traces to one input the two papers set roughly 200 times apart:
per-node storage share (10 million documents in `ASTHANA-ICTIR-11` against
50,000 in `COX-ICTIR-09`'s worked example). `COX-ICTIR-09`'s own text states
the 0.03-overlap result is attributable to "insufficient per-machine storage
capacity relative to collection size," and separately computes that raising
per-machine capacity to 340 gigabytes (Asthana's order of magnitude) restores
63% accuracy at the smaller fan-out — which the two papers' own numbers
corroborate. A synthesis choosing a target per-node storage budget must use
that paper's own accuracy-versus-nodes-queried curve, not the other's:
`ASTHANA-ICTIR-11`'s low node-count figures assume gigabyte-scale per-node
storage across a million-node network; `COX-ICTIR-09`'s peer-to-peer worked
example assumes commodity (1-gigabyte) storage and finds three orders of
magnitude more nodes must be queried to compensate.

## 3. Recall and accuracy figures do not share one scale across this corpus

Every "recall," "accuracy," or "overlap" figure in this family is measured
against a different baseline, a different corpus, and a different peer count,
and the figures are not interchangeable:

| Entry | Figure | Corpus | Peers/nodes | What the number measures |
|---|---|---|---|---|
| `ASTHANA-ICTIR-11` | 90% top-1 accuracy | 10B synthetic documents | 780-2,750 of 1,000,000 queried | overlap with an exhaustive top-1 result, PAC model |
| `COX-ICTIR-09` | 63% overlap | 17B synthetic documents | 340,000 of 1,000,000 queried | overlap with a deterministic top-r list |
| `COX-ECIR-10` | 67%→96% over 10 iterations | TREC-8, ~500,000 documents | 1,000 of 300,000 queried per iteration | BM25-ranked accuracy under a centralized node-caching coordinator |
| `MICHEL-VLDB-05` | 90% (GOV) / 79-83% (XGOV) recall@20 | 1.25M-document GOV crawl | up to 5 (GOV) / 18 (XGOV) cohort peers | approximate top-k recall against exact TA/NRA |
| `TANG-CCR-03` (pSearch) | 95% accuracy visiting 0.4-1.0% of nodes | TREC, 528,543 documents | 1,000-10,000 network nodes | overlap with non-distributed LSI results |
| `CRESPO-AP2PC-04` | 93% average maximum recall | 1,800-node Napster crawl | flat overlay, semantic-overlay routing | fraction of matching documents found, Layered SONs |
| `NEAGUE-ARXIV-25` (Semantica) | 12.75% two-hop document-retrieval rate | AOL4PS, 6,978 users | chain-hop, mean ~208 known-users per peer | retrieval rate under an assumed-perfect local search |
| `RICHARDSON-SIGIR-14` | ~0.9 theoretical, degrading under attack | WT10g, 1.69M documents | n=10,000, z swept 1-10,000 | PAC accuracy under adversarial global-statistics estimation |
| `ADAMS-ARXIV-25` | 90.8% recall@5 / 71.9% recall@200 | 50B-vector Bing production index | thousands of trusted, co-located machines | approximate-nearest-neighbor recall, single-operator cluster |
| `ZHOU-EPRINT-24` (Pacmann) | ~90% of a non-private baseline's recall | 100M-vector SIFT / 3.2M-document MS-MARCO | single client, single server (PIR) | private ANN recall relative to NGT, semi-honest server |

No two rows in this table measure the same quantity under comparable
conditions. Three distinct notions of "accuracy" appear (overlap with a
deterministic/exhaustive baseline; ranked recall against ground truth;
approximate-nearest-neighbor recall against an exact non-private baseline),
over collections spanning four orders of magnitude (528,543 to 50 billion),
under peer counts spanning six orders of magnitude (a handful of cohort
peers to a million-node network). None of this is a disagreement — each
figure is internally consistent with its own paper — but averaging or
ranking them against each other, as a synthesis table might be tempted to
do, would compare unlike quantities. The one instance where two papers
report the same quantity under close-enough conditions to compare directly
is Section 2 above.

`MINERVA` (Bender, Michel, Triantafillou, Weikum, Zimmer, VLDB 2005),
the recall-versus-peers-queried result `BRIEF.md` section 7 lists as an
already-verified seed for this family, has no entry in
`registry/evidence/`. It is cited as foundational by three retrieved papers
in this batch (`ASTHANA-PHD-14`, and by name in the brief itself) but its own
recall figures are not present in the evidence corpus and cannot be added to
the table above or checked against any other entry here. A synthesis citing
MINERVA's recall-versus-peers curve is citing a figure this corpus does not
carry.

## 4. Caching-benefit figures measure different mechanisms at different scales

`LI-IPTPS-03` reports posting-list caching reduces average per-query
communication cost by 38% (a 1.5x factor), on an 81,000-query trace against a
1.7-million-page mit.edu index; the paper attributes the modest gain to most
trace queries appearing only once, so a cached posting list is rarely reused.
`REYNOLDS-MIDDLEWARE-03` reports caching gives more than a 50% reduction in
total bytes transmitted per query, on a 95,409-query IRCache trace against a
105,593-document collection. Both cache the same kind of object (a fetched
posting list or Bloom filter, kept so a repeated query for the same keyword
pair skips a network round trip), so the two figures are comparable in
mechanism. The gap (38% against >50%) is not a disagreement about how well
caching works; it is a difference in how repetitive the two traces are —
`LI-IPTPS-03` states its own trace's low reuse rate as the reason for the
smaller gain, and neither paper claims a general caching-benefit constant
independent of query-repetition structure. `COX-ECIR-10` also reports a
caching-like gain (67% to 96% accuracy over 10 repeated iterations of the
same query), but this "node caching" retains which computers answered a
query best, not a posting list or filter, and the figure is an accuracy gain
under a centralized coordinator, not a bandwidth reduction — a different
mechanism and a different measured quantity from the other two, not a third
data point on the same scale.

## 5. Destroyed preconditions

### 5.1 Square-root replication's "which item was found" signal, destroyed by search that hides it — a concrete instance, not a reconciliation

`COHEN-SIGCOMM-02` proves square-root replication minimizes expected search
size, and states directly that path replication and sibling-number memory
"require the requesting node, after a successful search, to know which item
was found," so the finder can create new copies of that specific item.
`RICHARDSON-ECIR-13` extends this requirement: its rank-aware replication
policies compute a per-document weighted retrieval rate that needs not only
the found item's identity but its rank position in the returned list, a
strictly stronger requirement than plain identity.

`ZHOU-EPRINT-24` (Pacmann) is a concrete, published search mechanism that
removes exactly this signal from every node capable of acting as a
forwarder. Its private-information-retrieval-based approximate-nearest-
neighbor search is built so "the server never sees which vertex indices are
fetched" — the paper's own stated design goal is that the server "cannot
infer the query's topic from access patterns." A server in Pacmann's role is
architecturally the forwarding/storage node in a P2P deployment; under
Pacmann's own privacy guarantee, that node never learns which item a search
found, by construction, regardless of how the client-side result is used.
This is the search channel `BRIEF.md` section 8's closing item asks whether
anyone has reconciled with square-root replication — found here as a
concrete, deployed instance of the conflict, not a reconciliation of it.
`ZHOU-EPRINT-24` does not attempt replication at all (its own stated
limitations list no support for database insertion or deletion after
preprocessing), so it offers no answer to how a system might replicate a
popular item while keeping this privacy property; it only confirms the
conflict extends from generic "match/no-match" search channels to a
published approximate-nearest-neighbor construction.

### 5.2 DistributedANN's trusted-operator requirement, destroyed by Byzantine-tolerant storage

`ADAMS-ARXIV-25` (DistributedANN) states its near-data node-scoring service —
the mechanism responsible for its bandwidth and IO advantages over
partitioned indices — requires the operator to co-locate scoring computation
with every storage host, and states this directly: "a system without control
over storage-host code placement (as in an untrusted peer storage layer)
could not deploy the near-data scoring service as described." Its own threat
model section confirms the deployment is a single-operator managed cluster
with no defense against a storage host returning corrupted data or false
distance scores. `DANEZIS-WALRUS-25` (Walrus) is a storage design built for
the opposite assumption: it tolerates up to n/3 Byzantine (malicious)
storage nodes by construction. A system that selects DistributedANN's
near-data scoring mechanism for vector search and a Byzantine-tolerant,
untrusted peer storage layer for content storage cannot deploy both as
published — the search mechanism assumes exactly the single-operator code-
placement control the storage mechanism's threat model exists to avoid
needing.

### 5.3 Two requirements flagged for the composition check, not independently confirmed destroyed

`CHEN-TPDS-09` (QRank) states its difficulty-aware routing requires "a small
subset of nodes ... chosen by the system as long-uptime, server-like" to form
a structured super-peer tier, and states a flat, single-tier unstructured
network "has no natural candidate for the structured-super-peer role the
paper's design depends on." Whether a selected capacity-ordering mechanism
(for example `HSkip+`, already a corpus seed) supplies that candidate subset
is a composition question for whichever agent covers capacity ordering, not
one this family's evidence answers alone.

`RICHARDSON-SIGIR-14` requires every node to index the same fixed document
count rho, uniformly at random, so that no node has disproportionate
influence over its adversarial global-statistics defense; the paper states
directly that a higher-capacity node split into multiple rho-sized virtual
nodes "must be defended against as a Sybil attack using a mechanism outside
the scope of this paper." Whether a selected Sybil-resistance mechanism
supplies that defense is a question for whichever agent covers Sybil
resistance.

## 6. Internal inconsistency: Pacmann's optimization-stack figure, as recorded, does not match its own quoted text

The `ZHOU-EPRINT-24` evidence entry's own narrative states the paper's three
search optimizations (beam search, fast starting, batched PIR) together give
"a 76% reduction in computation and a near-70% reduction in end-to-end
latency." The same entry's verbatim-extract section quotes the paper
directly as reporting "up to 62% reduction in computation time and 22%
reduction in overall latency." These are two different figures for what the
entry presents as the same result. The verbatim quote is the higher-
confidence source (direct quotation, marked as such); the narrative figure
is the extracting agent's paraphrase and is not separately sourced to a page
or table in the entry. A synthesis citing Pacmann's optimization-stack
benefit should cite the quoted 62%/22% figures and flag the entry's own
narrative figure for a re-check against the primary source before either
number is relied on for a selection decision.

## 7. Unsupported attributions: none found in this family

No entry in this batch attributes a figure or property to another retrieved
paper in a way its own text contradicts. Two candidate cases were checked and
found unconfirmable rather than unsupported: `NEAGUE-ARXIV-25` cites Tang,
Xu, and Dwarkadas (SIGCOMM 2003) for a claim of "low latency and high
accuracy... comparable to centralized approaches" and flags the claim itself
as "worth checking directly" — that paper is a different Tang-led paper from
`TANG-CCR-03` (which is Tang, Xu, and Mahalingam) and is not in this corpus,
so the attribution cannot be checked either way. `CHEN-TPDS-09` reports GAB's
(Zaharia and Keshav's) own stated improvements over a third system as
background; GAB itself is not separately retrieved in this corpus, so that
figure is also unconfirmable rather than confirmed wrong. Neither is reported
as a finding.
