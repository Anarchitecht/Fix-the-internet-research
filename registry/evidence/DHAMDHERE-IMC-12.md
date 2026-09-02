## [DHAMDHERE-IMC-12] Measuring the Deployment of IPv6: Topology, Routing and Performance
**Citation:** Amogh Dhamdhere, Matthew Luckie, Bradley Huffaker, kc claffy, Ahmed Elmokashfi, Emile Aben. "Measuring the Deployment of IPv6: Topology, Routing and Performance." ACM Internet Measurement Conference (IMC), 2012. DOI 10.1145/2398776.2398832.
**Retrieved:** full text via users.caida.org PDF
**Source URL:** https://users.caida.org/~amogh/papers/ipv6-IMC12.pdf
**Domain:** L

### What it does
The paper compares the IPv6 network's topology, routing dynamics, and data-plane performance against IPv4's, at a point when IPv6 deployment was still small, to determine whether the IPv6 network was converging toward the structure of the mature IPv4 network or remaining a separate, immature overlay. It builds historical topology snapshots by collecting BGP AS-path data from Route Views and RIPE RIS, applying a majority-filtering method (five samples of AS paths over a three-week window, keeping only paths seen in the majority of samples) to remove backup and transient links, repeated every three months, producing 56 IPv4 snapshots and 36 IPv6 snapshots spanning 1998-2011 (IPv4) and 2003-2011 (IPv6). It classifies AS business type using the authors' own prior algorithm and AS-to-AS business relationships (customer/provider/peer) using Gao's algorithm. For routing dynamics it processes BGP update streams from five networks that reported both IPv4 and IPv6 data throughout the study period (AT&T, Hurricane Electric, NTT-America, Tinet, IIJ), filtering out update bursts caused by monitor session resets using a method from prior work. For performance it runs its own active measurement: fetching a same-origin-AS webserver object of at least 10,000 bytes over both IPv4 and IPv6, alternating protocol, three fetches per server, from five vantage points, then comparing fetch time and RTT.

### Measured results
| Metric | Result | Conditions |
|---|---|---|
| Topology growth model | AS-count and AS-link growth both fit linear-then-exponential curves, with the inflection around 2008; exponents 0.13 (ASes) and 0.16 (AS links) for the post-2008 exponential phase | BGP topology snapshots, 1998-2011 (IPv4) / 2003-2011 (IPv6), majority-filtered as described above |
| Single-player dominance | Hurricane Electric (HE) appeared in 20% to 95% of IPv6 AS paths depending on vantage point; in 2012, HE was added to between 20% and 50% of paths where IPv4 and IPv6 paths for the same pair of endpoints differed | five BGP vantage points providing both IPv4 and IPv6 data since 2003 (Table 1); percentages vary by which vantage point is used |
| Path congruence | only 40-50% of AS-level paths toward dual-stacked origin ASes were identical between IPv4 and IPv6 at time of measurement; up to 95% could become identical if IPv6-capable ASes established IPv6 peerings matching their existing IPv4 peerings | AS-path comparison for dual-stacked origin ASes across the same BGP vantage points, October 2011 snapshot referenced for the "same AS for each VP" figure |
| Performance vs. path congruence | 79% of paths had IPv6 performance within 10% of IPv4 (or better) when the forward AS-level path was identical between protocols; only 63% had comparable performance when the AS-level paths differed | active measurement, five vantage points (a state network in New York, a research network and a commercial ISP in Japan, a commercial network and an enterprise customer in the Netherlands), objects ≥10,000 bytes, three fetches per server alternating protocol, five-second gap between measurements, filtered to exclude measurements with >10% standard error of mean download time (95% confidence) or IPv4/IPv6 object-size mismatch >1%; final dataset 544 dual-stack ASes (233 enterprise/customer, 106 small transit providers, 10 large transit providers, 195 content/access/hosting providers) |
| Relative fetch-time distribution | of paths tested, roughly 5% had IPv6 faster and 21% had IPv4 faster by more than 10% when the AS-level path differed between protocols; 37% were within 10% of each other on the same path, 10% differed by more than 10% on the same path | same active-measurement dataset as above, per Figure 14's four-way breakdown (same-path/different-path × IPv4-faster/IPv6-faster) |
| Reachable-AS-link overlap | 60-70% of IPv4 AS-path links toward dual-stacked origins were already present in the IPv6 topology, without any new BGP peering session being required | same BGP topology dataset, snapshot referenced in Figure 15 |

