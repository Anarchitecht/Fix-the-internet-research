## [GONG-USENIXSEC-20] Zero-delay Lightweight Defenses against Website Fingerprinting
**Citation:** Jiajun Gong, Tao Wang. "Zero-delay Lightweight Defenses against Website Fingerprinting." 29th USENIX Security Symposium, 2020.
**Retrieved:** full text via https://www.usenix.org/system/files/sec20-gong.pdf
**Source URL:** https://www.usenix.org/system/files/sec20-gong.pdf
**Domain:** G

### What it does
FRONT and GLUE both hide, from a passive eavesdropper positioned between a Tor client and the Tor network entry node, which webpage a client loaded, by adding dummy packets to the encrypted traffic between the client and a cooperating Tor middle node acting as a defense proxy. Neither defense delays any real packet, so both add zero latency overhead; both add only data overhead (extra dummy packets), which the paper calls "lightweight." FRONT targets the observation that a Website Fingerprinting (WF) classifier extracts most of its useful features from the first few seconds of a page-load trace (the "trace front"). For each trace, the client draws a random count of outgoing dummy packets from a discrete uniform distribution bounded by parameter N_c, and the cooperating proxy independently draws a random count of incoming dummy packets bounded by N_s; each side also draws a random padding-window width from a uniform distribution bounded by W_min and W_max. Each side schedules its dummy packets by sampling arrival times from a Rayleigh distribution with that side's padding-window width as its scale parameter, which concentrates roughly 40% of dummy packets within the first window-width of the trace and tapers the rest, producing a front-loaded burst without a hard cutoff. Because the packet count and window width are redrawn independently for every trace of the same webpage, repeated visits to the same page produce traces with different total lengths and different packet-order patterns, defeating a classifier trained on defended traces. GLUE targets a different attacker step: before running any per-page classifier, the attacker must first segment a continuous traffic stream into per-page traces (find where one page-load ends and the next begins). GLUE inserts dummy "glue traces" between consecutive real page loads so a sequence of separately visited pages appears to the eavesdropper as one long, undivided trace; an attacker must first solve "split decision" (does this stream contain multiple pages at all) and "split finding" (where are the boundaries) before any per-page WF classifier can even run. GLUE also incorporates FRONT noise on the first page of each glued sequence, because the paper found GLUE alone leaves the first page's front insufficiently obscured.

### Measured results
Dataset DS-19, collected by the authors between February and April 2019 using Tor Browser 8.5a7 on Tor 0.4.0.1-alpha, driven by automated command-line browsing on one machine on a university network: Alexa top 100 websites, 100 visits each, as monitored pages, plus 10,000 other pages (after filtering pages that failed to load through Tor) as non-monitored pages. All FRONT results below use open-world evaluation with r = 10 (client visits one monitored page for every ten non-monitored pages) and 10-fold cross-validation, with true/wrong/false positives summed across folds before computing True Positive Rate (TPR), Wrong Positive Rate, False Positive Rate, precision, and F1.

Defense overhead (Table 3), against a no-defense baseline of 0% latency and 0% data overhead:

| Defense | Parameters | Latency overhead | Data overhead |
|---|---|---|---|
| Tamaraw | rho_out=0.04, rho_in=0.012, L=50 | 78.43% | 162.93% |
| WTF-PAD | Normal rcv histogram | 0% | 32.71% |
| FT-1 (FRONT) | N_s = N_c = 1700, W_min = 1s, W_max = 14s | 0% | 33.01% |
| FT-2 (FRONT) | N_s = N_c = 2500, W_min = 1s, W_max = 14s | 0% | 48.80% |

F1 score (lower is a more effective defense) on DS-19, by attack (Table 4), against four published attacks: kNN, CUMUL, kFP (k-fingerprinting), and DF (Deep Fingerprinting), with DF's maximum trace length raised to 10,000 (from the 5,000 the DF paper recommends) to accommodate FRONT's dummy packets:

| Defense | kNN F1 | CUMUL F1 | kFP F1 | DF F1 |
|---|---|---|---|---|
| No defense | 0.86 | 0.76 | 0.93 | 0.94 |
| Tamaraw | 0.028 | 0.052 | 0.038 | 0.11 |
| WTF-PAD (33% data overhead) | 0.16 | 0.28 | 0.61 | 0.70 |
| FT-1, similar overhead to WTF-PAD | 0.048 | 0.18 | 0.54 | 0.47 |
| FT-2, 49% data overhead | 0.016 | 0.13 | 0.46 | 0.40 |

At matched data overhead against WTF-PAD, FT-1 lowers F1 against every one of the four attacks; against DF specifically, FT-1's F1 (0.47) is roughly two-thirds of WTF-PAD's (0.70).

Mechanism-level comparison against WTF-PAD, same DS-19 dataset: WTF-PAD spends 24% of its dummy-packet budget in the first quarter of a trace and 49% in the first half; FRONT spends 40% in the first quarter and 69% in the first half. The median coefficient of variation of dummy-packet counts injected per webpage class is 42% for FRONT versus 36% for WTF-PAD.

