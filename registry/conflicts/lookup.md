# Conflicts: lookup family

Scope: distributed-hash-table lookup latency, hop count, publication and retrieval latency,
routing success under a stated adversary fraction, eclipse-attack effectiveness, churn tolerance,
routing-table poisoning, the disjoint-path success formula, and proximity neighbour selection.

Every entry opened for this family: `CASTRO-OSDI-02`, `GUMMADI-SIGCOMM-03`, `HEEP-ATNAC-10`,
`RHEA-USENIXATC-04`, `LI-INFOCOM-05`, `SIT-IPTPS-02`, `URDANETA-CSUR-11`, `HEILMAN-USENIXSEC-15`,
`MARCUS-EPRINT-18`, `SINGH-INFOCOM-06`, `CORTESGOICOECHEA-ARXIV-24`, `BALDUF-IMC-23`,
`TRAUTWEIN-SIGCOMM-22`, `TRAUTWEIN-INFOCOM-24`, `WEI-NSDI-24`, `STEINER-CCR-07`, `STEINER-IMC-07`,
`STUTZBACH-IMC-06`, `LI-EPRINT-25`, `KROL-EUROSP-24`, plus a pass over the full measurement and
requirements indexes for domains A, J, and L.

## Measurement disagreements

### IPFS Kademlia DHT cloud-hosting share of DHT server nodes

`BALDUF-IMC-23` crawls the live IPFS DHT (101 crawls, 2023-04-18 to 2023-05-26) and reports 79.6%
of DHT servers cloud-hosted (20,300 of an average 25,510 crawled nodes, its own "average-unique-
nodes-per-crawl" counting method) or 39.9% (34,375 of 86,064 addresses) when it re-derives the same
2023 crawl data using the counting method `TRAUTWEIN-SIGCOMM-22` used — global-unique-IP across all
crawls. `TRAUTWEIN-SIGCOMM-22` crawls the same live DHT roughly two years earlier (9,500 crawls,
2021-07-09 to 2022) and reports under 2.3% of nodes cloud-hosted. Both papers classify hosting with
the same Udger IP-to-provider database, so the classification tool is not the source of the gap.

`BALDUF-IMC-23`'s own text attributes the entire disagreement to counting methodology and crawl
frequency, not to a change in the network between the two measurement windows. That attribution is
not independently checked anywhere in this corpus: even after `BALDUF-IMC-23` matches
`TRAUTWEIN-SIGCOMM-22`'s own counting method, the residual gap is 39.9% against under 2.3%, a
seventeen-fold difference the methodology match does not close, over a twenty-month interval on a
deployment whose participant population the corpus elsewhere shows churns heavily. A synthesis
citing an IPFS cloud-hosting rate should use `BALDUF-IMC-23`'s 2023 figures, because that paper ran
its own crawl under both counting methods and is closer to any 2026 deployment date; it should not
average the two papers' figures or treat the disagreement as resolved by the methodology
explanation alone.

### KAD/eMule Kademlia-DHT deployed network size

`STEINER-CCR-07` and its companion `STEINER-IMC-07` crawl the entire live KAD identifier space and
report "we found between 3 and 4.3 million different peers" per full crawl, stating separately that
1.5 to 2 million of those were directly reachable (not behind NAT or a firewall). `URDANETA-CSUR-11`,
a survey, restates this as "KAD DHT estimated size: 1.5 million nodes (Steiner et al. 2007)" and
contrasts it with "4 million nodes (Crosby and Wallach 2007)," without stating Crosby and Wallach's
own methodology.

Read against `STEINER-CCR-07`'s own text, the 1.5 million figure the survey uses as "estimated size"
looks like Steiner's NAT/firewall-free reachable subset, not Steiner's own headline total-population
figure of 3 to 4.3 million — a total that sits close to, not far from, the 4 million the survey
poses as the disagreeing figure. This is not a case of two measurement studies disagreeing about KAD's
size; it is the survey collapsing two of Steiner's own numbers (total found, and reachable subset)
into one "estimated size" figure and comparing that figure against a different study's total. A
synthesis wanting deployed-KAD network size should cite `STEINER-CCR-07`/`STEINER-IMC-07` directly
and state which of the two Steiner figures it means, not cite `URDANETA-CSUR-11`'s paraphrase.
`CASTRO-OSDI-02`'s own evidence entry independently makes the same general point about preferring
the primary source over `URDANETA-CSUR-11`'s paraphrase, for a different set of figures (the
0.77/0.12 false-positive pair and the 2.7-extra-hops figure), which that survey does restate
correctly.

### Kademlia DHT lookup hop count, live network against a simulator calibrated against it

`CORTESGOICOECHEA-ARXIV-24` measures both sides of exactly the comparison this family was asked to
watch for, inside one paper. On the live IPFS DHT (100 sets of 80 concurrent lookups, a single AWS
node, 3 October 2023), 99% of lookups complete in under 18 hops, with a 1% tail reaching up to 100
hops. In the paper's own discrete-event simulator, calibrated against that live measurement
(100 sets of 200 concurrent lookups, k=20, alpha=3, beta=20, a 10% connection-refusal rate injected),
the 99th percentile is 12 to 14 hops.

