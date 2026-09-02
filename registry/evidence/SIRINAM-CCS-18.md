## [SIRINAM-CCS-18] Deep Fingerprinting: Undermining Website Fingerprinting Defenses with Deep Learning
**Citation:** Payap Sirinam, Mohsen Imani, Marc Juarez, Matthew Wright. "Deep Fingerprinting: Undermining Website Fingerprinting Defenses with Deep Learning." ACM CCS, 2018. DOI 10.1145/3243734.3243768.
**Retrieved:** full text via https://arxiv.org/abs/1801.02265
**Source URL:** https://arxiv.org/abs/1801.02265
**Domain:** G

### What it does
Deep Fingerprinting (DF) identifies which website a Tor user is visiting by analyzing the pattern of encrypted packet timing and direction on the link between the user and Tor's entry node, without decrypting any traffic. The adversary is local (observes only that one link, for example an internet service provider (ISP) or a local network eavesdropper) and passive (records but does not modify, delay, or drop packets). DF represents each observed connection as a fixed-length sequence of packet directions (5,000 cells long, the input length the paper found gives the best classification accuracy) and feeds that sequence into a convolutional neural network (CNN), a deep-learning architecture that scans a signal with learned filters to detect local patterns regardless of where in the sequence they occur. The DF architecture uses four convolutional blocks with a mix of ELU and ReLU activation functions, max pooling (rather than average pooling), two fully connected layers, batch normalization after every convolutional and fully connected layer, and dropout regularization tuned to different rates at different depths (0.1 after pooling layers, 0.7 and 0.5 after the two fully connected layers) — all more numerous and more heavily regularized than the prior CNN-based automated website fingerprinting (AWF) model by Rimmer et al. The full hyperparameter search space and final selected values are given in the paper's Table 1. In the open-world evaluation, the classifier outputs a probability for each monitored site; if the highest probability exceeds a chosen threshold and belongs to a monitored site, the trace is classified as a visit to that site, otherwise it is classified as unmonitored, with the threshold tunable to trade precision against recall.

### Measured results
| Result | Value | Conditions |
|---|---|---|
| Closed-world accuracy, undefended traffic, DF vs. prior attacks | DF 98.3%; k-fingerprinting (k-FP) 95.5%; CUMUL 97.3%; k-nearest-neighbors (k-NN) 95.0%; AWF 94.9%; stacked denoising autoencoder (SDAE) 92.3% | closed-world dataset of 95 sites with 1,000 visits each (Alexa top 100 minus discarded sites), k-fold cross-validation, tor-browser-crawler used to drive Tor Browser |
| Closed-world accuracy against defenses (Table 3) | BuFLO: DF 12.6%, SDAE 9.2%, AWF 11.7%, k-NN 10.4%, CUMUL 13.5%, k-FP 13.1%, at 246% bandwidth / 137% latency overhead. Tamaraw: DF 11.8%, SDAE 11.8%, AWF 12.9%, k-NN 9.7%, CUMUL 16.8%, k-FP 11.0%, at 328% bandwidth / 242% latency overhead. WTF-PAD: DF 90.7%, SDAE 36.9%, AWF 60.8%, k-NN 16.0%, CUMUL 60.3%, k-FP 69.0%, at 64% bandwidth / 0% latency overhead. Walkie-Talkie (W-T): DF 49.7%, SDAE 23.1%, AWF 45.8%, k-NN 20.2%, CUMUL 38.4%, k-FP 7.0%, at 31% bandwidth / 34% latency overhead | closed-world dataset, WTF-PAD and BuFLO/Tamaraw simulated by author-provided scripts, Walkie-Talkie collected via a real half-duplex crawl using a modified Tor Browser Bundle 7.0.6 |
| Impact of dataset size on closed-world accuracy | DF and CUMUL reach 90% accuracy with 50 training traces per site; k-NN, k-FP and AWF need 250 traces to reach 90%; SDAE needs 750 traces; accuracy for all but SDAE saturates after 550 traces | closed-world dataset, non-defended traffic |
| GPU training time (30 epochs) | SDAE 16 minutes (13 pre-training + 3 fine-tuning); DF 64 minutes; AWF 4 minutes | NVIDIA GTX 1070 GPU, 8 GB memory |
| CPU-only training time | SDAE 96 minutes; DF approximately 10 hours; AWF 1 hour; k-NN 12.5 hours; CUMUL 57 hours (parallelized, 4 processes); k-FP 1 hour | no GPU acceleration |
| Open-world results, non-defended traffic, standard model | DF 0.957 true positive rate (TPR) / 0.007 false positive rate (FPR) at 20,000 unmonitored training sites; overall 0.99 precision / 0.94 recall | training set 85,500 monitored traces (900 instances x 95 sites), unmonitored training sites varied 900 to 20,000, test set 9,500 monitored traces + 20,000 unmonitored traces (disjoint from training unmonitored set) |
| Open-world results, WTF-PAD-defended traffic, standard model | DF: precision 0.96 / recall 0.68 when tuned for high precision; 0.67 precision / 0.96 recall when tuned for high recall (reported elsewhere in the paper as 0.95 precision / 0.70 recall) | training set 91,000 monitored traces (910 instances x 100 sites), test set 9,000 monitored traces + 20,000 unmonitored traces |
| Open-world results, W-T-defended traffic | precision below 0.36 across all thresholds tested | same open-world dataset construction as the WTF-PAD open-world evaluation |
| Closed-world Top-2 accuracy against symmetric-collision W-T | 98.44% | closed-world W-T dataset, DF classifier |
| Closed-world DF accuracy against W-T under an asymmetric-collision implementation (guideline violation) | 87.2%, compared to 49.7% under correct symmetric collisions | same closed-world W-T dataset, defense implemented without pairing decoy sites symmetrically |
| Open-world DF results when 10% of users violate W-T's symmetric-collision guideline | TPR 0.85 / FPR 0.23, compared to TPR 0.80 / FPR 0.76 when all users comply | open-world W-T dataset |
| ROC operating points, DF vs. non-defended traffic | 0.98 TPR at 0.03 FPR (tuned for high TPR); 0.94 TPR at 0.004 FPR (tuned for low FPR) | open-world dataset, standard model |

