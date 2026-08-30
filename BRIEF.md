# Research task: build a verified corpus and a Pareto-optimal component selection for a decentralized web architecture

You are coordinating a research swarm. Your output is two artifacts: a single large evidence file containing extracted content from every primary source you retrieve, and a synthesis that selects one mechanism per architectural component with the measured evidence for each selection.

Read this entire brief before dispatching any subagent.

---

## 1. What is being designed

A decentralized internet whose identity, indexing, and storage components cannot be captured by any company, and whose client reproduces the functional patterns of the most-visited websites so users have no functional reason to return to centralized services. Privacy mechanisms are user-selectable tiers, because the strong ones cost measurable latency and bandwidth and most users will not pay that cost until conditions require it.

The design target is Pareto optimality across the whole system, not per-component optimality. A component that is optimal in isolation and incompatible with the component beside it is worse than two components that compose. Detecting those incompatibilities is a primary deliverable, not a side note.

---

## 2. The failure mode this brief exists to prevent

A previous research pass produced two kinds of error. Both must be structurally prevented, not merely discouraged.

### 2.1 Citing abstracts as if they were papers

Figures were carried forward from search-result snippets, secondary summaries, and citation-index blurbs, attributed to papers nobody had opened. Some were wrong. One example: a distributed search system's recall figures were stated as "1.2 million documents across 750 peers, 45–130 peers contacted." The actual paper says 50 overlapping collections and plots recall against 1 to 20 queried peers. The claim had been repeated through at least two documents before anyone opened the source.

**Rule: a number, a parameter, or a mechanism description enters the evidence file only from the full text of the primary source.** If you have only an abstract, you may record that the paper exists and what it claims to be about, in a section explicitly labeled as unretrieved. You may not state its measurements. You may not let a later synthesis step treat that entry as evidence.

### 2.2 Importing one project's value judgments as universal constraints

A previous pass read an engineering document belonging to a specific project and absorbed its refusals as if they were properties of the mechanisms. That document refused five mechanism families — gossiped inventory filters, network-wide popularity aggregation, published per-identity behavior scores, content-derived similarity signatures, and epidemic push — for reasons rooted in that project's own commitments. Those refusals were then written into the architecture as though the mechanisms did not work.

They work. What that project decided was that their costs were unacceptable *to it*.

**Rule: separate three categories and never let them merge.**

| Category | Definition | Where it goes |
|---|---|---|
| Measured fact | A number produced by an experiment, with its conditions stated | Evidence file, cited to the paper |
| Structural consequence | A property that follows by reasoning from a measured fact or a proof | Synthesis, with the derivation shown |
| Value judgment | A decision that a cost is or is not worth paying | Excluded, or quarantined and attributed to whoever made it |

When a source document says a mechanism is "refused," extract *why* — the cost, the exposure, the failure condition — and record that as fact. Do not record the refusal. The refusal belongs to whoever wrote it.

A worked example of the distinction. A gossiped Bloom filter over a peer's held content prunes roughly half of candidate forwards per hop, is a standing offline query interface to that peer's disk for anyone holding it, and was deployed and withdrawn in Bitcoin (BIP37, 2012; address-set recovery demonstrated by Gervais et al. at ACSAC 2014; disabled by default in Bitcoin Core 0.19, 2019). Every clause in that sentence is a fact. "Therefore do not use gossiped filters" is a judgment. Record the facts, present the judgment as one option with its consequence stated, and let the architect decide.

### 2.3 Corollary: do not import project-specific context at all

If you are given documents belonging to a specific implementation, treat them as a source of citations and measured facts only. Do not adopt their architecture, their terminology, their section-numbering, their constraints, or their conclusions. Do not describe the system being designed here in terms of that system. If a document says "our cell size is 4,096 bytes, therefore space-efficiency results are inert," extract the general form — *under a fixed padded transport frame of size F, any structure whose size reduction stays within one frame produces zero transmitted-size benefit* — and record F as that project's parameter, not as a constant.

