# Open problem: repair economics for volunteer erasure-coded storage under measured churn

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
