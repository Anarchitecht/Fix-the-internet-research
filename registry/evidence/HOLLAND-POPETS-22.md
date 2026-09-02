## [HOLLAND-POPETS-22] RegulaTor: A Straightforward Website Fingerprinting Defense
**Citation:** James K. Holland, Nicholas Hopper. "RegulaTor: A Straightforward Website Fingerprinting Defense." Proceedings on Privacy Enhancing Technologies (PoPETs), 2022(2):344-362. DOI: 10.2478/popets-2022-0049.
**Retrieved:** full text via https://petsymposium.org/popets/2022/popets-2022-0049.pdf
**Source URL:** https://petsymposium.org/popets/2022/popets-2022-0049.pdf
**Domain:** G

### What it does
RegulaTor defends a Tor circuit against website fingerprinting (WF), a traffic-analysis attack in which a passive local eavesdropper between the client and the Tor entry node observes the sequence of packet sizes and timings and classifies which page the client is loading. RegulaTor exploits an observed common pattern in web-page loads: a large initial burst ("surge") of download data followed by decay, driven by the browser first requesting a base page and then requesting many embedded objects whose responses arrive in a decaying rate over time. It reshapes both download and upload traffic to always follow this generic decaying-surge shape, so page-specific volume and timing information is masked, without a machine-learned model and without per-page tuning.

The download-side mechanism: RegulaTor first sends the initial 10 real download packets at a constant, unmodified rate, so the TLS handshake and circuit build finish normally and no artificial surge starts before real data exists. It then begins a decaying surge at rate R packets/second, where the instantaneous target sending rate at time t seconds after the surge began is R * D^t (D is a decay constant, D < 1, so the rate decays exponentially). Real packets in the send queue are sent at the target rate; when the queue is empty a dummy packet is sent instead, up to a total padding budget of N dummy packets drawn uniformly at random from (0, N) at the start of each page load (once the N-packet budget is used, no more dummy packets are sent, though real packets may still be delayed to match the target rate). If the queue of waiting real packets exceeds a threshold T times the current target rate, a new surge is triggered (the surge-time counter resets) to avoid excess queuing delay when the real page data genuinely needs high bandwidth. If a real packet has been delayed more than a cap of C seconds, it is sent immediately regardless of the schedule.

