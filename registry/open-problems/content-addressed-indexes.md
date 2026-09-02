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
