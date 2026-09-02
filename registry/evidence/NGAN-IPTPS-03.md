## [NGAN-IPTPS-03] Enforcing Fair Sharing of Peer-to-Peer Resources
**Citation:** Tsuen-Wan "Johnny" Ngan, Dan S. Wallach, Peter Druschel. "Enforcing Fair Sharing of Peer-to-Peer Resources." IPTPS, 2003. DOI 10.1007/978-3-540-45172-3_14.
**Retrieved:** full text via https://www.cs.rice.edu/~druschel/publications/samsara-iptps03.pdf (candidate URL; matched title and authors in first 2000 characters)
**Source URL:** https://link.springer.com/chapter/10.1007/978-3-540-45172-3_14
**Domain:** I

### What it does
Enforces a storage-consumption limit per participant in a peer-to-peer network — a node may store no more remote data than the local disk space it advertises as available to others — using a publish-and-audit mechanism rather than a central broker or a hardware trust anchor, so no single point of failure or trusted issuing authority is required.

Every node keeps a signed usage file readable by any other node, containing the node's advertised storage capacity, a local list of (nodeId, fileId, size) entries for files the node stores on behalf of others, and a remote list of fileIds (with sizes) the node has published to remote storage. A node is "under quota" and permitted to write new files when advertised capacity minus the sum of its remote list (charging per replica) is positive; a node accepting a file first fetches the publisher's usage file to check this. Filesystem possession is checked by a challenge mechanism: for each stored file, a node periodically picks a replica holder as challenge target, notifies the other replica holders, and queries the target for the hash of a few randomly selected blocks; the target can answer only if it holds the file, and any attempt to fetch the file from another holder mid-challenge is visible to the challenger, who restarts the challenge.

Inflation of the local list (claiming to store files nobody actually published) is detected by two audit mechanisms. A normal audit: any node with a file entry in a target's remote list periodically (anonymized via a Crowds-style one-hop random relay so the target cannot identify its auditor) fetches the target's usage file and checks the file is present. A random audit: every node, at lower frequency, picks a node uniformly at random from the whole overlay, fetches its usage file, and cross-checks every entry in its local list against the corresponding remote-list entry at the nodes identified there. Cheaters who collude to push their own debt onto each other's books form a chain; the chain necessarily terminates at a "cheating anchor" node whose local list contains an entry with no matching remote-list entry anywhere, and random auditing discovers that anchor with a bounded probability per period (derived below). Because usage files are digitally signed, the anchor's own file is a signed record of its inconsistency, usable as evidence for ejecting it from the network; ejecting the anchor exposes the next cheater in the chain who depended on it.

A competing design, quota managers, replaces this publish-and-audit approach with a manager set: a fixed set of nodes adjacent to a given node in the overlay's identifier space, which jointly track that node's storage consumption and must approve (via a Byzantine fault-tolerant agreement protocol among the managers) every new-file request from the node they manage.

