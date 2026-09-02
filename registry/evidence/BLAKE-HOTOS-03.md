## [BLAKE-HOTOS-03] High Availability, Scalable Storage, Dynamic Peer Networks: Pick Two

**Citation:** Charles Blake, Rodrigo Rodrigues. "High Availability, Scalable Storage, Dynamic Peer Networks: Pick Two." Workshop on Hot Topics in Operating Systems (HotOS IX), 2003.
**Retrieved:** full text via https://www.usenix.org/legacy/events/hotos03/tech/blake.html
**Source URL:** https://www.usenix.org/legacy/events/hotos03/tech/blake.html
**Domain:** C

### What it does

The paper derives a lower bound on the per-node bandwidth a cooperative storage system needs to spend maintaining redundancy against membership turnover, so a designer can check whether a target combination of data scale, redundancy level, and host turnover rate is reachable with a given per-host bandwidth budget before building the system. The bound follows from a resource-usage model, not from an implementation.

The base model holds `N` identical hosts cooperatively storing `D` bytes of unique data with redundancy expansion factor `k` (replication factor or coding expansion), for `S = kD` bytes of total contributed storage. Hosts join at rate `α` and leave at rate `λ`, with `α = λ` holding the population size constant; average membership lifetime is `T = N/λ`. Every join requires downloading the joining host's assigned share of data, `S/N` bytes on average; every leave requires copying that departing host's `S/N` bytes to replacement hosts to avoid a permanent redundancy loss. Summing both directions gives total maintenance bandwidth `2S/T`, or per-node bandwidth `B/N = 2(S/N)/T` — twice the average per-host storage contribution divided by the average membership lifetime (Equation 1).

The model is then extended to separate transient disconnection from permanent departure using a membership timeout `τ`: a host is treated as still a member, and its data is not re-replicated, until it has been unreachable longer than `τ`. Delaying response to failure this way lengthens the effective average lifetime (`Tτ`) but also means only a fraction of members — the availability `a` — are actually serving data at any instant, so replacing `B` with `aτB` and re-deriving redundancy needed for a per-object unavailability target `ϵa` yields, for pure replication, `ka = log(ϵa) / log(1 - aτ) ≈ log(1/ϵa) / aτ` (Equation 2), and a resulting per-node bandwidth `Bτ/Nτ = (2D / (Nτ·aτ·Tτ)) · log(ϵa)/log(1-aτ)` (Equation 3). For erasure coding, where an object is split into `b` blocks stored with effective redundancy factor `kc` and reconstructed from any `m ≈ b` available blocks out of `kc·b` stored, the analogous redundancy factor is derived from the normal approximation to the binomial distribution as a function of `b`, `a`, and `σϵ` (the number of standard deviations of the normal distribution corresponding to the target availability, e.g. `σϵ = 4.7` for six nines) (Equations 4-5).

### Measured results

| Result | Conditions |
|---|---|
| Storing 1 TB of unique data at high availability is described as effectively infeasible with Gnutella-like participation and cable-modem-like bandwidth, per the derived model | model parameters `Nτ`, `aτ`, `Tτ` estimated from an original crawler-and-prober measurement of ~33,000 Gnutella hosts, conducted April 11-19, 2003, methodology adapted from Saroiu, Gummadi, Gribble (2002) with a crawler extended to capture the entire membership for a precise host-count estimate |
| Discriminating true departure from transient downtime (increasing the membership timeout τ) yields up to roughly a 30x reduction in maintenance bandwidth | same Gnutella trace, target: 1 TB unique data at 6 nines (99.9999%) per-object availability, replication-style redundancy, varying leave timeout from near 0 to 30 hours (Figure 2) |
| At large τ, erasure coding at b=15 fragments needs a redundancy factor of about 15 to match the availability that replication needs a redundancy factor of about 120 for — an 8-fold bandwidth saving from coding over replication on this trace | same Gnutella trace and target (6 nines, 1 TB unique data), b=15 fragments, comparing replication vs. erasure coding redundancy factors (Figure 3) |
| With coding, maintaining 1 TB of unique data at Gnutella-like participation requires about 75 Kbps per-node maintenance bandwidth while up, contributing about 500 MB of disk per host | same trace, coding at b=15, large τ |
| 5% of the 33,000 Gnutella hosts (about 6,000 hosts) provided 40% of total service time (29 of 72 total service-years) in a 3-day subset of the trace; average availability of that top-5% subset was about 40% | same Gnutella crawl/probe trace, 3-day subset used for the service-time-by-host-fraction measurement (Figure 4) |
| Restricting to the top 5% of hosts with a 1-day membership timeout reduces required bandwidth to about 30 Kbps per node per unique TB using coding — roughly a 1,000-fold improvement in maintenance bandwidth over the least favorable point (short timeout) in Figure 2 | same trace, admission-control scenario: top-5%-availability subset only, 1-day timeout, coding |
| Stricter admission control identifies a subset of 967 Gnutella hosts with 99.5% availability, exceeding measured enterprise availability from a cited prior study, at the cost of a 10-fold reduction in aggregate service time versus using all hosts | same Gnutella trace, admission-control analysis restricting to the most-available hosts |
| Disk capacity for a "typical" user grew roughly 8,000-fold from 1990 to a projected 2005 figure, while home/academic access bandwidth grew only about 50-fold over the same period (Table 1: disk 60 MB in 1990 to 0.5 TB in 2005; home bandwidth 9.6 Kbps in 1990 to 384 Kbps in 2005) | figures the paper states as "generous bandwidth estimates," a trend table constructed from historical/projected typical consumer hardware, not a controlled experiment |