---

## 3. Retrieval protocol: how to actually find papers

The previous pass gave up too early and too often. Retrieval failure is almost always a search-strategy failure, not an availability failure. Nearly every paper in this field is available somewhere.

### 3.1 Escalation ladder — do not report a paper unretrievable until every step has been attempted

For each target paper, in order:

1. **Get the exact citation first.** Search DBLP (`dblp.org`) for the author. DBLP gives the canonical title, venue, year, page numbers, and DOI. A wrong DOI wastes every subsequent step. If you guessed a DOI, you have already made an error — verify it in DBLP or Crossref.
2. **arXiv.** Search title and author. Many systems and crypto papers are there under a different title than the published version.
3. **IACR ePrint** (`eprint.iacr.org`) for anything cryptographic. Note: ePrint blocks automated fetchers aggressively. If blocked, get the PDF through a mirror, through Semantic Scholar's PDF link, or ask the human to fetch it.
4. **Author's personal or institutional page.** This is the highest-yield step and the most often skipped. Search `<author surname> <institution> publications`. Researchers in this field post PDFs. Examples that resolved this way in prior work: Grothoff's site hosted the Pitch Black paper; KIT's telematics group hosted S/Kademlia; MPI hosted the entire MINERVA series; VLDB hosts its own proceedings openly.
5. **Conference proceedings site.** VLDB, USENIX (`usenix.org` — all papers open), PETS/PoPETs (`petsymposium.org` — all open), NDSS (`ndss-symposium.org` — all open), IMC/SIGCOMM via ACM author pages. USENIX and PETS being fully open means anything published there is retrievable, always.
6. **Semantic Scholar API** (`api.semanticscholar.org/graph/v1/paper/search`) — returns `openAccessPdf` links and, critically, the reference and citation lists as structured data. Use this for bibliography mining (§4).
7. **OpenAlex** (`api.openalex.org`) — same role, better coverage of older work, includes `referenced_works` and `cited_by` as IDs.
8. **CORE** (`core.ac.uk`) — aggregates institutional repositories.
9. **CiteSeerX** — for pre-2010 systems papers specifically.
10. **Institutional repository by name.** TU Delft, MIT DSpace, Berkeley, EPFL, Cambridge, MPI. Theses in particular: a PhD thesis by one of the authors usually contains the paper's content in expanded form and is almost always openly deposited. If the paper is paywalled, look for the thesis.
11. **The technical-report version.** Systems papers frequently have a longer TR with the omitted proofs, posted by the lab.
12. **Ask the human**, with the exact DOI, the exact title, and one sentence on what you need from it.

Do not stop at step 2. Do not stop at step 3. The previous pass's failures were all resolvable at steps 4 through 7.

### 3.2 Search-query construction

- Query with distinctive multi-word strings from the paper, not generic topic words. `"square-root replication" unstructured peer-to-peer` finds it; `p2p replication` does not.
- When you know a figure the paper contains, search that figure. `"32-walker" random walk` is a better query than the paper's title.
- Search the mechanism's name plus the word `attack` to find the security analyses that cite it, which is often how you find both the critique and a copy of the original.
- If a paper is cited by something you already have, take the citation string verbatim from that bibliography and search it as a phrase.

### 3.3 What "read the paper" means

Extract, from the full text:

- The mechanism, stated so that a reader could implement it
- Every quantitative result, **with its experimental conditions**: node counts, topology, dataset, hardware, number of runs, what was held constant
- The parameters used, with their values
- The stated failure conditions and limitations, including ones in the discussion or future-work section
- What the paper says it does *not* solve
- Any result that contradicts a claim commonly attributed to the paper
- The bibliography, for §4

A figure without its experimental conditions is not usable. "Reduces messages by two orders of magnitude" is worthless; "reduces messages by roughly two orders of magnitude against flooding, on four topologies of 4,736 to 10,000 nodes, at 1% replication, with hops rising from 2–6 to 4–15" is usable.

