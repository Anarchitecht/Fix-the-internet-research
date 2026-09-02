## [LI-IWQOS-23-STORJ] An Empirical Study of Storj DCS: Ecosystem, Performance, and Security
**Citation:** Hao Li, Xianghang Mi, Yanzhi Dou, Shanqing Guo. "An Empirical Study of Storj DCS: Ecosystem, Performance, and Security." IEEE/ACM International Symposium on Quality of Service (IWQoS), 2023.
**Retrieved:** full text (retrieved and read in full for the corpus's `volunteer-repair-economics.md` open-problem entry; no `targets-deduped.json` record for this key)
**Source URL:** not recorded in the registry for this key
**Domain:** C (also relevant to J — deployed-system measurement)

### What it does
The paper measures the live Storj decentralized cloud storage (DCS) network by building a storage-node
collector: a program that repeatedly uploads probe files to Storj's centralized coordination servers
(Satellites) and records which storage nodes the Satellite returns as upload targets, since Storj
publishes no complete node list. Storj's storage pipeline, as the paper describes it from the protocol's
own design: a client splits a file into 64 MB segments, encrypts each segment locally, then applies
Reed-Solomon erasure coding to split each segment into n = 80 pieces; to route around slow nodes during
upload, the Satellite selects o = 110 candidate storage nodes and the client keeps only the first n = 80
pieces to finish uploading (the paper's text states the encoding parameters as (k, l, n, o) = (29, 39, 80,
110)); on download, the client attempts to fetch pieces from l = 39 storage nodes and needs only k = 29 of
the returned pieces to reconstruct the segment. A Satellite additionally tracks a per-node reputation
score built from audit failures and PUT/GET selection-and-success counts, and factors that score into
which nodes get selected for future uploads.

