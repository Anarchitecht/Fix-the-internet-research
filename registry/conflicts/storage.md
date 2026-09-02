# Storage family: conflicts and disagreements

Scope: erasure-coding overhead ratios, replication factors, repair bandwidth,
reconstruction thresholds, durability under churn or failure, proof-of-storage
verification cost, and the liveness requirement each repair scheme places on
holder reachability. Entries covered: `BLAKE-HOTOS-03`, `CHUN-NSDI-06`,
`BHAGWAN-NSDI-04`, `BHAGWAN-IPTPS-03`, `RHEA-USENIXATC-04`, `RODRIGUES-IPTPS-05`,
`WEATHERSPOON-IPTPS-02`, `DIMAKIS-TIT-10`, `HUANG-ATC-12`, `SATHIAMOORTHY-VLDB-13`,
`VAJHA-FAST-18`, `DANEZIS-WALRUS-25`, `WILKINSON-STORJ-18`, `VORICK-SIA-14`,
`BENET-FILECOIN-17`, `WILCOX-OHEARN-STORAGESS-08`, `ATENIESE-CCS-07`,
`SHACHAM-ASIACRYPT-08`, `DZIEMBOWSKI-CRYPTO-15`, `FISCH-EUROCRYPT-19`,
`ANDERSON-CCGRID-06`, `STUTZBACH-IMC-06`.

## 1. Feasibility of wide-area durable storage on unreliable nodes

`BLAKE-HOTOS-03` and `CHUN-NSDI-06` reach opposite conclusions about the same
question — whether a wide-area population of unreliable nodes can hold a large
amount of data durably — because they model two different loss regimes.

`BLAKE-HOTOS-03` derives a bandwidth bound from a model of continual membership
turnover: nodes join and leave a cooperative storage pool at rate matched to
measured Gnutella churn (about 33,000 hosts crawled April 11-19, 2003), and
every join or leave moves that node's share of the stored data. Under that
model, holding 1 TB of unique data at high availability with Gnutella-like
participation and cable-modem-like bandwidth is stated as effectively
infeasible: "it seems hopeless to field even 1TB at high availability with
Gnutella-like participation." Restricting membership to the most available 5%
of hosts and coding at b=15 fragments lowers the bandwidth requirement to about
30 Kbps per node per unique TB, but the paper states admission control does not
change the underlying bandwidth-scale-dynamics tradeoff.

`CHUN-NSDI-06` measures Carbonite, a replica-maintenance algorithm, against a
one-year PlanetLab trace (632 hosts, 21,255 transient failures, 219 disk
failures, March 2005-February 2006) where data loss is driven by disk failure
against a comparatively stable membership, not by continual peer churn.
Carbonite keeps 1 TB of data durable at 44% more network traffic than an oracle
system that repairs only on true disk failure, and the paper states the
practical repair threshold (rL=3) loses no data on the PlanetLab trace.

`CHUN-NSDI-06` states the difference in conclusion directly: it attributes its
own more favorable result to considering "a relatively stable system membership
where data loss is driven by disk failure" rather than `BLAKE-HOTOS-03`'s
continual-churn regime. Node population, loss cause, and membership stability
all differ between the two studies, so this is a difference in modeled
scenario, not a numeric disagreement over the same measured quantity. A design
built on a stable-membership, disk-failure-dominated population (data-center or
managed-node deployment) can cite `CHUN-NSDI-06`'s feasibility result; a design
built on continual, Gnutella-like peer churn cannot, and `BLAKE-HOTOS-03`'s
bound is the one that applies to it.

## 2. Erasure-coding-vs-replication savings ratio

`WEATHERSPOON-IPTPS-02` and `RODRIGUES-IPTPS-05` both compute how much
bandwidth erasure coding saves over replication for maintaining object
durability, and report savings factors an order of magnitude apart.
`RODRIGUES-IPTPS-05` names this exact comparison unchecked in its own entry
and flags it for a synthesis step to resolve.

`WEATHERSPOON-IPTPS-02` derives its comparison analytically from an assumed
disk-lifetime distribution (Patterson and Hennessy), independent and
identically distributed disk failures, and a periodic sweep-and-repair
process. Holding system mean time to failure (MTTF) at 1000 years and the
repair epoch at 4 months, replication (r=22) uses 11 times the bandwidth,
storage, and disk seeks of a rate-1/2, n=64 erasure code for the same block
count. Holding block MTTF and storage overhead fixed instead, replication uses
28 times the repair bandwidth of the matched code.