The upload-side mechanism: RegulaTor pads upload traffic at a constant rate until the initial download surge begins to arrive (covering the client's initial page request), then schedules upload packets at rate (download rate) / U, where U is a fixed ratio; because upload sequences are typically small in volume, sending upload dummy packets at this pace costs little bandwidth while removing upload-side timing information. Any upload packet delayed more than C seconds is sent immediately.

Two operating points are tuned by the authors using the Tree-Structured Parzen Estimator (TPE) hyperparameter-search technique (via the Python `hyperopt` library), optimizing a weighted combination of latency overhead, bandwidth overhead, and the Tik-Tok attack's accuracy against the resulting defended traces: RegulaTor-Light (favoring lower overhead) and RegulaTor-Heavy (favoring stronger defense).

### Measured results

| Result | Figures | Conditions |
|---|---|---|
| Closed-world accuracy, undefended | Tik-Tok 97.0%, Deep Fingerprinting (DF) 98.4%, CUMUL 97.2% | Table 3; DF-CW dataset: 95 sites, 1,000 instances each, collected by Sirinam et al. in 2016 via tor-browser-crawler on ten low-end machines visiting Alexa Top 100 homepages 1,250 times each, batched 25-per-site per round to control long/short-term variance, corrupted traces discarded |
| Closed-world accuracy, WTF-PAD | Tik-Tok 94.2%, DF 92.4%, CUMUL 59.4% | Table 3, same dataset, default WTF-PAD (`normal_rcv`) parameters, authors' original code |
| Closed-world accuracy, FRONT-1700 | Tik-Tok 78.2%, DF 77.5%, CUMUL 31.6% | Table 3; Ns=Nc=1700, Wmin=1, Wmax=14 |
| Closed-world accuracy, FRONT-2500 | Tik-Tok 66.0%, DF 69.8%, CUMUL 17.1% | Table 3; Ns=Nc=2500, Wmin=1, Wmax=14 |
| Closed-world accuracy, RegulaTor-Light | Tik-Tok 34.8%, DF 23.3%, CUMUL 20.8% | Table 3; R=260, D=0.860, T=3.75, N=2080, U=4.02, C=2.08 |
| Closed-world accuracy, RegulaTor-Heavy | Tik-Tok 25.4%, DF 19.6%, CUMUL 16.3% | Table 3; R=277, D=0.940, T=3.55, N=3550, U=3.95, C=1.77 |
| Closed-world accuracy, Tamaraw | Tik-Tok 10.1%, DF 9.9%, CUMUL 17.0% | Table 3; rho_out=0.04, rho_in=0.012, L=100; Tao Wang's implementation; included as an example of a high-theoretical-strength but high-overhead defense |
| Closed-world defense overhead on DF-CW | Tamaraw: 36.9% latency / 196% bandwidth; WTF-PAD: 0% / 54.0%; FRONT-1700: 0% / 81.0%; FRONT-2500: 0% / 119.0%; RegulaTor-Light: 8.9% / 48.3%; RegulaTor-Heavy: 6.6% / 79.7% | Table 4; latency overhead = additional time to send the last real packet of the defended trace versus the undefended trace, divided by undefended sending time; bandwidth overhead = dummy packets sent divided by real packets in the undefended trace |
| Open-world precision-tuned Tik-Tok F1-score | WTF-PAD 0.870, FRONT-2500 0.625, RegulaTor-Heavy 0.135 (lower is more effective defense) | open-world dataset DF-OW: 40,716 traces from Alexa Top 50,000 (excluding the top 100 used in DF-CW), collected via tor-browser-crawler on ten low-end machines, one visit per site; open-world test set composition favored the attacker, with 9,500 of 29,500 test traces from the monitored class |
| Generalization to KNN dataset (RegulaTor-Heavy parameters tuned on DF-CW, reused unmodified) | Tik-Tok accuracy 17.8%, 5.1% latency overhead, 77.3% bandwidth overhead; FRONT-2500 comparison: Tik-Tok accuracy 44.9%, 98.3% bandwidth overhead | KNN dataset: Wang et al., 2020, 50 websites x 10 pages x 20 samples = 10,000 total samples; only closed-world traces used |
| Generalization to GE dataset, unadjusted RegulaTor-Heavy | Tik-Tok accuracy 11.3%, 15.1% latency overhead, 39.6% bandwidth overhead | GE (Goodenough) dataset, Pulls, 2014, 100 websites x 90 instances, average 5,663.9 packets per trace versus 2,100.9 for DF-CW and 1,807.6 for KNN |
| Generalization to GE dataset, volume-adjusted RegulaTor-Heavy | Tik-Tok accuracy 5.2%, latency overhead 2.9%, bandwidth overhead 82.9% | initial surge rate R scaled by 2.431x (relative traffic-volume increase) to R=673, padding budget N scaled to 8,030; comparison FRONT tuned to match FRONT-2500 bandwidth (padding budget 2,830 both directions) achieved Tik-Tok accuracy 43.4% at 45.8% bandwidth overhead |
| Real-world pluggable-transport deployment | Tik-Tok accuracy 11.6%, latency overhead 13.9%, bandwidth overhead 78.2% | PT dataset: 100 Alexa Top 100 websites x 100 samples, collected over one month (August 2021), via a Tor bridge running WFPadTools (Obfsproxy-based) as the pluggable transport, compared against a "dummy" pluggable transport baseline; initial surge rate raised to 356 and padding budget to 4,564 based on 10-sample-per-site average trace length of 2,697.2, other RegulaTor-Heavy parameters left unchanged |

### Parameters
Six tunable parameters (Table 1): R (initial surge rate, packets/second), D (packet-sending decay rate per second, D < 1), T (surge threshold ratio, triggers a new surge when the waiting-packet queue exceeds T times the current target rate), N (padding budget in packets, the maximum dummy packets sent per page load, with the actual count drawn uniformly at random from (0, N) each load), U (download-to-upload packet-rate ratio, upload packets sent at rate = download rate / U), C (delay cap in seconds, a delayed packet beyond this cap is sent immediately).

Values used: RegulaTor-Light: R=260, D=0.860, T=3.75, N=2080, U=4.02, C=2.08. RegulaTor-Heavy: R=277, D=0.940, T=3.55, N=3550, U=3.95, C=1.77. Both sets were found via Tree-Structured Parzen Estimator hyperparameter search, minimizing a weighted loss combining latency overhead, bandwidth overhead, and Tik-Tok attack accuracy on the RegulaTor-defended DF-CW dataset; the search space's exact bounds are stated to be detailed in an appendix not reached in this extraction pass.

Cross-dataset parameter transfer: R and N were rescaled proportionally to the ratio of the target dataset's average trace length to DF-CW's average trace length (2.431x for the GE dataset); D, T, U, C were left unchanged and reported to generalize regardless of traffic volume.

### Stated limitations
The paper states it did not test RegulaTor against an attacker who links a defended packet sequence to a web site using information from a series of page loads on that site, rather than a single page load in isolation, and states this "task may be easier for an attacker able to use information about multiple web pages on the same website"; this is left explicitly for future work.

The paper states RegulaTor's choice of surge parameters depends on the traffic volume of the undefended sequence: if the surge size is too small relative to real traffic volume, latency increases unnecessarily as data waits behind an undersized surge budget; the paper's own generalization test (GE dataset) shows unadjusted parameters raise latency overhead from roughly 6.6-8.9% to 15.1% when applied to a dataset with roughly 2.7x the packet volume of the tuning dataset, and states that some occasional data collection is needed to re-estimate relative traffic volume when moving RegulaTor to a new site population.

The paper notes RegulaTor's parameters were tuned specifically against the Tik-Tok attack, while WTF-PAD and FRONT in the same comparison used only their original authors' default parameters (not re-tuned against Tik-Tok), and states this may give RegulaTor "a slight advantage against Tik-Tok" in the closed-world comparison — a caveat on the paper's own headline comparison, not an external critique.

The paper reports that CUMUL's accuracy against RegulaTor-Light (20.8%) was not necessarily lower than CUMUL's accuracy against FRONT (compared figures not fully separated in this extraction), and attributes this to CUMUL deriving most of its features from a cumulative-sum trace representation that FRONT's early-burst obfuscation disturbs more than RegulaTor's shape-preserving approach does — stated as a case where RegulaTor's advantage over FRONT does not hold uniformly across attacks.

### Requirements it places on the rest of the system
Both the client and the entry-side proxy (in the paper's implementation, a Tor bridge running a pluggable transport) must run the RegulaTor scheduler in lockstep: the upload-side schedule is derived from the observed download-side sending rate (rate = download rate / U), so the proxy's download pacing must be visible to, or coordinated with, the client's upload pacing logic.

The defense pads traffic only between the client and the first relay in the circuit (the entry node or bridge); the paper states this keeps the real-world bandwidth cost of padding low because Tor's overall capacity is limited chiefly by exit-node availability, not entry-node link capacity — a system reusing this design should not extend padding further into the circuit expecting the same bandwidth-cost argument to hold, since that argument depends specifically on entry-side padding.

The threat model assumes a passive local eavesdropper who observes packet sizes and timing but does not decrypt or tamper with traffic; results are reported for both a closed-world attacker (limited to a fixed monitored-site set) and an open-world attacker, and the paper states the open-world test set favored the attacker by using an unrealistically high monitored-to-unmonitored ratio (9,500 of 29,500 traces monitored) relative to real-world browsing.

Deploying RegulaTor against a new site population requires estimating that population's typical page traffic volume in advance (via a small sample collection) so R and N can be rescaled; the paper's real-world pluggable-transport deployment collected only 10 samples per site to perform this rescaling, which it states was sufficient.

### Contradicts
None found.

### References worth retrieving
- **Competing:** J. Gong, T. Wang, "Zero-delay lightweight defenses against website fingerprinting" (FRONT), USENIX Security 2020 — the primary comparison target throughout, described in this paper as "the best published deployable defense" prior to RegulaTor; holds FRONT's own reported overhead and accuracy figures.
- **Competing:** X. Cai, R. Nithyanand, T. Wang, R. Johnson, I. Goldberg, "A systematic approach to developing and evaluating website fingerprinting defenses" (Tamaraw), ACM CCS 2014 — the strong-but-impractical-overhead baseline.
- **Competing:** K. P. Dyer, S. E. Coull, T. Ristenpart, T. Shrimpton, "Peek-a-boo, I still see you: Why efficient traffic analysis countermeasures fail," IEEE S&P 2012 — WTF-PAD's predecessor line, the other lightweight-defense comparison baseline.
- **Competing:** W. De la Cadena et al., "TrafficSliver: Fighting website fingerprinting attacks with traffic splitting," ACM CCS 2020 — a traffic-splitting defense discussed as protecting against a different (guard-node-only) attacker, explicitly not defending against the local eavesdropper this paper's threat model uses.
- **Competing:** S. Henri, G. Garcia-Aviles, P. Serrano, A. Banchs, P. Thiran, "Protecting against website fingerprinting with multihoming," PoPETs 2020 — a second traffic-splitting defense discussed as not protecting against local attackers who see outgoing traffic.
- **Attack:** M. S. Rahman, P. Sirinam, N. Mathews, K. G. Gangadhara, M. Wright, "Tik-Tok" — the primary attack this defense is tuned against (cited as reference [38] in this paper's own numbering; full citation not reached in this extraction pass but referenced throughout as the strongest attack).
- **Attack:** J. Hayes, G. Danezis, "k-fingerprinting: A robust scalable website fingerprinting technique," USENIX Security 2016 — kFP, cited for the KNN dataset origin.
- **Foundational:** J. Bergstra, R. Bardenet, Y. Bengio, B. Kegl, "Algorithms for hyper-parameter optimization," NeurIPS 2011 — the Tree-Structured Parzen Estimator technique this paper uses for RegulaTor parameter tuning.
- **Attack/critique:** X. Cai, X. Zhang, B. Joshi, R. Johnson, "Touching from a distance: Website fingerprinting attacks and defenses," ACM CCS 2012 — cited as the paper that defeated earlier application-level object-reordering defenses.

### Verbatim extracts
- "RegulaTor reduces the accuracy of the state-of-the-art attack, Tik-Tok, against comparable defenses from 66% to 25.4%" (Abstract).
- "it requires 6.6% latency overhead and a bandwidth overhead 39.3% less than the leading moderate-overhead defense" (Abstract).
- "RegulaTor limits a precision-tuned Tik-Tok attack to an F1-score of .135, compared to .625 for the best comparable defense" (Abstract).
- "the sending rate is reduced according to the decay constant, D, such that the sending rate is RD^t" (Section 3.2, mechanism description).
- "we did not test it in terms of preventing an attack from identifying a web site based on a series of page loads" (Section 6, Conclusion and Future Work).
- "the open-world setup used in this paper favored the attacker by using a test set where 9500 of the 29,500 traces were from the monitored class" (Section 4.2.2).