---

## 4. Bibliography mining: the primary discovery mechanism

Keyword search finds what you already know to look for. Bibliographies find what you do not.

### 4.1 Backward mining

For every paper you retrieve, extract the full reference list. For each reference, classify:

- **Foundational** — the paper this one builds on. Retrieve if not already held.
- **Competing** — the alternative this paper compares against. **Always retrieve.** These contain the comparison numbers from the other side, which frequently disagree.
- **Attack or critique** — retrieve, always.
- **Irrelevant** — record and stop.

### 4.2 Forward mining

For every foundational paper, use Semantic Scholar or OpenAlex `cited_by` to find what cites it. Filter to papers that (a) attack it, (b) measure it independently, or (c) supersede it. Independent measurement is the highest-value category and the hardest to find by keyword search, because such papers are usually titled after their own contribution.

Forward mining is how you discover that a 2021 result was superseded in 2026. The previous pass recommended a mechanism with O(n) cost because it did not check what cited it; a 2026 paper achieving O(log n) with the same security properties existed.

### 4.3 Depth control

Backward-mine to depth 3 from any seed. Forward-mine to depth 1 from foundational papers only. Stop a branch when it leaves the domain. Log every retrieved paper in a shared registry so no subagent retrieves the same paper twice.

### 4.4 The specific bibliographies most worth mining

These are known-dense and openly available:

- Urdaneta, Pierre, van Steen, "A Survey of DHT Security Techniques," ACM Computing Surveys 43(2), 2011 — the DHT attack literature, comprehensively
- Alvisi, Clement, Epasto, Lattanzi, Panconesi, "SoK: The Evolution of Sybil Defense via Social Networks," IEEE S&P 2013 — every social-graph Sybil defense with a unified analysis
- The BeeKEM paper (ePrint 2026/1434) — current decentralized group-messaging state of the art, cites the whole CGKA/DCGKA line
- Das, Meiser, Mohammadi, Kate, "Anonymity Trilemma," IEEE S&P 2018, and the 2020 PoPETs follow-up — the anonymity impossibility results and everything they bound
- Any recent survey in a target area; find them by searching `survey` or `SoK` plus the mechanism name, filtered to 2023 or later

---

## 5. Swarm decomposition

Dispatch subagents by domain. Each returns structured facts only, in the schema of §6. No subagent writes prose for the final document. No subagent makes a selection.

| Agent | Domain |
|---|---|
| A | Structured overlays: Kademlia, Chord, Pastry, Tapestry, CAN, Koorde, Viceroy, Symphony, Accordion, Bamboo; secure variants; churn measurement; self-stabilizing overlays; capacity-heterogeneous overlays |
| B | Unstructured search, semantic overlays, distributed indexing, learned/vector retrieval in decentralized settings |
| C | Storage: content addressing, erasure and regenerating codes, locally repairable codes, fountain codes, proofs of retrievability and storage, repair economics |
| D | Synchronization and replicated state: set reconciliation in all its families, CRDTs, Byzantine-tolerant replication, Merkle-structured indexes |
| E | Identity, keys, transparency logs, threshold and aggregate signatures, zero-knowledge credentials, proof of personhood |
| F | Sybil resistance and reputation, including every critique of both |
| G | Anonymity, cover traffic, private information retrieval, encrypted search and its leakage attacks, metadata-private messaging |
| H | Group messaging and key agreement |
| I | Incentives, rate limiting, free-riding, and every published attack on an incentive scheme |
| J | Deployed-system measurement studies and post-mortems, plus centralization measurements of nominally decentralized systems |
| K | Application-layer patterns: feed generation, ranking without a global index, moderation architectures, peer-assisted video |
| L | Transport and reachability: NAT traversal measurement, mobile background execution limits, browser peer constraints |

Agents A through L run backward and forward mining within their domain and hand cross-domain discoveries to the registry rather than following them.