`RODRIGUES-IPTPS-05` computes the same class of ratio (redundancy savings from
coding versus replication, m=7 fragments, matching the parameter Chord/CFS
uses) but drives its model from measured node-availability traces — Overnet
(2,400 peers), Farsite (51,663 corporate desktops), and PlanetLab (186 hosts) —
rather than an assumed disk-failure distribution, and reports a savings ratio
of 1x to 3x, rising as measured availability falls and as the target
availability level rises. On the Overnet peer-to-peer trace, average node
availability falls below 50% once the membership timeout exceeds 11 hours; the
resulting coding-vs-replication bandwidth saving is real but the paper states
the maintenance bandwidth remaining after that saving — around 100 Kbps per
node — is "unsustainable for home users."

Both figures are as each paper states them; the ten-fold gap traces to the
node population each model assumes. `WEATHERSPOON-IPTPS-02`'s savings factor
holds for a population with near-permanent per-node availability (disk MTTF
measured in years, not the fraction-of-time-reachable figures `RODRIGUES-IPTPS-05`
measures). `RODRIGUES-IPTPS-05`'s 1x-3x figure holds for populations with
substantially lower, measured availability, including a real peer-to-peer
trace. A synthesis describing coding's bandwidth advantage for a decentralized,
peer-operated deployment should cite `RODRIGUES-IPTPS-05`'s 1x-3x figure, not
`WEATHERSPOON-IPTPS-02`'s 11x-28x figure, which assumes a data-center-like,
highly-available node population that a decentralized deployment does not have.

## 3. Unsupported attribution: Sia's storage overhead

`DANEZIS-WALRUS-25` (Table 1) states a storage overhead of 3x for "classic
erasure-coded systems (Storj, Sia)" at twelve-nines durability, attributing
this figure to Sia among others. Sia's own paper, `VORICK-SIA-14`, states no
such figure. It leaves the erasure-code redundancy ratio "as a design choice
for the client," and its one numeric worked example — m=10 pieces recoverable
out of n=100 stored, a 10x expansion — is explicitly flagged by its own authors
as "only illustrative" and "an extreme example," not a specification or a
recommended value. `VORICK-SIA-14`'s stated limitations describe Sia's storage
proof as verifying only that a host holds a file, with the choice of erasure
code and redundancy level left entirely to the client. The 3x figure
`DANEZIS-WALRUS-25` attributes to Sia does not trace to Sia's own paper.

## 4. Internal inconsistency: Storj's storage overhead, and a related figure gap

`DANEZIS-WALRUS-25`'s own text gives Storj's overhead three different values
without reconciling them. Its headline Table 1 states 3x, the same "classic
erasure-coded systems (Storj, Sia)" figure used for the Sia comparison above.
Its related-work section separately states "This approach results in a 2.75×
replication factor," citing Storj's own 29-of-80 Reed-Solomon configuration
from a 2026 Storj Labs document outside this corpus. The paper does not
reconcile the 3x Table 1 figure against its own 2.75x related-work figure for
the same system.

A third figure sits alongside these two. Storj's whitepaper as retrieved in
this corpus, `WILKINSON-STORJ-18`, states its own "typical scenario" deployment
example as "40 disk drives (a 20/40 Reed-Solomon setup)" — a 2x expansion
factor, lower than either of `DANEZIS-WALRUS-25`'s two figures. `WILKINSON-STORJ-18`
gives no single fixed overhead either; its repair-bandwidth table (k,n) pairs
range from 1.33x to 3x depending on target mean time to failure and repair
threshold, so no single number in that paper is "Storj's overhead" without
naming the (k,n) pair. `DANEZIS-WALRUS-25`'s 3x Table 1 figure, its own 2.75x
related-work figure, and `WILKINSON-STORJ-18`'s own 2x "typical scenario" figure
are three different numbers for the same claimed system, none reconciled
against the other two.

## Not found

No destroyed-precondition pair specific to this family survived a check
against the requirements index closely enough to report. The candidates
considered and rejected: a possible tension between `DIMAKIS-TIT-10`'s OMMDS
scheme, which requires a newcomer to connect to n-1 fragment-holders
simultaneously, and `RHEA-USENIXATC-04`'s finding that DHT lookups fail under
heavy churn — rejected because `RHEA-USENIXATC-04` measures routing-layer
lookup completion, not the separate holder-discovery layer `DIMAKIS-TIT-10`
assumes is supplied by an underlying storage substrate, so the two do not
measure the same mechanism. A possible tension between the independent,
uniformly-random fragment placement `WEATHERSPOON-IPTPS-02` and
`RODRIGUES-IPTPS-05` require for their durability figures to hold, and reports
of correlated failure in real deployments — rejected because the only
correlated-failure evidence in this family (`CHUN-NSDI-06`'s own PlanetLab
trace, and `HUANG-ATC-12`'s stated limitation) comes from the same papers that
already state the independence assumption as a caveat, not from a second paper
whose own mechanism removes it.
