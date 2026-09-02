## [GONG-SP-22] Surakav: Generating Realistic Traces for a Strong Website Fingerprinting Defense
**Citation:** Jiajun Gong, Wuqi Zhang, Charles Zhang, Tao Wang. "Surakav: Generating Realistic Traces for a Strong Website Fingerprinting Defense." IEEE Symposium on Security and Privacy, 2022. Pages 1558-1573. DOI: 10.1109/SP46214.2022.9833722.
**Retrieved:** full text via https://www.computer.org/csdl/proceedings-article/sp/2022/131600b035/1B68w6QujMg
**Source URL:** https://www.computer.org/csdl/proceedings-article/sp/2022/131600b035/1B68w6QujMg
**Domain:** G

### What it does
Surakav defends a Tor circuit against website fingerprinting (WF): a traffic-analysis attack in which a local eavesdropper between the client and the entry node observes only encrypted packet sizes and timings and trains a classifier to guess which page the client is loading. Surakav hides the size and timing pattern of a page load by regulating both the client's and the entry-node proxy's packet sending according to a synthetic "reference trace" sampled from a trained generative model, so a real page load's traffic pattern is pulled toward a generated pattern the attacker cannot correlate with any specific page.

The mechanism has two phases. In the training phase, a Generative Adversarial Network (GAN) with three components — a generator (a multilayer perceptron taking a class label and a noise vector and outputting a burst-size sequence and trace length), a discriminator (a multilayer perceptron scoring real versus generated traces), and an added "observer" (a pretrained Deep Fingerprinting classifier that scores whether a generated trace, once it fools the discriminator, is still classifiable as its intended webpage class) — is trained on a labeled dataset of real page-load traces until the generator produces burst-size sequences realistic enough to fool the discriminator while remaining distinguishable by class to the observer.

In the deployment phase, a regulator component R runs on both the client and the entry-node proxy. On each round, R samples a time gap from a Kernel Density Estimation (KDE) model of real inter-burst gaps, sleeps for the minimum of that gap and a ceiling parameter rho, then sends an outgoing burst. The burst size is snapped toward a reference burst size drawn from a freshly sampled generator trace, using a tolerance parameter delta: if the real buffered data's size already falls within (1-delta) to (1+delta) of the reference burst size, it is sent unmodified; otherwise dummy packets are added or real data is held back to move the sent burst to the nearest boundary of that range. A second mechanism, Random Response, lets the proxy skip sending a burst entirely with probability q (resampled per page load from a uniform distribution) whenever there is no real data queued, which lowers data overhead without delaying any real packet.

### Measured results