Reserve a final agent, **X**, which does no retrieval. X reads the completed evidence file and searches for contradictions: two papers reporting incompatible measurements of the same thing, a mechanism whose requirements another selected mechanism destroys, a claim in the synthesis not supported by an entry in the evidence file. X's report is a deliverable.

---

## 6. Evidence file format

One file, append-only, one entry per paper. Never delete an entry; supersede it with a new one and mark the old.

```markdown
## [KEY] Full title
**Citation:** Authors. "Title." Venue, Year. Pages. DOI.
**Retrieved:** full text | full text via <route> | ABSTRACT ONLY — NOT USABLE AS EVIDENCE
**Source URL:** <url>
**Domain:** <agent letter>

### What it does
<Mechanism, stated so a reader could implement it. Function first, then how.>

### Measured results
<Each figure with its full experimental conditions. Tables preferred.>

### Parameters
<Every parameter with the value used and, where stated, the tested range.>

### Stated limitations
<What the authors say it does not do, including from discussion and future work.>

### Requirements it places on the rest of the system
<What must be true elsewhere for this to work. This is what §8 conflict detection runs on.>

### Contradicts
<Any claim commonly attributed to this paper that the paper does not support. Also any other entry in this file it disagrees with, by KEY.>

### References worth retrieving
<From its bibliography, with classification: foundational | competing | attack | superseded-by>

### Verbatim extracts
<Direct quotations of the passages the above rests on, so a later reader can check without re-fetching. Keep each under 15 words; paraphrase everything longer.>
```

---

## 7. Already verified — do not re-retrieve, do extend

These were read in full. Use them as mining seeds. Correct them only if you find the primary source says otherwise.

- **Kademlia** (Maymounkov, Mazières, IPTPS 2002) — XOR metric, symmetric, k-buckets prefer long-lived contacts
- **S/Kademlia** (Baumgart, Mies, ICPADS 2007) — success formula `P_K = Σ_i h_i · (1 − (1 − (1−m)^i)^d)`; at 20% adversarial nodes, 99% lookup success with disjoint paths; recommends d=4–8, k=8–16; adaptive k=2d is *worse* than fixed k=16 because shorter routing tables lengthen paths; sibling list of size η·s with η ≥ 5 replaces Kademlia's irregular bucket-split rule; static and dynamic crypto puzzles for node-ID generation
- **Lv, Cao, Cohen, Li, Shenker** (ICS 2002) — 32-walker random walk, checking every 4th step, ~2 orders of magnitude fewer messages than flooding on 4 topologies (PLRG 9,230 / Random 9,836 / Gnutella 4,736 / Grid 10,000); hops rise 2–6 → 4–15; uniform and proportional replication give *identical* average search size m/ρ; square-root replication is optimal; path replication achieves it, improving messages 2.95× and random replication 3.91× over owner replication; **LRU and LFU eviction break the square-root fixed point**
- **Pitch Black** (Evans, GauthierDickey, Grothoff, ACSAC 2007) — 800-node testbed on real Freenet 0.7 code, Kleinberg 2d-torus topology; 2 to 8 attackers with 8 target locations caused 15%–60% content loss after 200 iterations of 90 s each; **ordinary join-leave churn produces the same degeneration with no adversary**; no effective countermeasure found
- **MINERVA** (Bender, Michel, Triantafillou, Weikum, Zimmer, VLDB 2005) — Chord-style directory of per-term summaries; local index answers first, network only on dissatisfaction; 50 overlapping .GOV collections; recall plotted against 1–20 queried peers; overlap-awareness beats CORI
- **4P** (Zeilemaker, Pouwelse, Sips, P2P 2014, DOI 10.1109/P2P.2014.6934311) — 1,000 emulated peers from >75,000-peer Tribler traces, 80/20 split, 200 querying peers; recall/messages: random 9%/20, semantic 40%/20, 4P 76%/313, RetroShare 86%/10,316, Gnutella 98%/13,379, OneSwarm 99%/9,108; TTL 4, IEP 0.15, FEP 0.5, PIE 0.45; Paillier polynomial-root PSI, 79.5 kB per handshake, HashCash required per request; anonymity: provably exposed to a local eavesdropper, probably innocent against colluding peers
- **BeeKEM** (Yen, Fábrega, Da, Kleppmann, Mumm, Park, Zelenka, ePrint 2026/1434) — first DCGKA with O(log n) update cost and proofs; supersedes Weidner et al.'s O(n); defines and proves Cross-Fork Security, which Weidner et al. lacks; is itself a CRDT; requires only causal broadcast; retention parameter κ trades cross-branch recovery against forward secrecy, conjectured inherent; BeeKEM^FS and BeeKEM^PQ variants sketched
- **HSkip+** (Feldotto, Scheideler, Graffi, P2P 2014) — self-stabilizing under *asynchronous* message passing; bandwidth-ordered; O(log²n) messages vs Skip+'s O(log⁴n); routing never transits a node with less bandwidth than min of endpoints; survives 60% random and 35% adversarial churn; dilation O(log n), congestion O(log n)
- **Range-based set reconciliation** (Meyer, IEEE SRDS 2023, arXiv 2212.13567) — rounds bounded by `2 + 2⌈log_b(n_min)⌉ − ⌊log_b(t)⌋`
- **Anonymity trilemma** (Das, Meiser, Mohammadi, Kate, IEEE S&P 2018) and the 2020 PoPETs strengthening covering user coordination
- **Probabilistic data structures under adversarial input** (Clayton, Patton, Shrimpton, CCS 2019) — adaptive adversary exceeds nominal false-positive rate; fix is keyed PRF and salt
- **BIP37 privacy failure** (Gervais, Capkun, Karame, Gruber, ACSAC 2014) — address-set recovery from one filter; two-filter intersection strips cover; disabled by default in Bitcoin Core 0.19