### Parameters

| Parameter | Definition | Value(s) used |
|---|---|---|
| `k` | redundancy expansion factor (fixed baseline scenario, Figure 1) | 20 |
| Data scales examined (Figure 1) | total unique data stored | 1 TB, 50 TB, 1000 TB |
| Link saturation threshold (Figure 1) | fraction of link capacity maintenance alone may consume | 50% |
| `τ` (leave timeout) range examined (Figures 2-3) | delay before treating a disconnected host as departed | 0 to 30 hours |
| `σϵ` for six-nines availability | standard-deviation count in the normal approximation | 4.7 |
| `b` (erasure code fragments) | blocks per object | 15 (Figure 3 comparison) |
| Gnutella trace host count | distinct hosts crawled | ~33,000 |
| Gnutella trace duration | measurement window | April 11-19, 2003 (about 8 days) |
| Admission-control subset sizes examined | most-available host subsets | top 5% (~6,000 hosts), and a stricter subset of 967 hosts at 99.5% availability |

### Stated limitations

The model rests on explicitly stated simplifying assumptions the authors say are each conservative individually (each would require more, not less, bandwidth if relaxed): identical per-node space and bandwidth contribution across all hosts, when real nodes vary; a constant average join/leave rate, when the relevant bound for a probabilistic guarantee is the worst-case rate, not the average; independence of leave events, when the authors state network and machine failures are not truly independent and that true guarantees would need more redundancy than the model computes; and a constant steady-state population and total data size, when a shrinking population needs more bandwidth and a growing one cannot sustain the model's steady-state assumption indefinitely. The model also excludes query bandwidth entirely, counting maintenance bandwidth only, and the authors state their bandwidth estimate is therefore conservative relative to any real deployed system, which must also serve reads. The paper states the availability-and-redundancy analysis assumes a static data placement strategy — a fixed function from current membership to the set of replicas per block — and does not model dynamic re-placement policies. Admission control and load-shifting strategies are analyzed and found not to change the fundamental bandwidth-scale-dynamics tradeoff; the paper states this explicitly as a conclusion of Section 4.1, not merely as an unexamined possibility.

### Requirements it places on the rest of the system

Any redundancy scheme relying on this paper's bandwidth bound requires an accurate, population-specific measurement of `N` (host count), `a` (fractional availability), and `T` (average membership lifetime) — the paper explicitly computes its own figures from an original Gnutella crawl rather than assuming a generic churn rate, and states the bound is only as good as those inputs. A system that wants the roughly 30x bandwidth saving from distinguishing transient disconnection from permanent departure needs a membership-timeout mechanism (`τ`) that defers re-replication until a host has been unreachable longer than that threshold, which in turn requires the system to track per-host last-contact time and to accept the corresponding increase in expected time-to-repair for genuinely departed hosts. Achieving the modeled improvement from admission control requires a mechanism that measures per-host availability over time and can refuse or deprioritize volatile hosts before assigning them data — the paper states this converts the design "into a garden variety distributed systems problem" of building storage from a smaller number of highly available collaborators, which is a structural consequence of restricting membership, not a property the paper claims comes free. Any comparison between replication-based and erasure-coded redundancy under this model requires knowing both the target per-object unavailability `ϵa` and the block-fragmentation parameter `b`, since the bandwidth advantage of coding over replication (measured at 8-fold on this trace) is a function of those two parameters, not a fixed ratio.