| Result | Figures | Conditions |
|---|---|---|
| Headline comparison (Abstract) | Surakav reduces attacker true positive rate (TPR) by 57%, at 55% data overhead and 16% time overhead; saves 42% data overhead versus FRONT for a comparable TPR reduction; in the heavyweight setting, requires 50% less overhead (data and time combined) than Tamaraw to reduce attacker TPR to 8% | live Tor network, open-world scenario, four state-of-the-art WF attacks (kFP, CUMUL, Deep Fingerprinting/DF, Tik-Tok) |
| Open-world attack results, no defense | kFP TPR 73.62% / FPR 0.18%; CUMUL TPR 74.23% / FPR 3.50%; DF TPR 96.24% / FPR 0.54%; Tik-Tok TPR 96.68% / FPR 0.70% | Table III; open-world dataset of 100 monitored sites x 100 loads + 60,000 non-monitored sites x 1 load, collected on the live Tor network from the Tranco top-1-million list (list dated 21 Jan 2021); 10-fold cross validation |
| Open-world attack results, FRONT defense | 97% data overhead, 0% time overhead; kFP TPR 0.92% / FPR 0.01%; CUMUL TPR 3.78% / FPR 9.55%; DF TPR 43.00% / FPR 4.66%; Tik-Tok TPR 42.63% / FPR 3.02% | Table III, same setup; FRONT configured with Nc=Ns=6000, Wmin=1s, Wmax=14s |
| Open-world attack results, Tamaraw defense | 121% data overhead, 26% time overhead; kFP TPR 0.36% / FPR 0.03%; CUMUL TPR 1.91% / FPR 8.99%; DF TPR 15.21% / FPR 1.17%; Tik-Tok TPR 12.99% / FPR 0.53% | Table III, same setup; Tamaraw configured with rho_c=14ms, rho_s=4ms, L=100 (payload size 514 bytes, a Tor cell), adjusted from the original paper's 750-byte payload |
| Open-world attack results, Surakav-light (delta=0.6) | 55% data overhead, 16% time overhead; kFP TPR 0.85% / FPR 0.02%; CUMUL TPR 11.24% / FPR 8.79%; DF TPR 39.40% / FPR 5.81%; Tik-Tok TPR 39.68% / FPR 4.41% | Table III, same setup |
| Open-world attack results, Surakav-heavy (delta=0.4) | 81% data overhead, 17% time overhead; kFP TPR 0.01% / FPR 0%; CUMUL TPR 2.74% / FPR 7.63%; DF TPR 8.14% / FPR 2.70%; Tik-Tok TPR 6.28% / FPR 1.04% | Table III, same setup |
| One-page setting, kFP attack (Table IV, harder scenario) | No defense: TPR 98.29+/-1.91%, FPR 1.48+/-1.63%; FRONT (97/0 overhead): TPR 85.20+/-6.83%, FPR 14.41+/-7.07%; Tamaraw (121/26): TPR 87.07+/-5.12%, FPR 13.24+/-5.05%; Surakav-light (55/16): TPR 86.11+/-7.27%, FPR 12.88+/-5.90%; Surakav-heavy (81/17): TPR 82.77+/-7.27%, FPR 19.43+/-7.35% | one-page setting proposed by Wang (a harder evaluation regime; exact difference from the multi-page setting not extracted here); values are mean +/- standard deviation across the same closed-world/open-world collection methodology |
| Information leakage (mutual information, top 100 non-redundant of 3,043 total features) | Undefended: most informative single feature leaks 2.85 bits; Tamaraw leaks at most 1.78 bits (median 1.41 bits); FRONT leaks at most 1.83 bits (median 1.22 bits); Surakav-light leaks at most 1.65 bits (median 1.22 bits); Surakav-heavy leaks at most 1.59 bits (median 1.09 bits) | WeFDE framework, same open-world dataset collection |
| GAN-fidelity check: generated traces classified under their intended label by a real-trace-trained DF classifier | 90% accuracy with the observer component included in training; 13% accuracy without the observer | preliminary experiment, DSgan training set (see Parameters) |
| Adversarial-perturbation defense (Nasr et al.) tested for applicability to this threat model | Reduced attacker TPR by over 94% when the attack classifier was trained only on undefended traces; reduced attacker TPR by only 4% when the attack classifier was trained on defended traces | brief simulation experiment, open-world scenario, same methodology as the paper's other experiments; cited as evidence that this defense category does not fit a threat model where the attacker can train on defended traces |
| Deployment hardware | Bridge (entry node): 1 CPU core at 2.3 GHz, 2 GB memory, Tor 0.4.4.5 on Debian 9.11. Clients: 4 CPU cores at 2.3 GHz, 16 GB memory, Ubuntu 18.04.4 LTS, customized Tor Browser 10.0.15, 10 parallel Docker-container clients across two Azure servers, each client bandwidth-limited to 120 Mbit/s (July 2021 global average per Speedtest) | Three Microsoft Azure servers; each page-load session capped at 80 s plus 5 s post-load wait; data collection ran over two months, producing 15 closed-world datasets (10,000 monitored instances each) and 5 open-world datasets (70,000 instances each: 100 monitored sites x 100 loads + 60,000 non-monitored sites x 1 load) |

### Parameters