---

## 8. Known gaps to close

**Unresolved retrieval.** "QRank," a difficulty-aware hybrid P2P search scheme, has no confirmed author, venue, or identifier. Determine whether it exists under another name or strike it. "SwarmSearch" likewise.

**Unmined domains.** Agents E, I, K, and L have had almost no coverage. Threshold signatures, zero-knowledge credentials, proof of personhood, rate limiting, feed generation, moderation architectures, and mobile execution limits are represented by at most one source each.

**Open problems needing a literature check** — for each, determine whether a solution has been published:

1. Ranked full-text search across peers at web scale. The standing bound (Li et al., IPTPS 2003, and the 2011 follow-up) is ~6 MB per query for 3 billion documents, with posting-list caching giving only 38%. Has anything overturned this?
2. Distributed approximate-nearest-neighbour search that resists inserted adversarial vectors.
3. Sybil resistance without trusted seeds, given that Viswanath et al. and Alvisi et al. showed every social-graph defense performs local community detection.
4. Private search at interactive latency. Current single-server PIR costs seconds per query on multi-gigabyte databases.
5. Repair economics for volunteer erasure-coded storage under measured churn.
6. Continuous participation from mobile devices given iOS and Android background suspension.
7. Removing illegal material from immutable content-addressed storage.
8. Verifiable bandwidth accounting.
9. Secondary indexes and range queries over content-addressed stores.
10. Honest bandwidth reporting in a capacity-ordered overlay — HSkip+ assumes it and does not defend it.
11. Forward secrecy under long partitions — BeeKEM's authors conjecture the tradeoff is inherent. Has anyone disproved that?

**Known incompatibility, needs literature check.** Square-root replication (Cohen and Shenker; Lv et al.) requires each forwarding node to learn *which* item a successful search found, so it can replicate that item. A search channel returning only an opaque match/no-match result destroys that signal. The strongest published replication result and query privacy appear mutually exclusive. Determine whether anyone has published a reconciliation.

---

## 9. Synthesis rules