### Parameters
| Parameter | Value used | Range / search space tested |
|---|---|---|
| Input dimension (sequence length in Tor cells) | 5,000 | search range 500-7,000 |
| Optimizer | Adamax | candidates: Adam, Adamax, RMSProp, SGD |
| Learning rate | 0.002 | search range 0.001-0.01 |
| Training epochs | 30 | search range 10-50 |
| Mini-batch size | 128 | search range 16-256 |
| Filter/pool/stride sizes | [8, 8, 4] | search range 2-16 |
| Activation functions | ELU (first two convolutional layers), ReLU (rest) | candidates: Tanh, ReLU, ELU |
| Number of filters per convolutional block | Block 1: [32,32]; Block 2: [64,64]; Block 3: [128,128]; Block 4: [256,256] | search ranges [8-64], [32-128], [64-256], [128-512] respectively |
| Pooling type | Max | candidates: Average, Max |
| Number of fully connected layers | 2 | search range 1-4 |
| Hidden units per fully connected layer | [512, 512] | search range 256-2048 |
| Dropout rates | pooling layers 0.1; FC1 0.7; FC2 0.5 | search range 0.1-0.8 |
| k in k-NN and k-FP open-world evaluation | 6 | tested k=2 to 10; TPR/FPR did not change significantly above k=5 |
| Closed-world dataset size | 95 sites, 1,000 visits each, minimum 1,000 visits retained per site | -- |
| Open-world dataset size | 40,716 traffic traces, Alexa top 50,000 excluding the closed-world top 100 | -- |

### Stated limitations
The paper states that the crawler models a simplistic sequential visiting pattern (round-robin batched visits), not real user browsing behavior, because modeling actual Tor user behavior is not possible given that Tor collects no user statistics for privacy reasons; it notes virtually all prior website fingerprinting (WF) datasets share this limitation. Data collected for training becomes stale: the paper cites that accuracy of WF attacks degrades significantly after 10-14 days of data age (attributing this measurement to Wang and Goldberg and to Juarez et al., not measuring it itself in this paper). Attack cost is nontrivial: collecting a large dataset requires multiple machines running for several days, which the paper states as a practical barrier for a weaker attacker. Traffic parsing (isolating one page-load's packets from concurrent Tor activity) is assumed already solved, following prior work's same assumption. The paper states that improving open-world classification via deeper architectures, more training data, or added timing features is left unexplored. It states that a semi-open-world targeted attack using auxiliary user profile information (for example, known language) is a possible extension not implemented here. Adversarial-machine-learning-based defenses are noted as a promising but unimplemented direction, complicated because Tor traffic streams live (the defender cannot see the full trace in advance) and Tor's transformation options are restricted to adding or delaying packets, not deleting or speeding them up.

### Requirements it places on the rest of the system
DF requires a labeled training dataset of traffic traces for every site the attacker wants classified in the monitored set, collected either from the same defense configuration the target will use or from data the attacker deliberately gathers under that defense; the closed-world evaluation retrains DF separately on defended and undefended datasets, so a defense's evaluation must specify whether the classifier was retrained on defended traffic. It requires the attacker to control the traffic-parsing step, either by running a Tor entry node (selecting a domain's traffic by its Tor circuit ID) or by using packet-parsing techniques on multiplexed Transport Layer Security (TLS) traffic; both cases are assumed solved, not built by this paper. It requires GPU or substantial CPU time for training (single-digit hours on a consumer GPU, roughly 10 hours without one), which any defense evaluation must account for as attacker overhead when comparing against classifiers with lower training cost such as k-FP. The open-world precision/recall interpretation requires an unmonitored-to-monitored traffic ratio consistent with the paper's own construction (more than two orders of magnitude); a differently structured base-rate assumption changes what precision and recall mean operationally, since the paper explicitly ties precision usefulness to avoiding the base-rate fallacy under a heavily imbalanced monitored/unmonitored split.