### Measured results
Simulation study; no real-world deployment or testbed measurement. All figures below use these fixed settings unless stated otherwise: 10,000 nodes, 285 files stored per node, average node lifetime 14 days, per-node storage capacity drawn from a truncated normal distribution ranging 2 GB to 200 GB with a 48 GB average, 1% of files reclaimed and republished per simulated day, two challenges issued per stored file per day against randomly chosen replicas, quota-manager sets of size 10 (tolerating 3 Byzantine nodes per set via Castro and Liskov's BFT algorithm), normal audits performed on average 4 times daily per remote-list entry, random audits performed once daily, and simulations assuming all nodes honestly follow the protocol (no cheating modeled). The measured quantity throughout is per-node communication bandwidth attributable to storage accounting only — overlay maintenance and actual file storage/retrieval traffic are explicitly excluded from the measurement.

| Experiment | Independent variable | Compared designs | Reported outcome |
|---|---|---|---|
| Figure 3: overhead vs. node count | 1,000 to 100,000 nodes (log scale), other parameters at baseline | Auditing without caching, auditing with caching, quota managers | Per-node upstream bandwidth (identical to downstream) stays nearly constant across this three-order-of-magnitude range of node counts for all three designs, i.e. all three scale with overlay size; axis range plotted is 0-80 bps |
| Figure 4: overhead vs. files stored per node | 0 to 700 files per node, other parameters at baseline | Same three designs | Overhead grows linearly with files-per-node for all three; auditing without caching grows at roughly twice the rate of the other two designs; axis range plotted is 0-200 bps |
| Figure 5: overhead vs. average node lifetime | 0 to 25 days average node lifetime, other parameters at baseline | Same three designs | Quota-manager overhead rises rapidly as node lifetime shortens, attributed to the cost of nodes joining and leaving manager sets and voting on file insertions for new nodes; axis range plotted is 0-350 bps |
| Random-audit detection probability (analytical, not simulated) | n-node network with c colluding ("conspiring") nodes | — | Probability the cheating anchor escapes random audit in one period is approximately ((n-2)/(n-1))^c, converging to e^-1 (about 0.368) as c grows; probability of discovery within three audit periods exceeds 95% |

The paper states, without giving a specific bandwidth figure, that under these conditions "auditing overhead is quite low — only a fraction of a typical p2p node's bandwidth," and that auditing with caching performs comparably to quota managers while quota managers are more sensitive to file turnover rate (higher voting cost) and to manager-set size (larger sets tolerate more Byzantine nodes but cost more).

### Parameters
- Node count: baseline 10,000; varied 1,000-100,000 in Figure 3.
- Files stored per node: baseline 285; varied 0-700 in Figure 4.
- Average node lifetime: baseline 14 days; varied 0-25 days in Figure 5.
- Per-node storage capacity: truncated normal distribution, 2 GB to 200 GB, average 48 GB.
- File reclamation/republication rate: 1% of files per simulated day.
- Challenge frequency: 2 challenges per stored file per day, against randomly selected replicas.
- Quota-manager set size: 10 nodes per set, tolerating up to 3 Byzantine-faulty members (via Castro and Liskov's BFT protocol), consistent with the standard n >= 3f+1 Byzantine fault tolerance bound.
- Normal audit frequency: average 4 times daily, per entry in a node's remote list.
- Random audit frequency: once daily, target chosen uniformly at random from the whole overlay.
- Anonymization for audits: one-hop random relay indirection (a technique the paper describes as similar to Crowds), stated as providing "weak anonymity sufficient for our purposes."

### Stated limitations
The paper states it focuses "primarily on minority collusions" — a threat model where a subset of nodes conspires but most of the network is not conspiring — and explicitly separates this from "minority bribery," where an adversary selects and bribes specific nodes; the authors state that while bribery-resistant mechanisms at this layer may be buildable, "it is entirely unclear that the lower-level p2p routing and messaging systems can be equally robust," and for the remainder of the paper they assume the correctness of the underlying peer-to-peer routing system rather than defending it. The paper explicitly excludes overlay-maintenance and file storage/retrieval bandwidth from its overhead measurements, so the reported figures cover accounting traffic only, not total system bandwidth. The simulation assumes all nodes honestly follow the protocol (no cheating is modeled in the reported experiments) — the discovery-probability analysis for the cheating anchor is a separate, closed-form calculation, not a simulated adversarial run. The recursive audit that would fully verify a node's entire dependency chain is stated to be "prohibitively expensive" to implement directly, which is why the paper substitutes random sampling (the random-audit mechanism) instead. Quota managers are stated to be vulnerable to bribery because "managers suffer no direct penalty if they grant requests that would be correctly denied."

### Requirements it places on the rest of the system
- Requires a public key infrastructure allowing every node to sign documents that any other node can verify and that others cannot forge; both the smart-card, quota-manager, and auditing designs assume this as given.
- Requires the underlying peer-to-peer storage system to supply a mechanism for locating the replica holders of a given fileId (the paper cites PAST for this) since the remote list stores only fileIds, not the identities of the nodes holding those replicas.
- Requires an anonymizing relay layer (one-hop indirection, described as Crowds-like) available to the accounting mechanism, so that an auditor's identity is hidden from the node it audits; without this, a node under audit could distinguish and selectively satisfy known auditors while defrauding others.
- Requires every node in the overlay to perform both normal audits (against nodes with entries in its own remote/local lists) and random audits (against nodes chosen uniformly from the whole overlay) on a regular schedule; the stated 95%-within-three-periods detection guarantee holds only if this schedule is actually followed by participants, which the paper treats as incentivized by mutual benefit from cheater ejection but does not separately verify under an adversarial simulation.
- The quota-manager alternative requires the overlay's node-identifier space to supply well-defined "adjacent" node sets usable as manager sets, and requires those manager sets to run a Byzantine fault-tolerant agreement protocol (Castro and Liskov's PBFT) tolerant of at most floor((set size - 1)/3) faulty members; increasing Byzantine-fault tolerance in this design requires enlarging manager sets, which the paper's Figure 5 result shows raises overhead as node lifetime shortens due to more frequent manager-set churn.
- Requires all nodes storing replicas of a file to be reachable for challenge-response block-hash queries; a challenge requires that other replica holders of the target file be notified in advance so a mid-challenge file-fetch from among them is visible to the challenger.

### Contradicts
None found among the current corpus. No other paper in this batch measures fair-sharing/storage-accounting overhead against which this paper's Figures 3-5 could be compared.

### References worth retrieving
- Foundational: M. Castro, B. Liskov, "Practical Byzantine fault tolerance," OSDI, 1999 — the BFT agreement protocol the quota-manager design's manager sets run, used directly in this paper's simulation.
- Foundational: M. Castro, P. Druschel, A. Ganesh, A. Rowstron, D. S. Wallach, "Security for structured peer-to-peer overlay networks," OSDI, 2002 — source of the minority-collusion threat-model framing this paper adopts and explicitly restricts itself to.
- Foundational: P. Druschel, A. Rowstron, "PAST: A large-scale, persistent peer-to-peer storage utility," HotOS, 2001 — the storage system this accounting mechanism is designed to sit on top of; source of the original smart-card quota proposal this paper rejects as unsuitable for "grassroots" (non-organizationally-backed) systems.
- Foundational: M. K. Reiter, A. D. Rubin, "Crowds: Anonymity for web transactions," ACM TISSEC 1(1), 1998 — the anonymization technique the auditor-identity-hiding mechanism is modeled on.
- Competing: R. Anderson, "The Eternity Service," Proc. 1st Int'l Conf. on the Theory and Applications of Cryptology, 1996 — an alternative fairness/persistence design using explicit electronic currency to purchase storage, contrasted with this paper's currency-free barter framing.
- Competing: M. Waldman, D. Mazieres, "Tangler: A censorship-resistant publishing system based on document entanglements," ACM CCS, 2001 — a small-scale (under 30 servers) certificate-based fairness design requiring a first-month no-publish period for new servers, cited as an alternative fairness mechanism.
- Attack/critique input: E. Adar, B. Huberman, "Free riding on Gnutella," First Monday 5(10), 2000 — measurement motivating the paper's fair-sharing problem statement.
- Related economic result: E. Fehr, S. Gachter, "Altruistic punishment in humans," Nature 415, 2002 — a human-subject economic study the paper cites as justification that users will accept the cost of performing random audits.
- Foundational (DAMD framing): J. Feigenbaum, S. Shenker, "Distributed algorithmic mechanism design: Recent results and future directions," DIALM, 2002 — the distributed-mechanism-design framing the paper's introduction adopts.

### Verbatim extracts
- "requiring nodes to publish auditable records of their usage can give nodes economic incentives"
- "This paper focuses primarily on minority collusions."
- "it is entirely unclear that the lower-level p2p routing and messaging systems can be equally robust"
- "the cheating anchor would be discovered in three periods with probability higher than 95%"
- "auditing overhead is quite low — only a fraction of a typical p2p node's bandwidth"
- "managers suffer no direct penalty if they grant requests that would be correctly denied"
- "auditing with caching has performance comparable to quota managers, but is not subject to bribery attacks"