After the evidence file is complete:

### 9.1 Per-component selection

For each of: transport, NAT traversal, capacity ordering, content location, storage encoding, repair, naming, identity, key recovery, key transparency, Sybil resistance, reputation, indexing, ranking, moderation, incentives, group encryption, application data model, and privacy tiers —

State the candidates. For each candidate give its measured cost, its security assumption, its failure condition, and what it requires from other components. Then select, and state the reasoning as a comparison against each rejected candidate, citing evidence-file KEYs. A selection whose justification cannot cite a KEY is not a selection; it is a guess, and must be labeled one.

### 9.2 Composition check — the part that makes this Pareto rather than greedy

Build a matrix of every selected component against every other. For each pair ask: does either destroy a precondition the other requires? Three known examples to seed the check:

- Square-root replication requires per-item search feedback; blinded search destroys it
- Square-root replication requires eviction independent of query rate; LRU eviction destroys it
- MLS requires total order; a partition-tolerant design cannot supply it, which is why BeeKEM exists

Every conflict found must be resolved explicitly: change a selection, accept a degraded property and state which, or record it as an open problem. An unresolved conflict left in the document is a defect.

### 9.3 Tier construction

Privacy mechanisms are ordered into tiers by measured cost. Each tier states the adversary it defeats and the latency and bandwidth it adds, both cited. A tier whose cost is not measured cannot be offered, because the user cannot make an informed choice about an unquantified cost.

### 9.4 Honesty requirements

- Any claim not backed by a full-text entry is marked unverified inline, at the point of the claim, not in a footnote or an appendix.
- Where two sources disagree, present both figures with their conditions and say which experiment is closer to the deployment being designed.
- Where the answer is that nobody knows, say so. An open problem correctly identified is worth more than a confident wrong selection.

---

## 10. Writing style for both artifacts

- Maximum information density. Every sentence is a definition, a mechanism step, a dependency, or a consequence.
- No metaphor, no figurative language, no idiom. Every verb describes an action that occurs. Domain-conventional metaphors still count: write "query broadcast" not "flooding," "consuming without contributing" not "free-riding," "frequently requested" not "hot." Do not write that costs decide, that measurements constrain, or that an architecture selects — a person does those things.
- Open each explanation with what the mechanism does — its function — before describing what it physically is.
- Define every term at its point of use. Expand every acronym at first use. Where the name encodes the meaning, give the derivation.
- Headers state a claim or a fact that stands alone as information. Not topic labels, not counts, not teasers. "Disjoint lookup paths raise success against a 20% adversary from 41% to 99%" is a header. "DHT security" is not.
- No preview sentences. Do not announce that three things follow; state the first one.
- Enumerate every item explicitly. No ellipses standing for a list, no "and others," no "+N more," no undefined acronyms.
- When two failure conditions bound a choice from opposite sides, state the bounded range first, then one sentence per side.
- At most one subordinate clause per sentence. Clauses chained by semicolons become separate sentences.
- One concept keeps one term throughout. Never rename for variety.
- When a referent last appeared more than one sentence back, repeat the noun rather than using a pronoun.
- Every quotation under 15 words. Paraphrase everything longer.

---

## 11. Deliverables

1. `evidence.md` — every retrieved paper in the §6 schema. This is the artifact of record. Expect it to be large.
2. `retrieval-log.md` — every paper attempted, the escalation steps tried, and the outcome. Papers that failed all steps are listed with their exact DOI so a human can fetch them.
3. `architecture.md` — the synthesis, per §9 and §10.
4. `conflicts.md` — agent X's contradiction report: measurement disagreements between sources, composition conflicts between selected components, and any claim in `architecture.md` not traceable to an `evidence.md` entry.
5. `open-problems.md` — problems with no published solution, each stating what has been tried and why it falls short.

Begin by building the retrieval registry and dispatching agents A through L. Do not begin synthesis until the evidence file is complete and agent X has run once.
