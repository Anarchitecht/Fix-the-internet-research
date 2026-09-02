## [LI-HCC-24] SoK: Decentralized Storage Network
**Citation:** Chuanlei Li, Minghui Xu, Jiahao Zhang, Hechuan Guo, Xiuzhen Cheng. "SoK: Decentralized Storage Network." High-Confidence Computing, 2024. DOI 10.1016/j.hcc.2024.100239.
**Retrieved:** full text (source URL not directly recorded in `targets-deduped.json`'s `candidate_urls`, which lists only the DOI and a generic `eprint.iacr.org` root; venue and DOI matched)
**Source URL:** https://doi.org/10.1016/j.hcc.2024.100239
**Domain:** C

### What it does
This is a systematization-of-knowledge (SoK) survey, not an experimental paper: it defines a common
abstract model for Decentralized Storage Networks (DSNs) and classifies five deployed systems against
it. The model represents any DSN as three functions over content-addressed data: `Put(D, SM) → CID`
(a client uploads data D to a storage miner SM and receives a Content Identifier, CID, addressing it),
`Manage(D, SM, ReM)` (storage and retrieval miners maintain availability, audit storage, and repair
faults), and `Get(CID, ReM) → D` (a client requests data back from a retrieval miner by CID). The paper
identifies three techniques as what distinguishes a DSN from a centralized store: Proof of Storage (PoS)
— a protocol letting a verifier confirm a miner still holds committed data without retrieving it, modeled
as `Setup, Store, Prove, Verify`; a consensus algorithm selecting which miner's proofs get recorded on a
shared ledger; and an incentive mechanism paying miners in the network's own cryptocurrency for storage
and retrieval service while penalizing detected misbehavior. Storage miners pledge storage capacity to
the network and can mine new blocks; retrieval miners serve data without pledging storage or generating
storage proofs. Every `Put` and `Get` is finalized only once its corresponding transaction (`TXPut` or
`TXGet`) is confirmed on the underlying blockchain.

### Measured results
This paper runs no experiment of its own and reports no primary measurement. Every quantitative figure
below is a fact this survey states about another system, sourced from that system's own documentation or
from a separate paper the survey cites — recorded here as reported-by-this-survey, attributed to its
original source, not as a measurement this paper performed.

| Figure | System | Attributed source (as cited by this survey) |
|---|---|---|
| Sealed-sector storage-proof validation required every 30 minutes | Filecoin | Guidi, Michienzi, Ricci (survey's reference [77]) |
| Minimum hardware to run a `lotus-miner` node: 256 GiB RAM, GPU with ≥11 GB VRAM | Filecoin | Filecoin's own Lotus documentation (survey's reference [78]) |
| Saturn CDN layer reaches 100 ms average Time to First Byte (TTFB) for IPFS content | Filecoin/IPFS's Saturn project | saturn.tech (survey's own footnote citation, not an independent benchmark) |
| 274 websites hosting child-sexual-abuse-material backups found stored inside the Bitcoin blockchain | Bitcoin (cited as an illustrative precedent for illegal-content persistence in any content-addressed store) | Matzutt et al. (survey's reference [85]) |

The survey's own comparative classification (Table I) — not a measurement, a structural comparison —
places five deployed decentralized systems and three centralized cloud providers against seven
categorical axes:

| System | Proof of Storage | Ledger structure | Consensus algorithm | Smart contract | Incentive | Redundancy | Cryptocurrency |
|---|---|---|---|---|---|---|---|
| Sia | Merkle Tree | Chain | Proof of Work | Yes | Yes | Erasure code | Siacoin |
| Storj | Proof of Retrievability | Chain | Proof of Stake (Ethereum) | No (smart-contract storage stated as a long-term Storj-forum goal, not shipped) | Yes | Erasure code | STORJ |
| Filecoin | PoRep/PoSt | Directed acyclic graph (DAG) | Expected Consensus | Yes | Yes | Full copy | FIL |
| FileDAG | PoRep/PoSt | DAG | DAG-Rider (an asynchronous Byzantine atomic broadcast protocol) | Yes | Yes | Full copy | FIL |
| Swarm | Merkle Tree | Chain | Proof of Work | Yes | Yes | Erasure code | BZZ |

### Parameters
- Erasure-code parameterization used to describe Sia, Storj, and Swarm's redundancy schemes: a (k, n)
  code splits data into n total chunks, any k of which reconstruct the original — the survey's own worked
  example uses a (3, 6) code.
- Storj's own extension of the (k, n) model, as this survey describes it: two additional thresholds m and
  o with k ≤ m ≤ o ≤ n — m is the minimum-safety chunk count that triggers a repair when available chunks
  drop below it; o is the number of chunks the network stops waiting for once uploaded, to avoid
  long-tail latency from the slowest nodes in a set. No numeric values for k, m, o, n are given by this
  survey; it describes only the parameter roles, citing the Storj whitepaper.
- Access-control granularity across surveyed systems, as this survey classifies it: exactly two
  categories exist in current deployments — fully public access (Filecoin) or uploader-exclusive access
  (Storj, Sia) — with no intermediate, revocable, per-grantee access control in any surveyed system.

### Stated limitations
The survey states DSNs currently cannot edit uploaded data, so representing multiple versions of a file
requires re-uploading each full version, causing storage waste; it cites one proposed fix (FileDAG,
survey reference [23], storing only the increment between file versions) but states that fix's own
storage-proof computation cost grows linearly with the number of versions stored, an unresolved
trade-off. It states existing DSN proof systems trade high computational cost for security: Filecoin's
proof-generation pipeline computes a Stacked Depth-Robust Graph and a zk-SNARK, both computationally
heavy, while Sia and Swarm "simplify their proof processes at the expense of data security" — a direct
trade-off this survey identifies without resolving. It states current DSN cross-chain interoperability is
confined to major blockchains (Bitcoin, Ethereum) and does not extend between DSNs themselves, so moving
data or verifying storage proofs across two different DSNs (its worked example: a Filecoin user wanting
to retrieve data stored on Storj) has no existing mechanism. It states DHT-based peer and content
discovery (the survey's example: IPFS, which Filecoin relies on) records node identifiers and content
identifiers in a form visible to any observer of the DHT, exposing querying clients to third-party
traffic monitoring, and states this exposure is unresolved by any surveyed system's current design. It
states no surveyed system provides a mechanism for permanently removing illegal content once it is
content-addressed: a single-bit change to a file produces a different Content Identifier, so a takedown
of one CID does not remove other copies of near-identical content, and on-chain smart-contract detection
of illegal content is described as impeded by the impracticality of passing large stored files as
on-chain computation inputs.

### Requirements it places on the rest of the system
Every DSN this survey classifies requires an underlying blockchain (or DAG-structured ledger) to finalize
both `Put` and `Get` operations — the paper states completion of these functions "is contingent upon the
confirmation of transactions on the blockchain," so any redesign removing a shared total-order or
partial-order ledger breaks the model's stated Put/Get semantics as described here. Proof of Storage
requires the storage miner to hold a challenge value the paper describes as read "from the blockchain,"
so PoS verification as modeled here presumes miners and verifiers share access to a common, tamper-evident
challenge source, not a mechanism generating challenges through a purely peer-to-peer channel. A
consensus algorithm is required to select which miner's proof of storage or proof of retrieval gets
recorded, meaning storage-proof correctness in this model is only as trustworthy as whatever fraction of
byzantine or malicious miners the chosen consensus algorithm tolerates — the survey's own cited attack
research (temporary block-withholding attacks against Filecoin's Expected Consensus) shows this
dependency is not merely theoretical for at least one deployed system.

### Contradicts
None found against other corpus entries on a measured fact — this survey performs no measurement itself.
Note for downstream synthesis: this survey's Table I classifies Storj's redundancy scheme as "Erasure
Code" without stating specific (k, n) values; LI-IWQOS-23-STORJ (an empirical measurement of the live
Storj network, also in this batch) should be checked for whether it states Storj's deployed (k, n, m, o)
values, since this survey does not.

### References worth retrieving
- **Foundational** — David Vorick, Luke Champine. "Sia: Simple decentralized storage." (Cited as
  reference [6]; the Sia whitepaper this survey's classification of Sia is drawn from.)
- **Foundational** — Storj Labs, Inc. "Storj: A decentralized cloud storage network framework." (Cited as
  reference [7]; source of the (k, m, o, n) redundancy-parameter description this survey summarizes.)
- **Foundational** — Protocol Labs. "Filecoin: A decentralized storage network." (Cited as reference [9];
  source of the PoRep/PoSt and Expected Consensus descriptions this survey summarizes.)
- **Foundational** — Hechuan Guo, Minghui Xu, Jiahao Zhang, Chunhui Liu, Dongxiao Yu, Schahram Dustdar,
  Xiuzhen Cheng. "FileDAG" (multi-version deduplication for Filecoin-style DSNs). (Cited as reference
  [23].)
- **Attack** — John R. Douceur. "The Sybil Attack." International Workshop on Peer-to-Peer Systems (IPTPS)
  2002. (Cited as reference [50]; the foundational Sybil-attack framing this survey applies to DSN storage
  miners.)
- **Attack** — Roman Matzutt, Jens Hiller, Martin Henze, Jan Henrik Ziegeldorf, et al. (title not fully
  captured in the retrieved bibliography text). (Cited as reference [85]; source of the 274-website
  child-sexual-abuse-material figure this survey cites for illegal-content persistence in content-
  addressed stores — retrieve to check whether this survey's citation of the figure and its conditions is
  accurate.)
- **Attack** — Xihan Wang, Sarah Azouvi, Marko Vukolić. "Security analysis" (of Filecoin's Expected
  Consensus, per this survey's description). (Cited as reference [82]; source of the n-split attack this
  survey cites against Filecoin's consensus.)
- **Attack** — Tianxiang Cao, Xin Li. "Temporary block withholding attacks" (against Expected Consensus,
  per this survey's description). (Cited as reference [83].)

### Verbatim extracts
- "clients need to be able to verify that a storage miner has retained file data without retrieving the
  data."
- "the completion of both the Put and Get functions is contingent upon the confirmation of transactions
  on the blockchain."
- "miners must periodically generate storage proofs, necessitating validation of each sealed sector every
  30 minutes."
- "a user must configure a system with 256GiB RAM and a GPU featuring no less than 11GB VRAM."
- "Matzutt et al. [85] documented the presence of backups for 274 websites containing child pornography
  within the Bitcoin network."
- "the granularity of access control within existing DSNs is markedly coarse, delineated into merely two
  categories."