The two figures are not directly comparable: the simulator run uses 200 concurrent lookups against
the live run's 80, and the simulator's fixed 10% refusal rate is a modeling choice, not a measured
property of the live network's actual failure modes. The paper does not reconcile the two tails.
A synthesis using this paper's simulator to project lookup-hop behavior at Ethereum-DAS scale should
treat the simulator's 12-to-14-hop 99th percentile as an optimistic figure next to what the live
network's own 1% tail showed (up to 100 hops), because the paper's headline "10-14 minutes to
complete" worst-case seeding-latency projection and its "50 to 70 times the slot deadline" claim are
both built on the simulator side of this same gap.

### Proximity neighbour selection: latency benefit against eclipse-defense effectiveness

`GUMMADI-SIGCOMM-03` measures proximity neighbor selection (PNS) as a latency optimization under
real-world latency distributions and finds it large: on the XOR routing geometry, PNS lowers median
path latency from 1036 ms to 139 ms measured from a Virginia vantage point, and from 1725 ms to
385 ms from a Japan vantage point, on a 16,384-node network. `SINGH-INFOCOM-06` measures PNS as an
incidental eclipse-attack defense — whether PNS's proximity bias keeps a malicious node's entries out
of a correct node's routing table — and finds it fails under the same kind of real-world latency data:
using King-tool-measured real Internet latencies rather than a synthetic GT-ITM topology, PNS's
eclipse-defense effect is "significantly reduced," and the paper's own conclusion is that "the
effectiveness of the PNS-based defense diminishes with increasing overlay size" and that a PNS-only
defense "will not be effective in the real Internet."

These are not contradictory results. They measure different quantities: `GUMMADI-SIGCOMM-03` measures
path latency under ordinary, non-adversarial conditions; `SINGH-INFOCOM-06` measures the fraction of
malicious routing-table entries under an active 20%-malicious eclipse attack. A design can get
Gummadi's latency benefit and still get eclipsed the way Singh measures, because the same proximity
bias that shortens paths under normal conditions also lets a well-positioned nearby attacker present
itself as the closest candidate. A synthesis should not cite `GUMMADI-SIGCOMM-03`'s latency figures as
evidence that PNS also protects against eclipse attacks; `SINGH-INFOCOM-06` measured that specific
claim directly and found it false under real Internet latency data.

## Destroyed preconditions

### Recursive routing removes the observable-lookup-progress defense

`SIT-IPTPS-02` states, as its design principle 2, that a querier must be able to observe lookup
progress hop by hop, so it can detect a lookup a malicious node has diverted away from converging on
the target key. The paper states this check is enforceable only under iterative routing, where each
hop reports the next hop back to the querier, and states explicitly that the check "is impossible"
under a recursive-forwarding design (the paper's example is CAN's proposed round-trip-time-optimized
recursive forwarding).

`HEEP-ATNAC-10`'s R/Kademlia is built specifically on recursive routing in place of Kademlia's
original iterative routing, and its measured latency and bandwidth advantage over iterative Kademlia
comes from that switch: at the paper's default churn setting, R/Kademlia's recursive routing with
proximity neighbor selection reaches roughly 225 ms mean latency against roughly 415 ms for iterative
routing with the same proximity mechanism. The paper's own description of recursive routing states
that "the initiator loses control of the message after the first hop" — precisely the property
`SIT-IPTPS-02`'s principle 2 requires the querier to retain.

A system cannot adopt R/Kademlia's recursive-routing performance advantage and `SIT-IPTPS-02`'s
per-hop-progress liveness defense at the same time; the mechanism that produces R/Kademlia's latency
and bandwidth reduction is the same mechanism `SIT-IPTPS-02` names as the thing that removes
progress observability. `HEEP-ATNAC-10` is a pure performance paper and does not discuss an adversarial
model or an alternative liveness defense for recursive routing. `CASTRO-OSDI-02` shows one way to
resolve this: it also adopts recursive-style routing on Pastry and, instead of Sit's per-hop check,
substitutes a statistical routing-failure test plus redundant neighbor-set-anycast routing, reaching
better-than-99.9%-of-replicas-reached success at up to 30% malicious nodes on a 100,000-node network.
A synthesis selecting R/Kademlia's routing style needs to either adopt an equivalent substitute
defense, accept degraded resistance to a misdirecting malicious forwarder, or record the gap as an
open problem.

### RHEA's Poisson churn model is the model STUTZBACH's own measurements say is wrong

`RHEA-USENIXATC-04`'s churn-handling results for Bamboo — its comparison against FreePastry and MIT
Chord, its reactive-versus-periodic-recovery findings, and its timeout-calculation comparisons — are
all produced under a Poisson node-death process: a memoryless, exponentially-distributed churn model
the paper's own limitations section calls "a relatively simple churn model" and states is a
simplification of real churn, citing an anonymous reviewer's suggestion (not adopted at the time of
writing) to use scaled traces of observed session times instead.

