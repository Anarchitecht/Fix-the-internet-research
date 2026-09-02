## [SHEN-SP-24] Real-Time Website Fingerprinting Defense via Traffic Cluster Anonymization

**Citation:** Meng Shen, Kexin Ji, Jinhe Wu, Qi Li, Xiangdong Kong, Ke Xu, Liehuang Zhu. "Real-Time Website Fingerprinting Defense via Traffic Cluster Anonymization." IEEE Symposium on Security and Privacy, 2024. Pages 3243-3261 (page range per IEEE Xplore pagination visible in text: 3243-3261, exact start/end not independently confirmed). DOI: 10.1109/SP54263.2024.00247.
**Retrieved:** full text via https://doi.org/10.1109/SP54263.2024.00247
**Source URL:** https://doi.org/10.1109/SP54263.2024.00247
**Domain:** G

### What it does
Palette defends a Tor client's traffic pattern against website fingerprinting (WF) attacks — machine-learning classifiers that identify which website a client is visiting from the size and timing of encrypted packets observed on the path between the client and the Tor guard node. Palette makes many distinct websites produce traffic that is statistically indistinguishable from each other, rather than trying to make one website's traffic look like unstructured noise.

Mechanism, in three stages. First, offline clustering groups a set of monitored websites into anonymity sets of size k based on similarity of their traffic patterns, represented as a Traffic Aggregation Matrix (TAM) that counts incoming and outgoing packets per small time slot; for each anonymity set the system builds one shared "super-matrix" summarizing the traffic shape all websites in that set will be regulated to match. Second, the super-matrix is refined using historical traces from the set's member websites to reduce the bandwidth and time overhead needed to force every member's traffic to match it. Third, at real-time packet-sending time, the client (via a Tor Pluggable Transport, a mechanism that transforms Tor traffic to disguise it from network observers) regulates the live trace against the anonymity set's super-matrix by injecting dummy packets or delaying real ones — "trace regularization." Two techniques reduce the overhead of this regularization: early sending, which forwards buffered real packets ahead of the super-matrix schedule once a buffer-occupancy threshold sampled uniformly from [0, U) is exceeded, avoiding buffer congestion and its time-overhead cost; and tail padding, which checks every B-th time slot whether the sending buffer is empty to infer the page has finished loading and stop dummy-packet padding, without needing to know the true page-load-completion time the way the competing Tamaraw defense does.

