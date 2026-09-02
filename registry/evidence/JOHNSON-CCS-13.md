## [JOHNSON-CCS-13] Users Get Routed: Traffic Correlation on Tor by Realistic Adversaries

**Citation:** Aaron Johnson, Chris Wacek, Rob Jansen, Micah Sherr, Paul Syverson. "Users Get Routed: Traffic Correlation on Tor by Realistic Adversaries." ACM CCS, 2013. DOI 10.1145/2508859.2516651.
**Retrieved:** full text via https://www.freehaven.net/anonbib/cache/ccs2013-usersrouted.pdf
**Source URL:** https://www.freehaven.net/anonbib/cache/ccs2013-usersrouted.pdf
**Domain:** J

### What it does
The paper measures how quickly a realistic passive adversary deanonymizes a Tor user (Tor is a low-latency onion-routing anonymity network that hides a user's address from the destination by relaying traffic through three volunteer-operated relays: guard, middle, exit). Deanonymization by traffic correlation occurs when the same party observes traffic both entering the network at the guard and leaving it at the exit and links the two observations as the same flow. The authors build a Monte Carlo path simulator, TorPS, that replays historical Tor consensus data (the hourly list of active relays and their properties) and five modeled user-behavior traces through Tor's actual path-selection algorithm, then measures, for each simulated user, the probability distribution over time until a hostile party occupies both the guard and exit position on a circuit (relay adversary) or observes both path segments as a carrier of network traffic without running any relay (network adversary: an autonomous system, an Internet exchange point, or an organization operating several exchange points).

### Measured results
| Result | Conditions |
|---|---|
| More than 80% chance of full deanonymization within 6 months; median time to full compromise always under 70 days, across all five user models | Relay adversary running one guard relay (83.3 MiB/s) and one exit relay (16.7 MiB/s), 5:1 guard-to-exit bandwidth ratio, simulated October 2012-March 2013, TorPS Monte Carlo simulation |
| Median time to compromised guard: 50-60 days; median time to compromised exit: under 2.5 days | Same adversary and period; guard compromise dominates because clients rotate exits far more often than guards |
| Median rate of fully compromised streams: 0.25%-1.5%, varying by user behavior model | Same adversary and period |
| BitTorrent user model: exit compromise at median time under 6 hours, median rate over 12% | Same adversary; BitTorrent trace creates 6,768 streams/week over 118 ports versus 2,632 streams/week over 2 ports for the Typical model |
| Doubling adversary bandwidth roughly halves time to first compromise; at 200 MiB/s, 50% probability of full compromise within 30 days; at 10 MiB/s, under 10% probability of ever compromising a user | Typical user model, adversary bandwidth varied 10-200 MiB/s, same simulated period |
| Adversary entering the network 2 months into the simulation (12/1/2012) still fully compromises the user with ~70% probability over the remaining 4 months, versus ~70% probability for an adversary present from the outset over the full 4 months compared | Typical user model, same simulation infrastructure |
| Worst-case client origin: 45.9% (Typical), 64.9% (IRC), 76.4% (BitTorrent) of samples use a compromised stream within 1 day against a single AS adversary; over 98% compromised within 3 months for all models | 50,000 Monte Carlo simulations per behavior, clients placed at 5 AS origins (4 German, 1 Italian) identified as popular Tor client ASes by Edman and Syverson (2009), January-March 2013 |
| Best-case client origin: IRC users exposed at 44 days median; 38% (BitTorrent) and 44% (Typical) of users still compromised within 90 days despite over 50% evading compromise for the full period | Same AS-adversary simulation, best-case client origin selected by smallest area under the compromise-time CDF |
| Best-case standalone IXP compromises 3.7% of samples within 30 days; best-case IXP organization (a single entity administering multiple exchange points) compromises 12.4% in the same period | 19 identified IXP organizations administering 90 distinct Internet exchange points (IXPs), Typical user model, same simulation period |
| Congestion-Aware Tor (CAT, an alternative path-selection algorithm) shows only a minor reduction in time to first compromise but a markedly larger increase in the total fraction of streams compromised, relative to standard Tor | Relay adversary at 83.3/16.7 MiB/s, Typical user model, congestion profiles built from a Shadow-simulated virtual Tor network (Tor version 0.2.3.25) run until the median Kolmogorov-Smirnov distance between repeated congestion traces fell below 5% |
| Linear regression converting adversary relay bandwidth to consensus selection weight: r² = 0.71 for guard relays, r² = 0.69 for exit relays | Regression fitted against relays in the consensuses spanning the simulation period |

### Parameters
- Adversary bandwidth allocation: 5:1 guard-to-exit ratio, selected after testing 1:1, 2:1, 5:1, 10:1, and 50:1 splits of 100 MiB/s (5:1 maximized the probability of compromising at least one stream over the 6-month test period and was adopted for all subsequent experiments).
- Baseline adversary relay bandwidths in the main experiments: 83.3 MiB/s guard, 16.7 MiB/s exit (from the 5:1 split of 100 MiB/s).
- User models: Typical (2,632 streams/week, 205 unique IPs, ports 80/443), IRC (135 streams/week, 1 IP, port 6697), BitTorrent (6,768 streams/week, 171 IPs, 118 ports), WorstPort (Typical traffic on port 6523, second-least exit capacity excluding rejected ports), BestPort (Typical traffic on port 443, highest exit capacity).
- Simulation window: October 2012-March 2013 for relay-adversary experiments; January-March 2013 for network-adversary experiments, using 50,000 Monte Carlo samples per behavior model.
- Client AS origins: the 5 most popular client ASes identified by Edman and Syverson (2009) — AS3320, AS3209, AS3269, AS13184, AS6805 (4 German, 1 Italian); Chinese ASes excluded because Tor was subsequently blocked in China.
- CAT congestion threshold: a circuit is dropped from use for new streams once the mean of its last 5 round-trip-time congestion measurements exceeds 0.5 seconds.
- Guard expiration parameter cited from Tor's own configuration history: minimum guard expiration time was 30 days at the time of this study and was increased to 60 days in Tor version 0.2.4.12-alpha partly in response to this paper's finding that guard expiration accelerates compromise.

### Stated limitations
The authors state they consider only a passive end-to-end correlating adversary and explicitly exclude circuit clogging, network latency attacks, active traffic alteration by the adversary beyond running relays, and adversarial bridges (Tor entry points not listed in the public consensus) from their adversary model. They state a "comprehensive evaluation of all potential threats against Tor is beyond the goals of this paper." They state their five user-behavior traces are "limited and somewhat artificial," each built from only 20 minutes of recorded activity replayed on a schedule. They state historical relay-congestion data does not exist for the study period, so CAT's congestion profiles are synthetic (from a separate Shadow simulation) rather than drawn from the same historical period as the relay-adversary experiments. They state hidden services and bridges are not considered. They identify, but explicitly place outside their adversary model and leave unresolved, an active attack in which an adversary already on a circuit degrades the response time of circuits it has not compromised to bias congestion-aware clients toward re-selecting compromised circuits.

### Requirements it places on the rest of the system
A capacity-weighted relay-selection mechanism that keeps a client's entry point fixed for tens of days (Tor's guard rotation, measured here at a 30-60 day tenure) concentrates deanonymization risk on whichever party is chosen during that tenure, so any design reusing guard-style fixed-entry selection must treat the guard-rotation interval as a directly load-bearing security parameter, not a performance-only tuning knob — this paper measures that increasing it from 30 to 60 days was adopted by the Tor Project specifically to increase time to first compromise. A path-selection algorithm that reacts to observed network conditions (Congestion-Aware Tor's round-trip-time measurement) requires that congestion measurement itself be resistant to adversarial manipulation, because a relay under adversary control can manufacture apparent congestion on circuits it does not control to bias client circuit selection toward relays it does control; this paper identifies that requirement as unmet and out of scope for its own security model. A traffic-correlation-resistant overlay routed above the transport layer requires knowledge of the underlying autonomous-system and Internet-exchange-point topology to reason about correlation risk, because two Tor relays chosen for AS-level diversity can still share a network-level adversary if traffic from both traverses the same exchange point or the same multi-exchange-point-owning organization.

### Contradicts
The paper states its results show Tor users are "far more susceptible to compromise than indicated by prior work" that modeled adversaries as independent per-AS entities rather than as adversaries who might operate several ASes or exchange points simultaneously; that prior-work estimate is not evaluated as a specific figure in this batch. No other paper in this batch measures Tor guard-compromise or exit-compromise timing, so no cross-paper numeric contradiction exists in this batch. This paper's guard-compromise-dominates-exit-compromise finding is consistent with, and cites, Elahi et al.'s (ELAHI-WPES-12) argument that guard selection is the primary bottleneck to full deanonymization.

### References worth retrieving
- foundational: Syverson, Tsudik, Reed, Landwehr. "Towards an Analysis of Onion Routing Security." Designing Privacy Enhancing Technologies, 2000.
- competing: Wang, Bauer, Forero, Goldberg. "Congestion-aware Path Selection for Tor." Financial Cryptography and Data Security (FC), 2012. (the CAT algorithm this paper evaluates)
- competing/related measurement: Wacek, Tan, Bauer, Sherr. "An Empirical Evaluation of Relay Selection in Tor." NDSS 2013.
- attack: Murdoch, Zieliński. "Sampled Traffic Analysis by Internet-Exchange-Level Adversaries." Privacy Enhancing Technologies (PET), 2007.
- attack: Murdoch, Danezis. "Low-Cost Traffic Analysis of Tor." IEEE S&P (Oakland), 2005.
- independent-measurement: Elahi, Bauer, AlSabah, Dingledine, Goldberg. "Changing of the Guards." WPES 2012. (already a target in this batch: ELAHI-WPES-12)
- foundational (simulation infrastructure): Jansen, Hopper. "Shadow: Running Tor in a Box for Accurate and Efficient Experimentation." NDSS 2012.
- attack: Wright, Adler, Levine, Shields. "The Predecessor Attack." ACM TISSEC 4(7), 2004.

### Verbatim extracts
- "Tor users are far more susceptible to compromise than indicated by prior work"
- "there is more than an 80% chance of deanonymization within 6 months by a malicious guard and exit"
- "the time it takes to choose a malicious guard, with a median of 50-60 days, dominates"
- "at 200MiB/s the adversary fully compromises a user within 30 days with probability 50%"
- "standalone IXPs are able to compromise just 3.7% of samples within 30 days, while organizations compromise 12.4%"
- "we do not consider circuit clogging, network latency, or application... attacks against Tor"
- "the Congestion-Aware Tor proposal exacerbates these vulnerabilities"
