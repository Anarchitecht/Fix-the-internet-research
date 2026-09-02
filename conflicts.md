# Conflicts

Three kinds, kept separate.

**Measurement disagreement.** Two papers report incompatible numbers for the same quantity. Both
figures appear with their experimental conditions, and the entry states which experiment is closer to
the system being designed.

**Destroyed precondition.** One selected component requires something another selected component
removes. Each entry states the requirement, the removal, and the resolution: a changed selection, an
accepted degradation with the degraded property stated, or a new open problem.

**Unsupported claim.** A statement in `architecture.md` that no `evidence.md` entry supports. Each
one is a defect until it is either traced to an entry or labeled a guess at the point it is made.

The composition check that fills the destroyed-precondition section runs after the evidence file is
complete. What follows is from the extraction pass, which reports a disagreement whenever one agent
reading one paper finds a figure that another paper in the corpus contradicts.

---

## Measurement disagreements

### Cloud-hosted share of IPFS DHT nodes: 79.6% against under 3%

Baldüf and colleagues (IMC 2023) report 79.6% of IPFS distributed-hash-table nodes hosted on cloud
providers, from 101 crawls run between 2023-04-18 and 2023-05-26, counting unique nodes averaged over
crawls. Trautwein and colleagues (ACM SIGCOMM 2022) are reported by that same paper as finding under
3%. Baldüf re-derives 39.9% on their own dataset using the 2022 paper's global-unique-IP counting
method, and attributes the whole remaining gap to counting methodology and crawl frequency rather
than to the network changing between the two measurement windows.

That attribution is the paper's own claim about another paper's method, so it is not yet established.
Reading the 2022 paper's own full text is what settles whether the gap is methodological. Until then,
neither figure may be cited as the cloud-hosted share.

### Ethereum node population: about 6,000 against about 223,000

Shi and colleagues (WWW 2026) state Ethereum mainnet holds roughly 6,000 nodes, from a snapshot of
the official DNS-based peer list (EIP-1459) taken 2025-07-01. Li and colleagues (ePrint 2025) crawl
the routing tables directly and measure the Discv4 network at 94,180 to 113,524 nodes, averaging
103,432, and Discv5 at 208,268 to 238,219, averaging 223,132, over 2024-12-12 to 2024-12-27. Nodes
tagged as Ethereum mainnet within the Discv4 population alone number 12,404 to 15,374.

These measure different populations by different methods: one counts what a curated bootstrap list
serves, the other counts what a full crawl reaches. Neither is wrong. A synthesis that cites "the
Ethereum node count" without stating which population and which method produces a discrepancy of
fifteen to forty times.

### IPFS content-announcement latency: 6.3 seconds against a 67% timeout rate

Trautwein and colleagues (INFOCOM 2024) measure single content-announcement operations on the live
IPFS network at 6.3 seconds median and 49.8 seconds at the 95th percentile under the unmodified
strategy. Cortés-Goicoechea and colleagues (arXiv 2024) run concurrent batches of 80 content
identifiers from one node on an AWS Paris virtual machine in October 2023, and record 20% completing
within 70 seconds and 67% reaching an 80-second timeout.

One measures independent single operations, the other measures 80 concurrent operations from one
node. Both describe announcement latency on the live network in the same period. A synthesis must
state which of the two an application's behavior resembles rather than averaging them.

### Argon2i under the Alwen-Blocki attack: no practical advantage against a factor of two

Biryukov, Dinu and Khovratovich (IEEE EuroS&P 2016), applying the attack's own published time-area
formula analytically, conclude the adversary gains an advantage below 1 up to 1 GB of memory and
below 2 up to 16 GB, and state the attack is no better than the ranking attack. Alwen and Blocki
(IEEE EuroS&P 2017) simulate an optimized version of the same attack and measure a factor-of-two cost
reduction against Argon2i-B at 1 GB with 6 passes, which is the maximum setting the IRTF proposal
recommends, and state more than 10 passes are needed for the attack to fail at that memory size.

Both analyze the same attack family at the same memory scale and reach opposite conclusions about
practical threat. The disagreement traces to heuristics the 2017 paper adds — an improved
depth-reducing-set construction and concrete-parameter optimization — that the 2016 analytic
treatment does not apply. For choosing a memory-hard function's parameters, the 2017 measurement is
the one to plan against, because it is an attack that was run rather than an attack that was bounded.

### Social-graph forgery defenses on a real graph where their assumption fails

Wei and colleagues (INFOCOM 2012) state SybilDefender requires the honest region to mix quickly and
the count of edges between honest and adversary identities to be small. Gao and colleagues (CNS 2018)
measure a 21,297,772-node Twitter graph where both conditions fail: modularity 0.0042, and 18.4
million edges between honest and adversary identities. On that graph, methods relying on graph
structure alone reach an area under the curve of 0.57 to 0.80, while SybilFuse, which does not
require those conditions, reaches 0.85.

This is not two measurements of one quantity. It is a measurement of the conditions a mechanism
requires, taken on a network where they do not hold. It bears directly on the brief's third open
problem.

---

## Wrong documents caught before extraction

The extraction pass required each agent to check the first page of the retrieved text against the
citation before extracting from it. Six of roughly 124 files checked were not the paper claimed — a
rate near 5%, which is why the check exists. Every one of these would have produced measurements
attributed to a paper that does not contain them.

| Key | What the retrieval actually produced |
|---|---|
| `SINGH-INFOCOM-06` | The 2004 ACM SIGOPS European Workshop paper by Singh, Castro, Druschel and Rowstron, not the INFOCOM 2006 paper by Singh, Ngan, Druschel and Wallach |
| `GUMMADI-SIGCOMM-03` | Krishna Gummadi's personal publications listing, not the routing-geometry paper it links to |
| `KREUTER-FC-22` | Kreuter, Lepoint, Orrù and Raykova's CRYPTO 2020 private-metadata-bit paper, not Silde and Strand's FC 2022 public-metadata paper |
| `KRISHNAN-ICIS-02` | Asvanund, Krishnan, Smith and Telang's 2004 NET Institute working paper, whose own bibliography cites the ICIS 2002 target as a separate document |
| `KOMLO-SAC-20` | Certicom's "SEC 1: Elliptic Curve Cryptography" standard, which contains no mention of FROST, Komlo or Goldberg in 356,756 characters |
| `BORMANN-SSR-25` | A white-box block-cipher fault-injection paper by a different author set |

Four were corrected mechanically once the mismatch was stated. The Kreuter file was re-registered
under its own correct key rather than discarded, because the CRYPTO 2020 paper it actually contains
is a competing construction that two other retrieved papers cite as foundational.

A seventh case is a registry error rather than a retrieval error. The target record for
`GAO-CNS-18` described its evaluation as using a Tuenti dataset with two attackers evading detection
differently. The retrieved paper contains no mention of Tuenti and evaluates on two Twitter-derived
networks instead. The description was wrong and reading the paper corrected it.

---

## Landing pages that passed the size check

Fifteen retrievals produced a publisher or repository page longer than the 6,000-character floor that
was supposed to separate a paper from a stub. Seven extraction agents caught this and marked their
entries unusable rather than extracting from an abstract, which is the rule working. The fetcher now
rejects a document carrying two or more markers that only a publisher page has, so the floor is no
longer the only check. Twelve of the fifteen were recovered as full text by requesting the PDF form
of the same URL.