### Measured results
Dataset: a public real-world dataset (cited as reference [6] in the paper, also used by other WF attack/defense papers) with a closed-world set of 1,000 traces across 95 websites and an open-world set of 40,716 websites at one trace each. Attacks compared: six published WF classifiers — CUMUL, k-FP, DF (a CNN using packet direction), Tik-Tok (DF's CNN structure on direction-times-time), Var-CNN (ResNet-based, uses direction, inter-packet time, and metadata), and RF (uses the TAM representation with a CNN) — all retrained by the authors with adversarial training on each defense's defended traffic, trained and tested on one server (Intel Core i7 3.4 GHz, 32 GB RAM, 10 GB GPU memory).

| Defense | Bandwidth overhead | Time overhead | Notes |
|---|---|---|---|
| Undefended | -- | -- | Baseline classifier accuracy 94.5-98.8% across all six attacks |
| Supersequence | 88% | 91% | Reduces all six attacks to below 30% accuracy |
| Tamaraw | 121% | 43% | Reduces all six attacks to below 30% accuracy |
| WTF-PAD | 61% | 0% | Defeated by four deep-learning attacks at over 90% accuracy |
| FRONT | 80% | 0% | RF attack still achieves over 90% accuracy against it |
| Surakav | 80% | 6% | Reduces DF/Tik-Tok/Var-CNN accuracy to 64.00%/67.63%/54.56%; ineffective against RF |
| RegulaTor | 80% | 5% | Reduces all six attacks to at least 53.11% accuracy |
| Palette | 84% | 9% | Reduces RF accuracy to 36.43%, a 16.68-percentage-point reduction versus RegulaTor's 53.11%; reduces the other five attacks to between 9.78% (CUMUL) and 24.73% (Var-CNN) |

Conditions for the above table: closed-world scenario, 95 monitored websites, 8:1:1 train/validation/test split, with adversarial training applied per attack per defense.

Open-world scenario: 95 monitored websites (900 training traces each) and 20,000 unmonitored-website training traces at an 8:1 split; testing used 95×100 monitored traces and 20,000 unmonitored traces. Without defense, DF, Tik-Tok, Var-CNN, and RF achieve high precision and recall. Palette reduces recall of all four deep-learning attacks below 0.1 at high precision, outperforming Surakav (effective only against DF and Tik-Tok) and RegulaTor (ineffective specifically against RF). As the unmonitored-website pool scaled from 10,000 to 40,000, Palette's bandwidth overhead grew from 79.63% to 81.81% and time overhead stayed roughly constant (8.89% to 8.86%).

One-page setting (single monitored website, k-FP attack, 900 positive / 102,600 negative training traces, 100 positive / 29,400 negative testing traces): Supersequence and Tamaraw outperform Palette on the ROC curve in this harder setting, but at 82% and 34% higher time overhead than Palette respectively.

Real-world deployment on the live Tor network: Palette implemented as a Pluggable Transport via the WFDefProxy framework, tested with two cloud servers (one Tor private bridge with 2 CPU cores/4 GB RAM, one client host with 8 CPU cores/16 GB RAM running eight Docker container clients in parallel over a 120 Mbps connection, Tor Browser 10.5.10, first 100 accessible sites from the February 2023 Tranco list). Under this deployment, Tamaraw incurred 135% bandwidth and 78% time overhead; RegulaTor's real-world time overhead rose to 112% (versus 5% in simulation) with attack accuracy on DF/Tik-Tok/RF improving by more than 10 percentage points relative to simulation; Palette reduced DF, Tik-Tok, and Var-CNN accuracy to under 15% and RF accuracy to 53.28%.

Varying network conditions (super-matrix and parameters fixed at 120 Mbps / Tor Browser, then applied under other conditions): at 80/120/160 Mbps bandwidth constraints on Tor Browser, Palette's bandwidth overhead was 76%/73%/77% and time overhead 28%/30%/34%, with RF accuracy 47.74%/50.87%/47.76%. Switching from Tor Browser to Chrome at the same 120 Mbps reduced bandwidth overhead by 54 percentage points and increased time overhead by 20 percentage points, attributed to Chrome's larger baseline traffic volume (Tor Browser strips SPDY/HTTP-2 features that inflate traffic).

Stability over time: traces recollected 5 days after initial collection (120 Mbps, Tor Browser) showed RF accuracy still at 48.98% (versus 50.87% at time 0), bandwidth overhead rising from 73% to 75%, time overhead falling from 30% to 29%.

Update cost: with anonymity-set size k tested at 5, 10, 15, 20, 30, 45, and 95, the super-matrix generation time held roughly constant at approximately 112.6-113.0 seconds regardless of k, while refinement time fell from 148.78s (k=5) to 65.75s (k=20) then rose again for larger k, and storage fell from 228 KB (k=5) to 17 KB (k=95). Communication overhead for distributing updated super-matrices was measured against Tor client-population scale (2.5M, 5M, 7.5M, 10M clients) and update frequency (1-30 days), plotted rather than tabulated in the source text available here.

Adaptive attacks (attacker has full knowledge of Palette's mechanism and first classifies which anonymity set a trace belongs to, then which website within it): highest resulting accuracy across DF, Tik-Tok, Var-CNN, and RF was 36.92% (under RF), only marginally above the non-adaptive adversarially-trained RF result of 36.43%.

Two separate parameter settings are used: for the closed-/open-world simulation experiments (Table 10), Palette used k=30, α=0.16, B=20, U=45; for the real-world Tor deployment (Table 11), Palette used k=30, α=0.25, B=1, U=15.

### Parameters
| Parameter | Description | Value(s) tested |
|---|---|---|
| k | anonymity set size (number of websites clustered together) | 5, 10, 15, 20, 30, 45, 95 tested for update cost and grid search; k=30 used for both the simulation (Table 10) and real-world deployment (Table 11) experiments |
| α | threshold for time-slot sampling in super-matrix construction | 0.16 (simulation, Table 10) / 0.25 (real-world deployment, Table 11) |
| B | multiple for tail padding (checks buffer emptiness every B-th time slot) | 20 (simulation) / 1 (real-world deployment) |
| U | upper bound for the early-sending threshold, sampled uniformly from [0, U) | 45 (simulation) / 15 (real-world deployment) |
| s | TAM time-slot width | 80 ms, with N=1,000 slots, "for a better overhead trade-off" |

### Stated limitations
The threat model assumes a local, passive eavesdropper limited to the connection between client and Tor guard node — an attacker who cannot modify, drop, or decrypt packets; defenses of this kind, including Palette, do not address an attacker capable of observing traffic at multiple points or performing active manipulation. The paper assumes the Tor client already knows the identity of the website being visited (needed to select the correct super-matrix) and assumes the client visits one page at a time, stating that multi-tab browsing is generally considered a harder scenario for attackers and is not evaluated. The website list for evaluation is drawn from the Tranco list, which the authors state "may not reflect the visiting interests of real Tor users"; they identify collecting a more representative list via a Tor exit node as raising ethical concerns about revealing real users' destinations, and leave this unresolved. The paper states, as explicit future work: extending clustering to a larger-scale open-world setting to improve within-set similarity of the small fraction of dissimilar websites; and assigning each website to multiple anonymity sets (rather than one) to defeat the adaptive attacker's anonymity-set-identification stage, since the current single-assignment design lets an adaptive attacker first narrow to the correct anonymity set before attacking individual websites within it. Performance stability was measured only over a 5-day window; the authors state "the performance over a longer period would be interesting future work," meaning no longer-horizon stability claim is supported. Real-world deployment measurements diverge from simulation for every defense tested, most severely for RegulaTor (time overhead more than doubling, from 5% to 112%); the authors attribute Palette's own smaller but present real-world overhead increase to packet dependencies between incoming and outgoing traffic that simulation cannot represent.

### Requirements it places on the rest of the system
- Requires a Tor Pluggable Transport deployment point on both the client and a cooperating Tor middle node (or bridge), since the defense negotiates and applies packet regulation between those two parties; a system without a controllable relay/bridge component in the path cannot deploy this mechanism as specified.
- Requires the client to know the destination website's identity before the connection begins, in order to select the correct super-matrix/anonymity set; a design in which the client's own component cannot observe or decide this in advance (e.g., a fully blinded browsing proxy) cannot supply this precondition.
- Requires an offline corpus of website traffic traces for the monitored set, collected in advance, to build the TAM-based super-matrices per anonymity set; a system targeting arbitrary, unenumerated destinations (the open-world case) falls back to randomly assigning an unmatched website to an existing anonymity set, which the paper shows increases bandwidth overhead as the unmonitored population grows (79.63% to 81.81% from 10,000 to 40,000 unmonitored sites).
- Requires periodic redistribution of updated super-matrices, PMFs, and anonymity-set mappings to every client; the paper measures the resulting communication overhead as a function of Tor's client population scale and the chosen update frequency, meaning a system adopting this mechanism inherits a scaling cost tied to total user population.
- Requires the underlying transport (Tor) to tolerate the added bandwidth (order of 70-90%) and delay (order of 5-35% depending on deployment condition) this defense introduces; a network or client-side agreement with a strict end-to-end latency budget below that added delay cannot adopt this mechanism without the traffic-cluster-anonymization tradeoff.

### Contradicts
None found within this corpus regarding a specific numeric conflict with another entry. The paper's own real-world results contradict its simulation results for other defenses it reproduces (most sharply RegulaTor's time overhead, 5% simulated versus 112% deployed) — this is an intra-paper finding, not a cross-paper contradiction with another corpus entry, and it is recorded here because it bears on the reliability of any other paper's simulation-only overhead figures for these same defenses (Supersequence, Tamaraw, WTF-PAD, FRONT, Surakav, RegulaTor) if those figures are cited from simulation rather than a real-network deployment.

### References worth retrieving
- competing: J. K. Holland, N. Hopper. "RegulaTor: A straightforward website fingerprinting defense." (Best-performing baseline this paper compares directly against; holds the closest comparison numbers.)
- competing: J. Gong, W. Zhang, C. Zhang, T. Wang. "Surakav: generating..." (Second comparison defense.)
- competing: J. Gong, T. Wang. "Zero-delay lightweight defenses against website fingerprinting." (FRONT, a zero-delay defense this paper shows is defeated by the RF attack.)
- competing: M. Juarez, M. Imani, M. Perry, C. Diaz, M. Wright. "Toward..." (WTF-PAD, a zero-delay obfuscation defense this paper shows is defeated by four of six deep-learning attacks.)
- competing: X. Cai, R. Nithyanand, T. Wang, R. Johnson, I. Goldberg. "A systematic approach to developing and evaluating website fingerprinting defenses." (Tamaraw, the strongest-protection but highest-overhead baseline.)
- attack: P. Sirinam, M. Imani, M. Juárez, M. Wright. "Deep fingerprinting: ..." (DF attack, one of the six benchmark WF attacks.)
- attack: M. S. Rahman, P. Sirinam, N. Mathews, K. G. Gangadhara, ... "Tik-Tok: ..." (Tik-Tok attack.)
- attack: S. Bhat, D. Lu, A. Kwon, S. Devadas. "Var-CNN: A data-efficient..." (Var-CNN attack.)
- attack: M. Shen, K. Ji, Z. Gao, Q. Li, L. Zhu, K. Xu. "Subverting website fingerprinting..." (RF attack using the Traffic Aggregation Matrix representation, the strongest attack against most defenses tested here, including a self-citation by overlapping authors of this paper.)
- foundational: R. Dingledine, N. Mathewson, P. F. Syverson. "Tor: The second-generation onion router." (Foundational Tor design this defense operates within.)
- attack: T. Wang. "The one-page setting: A higher standard for evaluating website fingerprinting defenses." (Source of the harder open-world evaluation setting used in Section 6.3.)
- foundational: J. Gong, W. Zhang, C. Zhang, T. Wang. "WFDefProxy: Real world..." (The deployment framework used for the real-Tor-network prototype; also the source of the observation, corroborated here, that RegulaTor's real-world performance differs sharply from simulation.)
- foundational: V. Le Pochat, T. Van Goethem, S. Tajalizadehkhoob, W. Joosen. (Tranco list, source of the website ranking used for real-world data collection.)

### Verbatim extracts
- "attacker is a local and passive eavesdropper"
- "cannot modify, drop, or decrypt packets"
- "assume that the client visits one page at a time"
- "reduce the accuracy of RF to 36.43%, a decrease of 16.68%"
- "the highest accuracy achieved by the adaptive attack is merely 36.92%"
- "the performance over a longer period would be interesting future work"
- "We leave these as the future work."
- "time overhead increases to 112%"