### Contradicts
The paper's own results (Table 3, closed-world) directly contradict a claim that WTF-PAD is an effective defense against a modern deep-learning classifier: DF reaches 90.7% accuracy against WTF-PAD, versus the much lower accuracy WTF-PAD was reported to hold prior non-deep-learning attacks to. The paper's discussion section states that Walkie-Talkie's own claimed effectiveness (bounded near 50% accuracy for symmetric collisions) depends on strict client-side adherence to symmetric decoy pairing; the paper's own asymmetric-collision experiment shows accuracy jumping to 87.2% (closed-world) or TPR 0.85/FPR 0.23 (open-world, 10% non-compliance) when that assumption is violated, so any claim that Walkie-Talkie's protection holds independent of implementation compliance is not supported by this paper. WANG-USENIXSEC-14 in this batch is the source of the k-NN attack and the BuFLO/Tamaraw-class provable defense referenced in this paper's Table 2 and Table 3 comparisons — it is not the Walkie-Talkie paper (Wang and Goldberg 2017, cited by Sirinam et al. as reference [41], distinct from reference [38] which is WANG-USENIXSEC-14).

### References worth retrieving
- Foundational: V. Rimmer, D. Preuveneers, M. Juarez, T. Van Goethem, W. Joosen, "Automated website fingerprinting through deep learning" (AWF paper, cited as [31]) — the direct architectural baseline this paper builds on and outperforms.
- Foundational: T. Wang, X. Cai, R. Nithyanand, R. Johnson, I. Goldberg, "Effective Attacks and Provable Defenses for Website Fingerprinting," USENIX Security 2014 (cited as [38]; = WANG-USENIXSEC-14 in this batch — the k-NN attack).
- Competing: T. Wang, I. Goldberg, "Walkie-talkie: An efficient defense against passive website fingerprinting attacks," USENIX Security 2017 (cited as [41]; the actual Walkie-Talkie paper, distinct from [38]).
- Competing: A. Panchenko, F. Lanze, A. Zinnen, M. Henze, J. Pennekamp, K. Wehrle, T. Engel, "Website fingerprinting at internet scale" (CUMUL, cited as [27]).
- Competing: J. Hayes, G. Danezis, "k-fingerprinting: A robust scalable website fingerprinting technique," USENIX Security 2016 (cited as [14]).
- Competing: K. P. Dyer, S. E. Coull, T. Ristenpart, T. Shrimpton, "Peek-a-Boo, I Still See You" (BuFLO, cited as [12]).
- Competing: X. Cai, R. Nithyanand, T. Wang, R. Johnson, I. Goldberg, "A systematic approach to developing and evaluating website fingerprinting defenses" (Tamaraw, cited as [7]).
- Competing: M. Juarez, M. Imani, M. Perry, C. Diaz, M. Wright, "Toward an Efficient Website Fingerprinting Defense" (WTF-PAD, cited as [20]).
- Foundational: K. Abe, S. Goto, "Fingerprinting attack on Tor anonymity using deep learning," 2016 (cited as [3]; earlier deep-learning WF attack, achieved 89% in this paper's own reimplementation).
- Attack/critique: R. Schuster, V. Shmatikov, E. Tromer, "Beauty and the Burst," 2017 (cited as [32]; encrypted-video traffic fingerprinting, adjacent attack class).

### Verbatim extracts
- "The DF attack attains over 98% accuracy on Tor traffic without defenses"
- "it is also the only attack that is effective against WTF-PAD with over 90% accuracy"
- "Walkie-Talkie remains effective, holding the attack to just 49.7% accuracy"
- "With just 50 traces per site, both DF and CUMUL achieve 90% accuracy"
- "the DF attack is much more accurate at 87.2%, compared to 49.7% with symmetric collisions"
- "DF can still detect patterns that remain after WTF-PAD is applied"
- "Addressing these challenges would be interesting for future work"