`STUTZBACH-IMC-06` measures real session-length distributions across five Gnutella datasets, four Kad
datasets, and three BitTorrent tracker logs, using two bias-corrected measurement methods (unbiased
peer selection and a create-based correction for censored long sessions). It finds session lengths in
every system fit a Weibull distribution, not an exponential one, with shape parameters below 1
(0.34–0.59 for the three BitTorrent datasets), meaning the true distribution departs more sharply from
memorylessness than an exponential model predicts. The paper's own "Requirements it places on the rest
of the system" section states directly: "a component that assumes session lengths are exponentially or
Poisson-distributed ... is contradicted by this paper's fitted Weibull/log-normal distributions," and
its bibliography names `RHEA-USENIXATC-04` by title as a churn-resilience mechanism whose "assumed
churn model this paper's measurements can validate or contradict."

The two papers do not directly disagree on a shared number — `RHEA-USENIXATC-04` never claims its
Poisson model matches deployed churn — but `RHEA-USENIXATC-04`'s own reported figures (its
mean-session-time sweep from 1.4 minutes to 3 hours, its FreePastry-versus-Chord-versus-Bamboo
comparison) are conditioned on a churn model `STUTZBACH-IMC-06` shows the underlying real systems do
not follow. `HEEP-ATNAC-10`, published six years after `RHEA-USENIXATC-04`, already resolves this for
its own results: it explicitly adopts a Weibull churn model (shape k=0.5) sourced from
`STUTZBACH-IMC-06`'s own measurement work rather than a Poisson model. A synthesis citing
`RHEA-USENIXATC-04`'s specific churn-rate thresholds (for example, the point at which reactive
recovery's bandwidth "jumps dramatically") should treat them as qualitative, not quantitatively
transferable to a deployment with a measured Weibull churn distribution, unless the same experiment is
re-run under that distribution the way `HEEP-ATNAC-10` did.

## Unsupported attribution

### LI-EPRINT-25 claims DISC-NG has no security analysis; DISC-NG's own text has one

`LI-EPRINT-25`'s own evidence entry states, describing `KROL-EUROSP-24` (DISC-NG): "this paper states
DISC-NG contains no comparison to dedicated single-service overlays and no security analysis." That
sentence is `LI-EPRINT-25`'s own characterization of DISC-NG's related-work discussion, not something
independently checked against DISC-NG's own text at the time it was extracted.

`KROL-EUROSP-24`'s own retrieved text contains an extensive security analysis. It reports eclipse-rate
measurements comparing DISC-NG against a plain DHT baseline, a DHT-plus-admission-control variant
(DHTTicket), and Ethereum's deployed DISCv5 protocol, at 20%, 33.33%, and 50% Sybil-node fractions
(DHT baseline reaching up to 59.7% eclipse rate; DISC-NG staying under roughly 0.5% across the same
range, per the paper's own stated prose). It separately tests robustness under non-uniform Sybil
placement concentrated near a target service identifier, where the DHT and DHTTicket baselines reach
100% eclipse and DISC-NG reaches 0%. It states and uses two liveness theorems (Theorems 2 and 3) under
an explicit partial-synchrony threat model with a named assumption (Assumption 2) about the underlying
DHT's own eclipse resistance.

The claim "no security analysis" is not supported by `KROL-EUROSP-24`'s own text. The other half of
`LI-EPRINT-25`'s characterization — that DISC-NG has no comparison to a dedicated single-service
overlay of the kind `LI-EPRINT-25` itself simulates — does appear accurate: DISC-NG's comparisons are
against a blended-overlay DHT baseline, DHTTicket, and DISCv5, not against a hypothetical
single-service-only overlay. A synthesis citing `LI-EPRINT-25`'s characterization of DISC-NG should
drop the "no security analysis" half of the claim and keep only the dedicated-overlay-comparison half,
which is the half `KROL-EUROSP-24`'s own text actually supports the absence of.

## Notes

No internal abstract-versus-conclusion inconsistency was found in any entry opened for this family.
`LI-INFOCOM-05`'s own evidence entry separately flags and self-corrects an unrelated error in the
registry's own retrieval metadata (a `why_needed` note wrongly attributing Accordion's self-tuning
routing-table design to this paper); that is a registry-metadata error already caught by the
extracting agent, not a disagreement between two retrieved papers, so it is not carried forward here
as a finding.

The eclipse-attack literature in this family spans three structurally different targets — Bitcoin's
unstructured connection table (`HEILMAN-USENIXSEC-15`), Ethereum's Kademlia-derived discovery table
(`MARCUS-EPRINT-18`, `SHI-WWW-26`, `LI-EPRINT-25`, `KROL-EUROSP-24`), and a generic structured-overlay
routing table (`CASTRO-OSDI-02`, `SINGH-INFOCOM-06`) — and none of these three groups reports a
directly comparable eclipse-success figure under matching conditions against another group; the
differences in reported percentages (for example Heilman's 85%–100% against Singh's 70%–90% malicious
routing-table-entry fractions) reflect different protocols and different measured quantities, not a
disagreement, and are not reported as findings above.