Recall of the kFP attack against FRONT-defended traces by webpage-size quartile (four groups of Alexa-top-100 pages divided by packet count, ranging up to 2039, 4368, 6611, and 28,199 packets per quartile): 24%, 24%, 35%, and 54% respectively; a tenfold increase in webpage size (quartile 1 to quartile 4) raises kFP's recall by 30 percentage points.

GLUE evaluation, same DS-19 dataset split into ATTACK_TRAIN (9,000 instances), SPLIT_TRAIN (2,000 instances), and EVALUATION (9,000 instances), FRONT noise set to N_s = N_c = 1100, glue-trace maximum duration d_max drawn from U(10s, 15s), inter-page dwell time drawn from U(1s, 10s), non-monitored-to-monitored page visit ratio 10:1. Two attacker conditions: told the true number of glued pages l directly ("without split decision"), or required to find l itself ("with split decision").

Without split decision, on undefended (no-GLUE) l-traces, the strongest attack (kFP) achieves 96% TPR and 97% precision at l=2, falling to 82% TPR and 82% precision at l=16. Against GLUE-defended traces, all four attacks fall below 5% TPR by l=16; DF is the best attack at l=2 with 54% TPR, then weakens quickly as l grows. With split decision required, all attacks perform worse than without it, falling below 1% precision by l=16; on undefended traces with split decision required, kFP still achieves 45%-75% TPR and 41%-77% precision across the same l range, since the paper's split-finding procedure exceeds 92% accuracy.

GLUE data overhead (Figure 12), computed from an average webpage load time d_P = 27.30 seconds measured on DS-19, under three assumed client dwell-time distributions: strict (dwell mean d_G = 2.5s, tail mean d_L = 5s) gives 3%-13% overhead depending on l; normal (d_G = 5.5s, d_L = 12.5s) gives 22%-44%; lenient (d_G = 10s, d_L = 20s) gives 35%-53%. Larger l (more pages glued together) reduces overhead within each setting. Measured overhead runs about 5-10 percentage points below the paper's closed-form overhead formula, attributed to uneven bandwidth density in real glue traces.

Impact of removing FRONT noise from the first page of a glued sequence (same l=2 to l=16 setting): with FRONT noise present, all four attacks achieve 20%-60% TPR on the first page; with FRONT noise removed, the same attacks achieve 40%-80% TPR on the first page.