| Parameter | Meaning | Value(s) used | Range searched |
|---|---|---|---|
| rho | maximum time gap allowed between two outgoing bursts | 100 ms (fixed default) | not stated as swept in the main results; Table I lists it as a regulator configuration parameter |
| delta | tolerance for burst-size adjustment, sets how far a real burst may deviate from the sampled reference burst before dummy packets or delay are applied | 0.6 (Surakav-light), 0.4 (Surakav-heavy) | not given as a numeric search range in the extracted text; light/heavy are the two settings reported |
| q | probability the proxy skips sending a burst when its buffer holds no real data | resampled per page load from Uniform(0,1) | Uniform(0,1), not a fixed constant |
| GAN training epochs | training iterations for generator/discriminator | 600 | [20, 1000] |
| Trace length | fixed-length output vector before truncation to the learned per-class length | 1400 | [500, 10000] |
| Optimizer | GAN optimizer | RMSProp | {Adam, Adamax, RMSProp} |
| Learning rate | GAN training learning rate | 0.0002 | [0.0001, 0.001] |
| Batch size | GAN training batch size | 64 | [16, 256] |
| z dim | noise vector dimensionality fed to the generator | 500 | [50, 1000] |
| Generator layer count | 4 | [3, 5] |
| Discriminator layer count | 4 | [3, 5] |
| Dropout | 0.2 | [0.2, 0.9] |
| Activation function | LeakyReLU | {ReLU, LeakyReLU, ELU} |
| alpha | weight balancing the Wasserstein loss term against the observer's cross-entropy loss in the generator's combined loss | 0.02 | [0.01, 1.0] |
| n_critic | number of discriminator training iterations per one generator training iteration | 3 | [1, 10] |
| GAN training dataset (hyperparameter search) | DSgan, drawn from Rimmer's dataset (900 classes x 2,500 instances, collected 2018), 100 randomly chosen classes used, 1,000 instances per class in the search runs | — | — |
| GAN generalization check dataset | DS95, from Sirinam et al., 95 classes, same hyperparameters from Table II reused without retuning | — | — |

### Stated limitations
The implementation deploys all compared defenses (including Surakav) on the Tor entry node rather than the middle node, because delaying real packets on a live Tor relay risks out-of-memory errors and Tor's own source code and protocols would need modification to move the defense to the middle node; the paper excludes the entry node itself as a potential attacker as a consequence, and states this exclusion as a limitation to be addressed in future work, not as a proven-safe assumption.

The reported overhead figures come from a fixed 10-parallel-client experimental setup and the paper states they should be treated as representative of a low-congestion deployment; a real Tor relay's variable client congestion would change packet scheduling and the resulting overhead, and the paper states further work is needed to measure other congestion regimes.

Surakav generates a reference trace for a randomly selected webpage regardless of which page the client is actually visiting; the paper states overhead could be further reduced by giving the generator prior knowledge of the page being visited to choose a more correlated decoy, but states this is left as future work because the correlation between the real and decoy page would need to be kept weak by design.

The paper's own simulation shows a competing defense category (Nasr et al.'s adversarial-perturbation defense) is ineffective under a threat model in which the attacker trains its classifier on defended traces (TPR reduced by only 4%, versus 94% when the attacker trains only on undefended traces); Surakav's authors state their own defense does not fall into this adversarial-perturbation category and does not depend on fooling a fixed trained classifier.

### Requirements it places on the rest of the system
Both the client and the entry-node proxy must run the regulator R and hold the same trained generator model; the regulator's Burst Adjustment and Random Response mechanisms require the proxy to receive a signal from the client (a message packet attached to each burst instructing how much data to respond with) so the two sides' bursts stay synchronized to the same reference trace.

The threat model assumes a passive local eavesdropper who does not compromise Tor's encryption and does not modify packets, and assumes the client loads one page at a time so the attacker can identify each page load's start and end; the paper states that a multi-tab browsing scenario is harder to attack and is not the scenario evaluated.

