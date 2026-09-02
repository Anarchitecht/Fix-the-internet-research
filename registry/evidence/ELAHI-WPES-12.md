## [ELAHI-WPES-12] Changing of the Guards: A Framework for Understanding and Improving Entry Guard Selection in Tor

**Citation:** Tariq Elahi, Kevin Bauer, Mashael AlSabah, Roger Dingledine, Ian Goldberg. "Changing of the Guards: A Framework for Understanding and Improving Entry Guard Selection in Tor." ACM WPES, 2012. Pages 43-54. DOI 10.1145/2381966.2381973.
**Retrieved:** full text via https://cypherpunks.ca/~iang/pubs/cogs-wpes.pdf
**Source URL:** https://cypherpunks.ca/~iang/pubs/cogs-wpes.pdf
**Domain:** J

### What it does
The paper measures how much of a Tor client's exposure to a malicious entry guard (a fixed relay a client uses as its long-term first hop) comes from ordinary relay churn versus from Tor's own scheduled guard rotation. The authors build COGS (Changing Of the Guards), a Tor-client path-selection simulator built on Tor's own source code (version 0.2.2.33), that replays real hourly consensus documents and relay descriptors from the live Tor network and simulates guard selection and rotation for tens of thousands of clients under configurable adversary and parameter settings, then logs which simulated clients have a malicious relay in their currently active guard list at each hour. A client is counted as compromised the instant any malicious relay appears in the first N online entries of its guard list (N being the client's configured number of guards), because the authors treat even brief exposure as potentially security-relevant.

### Measured results
| Result | Conditions |
|---|---|
| Guard relay uptime/downtime statistics: median guard down time 3 hours, median guard up time 20 hours (mean 42.17h down, 156.7h up); general relay population median down 10 hours, median up 4 hours (mean 45h down, 19.82h up) | Tor Metrics Portal consensus data, April-November 2011, relays present throughout the period |
| Fraction of active guard lists compromised increases monotonically over an 8-month simulated period, both with and without guard rotation, with guard rotation producing a markedly higher compromise curve that peaks around late May and then reaches a steady state | COGS simulation, 80,000 simulated clients, malicious relay bandwidth fixed at 100 weighted bandwidth units (WBU, approximately top 20% of guard bandwidth), introduced one hour into the simulation, guard-only flag, April-November 2011 real consensus replay |
| With standard 30-60-day guard rotation, a client is expected to see 12 to 24 unique guards over 8 months (average 17); without rotation, minimum 3 guards per client | Derived from Tor's guard-list size (3) and the 30-60-day rotation window over the 8-month simulation period |
| With guard rotation, mean number of guards seen per client rises to 19; without guard rotation, mean rises only to 5 (versus a minimum of 3) | Same COGS simulation, client guard-exposure log over April-December 2011 |
| Increasing guard list size (1, 2, 3, 5, 10 guards) increases compromise rate when guard rotation is on; with guard rotation off, guard list sizes above 3 initially show lower compromise, an effect the authors observe does not persist over time as guards fail and get replaced | Same COGS simulation, independent runs per guard-list-size setting |
| Only about 9% of guards remained part of the Tor network for the full 8-month study period; median guard longevity 1,371 hours (~57 days) | Guard longevity CDF computed from the same April-November 2011 consensus data |
| Median guard bandwidth across all consensuses in the 8-month period peaked at 113 WBU; a client with 3 or more guards always exceeds this bandwidth on average, while 5% of single-guard clients fall below it | Same dataset, guard bandwidth statistics (min 40, median 67, mean 68.31, max 113 WBU) |
| Tor with 1 guard versus 3 guards: 1-guard clients experience 60% worse expected circuit bandwidth 50% of the time, but 25% more average guard-list bandwidth the other 50% of the time | Same COGS simulation, expected circuit performance measured with and without guard rotation across guard-list sizes |
| Compromise rate increases with adversarial bandwidth (tested at 10, 100, and 1,000 WBU) but not linearly | Same COGS simulation, adversarial-bandwidth sweep, April-July 2011 window |