### Parameters
- N_c, N_s (FRONT): client and proxy dummy-packet budgets; tested at N_c=N_s=1700 (FT-1, matched to WTF-PAD's ~33% overhead) and N_c=N_s=2500 (FT-2, 49% overhead); GLUE evaluation used N_c=N_s=1100.
- W_min, W_max (FRONT): padding-window bounds; both FT-1 and FT-2 use W_min=1s, W_max=14s. Appendix A (not extracted here in full) discusses tuning these.
- Rayleigh distribution scale parameter w: set per-trace to the sampled window width w_c (client) or w_s (proxy); about 40% of dummy packets fall within [0, w] by construction (closed-form: integral of the Rayleigh probability density from 0 to w equals ~0.40).
- l (GLUE): number of real pages glued into one apparent trace; evaluated across the range 2 to 16.
- d_max (GLUE): maximum glue-trace duration, drawn from U(10s, 15s) in the main evaluation.
- r (open-world precision definition): ratio of non-monitored to monitored page visits by the client; set to 10 for the FRONT evaluation ("a client that visits one monitored webpage for every ten non-monitored webpages").
- Attack parameters: kNN, kFP, and DF use each attack's own paper-suggested parameters, except DF's maximum trace length is raised from 5,000 to 10,000 to accommodate FRONT's added dummy packets; CUMUL's Support Vector Machine (SVM) parameters are tuned by the authors following CUMUL's own paper's procedure.

### Stated limitations
The paper states FRONT's performance was not sensitive to dataset age (tested on two datasets collected five years apart) or to page-size subsetting, except that it performed worse on very large webpages (consistent with the quartile-recall result above). The paper states it did not explore whether a client's own poor network conditions (where the client's link, not Tor, is the bottleneck) degrade FRONT's effectiveness, and states building FRONT to self-adjust to such conditions is left as future work. For GLUE, the paper states it evaluated an attacker with complete knowledge of the entire database of glue traces, and states it cannot prove that an attacker who instead pursues a strategy of directly detecting glue traces in the client's stream must fail; it offers three specific reasons that attack is difficult (network jitter perturbing scheduled glue-trace timestamps, glue traces being cut off early when the client resumes browsing, and glue traces being drawn from a population meant to resemble real page loads) but leaves the question of whether glue-trace detection is possible as open future work. The paper states it did not design FRONT or GLUE to provide a guarantee against all future attacks, contrasting this with Tamaraw's stronger (but far more expensive) property; it states it cannot prove that its "split decision" and "split finding" problems, which GLUE relies on being hard, are unsolvable in general. The paper proposes but does not implement or measure one deployment component: it proposes that Tor directory servers maintain and distribute large databases of glue traces for clients to draw from, and states only informally ("quite low") that the resulting distribution cost is acceptable, without a measured figure; it separately proposes, without evaluating, an on-the-fly client-side glue-trace generation alternative to eliminate that distribution cost.

### Requirements it places on the rest of the system
Both defenses require a cooperating relay to run the defense logic jointly with the client; the paper specifies this must be the middle node of a three-hop Tor circuit, not the entry or exit node, because the entry node is the position the adversary is assumed to occupy and the exit node and web server must see undefended traffic (the middle node strips dummy packets before forwarding onward). The threat model assumes a purely passive eavesdropper that observes but does not delay, modify, or drop packets; the paper does not evaluate either defense against an active adversary. GLUE's protection depends on the client's own browsing behavior: the number of pages glued (l) and the resulting overhead are functions of how long the client dwells between page loads, so a system deploying GLUE has no fixed overhead figure to budget against and instead exposes a client-controllable range (3% to 53% in the paper's three tested dwell-time regimes). GLUE's proposed production deployment requires an additional infrastructure component not built or measured in this paper: a directory-server-hosted store of pre-generated glue traces that clients download from, which becomes a new object other components must serve, keep available, and refresh. FRONT requires the client and the cooperating proxy to independently and correctly instantiate the same Rayleigh-distribution sampling and the same discrete-uniform packet-count sampling procedure using their own local randomness; the two sides do not coordinate a shared random seed, since the padding schemes for the two directions are described as generated independently.

### Contradicts
None found among papers currently in this corpus. The paper's own comparison contradicts a claim, sometimes made informally elsewhere, that WTF-PAD adequately defends Tor against modern classifiers: Table 4 measures WTF-PAD leaving kFP and DF at 0.61 and 0.70 F1 respectively, effectiveness the paper characterizes as remaining high for those two attacks despite WTF-PAD's overhead.

### References worth retrieving
- competing: M. Juarez, M. Imani, M. Perry, C. Diaz, M. Wright. "Toward an Efficient Website Fingerprinting Defense" (WTF-PAD), ESORICS 2016 — the direct lightweight-defense baseline FRONT is compared against throughout.
- competing: X. Cai, R. Nithyanand, T. Wang, R. Johnson, I. Goldberg. "A Systematic Approach to Developing and Evaluating Website Fingerprinting Defenses" (Tamaraw), ACM CCS 2014 — the heavyweight regularization baseline compared against in Table 3 and Table 4.
- attack: P. Sirinam, M. Imani, M. Juarez, M. Wright. "Deep Fingerprinting: Undermining Website Fingerprinting Defenses with Deep Learning" (DF), ACM CCS 2018 — the strongest attack used throughout the evaluation; described as having defeated WTF-PAD.
- attack: J. Hayes, G. Danezis. "k-fingerprinting: A Robust Scalable Website Fingerprinting Technique" (kFP), USENIX Security 2016 — one of the four benchmark attacks.
- attack: A. Panchenko et al. "Website Fingerprinting at Internet Scale" (CUMUL), NDSS 2016 — one of the four benchmark attacks.
- foundational: P. Syverson, R. Dingledine, N. Mathewson. "Tor: The Second Generation Onion Router," USENIX Security 2004 — the onion-routing network both defenses are deployed on; already in this corpus as DINGLEDINE-USENIXSEC-04.
- competing: X. Wang, I. Goldberg. "Walkie-Talkie" as introduced by Wang and Goldberg, 2017 — a confusion-category defense using half-duplex browser communication, requiring client knowledge of webpage sizes, contrasted against FRONT's no-extra-infrastructure design in Table 1.
- attack: K. P. Dyer, S. E. Coull, T. Ristenpart, T. Shrimpton. "Peek-a-Boo, I Still See You: Why Efficient Traffic Analysis Countermeasures Fail" (introduces BuFLO), IEEE S&P 2012 — foundational regularization-defense analysis Table 1 compares against.

### Verbatim extracts
- "FRONT outperforms the best known lightweight defense, WTF-PAD" (abstract).
- "Both defenses have no latency overhead" (abstract).
- "expect 40% of the dummy packets to lie in the time interval [0, w]."
- "FRONT uses 40% of its budget in the first quarter and 69% in the first half."
- "all attacks achieve less than 5% TPR" (GLUE at l = 16, without split decision).
- "the data overhead of GLUE is...3% to 13%...22% to 44%...35% to 53%."
- "We did not explore this situation; making FRONT automatically self-adjusting...is a potential future direction."
- "we cannot prove the impossibility of identifying glue traces in traffic, we leave the question open as future work."