### Measured results
Data-collection methodology: a storage-node collector queried Storj's satellite servers at most once per
second (Storj's own free-tier rate limit is 100 requests/second), terminating each day's collection run
after 10 consecutive rounds with no newly discovered node, running under 18 hours per day in most cases,
over a 16-month measurement window from April 30, 2021 to August 30, 2022.

| Finding | Figure | Conditions |
|---|---|---|
| Unique storage nodes observed | 32,881 | Cumulative, over the full 16-month window |
| Unique IP addresses that ever hosted a storage node | 155,457 | Same window |
| Geographic and network spread | 122 countries, 2,418 Autonomous System Numbers (ASNs), 205 /8 IPv4 prefixes | Geolocation via IPinfo, a third-party IP-data provider the paper cites as handling 420 billion requests/year |
| Growth in storage-node-ID count | 183% increase | April 30, 2021 to August 30, 2022 |
| Daily active storage nodes | Stable at roughly 13,000 | Across the measurement window |
| Node retention | 44% of nodes active in April 2021 still active by August 2022 | Same population tracked across the full window |
| Average month-by-month churn rate | 9.6% | Computed across all 16 monthly transitions, May 2021 to August 2022 |
| Month-by-month churn rate range | 4.55% (February 2022, 515 departing nodes) to 15.28% (November 2021, 1,860 departing nodes) | Individual monthly transitions; full 16-month table given in the paper (14.48%, 10.93%, 10.33%, 9.43%, 7.56%, 13.41%, 15.28%, 14.47%, 4.55%, 8.45%, 7.67%, 8.06%, 7.54%, 5.29%, 6.21% across May 2021–July 2022) |
| IP addresses that migrated across at least 2 distinct IPs | 32,881 nodes migrated (paper states this equals its full observed node count, i.e., the finding applies broadly across the observed population) | Attributed largely to nodes on dynamic public IP addresses re-resolving under a stable hostname |
| Storage nodes with IP addresses linked to at least one malicious activity (VirusTotal threat-intelligence lookup) | 4.48% of the 155,457 observed IPs | Malicious-activity categories: communicating with malware samples (5,643 IPs, 3.63%, hosting 4,869 storage nodes = 14.8% of the IPs in this sub-category) and being referenced inside malware payloads (1,321 IPs, 0.85%) |
| Malware sample categories contacting these IPs | 19,202 unique malware samples total; over 86% categorized Trojan, 6.7% Virus, 0.3% crypto-mining software | VirusTotal metadata over the 5,643 communicating-malware IPs |
| Malware file-type distribution contacting these IPs | ~76% Win32 executable, ~20% Android application | Same 5,643-IP subset |
| Case-study upload latency, Storj Uplink client | ~19 s measured, consistent with the paper's own derived formula (L = 8xo / (b_c k)) | File size x = 64 MB, client bandwidth b_c = 100 Mbps, region EU-DE, k = 29, o = 110 |
| Case-study upload latency, Storj S3 gateway | ~7 s measured, consistent with the paper's own derived formula | Same file and client, assumed gateway bandwidth b_s3 = 1,000 Mbps |

Reputation-manipulation attack (Section V-B): demonstrated on a private testbed running Storj Test
Network v1.40.4 on one Ubuntu 20.04 Linux server with 256 GB RAM, consisting of one Uplink client, ten
storage nodes, and one satellite — not a measurement of the live production network. The paper's own
source-code analysis found several reputation factors (PUT/GET selection count, successful PUT/GET count,
PUT/GET selection success count) forgeable by a Byzantine node that acts as both storage node and storage
client simultaneously, using a modified Uplink client to redirect uploads to nodes under its own control
rather than the nodes the satellite assigned; the paper confirms in its testbed that this both raises the
attacker's own reputation and can be inverted to falsely lower an honest victim node's reputation by
forging failed PUT/GET operations. The paper states it reported this to Storj.io and that Storj's team
assessed it as a common (already-known-class) vulnerability — an attributed statement, not an independent
confirmation the paper obtained.

### Parameters
- Storj erasure-coding parameters at time of writing: (k, l, n, o) = (29, 39, 80, 110) — k the minimum
  pieces to reconstruct, l the number of storage nodes a download attempts to contact, n the total pieces
  a segment is encoded into, o the number of candidate nodes a satellite selects for upload before the
  client keeps only the fastest n. The paper explicitly states these values "may change in the future."
- Segment size: 64 MB, the fixed unit Storj Uplink splits an uploaded file into before erasure coding.
- Collector polling rate: at most 1 request/second to a satellite, versus Storj's stated free-tier rate
  limit of 100 requests/second — chosen to keep the collector's own traffic negligible relative to normal
  client load.

### Stated limitations
The paper's own comparative background section (Table I) states that, among the three decentralized cloud
storage networks it compares, only Storj and Sia support erasure coding and client-side encryption;
Filecoin at the time of writing stored files with a single storage provider by default, without
client-side encryption. The paper reports no repair-traffic measurement of any kind — no figure in the
paper states bytes moved, nodes contacted, or time elapsed when a lost erasure-coded piece is
reconstructed and re-uploaded; the paper's "audit and repair" description of a Satellite's role is stated
once, in the background section, without measurement. The reputation-manipulation attack is demonstrated
only on a small (10-node) private testbed, not observed or reproduced against the live production
network; the paper does not state whether the vulnerability was exploited in the wild during the
measurement window.

### Requirements it places on the rest of the system
Storj's repair and node-selection mechanism, as this paper describes it, depends entirely on the
Satellite — a centralized coordination service — to track node reputation, select which nodes serve each
upload, and audit stored data; the paper's own attack finding shows this dependency is a single point of
manipulation, since forging PUT/GET success and failure counts (observable and forgeable, per the paper's
source-code analysis, by any node colluding with a client) directly changes which nodes the Satellite
selects for future storage, without requiring any cryptographic break. Client-side erasure coding and
encryption require the client to correctly implement Reed-Solomon splitting into exactly n pieces and
correctly track which k of them, from among the l attempted downloads, suffice for reconstruction — a
protocol-level parameter (k, l, n, o) any compatible node or client must share, since the paper's own
latency formulas are derived directly from these four values and match measured latency only when both
sides agree on them.

### Contradicts
None found against other corpus entries on a measured fact. This entry supplies the churn-rate and
node-count figures that the corpus's `volunteer-repair-economics.md` open-problem synthesis already cites
by KEY (`LI-IWQOS-23-STORJ`) as the most recent real-population churn trace available, alongside a
recorded absence of any repair-traffic figure from this same source — consistent with what is found in
the full text here.

### References worth retrieving
- **Foundational** — Storj Labs, Inc. "Storj: A decentralized cloud storage network framework."
  (Background source for this paper's description of Storj's architecture and erasure-coding design;
  already covered as the whitepaper cited by `LI-HCC-24`/`LI-EPRINT-24-SOKDSN` in this batch as reference
  [7].)
- **Attack** — cited as reference [25] in this paper (IP-reputation-based traffic filtering, source of
  the paper's framing that abused IPs are more likely blocked by security tooling) — bibliography detail
  not fully captured in this extraction pass; retrieve to confirm.
- **Competing measurement** — the paper's own reference [28], cited alongside VirusTotal as prior work
  finding cloud-hosted services abused for botnet and spam activity — bibliography detail not fully
  captured in this extraction pass; retrieve to confirm identity and compare against this paper's 4.48%
  figure.

### Verbatim extracts
- "erasure coding variables are (k, l, n, o) = (29, 39, 80, 110)."
- "the churn rate ranges from 4.55% to 15.28%, and the average churn rate is 9.6%."
- "44% were still active by the last month of our measurement."
- "4.48% of all the storage nodes' IPs have been associated with at least one malicious activity."
- "a Byzantine node can forge a set of reputation factors ... to improve its overall reputation."
- "Storj's team assessed this to be a common vulnerability."