### Parameters
| Parameter | Value | Source |
|---|---|---|
| Topology snapshot window | 5 AS-path samples over 3 weeks, majority-filtered, one snapshot every 3 months | Section 2, "BGP topology data" |
| Object-size threshold for performance fetches | ≥10,000 bytes, to escape TCP slow start | Section 2, "Performance data" |
| Fetches per webserver | 3, alternating IPv4/IPv6 sequentially, ~5 s gap between measurements | Section 2, "Performance data" |
| Filtering threshold for performance data | excluded if standard error of mean download time >10% at 95% confidence, or IPv4/IPv6 object sizes differ by >1% | Section 2, "Performance data" |
| Webservers tested per origin AS | up to 3, drawn from the Alexa top 1-million list | Section 2, "Performance data" |
| Active-measurement tools | scamper's `tbit` (page fetch with TCP SACK/timestamps negotiated, full packet trace) and `traceroute` | Section 2, "Performance data" |

### Stated limitations
The authors state that Route Views/RIPE RIS BGP data is known from prior work to inadequately expose the complete Internet topology, missing a significant fraction of peering and backup links at the edge; they mitigate this by focusing on customer-provider links, which they argue dominate the collected data, and note that any counts derived from this data are at worst lower bounds. They state they cannot determine, from the data available, why IPv6 deployment lags at the network edge, and offer a lack-of-incentive explanation as a conjecture rather than a measured finding. They state that a single dominant player (Hurricane Electric) can significantly skew graph-theoretic metrics such as average AS-path length computed over the IPv6 topology, which the reader must account for when comparing IPv6 topology statistics to IPv4's. Future work stated: continued periodic release of topology/routing data, measurement of whether deployment accelerated after World IPv6 Launch (June 2012, after this paper's writing), a quantitative organization-level adoption model, and extension of performance measurement to loss, fragmentation, and reordering causes beyond RTT.

### Requirements it places on the rest of the system
A design that assumes an IPv4 and an IPv6 path between the same pair of ASes traverse the same intermediate networks cannot rely on that assumption for this paper's measurement period: only 40-50% of such paths were identical, so protocol-specific routing decisions (congestion control tuned to one protocol's path characteristics, or a latency budget derived from one protocol) cannot be transferred to the other protocol without checking path congruence first. A design relying on the IPv6 topology having redundancy or path diversity comparable to IPv4's must account for the observed single-player dominance: Hurricane Electric's presence in up to 95% of measured IPv6 AS paths (from some vantage points) means many nominally distinct IPv6 routes share one transit AS, so IPv6 path diversity computed by naive AS-path counting overstates independence relative to a design that needs disjoint failure domains.

### Contradicts
None found. This paper corroborates rather than contradicts CZYZ-SIGCOMM-14's performance-methodology citation (Nikkhah et al.) and states its own performance result (79%/63% path-congruence split) is a confirmation, not a contradiction, of that prior work.

### References worth retrieving
- **Foundational** — Amogh Dhamdhere, Constantine Dovrolis. "Twelve Years in the Evolution of the Internet Ecosystem." IEEE/ACM Transactions on Networking, 19(5), 2011. — source of the AS business-type classification algorithm and majority-filtering method this paper reuses.
- **Foundational** — Lixin Gao. "On Inferring Autonomous System Relationships in the Internet." IEEE/ACM Transactions on Networking, 9(6), 2001. — source of the AS relationship (customer/provider/peer) classification algorithm this paper reuses.
- **Competing** — Mehdi Nikkhah, Roch Guérin, Yiu Lee, Richard Woundy. "Assessing IPv6 through web access: a measurement study and its findings." CoNEXT 2011. — the performance-measurement methodology this paper follows and confirms (also cited by CZYZ-SIGCOMM-14).
- **Foundational** — Matthew Luckie. "Scamper: a scalable and extensible packet prober for active measurement of the Internet." IMC 2010. — the tool used for the active `tbit`/traceroute measurements.
- **Foundational** — Ahmed Elmokashfi, Amund Kvalbein, Constantine Dovrolis. "BGP churn evolution: A perspective from the core." IEEE/ACM Transactions on Networking, 20, 2011. — churn-normalization method the routing-dynamics section applies.
- **Attack or critique** — H. Chang, W. Willinger. "Difficulties Measuring the Internet's AS-Level Ecosystem." Annual Conference on Information Sciences and Systems, 2006. — one of several sources this paper cites as documenting BGP-collector topology bias.
- **Attack or critique** — Y. He, G. Siganos, M. Faloutsos, S. V. Krishnamurthy. "A Systematic Framework for Unearthing the Missing Links: Measurements and Impact." NSDI 2007. — cited alongside the above for the same missing-links critique of public BGP data.

### Verbatim extracts
"Hurricane Electric currently appears in between 20% and 95% of IPv6 AS paths"
"79% of paths we observed had IPv6 performance within 10% of IPv4"
"only 40-50% of AS paths are currently identical in IPv4 and IPv6, up to 95% of AS paths could be identical"
"the exponents for ASes and AS links are 0.13 and 0.16, respectively"
"This filtering left us with 544 dual-stack ASes represented in our dataset"