Deploying the defense requires distributing the trained generator's weights (stated as several megabytes) to every client in advance of use; the generator must have been trained on a labeled dataset of real page-load traces representative of the pages the defense is meant to protect, since the observer component's feedback during training depends on a Deep-Fingerprinting-style classifier's ability to recognize per-class structure in the generated traces.

Tamaraw's payload-size-dependent parameters (rho_c, rho_s) had to be recalculated for this deployment because Tor's actual cell size (514 bytes) differs from the 750-byte payload assumed in Tamaraw's original paper; any system reusing Tamaraw's published parameters directly, without adjusting for the transport's actual frame size, will not reproduce Tamaraw's reported overhead or security level.

### Contradicts
None found.

### References worth retrieving
- **Competing:** J. Gong, T. Wang, "Zero-delay lightweight defenses against website fingerprinting" (FRONT), USENIX Security 2020 — the lightweight defense directly compared against Surakav throughout; holds FRONT's own overhead/TPR figures.
- **Competing:** X. Cai, R. Nithyanand, T. Wang, R. Johnson, I. Goldberg, "A systematic approach to developing and evaluating website fingerprinting defenses" (Tamaraw), ACM CCS 2014 — the strong-defense baseline compared against Surakav; original payload-size and rho parameters this paper adjusts.
- **Competing:** T. Wang, I. Goldberg, "Walkie-Talkie: An efficient defense against passive website fingerprinting attacks," USENIX Security 2017 — assumes known burst patterns in advance; a "fortified" variant (Random-WT) is used as a comparison baseline in this paper.
- **Competing:** W. de la Cadena et al., "TrafficSliver: Fighting website fingerprinting attacks with traffic splitting," ACM CCS 2020 — defends a different threat model (malicious entry node); this paper shows it is weak against the local-eavesdropper threat model and augments it with the GAN trace generator.
- **Attack:** P. Sirinam, M. Imani, M. Juarez, M. Wright, "Deep Fingerprinting: Undermining website fingerprinting defenses with deep learning," ACM CCS 2018 — the DF attack used as the primary benchmark and as the observer's architecture.
- **Attack:** M. S. Rahman, P. Sirinam, N. Mathews, K. G. Gangadhara, M. Wright, "Tik-Tok: The utility of packet timing in website fingerprinting attacks," PoPETs 2020 — the strongest attack benchmarked, incorporating timing information DF omits.
- **Attack:** J. Hayes, G. Danezis, "k-fingerprinting: A robust scalable website fingerprinting technique," USENIX Security 2016 — kFP attack, one of the four benchmarks.
- **Attack:** A. Panchenko et al., "Website fingerprinting at internet scale" (CUMUL), NDSS 2016 — CUMUL attack, one of the four benchmarks.
- **Foundational:** M. Juarez, M. Imani, M. Perry, C. Diaz, M. Wright, "Toward an efficient website fingerprinting defense" (WTF-PAD), ESORICS 2016 — earlier lightweight defense broken by DF before Tor deployment; motivates this paper's design.
- **Attack/critique:** R. Nithyanand, X. Cai, R. Johnson, "Glove: A bespoke website fingerprinting defense," WPES 2014 — requires prior page-list knowledge, cited as too expensive to use.
- **Superseded-by relationship (self-noted):** the paper states WTF-PAD "was broken by DF before it was ready to be deployed on Tor," documenting an attack superseding a defense within this same bibliography.

### Verbatim extracts
- "reduce the attacker's true positive rate by 57% with 55% data overhead and 16% time overhead" (Abstract).
- "requiring 50% less overhead in data and time to lower the attacker's true positive rate to only 8%" (Abstract).
- "we assume the attacker does not try to compromise the encryption of Tor or modify any packets" (Section on Threat Model).
- "we have to modify Tor's source code and change its protocols to do so" (Section VII, on why the middle node was not used).
- "Surakav chooses to generate a trace of a randomly selected webpage, no matter which webpage the client is visiting" (Section VII).
- "This led to a 90% accuracy on DF, compared to 13% without an observer" (Section IV-C1, on the observer component).