### Contradicts

None found within this batch on a shared measured quantity. This paper's central claim — that combining high redundancy guarantees, large data scale, and fast membership dynamics simultaneously overreaches available bandwidth "regardless of lookup" — is a critique of the premise that distributed hash table (DHT)-based lookup robustness by itself yields storage robustness; it does not report a number that conflicts with a number in another paper in this batch, since its Gnutella measurement (host count, availability distribution, service-time concentration) is on a different network from the Overnet measurements in BHAGWAN-IPTPS-03 and the trace-driven simulation results in BHAGWAN-NSDI-04 and CHUN-NSDI-06. Note for later cross-paper checking: CHUN-NSDI-06 (Carbonite) reports live PlanetLab repair-bandwidth measurements explicitly aimed at the same delayed-repair strategy this paper analyzes only by model: a later synthesis step should check whether Carbonite's measured bandwidth reduction from deferring repair on short departures is of comparable magnitude to this paper's roughly 30x figure derived analytically from the Gnutella trace, since the two are different methodologies (measured live system vs. an analytic bound applied to trace-derived parameters) answering a related but not identical question.

### References worth retrieving

- Bhagwan, Savage, Voelker, "Replication strategies for highly available peer-to-peer storage systems," UCSD Technical Report CS2002-0726, Nov 2002 — foundational (source of the normal-approximation coding-redundancy derivation this paper's Equations 4-5 build on)
- Bhagwan, Savage, Voelker, "Understanding availability," IPTPS 2003 — foundational (already in this corpus as BHAGWAN-IPTPS-03; source of the distinguishing-downtime-from-departure framing this paper adopts)
- Bolosky, Douceur, Ely, Theimer, "Feasibility of a serverless distributed file system deployed on an existing set of desktop PCs," SIGMETRICS 2000 — competing (the enterprise-availability figure this paper's 967-host, 99.5%-availability subset is compared against)
- Dabek, Kaashoek, Karger, Morris, Stoica, "Wide-area cooperative storage with CFS," SOSP 2001 — competing (a DHT-based storage system the paper's introduction cites as an example that hopes to inherit robustness from lookup)
- Rowstron, Druschel, "Storage management and caching in PAST," SOSP 2001 — competing (same category as CFS)
- Saroiu, Gummadi, Gribble, "A measurement study of peer-to-peer file sharing systems," MMCN 2002 — foundational (the prior study whose crawler methodology this paper's own Gnutella measurement is adapted from and extended)
- Weatherspoon, Kubiatowicz, "Erasure coding vs. replication: A quantitative comparison," IPTPS 2002 — competing (the erasure-coding-for-storage proposal this paper's Section 3.3 formula generalizes)
- Ratnasamy, Francis, Handley, Karp, Shenker, "A scalable content-addressable network (CAN)," SIGCOMM 2001 — foundational (one of the DHT lookup systems whose robustness the paper argues does not transfer to storage robustness)
- Stoica, Morris, Karger, Kaashoek, Balakrishnan, "Chord: A scalable peer-to-peer lookup service for internet applications," SIGCOMM 2001 — foundational (already established per BRIEF.md §7)
- Zhao, Kubiatowicz, Joseph, "Tapestry: An infrastructure for fault-tolerant wide-area location and routing," UC Berkeley Technical Report UCB/CSD-01-1141, 2001 — foundational

### Verbatim extracts

- "large-scale cooperative storage is limited by likely dynamics and cross-system bandwidth — not by local disk space"
- "each node joining the overlay must download all the data which it must later serve"
- "discriminating downtime from departure can lead to a factor of 30 savings in maintenance bandwidth"
- "the bandwidth savings are only a factor of 8 for our Gnutella trace"
- "5% of hosts provide 40% of the total service time"
- "leveraging tens of thousands of flaky home users only doubles total data service"
- "we make a number of simplifying assumptions. Each one is conservative"
- "it seems hopeless to field even 1TB at high availability with Gnutella-like participation"