### Parameters
- Simulated client population: 80,000 clients per run, chosen by increasing the sample size until the resulting compromise-rate distributions stabilized according to the Kolmogorov-Smirnov distance test.
- Simulation period: April 2011-November 2011 (8 months), chosen for relatively stable network bandwidth and a consistent consensus format version.
- Simulation granularity: 1 hour, matching consensus document publication frequency.
- Malicious relay: introduced 1 hour after simulation start (after clients already hold honest guards, establishing what the authors describe as a conservative, lower-bound compromise-rate estimate), assigned only the guard flag (not exit, to avoid confounding selection probability), bandwidth held constant at 100 WBU for most experiments (varied to 10 and 1,000 WBU in one sweep), representing approximately the top 20% of guard bandwidth.
- Guard list size tested: 1, 2, 3 (Tor default), 5, and 10 guards, with and without guard rotation.
- Guard rotation window (Tor's default parameter at the time of this study): guards are dropped between 30 and 60 days of age.
- Client model: constant population (no churn of clients themselves, only of relays), clients simulated as always online (stated as a worst-case assumption relative to real intermittently-connected clients).

### Stated limitations
The authors state they did not vary the guard rotation period itself in this paper and explicitly leave a rotation mechanism independent of relay stability and network characteristics to future work. They state it is "unclear how to best model the client behaviour" for join/leave dynamics and adversary insertion timing, and describe this as an open research problem outside this paper's scope; they used a fixed client population with the adversary entering after all clients already hold guards, and state that "counterintuitive properties" they observed (larger guard lists reducing compromise rates when rotation is off) "may not hold for other conditions" of client and adversary modeling. They state it is unclear whether low-bandwidth guards, despite rarely being solely responsible for a client's active list bandwidth, provide load-balancing or relay-diversity security benefits, and cite this as an avenue for future investigation. They state their choice to model the adversary as a single high-bandwidth relay (rather than many low-bandwidth relays with equivalent total bandwidth) relies on an equivalence result from Murdoch and Watson (PETS 2008) rather than on an independent derivation in this paper.

### Requirements it places on the rest of the system
Any capacity-ordered relay-selection mechanism that keeps a client's first hop fixed for a multi-week tenure (Tor's guard-flag design, measured here) requires the tenure length itself to be treated as a tunable security parameter with a measured trade-off against performance, because this paper measures that increasing the number of guards a client rotates through over a fixed period directly increases the number of relays capable of compromising that client, while reducing rotation frequency or guard-list size directly reduces average circuit bandwidth. A mechanism that selects relays for a persistent role in proportion to self-reported or measured bandwidth (Tor's bandwidth-weighted guard selection) requires that a small set of injected high-bandwidth malicious relays be assumed at least as effective as many low-bandwidth ones at equal aggregate bandwidth, an assumption this paper adopts from prior work rather than independently testing. A design relying on relay uptime/downtime stability to justify a long-lived special role (the entry-guard role, justified by relays' longer up-times and shorter down-times relative to the general relay population, measured here in Table 1) still exhibits enough natural churn that a persistent adversary is guaranteed eventual appearance in every client's guard list given sufficient elapsed time, independent of any scheduled rotation mechanism.

### Contradicts
None found. This paper's finding that guard rotation contributes more to compromise risk than natural churn alone is consistent with, and is cited as support for, the guard-compromise-dominates finding in JOHNSON-CCS-13 (which measures median guard-compromise time of 50-60 days against median exit-compromise time under 2.5 days, on the live Tor network rather than in simulation); no numeric figure in this batch contradicts another entry.

### References worth retrieving
- foundational: Wright, Adler, Levine, Shields. "Defending Anonymous Communications against Passive Logging Attacks." IEEE S&P 2003. (introduces "helper nodes," the predecessor of entry guards)
- foundational: Wright, Adler, Levine, Shields. "The predecessor attack: An analysis of a threat to anonymous communications systems." ACM TISSEC 7(4), 2004.
- foundational: Øverlier, Syverson. "Locating Hidden Servers." IEEE S&P 2006. (proposes entry guards for onion routing)
- attack: Bauer, McCoy, Grunwald, Kohno, Sicker. "Low-Resource Routing Attacks against Tor." WPES 2007. (Sybil attack replacing honest guards via inflated self-reported bandwidth)
- attack: Borisov, Danezis, Mittal, Tabriz. "Denial of service or denial of security?" ACM CCS 2007. (selective DoS attack interaction with entry guards)
- foundational (equivalence result used as a simulation assumption): Murdoch, Watson. "Metrics for security and performance in low-latency anonymity networks." PETS 2008.
- competing/related: Edman, Syverson. "AS-awareness in Tor path selection." ACM CCS 2009.
- attack: Danezis, Syverson. "Bridging and Fingerprinting: Epistemic Attacks on Route Selection." PETS 2008.

### Verbatim extracts
- "we empirically demonstrate that natural, short-term entry guard churn and explicit time-based entry guard rotation contribute to clients using more entry guards than they should"
- "guard rotation increases the visibility of each client on average to 19 guards"
- "only about 9% of guards remained part of the Tor network for the entire 8-month duration"
- "Tor with one guard offers the least likelihood of compromised guard lists"
- "we did not vary guard rotation periods in this paper"
- "it is unclear how to best model the client behaviour"
